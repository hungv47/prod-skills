# Product Skills — Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning is [SemVer](https://semver.org/spec/v2.0.0.html) — major.minor.patch.

This file tracks stack-level releases. SKILL.md files describe current behavior; this file documents what changed and when.

---

## [2.0.0] - 2026-05-16

**Agent Skills 2.0 — fresh start.** The product-skills stack reset to 2.0.0 as part of the umbrella Agent Skills 2.0 release. Released as a pre-release tag on the `refactor/v2.0` branch. The `main` branch holds the legacy v1.x line for users who do not opt into the 2.0 trunk.

### Skills (6)

- `orchestrate-product` — router that reads project state (spec, flows, architecture) and proposes the next skill
- `user-flow` — multi-step in-product flow mapping (screens, decisions, transitions, edge cases)
- `system-architecture` — technical blueprint (stack, schema, API, deployment) → `architecture/system-architecture.md`
- `code-cleanup` — refactor existing code for readability + dead-code removal (5 golden rules: preserve behavior, small steps, conventions, test after each change, rollback awareness)
- `machine-cleanup` — developer-machine audit + cleanup (dotfolders, caches, toolchains, package-manager globals)
- `docs-writing` — generate docs from a codebase (README, API ref, runbook, ship log, release notes)

### Recommended order

Run `user-flow` BEFORE `system-architecture`. User flows define WHAT screens and transitions exist; architecture defines HOW to build them.

### Cross-stack inputs

- `research/product-context.md` (from `icp-research` in research-skills) — system-architecture + docs-writing read for context
- `.agents/skill-artifacts/meta/sketches/prioritize-*.md` (from `prioritize` in research-skills) — system-architecture reads for what to build
