# Product Skills — Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning is [SemVer](https://semver.org/spec/v2.0.0.html) — major.minor.patch.

This file tracks stack-level releases. SKILL.md files describe current behavior; this file documents what changed and when.

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
