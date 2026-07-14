# MarketingOS — System Design (Blueprint Stage)

## Version 1.0

This document translates the product/content requirements in `PRD.md`, `KNOWLEDGE_ARCHITECTURE.md`, and `INFORMATION_ARCHITECTURE.md` into a technical architecture. **No code is written against this yet** — it exists so the eventual implementation has a stable target, and so you can approve or redirect the architecture before any is built.

---

# 1. Architectural Requirements (derived from the product docs)

* **Content-heavy but not static**: thousands of content items eventually, most of which are read-only text/structure, plus a meaningful subset (calculators) that are interactive mini-applications.
* **Modular & independently maintainable**: content, tooling (calculators), search, and personalization are different concerns with different change rates — content changes daily, calculator logic changes rarely, personalization/auth changes with product iteration. They should not be entangled in one monolith.
* **Non-engineer-editable content**: a Marketing Director or subject-matter expert contributing a Framework or SOP should not need to write application code — matches the Content Governance contributor model in `CONTENT_GOVERNANCE.md`.
* **Versioned, reviewable content**: every content item has `status: draft/in_review/published/deprecated` and a `last_reviewed` date (from `KNOWLEDGE_ARCHITECTURE.md §4`) — this implies content needs a review/approval workflow, not just a database write.
* **Fast reads, infrequent writes**: read:write ratio is extremely read-heavy (professionals looking things up), so the architecture should optimize for read performance/caching over write throughput.
* **Search & filter across a large, richly-tagged corpus** — full-text plus faceted filters (domain/topic/type/level/tag) from day one; semantic search is a later capability, but the data model must not preclude it.
* **Scalable to 14 domains × ~8 topics × ~6 modules × several items** — on the order of several thousand content items at full maturity. The architecture must not need to be redesigned between "3 domains, MVP" and "14 domains, mature."

---

# 2. High-Level Architecture

Five loosely-coupled layers, each independently deployable/maintainable:

```
┌─────────────────────────────────────────────────────────────────┐
│  Presentation Layer  (web app: content pages, tool UIs, search)  │
├─────────────────────────────────────────────────────────────────┤
│  Tool Engine          │  Search & Discovery  │  Personalization  │
│  (calculator/template │  (index, facets,     │  (auth, progress, │
│   plugin registry)    │   query resolution)  │   bookmarks)      │
├─────────────────────────────────────────────────────────────────┤
│  Content Layer  (structured content store — the source of truth) │
├─────────────────────────────────────────────────────────────────┤
│  Data Store  (user/account data — separate from content)         │
└─────────────────────────────────────────────────────────────────┘
```

Key architectural decision: **content and user data are deliberately separate systems.** Content (the 14-domain knowledge graph) is structured, versioned, and mostly authored by humans/editors; user data (accounts, progress, bookmarks) is transactional application data. Conflating them into one database, as a typical CMS-backed app might, would make content review/versioning (a Content Governance requirement) awkward and would couple content release cycles to application deploys unnecessarily.

---

# 3. Content Layer

**Recommendation: git-backed structured content, not a database-backed CMS, for V1.**

Rationale:
* Content items map naturally to structured files (metadata schema from `KNOWLEDGE_ARCHITECTURE.md §4` as frontmatter/schema-validated fields + a body).
* Git gives free versioning, diff-based review (a content PR is reviewable exactly like a code PR), and an audit trail for `last_reviewed`/`author`/`reviewer` — directly satisfying the Content Governance review workflow without building a custom CMS review UI in V1.
* Non-engineer contributors can still work through a constrained authoring UI *on top of* the git-backed store later (Phase 2+, see `ROADMAP.md`) without changing the underlying source of truth.
* Avoids standing up and operating a headless CMS service before the content model has proven itself with real authoring.

Trade-off acknowledged: this defers a friendly WYSIWYG authoring experience for non-technical contributors; that is an explicit, revisit-later decision, not an oversight — flagged in the Open Decisions list.

Each content item is validated at build/publish time against the metadata schema from `KNOWLEDGE_ARCHITECTURE.md §4` — a content item missing required fields (e.g., no `skill_levels`, no `last_reviewed`) should fail validation, not publish silently non-compliant.

---

# 4. Tool Engine (Calculators & Interactive Templates)

Calculators are the one part of the content graph that is *executable*, not just readable, so they get their own subsystem rather than being modeled as regular content.

* Each calculator is a self-contained **tool module** conforming to a shared contract: an **input schema** (typed fields: number/currency/percentage/select, with labels, defaults, validation ranges), a **compute function** (pure, deterministic — given inputs, produces outputs, no side effects), and an **output/interpretation spec** (what the numbers mean in plain language, and which thresholds trigger which guidance, e.g., "ROAS below breakeven — see troubleshooting guide X").
* A central **tool registry** lists all calculators with their metadata (same content-item metadata fields as `KNOWLEDGE_ARCHITECTURE.md §4` — domain, topic, skill level, related content) so calculators are discoverable through the same search/filter/domain-hub surfaces as any other content item, not a walled-off "tools" ghetto.
* New calculators are added by implementing the shared contract and registering — this is the modularity requirement in action: adding calculator #40 must not require touching calculator #1–39.
* Templates (the downloadable/fillable document type) are simpler: they are static assets (or structured documents) with the same metadata wrapper, no compute logic, served from the content layer directly.

---

# 5. Search & Discovery Layer

* V1: a **full-text + faceted search index** built from the content layer's metadata (domain/topic/module/type/skill_levels/tags) — a dedicated search index service (rebuilt/updated whenever content is published) rather than ad hoc database `LIKE` queries, since facet + relevance ranking is a first-class product requirement (`INFORMATION_ARCHITECTURE.md §4`).
* The index is derived/rebuildable from the content layer at any time — it is a cache/projection, never the source of truth, so it can be rebuilt or swapped (e.g., to add semantic/vector search in Phase 3+) without touching content.
* Curated query→content mappings (e.g., "ROAS dropped" → specific Troubleshooting Guide) are a lightweight editorial layer on top of the index for V1, ahead of investing in semantic search.

---

# 6. Personalization Layer

* Holds: user account, stated role, stated skill level per domain, bookmarks, per-domain progress, saved calculator results.
* Deliberately thin in V1 per `INFORMATION_ARCHITECTURE.md §5` — explicit user-set state, not behavioral inference — which keeps this layer's data model simple: essentially user profile + a set of (user, content_item) interaction records.
* This is the one layer that needs a conventional transactional data store (relational), since it's write-heavy relative to content and has real per-user state.

---

# 7. Modularity & Repo Structure (conceptual, pre-code)

To satisfy "modular, scalable, maintainable, expandable" concretely, the eventual codebase should separate along these lines (exact framework/tooling choices deferred to implementation planning, not this blueprint):

* **Content package** — the structured content store + schema/validation, framework-agnostic.
* **Web application** — presentation layer, consumes content + tool engine + search + personalization through defined interfaces, doesn't reach into any of their internals.
* **Tool engine package** — calculator/template contracts + registry, independently testable (a calculator's compute function is pure and unit-testable in isolation from the UI).
* **Search package** — index build + query resolution, replaceable independently of the web app.
* **Personalization/account service** — the one component with real backend state and auth concerns, isolated so its security surface is contained.
* **Shared design system** — the content-item template, calculator template, badges (type/level/freshness), etc. from `INFORMATION_ARCHITECTURE.md §3.3–3.4`, shared across all content-rendering surfaces so the "one consistent template" UX principle is enforced by shared components, not by author discipline.

This separation directly mirrors the five architectural layers in §2 — each layer is a package/service boundary, not just a conceptual diagram.

---

# 8. Non-Functional Notes

* **Performance**: read-heavy, cacheable content pages — favor pre-rendering/caching content pages over dynamic per-request rendering where personalization doesn't require it (i.e., cache the content, personalize the surrounding chrome/recommendations).
* **Internationalization**: not in V1 scope unless you tell us otherwise (flagged in Open Decisions) — the metadata schema should not preclude a future `locale` field, but no i18n work is scoped now.
* **Accessibility**: standard WCAG-conformant practices for the content template and calculator forms — non-negotiable baseline, not a phase-gated feature.
