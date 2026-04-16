---
name: user-flow
description: "Maps multi-step in-product flows — screens, decisions, transitions, edge cases, and error states for features or user journeys. Produces `.agents/design/user-flow.md`. Not for visual brand design (use brand-system) or single-page conversion (use lp-optimization). For technical architecture, see system-architecture. For task decomposition, see task-breakdown."
argument-hint: "[feature or flow to map]"
allowed-tools: Read Grep Glob Bash
license: MIT
metadata:
  author: hungv47
  version: "3.0.0"
  budget: standard
  estimated-cost: "$0.15-0.40"
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
    - design/user-flow.md
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

*Design — Step 2 of 2. Coordinates specialized agents to map navigation paths, decision points, edge cases, and screen-to-screen transitions into a validated flow diagram.*

**Core Question:** "Can the user complete their goal without thinking?"

## Critical Gates — Read First

- **Do NOT create diagrams before mapping structure.** Diagram-agent needs structure-agent's screen inventory and edge-case-agent's state coverage. Visualizing before mapping produces incomplete flows.
- **Do NOT skip edge cases.** Error, empty, loading, permission, and offline states must be mapped for every screen. Happy-path-only flows break at the first unexpected state.
- **Do NOT accept >7 happy path steps without challenge.** Miller's threshold is the validation baseline. Every step must justify its existence — can it be removed, combined, or automated?
- **Stale product context (>30 days) produces misaligned flows.** Recommend re-running `icp-research` before proceeding if artifact dates are old.

## Inputs Required
- A product or feature requiring flow mapping (new feature, redesign, or existing flow audit)
- Target user role or persona (flows change per role)
- The user goal the flow serves (one goal per flow)

## Output
- `.agents/design/user-flow.md`

## Quality Gate
Before delivering, the **critic agent** verifies:
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
| Structure Agent | 1 (parallel) | `agents/structure-agent.md` | Entry points, core screens, decision points, exit points, flow type |
| Edge Case Agent | 1 (parallel) | `agents/edge-case-agent.md` | Error, empty, loading, permission, offline states |
| Diagram Agent | 2 (sequential) | `agents/diagram-agent.md` | Mermaid flowchart with 5 node shapes, annotations |
| Validation Agent | 2 (sequential) | `agents/validation-agent.md` | Miller's threshold, ≤3 actions/screen, structural integrity |
| Critic Agent | 2 (final) | `agents/critic-agent.md` | All edge cases handled, notation correct, screen inventory complete |

### Shared References (read by agents)
- `references/research-checklist.md` — Pre-design research: user research methods, information architecture, content strategy

---

## Routing Logic

Only one route — all flows use the full agent stack. Complexity is handled by the structure-agent's sub-flow decomposition (flows >15 screens are split automatically).

```
1. Pre-dispatch: Gather context (Step 0) + Flow Interview
2. LAYER 1 — Dispatch IN PARALLEL:
   - structure-agent (maps screens, decisions, transitions)
   - edge-case-agent (maps error, empty, loading, permission, offline states)
3. MERGE: Combine structure + edge cases into unified flow model
4. LAYER 2 — Dispatch SEQUENTIALLY:
   - diagram-agent (receives merged structure + edge cases)
   - validation-agent (receives structure + edge cases + diagram)
5. Dispatch: critic-agent (receives complete flow)
6. If FAIL → re-dispatch named agent(s) with feedback (max 2 cycles)
7. Deliver artifact
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
| `.agents/design/brand-system.md` | brand-system | Component inventory and design tokens inform screen-level detail |

### Flow Interview
Interview for these dimensions before proceeding:

**Product context**
1. What product or feature needs flow mapping?
2. What problem does it solve for the user?
3. Who is the primary user? (role, technical skill, frequency of use)

**Flow scope**
4. What is the single user goal this flow serves?
5. Where does the flow start? (specific trigger: link click, app launch, notification tap)
6. What does success look like? (specific end state)
7. Are there existing flows to reference, replace, or extend?

**Constraints**
8. Platform — web, iOS, Android, cross-platform?
9. Authentication requirements? (logged in, guest, role-based)
10. Technical or business rules that force specific paths?

### Context to Pass to All Agents
1. **Product:** description, feature, problem it solves
2. **User:** role, persona, technical skill, frequency
3. **Goal:** the single user goal this flow serves
4. **Platform:** web, iOS, Android, cross-platform
5. **Constraints:** auth requirements, business rules, existing flows

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
- Layer 2: create Mermaid diagram from structure + edge cases, then validate against usability thresholds
- Final: evaluate with critic rubric

---

## Layer 1: Parallel Foundation

Spawn **IN PARALLEL**:

| Agent | Instruction File | Pass These Inputs | Reference Files |
|-------|-----------------|-------------------|-----------------|
| Structure Agent | `agents/structure-agent.md` | brief (product + user + goal + platform + constraints) | `references/research-checklist.md` |
| Edge Case Agent | `agents/edge-case-agent.md` | brief (product + user + goal + platform + constraints) | `references/research-checklist.md` |

Wait for both to complete. Their outputs feed the merge step and Layer 2.

---

## Merge Step

Combine structure-agent and edge-case-agent outputs into a unified flow model:

| Section | Owner Agent |
|---------|-----------|
| Flow classification | Structure Agent |
| Entry points | Structure Agent |
| Core screens (name, purpose, actions, responses) | Structure Agent |
| Decision points (condition, exits, who decides) | Structure Agent |
| Exit points | Structure Agent |
| Screen-to-screen transitions | Structure Agent |
| Error states per screen | Edge Case Agent |
| Empty states per screen | Edge Case Agent |
| Loading states per screen | Edge Case Agent |
| Permission states per screen | Edge Case Agent |
| Offline states per screen | Edge Case Agent |
| Back/cancel paths | Edge Case Agent |

**Cross-reference check before Layer 2:** Verify that every screen in the structure-agent's inventory has been checked by the edge-case-agent. If any screen is missing edge case coverage, flag it before dispatching diagram-agent.

---

## Layer 2: Sequential Chain

Dispatch **ONE AT A TIME, IN ORDER**:

| Step | Agent | Instruction File | Receives |
|------|-------|-----------------|----------|
| 1 | Diagram Agent | `agents/diagram-agent.md` | Merged structure + edge cases |
| 2 | Validation Agent | `agents/validation-agent.md` | Structure + edge cases + diagram |
| 3 | Critic Agent | `agents/critic-agent.md` | Complete flow (all outputs merged + validation results) |

---

## Critic Gate

- **PASS:** Deliver the artifact.
- **FAIL:** Re-dispatch named agent(s) with critic feedback. Max 2 rewrite cycles. After 2 failures, deliver with critic annotations and flag to user.

---

## Artifact Template

On re-run: rename existing artifact to `user-flow.v[N].md` and create new with incremented version.

```markdown
---
skill: user-flow
version: 1
date: {{today}}
status: draft
---

# User Flow: [Flow Name]

## Context
- **Product:** [product/feature]
- **User:** [role/persona]
- **Goal:** [single user goal]
- **Platform:** [web/iOS/Android/cross-platform]
- **Flow type:** [linear/branching/cyclical/hub-and-spoke]

## Flow Diagram

​```mermaid
graph TD
    [diagram here]
​```

**Annotations:**
1. [Node]: [implementation detail or business rule]

## Screen Inventory

| # | Screen | Purpose | Actions | Next States |
|---|--------|---------|---------|-------------|
| 1 | [name] | [why it exists] | [user actions] | [where each action leads] |

## Edge Cases Handled

| State | Screen(s) | Handling |
|-------|-----------|----------|
| Error | [screens] | [recovery path] |
| Empty | [screens] | [placeholder/onboarding] |
| Loading | [screens] | [skeleton/spinner] |
| Permission | [screens] | [upgrade/redirect] |

## Validation Summary

- Happy path length: [N steps]
- Decision points: [N total]
- Error recovery paths: [N total]
- Dead ends: 0

## Sub-flows

- [Sub-flow name] → see `user-flow-[name].md`

## Next Step

Hand off to implementation. Pair with `brand-system` for visual design tokens if not already created.
```

---

## Worked Example — Mobile Checkout (Full Flow)

**User:** "Map the checkout flow for our e-commerce app."

### Step 0: Pre-Dispatch + Interview
- Platform: Mobile app, iOS and Android
- User: Logged-in customer with items in cart
- Entry: User taps "Checkout" from cart
- Goal: Complete purchase
- Constraints: Apple Pay, credit card, PayPal. Minimum order $10.
- Flow type assessment: Branching (payment method creates 3 parallel paths)

### Layer 1: Parallel Foundation
Both agents dispatched in parallel:
- **Structure agent** returns: 6 core screens (Shipping Address, Shipping Method, Payment Selection, Card Entry Form, Order Review, Order Confirmation). 3 decision points (minimum check, payment method, payment result). 2 entry points (Checkout button, deep link). 3 exits (success, abandonment, back to cart).
- **Edge case agent** returns: Error states for payment (API timeout, card declined, rate limit). Empty state for address (pre-fill from profile). Loading state for payment processing (spinner + disable back). Permission state for Apple Pay (hide if unsupported). Back/cancel at every screen with data preservation.

### Merge
Combined into unified flow model. Cross-reference: all 6 screens have edge case coverage. Proceed.

### Layer 2: Sequential Chain
- **Diagram agent** returns: Mermaid `graph TD` with correct shapes (stadiums for entry/exit, diamonds for decisions, hexagons for payment processing). 3 annotations (MinCheck evaluated on subtotal, ApplePay uses Stripe SDK, Processing 3s timeout).
- **Validation agent** returns: Happy path 5 steps (PASS ≤7). Max 3 actions per screen (PASS). All paths traced to exits (PASS). 3 error recovery paths (PASS). 0 dead ends. Handoff ready (screen names match dev vocabulary, conditions implementable).
- **Critic agent** returns: PASS. All quality gate items checked. Scoring: structural integrity 5, edge case coverage 5, diagram correctness 5, usability 5, handoff readiness 4 (one annotation could be more specific). Overall: 4.8.

### Deliver
Artifact saved to `.agents/design/user-flow.md`.

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

---

## Agent Files

### Sub-Agent Instructions (agents/)
- [agents/structure-agent.md](agents/structure-agent.md) — Entry points, screens, decisions, exits, flow type
- [agents/edge-case-agent.md](agents/edge-case-agent.md) — Error, empty, loading, permission, offline states
- [agents/diagram-agent.md](agents/diagram-agent.md) — Mermaid flowchart, annotations, sub-flow references
- [agents/validation-agent.md](agents/validation-agent.md) — Usability thresholds, structural integrity, handoff readiness
- [agents/critic-agent.md](agents/critic-agent.md) — Quality scoring, PASS/FAIL

### Shared References (references/)
- [references/research-checklist.md](references/research-checklist.md) — Pre-design research: user research methods, information architecture, content strategy

### Scripts
- [scripts/generate_flow.py](scripts/generate_flow.py) — Generate Mermaid diagrams programmatically for complex or multi-variant flows
