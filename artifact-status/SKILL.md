---
name: artifact-status
description: "Scan .agents/ — report what exists, what's stale, and the critical path to your next goal. Run at session start or when deciding what to do next."
argument-hint: "[optional: goal — e.g. 'launch content', 'build the app', 'run strategy']"
user-invocable: true
license: MIT
metadata:
  author: hungv47
  version: "2.0.0"
---

# Artifact Status

Scan `.agents/`, report state, recommend next action.

## Execute

1. **Scan** `.agents/` for every `.md` file. For each, read frontmatter to extract `skill:`, `date:`, `status:`, `version:`.

2. **Report** as a single table sorted by date (newest first). Mark **STALE** if `date:` is >30 days old. Include file count for glob paths (`mkt/content/*.md`).

```
| Artifact | Skill | Date | Age | Status |
|----------|-------|------|-----|--------|
| product-context.md | icp-research | 2026-03-15 | 13d | ok |
| solution-design.md | solution-design | 2026-02-10 | 46d | STALE |
| mkt/content/ | content-create | — | — | 4 files |
```

If `.agents/` doesn't exist or is empty, say so and skip to step 3.

3. **Recommend** based on the user's goal. If they gave one, trace the dependency chain backward from that goal and identify the first missing or stale artifact. If no goal, use this priority:

| If this is missing/stale | Run this | Because |
|--------------------------|----------|---------|
| `product-context.md` | `/icp-research` | 12+ downstream skills depend on it |
| `solution-design.md` (and goal involves building) | `/market-research` → `/solution-design` | Architecture needs business context |
| `spec.md` (and goal involves building) | `/plan-interviewer` | Can't architect without a spec |
| `system-architecture.md` | `/system-architecture` | Can't break down tasks without architecture |
| `mkt/imc-plan.md` (and goal involves content) | `/imc-plan` | Content needs channel strategy |

Don't list every missing artifact — focus on the **one or two skills that unblock the most**.

## Dependency Graph

```
product-context.md ← /icp-research
├→ market-research.md ← /market-research ─┐
├→ problem-analysis.md ← /problem-analysis ┤
│                                           ├→ solution-design.md ← /solution-design
│                                           │   ├→ targets.md ← /funnel-planner → experiment-*.md
│                                           │   ├→ mkt/imc-plan.md ← /imc-plan → mkt/content/ → mkt/*.humanized.md
│                                           │   └→ system-architecture.md ← /system-architecture
│                                           │       └→ tasks.md ← /task-breakdown
├→ spec.md ← /plan-interviewer ────────────→┘
├→ design/brand-system.md ← /brand-system
└→ design/user-flow.md ← /user-flow ──→ system-architecture.md, tasks.md
```

Trace from the user's goal back through this graph to find the first gap.
