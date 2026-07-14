# MarketingOS — Content Governance & Quality Standards

## Version 1.0 (Blueprint Stage)

A knowledge platform lives or dies on whether its readers can trust it. This document defines the editorial bar every content item must clear, and the workflow that keeps the corpus from silently going stale — the single biggest risk to a "reference for your whole career" product, since marketing tactics and platform behavior change constantly even when marketing *principles* don't.

---

# 1. Quality Bar (applies to every content item)

1. **Sourced or labeled.** Any data-backed claim (a benchmark number, a stat, "X% of marketers do Y") must cite a source. Claims without a citable source must be explicitly labeled practitioner opinion/heuristic, not presented as fact.
2. **Actionable, not just descriptive.** Every Theory/Framework item should answer "so what do I do with this" — either directly or via an explicit link to the SOP/Calculator/Template that operationalizes it.
3. **Level-appropriate.** Content tagged Beginner must not assume Advanced-level prerequisite knowledge without listing it in `prerequisites` (per the metadata schema in `KNOWLEDGE_ARCHITECTURE.md §4`).
4. **Self-sufficient for its type.** Decision Trees and Troubleshooting Guides in particular must be usable without first reading a Theory item (Product Principle in `PRD.md §5`).
5. **Consistent structure for its type.** Authors follow the per-type template (`KNOWLEDGE_ARCHITECTURE.md §3`) — an SOP that reads like a Theory essay is a defect, not a style choice.

---

# 2. Freshness & Review SLA

Different content types decay at different rates. Review cadence is tiered accordingly:

| Content type | Review cadence | Why |
|---|---|---|
| Benchmarks | Every 6 months | Platform CPMs/CTRs/CVRs shift fast; stale benchmarks actively mislead |
| SOPs, Checklists | Every 6–12 months | Platform UIs and best practices change |
| Troubleshooting Guides, Decision Trees | Every 12 months | Diagnostic logic is more durable but platform-specific causes shift |
| Frameworks, Theory/Concepts | Every 18–24 months | Principles are the most durable content type |
| Case Studies | Not "refreshed," but flagged with a visible date | A case study is a historical artifact — its value is context, not currency; readers just need to know when it happened |
| Glossary | As needed, on drift | Low decay rate |

Every content item displays `last_reviewed` to the reader (per `KNOWLEDGE_ARCHITECTURE.md §4` and `INFORMATION_ARCHITECTURE.md §3.3`) — freshness is a visible trust signal, not just an internal ops metric. Content past its SLA window is flagged (visibly, e.g. "due for review") rather than silently left as-is or silently removed.

---

# 3. Editorial Workflow

```
draft → in_review → published → (eventually) deprecated
```

* **draft** — author-only visibility, not searchable/browsable.
* **in_review** — a named reviewer (per the `reviewer` metadata field) checks against §1's quality bar before publish. In V1 with a single author/owner, this is a deliberate self-review checklist pass, not skipped — the workflow state exists specifically so it scales to multiple contributors later without redesign (per `SYSTEM_DESIGN.md §1`'s non-engineer-contributor requirement).
* **published** — live, indexed, discoverable.
* **deprecated** — superseded or no longer accurate; kept (not deleted) for link integrity and historical case-study value, but excluded from search/browse and clearly marked if a stale inbound link resolves to it.

Because the content layer is git-backed (`SYSTEM_DESIGN.md §3`), this workflow maps directly onto a PR-based review process: a content change is a diff, `in_review` is an open PR, `published` is merge.

---

# 4. Contribution Model

V1 is single-author/owner (you), but the schema and workflow above are designed from day one to support additional contributors and subject-matter-expert reviewers without rearchitecting — this is a deliberate scalability decision (mirrors the single-user-but-scalable posture the sibling Real Estate AI Assistant project in this repo also takes, for a different reason). Concretely:

* The `author`/`reviewer` metadata fields already distinguish the two roles.
* The git-PR-shaped workflow already supports external reviewers commenting/approving without further tooling.
* A non-engineer-friendly authoring UI on top of the git-backed store is an explicit Phase 2+ item (`ROADMAP.md`), not assumed to exist at launch — V1 contributors author content directly in the structured format.

---

# 5. Style Guide (summary — full style guide is a Phase 1 deliverable, not this blueprint)

* Practical register: written for someone about to *do* something, not written to be impressive.
* No unexplained jargon — first use of a term either links to the Glossary or defines inline.
* Numbers over adjectives wherever possible ("CTR below 0.8%" beats "a low CTR").
* Every SOP/Checklist uses imperative, numbered steps with explicit done-criteria — not narrative prose.
