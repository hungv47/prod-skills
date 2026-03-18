---
name: task-breakdown
description: "This skill should be invoked when the user has a spec, architecture, or defined feature and needs it broken into buildable tasks with acceptance criteria. Triggers include 'break this into tasks', 'create tasks', 'what do I build first', 'make this actionable', 'create tickets', 'sprint planning', 'backlog', 'implementation order', or 'break this into sprints' -- even if they just say 'this is too big, where do I start' or 'I'm overwhelmed by how much there is to do.' Produces tasks for AI agents or engineers. Not for clarifying unclear requirements (use plan-interviewer), designing architecture (use system-architecture), marketing/strategic plans (use imc-plan or solution-design), or diagnosing root causes (use problem-analysis)."
license: MIT
metadata:
  author: hungv47
  version: "1.1.0"
---

# Task Breakdown

*Productivity — Standalone skill. Break architecture into executable tasks and build them one at a time with AI agents.*

**Core Question:** "Can an engineer pick up any single task and ship it independently?"

## Inputs Required
- Architecture document, feature spec, or problem description to decompose
- Target scope (MVP, full feature, spike)

## Output
- `.agents/tasks.md`

## Quality Gate
Before delivering, verify:
- [ ] Every task has exactly ONE acceptance test
- [ ] No task depends on something not yet defined
- [ ] Risky/uncertain work is front-loaded
- [ ] All external config is in Prerequisites, not buried in tasks
- [ ] A junior dev could verify each acceptance criterion
- [ ] No task requires unstated knowledge to complete

## Chain Position
Previous: `system-architecture` or `plan-interviewer` | Next: task execution (Phase 2)

**Re-run triggers:** When architecture changes after initial breakdown, when scope mode changes (e.g., full → minimal), or when tasks consistently fail acceptance criteria (indicates decomposition issues).

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `system-architecture.md` | system-architecture | Architecture defines structure for task decomposition |
| `spec.md` | plan-interviewer | Feature specification with decided requirements |
| `.agents/design/user-flow.md` | user-flow (from `hungv47/design-skills`) | User flow diagrams for feature decomposition and acceptance criteria |

If upstream artifacts' `date` fields are older than 30 days, recommend re-running the source skill before proceeding — stale architecture or specs produce misaligned tasks.

---

## Step 0: Scope Mode

Before decomposing, confirm the user's scope intent. This prevents mismatch between decomposition behavior and expectations.

| Mode | When | Behavior |
|------|------|----------|
| **FULL SCOPE** | Discovery, greenfield, "what would it take?" | Capture everything — defer cuts to after decomposition |
| **LOCKED SCOPE** | Spec is final, ready to build | Decompose exactly what's written — flag gaps but don't add |
| **MINIMAL SCOPE** | Too much on the plate, need an MVP | Actively cut before decomposing — ask "can we ship without this?" for each feature |

Ask: *"Are we decomposing everything (full scope), building exactly what's spec'd (locked), or cutting to minimum (minimal)?"*

Default to LOCKED SCOPE if the user provides a finished spec. Default to MINIMAL SCOPE if the user mentions MVP, prototype, or time pressure. If arriving from `plan-interviewer`, check the spec for scope signals before asking — the user may have already decided.

---

## Phase 1: Task Decomposition

### Task Format

```markdown
## Task [N]: [Title]

**Depends on:** [Task numbers this requires, or "None"]

**Outcome:** [What exists when done - one sentence]

**Why:** [What this unblocks]

**Acceptance:** [How to verify - specific test, expected result]

**Human action:** [External setup needed, if any]
```

### Sizing Rules

Right size:
- Changes ONE testable thing
- 5-30 min agent implementation time
- Failure cause is obvious and isolated

Split if:
- Multiple independent things to test
- Multiple files for different reasons
- Acceptance has multiple unrelated conditions

### Content Rules

**Outcomes, not implementation.**

Bad: "Create users table with id, email, created_at using Prisma"
Good: "Database stores user records with unique emails and timestamps"

Bad: "Install React Query and create useUser hook"
Good: "User data fetches efficiently with caching"

The agent knows their tools. Define success, not steps.

**Risk-first ordering.**

Put uncertain/complex tasks early. Fail fast on hard problems. Don't save integrations and edge cases for the end.

Typical flow: setup > risky core logic > database > API > UI > integration

**Dependencies explicit.**

Every task lists what it needs. Enables parallel work and failure impact analysis.

### Output Structure

```markdown
# [Project] Tasks

## Prerequisites
[External setup: accounts, keys, env vars]

## Tasks
[Ordered task list with dependencies]

## Out of Scope
[What's NOT in this MVP]
```

### Pre-Execution Gate

Before starting execution, run the Quality Gate checklist at the top of this skill.

### Anti-Patterns

**Too big:** "Build the auth system" - This is 5+ tasks disguised as one.

**Too small:** "Create the Button component" then "Add onClick to Button" - Combine unless genuinely separate concerns.

**Hidden dependency:** Task 8 needs an API key not mentioned until Task 8. Put it in Prerequisites.

**Vague acceptance:** "User flow works correctly" - Works how? What's the test?

**Implementation-as-outcome:** "Use Redux for state management" - That's a how, not a what.

---

## Phase 2: Task Execution

### Before Starting

1. Read architecture doc fully
2. Read task list fully
3. Understand the end state before writing code
4. If anything is ambiguous, ask — assumptions cause rework.

### Per-Task Protocol

1. State which task you're starting
2. Write minimum code to pass acceptance
3. State exactly what to test and expected result
4. Stop and wait for confirmation — proceeding without it risks wasted work.
5. Pass → commit, announce next task
6. Fail → fix the specific issue only, don't expand scope

### Coding Rules

**Do:**
- Write absolute minimum code required
- Focus only on current task
- Keep code modular and testable
- Preserve existing functionality

**Avoid — these cause scope creep and breakage:**
- Sweeping changes across unrelated files
- Touching unrelated code
- Refactoring unless the task requires it
- Adding features not in the current task
- Premature optimization

**When human action is needed:**
- State exactly what to do and which file/value to update
- Wait for confirmation before continuing

### When Stuck

1. State what's blocking
2. Propose smallest modification to unblock
3. Wait for approval

Avoid silently skipping acceptance criteria — it masks failures. Avoid reinterpreting the task — flag ambiguity instead.

### Scope Change Protocol

If you discover a missing requirement:

1. Stop current task
2. State what's missing and why it's needed
3. Propose where it fits in task order
4. Wait for PM to update task list
5. Resume only after task list is updated

Avoid improvising new requirements into existing tasks — it creates untested scope.

---

## PM Feedback Format

When reporting test results:

```
Task [N]: PASS | FAIL | BLOCKED

[If FAIL]: What broke, error message, steps to reproduce
[If BLOCKED]: What's preventing test
```

Keep it tight. Agent needs signal, not narrative.

---

## Example

```markdown
# Todo App Tasks

## Prerequisites
- Supabase project with URL + anon key in .env.local
- Resend API key in .env.local

## Tasks

## Task 1: Scaffold
**Depends on:** None
**Outcome:** Next.js app runs with Supabase client configured
**Why:** Foundation for all features
**Acceptance:** `npm run dev` shows page, console logs "Supabase connected"

## Task 2: Signup
**Depends on:** 1
**Outcome:** Users create accounts via email/password
**Why:** Unblocks all authenticated features
**Acceptance:** Submit signup form → user appears in Supabase Auth → confirmation email sent

## Task 3: Login + Protected Routes
**Depends on:** 2
**Outcome:** Users log in and access protected pages
**Why:** Unblocks task management UI
**Acceptance:** Login → redirect to /dashboard. Visit /dashboard logged out → redirect to /login

## Task 4: Tasks Table + RLS
**Depends on:** 1
**Outcome:** Database stores tasks per user
**Why:** Unblocks task CRUD
**Acceptance:** Insert task via Supabase dashboard with user_id, title, due_date, completed. Query as different user returns empty.

## Task 5: Create Task
**Depends on:** 3, 4
**Outcome:** Users create tasks from UI
**Why:** Core feature
**Acceptance:** Submit form → task in DB → appears in list without refresh

## Out of Scope
- Social auth
- Task sharing
- Mobile app
```

---

## Artifact Template

On re-run: rename existing artifact to `tasks.v[N].md` and create new with incremented version.

Save to `.agents/tasks.md` using the Output Structure format from Phase 1.
