# Product Skills

UX design, technical architecture, code cleanup, and documentation — the skills for designing and building software.

## Installation

```bash
npx skills add hungv47/product-skills
```

## Skills

| Skill | Description |
|-------|-------------|
| `user-flow` | Map screens, decisions, transitions, edge cases, and error states |
| `system-architecture` | Technical blueprints — tech stack, database schema, API design, file structure, deployment plan |
| `code-cleanup` | Structural cleanup, AI slop removal, refactoring |
| `technical-writer` | Generate clear product documentation and user guides from codebases |

## Workflows

```
user-flow → system-architecture → (execution)
code-cleanup, technical-writer: standalone
```

## Cross-Stack DAG

```
research:   icp-research → product-context.md
            market-research + problem-analysis → solution-design

marketing:  brand-system, imc-plan → content-create → attribution

product:    user-flow → system-architecture → (execution)
            code-cleanup, technical-writer (horizontal)

meta:       preflight → plan-interviewer → task-breakdown (before builds)
            multi-lens (decisions), review-chain (verification)
```

`system-architecture` can read `.agents/solution-design.md` (from research-skills) and `.agents/design/user-flow.md` for cross-stack context.

Artifacts save to `.agents/`.

## Cross-Stack Workflow

`system-architecture` and `technical-writer` can read `.agents/product-context.md`, created by `icp-research` from [research-skills](https://github.com/hungv47/research-skills).

## Usage

- "Map user flows" → `user-flow`
- "Design system architecture" → `system-architecture`
- "Clean up the codebase" → `code-cleanup`
- "Write documentation" → `technical-writer`

## License

MIT
