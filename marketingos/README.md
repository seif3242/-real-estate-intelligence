# MarketingOS

**Status: Blueprint stage. No implementation code exists yet. Do not begin building until the Open Decisions below are resolved and the blueprint is explicitly approved.**

MarketingOS is a professional operating system for marketing — not a website or blog — covering Marketing Strategy, Performance Marketing, Media Buying, E-commerce, Growth, Analytics, Creative Strategy, Copywriting, Consumer Psychology, CRM, SEO, Content Creation, Brand, and Marketing Finance/Leadership, structured Beginner → Intermediate → Advanced → Senior → Expert, with theory, frameworks, calculators, SOPs, checklists, decision trees, templates, case studies, and benchmarks.

This is a self-contained initiative living in this repository alongside the unrelated Real Estate AI Assistant project (see root `docs/`) — nothing here modifies that project.

---

## Blueprint Documents

| Doc | Covers |
|---|---|
| [`docs/PRD.md`](./docs/PRD.md) | Vision, non-goals, personas & jobs-to-be-done, skill-level framework, domain taxonomy, product principles, success metrics |
| [`docs/KNOWLEDGE_ARCHITECTURE.md`](./docs/KNOWLEDGE_ARCHITECTURE.md) | Content hierarchy (Domain→Topic→Module→Item), the 11 content types, metadata schema, learning paths |
| [`docs/INFORMATION_ARCHITECTURE.md`](./docs/INFORMATION_ARCHITECTURE.md) | Navigation models, site map, key UX flows (onboarding, domain hub, calculators, troubleshooting), search, personalization, UX principles |
| [`docs/SYSTEM_DESIGN.md`](./docs/SYSTEM_DESIGN.md) | Technical architecture: content layer, tool engine, search layer, personalization layer, modular repo structure |
| [`docs/CONTENT_GOVERNANCE.md`](./docs/CONTENT_GOVERNANCE.md) | Quality bar, freshness SLA by content type, editorial workflow, contribution model, style guide |
| [`docs/ROADMAP.md`](./docs/ROADMAP.md) | Phase 0 (this blueprint) → Phase 1 (3-domain MVP) → Phase 2 (horizontal expansion) → Phase 3 (intelligence layer) → Phase 4 (platform maturity) |

Read in that order — each doc builds on the ones before it.

---

## Open Decisions (need your call before implementation starts)

These are the choices that materially change the architecture and were deliberately **not** assumed:

1. **Audience & access model.** Is this a personal/single-user knowledge base for you (like the sibling Real Estate AI Assistant project — local, single-user, no auth complexity), or a product meant for other people (team, clients, or public/commercial), which implies real accounts, auth, and possibly a monetization model? This single decision changes the Personalization Layer (`SYSTEM_DESIGN.md §6`) from "trivial" to "a real subsystem," and determines whether multi-tenancy/permissions need to be designed now rather than later.
2. **Flagship domains for Phase 1.** `ROADMAP.md` recommends Performance Marketing & Media Buying, Analytics & Data, and Copywriting & Messaging as the 3 domains to build first — confirm, or name different priorities based on what you personally need soonest.
3. **Content authoring reality.** `SYSTEM_DESIGN.md §3` recommends a git-backed structured content store (not a database CMS) for V1, trading away a friendly non-engineer authoring UI in exchange for free versioning/review via the same PR workflow as code. If you (or future contributors) need a point-and-click editing UI from day one, that's a different — and larger — Phase 1 scope.
4. **Language scope.** The sibling Real Estate AI Assistant project in this repo explicitly supports Arabic + English throughout. Should MarketingOS be English-only for V1, or does it need multi-language support from the start? Not assumed either way — flagged because it affects the content schema (`KNOWLEDGE_ARCHITECTURE.md §4` would need a `locale` field) and every piece of content produced from Phase 1 onward.
5. **Certification/business model** (Phase 4 item, but worth flagging now). Is there any intent for this to eventually be sold, gated, or offer certification-style credentials? Doesn't block Phase 1, but affects whether the Personalization Layer should be designed with payments/entitlements in mind from the start.

---

## What happens after approval

Once the blueprint and open decisions are settled, the next step is **Phase 1 planning** (per `ROADMAP.md`) — a detailed implementation plan for the 3 flagship domains, the platform skeleton, and the tool engine. No code is written before that plan is reviewed, per your original instruction.
