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

### Known limitation of group detection

Groups are distinguished from one-on-one chats by checking each chat
row's icon for WhatsApp's default "group" icon (`data-icon="default-group"`
or `default-group-refreshed`). A group that has a **custom photo set**
will not show this icon and will currently be skipped. This is a known
limitation of DOM-based detection without using WhatsApp's internal
JS store; revisit if it proves too lossy in practice.
