# Productivity Skills

Engineering productivity, process quality, and workflow orchestration — code cleanup, task planning, architecture, documentation, multi-perspective analysis, and post-implementation review.

## Installation

```bash
npx skills add hungv47/product-skills
```

## Skills

| Skill | Description |
|-------|-------------|
| `plan-interviewer` | Multi-round interviews to surface requirements before implementation |
| `system-architecture` | Technical blueprints — tech stack, database schema, API design, file structure, deployment plan |
| `task-breakdown` | Break down implementation into granular, testable tasks with acceptance criteria |
| `code-cleanup` | Structural cleanup, code-level cleanup (AI slop removal), and refactoring |
| `technical-writer` | Generate clear product documentation and user guides from codebases |
| `skill-router` | Analyze a goal → suggest the right skill team → orchestrate multi-phase workflows (includes artifact scanning via `status` mode) |
| `multi-lens` | Multi-agent debate (agents argue in rounds) or consensus polling (agents analyze independently) for decisions |
| `review-chain` | Fresh-eyes review chain — implement → review → resolve, max 2 rounds |

## Workflows

```
plan-interviewer → task-breakdown or system-architecture
system-architecture ↔ task-breakdown
code-cleanup, technical-writer: standalone
skill-router: goal analysis → skill team suggestion → orchestration (includes artifact scanning via `status` mode)
multi-lens: multi-agent debate or consensus polling (domain-agnostic, composes with any skill)
review-chain: fresh-eyes review → resolve chain (domain-agnostic, composes with any skill)
```

## Cross-Stack DAG

```
strategy: problem-analysis → solution-design → funnel-planner → experiment
                                    ↓                  ↓
comms:    icp-research → imc-plan → content-create → attribution
               ↓              ↕ (reads solution-design, targets)
design:   brand-system → user-flow
                              ↓
prod:     plan-interviewer → system-architecture ↔ task-breakdown
          code-cleanup, technical-writer, skill-router (standalone)
          multi-lens, review-chain (horizontal — compose with any skill)
```

`system-architecture` can read `.agents/solution-design.md` (from research-skills) and `.agents/design/user-flow.md` (from product-skills) for cross-stack context.

Artifacts save to `.agents/`.

## Cross-Stack Workflow

`system-architecture` and `technical-writer` can read `.agents/product-context.md`, created by `icp-research` from [marketing-skills](https://github.com/hungv47/marketing-skills).

## Usage

- "Help me think through this" → `plan-interviewer`
- "Design system architecture" → `system-architecture`
- "Break down tasks" → `task-breakdown`
- "Clean up the codebase" → `code-cleanup`
- "Write documentation" → `technical-writer`
- "What artifacts do I have?" → `skill-router status`
- "What skill should I run?" → `skill-router`
- "Debate this decision" → `multi-lens` (debate mode)
- "Get consensus from multiple perspectives" → `multi-lens` (poll mode)
- "Verify this code/output" → `review-chain`

## License

MIT
