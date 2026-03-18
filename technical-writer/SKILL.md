---
name: technical-writer
description: "Document this project, create a user guide, write documentation, explain this app, create README, write technical docs, document the codebase — product documentation, user guides, API references, technical writing. Scans project structure and translates code into clear, structured documentation."
license: MIT
metadata:
  author: hungv47
  version: "2.1.0"
---

# Technical Writer

*Productivity — Standalone skill. Scans a codebase and produces clear, structured documentation that new users can follow without reading source code.*

**Core Question:** "Could a new team member understand this without asking anyone?"

## Inputs Required
- A codebase or project to document
- (Optional) Target audience — developer, end-user, operator, or mixed
- (Optional) Documentation type — README, User Guide, API Reference, or Configuration Guide

## Output
- Documentation artifact saved to project root or specified location (e.g., `docs/`, `README.md`)

## Quality Gate
Before delivering, verify:
- [ ] Every user-facing feature has a documentation section
- [ ] Setup steps are numbered with expected outcomes after each step
- [ ] A new user could follow Getting Started independently without reading source code
- [ ] Code examples compile/run — no pseudocode unless explicitly labeled
- [ ] Configuration options list defaults and valid values
- [ ] Troubleshooting covers errors visible in the codebase's error handling

## Chain Position
Previous: none | Next: none (standalone)

Pairs well with: `system-architecture` (for architecture docs), `task-breakdown` (for contributor guides)

**Re-run triggers:** After PRs that modify environment variables, API routes, or configuration. After major version releases. When new features ship without documentation updates.

---

## Before Starting

### Step 0: Product Context

Check for existing context files: `README.md`, `CLAUDE.md`, `.agents/product-context.md`, `package.json#description`, `pyproject.toml`, `Cargo.toml`. Read all available context before scanning code.

### Required Artifacts
None — scans project structure directly.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | icp-research (from `hungv47/comms-skills`) | Product positioning, audience, and value prop already defined |
| `system-architecture.md` | system-architecture | Architecture decisions and component relationships pre-mapped |
| `.agents/design/brand-system.md` | brand-system (from `hungv47/design-skills`) | Brand voice and terminology guidelines for documentation tone consistency |

### Audience Interview
If the user doesn't specify an audience, interview:
1. Who reads this documentation? (developers integrating, end-users, ops team, all three?)
2. What's their technical level? (beginner, intermediate, expert)
3. What's the single most important thing they need to accomplish?

Audience clarity is necessary because writing for developers vs. end-users produces fundamentally different documents — mixing them confuses both.

---

## Documentation Types

Choose the type based on audience and project needs. A project may need multiple types.

| Type | Audience | Focus | Length |
|------|----------|-------|--------|
| **README** | Developers discovering the project | What it does, quick start, contribution | 1-3 pages |
| **User Guide** | End-users operating the product | Workflows, features, troubleshooting | 5-20 pages |
| **API Reference** | Developers integrating | Endpoints, parameters, responses, errors | Varies |
| **Configuration Guide** | Operators deploying | Environment vars, settings, infrastructure | 2-5 pages |
| **Getting Started Tutorial** | New users of any type | Single workflow, start to finish | 1-2 pages |

Default to **User Guide** if the user says "document this" without specifying type.

---

## Step 1: Scan Project Structure

Map the project to understand scope and architecture.

**Small projects (<50 files):**
```bash
find . -type f \( -name "*.js" -o -name "*.ts" -o -name "*.tsx" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.swift" -o -name "*.kt" \) | head -100
```

**Monorepos and large codebases (>50 files):**
1. Start with the top-level directory listing — identify packages, services, and apps
2. Read the root `package.json`, `workspace` config, or build manifest to understand project boundaries
3. Scan each package/service entry point separately
4. Treat each package as a documentation unit — decide which ones need docs vs. which are internal utilities

**Check for context files in this order:**
1. `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` — dependencies and project metadata
2. `README.md` — existing documentation to build on, not duplicate
3. `.env.example`, `config/`, `settings/` — configuration surface
4. `Dockerfile`, `docker-compose.yml` — deployment context
5. `openapi.yaml`, `swagger.json` — API contracts already defined
6. CI/CD configs (`.github/workflows/`, `Jenkinsfile`) — build and deploy patterns

---

## Step 2: Identify Key Files

Rank files by documentation value. Read 5-10 highest-ranked files.

**File importance ranking (highest to lowest):**

| Rank | File Type | What It Reveals | Priority |
|------|-----------|-----------------|----------|
| 1 | Entry points (`main.*`, `index.*`, `app.*`) | App initialization, core structure, dependency wiring | Read first |
| 2 | Route/endpoint definitions | Feature surface area and user-facing capabilities | Read second |
| 3 | Config/env files | Setup requirements, feature flags, environment needs | Read third |
| 4 | Models/Types/Schemas | Core data entities, relationships, validation rules | Read for depth |
| 5 | Components/Views | UI structure, user interactions, state management | Read for UX docs |
| 6 | Middleware/Interceptors | Auth, logging, error handling patterns | Read for ops docs |
| 7 | Migration files | Data model evolution, schema requirements | Skim for setup |

**Skip:** Generated files, `node_modules`, `vendor/`, `.git/`, build output, lock files. Skip test files unless documenting testing patterns.

---

## Step 3: Extract Core Concepts

Read each key file and extract documentation content using these specific techniques.

**Product Identity — scan entry points and README:**
- What problem does this solve? (look for comments, package description, CLI help text)
- Who is the target user? (look for onboarding flows, permission models, pricing tiers)
- What's the core value proposition? (look for the primary workflow — what does the happy path do?)

**Features and Capabilities — scan routes, components, and handlers:**
- List every user-facing endpoint or UI component
- Trace the primary workflow start-to-finish: entry → processing → output
- Identify input/output patterns: what goes in, what comes out, what format?

**Setup Requirements — scan config, env, and infrastructure files:**
- Extract every environment variable with its purpose and default
- List external service dependencies (databases, APIs, queues)
- Identify required vs. optional configuration

**Error Patterns — scan error handlers, validators, and catch blocks:**
- Catalog user-facing error messages
- Map each error to its cause and resolution
- Note validation rules that users need to satisfy

**Architecture Decisions — scan dependency graph and patterns:**
- Why was this tech stack chosen? (infer from dependencies and patterns)
- What design patterns are used? (MVC, event-driven, microservices)
- What are the system boundaries?

---

## Step 4: Generate Documentation

### Audience Calibration

Adjust language and depth based on the target audience:

| Audience | Vocabulary | Code Examples | Assumed Knowledge |
|----------|-----------|---------------|-------------------|
| **End-user** | Plain language, no jargon | Only CLI commands they run | Can install software, use a browser |
| **Developer** | Technical terms, API vocabulary | Request/response samples, code snippets | Can read code, use package managers |
| **Operator** | Infrastructure terminology | Config files, deployment commands | Understands networking, servers, CI/CD |

### Writing Principles
- Write for someone who has never seen the code
- Explain the "why" before the "how"
- Use concrete examples over abstract descriptions
- Include screenshots or diagrams when describing UI flows
- Keep technical jargon to a minimum — define it in a glossary when unavoidable
- Number every setup step and include the expected outcome

### Structure
Follow the template in `references/doc-template.md`. Adapt sections based on what the codebase reveals — omit sections with no content rather than writing placeholder text.

---

## Documentation Audit Mode

Documentation rots faster than code — setup steps reference old versions, env vars get added without updating docs, and architecture diagrams describe last quarter's design. Stale docs are worse than no docs because they actively mislead.

Trigger this mode when asked to "audit docs", "check documentation", or "are docs up to date." Also recommend running it after any PR that modifies environment variables, API routes, or configuration — these are the changes most likely to make docs stale.

### Step 1: Inventory
List all documentation files: README.md, CONTRIBUTING.md, CHANGELOG.md, ARCHITECTURE.md, docs/, and any .md files referenced in code.

### Step 2: Staleness Check
For each doc file, compare against current codebase:
- [ ] Setup steps match actual dependencies (check package.json/requirements.txt versions)
- [ ] Environment variables listed match .env.example or code references
- [ ] API endpoints documented match actual route definitions
- [ ] Configuration options match current defaults and valid values
- [ ] Architecture descriptions match current file/folder structure
- [ ] Links and cross-references resolve (no 404s within docs)

### Step 3: Consistency Check
- [ ] No contradictions between documents (README says X, CONTRIBUTING says Y)
- [ ] Terminology is consistent (same feature isn't called different names)
- [ ] Code examples compile/run against current codebase

### Step 4: Staleness Report
For each finding:
- **What's stale:** specific text or section
- **What's current:** actual state from codebase
- **Fix:** exact replacement text or "remove section"

Prioritize: Security-relevant docs (auth, env vars) > Setup docs > Architecture > Everything else.

---

## Anti-Patterns

Avoid these — they produce documentation that users ignore.

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Restating code as prose** | "The `handleSubmit` function handles form submission" adds nothing | Describe what the user experiences, not what the code does internally |
| **Missing prerequisites** | User gets stuck at step 3 because step 0 was assumed | List every dependency, version, and account needed before step 1 |
| **Wall of text** | Users scan, not read — long paragraphs get skipped | Use tables, numbered lists, and headers. One idea per paragraph |
| **Outdated screenshots** | Screenshots rot faster than text | Prefer text descriptions of UI elements. Use screenshots only for complex layouts |
| **Documenting internals** | Users don't care about your ORM layer | Document behavior and interfaces, not implementation |
| **"See code for details"** | Defeats the purpose of documentation | Extract the relevant detail into the doc |

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

Generate a single markdown file with all documentation. See `references/doc-template.md` for the full structure.

If the project is large, split into multiple focused guides:
- Getting Started Guide
- Feature Reference
- User Workflows
- Configuration Guide
- API Reference

---

## Worked Example

**User:** "Document this project" (a Node.js REST API for task management)

**Step 1 — Scan:** Found `src/index.ts`, `src/routes/`, `src/models/`, `prisma/schema.prisma`, `package.json`, `.env.example`

**Step 2 — Key files read:**
1. `src/index.ts` — Express app with JWT auth middleware
2. `src/routes/tasks.ts` — CRUD endpoints for tasks with status transitions
3. `src/routes/auth.ts` — Login/register with email verification
4. `prisma/schema.prisma` — User, Task, Team models
5. `.env.example` — DATABASE_URL, JWT_SECRET, SMTP_HOST

**Step 3 — Extracted:**
- Product: Team task management API
- Features: Task CRUD, status workflow (todo→in-progress→done), team assignment, email notifications
- Setup: PostgreSQL, SMTP server, JWT secret
- Errors: 401 on expired token, 403 on cross-team access, 422 on invalid status transition

**Step 4 — Audience:** Developer (API consumers). **Type:** README + API Reference.

**Artifact saved to `README.md`:**

```markdown
---
skill: technical-writer
version: 1
date: 2026-03-17
status: draft
audience: developer
doc-type: readme
---

# TaskFlow API

REST API for team task management with status workflows and email notifications.

## What It Does

TaskFlow lets teams create, assign, and track tasks through a defined workflow:
todo → in-progress → done. Each status transition triggers email notifications
to assigned team members.

### Core Capabilities

- **Task Management** — Create, update, delete, and list tasks with filtering by status and assignee
- **Status Workflows** — Enforced transitions prevent skipping steps (e.g., can't go from todo → done)
- **Team Collaboration** — Users belong to teams; tasks are team-scoped with role-based access
- **Email Notifications** — Automatic alerts on assignment and status changes

## Getting Started

### Requirements

- Node.js 18+
- PostgreSQL 14+
- SMTP server (or Mailtrap for development)

### First-Time Setup

1. Clone and install dependencies
   ```bash
   git clone https://github.com/example/taskflow-api.git
   cd taskflow-api && npm install
   ```
   Expected result: No errors in console

2. Copy environment config
   ```bash
   cp .env.example .env
   ```
   Expected result: `.env` file created

3. Set required variables in `.env`

   | Variable | Purpose | Example |
   |----------|---------|---------|
   | DATABASE_URL | PostgreSQL connection | postgresql://user:pass@localhost:5432/taskflow |
   | JWT_SECRET | Token signing key | any-random-string-32-chars |
   | SMTP_HOST | Email server | smtp.mailtrap.io |

4. Run database migrations
   ```bash
   npx prisma migrate deploy
   ```
   Expected result: "All migrations applied"

5. Start the server
   ```bash
   npm start
   ```
   Expected result: "Server listening on port 3000"

## Configuration Options

| Setting | Purpose | Default | Valid Values |
|---------|---------|---------|--------------|
| PORT | Server port | 3000 | 1024-65535 |
| DATABASE_URL | PostgreSQL connection | — (required) | PostgreSQL connection string |
| JWT_SECRET | Token signing | — (required) | String, min 32 characters |
| JWT_EXPIRY | Token lifetime | 24h | Duration string (1h, 7d) |
| SMTP_HOST | Email server | — (required) | Hostname |

## Troubleshooting

### "Invalid status transition"
**Cause:** Attempted to move a task to a status that isn't the next step in the workflow.
**Solution:** Tasks must follow todo → in-progress → done. Check current status before updating.

### "403 Forbidden" on task endpoints
**Cause:** Accessing a task belonging to a different team.
**Solution:** Verify the authenticated user belongs to the same team as the task.
```

---

## References

- [references/doc-template.md](references/doc-template.md) — Full documentation template with writing guidelines and code-to-doc mapping
