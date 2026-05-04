# Product Skills

UX design, technical architecture, code cleanup, and documentation.

## Workflows
- user-flow → system-architecture → (execution) → fresh-eyes
- code-cleanup, docs-writing: standalone

## Artifacts
Skills write to `.agents/` by default; canonical records live in top-level folders:
- `.agents/product/flow/<flow-name>.md` — one file per flow (checkout.md, onboarding.md, etc.)
- `.agents/product/flow/index.md` — catalog, auto-generated when ≥2 flow files exist
- `architecture/system-architecture.md` — canonical system blueprint (top-level folder, co-locates schemas/ADRs/diagrams)
- `.agents/cleanup-report.md`
- `docs-writing` writes directly to the project (README.md, docs/) or `research/product-context.md` (ship log mode)

## Cross-Stack (Optional)
system-architecture and docs-writing can read `research/product-context.md`.
Created by `icp-research` (market/audience context) or `docs-writing --ship-log` (product state context).
Install research-skills: `npx skills add hungv47/research-skills`

## Cross-Stack Connections
- `.agents/prioritize.md` (from research-skills) → `system-architecture`: Business initiatives inform what to build
- `.agents/product/flow/<flow-name>.md` → `system-architecture`: User flows inform API design and feature decomposition. System-architecture consumes all flow files in the directory.

## Recommended Order
Run `user-flow` BEFORE `system-architecture`. User flows define WHAT screens and transitions exist; architecture defines HOW to build them.

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
