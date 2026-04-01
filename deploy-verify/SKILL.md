---
name: deploy-verify
description: "Post-deploy health check — verifies a production URL is healthy after shipping. Checks page load, console errors, critical flows, and response times. Reports HEALTHY / DEGRADED / BROKEN with evidence. Not for pre-merge review (use review-chain) or shipping (use ship)."
argument-hint: "<production URL to verify>"
user-invocable: true
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
routing:
  intent-tags:
    - deploy
    - verify
    - health-check
    - production
    - canary
    - post-deploy
  position: pipeline
  produces:
    - deploy-verify-report.md
    - deploy-verify-baseline.json
  consumes:
    - ship-report.md
  requires: []
  defers-to:
    - skill: review-chain
      when: "user wants pre-merge code review, not post-deploy verification"
    - skill: ship
      when: "user wants to create a PR, not verify a deployed site"
  parallel-with: []
  interactive: false
  estimated-complexity: light
---

# Deploy Verify

*Product — Single-agent orchestration. Single-pass post-deploy health check using bash and optional browser automation.*

**Core Question:** "Is the deployed version working correctly in production?"

## Critical Gates — Read First

1. **This is a health check, not QA.** Check critical paths work — don't audit every page.
2. **Compare against baseline when available.** New errors that weren't in the baseline are regressions. Pre-existing errors are not.
3. **Evidence for every finding.** "The page is broken" without a screenshot, error message, or status code is not a finding.
4. **Stop at first BROKEN signal.** If the main page doesn't load, don't continue checking sub-pages.

## Inputs Required
- A production URL to verify
- (Optional) A baseline from a prior run (`.agents/deploy-verify-baseline.json`)

## Output
- `.agents/deploy-verify-report.md`
- `.agents/deploy-verify-baseline.json` (updated baseline for future comparisons)

## Chain Position
Previous: `ship` (recommended) | Next: none

---

## Execution

### 1. Pre-Flight

Determine what to verify:
- Read `.agents/ship-report.md` if it exists — extract what was changed and the PR URL
- If the user provided a URL, use it
- If no URL provided, check `.agents/ship-report.md` for a production URL or ask the user

### 2. Primary Health Check

Check the production URL for basic health:

```bash
# Check HTTP status
curl -s -o /dev/null -w "%{http_code}" <URL>
```

```bash
# Check response time
curl -s -o /dev/null -w "%{time_total}" <URL>
```

| Check | HEALTHY | DEGRADED | BROKEN |
|-------|---------|----------|--------|
| HTTP status | 200 | 3xx (redirect loop?) | 4xx, 5xx |
| Response time | <3s | 3-10s | >10s or timeout |
| Page content | Contains expected content | Partially loaded | Empty or error page |

### 3. Console Error Check (if browser available)

If `agent-browser` or similar browser automation is available:
1. Navigate to the URL
2. Capture console errors
3. Compare against baseline (if exists) — only NEW errors are findings
4. Take a screenshot as evidence

If no browser is available, skip this step and note it in the report.

### 4. Critical Path Verification

Based on what was shipped (from `.agents/ship-report.md`), verify the specific features that changed:
- If an API endpoint was modified, hit it and verify the response shape
- If a page was modified, verify it renders
- If auth was changed, verify login still works (if possible without credentials)

Keep this focused — verify 2-3 critical paths, not exhaustive QA.

### 5. Baseline Comparison

If `.agents/deploy-verify-baseline.json` exists from a prior run:
- Compare current console errors against baseline — flag only NEW errors
- Compare response times — flag regressions >2x baseline
- Compare HTTP status — flag any status change

### 6. Update Baseline

If the deployment is HEALTHY, save the current state as the new baseline:

```json
{
  "url": "<URL>",
  "date": "<ISO date>",
  "http_status": 200,
  "response_time_ms": 450,
  "console_errors": ["<any pre-existing errors>"],
  "screenshot": "<path if taken>"
}
```

Save to `.agents/deploy-verify-baseline.json`.

### 7. Write Report

Write to `.agents/deploy-verify-report.md`:

```markdown
---
skill: deploy-verify
version: 1
date: {{today}}
status: {{HEALTHY | DEGRADED | BROKEN}}
---

# Deploy Verification Report

**URL**: {{url}}
**Date**: {{date}}
**Verdict**: {{HEALTHY | DEGRADED | BROKEN}}

## Health Checks
| Check | Result | Evidence |
|-------|--------|----------|
| HTTP status | {{status code}} | — |
| Response time | {{time}}ms | {{comparison to baseline if available}} |
| Page content | {{loaded / partial / error}} | — |
| Console errors | {{count}} new ({{count}} pre-existing) | {{error messages}} |

## Critical Paths Verified
| Path | Result | Evidence |
|------|--------|----------|
| {{path}} | {{OK / FAILED}} | {{detail}} |

## Regressions (compared to baseline)
{{List of new issues not present in baseline, or "No baseline available" or "No regressions found"}}

## Recommendation
{{If BROKEN: "Investigate immediately. Consider rolling back." + defer to problem-analysis}}
{{If DEGRADED: "Monitor closely. Non-critical issues found."}}
{{If HEALTHY: "Deployment verified. Baseline updated."}}
```

---

## Edge Cases

- **No browser available**: Skip console error check and screenshots. Note in report.
- **URL requires authentication**: Note that authenticated paths could not be verified. Report on public paths only.
- **URL is not reachable**: Report BROKEN with "Connection refused" or "DNS resolution failed."
- **No baseline exists**: This is the first run. Everything is reported without comparison. Save current state as baseline.
- **Existing report**: Rename to `deploy-verify-report.v[N].md` and create new.

## Output Files

| File | Description |
|------|-------------|
| `.agents/deploy-verify-report.md` | Health check results with evidence |
| `.agents/deploy-verify-baseline.json` | Baseline state for future comparisons |
