# MarketingOS

## Product Requirements Document — Version 2.0 (Complete)

> **Status: Blueprint stage. No implementation code exists yet.** This is the canonical, complete PRD superseding v1.0. Companion deep-dive docs (`KNOWLEDGE_ARCHITECTURE.md`, `INFORMATION_ARCHITECTURE.md`, `SYSTEM_DESIGN.md`, `CONTENT_GOVERNANCE.md`, `ROADMAP.md`) remain in this folder for extended detail on their respective areas and are referenced inline, but this document is self-contained — read it alone if you only read one file.

### Assumptions made to keep this document unblocked

The v1.0 blueprint left five decisions open for your approval. Rather than pause again, this PRD proceeds on the following defaults — **explicitly called out so you can override any of them**, each chosen for a stated reason:

| # | Decision | Default assumed here | Why this default |
|---|---|---|---|
| 1 | Audience/access model | Start single-owner (you), but every design decision below is made so flipping to multi-user later is additive, not a rewrite | Matches the sibling Real Estate AI Assistant project's philosophy in this repo; avoids building unused auth complexity now |
| 2 | Phase 1 flagship domains | Performance Marketing & Media Buying, Analytics & Data, Copywriting & Messaging | Highest persona demand + widest coverage of content-type variety (calculators, frameworks, templates) |
| 3 | Content authoring | Git-backed structured content for V1; friendly authoring UI is Phase 2 | You're a technical user; free versioning/review beats a CMS you'd have to build first |
| 4 | Language | English-only V1; schema reserves a `locale` field | No stated requirement for Arabic/multi-language on this project, unlike the sibling repo |
| 5 | Monetization/certification | None in V1; data model doesn't block it later | No stated business-model intent yet |

---

# 1. Product Vision

MarketingOS is the professional operating system for marketing — the single reference and toolset a professional keeps open across their entire career, spanning Marketing Strategy, Performance Marketing, Media Buying, E-commerce, Growth, Analytics, Creative Strategy, Copywriting, Consumer Psychology, CRM, SEO, Content Creation, Brand, and Marketing Finance/Leadership.

It unifies four things that normally live in disconnected tools: **theory** (why it works), **practice** (SOPs/templates/calculators to execute now), **diagnosis** (decision trees/troubleshooting for when something's broken), and **progression** (a real Beginner→Expert ladder, identical across every domain).

**Positioning:** *For marketing professionals at every level, MarketingOS replaces a scattered stack of blog posts, spreadsheets, and outdated courses with one structured, always-current, actually-usable knowledge and tooling platform.*

**What it is not:** a blog, a graded LMS, a social/community platform, a live ad-account integration, or a general business wiki. See `KNOWLEDGE_ARCHITECTURE.md` for full scope boundaries.

---

# 2. Product Goals

Year-one goals, stated so they're falsifiable — a Senior PM writes goals that can fail, not aspirations:

| Goal | Definition of done |
|---|---|
| **G1 — Prove the model, not just plan it** | 3 flagship domains (Assumption #2) built Beginner→Expert, with all 11 content types represented, used for real work at least weekly |
| **G2 — Be the first stop, not the last resort** | Return-visit rate and tool-invocation rate (§11) establish MarketingOS as a standing reference, not a one-time read |
| **G3 — Never silently go stale** | 100% of published content has a source or explicit "practitioner opinion" label and a visible `last_reviewed` date; 0% of content is past its governance SLA (`CONTENT_GOVERNANCE.md §2`) undetected |
| **G4 — Architect once for 14 domains, not 3** | The platform skeleton (content layer, tool engine, search, personalization) handles Phase 1's 3 domains without any structural change required to add domains 4–14 |
| **G5 — Utility beats reading** | At maturity, sessions ending in a calculator use / template download / SOP copy outnumber sessions that are read-only |

---

# 3. Target Users

Three usage modes, twelve personas (full detail in §4):

| Mode | Personas | Primary need |
|---|---|---|
| **Execute** | Media Buyer, Performance Marketer, CRM Specialist, Content Creator, Copywriter | Fast, in-the-moment tools: calculators, SOPs, checklists, troubleshooting |
| **Design & Manage** | Marketing Manager, E-commerce Manager, Growth Marketer, Brand Manager | Frameworks, decision models, case studies, planning templates |
| **Direct & Own** | Marketing Director, Business/Agency Owner | Strategic frameworks, cross-domain fluency to evaluate teams/vendors, finance-of-marketing literacy |

---

# 4. User Personas

Each persona: context, goals, frustrations with the status quo, primary jobs-to-be-done, primary/secondary domains (cross-referenced with `KNOWLEDGE_ARCHITECTURE.md §2`).

### 4.1 Mona — Media Buyer / Performance Marketer
- **Context:** Runs paid social + search budgets for 3–5 client accounts. Works fast, works often after-hours when something breaks.
- **Frustrations:** Knowledge is scattered across Twitter threads, old blog posts, and tribal Slack knowledge; benchmarks are outdated the moment she finds them.
- **JTBD:** *"When my ROAS drops 30% overnight, I want a diagnostic flow, not a 2,000-word article, so I can find the cause in minutes."*
- **Domains:** Performance Marketing (primary), Analytics, Creative Strategy (secondary).

### 4.2 Karim — Marketing Manager
- **Context:** Owns quarterly planning for a mid-size brand's marketing function.
- **Frustrations:** Starts every plan from a blank doc; no consistent internal framework library.
- **JTBD:** *"When I plan next quarter, I want a proven framework and a fillable template, so I'm not reinventing structure every time."*
- **Domains:** Marketing Strategy, Content, Brand (primary); Analytics, CRM (secondary).

### 4.3 Yara — E-commerce Manager
- **Context:** Owns a DTC brand's P&L across channels.
- **Frustrations:** Can't quickly model whether a new channel is worth the budget before committing.
- **JTBD:** *"When evaluating a new channel, I want to model CAC/LTV before I commit budget."*
- **Domains:** E-commerce, Performance Marketing, CRM (primary); Finance, Analytics (secondary).

### 4.4 Tarek — Growth Marketer
- **Context:** Runs a weekly experimentation cadence across funnel stages.
- **Frustrations:** No repeatable SOP for experiment design; results get lost, mistakes repeat.
- **JTBD:** *"When I run an experiment, I need an SOP/checklist so nothing gets missed and I can move fast without re-deriving process."*
- **Domains:** Growth, Analytics, Psychology (primary); Performance Marketing, Content (secondary).

### 4.5 Salma — CRM Specialist
- **Context:** Owns lifecycle email/SMS for a subscription business.
- **Frustrations:** Copy and flow design leans on gut feel; no psychology-backed framework to justify choices.
- **JTBD:** *"When I design a lifecycle flow, I want proven templates and psychology-backed copy frameworks."*
- **Domains:** CRM, Copywriting, Psychology (primary); Analytics (secondary).

### 4.6 Nadia — Content Creator
- **Context:** Produces short-form and long-form content across owned channels.
- **Frustrations:** Hard to know which content frameworks are current vs. outdated platform advice.
- **JTBD:** *"When I plan content, I want frameworks that connect to actual discovery/SEO mechanics, not vibes."*
- **Domains:** Content Creation, Copywriting, SEO (primary); Brand, Psychology (secondary).

### 4.7 Omar — Copywriter
- **Context:** Writes direct-response and brand copy across formats.
- **Frustrations:** Swipe files exist but aren't connected to the psychology principles that explain *why* they work.
- **JTBD:** *"When I write high-converting copy, I want frameworks plus the psychology behind them, not just examples to imitate blindly."*
- **Domains:** Copywriting, Psychology, Brand (primary); Content Creation (secondary).

### 4.8 Layla — Brand Manager
- **Context:** Owns brand positioning and creative consistency.
- **Frustrations:** Brand strategy feels disconnected from performance metrics — hard to defend brand investment internally.
- **JTBD:** *"When I position a brand, I want frameworks that connect positioning to performance outcomes I can defend in a budget meeting."*
- **Domains:** Brand, Marketing Strategy, Creative Strategy (primary); Psychology, Finance (secondary).

### 4.9 Hassan — Marketing Director
- **Context:** Owns the marketing org's strategy and budget; manages managers.
- **Frustrations:** Needs enough fluency across every discipline to direct specialists and defend budget to the C-suite, but has no time to become deep-expert in all of them.
- **JTBD:** *"When I set strategy, I want cross-domain frameworks and enough finance literacy to translate marketing plans into business outcomes."*
- **Domains:** Marketing Strategy, Finance, Business/Leadership (primary); all others at breadth-over-depth.

### 4.10 Rania — Business / Agency Owner
- **Context:** Runs an agency or owns a business that depends on marketing but isn't a marketing specialist.
- **Frustrations:** Can't evaluate whether agency/freelancer output is actually good; gets sold jargon.
- **JTBD:** *"When I evaluate agency deliverables or hire, I want to quickly learn enough to ask the right questions and judge output quality."*
- **Domains:** Business/Leadership, Finance, Marketing Strategy (primary); all others at breadth-over-depth.

### 4.11 & 4.12 — Additional execute-mode personas
Two further personas share the "Execute" mode pattern of Mona/Salma/Omar closely enough to reuse their JTBD shape rather than duplicate full cards: a **second CRM/Lifecycle specialist focused on push/SMS specifically**, and a **Paid Search specialist** within the Performance Marketing persona family (Google Ads/PMax vs. Mona's paid-social lean). Both are covered by the same Performance Marketing / CRM domain content — flagged here so the persona count matches the taxonomy's twelve without inflating this section with near-duplicate cards.

---

# 5. Problems Solved

1. **Fragmentation** — knowledge for one discipline is spread across dozens of blogs, courses, PDFs, and Slack DMs with no single source of truth.
2. **Staleness without warning** — content (especially benchmarks) goes out of date silently; readers can't tell if what they're reading is still true.
3. **Theory without execution** — most marketing content explains concepts but doesn't hand the reader a usable SOP, template, or calculator to act on it immediately.
4. **No real progression model** — "beginner" and "advanced" content exist but aren't structured as a coherent ladder within or across disciplines.
5. **No diagnostic layer** — when something breaks (ROAS drops, open rates crash), there's no fast, self-sufficient troubleshooting path; the reader has to reconstruct a diagnosis from theory articles under time pressure.
6. **Cross-domain literacy gap** — managers/directors/owners need working fluency across disciplines they don't specialize in, but most resources are written for specialists only.
7. **Unsourced claims** — benchmark numbers and "best practices" circulate without citation, making it impossible to judge trustworthiness.

---

# 6. Features

Grouped by system area (full technical detail in `SYSTEM_DESIGN.md`):

**Content System**
- Structured, typed content items across 11 content types (`KNOWLEDGE_ARCHITECTURE.md §3`)
- Domain → Topic → Module hierarchy across 14 domains
- Skill-level tagging (Beginner→Expert) on every item
- Prerequisite and related-item cross-linking (knowledge graph, not a tree)
- Source citation and freshness (`last_reviewed`) on every item

**Tool Engine**
- Interactive calculators (CAC/LTV, ROAS/breakeven, budget pacing, media mix, and per-domain calculators)
- Downloadable/fillable templates (briefs, media plans, sequences, calendars)
- Decision-tree / troubleshooting interactive flows

**Discovery**
- Full-text + faceted search (domain/topic/type/level/tag)
- Six parallel navigation models (by domain, level, role, content type, problem/search, job-to-be-done) — `INFORMATION_ARCHITECTURE.md §1`
- Curated Role Paths and Level Paths (`KNOWLEDGE_ARCHITECTURE.md §5`)

**Personalization**
- Role + skill-level onboarding, explicit (not inferred) in V1
- Personal library: bookmarks, saved calculator results, per-domain progress
- Personalized home/dashboard (§21)

**Governance / Admin**
- Draft → in-review → published → deprecated content workflow
- Freshness SLA tracking and flagging
- Author/reviewer accountability fields

---

# 7. Feature Priorities

MoSCoW, mapped to `ROADMAP.md` phases:

| Priority | Features | Phase |
|---|---|---|
| **P0 — Must have (MVP)** | Content item template + 11 content types; Domain/Topic/Module hierarchy for 3 flagship domains; core calculators (CAC/LTV, ROAS/breakeven, budget pacing); full-text + faceted search; universal content-item page template; domain hub page; onboarding (role + level); content validation against metadata schema; draft/review/publish workflow | Phase 1 |
| **P1 — Should have** | Role Paths & Level Paths; personal library (bookmarks/progress); remaining 11 domains; expanded tool library; non-engineer content authoring UI | Phase 2 |
| **P2 — Could have** | Semantic/NL search; adaptive path recommendations; feedback-loop instrumentation ("this changed a decision") | Phase 3 |
| **P3 — Won't have (yet)** | Live ad-account/benchmark data integrations; offline/mobile app; certification credentials; multi-tenant accounts | Phase 4 / explicitly deferred |

---

# 8. User Stories

Format: *As a [persona], I want [capability], so that [outcome].* Grouped by feature area, IDs for traceability to Functional Requirements in §9.

**Content consumption**
- US-01: As Mona (Media Buyer), I want a troubleshooting guide I can use without reading theory first, so I can fix a live campaign issue fast.
- US-02: As Karim (Marketing Manager), I want a framework with a fillable template attached, so I don't start planning from a blank page.
- US-03: As any user, I want every content page to show its skill level and last-reviewed date, so I can judge whether it applies to me and whether it's current.
- US-04: As Nadia (Content Creator), I want related content and prerequisites linked from every article, so I can go deeper or fill gaps without searching manually.

**Tools**
- US-05: As Yara (E-commerce Manager), I want a CAC/LTV calculator with plain-language interpretation of my result, so I can decide on a new channel without building my own spreadsheet.
- US-06: As Mona, I want calculator results to link to the relevant troubleshooting guide when my number is bad, so I get a next step, not just a number.
- US-07: As any returning user, I want to save a calculator result to my library, so I can reference it later without recomputing.

**Navigation & discovery**
- US-08: As Rania (Business Owner), I want to browse a domain by its Beginner→Expert curriculum map, so I can quickly get fluent enough to evaluate my agency.
- US-09: As any user, I want to search "ROAS dropped" and land on a troubleshooting guide, not a generic theory article, so I get to a fix fast.
- US-10: As a new user, I want to select my role and level at onboarding, so my home page and domain hubs are pre-filtered to what's relevant.
- US-11: As Hassan (Marketing Director), I want a role-based curated path spanning multiple domains, so I get cross-domain fluency without hunting domain by domain.

**Personal layer**
- US-12: As a returning user, I want to see my progress ladder per domain, so I know what I've covered and what's next.
- US-13: As a returning user, I want a "continue where I left off" prompt on my home page, so I don't lose my place between sessions.
- US-14: As any user, I want to bookmark content and tools, so I can build my own quick-reference set over time.

**Content governance (author-facing)**
- US-15: As the content author/owner, I want new content to fail validation if required metadata (skill level, sources, review date) is missing, so nothing incomplete gets published.
- US-16: As the content author/owner, I want content flagged automatically when it passes its freshness SLA, so staleness doesn't go unnoticed.
- US-17: As a future contributor, I want a review workflow (draft → in-review → published) that maps to a PR-style diff review, so my contribution can be checked before going live.

---

# 9. Functional Requirements

Numbered `FR-XXX`, grouped by system area. "Shall" = must; "should" = should but not blocking.

**Content**
- FR-001: The system shall render every content item through a single consistent template regardless of type, varying only the body structure per type.
- FR-002: The system shall reject publishing any content item missing a required metadata field (`skill_levels`, `domain`/`topic`/`module`, `type`, `last_reviewed`, `status`).
- FR-003: The system shall support bidirectional-feeling cross-links (`prerequisites`, `related_items`, `applies_to_calculators`, `applies_to_templates`) independent of the authoring hierarchy.
- FR-004: The system shall display `last_reviewed` date and source citations (or an explicit "practitioner opinion" label) on every content item.
- FR-005: The system shall support content lifecycle states `draft`, `in_review`, `published`, `deprecated`, with only `published` content indexed/browsable.

**Tools (Calculators)**
- FR-010: The system shall provide a shared calculator contract (typed input schema, pure compute function, output/interpretation spec) that all calculators implement.
- FR-011: Calculators shall recompute results on input change without requiring an explicit submit action, where computation is inexpensive.
- FR-012: Calculator results shall include a plain-language interpretation, not a bare number, and link to related content when thresholds indicate a problem.
- FR-013: The system shall allow a signed-in user to save a calculator result (inputs + outputs + timestamp) to their personal library.

**Search & Discovery**
- FR-020: The system shall provide full-text search across all published content with facet filters for domain, topic, type, skill level, and tag.
- FR-021: The system shall support curated query→content mappings so common problem-phrased queries resolve to the correct troubleshooting/decision-tree content.
- FR-022: The search index shall be rebuildable from the content layer at any time without content-layer changes (index is a derived projection, not a source of truth).

**Navigation & Paths**
- FR-030: The system shall expose all six navigation models (domain, level, role, content type, search, job-to-be-done) as first-class entry points, not nested behind a single menu.
- FR-031: The system shall support curated, ordered Learning Paths that span multiple domains.
- FR-032: Domain hub pages shall render a visual Beginner→Expert curriculum map.

**Personalization**
- FR-040: The system shall allow a user to explicitly set and change their role and per-domain skill level at any time.
- FR-041: The system shall use stated role/level to pre-filter onboarding output and sort (not hide) search/browse results.
- FR-042: The system shall track per-user bookmarks, saved calculator results, and per-domain progress.

**Governance**
- FR-050: The system shall flag any published content item whose `last_reviewed` date exceeds its type's freshness SLA (`CONTENT_GOVERNANCE.md §2`).
- FR-051: The system shall retain `deprecated` content (not delete it) for link integrity, excluded from search/browse and visibly marked when reached via a stale link.

---

# 10. Non-functional Requirements

Numbered `NFR-XXX`.

| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Performance | Content pages are cacheable/pre-renderable; a content page load should not require a personalization round-trip to render the core content |
| NFR-02 | Performance | Calculator recompute-on-input shall feel instantaneous (client-side compute, no network round-trip per keystroke) |
| NFR-03 | Availability | Read path (content browsing/search) should degrade gracefully if the personalization layer is unavailable — a logged-out-equivalent experience, not an error page |
| NFR-04 | Accessibility | All content templates and calculator forms conform to WCAG AA as a baseline, not a phase-gated feature |
| NFR-05 | Security | Personalization/account layer is the only component holding user PII; content layer holds no user data, minimizing breach blast radius |
| NFR-06 | Maintainability | Adding a new calculator shall not require modifying any existing calculator's code (registry pattern, per `SYSTEM_DESIGN.md §4`) |
| NFR-07 | Maintainability | Adding a new domain shall not require structural changes to the content schema, tool engine, search layer, or personalization layer |
| NFR-08 | Data integrity | Content validated against the metadata schema at publish time; invalid content cannot reach `published` state |
| NFR-09 | Internationalization | Schema reserves a `locale` field even though V1 ships English-only (Assumption #4), so adding a language later doesn't require a schema migration |
| NFR-10 | Auditability | Every content item's authorship, review history, and status transitions are traceable (git history satisfies this per `SYSTEM_DESIGN.md §3`) |
| NFR-11 | Browser support | Modern evergreen browsers (Chrome, Safari, Firefox, Edge, current + 1 prior major version); no legacy IE support |
| NFR-12 | Mobile | Calculators and troubleshooting flows must be usable (not just viewable) on mobile viewports; dense curriculum maps may be desktop-optimized |

---

# 11. Success Metrics

| Category | Metric | Target signal |
|---|---|---|
| Coverage | % of taxonomy (domain × topic × module) with published content per skill level | Track weekly during Phase 1–2; north star for "complete reference" claim |
| Usage | Returning-visit rate; tool invocations per user per week | Growing week-over-week post-Phase-1 launch |
| Utility | % of sessions ending in template download / calculator use / SOP copy vs. read-only | Trending toward parity or majority-utility, validating "not a blog" |
| Trust | % of content within governance freshness SLA | Sustained ~100%; any drop is a defect, not a KPI to "manage" |
| Outcome | Self-reported "this changed a decision I made at work" (feedback prompt) | Present and collected from Phase 1 onward, even if V1 volume is low |
| Search | % of searches resulting in a content view with no immediate re-search | High is good; track separately for problem-phrased vs. browse-style queries |

---

# 12. Risks

Risk register: likelihood/impact each High/Medium/Low, with mitigation.

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Scope creep across 14 domains before any domain is proven** | High | High | Hard phase gate in `ROADMAP.md`: Phase 2 does not start until Phase 1's 3 domains meet exit criteria |
| **Single-author bottleneck stalls content velocity** | High | Medium | Governance workflow (draft/review/publish) designed for multi-contributor from day one even though V1 is single-author (`CONTENT_GOVERNANCE.md §4`); Phase 2 opens contribution |
| **Content goes stale silently, eroding trust** | Medium | High | Freshness SLA + visible `last_reviewed` date + automated staleness flagging (FR-050) |
| **Calculator formula errors lead to bad real-world business decisions** | Low | High | Calculators require source/derivation citation like any content item; compute functions are pure and unit-testable in isolation (`SYSTEM_DESIGN.md §4`); Phase 1 calculators get explicit correctness review before publish |
| **Search relevance fails for problem-phrased queries, undermining the "3am troubleshooting" use case** | Medium | Medium | Curated query→content mappings for V1 (FR-021) ahead of investing in semantic search; success metric tracked explicitly in §11 |
| **Over-architecting before the content model is validated with real usage** | Medium | Medium | Phase 1 deliberately scoped to 3 domains specifically to validate before scaling the architecture's assumptions |
| **Personalization built on too little behavioral data produces bad recommendations** | Medium | Low | V1 personalization is explicit (user-stated role/level), not inferred; adaptive/behavioral personalization deliberately deferred to Phase 3 |
| **Opening contribution too early dilutes quality** | Low (V1) / Medium (Phase 2) | Medium | Review workflow gate (`in_review` state) is mandatory before any contributor's content reaches `published`, regardless of contributor count |
| **Low adoption — built but not used as a daily reference** | Medium | High | G2/G5 (§2) and the utility-vs-read metric (§11) are tracked from Phase 1 launch specifically to catch this early, not at Phase 4 |

---

# 13. Future Expansion

Beyond `ROADMAP.md` Phase 4:

- **AI-assisted diagnostic chat** over the knowledge graph — natural-language Q&A that cites and links back into the structured content, rather than generating unsourced answers.
- **Live benchmark data feeds** replacing periodically-refreshed static benchmark tables.
- **Certification-style path completion**, if validated as wanted (business-model question, not assumed — see Assumption #5).
- **Multi-tenant team/agency accounts** — shared bookmarks, team progress dashboards, internal contribution for a company's own playbooks layered on top of MarketingOS's core content.
- **API access** for pulling calculators/frameworks into other internal tools.
- **Offline/mobile app** for field reference.
- **Community layer** (explicitly out of scope through Phase 4; revisit only after the reference-quality product is proven, to avoid diluting content trust with unmoderated contribution).

---

# 14. Information Architecture

Full detail in `INFORMATION_ARCHITECTURE.md`. Summary: content is authored as a strict tree (Domain→Topic→Module→Item, per §16) but navigated as a graph through six parallel entry models (§15), because different users think about the same content differently depending on whether they're studying, executing, or diagnosing.

Site map:

```
/                          Home — role/level-aware entry point
/domains                   Domain index
/domains/:domain           Domain hub — curriculum map, key frameworks, tools
/domains/:domain/:topic    Topic page
/item/:id                  Universal content item template
/tools                     All calculators/interactive tools
/tools/:calculator         Calculator experience
/templates                 All templates
/troubleshoot              Decision-tree / troubleshooting entry
/paths                     Learning paths index
/paths/:path               Guided path player
/search?q=                 Universal search
/glossary                  Glossary index + lookup
/library                   Personal layer: bookmarks, progress, saved results
/account                   Profile, role/level settings
```

---

# 15. Navigation

Six parallel models, all first-class (not nested under a single "Browse" menu):

| Model | Entry question | Primary users |
|---|---|---|
| By Domain | "Show me everything about Performance Marketing" | Explorers, researchers |
| By Skill Level | "I'm Intermediate — what's my curriculum?" | Deliberate learners |
| By Role | "I'm a Media Buyer — curate this for me" | New users at onboarding |
| By Content Type | "I just need a calculator/template/checklist" | Mid-task, high urgency |
| By Problem (search) | "My ROAS dropped" | Mid-crisis or mid-decision |
| By Job-to-be-done | "I'm planning next quarter" | Users starting a defined project |

Primary nav bar composition: persistent search (always visible, not an icon-only affordance), Domains, Tools, Paths, Library. Breadcrumbs on every content page reflect the authoring hierarchy (Domain > Topic > Module) even when the user arrived via search or a cross-link, so orientation is never lost regardless of entry model.

---

# 16. Knowledge Taxonomy

14 domains, each decomposed Domain → Topic → Module → Content Item (full schema in `KNOWLEDGE_ARCHITECTURE.md §1–4`):

1. Marketing Strategy & Foundations
2. Performance Marketing & Media Buying
3. E-commerce & DTC
4. Growth Marketing
5. Analytics & Data
6. Creative Strategy & Ad Creative
7. Copywriting & Messaging
8. Consumer Psychology & Behavioral Economics
9. CRM & Lifecycle Marketing
10. SEO & Organic Discovery
11. Content Creation & Content Marketing
12. Brand Marketing
13. Marketing Finance & Unit Economics
14. Business & Leadership for Marketers

Skill ladder (identical vocabulary across all 14 domains, operational definitions in `KNOWLEDGE_ARCHITECTURE.md §3` / PRD v1.0): Beginner → Intermediate → Advanced → Senior → Expert.

---

# 17. Learning Paths

Two types (`KNOWLEDGE_ARCHITECTURE.md §5`):

- **Role Paths** — curated per persona (e.g., "Media Buyer: Beginner → Advanced"), spanning the persona's primary + secondary domains per the matrix in `KNOWLEDGE_ARCHITECTURE.md §2`.
- **Level Paths** — domain-agnostic, "everything a marketer needs to reach Intermediate across foundational domains," for generalists early in career.

V1 paths are curated by the content owner, not auto-generated — adaptive/behavior-based path generation is a Phase 3 capability (§13/`ROADMAP.md`). A path is simply an ordered list of content-item references that can cross domain boundaries; no separate content is authored for a path beyond the ordering and framing copy.

---

# 18. Content Categories

11 content types, each with a distinct authoring template and UI rendering (full detail `KNOWLEDGE_ARCHITECTURE.md §3`):

| # | Type | Purpose |
|---|---|---|
| 1 | Theory / Concept | Explain why; build mental models |
| 2 | Framework | Reusable structured methodology |
| 3 | Calculator | Inputs → decision-ready number, instantly |
| 4 | SOP | Repeatable execution, zero ambiguity |
| 5 | Checklist | Pre-flight / QA gate |
| 6 | Decision Tree | Diagnose or choose under uncertainty |
| 7 | Template | Reusable, fillable artifact |
| 8 | Case Study | Theory grounded in a real, numbers-backed example |
| 9 | Benchmark | Comparative reference data, sourced and dated |
| 10 | Troubleshooting Guide | Fix a known-broken state fast |
| 11 | Glossary Term | Fast definition lookup |

Design rule: Decision Trees and Troubleshooting Guides must never require reading a Theory item first — they link out to Theory/Frameworks for readers who want the "why" afterward, not as a prerequisite.

---

# 19. Internal Linking Strategy

Every content item carries structured, typed links (not free-text hyperlinks embedded in prose alone):

- **`prerequisites`** — items a reader should understand first; powers "read this first" prompts and path sequencing.
- **`related_items`** — cross-links independent of hierarchy position; this is what makes the content a graph rather than a tree, and is the primary mechanism for the "no dead ends" UX principle (`INFORMATION_ARCHITECTURE.md §6`).
- **`applies_to_calculators` / `applies_to_templates`** — explicit links from theory/framework content to the tools that operationalize them, and back (a calculator links to the framework it implements).
- **Troubleshooting → SOP** links — every diagnosed fix links to the SOP/Checklist that prevents recurrence.

**Rules enforced at publish time (extends FR-002/NFR-08):**
1. No orphan content — every published item must have at least one inbound link (from a domain/topic index, a related-items link, or a path) or it fails validation; unreachable content defeats the "no dead ends" principle before a user ever hits it.
2. Cross-domain links are allowed and expected (e.g., a Copywriting Framework linking to a Psychology Theory item) — the graph is not domain-siloed.
3. Link integrity is checked on every content build; a broken internal link fails validation the same as a missing metadata field.
4. A periodic link audit (governance task, `CONTENT_GOVERNANCE.md`) checks for content that has inbound links only from `deprecated` items, which behaves like an orphan in practice even though it technically has an inbound link.

---

# 20. Search Strategy

- **Indexing:** full-text + faceted index (domain/topic/module/type/skill_levels/tags) derived from the content layer, rebuilt on every publish — a projection, never the source of truth (FR-022), so it can be replaced (e.g., with semantic search in Phase 3) without touching content.
- **Ranking signals (V1):** exact/partial text match; skill-level match to the user's stated level (boost, not filter); freshness (recently reviewed content ranks slightly above stale-but-not-yet-deprecated content of otherwise equal relevance); type-priority override for problem-phrased queries (a query pattern matching known troubleshooting phrasing ranks Troubleshooting Guides/Decision Trees above Theory items even at equal text-match score).
- **Facets:** domain, topic, type, skill level, tag — all combinable.
- **Curated query mappings:** hand-authored query→content overrides for known high-value problem queries (e.g., "ROAS dropped," "email open rate low") ahead of investing in semantic search (FR-021).
- **Phase 3 evolution:** semantic/vector search for natural-language problem queries, replacing/augmenting curated mappings as query volume and variety grow beyond what curation can cover.
- **Search is persistent UI**, not a hidden icon (§15) — reflecting that "by problem" is a top-frequency navigation model, not an edge case.

---

# 21. Dashboard Layout

The personalized Home (`/`) is the primary return-visit surface — it must justify the "operating system I keep open" positioning within one screen, no scrolling required to see the first useful thing.

```
┌─────────────────────────────────────────────────────────────────┐
│  [Persistent search bar — full width]                            │
├─────────────────────────────────────────────────────────────────┤
│  Continue where you left off                                     │
│  [Last-viewed content item card, with % progress if a path]      │
├───────────────────────────────┬───────────────────────────────────┤
│  Your domains — progress       │  Quick tools                       │
│  ladder (per stated role's     │  [Top 4–6 calculators/templates    │
│  primary domains, per §4)      │   relevant to stated role]         │
│  [Beginner→Expert bar per      │                                    │
│   domain, current position     │                                    │
│   marked]                      │                                    │
├───────────────────────────────┴───────────────────────────────────┤
│  Recommended next                                                  │
│  [2–3 content-item cards: next module in progress, or a Role Path  │
│   step, curated not adaptive in V1 — see §17]                      │
├─────────────────────────────────────────────────────────────────┤
│  Recently viewed                    │  Bookmarks                    │
│  [horizontal scroll of last 5–8]    │  [pinned items, up to 6]      │
└─────────────────────────────────────┴────────────────────────────┘
```

Design intent: the top-left "continue where you left off" and top-right "quick tools" are the two highest-frequency return-visit actions (per the utility-over-reading principle, §2 G5) and are placed above the fold; the curriculum-ladder and recommendation rails are secondary, discovery-oriented content.

---

# 22. Component List

Shared design-system components (`SYSTEM_DESIGN.md §7` names this package `design-system`), listed by where they're used:

**Badges / Metadata**
- `TypeBadge` (one of the 11 content types)
- `SkillLevelBadge` (Beginner…Expert, supports multi-level)
- `FreshnessIndicator` (last-reviewed date + SLA-flag state)

**Content surfaces**
- `ContentItemTemplate` (the universal page shell, §14/`INFORMATION_ARCHITECTURE.md §3.3`)
- `ContentCard` (compact preview used in search results, related-content rails, domain hub lists)
- `RelatedContentRail`
- `SourceCitationList`
- `PrerequisiteBanner` ("read this first")

**Domain / curriculum**
- `DomainHubHeader`
- `CurriculumMap` (visual Beginner→Expert ladder)
- `TopicList` / `ModuleList` (expandable)

**Tools**
- `CalculatorInputField` (typed: number/currency/percentage/select, with validation)
- `CalculatorResultPanel` (result + plain-language interpretation + related-content links)
- `TemplateDownloadCard`

**Diagnostics**
- `DecisionTreeNode` (single question, branching options, back navigation)
- `TroubleshootingOutcomePanel` (diagnosis + ranked causes + fix link + "prevent this" link)

**Discovery**
- `SearchBar` (persistent, global)
- `FacetFilterPanel`
- `SearchResultList`

**Paths & progress**
- `PathPlayer` (ordered step navigator)
- `ProgressLadder` (per-domain, reused on dashboard and domain hub)

**Personalization**
- `OnboardingRoleSelector`
- `OnboardingLevelSelector`
- `BookmarkButton`
- `RecentlyViewedRail`

**Navigation**
- `PrimaryNavBar`
- `Breadcrumb`

---

# 23. Folder Structure

Conceptual monorepo layout implementing the five layers from `SYSTEM_DESIGN.md §2` as package/service boundaries. Exact tooling choices remain deferred to implementation planning — this is the shape, not the stack:

```
marketingos/
├── apps/
│   └── web/                       # Presentation layer — the user-facing app
├── packages/
│   ├── content/                   # Content package: schema, validation, content-graph queries
│   ├── tool-engine/                # Calculator/template contract + registry
│   ├── search/                     # Index build + query resolution
│   ├── personalization/            # Account/profile/bookmarks/progress service
│   └── design-system/              # Shared components listed in §22
├── content/                        # The structured content store itself (git-backed, SYSTEM_DESIGN.md §3)
│   └── domains/
│       ├── performance-marketing/
│       │   └── meta-ads/
│       │       ├── account-structure.md
│       │       └── troubleshooting-frequency-cap.md
│       ├── analytics-and-data/
│       └── copywriting-and-messaging/
├── docs/                           # This blueprint/PRD document set
└── README.md
```

---

# 24. File Structure

**Content files** — one file per content item, path encodes Domain/Topic (Module expressed via frontmatter, not nesting, to avoid overly deep paths as modules grow):

```
content/domains/<domain-slug>/<topic-slug>/<item-slug>.md
```

Each content file's frontmatter mirrors the metadata schema (`KNOWLEDGE_ARCHITECTURE.md §4`) exactly:

```yaml
---
id: perf-mktg-meta-ads-troubleshoot-frequency
type: troubleshooting_guide
domain: performance-marketing
topic: meta-ads
module: troubleshooting-diagnostics
title: "Frequency cap suppressing reach — troubleshooting guide"
summary: "Diagnose and fix reach drops caused by audience frequency saturation."
skill_levels: [intermediate, advanced]
prerequisites: []
related_items: [perf-mktg-meta-ads-audience-targeting, perf-mktg-benchmarks-frequency-by-industry]
applies_to_calculators: [budget-pacing-calculator]
tags: [meta-ads, frequency, reach, troubleshooting]
sources:
  - "Meta Ads Manager documentation, accessed 2026-06"
author: "<owner>"
reviewer: "<owner>"
last_reviewed: 2026-07-01
status: published
---
```

**Calculator modules** — one module per calculator, implementing the shared contract from `SYSTEM_DESIGN.md §4`:

```
packages/tool-engine/calculators/<calculator-slug>/
├── schema.ts        # typed input schema
├── compute.ts        # pure compute function, unit-testable in isolation
├── interpret.ts       # output/interpretation + threshold-based content links
└── metadata.ts        # domain/topic/skill_levels/related content, same shape as content metadata
```

**Component files** — one component per file in `design-system`, named identically to the component list in §22 (e.g., `CalculatorResultPanel.tsx`), co-located with its own styles/tests rather than split across parallel directories.

---

# 25. Database Structure (if needed)

**Needed — yes, for the Personalization layer only** (per `SYSTEM_DESIGN.md §6`). Content itself is *not* database-backed (it's git-backed structured files, §23/§24) — the database exists solely for real per-user transactional state, keeping the two systems' release cycles and failure domains separate (NFR-05).

Conceptual relational schema:

```
users
├── id (pk)
├── email
├── created_at
└── auth fields (deferred to implementation — depends on Assumption #1's resolution)

user_domain_level
├── user_id (fk → users.id)
├── domain (matches content taxonomy slug, §16)
├── skill_level (Beginner…Expert)
└── updated_at

user_role
├── user_id (fk → users.id)
└── role (one of the 12 personas / "generalist")

bookmarks
├── id (pk)
├── user_id (fk → users.id)
├── content_item_id (references content-layer id, not a DB fk — content lives outside this database)
└── created_at

progress
├── id (pk)
├── user_id (fk → users.id)
├── content_item_id
├── status (viewed / completed)
└── updated_at

saved_calculator_results
├── id (pk)
├── user_id (fk → users.id)
├── calculator_id
├── inputs (jsonb)
├── outputs (jsonb)
└── created_at

path_progress
├── id (pk)
├── user_id (fk → users.id)
├── path_id
├── current_step_index
└── updated_at
```

Note: `content_item_id`/`calculator_id`/`path_id` are references to IDs defined in the content layer (§24's frontmatter `id` field), not foreign keys enforced by this database — the two systems are deliberately decoupled (per `SYSTEM_DESIGN.md §2`'s "content and user data are separate systems" decision), so a content item can be renamed/moved without a database migration, at the cost of the database not being able to enforce referential integrity against content IDs at the schema level. This tradeoff is accepted because content changes far more often than the personalization schema.

---

# 26. Scalability Plan

| Dimension | Approach |
|---|---|
| **Content volume** (→ thousands of items across 14 domains) | Git-backed flat files scale fine into the tens of thousands without infrastructure changes; the search index (a derived projection, §20) is what actually needs to scale for query performance, and it can be rebuilt/resized independently of the content store |
| **Domain rollout** | Phased per `ROADMAP.md` — Phase 1 validates the model on 3 domains before Phase 2 replicates it across 11 more, so scaling mistakes are caught at small scale, not large |
| **Read traffic** | Read-heavy by nature (NFR-01); content pages are cacheable/pre-renderable, so read scaling is primarily a caching/CDN concern, not a database-scaling concern, because content isn't in a database at all |
| **Write traffic (content)** | Low-frequency, human-paced (editorial publishing, not user-generated at volume) — no write-scaling concern for the content layer |
| **Write traffic (personalization)** | Conventional relational scaling (read replicas, connection pooling) only becomes relevant at real multi-user scale (Assumption #1); V1 single-owner usage has negligible load |
| **Search** | Index is rebuildable and swappable independently (FR-022); moving from keyword to semantic search (Phase 3) is a search-package-only change, touching neither content nor personalization |
| **Contributor scaling** | Governance workflow (draft/review/publish, `CONTENT_GOVERNANCE.md`) is designed for multi-contributor from day one even in a single-author V1, so opening contribution in Phase 2 is a process change, not a re-architecture |
| **Team/multi-tenant scaling** | Explicitly deferred (Assumption #1, §13 Future Expansion) — the personalization schema (§25) is already scoped per-user, so adding an `organization_id` layer later is additive rather than a redesign, but is not built now |
| **Internationalization scaling** | `locale` field reserved in the metadata schema now (NFR-09) even though unused in V1, so adding a language later is a content-authoring effort, not a schema migration |

---

# Cross-references

This PRD is self-contained but intentionally not duplicative of implementation-level detail already covered in:
- `KNOWLEDGE_ARCHITECTURE.md` — full content-type authoring templates, per-domain topic/module breakdowns as they're planned
- `INFORMATION_ARCHITECTURE.md` — full UX flow detail (onboarding, calculator flow, troubleshooting flow)
- `SYSTEM_DESIGN.md` — architectural rationale and trade-offs behind §23–26 above
- `CONTENT_GOVERNANCE.md` — full quality bar, style guide, freshness SLA table
- `ROADMAP.md` — phase-by-phase sequencing this PRD's priorities (§7) map to

**Still no code has been written.** This PRD is the complete pre-implementation reference; the next step, per your original instruction, is Phase 1 implementation planning — which should not begin until you've reviewed this and confirmed or corrected the five assumptions at the top.
