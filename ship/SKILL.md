---
name: ship
description: "Automated pre-merge pipeline — runs tests, checks review gate, organizes commits, generates PR with structured body. Produces `.agents/ship-report.md`. Not for code review (use review-chain) or task decomposition (use task-breakdown). For code cleanup before shipping, see code-cleanup. For post-deploy health check, see deploy-verify."
argument-hint: "[optional: PR title or description]"
allowed-tools: Read Grep Glob Bash
user-invocable: true
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
  budget: standard
  estimated-cost: "$0.15-0.40"
routing:
  intent-tags:
    - ship
    - deploy
    - pr
    - pull-request
    - merge
    - push
  position: pipeline
  produces:
    - ship-report.md
  consumes:
    - meta/review-chain-report.md
    - tasks.md
    - spec.md
  requires: []
  defers-to:
    - skill: review-chain
      when: "user wants a code review, not a shipping pipeline"
    - skill: task-breakdown
      when: "user needs to break work into tasks, not ship completed work"
  parallel-with: []
  interactive: false
  estimated-complexity: medium
---

# Ship — Orchestrator

*Product — Multi-agent orchestration. Automated pre-merge pipeline from tests through PR creation.*

**Core Question:** "Is this branch ready to merge, and can I prove it?"

## Inputs Required
- A feature branch with committed changes (not on the base branch)
- Tests (if any exist in the project)

## Output
- `.agents/ship-report.md`
- A pull request on the remote repository

## Chain Position
Previous: `review-chain` (recommended) | Next: `deploy-verify` (optional)

**Re-run triggers:** After fixing review findings, after rebasing, or after adding last-minute changes.

---

## Multi-Agent Architecture

### Agent Roster

| Agent | File | Focus |
|-------|------|-------|
| test-runner-agent | `agents/test-runner-agent.md` | Runs tests, reports results and coverage |
| commit-organizer-agent | `agents/commit-organizer-agent.md` | Splits uncommitted changes into bisectable commits |
| pr-writer-agent | `agents/pr-writer-agent.md` | Generates PR title and body from diff + artifacts |
| critic-agent | `agents/critic-agent.md` | Verifies all shipping gates pass |

### Execution Layers

```
Gate (must pass before continuing):
  test-runner-agent ──────────── run tests, report results

Pipeline (sequential):
  commit-organizer-agent ─────── organize uncommitted changes into clean commits
    → pr-writer-agent ─────────── generate PR title + body
      → critic-agent ──────────── final shipping gate review
```

Note: Unlike other skills that use parallel Layer 1 → sequential Layer 2, ship uses a gate → pipeline pattern. The test-runner is a hard gate (fail = stop). The pipeline only runs if the gate passes.

### Dispatch Protocol

1. **Pre-flight** — verify branch state, detect base branch, check for uncommitted changes
2. **Gate check** — verify review-chain has run (check `.agents/meta/review-chain-report.md`)
3. **Layer 1** — dispatch test-runner-agent. If tests fail, STOP and report.
4. **Layer 2** — dispatch commit-organizer (if uncommitted changes exist), then pr-writer, then critic.
5. **Ship** — push branch, create PR via `gh pr create`
6. **Report** — save `.agents/ship-report.md`

### Routing Logic

| Condition | Route |
|-----------|-------|
| On base branch (main/master) | ABORT — "Cannot ship from the base branch" |
| No changes vs base branch | ABORT — "Nothing to ship — branch is identical to base" |
| Review-chain report missing | WARN — "No review-chain report found. Run `/review-chain` first for a quality gate. Continue anyway?" (ask user) |
| Review-chain verdict = CRITICAL | STOP — "Review found critical issues. Fix them before shipping." |
| Tests fail | STOP — "Tests failed. Fix before shipping." Report failures. |
| Tests pass or no tests exist | Continue to commit organization |
| Critic PASS | Push and create PR |
| Critic FAIL | Re-dispatch failed agent with feedback (max 1 cycle) |

---

## Critical Gates

Before shipping, the critic-agent verifies ALL of these pass:

- [ ] Branch is not the base branch
- [ ] Tests pass (or no test framework exists — noted in report)
- [ ] No merge conflicts with base branch
- [ ] Review-chain status is recorded (PASS, FIXED, or user-overridden warning)
- [ ] All commits have meaningful messages (not "wip", "fix", "asdf")
- [ ] PR body includes: summary, test results, and review status

**If any gate fails:** the critic identifies which agent must fix it and the orchestrator re-dispatches with specific feedback. Maximum 1 revision cycle — if it still fails, report to user.

---

## Execution Detail

### Step 0: Pre-Flight

```bash
# Detect base branch
git remote show origin | grep 'HEAD branch' | awk '{print $NF}'
```

```bash
# Check current branch
git branch --show-current
```

```bash
# Check for uncommitted changes
git status --short
```

```bash
# Check diff against base branch
git log --oneline <base>..HEAD
```

Verify:
- Not on base branch
- Has commits or uncommitted changes vs base
- Remote is reachable

### Step 1: Review Gate Check

Read `.agents/meta/review-chain-report.md` if it exists.

| Review Status | Action |
|--------------|--------|
| PASS or FIXED | Record in ship report. Continue. |
| CRITICAL | STOP. Tell user to fix critical issues first. |
| File missing | WARN user: "No review-chain report found. Running without quality gate." Ask if they want to continue. |

### Step 2: Run Tests

Dispatch `test-runner-agent`. It detects the project's test framework and runs the test suite.

If tests fail:
- Report which tests failed with output
- STOP — do not continue to PR creation
- Suggest fixes if the failures are obvious

If no test framework is detected:
- Note "No tests found" in the report
- Continue — absence of tests is not a blocker (but flag it)

### Step 3: Organize Commits

If there are uncommitted changes, dispatch `commit-organizer-agent`.

The organizer:
- Groups changes by logical unit (infrastructure, models, controllers, tests, config)
- Creates one commit per logical group with a descriptive message
- Ensures each commit is independently valid (no half-finished states)

If all changes are already committed with good messages, skip this step.

If existing commits have bad messages (e.g., "wip", "fix", "asdf") but the code is correct, the commit-organizer cannot fix these — interactive rebase requires manual intervention. Tell the user: "Commits X and Y have unclear messages. Run `git rebase -i <base>` to clean them up, then re-run `/ship`." Do NOT force-push or rewrite history automatically.

### Step 4: Generate PR

Dispatch `pr-writer-agent`. It reads:
- The full diff against the base branch
- `.agents/tasks.md` (if exists) — to check task completion
- `.agents/spec.md` (if exists) — to reference the original spec
- `.agents/meta/review-chain-report.md` (if exists) — to include review status
- Test results from Step 2

It generates:
- **PR title** — short (under 70 chars), descriptive
- **PR body** — structured with Summary, Test Results, Review Status, and Tasks Completed sections

### Step 5: Critic Review

Dispatch `critic-agent` to verify all shipping gates pass.

If PASS: proceed to push.
If FAIL: re-dispatch the responsible agent with feedback. Max 1 cycle.

### Step 6: Push and Create PR

```bash
git push -u origin $(git branch --show-current)
```

```bash
gh pr create --title "<title>" --body "$(cat <<'EOF'
<generated body>
EOF
)"
```

### Step 7: Save Report

Write to `.agents/ship-report.md`:

```markdown
---
skill: ship
version: 1
date: {{today}}
status: shipped
---

# Ship Report

**Branch**: {{branch name}}
**Base**: {{base branch}}
**PR**: {{PR URL}}
**Date**: {{date}}

## Test Results
- Framework: {{detected framework}}
- Result: {{PASS / FAIL / NO TESTS}}
- Details: {{test output summary}}

## Review Gate
- Status: {{PASS / FIXED / WARNING (no review) / CRITICAL (blocked)}}
- Report: `.agents/meta/review-chain-report.md`

## Commits
| # | Hash | Message |
|---|------|---------|
| 1 | abc123 | feat: add user authentication |
| 2 | def456 | test: add auth integration tests |

## Tasks Completed
{{List of tasks from .agents/tasks.md marked as done, or "No task file found"}}

## PR Body
{{The generated PR body for reference}}
```

## Next Step

After PR is merged, run `deploy-verify` to confirm production health. Run `technical-writer` in ship-log mode to update product context.

---

## Single-Agent Fallback

When context window is constrained or the project is small (fewer than 5 changed files):

1. Skip multi-agent dispatch
2. Run tests directly via bash
3. Check for uncommitted changes, commit if needed
4. Generate PR title and body inline
5. Push and create PR
6. Save ship report

---

## Anti-Patterns

| Anti-Pattern | Problem | INSTEAD |
|--------------|---------|---------|
| Shipping without running tests | Silent regressions hit production | Always run tests first — no tests is noted, failing tests block |
| "wip" commits in PR | Reviewers can't understand changes | commit-organizer splits into logical, bisectable commits |
| PR body says "various fixes" | No context for reviewers or future archaeology | pr-writer generates structured body from diff and artifacts |
| Force-pushing to shared branches | Destroys others' work | Never force-push — rebase and regular push only |
| Shipping with CRITICAL review findings | Known bugs in production | Review gate blocks shipping on CRITICAL |

---

## Edge Cases

- **No test framework**: Note it in the report, continue. Absence of tests is a flag, not a blocker.
- **No review-chain report**: Warn user, ask if they want to continue without the quality gate.
- **All changes already committed**: Skip commit-organizer, proceed to PR generation.
- **PR already exists for this branch**: Update the existing PR body instead of creating a new one. Use `gh pr edit`.
- **Remote push fails**: Report the error. Common causes: no upstream, auth issues, branch protection rules.
- **Merge conflicts with base**: Report conflicts. Do NOT auto-resolve — tell user to rebase manually.
- **Existing ship-report**: Rename to `ship-report.v[N].md` and create new with incremented version.

## Output Files

| File | Description |
|------|-------------|
| `.agents/ship-report.md` | Shipping report with PR URL, test results, review gate status |
