# MarketingOS — UI/UX Design

## Version 1.0 (Complete, Blueprint Stage)

> **Status: Blueprint stage. No implementation code exists yet.** This document is the visual/interaction design system — it sits below `INFORMATION_ARCHITECTURE.md` (which defines *what* exists and *where*) and specifies *how it looks and behaves*. A companion visual mockup is provided alongside this document so the system isn't only described in prose.

---

# 1. Design Philosophy & Identity

**MarketingOS looks like an operating system, not a blog.** Every visual decision below is a rejection of the content-marketing-site aesthetic (warm editorial serif, big hero images, generous whitespace as decoration) in favor of an instrument-panel aesthetic: dense, precise, fast to scan, built for someone returning to it fifty times a week — consistent with the PRD's non-goal of *not* being a blog and the Product Principle that tools must be usable in under 30 seconds (`PRD.md §2`, `INFORMATION_ARCHITECTURE.md §6`).

Two decisions carry the whole identity:

1. **The interface typeface is the visitor's own operating system's font**, not a licensed brand face. This is a literal decision, not a cost-saving default: a product named MarketingOS should render in the same font as the reader's Finder, Explorer, or GNOME shell — it reinforces "this is infrastructure you live in," not "this is a website you visited." (Detailed in §3.2.)
2. **Numbers get their own typeface.** Every metric, benchmark, calculator output, and badge label renders in a monospace face, visually distinct from prose. This is a working distinction, not decoration: it lets a user's eye separate "data to trust" from "explanation to read" at a glance, the same instinct a spreadsheet or terminal trains.

Color is spent deliberately and narrowly: one accent hue (blue) carries both interactivity *and* the skill-level progression (deepening as level rises — see §3.1), status colors are reserved exclusively for freshness/validation state and never reused as decoration, and the 11 content types and 14 domains are **never color-coded** — with that many categories, color-coding would either force an unreadable rainbow or force arbitrary reuse of hues across unrelated categories. Both are avoided by using icon + label instead (§4.1), which scales to any number of categories without adding colors.

The full color and type system is drawn from a validated, contrast- and colorblind-safety-checked palette (methodology: the `dataviz` design-system reference palette) rather than picked by eye — every token in §3 traces to a checked value.

---

# 2. Design Principles (visual/interaction layer)

These extend the UX principles already established in `INFORMATION_ARCHITECTURE.md §6` with visual-specific rules:

1. **State is encoded in form, not just color.** A stale content item doesn't just turn orange — it gets a distinct badge shape/icon, because color alone excludes colorblind users and fails in bright-sunlight mobile use (troubleshooting happens in the field, `PRD.md §4` Mona persona).
2. **Every interactive element looks interactive.** Buttons, links, calculator inputs, and facet chips all carry a consistent hover/focus treatment (§7) — nothing that responds to a click looks like static text.
3. **Density over air.** Given the "operating system" identity (§1), MarketingOS uses tighter vertical rhythm than a typical content site — more visible per screen, because the user is scanning for the one thing they need, not being walked through a narrative.
4. **One accent, spent on the primary action.** Every screen has exactly one element in the accent color performing the primary action (§6, `INFORMATION_ARCHITECTURE.md §6` principle 8); everything else is ink, border, or status color.
5. **The system is symmetrical in both themes.** Dark mode is not an inverted afterthought (§8) — it's designed with its own token values from the same validated ramps, since professionals reference this tool at all hours (`INFORMATION_ARCHITECTURE.md §6` principle 5).

---

# 3. Design Tokens

## 3.1 Color

All values below are drawn from the `dataviz` skill's validated reference palette (checked for contrast, colorblind-safe adjacent-hue separation, and light/dark parity) — not eyeballed.

**Neutrals & surfaces**

| Token | Light | Dark | Use |
|---|---|---|---|
| `--surface-page` | `#f9f9f7` | `#0d0d0d` | App background |
| `--surface-raised` | `#fcfcfb` | `#1a1a19` | Cards, panels, modals |
| `--ink-primary` | `#0b0b0b` | `#ffffff` | Headings, primary text, data values |
| `--ink-secondary` | `#52514e` | `#c3c2b7` | Body text, descriptions |
| `--ink-muted` | `#898781` | `#898781` | Timestamps, helper text, disabled |
| `--border-hairline` | `rgba(11,11,11,0.10)` | `rgba(255,255,255,0.10)` | Card borders, dividers |
| `--gridline` | `#e1e0d9` | `#2c2c2a` | Table rules, facet-panel dividers |

Note these are warm-biased neutrals (a slight olive/yellow undertone, not flat `#808080` gray) — a deliberate pairing with the blue accent, not an inherited default.

**Accent (interactive + skill-level progression)**

| Token | Light | Dark | Use |
|---|---|---|---|
| `--accent` | `#2a78d6` | `#3987e5` | Primary buttons, links, active nav, focus ring |
| `--accent-hover` | `#1c5cab` | `#5598e7` | Hover/active state of the above |

**Skill-level scale** — the same blue ramp used for the accent, stepped ordinally so *deepening blue = rising mastery*, a deliberate narrative device rather than five arbitrary hues:

| Level | Light | Dark |
|---|---|---|
| Beginner | `#86b6ef` | `#b7d3f6` |
| Intermediate | `#5598e7` | `#86b6ef` |
| Advanced | `#2a78d6` | `#5598e7` |
| Senior | `#1c5cab` | `#2a78d6` |
| Expert | `#104281` | `#1c5cab` |

**Status (fixed — reserved exclusively for freshness/governance state, per `CONTENT_GOVERNANCE.md §2`; never themed, never reused as decorative accent)**

| Role | Hex (both modes) | Use |
|---|---|---|
| `--status-good` | `#0ca30c` | Content within freshness SLA; `published` state |
| `--status-warning` | `#fab219` | Approaching freshness SLA; `in_review` state |
| `--status-critical` | `#d03b3b` | Past freshness SLA; `deprecated` state |

Status colors always ship with an icon + text label (§4.1), never color alone — required both for accessibility and because two of these fall under 3:1 contrast on the light surface by design (mitigated by the icon/label pairing, matching the validated palette's own documented tradeoff).

## 3.2 Typography

| Token | Stack | Role |
|---|---|---|
| `--font-ui` | `system-ui, -apple-system, "Segoe UI", sans-serif` | All interface chrome, headings, body prose — the reader's own OS font (§1) |
| `--font-data` | `ui-monospace, "SF Mono", "Cascadia Code", Consolas, monospace` | Metrics, calculator inputs/outputs, badges, benchmark tables, glossary terms shown inline |

Type scale (size/line-height/weight):

| Role | Size / Line-height | Weight | Face |
|---|---|---|---|
| Display (rare — onboarding, empty-state headlines only) | 32/40px | 700 | `--font-ui` |
| H1 (content item title, page title) | 26/34px | 700 | `--font-ui` |
| H2 (section heading) | 20/28px | 650 | `--font-ui` |
| H3 (subsection, card title) | 16/24px | 600 | `--font-ui` |
| Body | 15/24px | 400 | `--font-ui` |
| Small / caption / eyebrow | 13/18px | 500, uppercase, +0.04em tracking | `--font-ui` |
| Data (calculator values, benchmarks, badge text) | 14/20px | 500, `tabular-nums` | `--font-data` |

Body text is capped at **65 characters measure** inside long-form content (Theory/Framework/Case Study bodies) per readability convention — but *not* inside dense UI surfaces (tables, facet panels, calculator forms), which intentionally use full container width, since those are scanned, not read linearly (§2 principle 3).

## 3.3 Spacing, Radius, Elevation

| Token | Value |
|---|---|
| `--space-1` … `--space-8` | 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64px |
| `--radius-sm` | 4px — inputs, chips, calculator fields |
| `--radius-md` | 8px — cards, panels |
| `--radius-lg` | 12px — modals only |

Radius is deliberately restrained (never the uniform `rounded-xl`-everywhere look) — data-dense elements (tables, inputs) stay closer to square, reinforcing the instrument-panel identity from §1; only true containers (cards, modals) get the softer radius.

Elevation is **flat by default** — surfaces are distinguished by `--surface-raised` + `--border-hairline`, not drop shadows. A single subtle shadow token exists for genuinely floating elements only (dropdowns, the decision-tree "next question" transition):

| Token | Value |
|---|---|
| `--shadow-float` | `0 4px 16px rgba(11,11,11,0.12)` (light) / `0 4px 16px rgba(0,0,0,0.4)` (dark) |

## 3.4 Motion

| Token | Value | Use |
|---|---|---|
| `--duration-fast` | 120ms ease-out | Hover, focus ring, badge state change |
| `--duration-base` | 200ms ease-out | Facet panel expand, calculator result update |
| `--duration-slow` | 280ms ease-out | Decision-tree question transition, path-player step change |

All motion respects `prefers-reduced-motion: reduce` — transitions collapse to instant state changes, never removed functionality, since motion here is never load-bearing for comprehension (unlike, say, a chart transition showing a data relationship).

---

# 4. Iconography & Badges

## 4.1 Icon System

A single, consistent icon set (outline style, 1.5px stroke, 16/20/24px sizes) covers:
* The 11 content-type badges (§`KNOWLEDGE_ARCHITECTURE.md §3`) — one fixed icon per type, e.g., a calculator glyph for Calculator, a branching-path glyph for Decision Tree, a checklist glyph for Checklist. Icon + label together, never icon alone, since an unfamiliar icon shouldn't be a comprehension barrier for a Beginner.
* Status states (§3.1) — check-circle (good), clock (warning/due), alert-triangle (critical).
* Navigation (§`INFORMATION_ARCHITECTURE.md §1`) — search, domains (grid), tools (wrench), paths (route), library (bookmark).

## 4.2 Badge Anatomy

Three badge types recur across nearly every template (`INFORMATION_ARCHITECTURE.md §3.3`):

```
TypeBadge:      [icon] LABEL              — neutral surface, ink-secondary text, uses --font-data at caption size
LevelBadge:     [filled dot] LABEL        — dot filled with the level's step color (§3.1), label in ink-secondary
FreshnessBadge: [status icon] "Reviewed <date>"  — status color only when past SLA; neutral/muted when current
```

None of the three badges use a filled color background — only the dot (LevelBadge) or icon (FreshnessBadge) carries color, keeping badges visually quiet until something needs attention (§2 principle 1).

---

# 5. Layout & Grid System

| Breakpoint | Width | Behavior |
|---|---|---|
| `sm` | < 640px | Single column; global nav collapses to bottom tab bar (`INFORMATION_ARCHITECTURE.md §10`) |
| `md` | 640–1024px | Single column content + collapsible facet panel (drawer, not sidebar) |
| `lg` | 1024–1440px | Two-column: content + persistent facet/related-content sidebar |
| `xl` | ≥ 1440px | Three-column on Domain Hub and Home only (local nav / content / contextual rail); everywhere else stays two-column — MarketingOS resists the temptation to "fill" ultra-wide screens with low-value panels |

Container max-width for long-form content bodies: **760px** (targets the 65-character measure from §3.2 at body size). Data-dense surfaces (tables, calculator grids, facet panels) are **not** width-capped — they use the full content column.

Base grid unit: **8px**, all spacing tokens (§3.3) are multiples of 4px nesting into 8px rhythm at the layout level.

---

# 6. Component Specifications

Extends the component inventory from `PRD.md §22` with visual/interaction detail. Each component's states: **default, hover, focus, active, disabled**, plus **loading**/**error** where applicable.

### `ContentCard`
- Default: `--surface-raised`, `--border-hairline`, `--radius-md`, TypeBadge + LevelBadge top row, H3 title, one-line summary in `--ink-secondary`.
- Hover: border shifts to `--accent` at 40% opacity, subtle `translateY(-1px)`, `--duration-fast`.
- Focus (keyboard): 2px `--accent` outline, offset 2px — never removed, never `outline: none` without a replacement.

### `CalculatorInputField`
- Default: `--font-data`, `--radius-sm`, hairline border, right-aligned when numeric (mirrors spreadsheet convention).
- Focus: border becomes `--accent`, 2px, no color-only change — border *width* changes too, so focus is visible under any color-vision condition.
- Error (out-of-range input): border `--status-critical`, inline message below in `--status-critical` text + an alert-triangle icon (never color alone, §3.1 rule).
- Loading (recompute in flight, for any calculator expensive enough to debounce): value dims to `--ink-muted` with a subtle pulse, `--duration-base` — recompute is client-side and near-instant per `PRD.md NFR-02`, so this state is rare by design, not a normal part of the flow.

### `CalculatorResultPanel`
- Result value: large, `--font-data`, `tabular-nums`, `--ink-primary`.
- Interpretation line directly below in `--font-ui` body — the pairing of a data-face number with a prose-face explanation is the same "trust vs. explain" split from §1, applied at component scale.
- Threshold-triggered guidance (e.g., "below breakeven"): rendered as a status-colored inline banner with icon, linking to the relevant Troubleshooting Guide.

### `DecisionTreeNode`
- One question per screen (`INFORMATION_ARCHITECTURE.md §3.5`); options rendered as full-width tappable rows (not a dropdown — speed and thumb-friendliness on mobile, per `INFORMATION_ARCHITECTURE.md §10`), hover/focus states matching `ContentCard`.
- Transition between questions: `--duration-slow`, slide + fade — the one place a slightly longer transition is warranted, since it reinforces "you moved forward in a diagnosis," a meaningful state change.
- Back navigation: persistent top-left, `--ink-secondary`, never removed mid-flow.

### `FacetFilterPanel`
- Each facet group: `--font-ui` caption-weight label (uppercase, per §3.2's eyebrow style), checkbox rows below in body size.
- Active facet count shown as a small `--accent`-filled numeral badge on the "Filters" trigger (mobile) — the one place a solid accent fill is used, reserved for exactly this "N active" signal.
- Live result-count update on facet change (`INFORMATION_ARCHITECTURE.md §8`): count text briefly pulses `--duration-fast`, `aria-live="polite"` announces the new count for screen readers (`INFORMATION_ARCHITECTURE.md §11`).

### `ProgressLadder`
- Five segments (Beginner→Expert), each filled with its level color (§3.1) up to the user's current position; remaining segments render as `--gridline` outline only — the ladder *is* the level-color scale made spatial, reusing the same token rather than inventing a second progress-color system.

### `PrimaryNavBar`
- Persistent search field is visually the widest element in the bar (§`INFORMATION_ARCHITECTURE.md §1`, models 4–5 priority) — not icon-only, always shows placeholder text ("Search MarketingOS…").
- Active route indicated by `--accent` text color + a 2px `--accent` underline, not a filled background pill (keeps the flat, instrument-panel language from §3.3).

### `SkillLevelBadge`, `TypeBadge`, `FreshnessIndicator`
See §4.2 — Badge Anatomy.

### `BookmarkButton`
- Unfilled outline icon default; filled `--accent` icon when bookmarked; single `--duration-fast` fill transition on click, no confirmation modal (low-stakes, reversible action, per the "don't over-confirm reversible actions" interaction principle).

---

# 7. Page-Level UI Specifications

Building on the structural definitions in `INFORMATION_ARCHITECTURE.md §3`, here is the *visual* composition of each primary template.

## 7.1 Home / Dashboard (`INFORMATION_ARCHITECTURE.md §3` intro, `PRD.md §21`)

Visual layout, top to bottom: full-width search bar (H_search = 56px, disproportionately prominent per §2 principle 4 — it's the single highest-frequency action) → "Continue where you left off" as one wide `ContentCard` variant with a thin `--accent` left rule (the *only* card style with a colored rule, reserved for this one highest-priority slot) → two-column row: `ProgressLadder` stack (left, one per primary domain) and a 2×2/2×3 grid of `Quick tool` chips (right, `--font-data` labels since these are named metrics like "CAC/LTV") → "Recommended next" as a horizontal `ContentCard` row → "Recently viewed" / "Bookmarks" as two lower-priority horizontal scroll rails, visually quieter (smaller card variant, no elevation).

## 7.2 Domain Hub (`INFORMATION_ARCHITECTURE.md §3.2`)

Orientation paragraph in body-size prose (the one place on this page long-form typography rules apply) → `CurriculumMap`: a horizontal five-segment bar per Topic (reusing `ProgressLadder`'s visual language) stacked vertically per topic, immediately establishing the Beginner→Expert structure visually before any text is read → "Core frameworks" as a 3–5 card horizontal rail, `--font-data` badges → Tools rail (same card style as Home's Quick tools) → Topic list as a dense, expandable tree (accordion), each row showing module count and a mini completion indicator.

## 7.3 Content Item Page (`INFORMATION_ARCHITECTURE.md §3.3`)

Badge row (Type, Level, Freshness — §4.2) → H1 title → summary in `--ink-secondary`, slightly larger than body (17px) to function as a dek → body content, width-capped at 760px (§5) with type-specific internal structure (an SOP's numbered steps get extra left-padding + `--font-data` step numbers; a Framework's named components get H3 subheadings; a Benchmark's data table is *not* width-capped, breaking out to full column width since tabular data needs room) → Related Tools rail (`--font-data` labels, positioned directly under body per the tool-urgency rule in `INFORMATION_ARCHITECTURE.md §7`) → Related Content rail (standard `ContentCard`s) → Sources as a plain numbered list, `--ink-muted`, small size — present but visually recessive, since it's a trust signal for those who look, not a primary reading element.

## 7.4 Calculator (`INFORMATION_ARCHITECTURE.md §3.4`)

Two-column on `lg`+ (inputs left, ~400px fixed; result right, fluid), single column stacked on mobile with inputs first (§`INFORMATION_ARCHITECTURE.md §10` mobile-first for this template specifically). Inputs use `CalculatorInputField` (§6); the result column is the one place per screen where `--font-data` appears at Display scale (32px) — the calculator's whole visual job is making that one number unmissable.

## 7.5 Troubleshooting / Decision Tree (`INFORMATION_ARCHITECTURE.md §3.5`)

Full-bleed single-question layout, centered column (max 480px) — deliberately narrower than the 760px content measure, because this is a rapid-fire flow, not reading material. `DecisionTreeNode` component (§6) fills the vertical center; progress through the tree is *not* shown as a percentage/step-count (the tree's length varies by path and a fake progress bar would mislead) — instead only "Back" is shown, keeping the visual promise honest.

## 7.6 Search Results (`INFORMATION_ARCHITECTURE.md §3.7`)

`FacetFilterPanel` as a persistent left column on `lg`+, a `md`-breakpoint drawer below that (§5) → result list as `ContentCard`s in a single column (not a grid — search results are rank-ordered, and a grid visually implies unordered equality, which would misrepresent the ranking in §`INFORMATION_ARCHITECTURE.md §4`) → "did you mean a tool?" prompt, when triggered, renders as a distinct callout above the list, `--accent` left rule, matching Home's "continue where you left off" treatment (§7.1) — the visual language for "this is the one thing to look at first" is consistent across the whole product.

## 7.7 Onboarding (`INFORMATION_ARCHITECTURE.md §3.1`)

The one place Display-scale type and generous whitespace are used (§3.2) — onboarding is a single first-impression moment, not a returning-user utility screen, so it earns the one exception to the density principle (§2.3). Role selection renders as a card grid (12 personas, `PRD.md §4`), skill-level selection as a per-domain slider using the same five-color level scale (§3.1) so the user sees, in color, what they're about to select before they select it.

## 7.8 Personal Library (`INFORMATION_ARCHITECTURE.md §3.6`)

Three tabs (Bookmarks / Progress / Saved Tools) as `--font-ui` caption-weight labels with the same active-tab underline treatment as `PrimaryNavBar` (§6) — reinforcing that this is still primary navigation, not a settings-style sub-page. Saved Tools renders each result as a compact `CalculatorResultPanel` variant showing the saved inputs/output without needing to re-open the full calculator.

---

# 8. Dark Mode

Dark mode is a **first-class, separately designed theme**, not an automatic inversion (`INFORMATION_ARCHITECTURE.md §6` principle 5) — every token in §3.1 has an explicit dark value drawn from the same validated ramp set, not a CSS `invert()` filter. Two implementation rules carry this through correctly regardless of how theme selection is wired up later:

* Dark values apply under **both** `prefers-color-scheme: dark` (OS-level signal) **and** an explicit `data-theme="dark"` attribute (in-product toggle) — the explicit toggle must win over the OS signal in both directions, so a user who prefers OS-dark but picks light-in-app (or vice versa) gets what they asked for.
* Components are written against the **token names** (`--accent`, `--surface-raised`, …), never against raw hex or against the media query directly — this is what makes §3.1's dark column a drop-in swap rather than a parallel stylesheet.

The skill-level scale (§3.1) and status colors (§3.1) both already carry validated dark-mode steps — no separate dark palette exercise is needed for those; only the neutrals and accent needed distinct dark values, which they have.

---

# 9. Accessibility & Contrast

Extends `INFORMATION_ARCHITECTURE.md §11` (landmarks, focus management, heading hierarchy) with the visual specifics:

* **Contrast**: `--ink-primary` on `--surface-page`/`--surface-raised` clears AAA in both themes; `--ink-secondary` clears AA for body text; `--ink-muted` is reserved for non-essential metadata (timestamps) specifically because it does *not* clear AA on its own — anything load-bearing never uses it alone.
* **Status color relief rule** (carried from §3.1): `--status-warning` and `--status-serious`-equivalent tones fall under 3:1 on the light surface by the validated palette's own design — every use is paired with an icon and a text label, never a bare colored dot.
* **Focus states are never suppressed.** Every interactive component in §6 defines an explicit focus treatment; `outline: none` never ships without a replacement indicator.
* **Touch targets**: minimum 44×44px on all tappable elements on `sm`/`md` breakpoints (decision-tree option rows, facet checkboxes, nav tabs) — checked explicitly for `DecisionTreeNode` and `FacetFilterPanel`, the two components most likely to be operated one-handed on mobile.
* **Color is never the sole signal** — restated once more here because it's the single most-violated rule in dashboard-style UIs: every colored state (LevelBadge dot, FreshnessBadge, calculator error, status banner) is paired with position, icon, or text, per §3.1/§4.2.

---

# 10. Content Design & Microcopy

* **Voice**: direct, practitioner-to-practitioner, no marketing register — matches `CONTENT_GOVERNANCE.md §5`'s style guide, extended here to UI copy specifically (not just article bodies).
* **Buttons name the result, not the mechanism**: "Save result" not "Submit"; "Start diagnostic" not "Begin"; "Download template" not "Export" — a control says exactly what happens (per general copy principle, applied consistently across `CalculatorResultPanel`, `TemplateDownloadCard`, `DecisionTreeNode`).
* **Errors explain and fix, never apologize**: a `CalculatorInputField` error reads "Enter a value between 0 and 100%" — not "Oops, something went wrong" or "Invalid input."
* **Empty states point at the action that fills them** (`INFORMATION_ARCHITECTURE.md §3.10`): "No bookmarks yet — the bookmark icon on any article saves it here," not a bare "Nothing to show."
* **Numbers are never bare**: every `CalculatorResultPanel` output ships with its one-line interpretation (§6) — a number without a verdict fails this component's spec, not just its copy.

---

# 11. Design System Governance

* **Tokens are the single source of truth.** A new component is built by composing existing tokens (§3) and reusing existing components (§6) — a one-off color or spacing value outside the token set is a defect, matching the same discipline `CONTENT_GOVERNANCE.md` applies to content.
* **New badge/status colors are not introduced ad hoc.** The status palette (§3.1) is fixed at four roles by design (good/warning/serious/critical, matching the validated reference palette) — a "fifth status" is a sign the underlying state model needs rethinking, not a sign a new color is needed.
* **Component additions go through the same catalog discipline as `PRD.md §22`** — a new component is named, specced with its states (§6's format), and added to that list before being built, so the design system and the implementation-facing component list never drift apart.

---

# Cross-references

This document specifies the visual/interaction layer for the structure defined in `INFORMATION_ARCHITECTURE.md` and the component inventory scoped in `PRD.md §22`. It does not introduce new pages, routes, or content types — see those documents for structural changes. A visual mockup applying these tokens to real screens accompanies this document.
