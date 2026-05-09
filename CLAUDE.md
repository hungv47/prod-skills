# Product Skills

UX design, technical architecture, code cleanup, and documentation.

## Workflows
- user-flow → system-architecture → (execution) → fresh-eyes
- code-cleanup, docs-writing: standalone

## Artifacts
Skills write under `.agents/skill-artifacts/` by default; canonical records live in top-level folders:
- `.agents/skill-artifacts/product/flow/<flow-name>.md` — one file per flow (checkout.md, onboarding.md, etc.)
- `.agents/skill-artifacts/product/flow/index.md` — catalog, auto-generated when ≥2 flow files exist
- `architecture/system-architecture.md` — canonical system blueprint (top-level folder, co-locates schemas/ADRs/diagrams)
- `.agents/skill-artifacts/meta/records/cleanup-*.md`
- `docs-writing` writes directly to the project (README.md, docs/) or `research/product-context.md` (ship log mode)

## Cross-Stack (Optional)
system-architecture and docs-writing can read `research/product-context.md`.
Created by `icp-research` (market/audience context) or `docs-writing --ship-log` (product state context).
Install research-skills: `npx skills add hungv47/research-skills`

## Cross-Stack Connections
- `.agents/skill-artifacts/meta/sketches/prioritize-*.md` (from research-skills) → `system-architecture`: Business initiatives inform what to build
- `.agents/skill-artifacts/product/flow/<flow-name>.md` → `system-architecture`: User flows inform API design and feature decomposition. System-architecture consumes all flow files in the directory.

## Recommended Order
Run `user-flow` BEFORE `system-architecture`. User flows define WHAT screens and transitions exist; architecture defines HOW to build them.

## Pre-Dispatch Protocol

All 5 skills follow the canonical Pre-Dispatch protocol (`meta-skills/references/pre-dispatch-protocol.md`). Cold Start (3-5 bundled questions, one round-trip) when context is missing; Warm Start (summary + optional probe) when artifacts/experience cover what's needed. Most product-skill answers persist to `.agents/experience/technical.md` (supported platforms, min OS versions, scale targets, deployment context, codebase conventions, machine-cleanup excluded paths) — durable cross-skill state. `user-flow` has a mandatory platforms+surfaces gate inside Pre-Dispatch.

## Manifest Spec

State detection across all product skills (especially `orchestrate-product`) reads `.agents/manifest.json` — a derived index of artifact metadata (producer, date, status, schema version, staleness, summary). The manifest is rebuilt from artifact frontmatter by `meta-skills/scripts/manifest-sync.ts`; skills don't write to it directly. See [`../meta-skills/references/manifest-spec.md`](../meta-skills/references/manifest-spec.md) for the full contract. Skills that produce artifacts (system-architecture, user-flow, code-cleanup, machine-cleanup, docs-writing) must write the required frontmatter fields (`skill`, `version`, `date`, `status`) and call sync as their last step.

## Multi-Agent Skills

All 4 skills use a multi-agent orchestration pattern.

### Agent Inventory

| Skill | Agents | Layer 1 (parallel) | Layer 2 |
|-------|--------|-------------------|---------|
| user-flow | 6 | structure, edge-case | diagram + wireframe (2a parallel) → validation → critic |
| system-architecture | 7 | stack-selection, infrastructure | schema → api → integration → scaling → critic |
| code-cleanup | 8 | structural-scanner, code-scanner, dependency-scanner, asset-scanner | safe-removal → refactoring → validation → critic |
| docs-writing | 6 | scanner, concept-extractor, audience-profiler | writer → staleness-checker → critic |

### Key Constraints
- **code-cleanup enforces 5 golden rules**: preserve behavior, small steps, check conventions, test after each change, rollback awareness.
- **Reference files are shared resources**: agents receive reference file paths in their input contract. The orchestrator resolves relative paths to absolute paths before dispatch.
