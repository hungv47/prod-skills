---
name: code-cleanup
description: "Clean up the codebase, reorganize files, remove dead code, remove AI slop, fix AI-generated code, clean up PR, remove unnecessary comments, refactor this, fix code smells, improve project structure — structural cleanup, code-level cleanup, dead code removal, and refactoring without breaking functionality."
license: MIT
metadata:
  author: hungv47
  version: "2.1.0"
---

# Code Cleanup

*Productivity — Standalone skill. Structural cleanup, code-level cleanup, and refactoring — without breaking functionality.*

**Core Question:** "Is this change purely structural with zero behavioral impact?"

## Inputs Required
- A codebase or set of files to clean up
- User intent: structural reorganization, code-level cleanup, refactoring, or all three

## Output
- `.agents/cleanup-report.md`

## Quality Gate
Before delivering, verify:
- [ ] All tests pass after every change
- [ ] No behavioral changes — observable behavior is identical before and after
- [ ] Every removal is justified (dead code, AI slop, or code smell — not "I think it's unused")
- [ ] Existing conventions (naming, formatting, linting) are preserved

## Chain Position
Previous: none | Next: none (standalone)

---

## Before Starting

### Step 0: Product Context

Check for project documentation (README, CONTRIBUTING.md, or similar). Understanding the project's purpose and conventions prevents removing code that looks dead but is used via dynamic imports, reflection, or external consumers.

### Required Artifacts
None — this is a standalone skill.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `.eslintrc` / `biome.json` / linting config | Project | Coding conventions to preserve |
| `CONTRIBUTING.md` | Project | File naming and structure conventions |

---

## Golden Rules

1. **Preserve behavior** — Every change must produce the same observable behavior. If you can't verify this, don't make the change.
2. **Small incremental steps** — One change at a time. Commit between steps. Never combine a refactor with a feature change.
3. **Check existing conventions first** — Before changing anything, read the codebase's existing coding guidelines, linting config, naming patterns, and file structure. Match them.
4. **Test after each change** — Run the test suite after every modification. If tests break, revert and try a smaller step.
5. **Rollback awareness** — Commit before starting. Note the hash. If a change chain gets too complex, `git reset --hard <hash>` and try a different approach.
6. **Session limits** — Cap at 30 changes per cleanup session. After 15 changes, generate an interim summary of what's been done and what remains. If each fix is spawning 2+ new issues, stop and reassess scope — cleanup is bounded work, not open-ended exploration.

## Triage

Determine scope before starting. These parts can be used independently or combined.

| User intent | Part to use |
|---|---|
| "Reorganize files", "remove dead code", "clean up repo structure" | Part 1: Structural |
| "Remove AI slop", "clean up PR", "fix code smells" | Part 2: Code-Level |
| "Refactor this", "extract this", "redesign this module" | Part 3: Refactoring |
| "Clean up the codebase" (broad) | Part 1 → Part 2 → Part 3 in order |

---

## Part 1: Structural Cleanup

Reorganize files, remove junk, and clean up project structure.

### Phase 1: Analysis

Before touching anything, understand the codebase.

1. Map the directory structure
   ```bash
   find . -type f -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" | head -100
   tree -L 3 -I 'node_modules|.git|__pycache__|.next|dist|build|venv|.venv' || find . -maxdepth 3 -type d | grep -v node_modules | grep -v .git
   ```

2. Identify entry points and config files
   - package.json, pyproject.toml, requirements.txt, Cargo.toml
   - Main entry files (index.*, main.*, app.*, server.*)
   - Config files (*.config.js, .env*, tsconfig.json)

3. Run `scripts/analyze_codebase.py` to generate dependency report

4. Interview for clarifications if needed
   - What is the primary tech stack?
   - Are there specific directories to preserve?
   - Any files that look dead but are actually used?

### Phase 2: Identify Cleanup Targets

**Safe to remove without verification:**
- Empty directories
- .DS_Store, Thumbs.db, desktop.ini
- Duplicate package lock files (keep one)
- __pycache__, .pyc, .pyo files
- node_modules/.cache
- Coverage reports, test artifacts
- Editor configs if inconsistent (.idea, .vscode with personal settings)
- Backup files (*.bak, *.backup, *~, *.swp)
- Log files (*.log)
- Compiled outputs if source exists

**Requires dependency check before removal:**
- Unused source files (verify no imports)
- Orphan test files (verify not in test config)
- Unused assets/images
- Old migration files (check if applied)
- Commented-out code blocks
- Unused dependencies in package.json/requirements.txt

**Avoid removing without explicit permission — these may be environment-specific or critical:**
- Config files (might be environment-specific)
- Database files or migrations
- CI/CD configs
- License files
- README or docs

### Phase 3: Reorganization Patterns

Only reorganize when explicitly asked. Follow the project's existing structure. If no structure exists, suggest one based on the stack and get confirmation before moving files.

**File naming conventions** — detect existing patterns first. Common defaults:
- Components: PascalCase (Button.tsx)
- Utilities: camelCase (formatDate.ts)
- Constants: UPPER_SNAKE_CASE or kebab-case file
- Tests: *.test.ts, *.spec.ts, or test_*.py

**When to consolidate:** fewer than 3 files with no growth path, multiple directories with same purpose (utils, helpers, lib), deeply nested single-file directories.

**When to split:** more than 15-20 files in one directory, mixed concerns, files with different lifecycle.

### Phase 4: Execute Changes

1. Create backup commit before changes
   ```bash
   git add -A && git commit -m "Pre-cleanup snapshot" 2>/dev/null || echo "No git or nothing to commit"
   ```

2. Remove safe-to-delete files first
   ```bash
   find . -name ".DS_Store" -delete 2>/dev/null
   find . -name "*.pyc" -delete 2>/dev/null
   find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
   find . -type d -empty -delete 2>/dev/null
   ```

3. Reorganize file structure (if applicable)
   - Move files in batches by category
   - Update imports after each batch
   - Run tests or type checks between batches

4. Update import paths
   - Grep for remaining references to old paths
   - Verify build still works after import updates

5. Remove dead code
   - Check for unused functions/variables with the analyzer script
   - Remove commented-out code older than current work

### Phase 5: Validation

Run whichever checks exist in the project:

```bash
# Tests
npm test 2>/dev/null || bun test 2>/dev/null || pytest 2>/dev/null || echo "No test runner found"

# Type checking
npx tsc --noEmit 2>/dev/null || echo "TypeScript check skipped"

# Linting
npm run lint 2>/dev/null || npx eslint . 2>/dev/null || echo "No linter found"

# Build
npm run build 2>/dev/null || bun run build 2>/dev/null || echo "Build check skipped"
```

List manual verification needed for features that lack test coverage.

---

## Part 2: Code-Level Cleanup

Remove AI slop, fix code smells, and improve code quality at the file level.

### Triage Order
Work safety-critical issues first, style issues second. A SQL injection in production matters more than a naming convention — fix the things that can hurt users before fixing things that annoy developers.
- **Pass 1 (Safety):** SQL injection, unhandled errors, race conditions, auth bypasses, data leaks
- **Pass 2 (Quality):** Naming, formatting, dead code, comments, code smells

Complete all Pass 1 fixes and verify tests pass before starting Pass 2. Mixing passes makes it hard to isolate whether a test failure came from a safety fix or a style change.

### Workflow

1. Determine scope:
   - PR cleanup → `git diff main --name-only` to get changed files
   - Specific files → user-specified targets
   - Whole codebase → scan all source files
2. For each file, read the surrounding code to understand existing style
3. Make edits to remove identified issues
4. Report a 1-3 sentence summary of changes

### AI Slop Patterns

**Comments to remove:**
- Obvious/redundant comments explaining what code clearly does
- Comments that don't match the commenting style elsewhere in the file
- Section divider comments when not used elsewhere

**Defensive code to remove:**
- Try/catch blocks around code that doesn't throw or is already in a trusted path
- Null/undefined checks when callers guarantee valid input
- Type guards that duplicate earlier validation
- Redundant error handling when parent functions already handle it

**Type issues to fix:**
- Casts to `any` that bypass TypeScript's type system
- Type assertions that hide real type mismatches
- Overly broad generic types when specific types exist

**Style inconsistencies:**
- Naming conventions that differ from the file
- Spacing/formatting patterns that differ from the file
- Import organization that differs from the file

### Code Smells — When to Act

Don't fix smells for their own sake. Fix them when the code is actively being worked on and the smell makes the change harder.

| Smell | Act when... | Leave alone when... |
|---|---|---|
| Long method (>30 lines) | Modifying part of it requires hunting for the right section | It's a straightforward sequential pipeline |
| Duplicated code | 3+ exact copies exist and one needs a change | 2 copies with different evolution paths |
| Long parameter list (>4 params) | The function is called from many places | It's an internal helper called once |
| Magic numbers | The value's meaning isn't obvious from context | It's a well-known constant (0, 1, -1, 100) |
| Nested conditionals (3+ levels) | Adding another branch requires tracing deep nesting | The nesting maps to domain logic clearly |
| Dead code | Always remove. Version control has the history. | — |
| Primitive obsession | Invalid values cause bugs (e.g., negative userId) | The domain is simple and won't grow |

---

## Part 3: Refactoring

Changing internal structure without changing external behavior.

### When NOT to Refactor

- **No test coverage** — You can't verify behavior is preserved. Write tests first.
- **Tight deadline** — Ship first, refactor later.
- **Code that won't change again** — If nobody will read or modify it, the investment doesn't pay off.
- **During a feature change** — Separate commits. Always.

### Phased Execution Order

When refactoring touches multiple files, follow this order to minimize breakage:

1. **Types/interfaces first** — Update or create types that define the new structure
2. **Implementation** — Refactor the actual logic to match new types
3. **Tests** — Update tests to match new structure, verify they pass
4. **Cleanup** — Remove old code, dead imports, unused types

### Dependency Tracking

For multi-file refactors, map dependencies before starting:
- Which files does this change affect?
- What blocks what? (e.g., "updating the API response type blocks the frontend component")
- What can be done in parallel?

### Pattern Refactoring

Apply design patterns only when the code has a concrete problem — not prophylactically.

**Strategy pattern** — When a conditional selects between 3+ distinct behaviors, each more than a few lines, and new behaviors are likely to be added.

**Chain of Responsibility** — When multiple checks run in sequence, each may short-circuit, and new checks are frequently added.

**Extract Method** — When a block has a clear single purpose and the method name would explain intent better than a comment. The most common and safest refactor.

---

## Common Pitfalls

- Moving files breaks dynamic imports (check for `require()` with variables, `import()`)
- Barrel files (index.ts re-exports) can hide dependency issues
- CSS/SCSS imports may use relative paths
- Asset paths in code may be hardcoded
- Environment-specific configs might reference paths
- Removing "unused" code that's actually used via reflection, dynamic imports, or string-based lookups
- Renaming a widely-used symbol without IDE support leaves broken references

---

## Worked Example

**User:** "Clean up this Express API project, it's gotten messy after 6 months of fast iteration."

**Step 1 — Structural scan:** Found 4 unused files in `/utils`, 2 duplicate helper modules, inconsistent naming (`userController.js` vs `product-controller.js`).

**Step 2 — Code-level:** Removed 12 `// TODO: fix later` comments with no context, 3 console.log statements, 2 commented-out code blocks (>50 lines each).

**Step 3 — Refactoring:** Extracted shared validation logic from 3 controllers into `middleware/validate.js`. Normalized file naming to kebab-case.

**Step 4 — Validation:** `bun test` — 47/47 passing. `tsc --noEmit` — clean. No behavioral changes.

**Artifact saved to `.agents/cleanup-report.md`.**

---

## Anti-Patterns

- **Behavioral changes disguised as cleanup** — if the observable output changes, it's not cleanup. Refactoring means same behavior, different structure.
- **"Tests pass so it's fine"** — passing tests don't guarantee behavioral equivalence if test coverage is incomplete. Flag uncovered code for manual verification.
- **Combining cleanup with features** — one change at a time. Never sneak a feature change into a cleanup PR.

---

## Artifact Template

On re-run: rename existing artifact to `cleanup-report.v[N].md` and create new with incremented version.

```markdown
---
skill: code-cleanup
version: 1
date: {{today}}
status: complete
---

# Cleanup Report

## Scope
[Structural / Code-Level / Refactoring / All]
[Files or directories targeted]

## Changes Made

### Structural
- [File moves, deletions, reorganizations]

### Code-Level
- [AI slop removed, code smells fixed, dead code deleted]

### Refactoring
- [Patterns applied, extractions, restructuring]

## Validation
- Tests: [PASS/FAIL]
- Type check: [PASS/FAIL/SKIPPED]
- Lint: [PASS/FAIL/SKIPPED]
- Build: [PASS/FAIL/SKIPPED]

## Manual Verification Needed
- [Features lacking test coverage that need manual check]
```
