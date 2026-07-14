# MarketingOS

## Product Requirements Document — Version 1.0 (Blueprint Stage)

> Status: **Blueprint / not yet approved for implementation.** No code has been written. This document and its companions in `marketingos/docs/` define the product before a single line is built.

---

# 1. Product Vision

## 1.1 What this is

MarketingOS is **not a website, blog, or course platform.** It is a professional operating system — the single reference a marketing professional keeps open throughout their career, spanning every discipline that touches modern marketing: Marketing Strategy, Performance Marketing, Media Buying, E-commerce, Growth, Analytics, Creative Strategy, Copywriting, Psychology, CRM, SEO, Content Creation, Brand, and the business/finance layer that sits underneath all of it.

It combines four things that normally live in separate, disconnected tools:

1. **Theory** — the concepts and mental models that explain *why* something works.
2. **Practice** — SOPs, checklists, templates, and calculators that let someone execute *right now*, mid-workday.
3. **Diagnosis** — decision trees and troubleshooting guides for when something is broken and there's no time to read a textbook.
4. **Progression** — a structured path from Beginner to Expert in every discipline, so the same platform serves a first-year associate and a CMO.

## 1.2 What this is not (V1 non-goals)

* Not a graded LMS / course-completion certificate mill.
* Not a social network or community/forum product.
* Not a live ad-platform integration (no pulling real account data from Meta/Google in V1) — content is reference and tooling, not a reporting dashboard.
* Not a general business wiki — every domain in scope must connect back to marketing, growth, or the commercial function of a business.
* Not (necessarily) multi-tenant SaaS from day one — see §7 Open Decision on audience/access model.

## 1.3 Positioning statement

> For marketing professionals at every level, MarketingOS is the operating system that replaces a scattered stack of blog posts, spreadsheets, Slack tips, and outdated courses with one structured, always-current, actually-usable knowledge and tooling platform — because a professional's reference material shouldn't be less rigorous than the professional themselves.

---

# 2. Target Users

MarketingOS serves twelve primary personas, grouped into three usage modes:

| Mode | Personas | Primary need |
|---|---|---|
| **Execute** | Media Buyer, Performance Marketer, CRM Specialist, Content Creator, Copywriter | Fast, in-the-moment tools: calculators, SOPs, checklists, templates, troubleshooting |
| **Design & Manage** | Marketing Manager, E-commerce Manager, Growth Marketer, Brand Manager | Frameworks, decision-making models, case studies, planning templates |
| **Direct & Own** | Marketing Director, Business/Agency Owner | Strategic frameworks, cross-domain fluency to evaluate teams/vendors, finance-of-marketing literacy |

Each persona is detailed with jobs-to-be-done, trigger moments, and success criteria in [`KNOWLEDGE_ARCHITECTURE.md §2`](./KNOWLEDGE_ARCHITECTURE.md).

Representative jobs-to-be-done:

* *"When my ROAS drops 30% overnight, I want a diagnostic flow, not a 2,000-word article, so I can find the cause in minutes."* — Media Buyer
* *"When I plan next quarter, I want a proven framework and a fillable template, so I'm not starting from a blank doc."* — Marketing Manager
* *"When I evaluate a new channel, I want to model CAC/LTV before I commit budget."* — E-commerce Manager
* *"When I brief an agency, I want to know enough about their discipline to tell good work from mediocre work."* — Business Owner

---

# 3. Skill Level Framework

Every piece of content, every tool, and every learning path is tagged against one operational skill ladder, used identically across all 14 domains:

| Level | Operational definition |
|---|---|
| **Beginner** | Knows core terminology; can execute a well-defined task under guidance; cannot yet evaluate whether their own output is good. |
| **Intermediate** | Independently runs a channel/process end-to-end; recognizes when something is wrong but may not know the fix; needs a diagnostic aid. |
| **Advanced** | Designs strategy across multiple channels/tools within a domain; optimizes systems, not just tasks; can mentor Beginners/Intermediates. |
| **Senior** | Owns budget/P&L for the domain; sets strategy; manages a team; operates cross-functionally with Finance, Product, Sales. |
| **Expert** | Sets direction others follow; originates frameworks rather than applying them; operates at executive/board level; judgment substitutes for playbooks. |

This ladder is the backbone of personalization: content, calculators, and learning paths are filtered by it, and it is the same five-level scale everywhere — a user's "Advanced" in Performance Marketing and "Beginner" in SEO are both expressed on one shared vocabulary.

---

# 4. Domain Taxonomy (scope of coverage)

MarketingOS covers 14 domains at launch-scope (not all built in Phase 1 — see [`ROADMAP.md`](./ROADMAP.md)):

1. Marketing Strategy & Foundations
2. Performance Marketing & Media Buying (Paid Search, Paid Social, Programmatic/DSP)
3. E-commerce & DTC
4. Growth Marketing (experimentation, funnels, PLG)
5. Analytics & Data (measurement, attribution, MMM, dashboards)
6. Creative Strategy & Ad Creative
7. Copywriting & Messaging
8. Consumer Psychology & Behavioral Economics
9. CRM & Lifecycle Marketing (email, SMS, push, retention)
10. SEO & Organic Discovery
11. Content Creation & Content Marketing
12. Brand Marketing
13. Marketing Finance & Unit Economics
14. Business & Leadership for Marketers (agency ops, team building, career growth)

Full breakdown of each domain into Topics → Modules → Content Items is in [`KNOWLEDGE_ARCHITECTURE.md`](./KNOWLEDGE_ARCHITECTURE.md).

---

# 5. Core Product Principles

1. **Usable mid-task, not just study material.** If a calculator or checklist can't be used in under 30 seconds during live work, it has failed its purpose.
2. **Every claim has a shelf life.** Ad platform benchmarks, algorithm behavior, and channel tactics decay. Every content item carries a `last_reviewed` date visible to the reader, and stale content is a defect, not a footnote.
3. **One taxonomy, five levels, everywhere.** No domain invents its own progression scale — this is what makes cross-domain learning paths and personalization possible.
4. **Content is a graph, not a tree.** A troubleshooting guide links to the SOP that prevents the problem, the framework that explains it, and the calculator that quantifies it. Users rarely arrive via a single hierarchical path.
5. **Depth over breadth, sequenced.** It is better to fully build Beginner→Expert in three domains than to have shallow Beginner-only coverage in fourteen. Breadth is a Phase 2+ goal, not a Phase 1 one.
6. **Practitioner-grade, sourced.** Data-backed claims are cited or explicitly labeled "practitioner opinion." No unsourced absolute benchmarks.

---

# 6. Success Metrics

| Category | Metric | Why it matters |
|---|---|---|
| Coverage | % of taxonomy (domain × topic × module) with published content per skill level | Tracks progress against the "complete reference" vision |
| Usage | Returning-visit rate; calculator/tool invocations per user per week | Distinguishes "read once" from "operating system I keep open" |
| Utility | % of sessions ending in template download / calculator use / SOP copy (not just article read) | Validates the "not a blog" positioning |
| Trust | % of content within governance freshness SLA (see [`CONTENT_GOVERNANCE.md`](./CONTENT_GOVERNANCE.md)) | A stale reference is a broken reference |
| Outcome (qualitative) | Self-reported "this changed a decision I made at work" | Proxy for career-reference value, the north star |
| Search | % of searches resulting in a content view with no immediate re-search (search abandonment inverse) | IA/search quality signal |

---

# 7. Open Decisions Requiring Your Approval

These materially affect the architecture and are called out explicitly rather than assumed. See the consolidated list with recommendations in the top-level [`marketingos/README.md`](../README.md) — do not proceed to implementation until these are resolved.
