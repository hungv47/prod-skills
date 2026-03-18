# Productivity Skills

Engineering and productivity skills — code cleanup, task planning, architecture, documentation.

## Installation

```bash
npx skills add hungv47/prod-skills
```

## Skills

| Skill | Description |
|-------|-------------|
| `plan-interviewer` | Multi-round interviews to surface requirements before implementation |
| `system-architecture` | Transform product documentation into comprehensive technical blueprints |
| `task-breakdown` | Break down implementation into granular, testable tasks |
| `code-cleanup` | Structural cleanup, code-level cleanup (AI slop removal), and refactoring |
| `technical-writer` | Generate clear product documentation and user guides from codebases |

## Workflows

```
plan-interviewer → task-breakdown or system-architecture
system-architecture ↔ task-breakdown
code-cleanup, technical-writer: standalone
```

## Cross-Stack DAG

```
strategy: problem-analysis → solution-design → funnel-planner → experiment
                                    ↓                  ↓
comms:    icp-research → imc-plan → content-create → attribution
               ↓              ↕ (reads solution-design, targets)
design:   brand-system → user-flow
                              ↓
prod:     plan-interviewer → system-architecture → task-breakdown
          code-cleanup (standalone)    technical-writer (standalone)
```

`system-architecture` can read `.agents/solution-design.md` (from strategy-skills) and `.agents/design/user-flow.md` (from design-skills) for cross-stack context.

Artifacts save to `.agents/`.

## Cross-Stack Workflow

`system-architecture` and `technical-writer` can read `.agents/product-context.md`, created by `icp-research` from [comms-skills](https://github.com/hungv47/comms-skills).

## Usage

- "Help me think through this" → `plan-interviewer`
- "Design system architecture" → `system-architecture`
- "Break down tasks" → `task-breakdown`
- "Clean up the codebase" → `code-cleanup`
- "Write documentation" → `technical-writer`
## License

MIT
