---
name: technical-writer
description: "Generates documentation from a codebase — READMEs, API references, setup guides, runbooks, and architecture docs with consistent structure and terminology. Produces documentation files in the project. Not for specifying what to build (use plan-interviewer) or restructuring code (use code-cleanup)."
argument-hint: "[codebase or project to document]"
license: MIT
metadata:
  author: hungv47
  version: "3.0.0"
routing:
  intent-tags:
    - documentation
    - readme
    - api-reference
    - setup-guide
    - runbook
  position: horizontal
  produces: []
  consumes:
    - product-context.md
  requires: []
  defers-to:
    - skill: plan-interviewer
      when: "need a spec for what to build, not docs for what exists"
    - skill: code-cleanup
      when: "need code quality improvements, not documentation"
  parallel-with:
    - code-cleanup
  interactive: false
  estimated-complexity: medium
---

# Technical Writer — Orchestrator

*Productivity — Multi-agent orchestration. Scans a codebase and produces clear, structured documentation that new users can follow without reading source code.*

**Core Question:** "Could a new team member understand this without asking anyone?"

## Inputs Required
- A codebase or project to document
- (Optional) Target audience — developer, end-user, operator, or mixed
- (Optional) Documentation type — README, User Guide, API Reference, or Configuration Guide

## Output
- Documentation artifact saved to project root or specified location (e.g., `docs/`, `README.md`)

## Chain Position
Previous: none | Next: none (standalone)

Pairs well with: `system-architecture` (for architecture docs), `task-breakdown` (for contributor guides)

**Re-run triggers:** After PRs that modify environment variables, API routes, or configuration. After major version releases. When new features ship without documentation updates.

---

## Multi-Agent Architecture

### Agent Roster

| Agent | File | Focus |
|-------|------|-------|
| scanner-agent | `agents/scanner-agent.md` | Maps project structure, file importance ranking, existing docs inventory |
| concept-extractor-agent | `agents/concept-extractor-agent.md` | Reads key files, extracts features, setup requirements, error patterns |
| audience-profiler-agent | `agents/audience-profiler-agent.md` | Identifies audience, calibrates vocabulary and depth |
| writer-agent | `agents/writer-agent.md` | Writes the documentation from extracted concepts for the profiled audience |
| staleness-checker-agent | `agents/staleness-checker-agent.md` | Compares documentation against current codebase for accuracy |
| critic-agent | `agents/critic-agent.md` | Quality gate review, audience calibration check, staleness integration |

### Execution Layers

```
Layer 1 (parallel):
  scanner-agent ──────────────┐
  concept-extractor-agent ────┤── run simultaneously
  audience-profiler-agent ────┘

Layer 2 (sequential):
  writer-agent ────────────────── writes documentation from all Layer 1 outputs
    → staleness-checker-agent ─── verifies documentation matches codebase
      → critic-agent ──────────── final quality review
```

### Dispatch Protocol

1. **Layer 1 dispatch** — send brief to all three Layer 1 agents in parallel:
   - `scanner-agent` maps the project and ranks files by importance
   - `concept-extractor-agent` reads ranked files and extracts documentation content
   - `audience-profiler-agent` determines who reads the docs and how to write for them
2. **Writer dispatch** — send all Layer 1 outputs to `writer-agent`. It produces the documentation following `references/doc-template.md`, calibrated for the audience.
3. **Staleness check** — send writer output + codebase facts to `staleness-checker-agent`. It verifies every claim in the docs matches the current codebase.
4. **Critic review** — send documentation + staleness results to `critic-agent`.
5. **Revision loop** — if critic returns FAIL, re-dispatch affected agents. Maximum 2 rounds.
6. **Save** — write documentation to project root or specified location.

### Routing Rules

| Condition | Route |
|-----------|-------|
| User specifies audience | audience-profiler-agent uses it directly (no inference needed) |
| User says "document this" (no type) | audience-profiler defaults to User Guide (developers) or README (library) |
| User says "audit docs" | Skip writer-agent; run scanner → staleness-checker → critic directly |
| Monorepo detected | scanner-agent identifies package boundaries; writer produces per-package docs |
| Critic PASS | Save and deliver |
| Critic FAIL | Re-dispatch cited agents with feedback |

---

## Critical Gates

Before delivering, the critic-agent verifies ALL of these pass:

- [ ] Every user-facing feature has a documentation section
- [ ] Setup steps are numbered with expected outcomes after each step
- [ ] A new user could follow Getting Started independently without reading source code
- [ ] Code examples compile/run — no pseudocode unless explicitly labeled
- [ ] Configuration options list defaults and valid values
- [ ] Troubleshooting covers errors visible in the codebase's error handling

**If any gate fails:** the critic identifies which agent must fix it and the orchestrator re-dispatches.

---

## Single-Agent Fallback

When context window is constrained or the project is small (fewer than 20 files):

1. Skip multi-agent dispatch
2. Scan project structure and identify key files using the 7-rank importance system
3. Read 5-10 highest-ranked files
4. Determine audience (developer, end-user, operator)
5. Write documentation following `references/doc-template.md`
6. Cross-check env vars, setup steps, and API endpoints against code
7. Run Critical Gates as self-review
8. Save to project root or specified location

---

## Documentation Types

| Type | Audience | Focus | Length |
|------|----------|-------|--------|
| **README** | Developers discovering the project | What it does, quick start, contribution | 1-3 pages |
| **User Guide** | End-users operating the product | Workflows, features, troubleshooting | 5-20 pages |
| **API Reference** | Developers integrating | Endpoints, parameters, responses, errors | Varies |
| **Configuration Guide** | Operators deploying | Environment vars, settings, infrastructure | 2-5 pages |
| **Getting Started Tutorial** | New users of any type | Single workflow, start to finish | 1-2 pages |

Default to **User Guide** if the user says "document this" without specifying type.

---

## File Importance Ranking (7 Ranks)

The scanner-agent ranks files by documentation value:

| Rank | File Type | What It Reveals | Priority |
|------|-----------|-----------------|----------|
| 1 | Entry points (`main.*`, `index.*`, `app.*`) | App initialization, core structure | Read first |
| 2 | Route/endpoint definitions | Feature surface area | Read second |
| 3 | Config/env files | Setup requirements, feature flags | Read third |
| 4 | Models/Types/Schemas | Core data entities, relationships | Read for depth |
| 5 | Components/Views | UI structure, user interactions | Read for UX docs |
| 6 | Middleware/Interceptors | Auth, logging, error handling | Read for ops docs |
| 7 | Migration files | Data model evolution, schema requirements | Skim for setup |

---

## 3 Audience Types

| Audience | Vocabulary | Code Examples | Assumed Knowledge |
|----------|-----------|---------------|-------------------|
| **End-user** | Plain language, no jargon | Only CLI commands they run | Can install software, use a browser |
| **Developer** | Technical terms, API vocabulary | Request/response samples, code snippets | Can read code, use package managers |
| **Operator** | Infrastructure terminology | Config files, deployment commands | Understands networking, servers, CI/CD |

---

## Documentation Audit Mode

Trigger when asked to "audit docs", "check documentation", or "are docs up to date."

In audit mode, the orchestrator skips the writer-agent and runs:
1. `scanner-agent` — inventory all documentation files
2. `staleness-checker-agent` — compare each doc against current codebase
3. `critic-agent` — report findings with priority (security-relevant > setup > architecture > everything else)

Prioritize: auth docs and env var docs being stale is a security risk.

---

## Anti-Patterns

| Anti-Pattern | Problem | INSTEAD |
|--------------|---------|---------|
| Restating code as prose | "handleSubmit handles form submission" adds nothing | writer-agent describes user experience, not internal code |
| Missing prerequisites | User stuck at step 3 because step 0 was assumed | concept-extractor lists every dependency and version |
| Wall of text | Users scan, not read — long paragraphs get skipped | writer-agent uses tables, numbered lists, headers |
| Outdated screenshots | Screenshots rot faster than text | writer-agent prefers text descriptions of UI elements |
| Documenting internals | Users don't care about ORM layer | writer-agent documents behavior and interfaces |
| "See code for details" | Defeats purpose of documentation | concept-extractor extracts the relevant detail |
| Stale docs shipped as current | Actively mislead users | staleness-checker verifies every claim against codebase |

---

## Worked Example

**User:** "Document this project" (a Node.js REST API for task management)

**Layer 1 (parallel):**
- `scanner-agent` → maps project: src/index.ts, src/routes/, src/models/, prisma/schema.prisma, package.json, .env.example. Existing README is stale (references Node 16, project uses Node 18).
- `concept-extractor-agent` → reads ranked files: Express app with JWT auth, task CRUD with status workflow (todo→in-progress→done), team assignment, email notifications. Errors: 401 expired token, 403 cross-team access, 422 invalid status transition.
- `audience-profiler-agent` → Developer audience (API consumers). Recommended type: README + API Reference.

**Layer 2 (sequential):**
- `writer-agent` → writes README with Getting Started (5 numbered steps), API Reference, Configuration table, Troubleshooting section
- `staleness-checker-agent` → flags: Node version in setup (docs say 16, code needs 18), missing SMTP_PORT env var (in code but not documented)
- `critic-agent` → FAIL: 2 staleness issues must be fixed

**Revision:** writer-agent updates Node version and adds SMTP_PORT. Critic → PASS.

**Artifact saved to `README.md`.**

---

## Before Starting

### Step 0: Product Context
Check for existing context files: `README.md`, `CLAUDE.md`, `.agents/product-context.md`, `package.json#description`. Read all available context before scanning code.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | icp-research (from `hungv47/marketing-skills`) | Product positioning and audience already defined |
| `system-architecture.md` | system-architecture | Architecture decisions pre-mapped |
| `.agents/design/brand-system.md` | brand-system (from `hungv47/marketing-skills`) | Brand voice and terminology guidelines |

---

## Artifact Template

On re-run: rename existing artifact to `[name].v[N].md` and create new with incremented version.

```yaml
---
skill: technical-writer
version: 1
date: {{today}}
status: draft
audience: [end-user | developer | operator | mixed]
doc-type: [readme | user-guide | api-reference | config-guide | tutorial]
---
```

---

## References

- [references/doc-template.md](references/doc-template.md) — Full documentation template with writing guidelines and code-to-doc mapping
