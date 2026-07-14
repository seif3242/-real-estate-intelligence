# MarketingOS — Information Architecture & UX

## Version 1.0 (Blueprint Stage)

The [`KNOWLEDGE_ARCHITECTURE.md`](./KNOWLEDGE_ARCHITECTURE.md) document defines how content is *authored* (a tree). This document defines how users actually *navigate and use* it — which is a graph accessed through several different entry models, because a Media Buyer at 11pm with a broken campaign and a Marketing Director planning next quarter's strategy do not think about the same content the same way.

---

# 1. Navigation Models

MarketingOS exposes six parallel ways into the same content graph. Every content item is reachable from all applicable models — there is no single "correct" path.

| # | Model | Entry question | Primary users |
|---|---|---|---|
| 1 | **By Domain** | "Show me everything about Performance Marketing" | New users exploring, researchers |
| 2 | **By Skill Level** | "I'm an Intermediate performance marketer — what's my curriculum?" | Learners on a deliberate path |
| 3 | **By Role** | "I'm a Media Buyer — curate this for me" | New users at onboarding |
| 4 | **By Content Type** | "I just need a calculator / template / checklist" | Users mid-task, high urgency |
| 5 | **By Problem (search)** | "My ROAS dropped" / "how do I price a retainer" | Users mid-crisis or mid-decision |
| 6 | **By Job-to-be-done** | "I'm planning next quarter" / "I'm launching a new channel" | Users starting a defined work project |

Models 4 and 5 are the highest-frequency, lowest-friction paths and are therefore first-class in the primary navigation UI (not buried under "Browse") — this reflects Product Principle #1 in the PRD: usable mid-task, not just study material.

---

# 2. Site Map (top level)

```
/                          Home — role/level-aware entry point, not a generic landing page
/domains                   Domain index (Model 1)
/domains/:domain           Domain hub — curriculum map Beginner→Expert, key frameworks, tools
/domains/:domain/:topic    Topic page
/item/:id                  Content item page (universal template, varies by type — see §4)
/tools                     All calculators/interactive tools (Model 4)
/tools/:calculator         Calculator experience
/templates                 All templates (Model 4)
/troubleshoot              Decision-tree / troubleshooting entry (Model 5/6 hybrid)
/paths                     Learning paths index (Model 2/3)
/paths/:path               Guided path player
/search?q=                 Universal search (Model 5)
/glossary                  Glossary index + lookup
/library                   Personal layer: bookmarks, progress, saved calculator results
/account                   Profile, role/level settings
```

---

# 3. Key User Flows

## 3.1 Onboarding

1. Role selection (from the 12 personas in the PRD, or "generalist/other").
2. Self-assessed skill level, per relevant domain (from §2 of `PRD.md`'s matrix — only the 2–3 domains relevant to that role are asked about, not all 14).
3. System generates a starter Role Path (§5 below) and a personalized Home.

No sign-up wall to *read* content — onboarding builds a better experience but is not a gate to entry-level use. See Open Decision on access model in the top-level README.

## 3.2 Domain Hub

Every domain hub page shows, in this order:
1. One-paragraph orientation ("what this domain covers and why it matters").
2. Curriculum map — a visual Beginner→Expert ladder with Topics as rungs, showing the user's current position if they're onboarded.
3. Core frameworks for the domain (the 3–5 "if you only know these, know these").
4. Tools available in this domain (calculators/templates), surfaced early — not buried at the bottom.
5. Topic list, each expandable into Modules.

## 3.3 Content Item Page (universal template)

Every content item, regardless of type, renders through one consistent template so users learn the page pattern once:

```
[Type badge] [Skill level badge(s)] [Last reviewed date]
Title
Summary (1–2 sentences, always visible, e.g. in search results/cards)
Body (structure varies by type — see KNOWLEDGE_ARCHITECTURE.md §3)
── Related tools (calculators/templates that operationalize this content) ──
── Related content (prerequisites, related items, "go deeper") ──
── Sources ──
[Bookmark] [Mark as learned] [Copy/Download if template]
```

Consistency here is a deliberate UX principle: scanability compounds across thousands of content items only if the shape never changes.

## 3.4 Calculator Flow

Input form (typed fields, sensible defaults where industry-standard) → instant recompute on input change (no submit button where feasible) → result with plain-language interpretation, not just a number → link to the Framework/Theory item behind the formula → "save this result" to `/library` → related SOPs/next actions.

## 3.5 Troubleshooting / Decision Tree Flow

Single starting question → branching Q&A (one question per screen, back button always available) → terminal node with: likely diagnosis, ranked list of causes, a fix (often linking an SOP), and a "prevent this next time" link (often linking a Checklist). Every terminal node is directly deep-linkable/shareable — a user should be able to send a teammate straight to "you have a frequency problem" without replaying the whole tree.

## 3.6 Personal Library

Bookmarks, saved calculator results, per-domain progress against the skill ladder, and "recently viewed." This is what makes the product feel like *my* operating system rather than a static reference site — it is the retention mechanic, and per PRD §6, its usage (return visits, saved-item reuse) is a primary success metric.

---

# 4. Search

* **Full-text** across all content types, with **facet filters**: domain, topic, type, skill level, tag.
* **Type-ahead** surfaces top calculators/templates first when the query pattern looks like a direct tool need (e.g., "CAC calculator").
* **Problem-phrased queries** ("ROAS dropped," "email open rate low") should resolve to Troubleshooting Guides / Decision Trees above generic Theory articles — this requires either curated query→content mappings at launch or, later, semantic search (Phase 3+, see `ROADMAP.md`).
* Search is a first-class nav element (persistent, not a hidden icon), reflecting that Model 5 (by problem) is a top-frequency path.

---

# 5. Personalization Model (V1 scope)

V1 personalization is **explicit, not inferred**: users set role + skill level themselves (and can change it anytime), and the system uses that to:
* Order/filter the Domain Hub curriculum map to their level.
* Pre-select a Role Path at onboarding.
* Sort search results to prefer their stated level (without hiding other levels — an Intermediate should still be able to see Advanced content, just not have it forced to the top).

Inferred/adaptive personalization (based on behavior, quiz results, etc.) is explicitly deferred — see `ROADMAP.md` Phase 3. Building it in V1 would require behavioral data the product hasn't yet collected, and risks personalizing on noise.

---

# 6. UX Design Principles

1. **30-second rule** — any calculator, checklist, or SOP must be usable by a returning user in under 30 seconds without re-reading instructions.
2. **Progressive disclosure** — Beginner-level users are never dropped into Expert content by default navigation; it's reachable, never forced.
3. **Consistent templates over creative layouts** — the content item template (§3.3) and calculator template (§3.4) are fixed shapes; visual variety happens within them, not to them.
4. **Mobile-usable, not mobile-first** — the primary work context is a desktop during work hours, but troubleshooting/reference lookups happen on mobile; calculators and troubleshooting flows must degrade gracefully to small screens, dense domain hub maps can be desktop-optimized.
5. **Dark mode as a first-class theme**, not an afterthought — professionals reference this tool at all hours.
6. **No dead ends** — every terminal page (calculator result, decision-tree outcome, glossary term) always surfaces a "next" link; the product should never leave a user at a page with nothing else to do.
