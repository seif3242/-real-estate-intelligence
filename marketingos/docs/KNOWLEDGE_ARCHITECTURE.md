# MarketingOS — Knowledge Architecture

## Version 1.0 (Blueprint Stage)

This document defines the taxonomy, content-type system, and metadata schema that every piece of MarketingOS content is built from. It is the "curriculum design" layer of the product — the part a Knowledge Architect owns.

---

# 1. Hierarchy

Content is organized in a four-level hierarchy. This is the *authoring* structure; the *navigation* structure (how users actually reach content) is deliberately different and is defined in [`INFORMATION_ARCHITECTURE.md`](./INFORMATION_ARCHITECTURE.md) — a strict tree is good for authors, bad for users who think in problems, not tables of contents.

```
Domain (14)
 └── Topic (≈6–10 per domain)
      └── Module (≈4–8 per topic)
           └── Content Item (the atomic, taggable, linkable unit)
```

Example — Domain 2, Performance Marketing & Media Buying:

```
Domain: Performance Marketing & Media Buying
 ├── Topic: Meta Ads
 │    ├── Module: Account & Campaign Structure
 │    ├── Module: Audience Targeting & Segmentation
 │    ├── Module: Bidding Strategies & Budget Optimization
 │    ├── Module: Creative Testing Frameworks
 │    └── Module: Troubleshooting & Diagnostics
 ├── Topic: Google Ads (Search, PMax, Shopping)
 ├── Topic: TikTok & Emerging Social Platforms
 ├── Topic: Programmatic & DSPs
 ├── Topic: Attribution & Measurement for Paid Media
 └── Topic: Budget Planning & Media Mix
```

Every domain follows this same pattern of decomposition; full per-domain Topic/Module breakdowns are produced during content planning for each domain (Phase 1 domains are broken down first — see [`ROADMAP.md`](./ROADMAP.md)), not exhaustively enumerated in this blueprint, to avoid the blueprint itself becoming stale before content work starts.

---

# 2. Personas → Domains Matrix

Maps who cares about which domains most, used to sequence content build order and to power role-based curated paths (see [`INFORMATION_ARCHITECTURE.md §9`](./INFORMATION_ARCHITECTURE.md)):

| Persona | Primary domains | Secondary domains |
|---|---|---|
| Media Buyer / Performance Marketer | Performance Marketing, Analytics, Creative Strategy | Psychology, Finance |
| Marketing Manager | Marketing Strategy, Content, Brand | Analytics, CRM |
| E-commerce Manager | E-commerce, Performance Marketing, CRM | Finance, Analytics |
| Growth Marketer | Growth, Analytics, Psychology | Performance Marketing, Content |
| CRM Specialist | CRM, Copywriting, Psychology | Analytics |
| Content Creator | Content Creation, Copywriting, SEO | Brand, Psychology |
| Copywriter | Copywriting, Psychology, Brand | Content Creation |
| Brand Manager | Brand, Marketing Strategy, Creative Strategy | Psychology, Finance |
| Marketing Director | Marketing Strategy, Finance, Business/Leadership | all (breadth over depth) |
| Business/Agency Owner | Business/Leadership, Finance, Marketing Strategy | all (breadth over depth) |

---

# 3. Content Item Types

Every atomic content item has exactly one primary **type**. Types are not interchangeable — each has a distinct authoring template and UI rendering, because each solves a different moment of need.

| # | Type | Purpose | Format | Example |
|---|---|---|---|---|
| 1 | **Theory / Concept** | Explain *why*; build mental models | Article: definition → mechanism → why it matters → common misconceptions | "How the Meta Ads auction actually works" |
| 2 | **Framework** | Reusable structured methodology | Named model + steps/components + when to use it + when not to | RACE, AARRR, Jobs-to-be-Done, StoryBrand |
| 3 | **Calculator** | Turn inputs into a decision-ready number, instantly | Interactive tool: inputs → formula → result → interpretation | CAC/LTV calculator, ROAS breakeven, budget pacing |
| 4 | **SOP (Standard Operating Procedure)** | Repeatable execution with zero ambiguity | Numbered steps, preconditions, tools needed, done-criteria | "SOP: Launching a new Meta campaign" |
| 5 | **Checklist** | Pre-flight / QA gate | Checkbox list, binary pass/fail items | "Pre-launch checklist: paid social campaign" |
| 6 | **Decision Tree** | Diagnose or choose under uncertainty | Branching Q&A → outcome/recommendation | "Which attribution model should I use?" |
| 7 | **Template** | Reusable, fillable artifact | Downloadable/copyable document or structure | Creative brief template, media plan template, email sequence template |
| 8 | **Case Study** | Ground theory in a real, numbers-backed example | Situation → action → result → what to take away | "How [category] brand cut CAC 40% with creative testing" |
| 9 | **Benchmark** | Comparative reference data | Table: metric by industry/channel/segment, with source + date | "Average CTR by industry, Meta Ads, 2026" |
| 10 | **Troubleshooting Guide** | Fix a known-broken state fast | Symptom → likely causes (ranked) → diagnostic steps → fix | "ROAS dropped suddenly — troubleshooting guide" |
| 11 | **Glossary Term** | Fast definition lookup | Term + one-paragraph definition + link to fuller Theory item | "What is MER (Marketing Efficiency Ratio)?" |

Design rule: **Decision Trees and Troubleshooting Guides are the "3 AM" content types** — they must never require reading a Theory item first. Every Decision Tree/Troubleshooting Guide is self-sufficient, and *links out* to Theory/Framework items for readers who want the "why" afterward.

---

# 4. Content Item Metadata Schema (conceptual)

Every content item, regardless of type, carries this metadata. This is the schema the content repository, search index, and personalization engine are all built against — defined here so [`SYSTEM_DESIGN.md`](./SYSTEM_DESIGN.md) has a stable contract to implement against later.

| Field | Description |
|---|---|
| `id` | Stable unique identifier (never reused, even if content is deprecated) |
| `type` | One of the 11 types in §3 |
| `domain`, `topic`, `module` | Position in the authoring hierarchy |
| `title`, `summary` | Display title and one-sentence summary (used in search results/cards) |
| `skill_levels` | One or more of Beginner/Intermediate/Advanced/Senior/Expert this item is written for |
| `prerequisites` | Other content item IDs a reader should understand first (powers "you may want to read this first" and path sequencing) |
| `related_items` | Cross-links to other items regardless of hierarchy position (powers the knowledge-graph browsing model) |
| `applies_to_calculators` / `applies_to_templates` | Explicit links from theory/framework content to the tools that operationalize them |
| `tags` | Free-form facets (channel, industry vertical, funnel stage, etc.) for filtering/search |
| `sources` | Citations for data-backed claims; empty only if explicitly marked practitioner opinion |
| `author`, `reviewer` | Accountability for accuracy |
| `last_reviewed` | Date, shown to readers; drives the freshness SLA in [`CONTENT_GOVERNANCE.md`](./CONTENT_GOVERNANCE.md) |
| `status` | `draft` / `in_review` / `published` / `deprecated` |

Calculators additionally define an **input schema** (typed fields), a **formula/logic spec**, and an **output/interpretation spec** — detailed in [`SYSTEM_DESIGN.md §4`](./SYSTEM_DESIGN.md).

---

# 5. Learning Paths (cross-cutting structure)

A **Learning Path** is an ordered sequence of content items that can cross domain/topic/module boundaries — it is the mechanism that turns the graph back into a guided curriculum when a user wants one.

Two path types:

1. **Role paths** — curated per persona (e.g., "Media Buyer: Beginner → Advanced"), spanning primarily one domain plus the secondary domains that persona needs (per the matrix in §2).
2. **Level paths** — "everything a marketer needs to go from Beginner to Intermediate across foundational domains," domain-agnostic, for generalists early in career.

Paths are curated content, not auto-generated in V1 (auto-generated/adaptive paths are a Phase 3 capability — see [`ROADMAP.md`](./ROADMAP.md)).
