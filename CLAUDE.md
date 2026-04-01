# Productivity Skills

Engineering productivity, process quality, and workflow orchestration: code cleanup, architecture, task breakdown, documentation, planning, skill routing, multi-perspective analysis, and post-implementation review.

## Workflows
- plan-interviewer → task-breakdown or system-architecture
- system-architecture ↔ task-breakdown
- code-cleanup, technical-writer: standalone
- skill-router: goal analysis → skill team suggestion → multi-phase workflow orchestration (includes artifact scanning via `status` mode)
- multi-lens: multi-agent debate or consensus polling for decisions (domain-agnostic, composes with any skill)
- review-chain: fresh-eyes review → resolve chain for post-implementation quality (domain-agnostic, composes with any skill)

## Artifacts
Skills write to `.agents/`:
- `.agents/cleanup-report.md`
- `.agents/system-architecture.md`
- `.agents/tasks.md`
- `.agents/spec.md`
- `.agents/workflow-plan.md` (skill-router orchestrate mode)
- `.agents/meta/multi-lens-report.md` (+ `multi-lens-transcript.json` for debate mode)
- `.agents/meta/review-chain-report.md`

Meta-artifacts in `.agents/meta/` are ephemeral — overwritten on each run.

## Cross-Stack (Optional)
system-architecture and technical-writer can read `.agents/product-context.md`.
Created by `icp-research`: `npx skills add hungv47/comms-skills`

## Recommended Order
Run `system-architecture` BEFORE `task-breakdown`. Architecture defines WHAT to build; tasks define HOW to build it. Running task-breakdown before architecture produces tasks without structural context.

## Cross-Stack Connections
- `.agents/solution-design.md` (from strategy-skills) → `system-architecture`: Business initiatives inform what to build
- `.agents/design/user-flow.md` (from design-skills) → `system-architecture` and `task-breakdown`: User flows inform API design and feature decomposition

## Multi-Agent Skills

### Static Two-Layer Pattern (6 skills)

The following multi-agent skills use orchestration with a shared pattern:
- **Layer 1 agents** run in parallel (scanners, extractors, profilers)
- **Layer 2 agents** run sequentially (each depends on prior output)
- **Critic agent** reviews the final output against a quality gate
- **Single-agent fallback** available for simple tasks or constrained contexts

### Agent Inventory

| Skill | Agents | Layer 1 (parallel) | Layer 2 (sequential) |
|-------|--------|-------------------|---------------------|
| system-architecture | 7 | stack-selection, infrastructure | schema → api → integration → scaling → critic |
| task-breakdown | 5 | decomposer, dependency-mapper | ordering → acceptance → critic |
| plan-interviewer | 7 | codebase-scanner, artifact-reader | challenger → interviewer → synthesis → critic (Route A/B); scope-contract (Route C) |
| code-cleanup | 7 | structural-scanner, code-scanner, dependency-scanner | safe-removal → refactoring → validation → critic |
| technical-writer | 6 | scanner, concept-extractor, audience-profiler | writer → staleness-checker → critic |
| skill-router | 3 | intent-classifier, artifact-scanner | team-composer (no critic — advisory only) |

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

### Dynamic Spawning Pattern (2 skills)

`multi-lens` and `review-chain` use a different pattern: agent count, roles, and instructions are defined at **runtime** based on the problem. There is no `agents/` directory — prompts are inline templates in SKILL.md.

- **multi-lens:** Spawns N agents (debate mode: argue in rounds; poll mode: independent analysis with varied framings). Agent roles/count/instructions defined per-invocation.
- **review-chain:** Spawns a reviewer agent (fresh eyes, no access to implementation reasoning) then a resolver agent if issues found. Max 2 verification loops.

These are domain-agnostic process wrappers — they compose with any skill in any stack:
- `multi-lens` for architecture decisions, strategic choices, or design trade-offs
- `review-chain` after `system-architecture`, `code-cleanup`, or any critical artifact

### Key Constraints
- **plan-interviewer is interactive**: the interviewer-agent uses AskUserQuestion tool for multi-round interviews. The orchestrator must relay questions to the user.
- **task-breakdown preserves Phase 2**: the execution protocol (per-task protocol, coding rules, scope change protocol) runs after decomposition and is NOT agent-orchestrated.
- **code-cleanup enforces 5 golden rules**: preserve behavior, small steps, check conventions, test after each change, rollback awareness. These are the Critical Gates.
- **Reference files are shared resources**: agents receive reference file paths in their input contract. The orchestrator resolves relative paths to absolute paths before dispatch.
