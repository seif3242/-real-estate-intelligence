# WhatsApp Web Authentication (Milestone 2)

This document explains how to link the Collector to a WhatsApp account for
the first time, and how that session is reused afterwards. It covers only
the connection layer — opening groups, reading messages, AI parsing, and
PDF processing are not implemented yet (see `docs/PROJECT_STRUCTURE.md`).

## How session persistence works

`WhatsAppWebProvider` launches Chromium via Playwright's
`launch_persistent_context(user_data_dir=WHATSAPP_SESSION_PATH)`. WhatsApp
Web's own session/auth data is written into that profile directory by the
browser itself (cookies, IndexedDB, etc.) — the application does not
read or store WhatsApp credentials directly.

- `WHATSAPP_SESSION_PATH` (see `backend/.env.example`) controls where the
  profile is stored. In `docker-compose.yml` this is the named volume
  `whatsapp_session`, mounted at `/data/whatsapp-session`, so it survives
  container restarts and rebuilds.
- On every `connect()` call, the provider opens WhatsApp Web in that
  profile and checks whether the chat list is already visible. If it is,
  the existing session was reused and no QR scan is needed. If it isn't,
  the provider falls back to QR authentication automatically — no
  separate "first run" flag or configuration is required.

## First-time authentication (QR scan)

The Chromium instance runs headless (this is meant to run on a server),
so the QR code can't be viewed on a connected screen. Instead, the
provider screenshots the QR code to a file you scan from your own
machine.

1. Make sure `WHATSAPP_SESSION_PATH` exists and is writable (in Docker
   this is the `whatsapp_session` volume; locally it can be any path,
   e.g. `/tmp/whatsapp-session`).
2. Run the bootstrap script, which authenticates and then lists groups
   as a smoke test:
   - Locally: `cd backend && .venv/bin/python -m app.collector.cli`
   - In Docker: `docker compose exec backend python -m app.collector.cli`
3. The script logs a line like:
   ```
   Scan the QR code at /data/whatsapp-session/qr.png with WhatsApp > Linked Devices within 117s to authenticate.
   ```
   Copy that file to a machine where you can view images (e.g.
   `docker compose cp backend:/data/whatsapp-session/qr.png ./qr.png`),
   open it, and scan it from your phone: **WhatsApp → Settings → Linked
   Devices → Link a Device**.
4. Once scanned, the provider detects the logged-in chat list and the
   script prints the discovered group names. The QR code expires after
   120 seconds (`QR_LOGIN_TIMEOUT_SECONDS` in `whatsapp_web.py`); if it
   times out, a `QrLoginTimeoutError` is raised — just re-run the script
   and scan the newly captured QR code.

## Reusing the session after a restart

No manual step is needed. Because the browser profile (and therefore the
WhatsApp Web login) lives in `WHATSAPP_SESSION_PATH`, any subsequent
`connect()` — whether from the CLI script, the API, or after restarting
the `backend` container — reuses it automatically as long as the session
hasn't been invalidated (e.g. unlinked from the phone, or expired). If it
has been invalidated, `connect()` falls back to the QR flow described
above the same way it did the first time.

## Verifying session validity

`is_connected()` doesn't just check that a browser is open — it actually
checks WhatsApp Web's live DOM for the logged-in chat list. `maintain_session()`
calls this and raises `ConnectionLostError` if the session is no longer
valid, which is what callers (the CLI script, the API endpoint, or the
future Queue) should react to.

## Listing groups

`GET /collector/groups` returns the group chat names visible to the
connected account:

```bash
curl http://localhost:8000/collector/groups
```

- Returns `200` with a JSON array of group names if connected.
- Returns `503` if the provider isn't connected or the QR code wasn't
  scanned in time — run the CLI bootstrap script above first.

This endpoint does not open any group, read any messages, or write
anything to the database — it only enumerates names already visible in
the chat list sidebar.

### How groups are reliably distinguished from one-on-one chats

WhatsApp Web's rendered DOM does not expose a chat's type anywhere —
there is no attribute on a chat row that says "this is a group". The
only DOM-visible cue is a default "group" icon shown for chats without a
custom photo, which means **any DOM-only heuristic has a structural blind
spot**: groups with a custom photo are indistinguishable from individual
chats by appearance alone. This is a genuine limitation of WhatsApp Web
itself, not a tuning problem, so `WhatsAppWebProvider` does not use the
DOM for group detection at all.

Instead, `list_groups()` reads WhatsApp Web's own internal chat model.
WhatsApp Web bundles its JS into webpack chunks exposed via a
`window.webpackChunk*` array. By pushing a synthetic chunk onto that
array, the provider obtains a working `require()` and locates the
module exporting the live `Chat` collection (`Chat.getModelsArray()`).
Each chat there carries its real JID, and `id.server` is `"g.us"` for
groups and `"c.us"`/`"s.whatsapp.net"` for individuals — this is
WhatsApp's own data, not a visual inference, so it is correct regardless
of custom photos. This is the same technique mature unofficial WhatsApp
Web automation libraries (e.g. `whatsapp-web.js`) use for the same
reason.

**Remaining risk**: this still relies on WhatsApp Web's unofficial,
undocumented internal module structure, which WhatsApp can change at any
time without notice (e.g. a frontend rewrite that changes how chunks are
bundled). If the chat store can't be located, `list_groups()` raises
`GroupListingUnavailableError` rather than silently returning an empty
or partial list — per Engineering Rules, failures must surface loudly,
never be swallowed into a misleadingly "successful" empty result.

**Production-grade long-term solution**: the durable fix is to stop
depending on WhatsApp Web's unofficial internals entirely and migrate to
the official [WhatsApp Business Platform Cloud API](https://developers.facebook.com/docs/whatsapp),
which exposes group/contact metadata through a stable, documented,
Meta-supported API instead of reverse-engineered browser automation.
Because `WhatsAppProvider` is already an abstraction (System Design
§2.2), this would mean adding a new `WhatsAppCloudApiProvider`
implementation behind the same interface — no changes required to
`CollectorService`, the API endpoint, or any other caller. This is
recommended as the next infrastructure investment once the business
requires guarantees this unofficial approach cannot make.
