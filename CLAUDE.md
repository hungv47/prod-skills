# Product Skills

UX design, technical architecture, code cleanup, documentation, and shipping.

## Workflows
- user-flow → system-architecture → (execution) → review-chain → ship
- code-cleanup, technical-writer: standalone

## Artifacts
Skills write to `.agents/`:
- `.agents/product/flow/<flow-name>.md` — one file per flow (checkout.md, onboarding.md, etc.)
- `.agents/product/flow/index.md` — catalog, auto-generated when ≥2 flow files exist
- `.agents/system-architecture.md`
- `.agents/cleanup-report.md`
- `.agents/ship-report.md`
- `.agents/deploy-verify-report.md` + `.agents/deploy-verify-baseline.json`
- `technical-writer` writes directly to the project (README.md, docs/) or `.agents/product-context.md` (ship log mode)

## Cross-Stack (Optional)
system-architecture and technical-writer can read `.agents/product-context.md`.
Created by `icp-research` (market/audience context) or `technical-writer --ship-log` (product state context).
Install research-skills: `npx skills add hungv47/research-skills`

## Cross-Stack Connections
- `.agents/solution-design.md` (from research-skills) → `system-architecture`: Business initiatives inform what to build
- `.agents/product/flow/<flow-name>.md` → `system-architecture`: User flows inform API design and feature decomposition. System-architecture consumes all flow files in the directory.

## Recommended Order
Run `user-flow` BEFORE `system-architecture`. User flows define WHAT screens and transitions exist; architecture defines HOW to build them.

## Multi-Agent Skills

5 of 6 skills use a multi-agent orchestration pattern (`deploy-verify` is single-agent):

### Agent Inventory

| Skill | Agents | Layer 1 (parallel) | Layer 2 |
|-------|--------|-------------------|---------|
| user-flow | 6 | structure, edge-case | diagram + wireframe (2a parallel) → validation → critic |
| system-architecture | 7 | stack-selection, infrastructure | schema → api → integration → scaling → critic |
| code-cleanup | 8 | structural-scanner, code-scanner, dependency-scanner, asset-scanner | safe-removal → refactoring → validation → critic |
| technical-writer | 6 | scanner, concept-extractor, audience-profiler | writer → staleness-checker → critic |
| ship | 4 | test-runner (gate) | commit-organizer → pr-writer → critic |
| deploy-verify | 0 | — | — (single-agent methodology) |

### Key Constraints
- **code-cleanup enforces 5 golden rules**: preserve behavior, small steps, check conventions, test after each change, rollback awareness.
- **Reference files are shared resources**: agents receive reference file paths in their input contract. The orchestrator resolves relative paths to absolute paths before dispatch.
