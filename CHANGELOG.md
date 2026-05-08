# Product Skills — Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning is [SemVer](https://semver.org/spec/v2.0.0.html) — major.minor.patch.

This file tracks stack-level releases. SKILL.md files describe current behavior; this file documents what changed and when.

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
