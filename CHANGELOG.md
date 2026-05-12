# Product Skills — Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning is [SemVer](https://semver.org/spec/v2.0.0.html) — major.minor.patch.

This file tracks stack-level releases. SKILL.md files describe current behavior; this file documents what changed and when.

---

## [5.0.1] - 2026-05-12

Coordinated cross-stack cleanup of cross-references to `lp-optimization`, which was hard-removed in marketing-skills 6.0.0.

### Changed
- `skills/user-flow/SKILL.md` description and `README.md` — replaced "single-page conversion (use lp-optimization)" with "landing-page architecture (use lp-brief)". The user-flow Not-for paragraph now points at the surviving skill that owns landing-page work; the prior pointer would have been broken after marketing-skills 6.0.0.

No skill behavior changed; description-text and doc-cleanup only.

## [5.0.0] - 2026-05-12

Stack-major cut coordinated across the 4-stack marketplace to mark the post-tier-discipline stable era. The stack-orchestrator declares itself fast-tier. `docs-writing` gains a new Route E for release-notes generation. Major bump signals the alignment + the new mode.

### Added
- `docs-writing` Route E (`--release-notes <version>`) — generates a CHANGELOG entry conforming to the agent-skills CHANGELOG convention defined in `RELEASING.md`. Convention-enforcing critic fails outputs with file inventories, fresh-eyes recaps, or anti-goals lists. Optional `--gh-release` flag emits a GitHub Release body draft.

### Changed
- `orchestrate-product` budget reclassified standard → fast; body declares it is a pure router (no agent dispatch, no critic gate).
- `docs-writing` skill internally bumped 3.1.0 → 3.2.0 (new mode); stack-level major masks the skill-internal minor.

Full review: `.agents/skill-artifacts/meta/records/2026-05-12-fresh-eyes-tier-discipline-phase-ab.md`

---

## [3.0.1] - 2026-05-11

`orchestrate-product` Step 1 starts from concrete disk state instead of asking the model to derive it. When you run `/orchestrate-product`, the skill now sees the actual artifact counts by domain, which top-level canonical folders exist (`research/`, `brand/`, `architecture/`), and the last 5 commits — all rendered inline before the manifest read kicks in.

### Changed
- **`skills/orchestrate-product/SKILL.md` §Step 1** — disk-snapshot block lifted from `orchestrate-meta`. Three `! \`<cmd>\`` interpolations (artifact-count-by-domain / canonical-folder check / git-log -5) substitute their output at slash-command invocation time, before the manifest read. The orchestrator starts from a deterministic snapshot instead of speculating about what's on disk.

### Notes
- Additive context. No behavioral change to routing, recommendations, or output schema. Existing invocations work unchanged.
- The block only renders when the skill is invoked as a slash command. If `SKILL.md` is read via the Read tool inside another skill, the bang-backtick lines pass through as literal syntax — by design.

---

## [3.0.0] - 2026-05-08

### BREAKING
- Renamed `start-product` → `orchestrate-product`. The skill scans existing artifacts and continues mid-pipeline; the orchestration role now reads explicitly in the slash command. No backward-compat alias — single-rev cutover.
- Update any `/start-product` invocations in your workflows to `/orchestrate-product`.

---

## [2.2.2] - 2026-05-08

CLAUDE.md doc cleanup — align stack-level documentation with the new `.agents/skill-artifacts/` taxonomy shipped in v2.2.1 and across the umbrella as marketplace 1.5.0.

### Changed

- `product-skills/CLAUDE.md` Artifacts and Cross-Stack Connections sections — every `.agents/product/...`, `.agents/cleanup-report.md`, `.agents/prioritize.md` reference migrated to the new taxonomy:
  - `.agents/product/flow/...` → `.agents/skill-artifacts/product/flow/...`
  - `.agents/cleanup-report.md` → `.agents/skill-artifacts/meta/records/cleanup-*.md`
  - `.agents/prioritize.md` → `.agents/skill-artifacts/meta/sketches/prioritize-*.md`
- "Skills write to `.agents/` by default" → "Skills write under `.agents/skill-artifacts/` by default."

### Notes

Doc-only patch — no SKILL.md or skill-behavior changes.

---

## [2.2.1] - 2026-05-08

T33 path migration — every skill SKILL.md updated to the new `.agents/skill-artifacts/` lifecycle taxonomy (see `agent-skills/CLAUDE.md` §"Artifact Placement"). Mechanical churn only — no behavior changes.

### Changed

- All 6 SKILL.md files (`code-cleanup`, `docs-writing`, `machine-cleanup`, `start-product`, `system-architecture`, `user-flow`) — frontmatter `description`, `routing.produces`, `routing.consumes`, and inline body references updated:
  - `.agents/cleanup-report.md` → `.agents/skill-artifacts/meta/records/cleanup-*.md`
  - `.agents/machine-cleanup-report.md` → `.agents/skill-artifacts/meta/records/machine-cleanup-*.md`
  - `.agents/product/flow/...` → `.agents/skill-artifacts/product/flow/...`
  - `.agents/spec.md`, `.agents/tasks.md`, `.agents/prioritize.md` → `.agents/skill-artifacts/meta/{specs,tasks.md,sketches/prioritize-*.md}` (consumer refs in start-product, system-architecture, etc.)
  - Top-level `architecture/system-architecture.md` and `research/product-context.md` paths unchanged (canonical).
- All 6 SKILL.md files declare `routing.lifecycle:` — `canonical` (system-architecture, docs-writing — produce top-level project records), `pipeline` (user-flow, start-product orchestrator), `snapshot` (code-cleanup, machine-cleanup).

### Notes

Non-behavioral release. No skill output changed format. Manifest reconciles automatically.

---

## [2.2.0] - 2026-05-07

Manifest-aware state detection in `start-product`.

### Changed

- `start-product` SKILL.md — Step 1 (State Detection) now reads `.agents/manifest.json` first with a status-aware lookup table (`done`, `done_with_concerns`, `blocked`/`needs_context`, `stale`, `frontmatter_present: false`). Per-artifact staleness flows from the manifest's `stale_after_days` field rather than the previous flow-vs-architecture mtime check or 60-day spec rule. The manifest's `experience` block surfaces Pre-Dispatch coverage (entries count for `technical.md`, `audience.md`, `goals.md`). Per-path filesystem scan demoted to fallback for fresh projects. Anti-pattern entry added: "Don't ignore the manifest." Added `side-effects: [manifest-sync]` to the skill's routing block.
- `CLAUDE.md` — added "Manifest Spec" section pointing producer skills (system-architecture, user-flow, code-cleanup, machine-cleanup, docs-writing) at the canonical contract in `meta-skills/references/manifest-spec.md` and the frontmatter obligations.

### Notes

This release lands the manifest-spec contract on the consumer side. Per-skill frontmatter retrofit (system-architecture, user-flow, etc.) follows in a later release — the spec's graceful fallback (`frontmatter_present: false`) keeps existing artifacts working until producers are migrated.

---

## [2.1.0] - 2026-05-06

Stack orchestrator added; declaration drift fixed.

### Added

- `start-product` — Stack orchestrator. Reads `.agents/product/`, `architecture/`, `.agents/spec.md`, `.agents/tasks.md`, and `.agents/experience/*.md`, parses the user's free-form ask (or asks one bundled scoping question if empty), and proposes the next 1–3 skills in the product pipeline (`user-flow` → `system-architecture` → `docs-writing`, with `code-cleanup` and `machine-cleanup` as standalone branches) with rationale + cost + duration. Knows two intentional cross-stack exceptions: `discover` (canonical upstream of any product build) and `task-breakdown` (canonical decomposition step between architecture and implementation) — these are referenced directly because they sit *inside* the product workflow rather than adjacent to it. All other meta-skills route via `/start-meta`. Never auto-invokes — always prints the `/skill-name` for the user to type. Persists a breadcrumb to `.agents/experience/product-workflow.md`. Standard budget, ~$0.10–0.30 per run. Pipeline catalog lives in `references/workflow-graph.md`.

### Fixed

- `machine-cleanup` was present on disk since v2.0.0 but missing from `.claude-plugin/plugin.json` `skills[]` — declaration restored. Skill now installs correctly via the Claude Code plugin marketplace path.

### Changed

- Plugin `keywords` extended with `machine-cleanup` to surface the developer-machine-hygiene capability in marketplace search.

---

## [1.0.0] - 2026-05-05

Initial public release. UX design, technical architecture, code cleanup, machine cleanup, and documentation generation.

### Added

**Skills (5)**

- `user-flow` — Maps a feature into structure, edge cases, platform-native wireframes per declared platform. **Mandatory platforms+surfaces gate** — no Layer 1 dispatch until target platforms (from canonical 13-platform catalog) and per-platform surfaces are explicit. "Cross-platform" rejected. Produces `.agents/product/flow/<flow-name>.md` + auto-generated `index.md` when ≥2 flows exist. 6 agents (structure, edge-case, diagram, wireframe, validation, critic).
- `system-architecture` — Transforms product specs into a comprehensive technical blueprint covering stack selection, schema, API design, infrastructure, scaling, and security review (STRIDE + OWASP + LLM security). Produces `architecture/system-architecture.md`. 7 agents (stack-selection + infrastructure parallel; schema → api → integration → scaling → critic sequential).
- `code-cleanup` — Multi-mode cleanup: dead code, unused dependencies, asset cleanup, refactoring. Enforces 5 golden rules (preserve behavior, small steps, check conventions, test after each change, rollback awareness). Produces `.agents/cleanup-report.md`. 8 agents (4 parallel scanners → safe-removal → refactoring → validation → critic).
- `machine-cleanup` — Audits dotfolders, caches, package globals, and toolchains; removes abandoned state without breaking active workflows. Produces `.agents/machine-cleanup-report.md`. Conservative / moderate / aggressive modes.
- `docs-writing` — Audience-aware documentation generation (READMEs, user guides, API references, config guides, tutorials, ship logs). Produces docs to project root or `docs/`. Ship-log mode writes `research/product-context.md` (cross-stack record). 6 agents (parallel scanner + concept-extractor + audience-profiler → writer → staleness-checker → critic).

**Workflows**

- Standard build: `user-flow` → `system-architecture` → (execution) → `fresh-eyes` (from meta-skills)
- `code-cleanup`, `docs-writing`, `machine-cleanup` are horizontal — invokable independently

**Architectural patterns**

- **Pre-Dispatch protocol** — every skill follows the canonical spec at `meta-skills/references/pre-dispatch-protocol.md`. Cold Start / Warm Start flows; answers persist to `.agents/experience/technical.md` (durable cross-skill state: supported platforms, min OS versions, scale targets, deployment context, codebase conventions, machine-cleanup excluded paths).
- **Status protocol** — every skill emits `DONE / DONE_WITH_CONCERNS / BLOCKED / NEEDS_CONTEXT` with skill-specific exit conditions; artifact frontmatter mirrors.
- **Multi-agent orchestration** — Layer 1 (parallel) → Layer 2 (sequential) → Critic gate (PASS/FAIL with max 2 rewrite cycles).

**Cross-stack**

- `system-architecture` consumes `.agents/prioritize.md` (research-skills) — business initiatives inform technical design.
- `system-architecture` consumes all `.agents/product/flow/*.md` files — user flows inform API design and feature decomposition.
- `docs-writing` reads `research/product-context.md` for product context; ship-log mode writes back to it.
