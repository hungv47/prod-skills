---
name: system-architecture
description: "Design system architecture, plan the tech stack, create database schema, design API structure, architect the system, plan the backend, design infrastructure — system architecture, technical blueprints, database design, API design, tech stack selection. Transforms product specs into production-ready technical blueprints before a single line of code is written."
license: MIT
metadata:
  author: hungv47
  version: "2.0.0"
---

# System Architecture Designer

*Productivity — Step 1 of 1. Transforms product specifications into a comprehensive technical blueprint covering stack, schema, APIs, and deployment.*

**Core Question:** "Will this still work at 10x scale with 10x team?"

## Inputs Required
- Product specification, PRD, or description of what needs to be built
- Scale expectations (users, requests, data volume) — gathered via interview if missing
- Known constraints (existing stack, compliance, budget, team skills)

## Output
- `.agents/system-architecture.md`

## Quality Gate
Before delivering, verify:
- [ ] Every tech choice has a rationale (not just "it's popular")
- [ ] API endpoints exist for every user-facing feature
- [ ] Database schema covers all entities mentioned in product spec
- [ ] Deployment section includes complete env var list
- [ ] File structure matches chosen framework conventions
- [ ] Auth model covers all user roles and permission levels
- [ ] At least one architectural trade-off is documented with alternatives considered

## Chain Position
Previous: `task-breakdown` (optional) | Next: `task-breakdown` (optional)

---

## Before Starting

### Step 0: Product Context

Check for `.agents/product-context.md`. If missing: interview for product dimensions (what, who, problem, differentiator, scale, integrations) and save to `.agents/product-context.md`. Or recommend running `icp-research` (from `hungv47/comms-skills`) to bootstrap it.

### Required Artifacts
None — this skill can run standalone.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | icp-research (from `hungv47/comms-skills`) | Industry context, user personas, and constraints |
| `task-breakdown.md` | task-breakdown | Feature list already decomposed into buildable units |

### Two Modes of Operation

**Mode 1: Tech Stack Already Chosen**
User provides tech stack upfront. Focus on architecture patterns, file structure, schema, and implementation details.

**Mode 2: Need Tech Stack Recommendations**
User needs help choosing stack. Recommend technologies based on requirements using `references/tech-stack-patterns.md`, then provide full architecture.

### Architecture Interview
If the user provides only a vague description ("build me an app", "I need a platform"):

1. What is the product and its core value proposition?
2. Who are the primary users? Expected concurrent users at launch and at 12 months?
3. What are the 3-5 critical user flows?
4. What data needs to be stored and queried?
5. Existing tech stack or team skill constraints?
6. Specific integrations needed? (payments, email, auth providers, etc.)
7. Performance requirements? (real-time updates, complex queries, offline support)
8. Security/compliance needs? (SOC2, HIPAA, GDPR, PCI)

All 8 answers are necessary before proceeding — without them, architectural decisions become guesswork and rework is inevitable.

---

## Step 1: Gather Context and Constraints

Extract from product spec or interview answers:

1. **User types** — list every role and what they can do
2. **Data entities** — every noun that needs to be stored
3. **Critical flows** — the 3-5 journeys that define the product
4. **Scale profile** — read-heavy vs. write-heavy, expected load, burst patterns
5. **Integration points** — every external service the system touches
6. **Non-functional requirements** — latency targets, uptime SLA, compliance

Use WebSearch if industry-specific benchmarks are needed: `"[product type] architecture patterns"` or `"[scale level] infrastructure recommendations"`.

---

## Step 2: Architecture Decisions

For each major decision, document the choice and the alternatives considered:

| Decision | Options Considered | Choice | Rationale |
|----------|-------------------|--------|-----------|
| Architecture pattern | Monolith, Microservices, Serverless | ? | ? |
| Database | PostgreSQL, MongoDB, DynamoDB | ? | ? |
| Auth | Clerk, Auth.js, Supabase Auth, Custom | ? | ? |
| Hosting | Vercel, AWS, Railway, Fly.io | ? | ? |
| Real-time (if needed) | WebSockets, SSE, Polling | ? | ? |

**Decision principles:**
- Start simple, scale when needed — a monolith is fine until it isn't
- Choose boring, proven tech over cutting-edge — reliability beats novelty
- Optimize for developer velocity first — speed of iteration matters most early on
- Ensure a clear upgrade path — avoid lock-in without escape routes

### Quick Stack Recommendations

| Use Case | Recommended Stack |
|----------|-------------------|
| MVP/Startup | Next.js + Supabase + Vercel |
| Enterprise SaaS | Next.js + PostgreSQL + Clerk + Stripe |
| Real-time App | Next.js + Supabase Realtime + Redis |
| API-first | Express/Fastify + PostgreSQL + Docker |
| Mobile App | React Native + Supabase + Expo |

Consult `references/tech-stack-patterns.md` and `references/tech-stack-matrix.md` for detailed comparisons.

---

## Step 3: Generate Architecture Document

Produce all 12 sections for the output artifact:

### Section Guide

| # | Section | Key Content | Reference |
|---|---------|-------------|-----------|
| 1 | System Overview | Architecture pattern, component diagram (text-based), key decisions | — |
| 2 | Tech Stack | Every dependency with version and rationale | `references/tech-stack-patterns.md` |
| 3 | File & Folder Structure | Complete tree with purpose annotations | `references/file-structure-patterns.md` |
| 4 | Database Schema | Tables, relationships, indexes, key queries | `references/database-patterns.md` |
| 5 | API Architecture | All endpoints: method, path, auth, request/response | `references/api-patterns.md` |
| 6 | State Management & Data Flow | Where state lives, data flow between layers | — |
| 7 | Service Connections | Inter-service communication, webhook handling, retry policies | — |
| 8 | Authentication & Authorization | Auth flow, permission model, session handling | `references/auth-patterns.md` |
| 9 | Key Features Implementation | Per-feature: components, API calls, state, edge cases | — |
| 10 | Deployment & Infrastructure | Env vars, CI/CD, staging/prod config | `references/deployment-patterns.md` |
| 11 | Monitoring & Debugging | Error tracking, logging, performance monitoring | — |
| 12 | Security Checklist | Input validation, secrets, HTTPS, headers, dependencies | — |

**Specificity rules:**
- Use exact package names and versions, not "some ORM"
- Use real file paths, not "a config file"
- Name specific services (e.g., "Sentry" not "an error tracker")
- Include actual code snippets for non-obvious patterns

---

## Step 4: Validation Cross-Reference

Before finalizing, cross-check the architecture against the product spec:

1. **Feature coverage** — trace every product feature to at least one API endpoint + DB table + UI component
2. **User flow completeness** — walk through each critical flow end-to-end and verify every step has infrastructure
3. **Edge case inventory** — for each flow: what happens on failure, timeout, invalid input, concurrent access?
4. **Env var audit** — every secret, API key, and config value is listed in the deployment section
5. **Scale check** — identify the first bottleneck under 10x current load; document the mitigation path

Flag gaps in the artifact under a `## Open Questions` section.

---

## Anti-Patterns

Avoid these — they cause predictable rework:

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| Premature microservices | Adds operational complexity before product-market fit | Start monolith, extract services at pain points |
| Schema without queries | Tables look clean but critical queries require full scans | Design schema around access patterns, not just entities |
| Auth as afterthought | Retrofitting permissions breaks existing flows | Define roles and permissions before API design |
| Missing error states | Happy-path-only architecture crumbles in production | Document error handling for every API endpoint |
| "We'll add monitoring later" | Debugging production without observability is guesswork | Include logging and error tracking in v1 |
| Over-engineering for scale | Building for 1M users when you have 100 wastes months | Design for 10x current load, have a plan for 100x |

---

## Artifact Template

On re-run: rename existing artifact to `system-architecture.v[N].md` and create new with incremented version.

```markdown
---
skill: system-architecture
version: 1
date: {{today}}
status: draft
---

# System Architecture: [Product Name]

## 1. System Overview

**Architecture pattern:** [monolith / microservices / serverless / hybrid]

**Component diagram:**
​```
[Client] → [API Layer] → [Database]
                ↓
         [External Services]
​```

**Key architectural decisions:**
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [decision] | [choice] | [why] |

## 2. Tech Stack

| Layer | Technology | Version | Rationale |
|-------|-----------|---------|-----------|
| Frontend | [framework] | [ver] | [why] |
| Backend | [framework] | [ver] | [why] |
| Database | [db] | [ver] | [why] |
| Auth | [provider] | [ver] | [why] |
| Hosting | [platform] | — | [why] |

## 3. File & Folder Structure

​```
project/
├── src/
│   ├── [dir]/ — [purpose]
│   └── [dir]/ — [purpose]
├── [config files]
└── [other root files]
​```

## 4. Database Schema

[Tables with columns, types, relationships, indexes]

**Key queries:**
- [Query 1]: [purpose]
- [Query 2]: [purpose]

## 5. API Architecture

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| [GET/POST/...] | [/api/...] | [role] | [what it does] |

## 6. State Management & Data Flow

[Where state lives, how data flows between layers]

## 7. Service Connections

[How services communicate, webhook handling, retry policies]

## 8. Authentication & Authorization

**Auth flow:** [description]
**Permission model:**
| Role | Permissions |
|------|-------------|
| [role] | [what they can do] |

## 9. Key Features Implementation
### [Feature 1]
- **Components:** / **API calls:** / **State:** / **Edge cases:**

## 10. Deployment & Infrastructure
**Env vars:** [VAR_NAME — purpose — required?]
**CI/CD:** [pipeline] | **Environments:** [staging, production]

## 11. Monitoring & Debugging
Error tracking: [tool] | Logging: [strategy] | Performance: [metrics]

## 12. Security Checklist
- [ ] Input validation, auth on protected routes, secrets in env vars
- [ ] HTTPS enforced, security headers, dependencies audited

## Open Questions

- [Any gaps or decisions that need user input]

## Next Step

Run `task-breakdown` to decompose this architecture into implementable tasks.
```

---

## Worked Example

**User:** "I need architecture for a SaaS invoicing tool. Small businesses send invoices, clients pay online. Need Stripe integration."

**Interview answers gathered:**
- Users: business owners (send invoices), clients (view/pay)
- Scale: ~500 businesses, ~2000 invoices/month at launch
- Integrations: Stripe for payments, SendGrid for email
- Requirements: PDF generation, payment tracking, dashboard
- Constraints: small team, fast launch needed

**Artifact saved to `.agents/system-architecture.md` (excerpts):**

```markdown
# System Architecture: InvoiceFlow

## 1. System Overview
Architecture: Monolith (appropriate for team size and launch timeline)
[React SPA] → [Next.js API Routes] → [PostgreSQL]
                    ↓          ↓
              [Stripe]    [SendGrid]

## 2. Tech Stack
| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | Next.js 14.x | Full-stack, fast iteration |
| Database | PostgreSQL via Supabase | Relational, strong joins for invoice queries |
| Auth | Clerk | Drop-in auth, org support |
| Payments | Stripe | Industry standard, PCI compliant |
| Hosting | Vercel | Zero-config Next.js deployment |

## 4. Database Schema (excerpt)
businesses: id, name, email, stripe_account_id, created_at
invoices: id, business_id (FK), client_id (FK), amount, status, due_date, pdf_url
payments: id, invoice_id (FK), stripe_payment_id, amount, status, paid_at
Indexes: invoices(business_id, status), payments(stripe_payment_id)

## 5. API Architecture (excerpt)
| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| POST | /api/invoices | business_owner | Create draft invoice |
| POST | /api/invoices/:id/send | business_owner | Send invoice email |
| GET | /api/pay/:token | public (token) | Client payment page |
| POST | /api/webhooks/stripe | stripe_signature | Payment status sync |

## 10. Deployment — Env Vars
DATABASE_URL, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, SENDGRID_API_KEY,
CLERK_SECRET_KEY, NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
```

*(Full artifact contains all 12 sections)*

---

## References

- [references/tech-stack-patterns.md](references/tech-stack-patterns.md) — Tech choice comparisons and recommendations
- [references/tech-stack-matrix.md](references/tech-stack-matrix.md) — Stack comparison matrix
- [references/file-structure-patterns.md](references/file-structure-patterns.md) — Directory structures by framework
- [references/database-patterns.md](references/database-patterns.md) — Common schemas and query patterns
- [references/api-patterns.md](references/api-patterns.md) — REST best practices and endpoint examples
- [references/auth-patterns.md](references/auth-patterns.md) — Authentication implementations
- [references/deployment-patterns.md](references/deployment-patterns.md) — CI/CD and infrastructure patterns
- [references/failure-modes.md](references/failure-modes.md) — Failure mode criticality classification
