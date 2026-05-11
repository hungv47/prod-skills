---
name: orchestrate-product
description: "Stack orchestrator for product-skills. Reads what's already done in `.agents/skill-artifacts/product/`, `architecture/`, and `research/`, parses your intent, and proposes the next 1–3 skills (user-flow → system-architecture → docs-writing, plus standalone code-cleanup and machine-cleanup). Use when you don't know which product skill to invoke, or want a guided run from user flows through architecture to docs. Not for executing the work itself — it routes to the skill that does. Not for cross-stack workflows (use orchestrate-meta or invoke skills directly). Renamed from `start-product` in v3.0.0."
argument-hint: "[free-form ask, or empty to be guided]"
allowed-tools: Read Grep Glob Bash
user-invocable: true
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
  budget: standard
  estimated-cost: "$0.10-0.30"
promptSignals:
  phrases:
    - "where do i start with product"
    - "what skill should i use for product"
    - "start product"
    - "begin product"
    - "product workflow"
    - "i need to design a feature"
    - "build something"
  allOf:
    - [where, start, product]
    - [what, skill, product]
  anyOf:
    - "product workflow"
    - "design a feature"
    - "system design"
    - "user journey"
    - "code cleanup"
    - "machine cleanup"
    - "documentation"
  noneOf:
    - "marketing campaign"
    - "landing page"
    - "icp"
  minScore: 5
routing:
  intent-tags:
    - product-orchestration
    - workflow-routing
    - stack-entry-point
    - product-guide
  position: orchestrator
  lifecycle: pipeline
  produces:
    - .agents/experience/product-workflow.md
  side-effects:
    - manifest-sync
  consumes:
    - research/product-context.md
    - .agents/skill-artifacts/product/flow/*.md
    - .agents/skill-artifacts/product/flow/index.md
    - architecture/system-architecture.md
    - .agents/skill-artifacts/meta/records/cleanup-*.md
    - .agents/skill-artifacts/meta/records/machine-cleanup-*.md
    - .agents/skill-artifacts/meta/specs/*.md
    - .agents/skill-artifacts/meta/tasks.md
    - .agents/experience/*.md
  requires: []
  defers-to:
    - skill: user-flow
      when: "designing a feature with multiple screens / decisions / states"
    - skill: system-architecture
      when: "tech stack, schema, API design, file structure"
    - skill: docs-writing
      when: "README, API reference, runbook, ship log, setup guide"
    - skill: code-cleanup
      when: "auditing existing code for dead code, duplication, refactor candidates"
    - skill: machine-cleanup
      when: "auditing developer machine — caches, dotfolders, package globals"
    - skill: discover
      when: "spec is unclear before any product skill can run"
    - skill: task-breakdown
      when: "spec + architecture exist, need a buildable task list"
  parallel-with: []
  interactive: true
  estimated-complexity: low
---

# Orchestrate Product

*Meta — Stack orchestrator. The entry point for the product-skills stack when you don't know what to invoke.*

**Core Job:** read what exists in `.agents/skill-artifacts/product/`, `architecture/`, and `research/`, infer where you are, propose the next skill.

**Core Question:** "Given the spec, the user-flow state, and the architecture state, what's the next product skill to run?"

This skill does NOT execute product work. It is a router. The actual work is done by the skill it routes you to.

---

## When To Use

- You just installed product-skills and don't know what to type.
- You're mid-build and forget which skill is next.
- You have a vague need ("design this feature", "clean up the codebase", "document this", "tidy my machine") and want a guided routing.
- You want to resume across sessions.

## When NOT To Use

- You already know which skill to run.
- Your task is cross-stack (e.g., needs research + product). Use `/orchestrate-meta`.
- You want execution rather than routing.

---

## How It Works

1. **State detection** — silently read `.agents/skill-artifacts/product/`, `architecture/`, `.agents/skill-artifacts/meta/specs/*.md`, `.agents/skill-artifacts/meta/tasks.md`, `.agents/experience/*.md`, `research/product-context.md`.
2. **Intention analysis** — parse user's free-form ask. If empty, ask one bundled scoping question.
3. **Routing decision** — propose 1–3 skills with rationale + cost + duration.
4. **User confirmation** — print hand-off `/skill-name` and exit. Never auto-invoke.

---

## Step 1: State Detection

**Disk snapshot** (rendered inline when `/orchestrate-product` is invoked — see `meta-skills/CLAUDE.md` §"Skill-Authoring Patterns" for the inline-shell-interpolation convention):

```
Artifacts by domain:
! `[ -d .agents/skill-artifacts ] && find .agents/skill-artifacts -mindepth 2 -name "*.md" -type f 2>/dev/null | awk -F/ '{print $3}' | sort | uniq -c | sort -rn | grep . || echo "  (no .agents/skill-artifacts/ yet)"`

Top-level canonical folders present:
! `found=0; for d in research brand architecture; do [ -d "$d" ] && { echo "  $d/ ✓"; found=1; }; done; [ $found -eq 0 ] && echo "  (none yet)" || true`

Last 5 commits in this repo:
! `git log --oneline -5 2>/dev/null | grep . || echo "no git history"`
```

The `! \`...\`` lines run at slash-command invocation time and substitute the command output — so the orchestrator starts from concrete state instead of speculating about what's on disk.

**Read `.agents/manifest.json` first** — it is the canonical state index for all artifact metadata. A single read gives you status, staleness, producer, and a one-line summary for every relevant artifact; no per-path filesystem scanning required.

If the manifest is missing or you suspect drift (e.g., artifacts exist that aren't listed), refresh it:

```bash
bun ${SKILLS_ROOT:-.claude/skills}/meta-skills/scripts/manifest-sync.ts
```

**Status-aware lookup:** for each product-relevant artifact key — `architecture/system-architecture.md`, `.agents/skill-artifacts/meta/specs/*.md`, `.agents/skill-artifacts/meta/tasks.md`, `.agents/skill-artifacts/product/flow/*.md`, `.agents/skill-artifacts/meta/records/cleanup-*.md`, `.agents/skill-artifacts/meta/records/machine-cleanup-*.md`, and any `docs-writing` outputs — read the manifest entry's `status` and `stale` fields to qualify the state map:

| Manifest signal | State map value |
|---|---|
| `status: done`, `stale: false` | ✅ done |
| `status: done_with_concerns` | ⚠️ done-with-concerns — surface the concern in routing output |
| `status: blocked` or `needs_context` | treat as missing |
| `stale: true` | ✅ done (stale) — propose refresh as an option, don't block |
| `frontmatter_present: false` | ✅ done (legacy, no frontmatter) — quality unknown, suggest refresh |

Staleness is derived per-artifact via the manifest's `stale_after_days` (defaults vary per artifact type — see manifest spec). Read the manifest entry's `stale` field directly; do not apply a fixed-day threshold here.

**Experience block:** also read the manifest's `experience` block. The `entries` count for `technical.md`, `audience.md`, and `goals.md` indicates Pre-Dispatch coverage for product-stack questions — a domain with 0–1 entries likely needs a Cold Start; 5+ entries is well-covered.

See [`../../../meta-skills/references/manifest-spec.md`](../../../meta-skills/references/manifest-spec.md) for the full contract.

**Path reference / filesystem fallback** — used only when `.agents/manifest.json` doesn't exist (fresh project) or sync hasn't been run.

| Path | What it tells you |
|---|---|
| `research/product-context.md` | Cross-stack ICP/business context exists. |
| `.agents/skill-artifacts/meta/specs/*.md` | A scoped spec exists (from `discover`). |
| `.agents/skill-artifacts/product/flow/index.md` | At least 2 user flows mapped. |
| `.agents/skill-artifacts/product/flow/*.md` | Specific flows mapped (each file = one flow). |
| `architecture/system-architecture.md` | System blueprint exists. |
| `.agents/skill-artifacts/meta/tasks.md` | Buildable task list exists (from `task-breakdown`). |
| `.agents/skill-artifacts/meta/records/cleanup-*.md` | Code cleanup audit done. |
| `.agents/skill-artifacts/meta/records/machine-cleanup-*.md` | Machine cleanup audit done. |
| `.agents/experience/technical.md` | Cold-start tech context (platforms, OS versions, scale, deployment, codebase conventions) persisted. |
| `.agents/experience/product-workflow.md` | Prior breadcrumb. |

State map:

```
spec:              done | partial | missing
flows-mapped:      [list of flow names]
architecture:      done | partial | missing
tasks-broken-down: done | partial | missing
code-cleanup:      done | not run
machine-cleanup:   done | not run
docs:              [skim README, docs/, look for ship log in product-context.md]
```

---

## Step 2: Intention Analysis

| User says | Intent | Pipeline position |
|---|---|---|
| "design this feature", "user journey", "screen flow", "edge states", "platform touchpoints" | flow-mapping | user-flow |
| "tech stack", "database schema", "API design", "file structure", "deployment plan", "system design" | architecture | system-architecture |
| "decompose tasks", "task list", "what to build first", "implementation order" | task-decomposition | task-breakdown (meta-skills) |
| "README", "API docs", "runbook", "setup guide", "ship log", "document this" | documentation | docs-writing |
| "clean up code", "dead code", "refactor", "code audit", "remove unused" | code-cleanup | code-cleanup |
| "machine cleanup", "clean my mac", "free disk space", "remove caches", "dotfolder audit", "developer hygiene" | machine-cleanup | machine-cleanup |
| "scope this", "clarify requirements", "what should we build" | discovery | discover (meta-skills) |

**If empty or ambiguous**, ask:

> "What are you trying to do? Pick one or describe in your words:
>
> 1. Design a feature (user flows, screens, edge states)
> 2. Design the system (stack, schema, API)
> 3. Document something (README, API ref, runbook)
> 4. Clean up code (refactor, dead code, duplication)
> 5. Clean up developer machine (caches, dotfolders)
> 6. Decompose into tasks (already have spec/architecture)"

---

## Step 3: Routing Decision

Apply rules in order — first match wins.

**Foundation gates:**
1. **No spec or product-context AND intent is flow-mapping or architecture** → defer to `/discover` (from meta-skills) first to clarify scope. Note: not strict — user can override if they have clarity in conversation already.

**Pipeline routing:**
2. **flow-mapping** → propose `user-flow`. Note: produces one file per flow; can be invoked multiple times for different flows (checkout, onboarding, etc.).
3. **architecture** → propose `system-architecture`. Soft-gate: if no flows mapped, note "system-architecture works without flows but is sharper with them — flows define what screens/transitions exist; architecture defines how to build them."
4. **task-decomposition** → defer to `/task-breakdown` (meta-skills). Hard requires either spec.md or system-architecture.md.
5. **documentation** → propose `docs-writing`. Ask user which mode (README / API ref / runbook / ship log / setup guide).
6. **code-cleanup** → propose `code-cleanup`. Standalone — no upstream gate.
7. **machine-cleanup** → propose `machine-cleanup`. Standalone — no upstream gate.
8. **discovery** → defer to `/discover` (meta-skills).

**Combined intents** ("I want to design and build a feature"):
- Propose 2-step path: `/user-flow` → `/system-architecture`. Show both as the recommended sequence with rationale.

**Cross-stack pull-in:**
- If intent is architecture AND `.agents/skill-artifacts/meta/sketches/prioritize-*.md` exists, mention: "system-architecture can read `.agents/skill-artifacts/meta/sketches/prioritize-*.md` to align technical work with business priorities."

---

## Step 4: Present + Confirm

```
## Where you are

- Spec: ✅ done (.agents/skill-artifacts/meta/specs/*.md, last week)
- Flows mapped: 1 (checkout)
- Architecture: ❌ missing
- Tasks broken down: ❌ missing
- Code cleanup: not run
- Machine cleanup: not run

## What you asked

"I need to design how this feature is built" → architecture intent.

## Recommended next: system-architecture

Why: spec is done; checkout flow is mapped. system-architecture consumes
both and produces the technical blueprint (stack, schema, API, file
structure, deployment plan).

Cost: ~$1–3 · Duration: ~10 min · Produces: architecture/system-architecture.md

Note: only 1 flow is mapped. If your feature spans multiple flows
(onboarding, settings, etc.), consider running /user-flow on those
first — system-architecture is sharper with all flows in place.

Run it?  →  /system-architecture
```

If multiple options apply, show 2–3.

---

## Step 5: Persist + Hand Off

Append to `.agents/experience/product-workflow.md`:

```markdown
## Session 2026-05-06

- Read state: spec ✅, flows [checkout], architecture ❌, tasks ❌
- User intent: architecture
- Recommended: system-architecture
- User confirmed: yes
```

Print:

> Run `/system-architecture` next. After it completes, re-run `/orchestrate-product` to plan the next step (likely `/task-breakdown`).

Exit.

---

## Pipeline Reference

For canonical pipeline, decision rules, per-skill catalog, see [`./references/workflow-graph.md`](./references/workflow-graph.md).

---

## Anti-Patterns

- **Don't ignore the manifest** — always read `.agents/manifest.json` first; per-path filesystem scans are a fallback, not the default.
- **Don't conflate code-cleanup and machine-cleanup.** Code = source files; machine = dotfolders, caches, globals.
- **Don't recommend system-architecture without any flows or spec context.** It produces hollow blueprints.
- **Don't auto-invoke.** Always print `/skill-name`.
- **Don't recommend more than 3 skills.**
- **Don't recommend skills outside this stack except `discover` (meta) and `task-breakdown` (meta).** These two are intentional exceptions because they sit *inside* the product workflow, not adjacent to it: `discover` is the canonical upstream of any product build (clarifies WHAT before flow/architecture); `task-breakdown` is the canonical downstream after architecture (decomposes HOW into tasks before implementation). For all other meta-skills (`agents-panel`, `fresh-eyes`) and for cross-stack work, route through `/orchestrate-meta`.

---

## Output

- **Inline only.**
- **Side effect:** appends one entry to `.agents/experience/product-workflow.md`.

## Status

Ends with one of:
- `DONE` — recommendation given, hand-off printed.
- `BLOCKED` — couldn't read state.
- `NEEDS_CONTEXT` — empty ask + no state. Ask scoping question.
