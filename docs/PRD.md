# Real Estate AI Assistant

## Product Requirements Document (PRD) — Version 1.1

> **Changelog from v1.0:** Unified message taxonomy with System Design; scoped V1 to text + PDF only (images/voice/video explicitly excluded); clarified notifications are Dashboard-only (no WhatsApp sending, ever); added WhatsApp Group onboarding requirement; added AI confidence scoring and manual correction workflow requirements; added duplicate-detection requirement; clarified permanence guarantees for structured data; reaffirmed single-user scope (no multi-user scaffolding in V1).

---

# 1. Product Vision

## Project Name

Real Estate AI Assistant

## Goal

Build an AI-powered assistant that automatically monitors WhatsApp real estate groups, understands every message, extracts structured information, stores it in a knowledge base, and allows the user to search or ask questions using natural language.

The system should become the user's daily real estate assistant, eliminating the need to manually read hundreds of WhatsApp messages.

---

# 2. Target User

Version 1.0/1.1

Single User Only

The system is built for one real estate broker, running as a local, single-user deployment.

**This is an intentional design constraint, not a temporary limitation.** No multi-user or tenant scaffolding (e.g. `user_id` columns, per-user authentication) will be introduced in V1. Multi-user support remains a tracked Future Feature (see §19) and will be designed as a deliberate, dedicated effort when it is scheduled — not bolted on incrementally.

---

# 3. Languages

The entire system must support:

* Arabic
* English

Including:

* User Interface
* AI Chat
* Search
* Message Understanding
* PDF Understanding

---

# 4. Main Objectives

The system should:

* Monitor WhatsApp groups automatically.
* Detect new messages.
* Read text messages.
* Read PDF files.
* Extract structured information.
* Classify every message.
* Store all information.
* Answer questions using AI.
* Generate daily summaries.
* Compare projects.
* Track historical changes.

---

# 5. Version 1 Scope — Supported Content Types

Version 1 explicitly supports only:

* **Text Messages**
* **PDF Files**

**Out of scope for V1 (explicitly excluded):**

* Images (e.g., price lists or floor plans shared as photos)
* Voice Notes
* Videos

These content types are common in real estate WhatsApp groups and are acknowledged as a likely V2 requirement, but are deliberately excluded from V1 to keep the initial scope achievable. The Collector and Attachment handling layers must not attempt to process them; messages containing only these media types should be stored as raw messages (for the 30-day retention window) without AI extraction.

---

# 6. Message Classification (Unified Taxonomy)

The AI must classify every text/PDF-bearing message into exactly one of the following categories. This taxonomy is canonical and must be used identically across the PRD, System Design, AI Parser implementation, and database schema.

1. **Launch**
2. **Request**
3. **Offer**
4. **Commission Update**
5. **Price Update**
6. **Brochure**
7. **News**
8. **General Information**

**Note:** "PDF" is **not** a classification category. A PDF is a content/attachment type, not a message intent — a message that contains a PDF is still classified into one of the eight categories above (most often Brochure, Launch, or Offer), and the fact that it carries a PDF attachment is recorded separately via the document/attachment relationship.

---

# 7. Data Extraction

The AI should extract whenever available:

Developer

Project Name

Location

Unit Types

Starting Price

Old Price

New Price

Down Payment

Installments

Delivery Date

Commission

Offer Details

Contact Information

Links

Attachments

## 7.1 Extraction Confidence

Every extracted field (or extraction record as a whole, at minimum) must be stored with an **AI confidence score**. If the AI is not confident enough that a field is correct, it must return "Information Not Available" rather than guess, per the AI Rules in the Engineering Rules document. Confidence scores are surfaced in the UI so the user can quickly identify low-confidence extractions that may need review.

## 7.2 Manual Correction Workflow

Because AI extraction will occasionally be wrong, the user must be able to **manually edit/correct** any extracted field from the UI (e.g., on a Project Page or a dedicated review screen). Corrections must:

* Be stored distinctly from the original AI-produced value (preserving an audit trail of "what the AI said" vs. "what the user corrected it to").
* Never be silently overwritten by a later automatic re-processing pass of the same source message.
* Be reflected immediately in the Dashboard, Search, Project Page, and AI Chat answers.

---

# 8. WhatsApp Groups

Every WhatsApp group belongs to one developer.

Messages received from a group are automatically associated with that developer.

## 8.1 Group Onboarding

A WhatsApp group must be **explicitly onboarded** before its messages are processed beyond raw storage. Onboarding means an administrator (the single user) registers the group and maps it to a developer. Until a group is onboarded:

* Its messages may still be collected and stored as raw messages (subject to the 30-day retention window), but
* They are **not** run through AI classification/extraction, since there's no developer to associate them with.

The system must provide a way to view newly detected/unmapped groups and onboard them (assign a developer, or mark the group as ignored).

---

# 9. PDF Processing

Every PDF should:

Be downloaded automatically.

Be analyzed completely.

Extract all available information.

Generate an AI summary.

Be linked to the correct developer and project.

PDF files are stored permanently.

---

# 10. Duplicate Detection

The same offer, brochure, or price list is frequently reposted — verbatim or near-verbatim — across multiple WhatsApp groups. To avoid unnecessary AI API calls and inconsistent duplicate records:

* Every incoming message and PDF must be **content-hashed** before being sent to the AI.
* If the content hash matches a previously processed message/document, the system must **reuse the existing extraction result** rather than invoking the AI again.
* True duplicates should still be linked to their respective groups/developers for traceability, even though they share one extraction result.

---

# 11. Price History

Whenever a price changes, the system must save:

Old Price

New Price

Difference

Date

History must never be overwritten.

---

# 12. Commission History

Store every commission change.

Maintain historical timeline.

---

# 13. Data Retention & Permanence

* **Raw WhatsApp messages**: stored for **30 days only**, then automatically deleted.
* **Extracted structured information** (classified messages, Launches, Requests, Offers, etc.): stored **permanently**.
* **PDF files**: stored **permanently**.
* **Price History**: stored **permanently**, never overwritten.
* **Commission History**: stored **permanently**, never overwritten.

The database design must guarantee that deleting an expired raw message **never** cascades into deleting any of the permanent structured data derived from it (see System Design §7 for the relational approach).

---

# 14. AI Chat

The user can ask questions naturally.

Examples:

What are today's launches?

Show today's requests.

Highest commission today.

Compare Project A and Project B.

Show Palm Hills updates.

Recommend a project under 8M.

What changed this week?

The AI answers using real stored data, accessed only through the Knowledge Engine's predefined query functions (see System Design §8) — the AI never generates or executes raw SQL.

---

# 15. Dashboard

Dashboard should display:

Today's Launches

Today's Requests

Today's Offers

Today's Price Updates

Today's Commission Updates

Today's PDFs

Developer Statistics

Project Statistics

The Dashboard is also the primary channel through which Notifications (§17) are surfaced to the user.

---

# 16. Search

Global search across:

Projects

Developers

Launches

Requests

Offers

PDFs

---

# 17. Project Page

Each project should include:

Timeline

Price History

Commission History

Launches

Offers

PDFs

Latest Updates

AI Summary

---

# 18. Developer Page

Each developer should include:

Projects

Latest Updates

Offers

Launches

Price History

PDFs

Statistics

---

# 19. Notifications

Notification types:

* Daily Summary
* New Launch Alerts
* Price Change Alerts
* Commission Alerts
* New Requests

## 19.1 Delivery Channel

Notifications are delivered **only through the Dashboard** in Version 1. **Email** is an allowed future delivery channel (not built in V1). **WhatsApp is never used as a notification delivery channel**, under any circumstances — this is consistent with the strict read-only / no-message-sending rule that governs the entire WhatsApp integration.

---

# 20. Security

Local deployment for Version 1.

Single user access — by design, with no multi-user/auth scaffolding in V1 (see §2).

No automatic message sending of any kind.

Read-only WhatsApp monitoring.

---

# 21. Future Features

CRM Integration

Telegram Integration

Email Integration (including email as a Notification channel)

Voice Assistant

Mobile Application

Cloud Deployment

Multi-user Support

Support for Image, Voice Note, and Video content types

---

# 22. Success Criteria

The project is considered successful if:

The user no longer needs to manually monitor WhatsApp groups.

The AI can answer real estate questions accurately.

The system automatically organizes market knowledge.

The user saves significant time every day while identifying launches, requests, offers, commissions, and market updates.
