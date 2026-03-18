# Productivity Skills

Engineering productivity: code cleanup, architecture, task breakdown, documentation, planning.

## Workflows
- plan-interviewer → task-breakdown or system-architecture
- system-architecture ↔ task-breakdown
- code-cleanup, technical-writer: standalone

## Artifacts
Skills write to `.agents/`:
- `.agents/cleanup-report.md`
- `.agents/system-architecture.md`
- `.agents/tasks.md`
- `.agents/spec.md`

## Cross-Stack (Optional)
system-architecture and technical-writer can read `.agents/product-context.md`.
Created by `icp-research`: `npx skills add hungv47/comms-skills`

## Recommended Order
Run `system-architecture` BEFORE `task-breakdown`. Architecture defines WHAT to build; tasks define HOW to build it. Running task-breakdown before architecture produces tasks without structural context.

## Cross-Stack Connections
- `solution-design.md` (from strategy-skills) → `system-architecture`: Business initiatives inform what to build
- `user-flow.md` (from design-skills) → `system-architecture` and `task-breakdown`: User flows inform API design and feature decomposition