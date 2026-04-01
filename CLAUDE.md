# Product Skills

UX design, technical architecture, code cleanup, and documentation.

## Workflows
- user-flow → system-architecture → (execution)
- code-cleanup, technical-writer: standalone

## Artifacts
Skills write to `.agents/`:
- `.agents/design/user-flow.md`
- `.agents/system-architecture.md`
- `.agents/cleanup-report.md`
- `technical-writer` writes directly to the project (README.md, docs/)

## Cross-Stack (Optional)
system-architecture and technical-writer can read `.agents/product-context.md`.
Created by `icp-research`: `npx skills add hungv47/research-skills`

## Cross-Stack Connections
- `.agents/solution-design.md` (from research-skills) → `system-architecture`: Business initiatives inform what to build
- `.agents/design/user-flow.md` → `system-architecture`: User flows inform API design and feature decomposition

## Recommended Order
Run `user-flow` BEFORE `system-architecture`. User flows define WHAT screens and transitions exist; architecture defines HOW to build them.

## Multi-Agent Skills

All 4 skills use a two-layer multi-agent orchestration pattern:

### Agent Inventory

| Skill | Agents | Layer 1 (parallel) | Layer 2 (sequential) |
|-------|--------|-------------------|---------------------|
| user-flow | 5 | structure, edge-case | diagram → validation → critic |
| system-architecture | 7 | stack-selection, infrastructure | schema → api → integration → scaling → critic |
| code-cleanup | 7 | structural-scanner, code-scanner, dependency-scanner | safe-removal → refactoring → validation → critic |
| technical-writer | 6 | scanner, concept-extractor, audience-profiler | writer → staleness-checker → critic |

### Key Constraints
- **code-cleanup enforces 5 golden rules**: preserve behavior, small steps, check conventions, test after each change, rollback awareness.
- **Reference files are shared resources**: agents receive reference file paths in their input contract. The orchestrator resolves relative paths to absolute paths before dispatch.
