# Project Structure

Status: Milestone 1 (project scaffolding, schema, Collector interface). See
`docs/SYSTEM_DESIGN.md` for the architecture this structure implements and
`docs/ENGINEERING_RULES.md` for the conventions enforced within it.

## Top level

```
.
├── backend/            FastAPI application (Python 3.12)
├── frontend/             React + TypeScript application (Vite)
├── docker/               Dockerfiles for backend and frontend images
├── docker-compose.yml    Local/production multi-container orchestration
├── scripts/              Operational scripts (DB backup, etc.)
├── docs/                 PRD, System Design, Engineering Rules, this file
└── .env.example          Root env vars consumed by docker-compose
```

## backend/

```
backend/
├── pyproject.toml        Dependencies, ruff/mypy/pytest config
├── alembic.ini            Alembic entrypoint config
├── .env.example           Backend env vars (DB, WhatsApp provider, AI keys)
├── app/
│   ├── main.py             FastAPI app factory + lifespan; mounts routers
│   ├── config/             Settings (pydantic-settings) and logging setup
│   ├── api/                HTTP routers (only /health in Milestone 1)
│   ├── database/
│   │   ├── base.py          Declarative Base, naming convention, TimestampMixin
│   │   ├── session.py       Async engine/session factory, get_session() dependency
│   │   └── migrations/      Alembic env.py, script template, versions/
│   ├── models/             SQLAlchemy ORM models — one module per entity
│   │                        (developer, project, whatsapp_group, message,
│   │                        extraction, extraction_correction, document,
│   │                        launch, request, offer, price_history,
│   │                        commission_history, notification, daily_summary)
│   │                        plus enums.py (shared taxonomy) and mixins.py
│   │                        (StructuredExtractionMixin shared by
│   │                        Launch/Request/Offer)
│   ├── collector/
│   │   ├── service.py        CollectorService — orchestrates a WhatsAppProvider
│   │   └── providers/
│   │       ├── base.py         WhatsAppProvider ABC + Collected* dataclasses
│   │       │                   (the only contract the rest of the system
│   │       │                   may depend on — System Design §2.2)
│   │       ├── whatsapp_web.py  Playwright-backed implementation
│   │       ├── factory.py       create_provider(settings) — provider selection
│   │       └── exceptions.py    ProviderError and subclasses
│   ├── queue/               Message processing queue — placeholder (Milestone 2+)
│   ├── parser/              AI text parser — placeholder (Milestone 2+)
│   ├── pdf/                 PDF processor — placeholder (Milestone 2+)
│   ├── knowledge/           Knowledge Engine (dedup, query functions) — placeholder
│   ├── chat/                Chat assistant — placeholder (later milestone)
│   ├── dashboard/           Dashboard-specific backend logic — placeholder
│   └── notifications/       Notification delivery — placeholder
└── tests/
    └── unit/                 Unit tests (provider factory, collector service,
                               health endpoint)
```

Modules listed as "placeholder" contain only a docstring stating their future
scope; they exist now so the package layout matches System Design §2 and
later milestones add files in-place rather than restructuring the tree.

## frontend/

```
frontend/
├── package.json           Scripts: dev, build, lint, format, test
├── vite.config.ts          Vite + Vitest (jsdom) configuration
├── .oxlintrc.json           oxlint configuration
├── .prettierrc.json         Prettier configuration
└── src/
    ├── main.tsx              React entrypoint
    ├── App.tsx                Root component (placeholder shell)
    ├── App.test.tsx           Vitest + Testing Library smoke test
    ├── setupTests.ts          jest-dom matchers for Vitest
    ├── pages/                 Route-level views — empty (later milestone)
    ├── components/            Shared UI components — empty (later milestone)
    └── api/                   Backend API client — empty (later milestone)
```

## docker/ and orchestration

```
docker/
├── backend.Dockerfile      python:3.12-slim, installs Playwright + Chromium,
│                            runs as non-root user, HEALTHCHECK on /health
└── frontend.Dockerfile     Multi-stage: node:22-slim build → nginx:1.27-alpine

docker-compose.yml          Services: postgres, backend, frontend.
                             Named volumes: postgres_data, whatsapp_session.
```

## Database migrations

Alembic is configured for autogenerate against `app.models` metadata. The
migration runtime connection uses the sync `psycopg` driver (converted from
the app's async `asyncpg` URL in `migrations/env.py`), since Alembic itself
runs synchronously.

To create and apply migrations locally:

```bash
cd backend
alembic revision --autogenerate -m "<description>"
alembic upgrade head
```

## What is intentionally NOT implemented in Milestone 1

Per the Milestone 1 scope, the following exist only as empty placeholder
packages or are entirely absent, and are out of scope until a later
milestone:

- AI parsing of message text (`app/parser/`)
- PDF processing (`app/pdf/`)
- Knowledge Engine dedup/query logic (`app/knowledge/`)
- Message processing queue logic (`app/queue/`)
- Dashboard backend/frontend (`app/dashboard/`, `frontend/src/pages/`)
- Chat assistant (`app/chat/`)
- Notifications (`app/notifications/`)
- Real WhatsApp message/attachment sync — `WhatsAppWebProvider.read_new_messages`
  and `download_attachment` raise `NotImplementedError` by design; only the
  browser session lifecycle (`connect`/`disconnect`/`is_connected`) is real.
