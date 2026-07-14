# MarketingOS — Roadmap & Phasing

## Version 1.0 (Blueprint Stage)

Fourteen domains built Beginner→Expert with full tooling is not a V1 — it's the finished product. This roadmap sequences the work so the model gets validated early, with real content and real usage, rather than fully architected and then built blind across everything at once.

---

# Phase 0 — Foundation (this blueprint stage)

**Goal:** agree on the model before building anything.

* Product, knowledge-architecture, IA/UX, and system-design blueprints (this document set).
* Resolve the Open Decisions (see top-level `marketingos/README.md`).
* No application code, no content authoring yet — approval gate.

---

# Phase 1 — MVP: Prove the Model on 2–3 Flagship Domains

**Goal:** validate that the content model, tool engine, IA, and governance workflow actually work end-to-end with real content and real usage, before committing to all 14 domains.

Recommended flagship domains (highest persona demand per `KNOWLEDGE_ARCHITECTURE.md §2`, and good coverage of content-type variety):
* **Performance Marketing & Media Buying** — exercises Calculators, Troubleshooting Guides, Decision Trees, Benchmarks heavily.
* **Analytics & Data** — exercises Frameworks and Theory heavily, underpins credibility of every other domain.
* **Copywriting & Messaging** — exercises Templates and Case Studies heavily, different content shape than the first two.

Scope:
* Full Beginner→Expert build-out for the 3 flagship domains (not just Beginner content).
* Core cross-domain calculators: CAC/LTV, ROAS/breakeven, budget pacing, basic media mix.
* Platform skeleton: content layer + validation, tool engine with the shared calculator contract, search/facets, the universal content-item template, domain hub template, onboarding (role + level selection).
* Governance workflow live (draft/in_review/published), even as a single-author self-review process.
* No personalized/adaptive recommendations beyond the explicit role/level model in `INFORMATION_ARCHITECTURE.md §5`.

**Exit criteria:** the 3 domains are usably complete end-to-end (a real Media Buyer or Copywriter could use this instead of their current scattered references for real work), and the success metrics in `PRD.md §6` have a baseline.

---

# Phase 2 — Horizontal Expansion

**Goal:** scale the proven model across the remaining domains and content depth.

* Build out remaining 11 domains to the same Beginner→Expert bar.
* Expand tool library (more calculators/templates per domain).
* Add Role Paths and Level Paths (`KNOWLEDGE_ARCHITECTURE.md §5`) now that there's enough cross-domain content to make paths meaningful.
* Non-engineer content authoring UI on top of the git-backed content store, opening contribution beyond the original author (per `CONTENT_GOVERNANCE.md §4`).
* Expand case-study and benchmark libraries specifically — these compound in value with volume more than other types.

---

# Phase 3 — Intelligence Layer

**Goal:** move from explicit to adaptive personalization, and from keyword to semantic discovery.

* Semantic/natural-language search for problem-phrased queries (`INFORMATION_ARCHITECTURE.md §4`), replacing/augmenting curated query mappings.
* Adaptive learning-path recommendations based on actual usage/progress, not just self-reported level.
* Expert/contributor review-workflow tooling matures beyond git-PR-shaped review if contributor volume warrants it.
* Feedback loop instrumentation ("this helped me make a decision") wired into the success metrics from `PRD.md §6`.

---

# Phase 4 — Platform Maturity

**Goal:** the parts that make it feel like infrastructure, not a website.

* Live benchmark data integration (pulling current industry data rather than periodically-refreshed static tables) — the first point where the product might integrate with external platforms, and only for benchmark data, consistent with the V1 non-goal of not doing live ad-account integrations.
* Offline/mobile-optimized access for reference lookups in the field.
* Certification-style path completion, if validated as wanted by users (not assumed — this is a business-model question, see Open Decisions).

---

# Sequencing Principle

Each phase only starts once the prior phase's exit criteria are real and observed, not scheduled by calendar date — this is a knowledge-quality product, and shipping Phase 2's breadth on top of an unvalidated Phase 1 model would scale mistakes, not value.
