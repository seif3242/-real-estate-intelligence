# MarketingOS

**Status: Blueprint stage. No implementation code exists yet.** `docs/PRD.md` v2.0 proceeds on explicit default assumptions for the open decisions below (see its top section) so the full PRD wasn't blocked on them — confirm or override those assumptions before implementation starts.

MarketingOS is a professional operating system for marketing — not a website or blog — covering Marketing Strategy, Performance Marketing, Media Buying, E-commerce, Growth, Analytics, Creative Strategy, Copywriting, Consumer Psychology, CRM, SEO, Content Creation, Brand, and Marketing Finance/Leadership, structured Beginner → Intermediate → Advanced → Senior → Expert, with theory, frameworks, calculators, SOPs, checklists, decision trees, templates, case studies, and benchmarks.

This is a self-contained initiative living in this repository alongside the unrelated Real Estate AI Assistant project (see root `docs/`) — nothing here modifies that project.

---

## Blueprint Documents

| Doc | Covers |
|---|---|
| [`docs/PRD.md`](./docs/PRD.md) | **Start here.** The complete, self-contained PRD — vision, goals, personas, problems solved, features & priorities, user stories, functional/non-functional requirements, success metrics, risks, future expansion, IA, navigation, taxonomy, learning paths, content categories, internal linking, search strategy, dashboard layout, component list, folder/file structure, database structure, scalability plan |
| [`docs/KNOWLEDGE_ARCHITECTURE.md`](./docs/KNOWLEDGE_ARCHITECTURE.md) | Deep dive: content hierarchy, per-type authoring templates, full metadata schema |
| [`docs/INFORMATION_ARCHITECTURE.md`](./docs/INFORMATION_ARCHITECTURE.md) | Deep dive: full UX flow detail (onboarding, calculator flow, troubleshooting flow) |
| [`docs/SYSTEM_DESIGN.md`](./docs/SYSTEM_DESIGN.md) | Deep dive: architectural rationale and trade-offs behind the PRD's technical sections |
| [`docs/CONTENT_GOVERNANCE.md`](./docs/CONTENT_GOVERNANCE.md) | Deep dive: full quality bar, style guide, freshness SLA table |
| [`docs/ROADMAP.md`](./docs/ROADMAP.md) | Deep dive: phase-by-phase sequencing behind the PRD's Feature Priorities |

`PRD.md` is the canonical, complete reference — read it alone if you only read one file. The others provide extended detail on their respective areas and are cross-linked from the PRD.

---

## Open Decisions (defaults assumed in PRD v2.0 — confirm or override)

These are the choices that materially change the architecture. `docs/PRD.md` now proceeds with a stated default for each (see its "Assumptions" table) rather than blocking, but none are truly settled until you confirm:

1. **Audience & access model.** Is this a personal/single-user knowledge base for you (like the sibling Real Estate AI Assistant project — local, single-user, no auth complexity), or a product meant for other people (team, clients, or public/commercial), which implies real accounts, auth, and possibly a monetization model? This single decision changes the Personalization Layer (`SYSTEM_DESIGN.md §6`) from "trivial" to "a real subsystem," and determines whether multi-tenancy/permissions need to be designed now rather than later.
2. **Flagship domains for Phase 1.** `ROADMAP.md` recommends Performance Marketing & Media Buying, Analytics & Data, and Copywriting & Messaging as the 3 domains to build first — confirm, or name different priorities based on what you personally need soonest.
3. **Content authoring reality.** `SYSTEM_DESIGN.md §3` recommends a git-backed structured content store (not a database CMS) for V1, trading away a friendly non-engineer authoring UI in exchange for free versioning/review via the same PR workflow as code. If you (or future contributors) need a point-and-click editing UI from day one, that's a different — and larger — Phase 1 scope.
4. **Language scope.** The sibling Real Estate AI Assistant project in this repo explicitly supports Arabic + English throughout. Should MarketingOS be English-only for V1, or does it need multi-language support from the start? Not assumed either way — flagged because it affects the content schema (`KNOWLEDGE_ARCHITECTURE.md §4` would need a `locale` field) and every piece of content produced from Phase 1 onward.
5. **Certification/business model** (Phase 4 item, but worth flagging now). Is there any intent for this to eventually be sold, gated, or offer certification-style credentials? Doesn't block Phase 1, but affects whether the Personalization Layer should be designed with payments/entitlements in mind from the start.

---

## What happens after approval

Once the blueprint and open decisions are settled, the next step is **Phase 1 planning** (per `ROADMAP.md`) — a detailed implementation plan for the 3 flagship domains, the platform skeleton, and the tool engine. No code is written before that plan is reviewed, per your original instruction.
