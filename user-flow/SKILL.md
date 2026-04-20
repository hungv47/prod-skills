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

*Design — Step 2 of 2. Coordinates specialized agents to map navigation paths, decision points, edge cases, platform-native touchpoints, and screen-to-screen transitions into a validated flow diagram.*

**Core Question:** "Can the user complete their goal without thinking — on every surface of every platform it ships on?"

## Critical Gates — Read First

- **Do NOT dispatch Layer 1 before platforms and surfaces are enumerated.** A flow without an explicit platform list and per-platform surface list has no grounding — wireframe size, entry points, and edge states all depend on it. See `references/platform-touchpoints.md` for the catalog and interview gate.
- **Do NOT accept "cross-platform" as a platform answer.** It isn't one. Enumerate every platform the flow ships on (macOS, iOS, iPadOS, Android, Windows, web-desktop, web-mobile, watchOS, tvOS, visionOS, CarPlay, Android Auto, Linux). A product that runs on macOS + iOS has two lists of surfaces, not one.
- **Do NOT create diagrams before mapping structure.** Diagram-agent needs structure-agent's screen inventory and edge-case-agent's state coverage. Visualizing before mapping produces incomplete flows.
- **Do NOT skip edge cases.** Error, empty, loading, permission, offline, *and platform-surface edge states* must be mapped for every screen and every selected surface. Happy-path-only flows break at the first unexpected state.
- **Do NOT accept >7 happy path steps without challenge.** Miller's threshold is the validation baseline. Every step must justify its existence — can it be removed, combined, or automated?
- **One flow = one file.** If the product has multiple flows (checkout, onboarding, password reset…), run this skill once per flow. Each run writes to `.agents/product/flow/<flow-name>.md`. Do not pool flows into a single file.
- **Stale product context (>30 days) produces misaligned flows.** Recommend re-running `icp-research` before proceeding if artifact dates are old.

## Inputs Required
- A product or feature requiring flow mapping (new feature, redesign, or existing flow audit)
- Target user role or persona (flows change per role)
- The user goal the flow serves (one goal per flow)
- **Target platforms** — explicit list from the platform catalog in `references/platform-touchpoints.md`
- **Per-platform surfaces in scope** — explicit list of surfaces per platform

## Output
- `.agents/product/flow/<flow-name>.md` — one file per flow run
- `.agents/product/flow/index.md` — catalog index, auto-created / auto-updated when ≥2 flow files exist in the directory

Flow name is derived from the user's brief (e.g., "checkout flow" → `checkout.md`); if ambiguous, the orchestrator confirms the slug with the user before writing.

## Quality Gate
Before delivering, the **critic agent** verifies:
- [ ] Target platforms explicitly enumerated (no "cross-platform" shorthand)
- [ ] Per-platform surfaces enumerated from `references/platform-touchpoints.md`
- [ ] Every selected platform × surface has an explicit entry point defined
- [ ] Every selected surface has at least one wireframe / mini-frame at the surface's native dimensions
- [ ] Every selected surface has per-surface edge states mapped (beyond generic error/empty/loading)
- [ ] Every decision point has ≥2 labeled exits (including the unhappy path)
- [ ] Error paths lead to recovery states — no dead ends
- [ ] Entry and exit points are explicit (not implied)
- [ ] Flow serves exactly one user goal — split if multiple goals emerged
- [ ] Empty, loading, and permission states are accounted for
- [ ] Back/cancel actions are defined at every step where the user might retreat
- [ ] Happy path ≤7 steps (Miller's threshold)
- [ ] ≤3 primary actions per screen
- [ ] Diagram notation correct (5 shapes used properly)
- [ ] Screen inventory complete with concrete names
- [ ] ASCII wireframe present for every core screen in the inventory
- [ ] Every core screen wireframe includes a 2-4 sentence Description (content/data, visual priority, mood) concrete enough for a designer or design agent to produce visuals from
- [ ] Wireframe CTAs match the structure-agent's actions column (no drift)
- [ ] 2-3 critical edge-state variants included (not one per screen, not zero)

## Chain Position
Previous: `brand-system` (optional — provides design tokens and component context) | Next: handoff to implementation

**Re-run triggers:** When product features change significantly, when user research reveals new patterns, after usability testing reveals flow issues, or when adding new user roles.

**Related skills (non-chain):** `system-architecture` (consumes flow diagrams for API design), `task-breakdown` (uses flows for feature decomposition), `discover` (generates specs that inform flows)

### Skill Deference
- **Requirements unclear?** Run `discover` first to clarify the spec.
- **Need brand context?** Run `brand-system` — it provides design tokens and component context.
- **Need to break flow into tasks?** Run `task-breakdown` after — it consumes flow diagrams.

---

## Agent Manifest

| Agent | Layer | File | Focus |
|-------|-------|------|-------|
| Structure Agent | 1 (parallel) | `agents/structure-agent.md` | Entry points, core screens, decision points, exit points, flow type, **per-platform surface entry map** |
| Edge Case Agent | 1 (parallel) | `agents/edge-case-agent.md` | Error, empty, loading, permission, offline states, **per-surface platform edge states** |
| Diagram Agent | 2 (parallel) | `agents/diagram-agent.md` | Mermaid flowchart with 5 node shapes, annotations |
| Wireframe Agent | 2 (parallel) | `agents/wireframe-agent.md` | ASCII wireframe per core screen + 2-3 critical edge-state variants + **mini-frame per selected surface** |
| Validation Agent | 2 (sequential) | `agents/validation-agent.md` | Miller's threshold, ≤3 actions/screen, structural integrity, wireframe/structure consistency, **platform-surface coverage** |
| Critic Agent | 2 (final) | `agents/critic-agent.md` | All edge cases handled, notation correct, screen inventory complete, wireframe coverage, **platform-surface coverage matrix** |

### Shared References (read by agents)
- `references/research-checklist.md` — Pre-design research: user research methods, information architecture, content strategy
- `references/platform-touchpoints.md` — Exhaustive surface catalog per platform (macOS, iOS, iPadOS, Android, Windows, web-desktop, web-mobile, watchOS, tvOS, visionOS, CarPlay, Android Auto, Linux, cross-platform channels) with entry triggers, flow roles, native dimensions, and edge states per surface

---

## Routing Logic

Only one route — all flows use the full agent stack. Complexity is handled by the structure-agent's sub-flow decomposition (flows >15 screens are split automatically).

```
1. Pre-dispatch: Gather context (Step 0) + Flow Interview + Platform & Surface Enumeration (gated)
2. LAYER 1 — Dispatch IN PARALLEL:
   - structure-agent (maps screens, decisions, transitions, per-platform surface entry points)
   - edge-case-agent (maps error, empty, loading, permission, offline, and per-surface platform edge states)
3. MERGE: Combine structure + edge cases into unified flow model + platform surface matrix
4. LAYER 2a — Dispatch IN PARALLEL (both consume merged structure + edge cases + surface matrix):
   - diagram-agent (Mermaid flowchart)
   - wireframe-agent (ASCII wireframe per core screen + critical edge variants + mini-frame per selected surface)
5. LAYER 2b — Dispatch SEQUENTIALLY:
   - validation-agent (receives structure + edge cases + diagram + wireframes + surface matrix)
   - critic-agent (receives complete flow)
6. If FAIL → re-dispatch named agent(s) with feedback (max 2 cycles)
7. Deliver artifact at `.agents/product/flow/<flow-name>.md`; update `index.md` if ≥2 flows exist
```

---

## Step 0: Pre-Dispatch Context Gathering

### Product Context Check
Check for `.agents/product-context.md`. If missing: **INTERVIEW.** Interview for product dimensions (what, who, problem, differentiator, constraints) and save to `.agents/product-context.md`. Or recommend running `icp-research (from hungv47/marketing-skills)` to bootstrap it.

If `.agents/product-context.md` has a `date` field older than 30 days, recommend re-running `icp-research` to refresh it before proceeding. Tip: `/navigate status` (from meta-skills) gives a single-pass freshness report across all upstream artifacts.

### Required Artifacts
None — this skill can run standalone.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | icp-research (from hungv47/marketing-skills) | Product and user context for better flow decisions |
| `brand/DESIGN.md` | brand-system | Component inventory and design tokens inform screen-level detail |
| `brand/BRAND.md` | brand-system | Voice + terminology — useful when writing screen Descriptions (content/data/mood) |

### Flow Interview
Interview for these dimensions before proceeding:

**Product context**
1. What product or feature needs flow mapping?
2. What problem does it solve for the user?
3. Who is the primary user? (role, technical skill, frequency of use)

**Flow scope**
4. What is the single user goal this flow serves?
5. Confirm the flow name — auto-derived as a slug from your brief (e.g. "checkout flow" → `checkout`). Say so if you want something different.
6. Where does the flow start? (specific trigger: link click, app launch, notification tap — answer multiple if multi-surface)
7. What does success look like? (specific end state)
8. Are there existing flows to reference, replace, or extend?

**Platforms & surfaces — mandatory gate (see `references/platform-touchpoints.md`)**
9. **Target platforms** — pick one or more explicit values: `macOS`, `iOS`, `iPadOS`, `Android`, `Windows`, `web-desktop`, `web-mobile`, `watchOS`, `tvOS`, `visionOS`, `CarPlay`, `Android Auto`, `Linux`. Reject "cross-platform" as an answer; push the user to enumerate.
10. **Per-platform surfaces in scope** — for every platform selected in Q9, open the catalog and pick every surface that will carry this flow. Examples:
    - macOS: dock tile · menu bar extra (NSStatusItem) · Notification Center · Spotlight · Services · Share extension · widgets · Finder ext · URL scheme · Handoff · App Intents · first-run · background agent · keyboard shortcuts · command palette · (etc.)
    - iOS/iPadOS: home icon · widgets (small/medium/large/lock) · Dynamic Island · Live Activity · Control Center · Spotlight · Siri/App Intents · notifications · Focus · universal links · App Clips · share sheet · Files · IME · PiP · CarPlay · iPad multitasking · Pencil · external keyboard · background modes · (etc.)
    - Android: launcher icon · widgets · Quick Settings tile · notifications · bubble · deep links · app shortcuts · Assistant · Auto · Wear · PiP · multi-window · IME · foreground service · (etc.)
    - Windows: Start · taskbar · jump list · system tray · toast · Widgets board · Explorer context · Snap layouts · URI protocol · (etc.)
    - web-desktop: tab/title · URL routing · Web Push · PWA install · Share/Badging/FSA APIs · service worker offline · OAuth redirects · (etc.)
    - web-mobile: PWA install · pull-to-refresh · back button · gestures · safe areas · mobile Web Push · (etc.)
    - watchOS / tvOS / visionOS / CarPlay / Linux: (see catalog)
11. **Cross-platform channels in scope** — email · SMS · push · calendar invite · in-app messaging · third-party chat · clipboard · OS contacts share.
12. **Primary surface per platform** — which *one* surface is the flow's default entry on each platform (used to pick the default wireframe size).

**Constraints**
13. Authentication requirements? (logged in, guest, role-based)
14. Technical or business rules that force specific paths?
15. Minimum OS versions? (drives which surfaces are available — e.g., Live Activities iOS 16.1+, Control Center custom controls iOS 18+)

**Gate:** Do not proceed to Layer 1 until Q9–Q12 are answered explicitly. "All surfaces" and "cross-platform" are not acceptable answers — they fail the enumeration test and force the orchestrator to ask again.

### Context to Pass to All Agents
1. **Product:** description, feature, problem it solves
2. **User:** role, persona, technical skill, frequency
3. **Goal:** the single user goal this flow serves
4. **Flow name / slug:** artifact filename for `.agents/product/flow/<slug>.md`
5. **Platform list:** explicit platforms (no "cross-platform" shorthand)
6. **Surface matrix:** selected surfaces per platform (subset of the catalog)
7. **Cross-platform channels:** email / SMS / push / etc.
8. **Primary surface per platform:** default entry on each platform
9. **Minimum OS versions** per platform
10. **Constraints:** auth requirements, business rules, existing flows

---

## Dispatch Protocol

### How to spawn a sub-agent

1. **Read** the agent instruction file — include its FULL content in the Agent prompt
2. **Append** the context (product, user, goal, platform, constraints) after the instructions
3. **Resolve file paths to absolute**: replace relative paths with absolute paths rooted at this skill's directory
4. **Pass upstream artifacts by content**: the orchestrator reads `.agents/` files FIRST, then includes relevant excerpts in context. Sub-agents should NOT read artifact files directly.
5. If **feedback** exists (from critic FAIL), append with header "## Critic Feedback — Address Every Point"

### Conventions

- **Source citation:** When stating facts about UX heuristics, usability research, or interaction patterns, cite the source. If from a web search, include the URL. If a fact cannot be attributed, flag it as `[UNVERIFIED]`.
- **Context loaded:** When producing the artifact, include which upstream artifacts were read and their versions/dates in the artifact body. This creates an audit trail for downstream skills.

### Single-agent fallback

If multi-agent dispatch is unavailable, execute each agent's instructions sequentially in-context:
- Layer 1: map flow structure (screens, decisions, entries, exits), then map edge cases (error, empty, loading, permission, offline)
- Layer 2: create Mermaid diagram from structure + edge cases, draft ASCII wireframes for every core screen + 2-3 critical edge-state variants, then validate against usability thresholds and wireframe/structure consistency
- Final: evaluate with critic rubric

---

## Layer 1: Parallel Foundation

Spawn **IN PARALLEL**:

| Agent | Instruction File | Pass These Inputs | Reference Files |
|-------|-----------------|-------------------|-----------------|
| Structure Agent | `agents/structure-agent.md` | brief (product + user + goal + platforms + surface matrix + constraints) | `references/research-checklist.md`, `references/platform-touchpoints.md` |
| Edge Case Agent | `agents/edge-case-agent.md` | brief (product + user + goal + platforms + surface matrix + constraints) | `references/research-checklist.md`, `references/platform-touchpoints.md` |

Wait for both to complete. Their outputs feed the merge step and Layer 2.

---

## Merge Step

Combine structure-agent and edge-case-agent outputs into a unified flow model:

| Section | Owner Agent |
|---------|-----------|
| Flow classification | Structure Agent |
| Entry points (core) | Structure Agent |
| **Platform-surface entry matrix** (per platform × surface) | Structure Agent |
| Core screens (name, purpose, actions, responses) | Structure Agent |
| Decision points (condition, exits, who decides) | Structure Agent |
| Exit points | Structure Agent |
| Screen-to-screen transitions | Structure Agent |
| Error states per screen | Edge Case Agent |
| Empty states per screen | Edge Case Agent |
| Loading states per screen | Edge Case Agent |
| Permission states per screen | Edge Case Agent |
| Offline states per screen | Edge Case Agent |
| **Per-surface platform edge states** (app not running, widget stale, background refresh throttled, notification grouping, permission per surface, deep-link fallback, etc.) | Edge Case Agent |
| Back/cancel paths | Edge Case Agent |

**Cross-reference checks before Layer 2:**
1. Every screen in the structure inventory has edge case coverage.
2. Every platform × surface declared at Step 0 has an entry row in the platform-surface matrix.
3. Every platform × surface has at least one per-surface edge state entry.

If any check fails, flag it before dispatching Layer 2.

---

## Layer 2a: Parallel Rendering

Spawn **IN PARALLEL** (both consume the same merged Layer 1 output):

| Agent | Instruction File | Pass These Inputs | Reference Files |
|-------|-----------------|-------------------|-----------------|
| Diagram Agent | `agents/diagram-agent.md` | brief + merged structure + edge cases | none |
| Wireframe Agent | `agents/wireframe-agent.md` | brief + platforms + surface matrix + merged structure + edge cases | `references/platform-touchpoints.md` (for per-surface native dimensions) |

Wait for both to complete before Layer 2b.

## Layer 2b: Sequential Chain

Dispatch **ONE AT A TIME, IN ORDER**:

| Step | Agent | Instruction File | Receives |
|------|-------|-----------------|----------|
| 1 | Validation Agent | `agents/validation-agent.md` | Structure + edge cases + diagram + wireframes |
| 2 | Critic Agent | `agents/critic-agent.md` | Complete flow (all outputs merged + validation results) |

---

## Critic Gate

- **PASS:** Deliver the artifact.
- **FAIL:** Re-dispatch named agent(s) with critic feedback. Max 2 rewrite cycles. After 2 failures, deliver with critic annotations and flag to user.

---

## Artifact Template

**Output path:** `.agents/product/flow/<flow-name>.md` (one file per flow).

**On re-run of the same flow:** rename the existing `<flow-name>.md` to `<flow-name>.v[N].md` and create a new file at `<flow-name>.md` with incremented version.

**Multi-flow products:** run this skill once per flow — each run creates its own file. After any run that results in ≥2 **distinct flow slugs** (not counting `.v[N]` versioned files of the same flow) in `.agents/product/flow/`, the orchestrator auto-creates or updates `.agents/product/flow/index.md` (see template below). Versioned files like `checkout.v1.md` sit next to their live `checkout.md` and are excluded from the slug count and from the index.

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
| macOS | ★ Main window | Menu bar extra · Notification Center · Spotlight · widgets · URL scheme | Dock right-click · Services · Finder ext · Touch Bar |
| iOS | ★ Home icon | Lock-screen widget · Dynamic Island · share sheet · App Intents · universal links | App Clips · CarPlay · Siri |
| web-desktop | ★ URL routing | Web Push · PWA install · OAuth redirect | Badging API · extension |

### Cross-platform channels in scope
- [ ] Email
- [ ] SMS
- [ ] Push
- [ ] Calendar invite
- [ ] Clipboard
- [ ] In-app messaging
- [ ] Third-party chat

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
| macOS | Menu bar extra | Click status icon | Cached user + last job id | Optional | Quick-action popover | Returns focus to previous app |
| iOS | Dynamic Island (compact) | Server push Live Activity | Live order status | Yes | Expanded Live Activity view | Auto-dismiss at delivery |
| web-desktop | URL routing `/flow/checkout` | Paste / link | Cart from cookie | Guest + member | Cart review | Redirect to `/orders/:id` |

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

*One ASCII mini-frame per selected surface, rendered at the surface's native dimensions. See `references/platform-touchpoints.md` for dimensions.*

### macOS — Menu bar extra (32 chars wide × ≤10 lines)

**Why this surface carries this flow:** [one line — what the surface does for this flow]

​```
┌──────────────────────────────┐
│  [ mini-frame ]              │
└──────────────────────────────┘
​```

### iOS — Dynamic Island (compact + expanded)

​```
compact:  ( ○ Active · 4m )
expanded: ┌──────────────────────────────┐
          │ [ expanded Live Activity ]   │
          └──────────────────────────────┘
​```

[Repeat for every selected surface from the matrix]

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
| macOS | Menu bar extra | ✓ | ✓ | ✓ |

## Edge Cases Handled

| State | Screen(s) | Handling |
|-------|-----------|----------|
| Error | [screens] | [recovery path] |
| Empty | [screens] | [placeholder/onboarding] |
| Loading | [screens] | [skeleton/spinner] |
| Permission | [screens] | [upgrade/redirect] |

## Per-Surface Edge States

Surface-specific failure modes that generic error/empty/loading don't capture. Pulled from `references/platform-touchpoints.md` per selected surface.

| Platform | Surface | Edge state | Handling |
|----------|---------|------------|----------|
| macOS | Menu bar extra | App terminated → icon disappears | Background agent relaunches on login; status icon reappears within 2s |
| macOS | Menu bar extra | Light/dark mode glyph swap | Provide template icon + tinted asset |
| iOS | Dynamic Island | 8h Live Activity ceiling hit | Demote to standard push notification with deep link to resume |
| iOS | Widget (medium) | Background refresh throttled by OS | Show last-known data + subtle "updated Nm ago" timestamp |
| web-desktop | Web Push | Permission denied | Fall back to in-app banner on next session; never re-prompt |

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
| [checkout.md](./checkout.md) | Checkout | iOS, Android, web-desktop, web-mobile | 2026-04-20 | 1 | draft |
| [onboarding.md](./onboarding.md) | Onboarding | iOS, Android | 2026-04-19 | 2 | done |
| [password-reset.md](./password-reset.md) | Password reset | iOS, Android, web-desktop | 2026-04-18 | 1 | done |

## Platform coverage at a glance

| Platform | Flows touching this platform |
|----------|-------------------------------|
| iOS | checkout · onboarding · password-reset |
| Android | checkout · onboarding · password-reset |
| web-desktop | checkout · password-reset |
| web-mobile | checkout |
```

---

## Worked Example — Food-Delivery Checkout (Multi-Platform)

**User:** "Map the checkout flow for our food-delivery app. We ship on iOS, Android, and web."

### Step 0: Pre-Dispatch + Interview
- Flow name / slug: `checkout`
- User: Logged-in customer with items in cart
- Goal: Complete purchase
- Platforms: `iOS` (17+), `iPadOS` (17+), `Android` (13+), `web-desktop`, `web-mobile`
- Surfaces per platform (subset from catalog):
  - **iOS:** ★ Home icon · Lock-screen widget (order-in-progress) · Dynamic Island / Live Activity (order tracking) · Apple Pay sheet · universal link
  - **iPadOS:** ★ Home icon · Live Activity · Split View layout
  - **Android:** ★ Launcher icon · Quick Settings tile (order status) · notification + inline reply · Google Pay sheet · app link
  - **web-desktop:** ★ URL routing `/checkout` · Web Push (delivery updates) · OAuth redirect (Apple/Google sign-in)
  - **web-mobile:** ★ URL routing · Safari share / Add-to-Home-Screen PWA · safe-area layout
- Cross-platform channels: email (receipt), push (order updates), SMS (fallback receipt)
- Flow type: Branching (payment method creates 3 parallel paths)
- Constraints: Apple Pay / Google Pay / credit card. Minimum order $10. Live Activity required for "order placed → delivered."

### Layer 1: Parallel Foundation
- **Structure agent** returns: 6 core screens (Cart Review, Shipping Address, Shipping Method, Payment Selection, Order Review, Order Confirmation). 3 decision points. 3 exits. **Per-surface entry matrix** with 13 rows (5 platforms × their selected surfaces), each specifying entry trigger, pre-loaded state, auth required, first screen.
- **Edge case agent** returns: Standard error / empty / loading / permission / offline coverage per screen. **Per-surface edge states:** (iOS Live Activity 8h ceiling → demote to push), (Android Quick Settings tile out of sync → force refresh on reopen), (web Push denied → in-app banner fallback), (PWA standalone mode state loss on iOS → restore from server), (universal link falls back to web if app not installed → deep-link parity).

### Merge
Matrix built. Cross-ref checks: all 6 screens have edge coverage; all 13 platform×surface rows have entries; all 13 have per-surface edge states. Proceed.

### Layer 2a: Parallel Rendering
- **Diagram agent** returns: Mermaid `graph TD` with 5 node shapes, annotations, sub-flow reference.
- **Wireframe agent** returns: 6 core-screen ASCII wireframes (mobile 34 chars for iOS/Android, desktop 68 chars for web), 2 critical edge variants, and **13 per-surface mini-frames**:
  - iOS Lock-screen widget (rectangular accessory, ~180×50pt proxy): shows order ETA glanceable
  - iOS Dynamic Island (compact + expanded): "○ Cooking · 12m" / expanded with progress bar + driver avatar
  - iOS Apple Pay sheet (36 chars): merchant · line items · total · Pay with Face ID
  - iPadOS Split View: cart pane 48 chars + menu pane 48 chars
  - Android Quick Settings tile: glyph + order-state label
  - Android notification with inline reply to "Where's my order?"
  - Google Pay sheet
  - web-desktop URL routing: 68-char URL bar + breadcrumb
  - web-desktop Web Push card
  - OAuth redirect sequence
  - web-mobile PWA shell with safe-area padding
  - web-mobile Add-to-Home-Screen prompt
  - (cross-platform) email receipt layout

### Layer 2b: Sequential Validation
- **Validation agent** returns: Happy path 5 steps (PASS ≤7). Max 3 actions per screen (PASS). All paths traced to exits (PASS). Surface coverage: 13/13 with entry + mini-frame + per-surface edge state (PASS). Handoff ready.
- **Critic agent** returns: PASS. Scoring 4.8.

### Deliver
Artifact saved to `.agents/product/flow/checkout.md`. Orchestrator checks the directory and finds only this flow — no `index.md` created yet. When a second flow (e.g., `onboarding.md`) is later produced, orchestrator creates the index on that second run.

---

## Anti-Patterns

**Happy path only** — Mapping only the success path produces flows that break at the first error. INSTEAD: Edge-case-agent runs in parallel with structure-agent, ensuring error/empty/loading/permission/offline states are mapped for every screen.

**Generic screen names** — "Step 1", "Step 2", "Step 3" tell nobody anything. INSTEAD: Concrete names that match dev/design vocabulary: "Payment Method Selection", "Shipping Address", "Order Review."

**Unlabeled diagram edges** — Bare `-->` connections create ambiguity. INSTEAD: Every edge has a label: `-->|"Clicks Submit"|`. Labels use present tense.

**Wrong diagram shapes** — Using rectangles for decisions or diamonds for screens. INSTEAD: 5 shapes used consistently — rectangle=screen, diamond=decision, stadium=start/end, hexagon=process, parallelogram=I/O.

**Dead-end errors** — "Something went wrong" with no recovery path. INSTEAD: Every error state leads to a recovery action (retry, go back, contact support, try alternative).

**Overloaded screens** — A screen with 5+ primary actions creates decision paralysis. INSTEAD: Split into focused screens or move secondary actions to navigation. ≤3 primary actions per screen.

**Vague decision conditions** — "If appropriate" or "when ready" are not implementable. INSTEAD: Exact rules a developer can code: "cart.subtotal >= 10.00", "user.role === 'admin'".

**Skipping validation** — Assuming the structure is correct without tracing paths. INSTEAD: Validation-agent traces every path from every entry to an exit, checking for orphans and dead ends.

**Flow tables without wireframes** — A screen inventory is a description, not a screen. Readers can't see layout, hierarchy, or CTA placement. INSTEAD: Wireframe-agent drafts one ASCII wireframe per core screen so every screen is a readable layout, not just a row in a table.

**Wireframing every edge state** — 6 screens × 5 edge states = 30 wireframes of noise. INSTEAD: Wireframe every core screen (always), plus 2-3 critical edge variants picked on impact (payment error, empty-state on core-value screen, permission denied on feature screen).

**"Cross-platform" as a platform answer** — Treating "cross-platform" as a valid Step 0 answer collapses platform-specific surface decisions into nothing. The whole point of the interview gate is that macOS surfaces, iOS surfaces, and Android surfaces are different — a flow on "cross-platform" has no defined surface set. INSTEAD: Force enumeration: `macOS + iOS + Android + web-desktop` is a list. "Cross-platform" is a refusal to enumerate.

**Pooling many flows into one file** — A single `FLOW.md` that tries to document checkout + onboarding + password reset becomes unreadable and drifts quickly (one feature changes, the whole file is stale). INSTEAD: One flow per file at `.agents/product/flow/<flow-name>.md`. Use `index.md` for the catalog view.

**Skipping per-surface mini-frames** — Picking surfaces at Step 0 but only wireframing main screens defeats the point. The menu-bar dropdown, Dynamic Island, widget, and notification card each have specific layout constraints that the main-window wireframe doesn't show. INSTEAD: One mini-frame per selected surface, rendered at that surface's native dimensions from `references/platform-touchpoints.md`.

**Treating surface-specific edge states as generic errors** — "Network error" doesn't cover "widget refresh budget exhausted" or "Live Activity 8h ceiling hit" or "universal link fell back to web because app not installed." Those are surface-specific edge states with surface-specific recovery paths. INSTEAD: The edge-case-agent produces a per-surface edge-state table in addition to the standard 5-category table.

**Drift between wireframe and structure inventory** — Wireframe shows 5 CTAs when the structure-agent listed 2 actions. INSTEAD: Wireframe CTAs must match the structure actions column exactly. Drift is a FAIL — either update structure or reduce the wireframe.

**Wireframes without descriptions** — An ASCII frame + CTA label gives layout but not intent. A designer or design agent can't infer what copy, data, or feeling belongs without guessing. INSTEAD: Each screen has a 2-4 sentence Description covering content/data, visual priority, and mood. "Shows information" is not a description — name the actual content, the actual hierarchy, the actual mood.

---

## Agent Files

### Sub-Agent Instructions (agents/)
- [agents/structure-agent.md](agents/structure-agent.md) — Entry points, screens, decisions, exits, flow type
- [agents/edge-case-agent.md](agents/edge-case-agent.md) — Error, empty, loading, permission, offline states
- [agents/diagram-agent.md](agents/diagram-agent.md) — Mermaid flowchart, annotations, sub-flow references
- [agents/wireframe-agent.md](agents/wireframe-agent.md) — ASCII wireframes per core screen + critical edge-state variants
- [agents/validation-agent.md](agents/validation-agent.md) — Usability thresholds, structural integrity, wireframe/structure consistency, handoff readiness
- [agents/critic-agent.md](agents/critic-agent.md) — Quality scoring, PASS/FAIL

### Shared References (references/)
- [references/research-checklist.md](references/research-checklist.md) — Pre-design research: user research methods, information architecture, content strategy
- [references/platform-touchpoints.md](references/platform-touchpoints.md) — Exhaustive platform surface catalog (macOS, iOS, iPadOS, Android, Windows, web-desktop, web-mobile, watchOS, tvOS, visionOS, CarPlay, Android Auto, Linux, cross-platform channels)

### Scripts
- [scripts/generate_flow.py](scripts/generate_flow.py) — Generate Mermaid diagrams programmatically for complex or multi-variant flows
