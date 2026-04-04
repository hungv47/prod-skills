# Product Skills

UX design, technical architecture, code cleanup, documentation, and shipping — the skills for designing and building software.

## Install

```bash
npx skills add hungv47/product-skills
```

## Pipeline

<picture>
  <img src="./assets/pipeline.svg" alt="Product pipeline: user-flow → system-architecture → ship → deploy-verify, plus horizontal code-cleanup and technical-writer" width="100%">
</picture>

## Skills

### `user-flow` — map the screens

Maps multi-step in-product flows — screens, decisions, transitions, edge cases, and error states for features or user journeys.

**Use when:**
- You're designing a new feature and need to think through every screen and user path
- You want to catch edge cases (errors, empty states, permissions) before building
- You need a visual reference that developers can implement from

**Not for:** visual brand design (use `brand-system`) or single-page conversion (use `lp-optimization`)

**Produces:** `.agents/design/user-flow.md`

---

### `system-architecture` — design the technical system

Technical blueprints — tech stack selection, database schema, API design, file structure, and deployment plan.

**Use when:**
- You know what to build and need to decide *how* — the technical design
- You want a database schema, API contracts, and deployment plan before writing code
- You need to evaluate tech stack trade-offs for a specific product

**Not for:** unclear requirements (use `discover`) or task decomposition (use `task-breakdown`)

**Produces:** `.agents/system-architecture.md`

---

### `code-cleanup` — audit and refactor existing code

Structural audit, AI slop removal, dead code detection, and refactoring — without changing behavior.

**Use when:**
- Your codebase has accumulated cruft and needs a quality pass
- You want to remove AI-generated patterns that hurt readability
- You need to identify dead code, unused dependencies, or structural issues

**Not for:** diagnosing business problems (use `problem-analysis`) or writing documentation (use `technical-writer`)

**Produces:** `.agents/cleanup-report.md` + in-place fixes

---

### `technical-writer` — generate documentation from code

READMEs, API references, setup guides, runbooks, and architecture docs with consistent structure and terminology.

**Use when:**
- You have a codebase and need documentation generated from it
- You want API references, setup guides, or runbooks that stay accurate to the code
- You need contributor documentation for an open-source project

**Not for:** specifying what to build (use `discover`) or restructuring code (use `code-cleanup`)

**Produces:** Documentation files directly in the project (README.md, docs/)

---

### `ship` — automated pre-merge pipeline

Runs tests, checks the review gate, organizes commits, and creates a PR with a structured body.

**Use when:**
- You've built and reviewed something and need to ship it cleanly
- You want an automated pipeline from tests through PR creation
- You need commits organized and a well-structured PR body

**Not for:** code review (use `review-chain`) or task decomposition (use `task-breakdown`)

**Produces:** `.agents/ship-report.md` + a pull request on the remote

---

### `deploy-verify` — post-deploy health check

Verifies a production URL is healthy after shipping — page load, console errors, critical paths, response times.

**Use when:**
- You just deployed and want to verify production is healthy
- You need evidence-backed health status (HEALTHY / DEGRADED / BROKEN)
- You want a baseline comparison against prior deploys

**Not for:** pre-merge review (use `review-chain`) or shipping (use `ship`)

**Produces:** `.agents/deploy-verify-report.md`, `.agents/deploy-verify-baseline.json`

---

## Cross-Stack

- `system-architecture` reads `.agents/solution-design.md` (from [research-skills](https://github.com/hungv47/research-skills)) and `.agents/design/user-flow.md` for cross-stack context
- `system-architecture` and `technical-writer` read `.agents/product-context.md` from research-skills
- `user-flow` output feeds into `system-architecture` and `task-breakdown` (from [meta-skills](https://github.com/hungv47/meta-skills))

## License

MIT
