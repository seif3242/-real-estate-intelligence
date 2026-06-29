# WhatsApp Message Reading (Milestone 3)

This document explains how on-demand message reading works for a single
WhatsApp group. It covers only read-only extraction of a group's most
recent messages — AI parsing/classification, PDF download/analysis,
database writes, deduplication, content hashing, background sync, the
Dashboard, Chat, and Notifications are all out of scope (see
`docs/PROJECT_STRUCTURE.md`).

## What this does

`GET /collector/messages` opens a named group and returns its most recent
messages as plain JSON, with exactly five fields per message:

```bash
curl "http://localhost:8000/collector/messages?group_name=My+Group&limit=50"
```

```json
[
  {
    "sender_name": "John",
    "timestamp": "2024-01-01T00:00:00Z",
    "message_type": "text",
    "message_text": "Hello everyone",
    "pdf_file_name": null
  },
  {
    "sender_name": "Property Bot",
    "timestamp": "2024-01-01T00:05:00Z",
    "message_type": "pdf",
    "message_text": null,
    "pdf_file_name": "brochure.pdf"
  }
]
```

- `group_name` (required) is matched against the group's display name.
- `limit` (optional, default `50`, max `500`) caps how many of the most
  recent messages are returned, oldest first.
- Returns `404` if no group with that name is currently visible.
- Returns `503` if the provider isn't connected, or WhatsApp Web's
  internal chat store couldn't be located (see Known Limitations below).

This is a one-shot read triggered by the request itself — there is no
polling, no background sync, and nothing is written to the database.
PDF attachments are identified by file name only; they are never
downloaded or opened.

## How extraction works

Message reading reuses the same technique introduced in Milestone 2 for
group detection (see `docs/WHATSAPP_AUTHENTICATION.md`), rather than
scraping rendered message bubbles from the DOM:

1. **Locate the chat.** The same webpack-module-store lookup used by
   `list_groups()` finds the live `Chat` collection and matches the
   requested `group_name` against `formattedTitle`/`name`. If no group
   matches, the request fails with `group_not_found`.
2. **Open it.** `chat.setActive(true)` marks the chat as active in
   WhatsApp Web's own internal store — functionally equivalent to a user
   clicking the chat, without simulating any DOM click.
3. **Load enough history.** Each chat already exposes a `msgs`
   collection of its synced messages. If fewer messages are loaded than
   `limit`, the provider calls WhatsApp Web's own
   `chat.loadEarlierMsgs()` — the same function the real UI calls when
   you scroll up — repeatedly (bounded to 20 attempts) until enough
   messages are available or the chat is exhausted (no more older
   messages to load).
4. **Extract and classify.** Each message model is read directly:
   - `sender_name`: `senderObj.pushname || senderObj.formattedName || senderObj.name`,
     falling back to the phone number portion of `author` (e.g.
     `"201111111111"`) if no contact name is known.
   - `timestamp`: the message's `t` field (Unix seconds) converted to
     UTC.
   - `message_type`: `"text"` if `type === "chat"`, `"pdf"` if
     `type === "document"` and `mimetype === "application/pdf"`,
     otherwise `"unsupported"` (images, voice notes, video, stickers,
     non-PDF documents, etc.) — these are still returned, just with
     null text/filename, so the response never crashes or silently
     drops a message because of an unrecognized type.
   - `message_text`: the message body, only for `"text"` messages.
   - `pdf_file_name`: the attachment's file name, only for `"pdf"`
     messages.
5. **Trim to `limit`.** The most recent `limit` messages are returned,
   oldest first.

### Why this avoids the DOM (and how Arabic/English both work)

Milestone 2's group-detection rework already established that DOM-based
heuristics in WhatsApp Web are unreliable (e.g. the old icon-based group
check broke for groups with a custom photo). The same risk applies even
more directly to message text: rendered bubble markup and right-to-left
shaping/bidi reordering for Arabic are exactly the kind of presentation
detail that can vary by layout, theme, or WhatsApp Web version.

Reading `msg.body`, `senderObj.name`, etc. directly from WhatsApp Web's
internal message models sidesteps this entirely — these are plain
Unicode strings independent of how WhatsApp Web chooses to render them.
No special-casing was needed for Arabic text; it round-trips correctly
because nothing in this path depends on rendering at all.

## Known limitations

- **Unofficial internals.** Like group detection, this depends on
  WhatsApp Web's undocumented internal module structure, which can
  change without notice. If the chat store can't be located, the
  request fails loudly with a `503` (`GroupListingUnavailableError`)
  rather than returning an empty or partial result.
- **Sender name fallback.** If the sender has no saved contact name
  visible to this account, `sender_name` falls back to their phone
  number (the JID's user portion). This is WhatsApp Web's own
  limitation — no display name is available to read in that case.
- **Ambiguous group names.** If multiple groups share the exact same
  display name, the first match found is used. WhatsApp Web's own chat
  list has this same ambiguity (display names are not unique
  identifiers); a future milestone could expose the group's internal
  ID instead of relying on name matching if this becomes a problem.
- **Message availability depends on what's synced.** `limit` is a
  request, not a guarantee — if a group has fewer messages than
  requested, or `loadEarlierMsgs()` reports no more are available,
  fewer messages are returned. This mirrors what a user would see
  scrolling up in the real WhatsApp Web UI.
- **Unsupported message types carry no content.** Images, voice notes,
  video, stickers, and non-PDF documents are returned as
  `"unsupported"` with null `message_text`/`pdf_file_name` — this is by
  design (Milestone 3 explicitly excludes AI/PDF analysis), not a bug.
