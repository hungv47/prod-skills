---
name: user-flow
description: "Maps multi-step in-product flows — screens, decisions, transitions, platform-native touchpoints (dock, menu bar, widgets, notifications, Live Activity, etc.), edge cases, and error states for features or user journeys. Produces `.agents/product/flow/<flow-name>.md` (one file per flow) plus an auto-generated `index.md` when ≥2 flows exist. Not for visual brand design (use brand-system) or single-page conversion (use lp-optimization). For technical architecture, see system-architecture. For task decomposition, see task-breakdown."
argument-hint: "[feature or flow to map]"
allowed-tools: Read Grep Glob Bash
license: MIT
metadata:
  author: hungv47
  version: "4.0.0"
  budget: standard
  estimated-cost: "$0.20-0.50"
promptSignals:
  phrases:
    - "user flow"
    - "screen flow"
    - "journey map"
    - "ux flow"
    - "wireframe flow"
    - "map the screens"
  allOf:
    - [user, flow]
    - [screen, map]
  anyOf:
    - "flow"
    - "journey"
    - "wireframe"
    - "screen"
    - "ux"
    - "transition"
  noneOf:
    - "brand identity"
    - "api design"
    - "database schema"
  minScore: 6
routing:
  intent-tags:
    - user-flow
    - screen-mapping
    - ux-flow
    - journey-mapping
    - wireframe-flow
  position: pipeline
  produces:
    - product/flow/[flow-name].md
    - product/flow/index.md  # auto-generated when ≥2 flows exist
  consumes:
    - product-context.md
    - brand/DESIGN.md
  requires: []
  defers-to:
    - skill: brand-system
      when: "need visual identity, not screen flows"
    - skill: system-architecture
      when: "need technical API design, not user-facing flow"
  parallel-with: []
  interactive: false
  estimated-complexity: medium
---

# User Flow Design — Orchestrator

*Design — Step 2 of 2. Maps navigation paths, decisions, edge cases, platform-native touchpoints, and screen transitions into a validated flow diagram.*

**Core Question:** "Can the user complete their goal without thinking — on every surface of every platform it ships on?"

## Critical Gates — Read First

- **No Layer 1 before platforms + surfaces enumerated.** See `references/platform-touchpoints.md`. Wireframe size, entries, edge states all depend on it.
- **Reject "cross-platform" as a platform.** Enumerate: macOS, iOS, iPadOS, Android, Windows, web-desktop, web-mobile, watchOS, tvOS, visionOS, CarPlay, Android Auto, Linux.
- **No diagrams before structure.** Diagram-agent needs structure + edge-case outputs first.
- **No skipping edge cases.** Error/empty/loading/permission/offline + per-surface edge states for every screen and surface.
- **Challenge >7 happy-path steps.** Miller's threshold. Every step must justify itself.
- **One flow = one file.** No pooling. Each run writes `.agents/product/flow/<flow-name>.md`.
- **Stale product context (>30 days) misaligns flows.** Recommend re-running `icp-research`.

## Inputs Required
- Product/feature requiring flow mapping (new, redesign, or audit)
- Target user role/persona (flows change per role)
- Single user goal (one per flow)
- **Target platforms** — explicit list from `references/platform-touchpoints.md`
- **Per-platform surfaces in scope** — explicit list per platform

## Output
- `.agents/product/flow/<flow-name>.md` — one file per flow run
- `.agents/product/flow/index.md` — auto-created/updated when ≥2 flow files exist

Slug derived from brief (e.g., "checkout flow" → `checkout.md`); orchestrator confirms if ambiguous.

## Quality Gate
**Critic agent** runs full rubric (see `agents/critic-agent.md`). Non-negotiable PASS checks:
- Platforms + per-platform surfaces explicitly enumerated (no "cross-platform")
- Every platform × surface has entry + mini-frame + per-surface edge state (Surface Coverage Map complete)
- Mini-frame dimensions match `references/platform-touchpoints.md`
- Every decision point has ≥2 labeled exits; no dead-end errors
- Happy path ≤7 steps; ≤3 primary actions per screen
- Every core screen has ASCII wireframe + 2-4 sentence Description; wireframe CTAs match structure actions
- 2-3 critical edge-state variants included

## Chain Position
Prev: `brand-system` (optional — design tokens). Next: implementation. Related: `system-architecture` (API design), `task-breakdown` (decomposition), `discover` (specs).

**Re-run triggers:** significant feature changes, new research, usability failures, new user roles.

**Deference:** `discover` if requirements unclear · `brand-system` for design tokens · `task-breakdown` for decomposition.

---

## Agent Manifest

| Agent | Layer | File | Focus |
|-------|-------|------|-------|
| Structure | 1 parallel | `agents/structure-agent.md` | Entries, screens, decisions, exits, flow type, **surface entry map** |
| Edge Case | 1 parallel | `agents/edge-case-agent.md` | Error/empty/loading/permission/offline + **per-surface edge states** |
| Diagram | 2a parallel | `agents/diagram-agent.md` | Mermaid flowchart, 5 node shapes, annotations |
| Wireframe | 2a parallel | `agents/wireframe-agent.md` | ASCII wireframe per core screen + edge variants + **per-surface mini-frames** |
| Validation | 2b seq | `agents/validation-agent.md` | Miller's threshold, ≤3 actions/screen, integrity, **surface coverage** |
| Critic | 2b final | `agents/critic-agent.md` | Full rubric PASS/FAIL + **surface coverage matrix** |

### Shared References (read by agents)
- `references/research-checklist.md` — pre-design research methods, IA, content strategy
- `references/platform-touchpoints.md` — surface catalog (13 platforms + cross-platform channels): entry triggers, flow roles, native dimensions, per-surface edge states

---

## Routing Logic

Single route — all flows use the full stack. Flows >15 screens auto-split via structure-agent's sub-flow decomposition. Pipeline: Step 0 (interview + gated enumeration) → **Layer 1 parallel** (structure + edge-case) → Merge → **Layer 2a parallel** (diagram + wireframe) → **Layer 2b sequential** (validation → critic). Critic FAIL re-dispatches named agents (max 2 cycles). Deliver to `.agents/product/flow/<flow-name>.md`; update `index.md` if ≥2 flows.

---

## Step 0: Pre-Dispatch Context Gathering

### Product Context Check
Check `research/product-context.md`. If missing: **INTERVIEW** for product dimensions (what, who, problem, differentiator, constraints) and save it — or recommend `icp-research (from hungv47/research-skills)` to bootstrap.

If `date` field >30 days old, recommend re-running `icp-research` first.

### Required Artifacts
None — runs standalone.

### Optional Artifacts
- `product-context.md` (icp-research) — product/user context
- `brand/DESIGN.md` (brand-system) — components, design tokens
- `brand/BRAND.md` (brand-system) — voice/terminology for Descriptions

### Flow Interview
Interview these dimensions first. Full platform/surface enumeration in `references/platform-touchpoints.md` § "Using this catalog at the interview."

**Product context**
1. Product/feature needing flow mapping?
2. Problem it solves?
3. Primary user? (role, technical skill, frequency)

**Flow scope**
4. Single user goal this flow serves?
5. Confirm flow slug (auto-derived, e.g. "checkout flow" → `checkout`).
6. Where does it start? (specific trigger — multiple if multi-surface)
7. Success state? (specific)
8. Existing flows to reference, replace, or extend?

**Platforms & surfaces — mandatory gate (see `references/platform-touchpoints.md`)**
9. **Target platforms** — from: `macOS`, `iOS`, `iPadOS`, `Android`, `Windows`, `web-desktop`, `web-mobile`, `watchOS`, `tvOS`, `visionOS`, `CarPlay`, `Android Auto`, `Linux`. Reject "cross-platform."
10. **Per-platform surfaces** — pick from catalog (authoritative; don't list from memory).
11. **Cross-platform channels** — from catalog's Cross-platform section.
12. **Primary surface per platform** — the *one* default entry (drives default wireframe size).

**Constraints**
13. Authentication? (logged in / guest / role-based)
14. Technical/business rules forcing specific paths?
15. Minimum OS versions? (drives available surfaces — e.g., Live Activities iOS 16.1+, Control Center custom controls iOS 18+)

**Gate:** No Layer 1 until Q9–Q12 are explicit. "All surfaces" / "cross-platform" fail.

### Context to Pass to All Agents
Product · user · goal · slug · platform list · surface matrix · cross-platform channels · primary surface per platform · min OS versions · constraints.

---

## Dispatch Protocol

### How to spawn a sub-agent

1. **Read** the agent instruction file — include FULL content in the Agent prompt.
2. **Append** context (product, user, goal, platform, constraints).
3. **Resolve paths to absolute** (rooted at this skill's directory).
4. **Pass upstream artifacts by content**: orchestrator reads `.agents/` files and includes excerpts; sub-agents don't read artifact files directly.
5. On critic FAIL, append feedback under `## Critic Feedback — Address Every Point`.

### Conventions

- **Source citation:** Cite UX heuristics/research/patterns; include URLs; flag unattributable claims `[UNVERIFIED]`.
- **Context loaded:** Artifact body lists which upstream artifacts were read + versions/dates (audit trail).

### Single-agent fallback

If multi-agent dispatch is unavailable, execute agent instructions sequentially in-context: Layer 1 (structure → edge cases) → Layer 2 (diagram + wireframes → validation) → critic.

---

## Layer 1: Parallel Foundation

Spawn **IN PARALLEL** (wait for both — outputs feed merge and Layer 2):

| Agent | Instruction File | Pass These Inputs | Reference Files |
|-------|-----------------|-------------------|-----------------|
| Structure Agent | `agents/structure-agent.md` | brief (product + user + goal + platforms + surface matrix + constraints) | `references/research-checklist.md`, `references/platform-touchpoints.md` |
| Edge Case Agent | `agents/edge-case-agent.md` | brief (product + user + goal + platforms + surface matrix + constraints) | `references/research-checklist.md`, `references/platform-touchpoints.md` |

---

## Merge Step

Combine structure + edge-case outputs into a unified flow model:

- **Structure:** flow classification, entry points, platform-surface entry matrix, core screens (name/purpose/actions/responses), decisions, exits, transitions.
- **Edge-case:** error/empty/loading/permission/offline per screen, back/cancel paths, per-surface platform edge states (app not running, widget stale, refresh throttled, notification grouping, deep-link fallback, etc.).

**Cross-reference checks before Layer 2:** (1) every screen has edge coverage; (2) every platform × surface has an entry-matrix row; (3) every platform × surface has a per-surface edge-state row. Flag failures before dispatching Layer 2.

---

## Layer 2a: Parallel Rendering

Spawn **IN PARALLEL** (both consume merged Layer 1 output; wait for both before Layer 2b):

| Agent | Instruction File | Pass These Inputs | Reference Files |
|-------|-----------------|-------------------|-----------------|
| Diagram Agent | `agents/diagram-agent.md` | brief + merged structure + edge cases | none |
| Wireframe Agent | `agents/wireframe-agent.md` | brief + platforms + surface matrix + merged structure + edge cases | `references/platform-touchpoints.md` (per-surface native dimensions) |

## Layer 2b: Sequential Chain

Dispatch **ONE AT A TIME, IN ORDER:**

| Step | Agent | Instruction File | Receives |
|------|-------|-----------------|----------|
| 1 | Validation Agent | `agents/validation-agent.md` | Structure + edge cases + diagram + wireframes |
| 2 | Critic Agent | `agents/critic-agent.md` | Complete flow (all outputs merged + validation results) |

---

## Critic Gate

- **PASS:** Deliver artifact.
- **FAIL:** Re-dispatch named agent(s) with feedback. Max 2 cycles. After 2 failures, deliver with critic annotations and flag to user.

---

## Artifact Template

**Output path:** `.agents/product/flow/<flow-name>.md` (one file per flow).

**Re-run of same flow:** rename existing `<flow-name>.md` → `<flow-name>.v[N].md`, create new `<flow-name>.md` with incremented version.

**Multi-flow products:** run once per flow — each creates its own file. After any run yielding ≥2 **distinct slugs** (excluding `.v[N]` versioned files) in `.agents/product/flow/`, orchestrator auto-creates/updates `.agents/product/flow/index.md` (template below). Versioned files sit next to live ones and are excluded from slug count and index.

### Per-flow file

```markdown
---
skill: user-flow
version: 1
date: {{today}}
status: draft
flow_name: [slug, matches filename]
platforms: [macOS, iOS, web-desktop, ...]
---

# User Flow: [Flow Name]

## Context
- **Product:** [product/feature]
- **User:** [role/persona]
- **Goal:** [single user goal]
- **Platforms:** [explicit list — e.g., macOS 13+, iOS 17+, web-desktop]
- **Flow type:** [linear/branching/cyclical/hub-and-spoke]

## Target Platforms & Surfaces

Matrix of every surface the flow occupies. Surfaces not listed are explicitly out of scope. Primary surface per platform marked ★.

| Platform | Primary surface ★ | Other surfaces in scope | Out-of-scope surfaces (explicit) |
|----------|-------------------|-------------------------|----------------------------------|
| [platform] | ★ [surface] | [surface · surface · ...] | [surface · surface · ...] |

### Cross-platform channels in scope
- [ ] Email / SMS / Push / Calendar / Clipboard / In-app / Third-party chat *(check all that apply; pull from catalog)*

## Flow Diagram

​```mermaid
graph TD
    [diagram here]
​```

**Annotations:**
1. [Node]: [implementation detail or business rule]

## Per-Surface Entry Points

One row per platform × surface from the matrix above.

| Platform | Surface | Entry trigger | Pre-loaded state | Auth required | First screen in flow | Handback when flow ends |
|----------|---------|--------------|-------------------|----------------|----------------------|--------------------------|
| [platform] | [surface] | [concrete trigger from catalog] | [data loaded before UI shows] | [yes/no/optional] | [screen name] | [where focus/state goes] |

## Screen Inventory

| # | Screen | Purpose | Actions | Next States |
|---|--------|---------|---------|-------------|
| 1 | [concrete name] | [why it exists] | [user actions] | [where each action leads] |

## Screen Wireframes

*Low-fidelity ASCII layouts — one per core screen. Shows regions and hierarchy, not brand design. Pair with `brand-system` for visual tokens.*

### Screen 1: [Name]

**Primary actions (≤3):** [action 1] · [action 2] · [action 3]
**Description:** [2-4 sentences — content/data, visual priority, mood. Designer-ready.]

​```
┌──────────────────────────────────────┐
│ [ wireframe ]                        │
└──────────────────────────────────────┘
​```

[Repeat for every screen in the inventory]

## Per-Surface Mini-Frames

*One ASCII mini-frame per selected surface, rendered at the surface's native dimensions. See `references/platform-touchpoints.md` for dimensions per surface.*

### [Platform] — [Surface name] ([native dimensions])

**Why this surface carries this flow:** [one line]

​```
┌──────────────────────────────┐
│  [ mini-frame ]              │
└──────────────────────────────┘
​```

[Repeat for every selected surface from the matrix. For multi-state surfaces (Dynamic Island compact/expanded, widget small/medium/large), include a mini-frame per state.]

## Critical Edge-State Variants

*2-3 high-stakes edge states across the whole flow — not one per screen.*

**Variant: [Screen — State]**

**Why this variant matters:** [one line]

​```
┌──────────────────────────────────────┐
│ [ variant wireframe ]                │
└──────────────────────────────────────┘
​```

## Coverage Map

| # | Screen | Wireframed | Edge variant(s) |
|---|--------|------------|-----------------|
| 1 | [name] | ✓ | — or [state] |

## Surface Coverage Map

| Platform | Surface | Entry defined ✓ | Mini-frame ✓ | Edge states ✓ |
|----------|---------|-----------------|--------------|----------------|
| [platform] | [surface] | ✓ | ✓ | ✓ |

## Edge Cases Handled

| State | Screen(s) | Handling |
|-------|-----------|----------|
| Error | [screens] | [recovery path] |
| Empty | [screens] | [placeholder/onboarding] |
| Loading | [screens] | [skeleton/spinner] |
| Permission | [screens] | [upgrade/redirect] |

## Per-Surface Edge States

Surface-specific failure modes that generic error/empty/loading don't capture. Pull candidates from the "Edge states to check" column of `references/platform-touchpoints.md` for each declared surface.

| Platform | Surface | Edge state | Handling |
|----------|---------|------------|----------|
| [platform] | [surface] | [surface-specific failure mode] | [recovery path] |

## Validation Summary

- Happy path length: [N steps]
- Decision points: [N total]
- Error recovery paths: [N total]
- Dead ends: 0
- Platforms × surfaces covered: [N]
- Surfaces with mini-frames: [N / total]
- Surfaces with per-surface edge states: [N / total]

## Sub-flows

- [Sub-flow name] → see `.agents/product/flow/[slug]-[sub].md`

## Next Step

Hand off to implementation. Pair with `brand-system` for visual design tokens if not already created.
```

### `index.md` (auto-generated when ≥2 flow files exist)

```markdown
---
skill: user-flow
type: index
date: {{today}}
---

# Product Flow Index

Generated from the files in this directory. Update whenever a flow file is added, renamed, or versioned.

## Flows

| File | Flow | Platforms | Last updated | Version | Status |
|------|------|-----------|--------------|---------|--------|
| [flow-slug.md](./flow-slug.md) | [Flow name] | [platforms] | [date] | [n] | [draft/done] |

## Platform coverage at a glance

| Platform | Flows touching this platform |
|----------|-------------------------------|
| [platform] | [slug · slug · ...] |
```

---

## Worked Example — Food-Delivery Checkout (Multi-Platform)

**User:** "Map the checkout flow for our food-delivery app. We ship on iOS, Android, and web."

**Step 0 — Interview** produces: slug `checkout`; platforms `iOS 17+` / `iPadOS 17+` / `Android 13+` / `web-desktop` / `web-mobile`; surfaces picked per platform from the catalog (primary marked ★), ~13 surfaces total across Home icon, Lock-screen widget, Dynamic Island / Live Activity, Apple Pay, Quick Settings tile, notification + inline reply, Google Pay, URL routing, Web Push, OAuth redirect, PWA install, Add-to-Home-Screen; cross-platform channels email + push + SMS; branching flow type; Apple Pay / Google Pay / card; minimum order $10; Live Activity required.

**Layer 1** — Structure agent returns 6 core screens (Cart Review → Shipping Address → Shipping Method → Payment Selection → Order Review → Order Confirmation), 3 decision points, 3 exits, and a 13-row Per-Surface Entry Matrix. Edge-case agent returns standard 5-category coverage per screen plus per-surface edge states pulled from the catalog (Live Activity 8h ceiling, Quick Settings tile desync, Web Push denied, PWA state loss on iOS, universal link fallback).

**Merge** — all 6 screens covered, all 13 platform × surface rows have entry + edge rows. Proceed.

**Layer 2a** — Diagram agent returns Mermaid `graph TD`. Wireframe agent returns 6 core-screen wireframes (mobile 34ch, desktop 68ch), 2 critical edge variants, and 13 per-surface mini-frames at native dimensions from the catalog.

**Layer 2b** — Validation: happy path 5 steps (PASS), ≤3 actions/screen (PASS), surface coverage 13/13 (PASS). Critic: PASS 4.8.

**Deliver** — `.agents/product/flow/checkout.md`. No `index.md` yet (only one flow). Second flow triggers index creation.

---

## Anti-Patterns

**Happy path only** — Flows break at the first error. INSTEAD: Edge-case-agent maps error/empty/loading/permission/offline for every screen.

**Generic screen names** — "Step 1", "Step 2" tell nobody anything. INSTEAD: Concrete names matching dev/design vocabulary — "Payment Method Selection", "Order Review."

**Unlabeled edges / wrong shapes** — Bare `-->` connections and mixed-up shapes break diagrams. INSTEAD: Every edge has a present-tense label (`-->|"Clicks Submit"|`); 5 shapes used consistently — rectangle=screen, diamond=decision, stadium=start/end, hexagon=process, parallelogram=I/O.

**Dead-end errors** — "Something went wrong" with no recovery path. INSTEAD: Every error state leads to a recovery action (retry, back, contact support, alternative).

**Overloaded screens** — 5+ primary actions creates decision paralysis. INSTEAD: ≤3 primary actions per screen; split or move to navigation.

**Vague decision conditions** — "If appropriate" is not implementable. INSTEAD: Exact rules a developer can code — `cart.subtotal >= 10.00`, `user.role === 'admin'`.

**Skipping validation** — Assuming structure is correct without tracing paths. INSTEAD: Validation-agent traces every path from every entry to an exit, checking orphans and dead ends.

**Flow tables without wireframes / wireframing every edge** — A screen inventory is not a screen; wireframing every edge state creates 30 frames of noise. INSTEAD: One wireframe per core screen + 2-3 critical edge variants picked on impact.

**"Cross-platform" as a platform answer** — Collapses platform-specific surface decisions into nothing. macOS, iOS, and Android surfaces are different — a flow on "cross-platform" has no defined surface set. INSTEAD: Enumerate every platform. "Cross-platform" is a refusal to enumerate.

**Pooling many flows into one file** — One `FLOW.md` for checkout + onboarding + password reset drifts quickly. INSTEAD: One flow per file at `.agents/product/flow/<flow-name>.md`. Use `index.md` for the catalog view.

**Skipping per-surface coverage** — Picking surfaces at Step 0 but only wireframing main screens, or treating "widget refresh budget exhausted" / "Live Activity 8h ceiling hit" / "universal link fell back to web" as generic "network errors." Each declared surface has specific layout constraints and specific failure modes. INSTEAD: One mini-frame per selected surface at its native dimensions, plus a per-surface edge-state table — both pulled from `references/platform-touchpoints.md`.

**Drift between wireframe and structure inventory** — Wireframe shows 5 CTAs when the structure-agent listed 2 actions. INSTEAD: Wireframe CTAs must match the structure actions column exactly.

**Wireframes without descriptions** — An ASCII frame + CTA label gives layout but not intent. INSTEAD: Each screen has a 2-4 sentence Description covering content/data, visual priority, and mood. "Shows information" is not a description — name the actual content, hierarchy, and mood.

---

## Files

**Agents:** see Agent Manifest above for the canonical list. Full instructions in [`agents/`](agents/).
**References:** [`references/research-checklist.md`](references/research-checklist.md) (pre-design research), [`references/platform-touchpoints.md`](references/platform-touchpoints.md) (surface catalog).
**Scripts:** [`scripts/generate_flow.py`](scripts/generate_flow.py) — generate Mermaid diagrams programmatically for complex / multi-variant flows.
