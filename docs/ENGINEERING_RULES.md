# Engineering Rules & Coding Standards

## Real Estate AI Assistant - Version 1.1

> **Changelog from v1.0:** Added a hard rule against AI-generated/executed SQL; added rules for the WhatsApp Provider Interface abstraction; added rules for content hashing/duplicate detection before AI calls; added rules for confidence scoring and the manual correction workflow; clarified FK lifecycle rules for expiring raw messages vs. permanent structured data; clarified that notifications must never be sent via WhatsApp; reaffirmed no multi-user/tenant scaffolding in V1; scoped V1 processing to text + PDF only.

---

# 1. General Principles

* Always follow the PRD.
* Always follow the System Design.
* Never implement features that are not approved.
* Suggest improvements before implementing them.
* Build for scalability from day one — **within the explicitly approved V1 scope** (see §2.1; this does not mean adding multi-user scaffolding, see §7.6).
* Keep every component independent.

---

# 2. Project Architecture

* Use Modular Architecture.
* Every service must have one responsibility.
* No business logic inside the UI.
* No AI logic inside the WhatsApp Collector.
* No database logic inside the AI layer.
* **The AI layer must never generate or execute raw SQL, under any circumstance.** All AI-to-database interaction happens exclusively through predefined, parametrized Knowledge Engine query functions (function-calling / tool use). If a new kind of question requires data the existing functions can't provide, add a new predefined function — never let the AI construct a query itself.
* The WhatsApp Collector must be implemented behind a **Provider Interface** (see §8.5) so the underlying transport (WhatsApp Web automation today, possibly an official API later) can be swapped without changes to the Queue, Parser, Knowledge Engine, or any other downstream component.

## 2.1 Version 1 Scope Boundary

* V1 processes **text messages and PDF files only**.
* Images, voice notes, and videos must **not** be processed, classified, or extracted from in V1 — code must not be written to attempt this. Messages containing only these media types are stored as raw messages and otherwise ignored by the AI pipeline.
* V1 is **single-user**. Do not add `user_id`, tenant identifiers, or any multi-user scaffolding to the schema or code (see §7.6).

---

# 3. Programming Language

Backend:

Python 3.12+

Frontend:

React + TypeScript

Database:

PostgreSQL

Automation:

Playwright

API:

FastAPI

AI:

Claude API

---

# 4. Folder Rules

Every module must be separated.

Never place all code inside one file.

Maximum file size:

500 lines

Maximum function size:

100 lines

---

# 5. Code Quality

Use:

* Type Hints
* Clean Code
* SOLID Principles
* DRY Principle
* KISS Principle

Avoid duplicated code.

Write reusable components.

---

# 6. Configuration

Never hardcode:

* API Keys
* Database Passwords
* Tokens

Everything must be stored inside:

.env

---

# 7. Database Rules

* Never delete historical data.
* Price changes must create history (Price_History), never overwrite.
* Commission changes must create history (Commission_History), never overwrite.
* Raw messages expire automatically after 30 days.
* PDF files remain permanently.
* All AI extraction results remain permanently, even after the source raw message expires.

## 7.1 WhatsApp Group Onboarding

* A WhatsApp group must be represented in `WhatsApp_Groups` and mapped to a developer (or explicitly marked ignored) before its messages are classified/extracted.
* Messages from a group with no mapping yet are stored raw only — never passed to the AI Parser.

## 7.2 Foreign Key Lifecycle (Expiring vs. Permanent Data)

* Any table holding permanent data that references `Messages` (e.g., `Documents`, `Launches`, `Requests`, `Offers`, `Price_History`, `Commission_History`, `Extractions`) must use a **nullable** `message_id` foreign key with **`ON DELETE SET NULL`**. `CASCADE` is forbidden on this relationship — deleting an expired raw message must never delete permanent structured data.
* These tables must store a denormalized snapshot of any fields needed for display (e.g., project/developer name at extraction time) so context is not lost once the source message is purged.

## 7.3 Content Hashing & Duplicate Detection

* Every message and PDF must be content-hashed at collection time.
* Before any AI call, the system must check for an existing record with a matching content hash and reuse its extraction result instead of invoking the AI again.
* Only genuinely new content hashes may proceed to the AI Parser / PDF Processor.

## 7.4 Confidence Scores

* Every AI extraction record must store a confidence score.
* Fields the AI is not confident about must be stored as "Information Not Available," never guessed.

## 7.5 Manual Corrections

* The system must support storing user-made corrections to AI extractions, separately from the original AI output (`Extraction_Corrections` or equivalent).
* A later automated re-processing pass of the same source content must never overwrite a field that has a recorded manual correction.

## 7.6 No Multi-User Scaffolding in V1

* Do not add `user_id`, tenant IDs, or per-user partitioning to any table or query in V1. The system is single-user by design. Multi-user support is a tracked Future Feature and will be implemented as a dedicated, deliberate migration — not introduced piecemeal now.

---

# 8. WhatsApp Rules

* Collector must be Read Only.
* Never send messages.
* Never edit messages.
* Never delete messages.
* Collector only reads new messages.
* Collector stores session securely (encrypted at rest, not plaintext).
* If WhatsApp disconnects: reconnect automatically, with a backoff/retry policy.
* If reconnection fails repeatedly (e.g., session invalidated, requires re-authentication), surface this as a Dashboard notification — never fail silently.
* Collector only forwards **text messages and PDF attachments** into the processing pipeline (see §2.1). Images, voice notes, and video attachments are not downloaded/processed for extraction purposes in V1.

## 8.5 Provider Interface

* The Collector must be implemented against a Provider Interface (`connect`, `read_new_messages`, `download_attachment`, `maintain_session`, `is_connected`, or equivalent) rather than calling WhatsApp Web automation directly from the rest of the system.
* All Playwright-specific logic lives inside the current provider adapter implementation, isolated from the Queue/Parser/Knowledge Engine.

---

# 9. AI Rules

AI should:

* Classify messages (using the unified taxonomy — see PRD §6 / System Design §4: Launch, Request, Offer, Commission Update, Price Update, Brochure, News, General Information).
* Extract information.
* Summarize PDFs.
* Answer questions.

AI must NEVER guess.

If information is missing:

Return "Information Not Available".

**AI must never generate or execute SQL, or any other direct database query language/command, under any circumstance.** All database reads required to answer a question happen through predefined Knowledge Engine query functions (function-calling).

Every AI classification/extraction must include a confidence score (see §7.4).

Before invoking the AI on a message or PDF, the system must perform the content-hash duplicate check (see §7.3) and skip the AI call if a match is found.

---

# 10. API Rules

All APIs must:

Return JSON.

Use proper HTTP Status Codes.

Include validation.

Include error handling.

Include documentation.

---

# 11. Logging

Every important action must be logged.

Examples:

Login

WhatsApp Sync

WhatsApp Group Onboarding

PDF Processing

AI Errors

Database Errors

API Errors

Manual Corrections

---

# 12. Error Handling

Application must never crash.

Every error should:

Be logged.

Return meaningful messages.

Retry when appropriate.

---

# 13. Testing

Every module must include:

Unit Tests

Integration Tests

Regression Tests

New features cannot be merged without passing tests.

---

# 14. Documentation

Every module must contain:

Purpose

Responsibilities

Dependencies

Public Functions

Configuration

Every API must be documented.

---

# 15. Git Rules

One feature per branch.

Meaningful commit messages.

No direct commits to main branch.

---

# 16. Performance

Process messages asynchronously.

Avoid blocking operations.

Optimize database queries.

Cache repeated AI results when possible — this is reinforced by the mandatory content-hash duplicate check in §7.3/§9, which prevents redundant AI calls for repeated content in the first place.

---

# 17. Security

Encrypt sensitive data.

Never expose API Keys.

Never expose database credentials.

Sanitize all user inputs.

Validate all uploaded files.

---

# 18. UI Rules

Responsive Design.

Arabic RTL support.

English LTR support.

Light & Dark Mode ready.

Accessible components.

---

# 19. AI Chat Rules

Every AI answer should:

* Use database facts first, retrieved exclusively via predefined Knowledge Engine query functions.
* Use AI reasoning second, to compose the final natural-language answer from those facts.
* Always cite the underlying stored data internally.
* Never invent project information.
* Never generate or execute SQL — see §2 and §9.

---

# 20. Deployment Rules

Use Docker.

Environment-based configuration.

Automatic backups.

Health checks.

Graceful shutdown.

Automatic restart after unexpected failures.

---

# 21. Development Workflow

Before coding:

1. Read PRD.
2. Read System Design.
3. Validate architecture.

During coding:

1. Build one module at a time.
2. Test immediately.
3. Document immediately.

Before finishing:

1. Run all tests.
2. Check performance.
3. Verify architecture compliance.

Never skip any step.

---

# 22. Golden Rule

Quality is more important than speed.

Never sacrifice architecture for faster implementation.

Every decision should support long-term maintainability, scalability, and reliability — within the explicitly approved scope (see §2.1).
