# Productivity Skills

Engineering productivity: code cleanup, architecture, task breakdown, documentation, planning.

## Workflows
- plan-interviewer → task-breakdown or system-architecture
- system-architecture ↔ task-breakdown
- code-cleanup, technical-writer: standalone
- artifact-status: cross-stack artifact scanner (run anytime to see what exists/what's stale)

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
- `.agents/solution-design.md` (from strategy-skills) → `system-architecture`: Business initiatives inform what to build
- `.agents/design/user-flow.md` (from design-skills) → `system-architecture` and `task-breakdown`: User flows inform API design and feature decomposition

## Multi-Agent Skills

All 5 skills use multi-agent orchestration with a shared pattern:
- **Layer 1 agents** run in parallel (scanners, extractors, profilers)
- **Layer 2 agents** run sequentially (each depends on prior output)
- **Critic agent** reviews the final output against a quality gate
- **Single-agent fallback** available for simple tasks or constrained contexts

### Agent Inventory

| Skill | Agents | Layer 1 (parallel) | Layer 2 (sequential) |
|-------|--------|-------------------|---------------------|
| system-architecture | 7 | stack-selection, infrastructure | schema → api → integration → scaling → critic |
| task-breakdown | 5 | decomposer, dependency-mapper | ordering → acceptance → critic |
| plan-interviewer | 6 | codebase-scanner, artifact-reader | challenger → interviewer → synthesis → critic |
| code-cleanup | 7 | structural-scanner, code-scanner, dependency-scanner | safe-removal → refactoring → validation → critic |
| technical-writer | 6 | scanner, concept-extractor, audience-profiler | writer → staleness-checker → critic |

### Orchestrator Responsibilities
1. **Dispatch** — route to correct agents based on user intent and routing rules
2. **Assemble** — merge agent outputs into the final artifact
3. **Gate** — enforce Critical Gates via the critic agent before delivery
4. **Revise** — re-dispatch specific agents when critic returns FAIL (max 2 rounds)
5. **Fallback** — use single-agent mode when multi-agent is overkill

### Agent File Convention
Agent definitions live in `[skill-name]/agents/[agent-name].md`. Each follows the template structure:
- Role (what it does, what it does NOT do)
- Input Contract (what it receives from the orchestrator)
- Output Contract (what it returns)
- Domain Instructions (craft knowledge, techniques, examples)
- Self-Check (quality criteria before returning)

### Key Constraints
- **plan-interviewer is interactive**: the interviewer-agent uses AskUserQuestion tool for multi-round interviews. The orchestrator must relay questions to the user.
- **task-breakdown preserves Phase 2**: the execution protocol (per-task protocol, coding rules, scope change protocol) runs after decomposition and is NOT agent-orchestrated.
- **code-cleanup enforces 5 golden rules**: preserve behavior, small steps, check conventions, test after each change, rollback awareness. These are the Critical Gates.
- **Reference files are shared resources**: agents receive reference file paths in their input contract. The orchestrator resolves relative paths to absolute paths before dispatch.
