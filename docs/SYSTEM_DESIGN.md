# System Design — Version 1.1

> **Changelog from v1.0:** Replaced AI-generated SQL with a function-calling Knowledge Engine (AI never writes/executes SQL); unified message taxonomy with the PRD; added a content-hashing/dedup step before any AI call; added a `WhatsApp_Groups` entity and onboarding flow; added confidence scoring and a correction audit trail to the schema; defined FK lifecycle between expiring raw messages and permanent structured data; restricted V1 to text + PDF (no image/voice/video processing); abstracted the WhatsApp Collector behind a Provider Interface; notifications routed through Dashboard (and future Email) only — never WhatsApp; removed multi-user/tenant scaffolding from the schema by design.

---

## 1. Overall Architecture

```
                        WhatsApp Web (current provider)
                              │
                              ▼
                 WhatsApp Provider Interface
                              │
                              ▼
                    WhatsApp Collector (adapter)
                              │
                              ▼
                  Content Hash / Duplicate Check
                              │
                              ▼
                     Message Processing Queue
                              │
                  ┌───────────┴───────────┐
                  ▼                       ▼
            AI Text Parser           PDF Processor
                  │                       │
                  └───────────┬───────────┘
                              ▼
                       Knowledge Engine
                  (entity resolution, dedup,
                   change detection, query functions)
                              │
                              ▼
                        PostgreSQL
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
      Dashboard          AI Chat API        Notification Service
   (incl. in-app                              (Dashboard now,
    notifications)                             Email in future)
```

V1 supports **text messages and PDF files only**. Images, voice notes, and videos are not processed by the pipeline — see §2.4 and PRD §5.

---

## 2. WhatsApp Collector

### 2.1 Sole Responsibility

* Open WhatsApp Web (or whichever provider is configured).
* Maintain login/session.
* Read new messages only.
* Download PDF attachments.
* Compute a content hash for each message/attachment (see §3.1) before handing off.
* Send the message (and any PDF) to the Queue.

The Collector must never analyze, classify, or extract information from a message. That is exclusively the Parser/PDF Processor/Knowledge Engine's job.

### 2.2 Provider Interface (Abstraction)

To avoid coupling the rest of the system to WhatsApp Web automation specifically, the Collector is implemented behind a **WhatsApp Provider Interface** with a small, stable contract, conceptually:

* `connect()` — establish/restore a session.
* `read_new_messages()` — return new messages since the last checkpoint.
* `download_attachment(message)` — fetch a PDF (or other supported attachment) for a message.
* `maintain_session()` — keep the session alive; trigger reconnect/backoff on failure.
* `is_connected()` — health check.

The current (V1) implementation of this interface is a Playwright-driven WhatsApp Web adapter. This abstraction exists specifically so that a future migration to another transport (e.g., the official WhatsApp Business Cloud API) only requires a new adapter implementing the same interface — no changes to the Queue, Parser, Knowledge Engine, or anything downstream.

### 2.3 Session Handling

* The session must be stored securely (encrypted at rest), not as plaintext browser-profile files.
* On disconnect, the Collector must reconnect automatically with a backoff/retry policy.
* If reconnection fails repeatedly (session fully invalidated, e.g. requires a fresh QR scan), the Collector must surface this as a notification on the Dashboard so the user knows manual intervention is needed — it must not fail silently.

### 2.4 Content Type Scope (V1)

The Collector only forwards **text messages and PDF attachments** into the pipeline. Messages that contain only images, voice notes, or video are stored as raw messages (for the 30-day window, per §7) but are **not** forwarded to the Parser/PDF Processor — no classification or extraction is attempted on them in V1.

---

## 3. Message Queue

Every collected message lands in the Queue before any AI processing happens. This guarantees that bursts (e.g., 500 messages arriving at once) are buffered and no message is lost, and that downstream processing stages run asynchronously and independently.

### 3.1 Duplicate Detection (Pre-AI)

Before a queued message is dispatched to the AI Parser or PDF Processor:

1. A content hash is computed (already done at collection time, §2.1) over the message text or PDF binary content.
2. The Knowledge Engine is checked for an existing record with the same content hash.
3. If a match exists, the system **reuses the prior extraction result** for the new message (linking the new message to the existing extraction, attributed to its own group/developer) and **does not invoke the AI again**.
4. Only messages/PDFs with no matching hash are dispatched to the AI Parser / PDF Processor.

This step exists specifically to reduce redundant AI API calls for content that is reposted verbatim or near-verbatim across multiple groups.

---

## 4. AI Parser

Reads a text message and:

1. Classifies it into exactly one of the unified taxonomy categories (see PRD §6):
   `Launch, Request, Offer, Commission Update, Price Update, Brochure, News, General Information`
2. Extracts structured data per PRD §7 (Developer, Project Name, Location, Unit Types, Starting Price, Old Price, New Price, Down Payment, Installments, Delivery Date, Commission, Offer Details, Contact Information, Links).
3. Attaches an **AI confidence score** to the classification and to the extraction as a whole (or per field, at minimum per record).
4. Returns "Information Not Available" for any field it isn't confident about, rather than guessing.

The Parser only processes messages belonging to an **onboarded** WhatsApp group (see §6.1) — unmapped groups' messages are stored raw but not classified.

---

## 5. PDF Processor

Any PDF goes through:

* Download
* OCR (only if the PDF itself is image-based/scanned — this is distinct from standalone image attachments, which remain out of scope per §2.4)
* Text Extraction
* AI Summary
* Data Extraction (same field set and confidence-scoring approach as §4)

Then it is linked to the correct developer and project via the Knowledge Engine.

---

## 6. Knowledge Engine

The Knowledge Engine is split into clearly separated responsibilities (rather than one monolithic "brain"), to keep each piece single-purpose:

* **Entity Resolution** — does this Developer/Project already exist, or is this a new one? (matches across language/spelling variants where possible)
* **Duplicate Detection** — is this message a duplicate of something already processed (works together with the pre-AI hash check in §3.1, and also handles near-duplicate cases post-extraction)?
* **Change Detection / Versioning** — has the price or commission changed since the last known value? Is this a new version of an existing brochure?
* **Query Functions** — a fixed, predefined set of parametrized functions that the AI Chat layer can call to answer questions (see §8). These are the *only* way the AI is allowed to read from the database.

### 6.1 Group Onboarding

The Knowledge Engine (via the API, §11) maintains the `WhatsApp_Groups` mapping (group → developer). Messages from a group that has not yet been onboarded are stored as raw messages only; they are not passed to the AI Parser until the group is mapped to a developer or explicitly marked as ignored.

---

## 7. Database

### 7.1 Core Tables

* `WhatsApp_Groups` — group_external_id, group_name, developer_id (nullable until onboarded), is_active, onboarded_at, last_synced_at
* `Developers`
* `Projects`
* `Messages` — raw messages, **purged after 30 days** (see §7.3)
* `Documents` — PDFs; **permanent**
* `Launches`, `Requests`, `Offers` — **permanent**
* `Price_History` — **permanent**, append-only
* `Commission_History` — **permanent**, append-only
* `Extractions` — generic record of an AI extraction result: source content hash, classification, confidence score, raw AI output, linked structured record(s)
* `Extraction_Corrections` — audit trail of manual corrections: extraction_id, field, original_ai_value, corrected_value, corrected_at
* `Notifications` — **permanent** (or time-boxed retention, TBD at implementation time; not required to expire in 30 days like raw messages)
* `Daily_Summaries` — **permanent**

No `user_id`/tenant columns are present anywhere in the schema. This is intentional — V1 is single-user by design (PRD §2), and multi-user support, when scheduled, will be designed as a dedicated migration rather than retrofitted incrementally.

### 7.2 Confidence & Corrections

Every row in `Extractions` (and, by extension, the structured records it produces) carries a confidence score. `Extraction_Corrections` stores user-made edits separately from the original AI output, so the system always retains both "what the AI said" and "what the user corrected it to." A later re-processing pass of the same source content must not overwrite a field that has a recorded manual correction.

### 7.3 Retention & FK Lifecycle

* `Messages` rows are deleted automatically after 30 days.
* Any table that derives permanent data from a message (`Documents`, `Launches`, `Requests`, `Offers`, `Price_History`, `Commission_History`, `Extractions`) must:
  * Use a **nullable** `message_id` foreign key with **`ON DELETE SET NULL`** (never `CASCADE`), and
  * Store any fields needed for display/context as a **denormalized snapshot** (e.g., project name, developer name at time of extraction) so that deleting the source message never degrades the permanent record.

---

## 8. AI Chat

The AI never generates or executes raw SQL. Instead, the chat flow uses **function-calling / tool use**:

```
User Question
      ↓
AI (interprets intent, selects one or more
    predefined Knowledge Engine functions
    and their parameters)
      ↓
Knowledge Engine Query Function
   (parametrized, pre-vetted — e.g.
    get_launches_today(), get_top_commission(date_range),
    compare_projects(project_a, project_b),
    search_projects(filters), get_price_history(project_id))
      ↓
Database (read-only access via the function)
      ↓
Knowledge Engine returns structured results to the AI
      ↓
AI composes the final natural-language answer from those results
      ↓
Answer
```

This guarantees the AI relies on real stored data ("database facts first"), never invents project information, and — critically — never has the ability to construct or run arbitrary SQL against the database. The Knowledge Engine's function surface is the only access path.

---

## 9. Dashboard

Displays:

Today's Summary

Latest Launches

Latest Requests

Latest Offers

Latest PDFs

Price Updates

Commission Updates

**In-app Notifications** (see §10) — the Dashboard is the primary and, in V1, only delivery surface for notifications.

---

## 10. Notification Service

Every morning, generates and delivers a Daily Summary. Also delivers alerts (e.g., a large new Launch) as they occur.

**Delivery channels:**

* **Dashboard (V1)** — the only channel implemented in V1.
* **Email (future)** — allowed future channel, not built in V1.
* **WhatsApp — never.** The Notification Service must not, under any circumstance, send a WhatsApp message. This is consistent with the Collector being strictly read-only across the entire system.

---

## 11. APIs

```
GET  /projects
GET  /developers
GET  /launches
GET  /offers
GET  /requests
GET  /updates
GET  /search
POST /chat
POST /sync

GET  /groups                 -- list known/unmapped WhatsApp groups
POST /groups                 -- onboard a group (map to a developer, or mark ignored)
PUT  /groups/{id}            -- update a group's mapping/status

PUT  /extractions/{id}/correct  -- submit a manual correction to an AI extraction

GET  /dashboard
GET  /notifications
```

---

## 12. Folder Structure

```
real-estate-ai/
  app/
    collector/
      providers/        -- WhatsApp Provider Interface + adapters (e.g. whatsapp_web/)
    parser/
    pdf/
    knowledge/
      query_functions/  -- predefined AI-callable functions (no raw SQL exposure)
    chat/
    dashboard/
    notifications/
    database/
    api/
    models/
    config/
  logs/
  tests/
  docker/
  docs/
  scripts/
```

---

## 13. AI Model Responsibilities

Claude is responsible for:

* Understanding messages (classification per the unified taxonomy).
* Summarizing PDFs.
* Extracting data (with confidence scores).
* Answering questions — exclusively via Knowledge Engine query functions (tool calling).

Claude is **not** responsible for:

* Reading WhatsApp.
* Storing data.
* Search.
* Managing the database.
* **Generating or executing SQL of any kind.**

---

## 14. Security

Read Only.

No Message Sending — ever, on any channel, including notifications.

Encrypted Database.

Daily Backup.

Error Logs.

Single-user, local deployment in V1 — no authentication/multi-user layer is in scope (intentional, see PRD §2 and §20).

---

## 15. Scalability

Today: 100 groups.

Tomorrow: 1000 groups.

No rewrite required — the Provider Interface abstraction (§2.2), async Queue-based processing, and pre-AI duplicate detection (§3.1) are specifically designed to let message volume grow without architectural changes.

---

## 16. Development Order

```
Phase 1   Project Setup
Phase 2   WhatsApp Collector (behind Provider Interface)
Phase 3   Queue + Content Hashing / Duplicate Detection
Phase 4   Parser (unified taxonomy, confidence scoring)
Phase 5   Database (incl. WhatsApp_Groups, Extractions, Extraction_Corrections)
Phase 6   Knowledge Engine (entity resolution, dedup, change detection, query functions)
Phase 7   Chat (function-calling only — no SQL generation)
Phase 8   Dashboard (incl. in-app notifications, manual correction UI)
Phase 9   Notification Service (Dashboard channel; Email scaffolding for future)
Phase 10  Testing
Phase 11  Deployment
```
