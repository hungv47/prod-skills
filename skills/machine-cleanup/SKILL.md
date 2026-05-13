---
name: machine-cleanup
description: "Audits and cleans a developer's machine — dotfolders, caches, language toolchains, and package-manager globals — with per-target classification, risk surfacing (auth, running processes, side effects), and explicit user confirmation before each deletion. Produces `skills-resources/meta/records/machine-cleanup-*.md`. Not for cleaning code (use code-cleanup) or for triaging user files in Documents/Downloads (those need human review)."
argument-hint: "[target: home | caches | runtimes | packages | all]"
allowed-tools: Read Grep Glob Bash
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
  budget: deep
  estimated-cost: "$1-3"
promptSignals:
  phrases:
    - "clean up my machine"
    - "clean my home directory"
    - "free up disk space"
    - "fresh start dev machine"
    - "what's taking up space"
    - "review every folder"
    - "remove abandoned tools"
    - "audit my dotfolders"
    - "uninstall what i don't use"
  allOf:
    - [clean, home]
    - [free, disk]
    - [audit, machine]
  anyOf:
    - "home directory"
    - "dotfolder"
    - "dotfile"
    - "disk space"
    - "uninstall"
    - "abandoned tools"
    - "fresh start"
    - "machine cleanup"
  noneOf:
    - "code review"
    - "refactor"
    - "documentation"
  minScore: 6
routing:
  intent-tags:
    - machine-cleanup
    - dotfolder-audit
    - cache-purge
    - package-prune
    - toolchain-removal
    - disk-reclaim
    - dev-machine-hygiene
  position: horizontal
  lifecycle: snapshot
  produces:
    - skills-resources/meta/records/machine-cleanup-*.md
  consumes: []
  requires: []
  defers-to:
    - skill: code-cleanup
      when: "cleaning source code, not machine state"
  parallel-with: []
  interactive: true
  estimated-complexity: heavy
---

# Machine Cleanup — Orchestrator

*Productivity — Multi-agent orchestration. Audits a developer's machine state and removes abandoned tools, orphaned caches, and unused toolchains — without breaking active workflows.*

**Core Question:** "Is this folder still owned by an installed tool I actively use, or is it leftover state from something I no longer have?"

## Inputs Required
- A machine to audit (the user's `$HOME` and adjacent state)
- User intent: full audit, caches only, runtimes only, package globals only, or specific folder

## Output
- `skills-resources/meta/records/machine-cleanup-*.md`

## Chain Position
Previous: none | Next: none (standalone)

**Re-run triggers:** New laptop setup, after trying many AI tools you've now abandoned, when disk is full, before passing the machine to someone else.

---

## Pre-Dispatch

Run the Pre-Dispatch protocol (`meta-skills/references/pre-dispatch-protocol.md`).

**Needed dimensions:** scope (dotfolders / caches / packages / runtimes / all), aggressiveness (conservative / moderate / aggressive), excluded paths.

**Read order:**
1. Machine scan: `du -sh ~/.*`, `df -h`, package globals (npm/brew/bun/cargo/go/pipx).
2. Experience: `skills-resources/experience/technical.md` for prior protected-paths list.

**Warm Start** (scope clear from invocation, e.g., "clean my caches"):

```
Found:
- scope → "[caches / dotfolders / etc.]"
- detected disk pressure → "[GB used in target scope]"

Aggressiveness defaults to moderate (suggests but asks before destructive deletes).
Override or proceed?
```

**Cold Start** (general "clean my machine"):

```
machine-cleanup audits dotfolders, caches, package globals, and toolchains
to remove abandoned state without breaking active workflows. Before I scan:

1. **Scope** — pick one or more:
   - dotfolders (~/.foo, ~/.bar — most common abandonment)
   - caches (~/.cache, ~/Library/Caches — usually safe to clear)
   - packages (npm/brew/bun/cargo/go/pipx globals)
   - runtimes (orphaned node/python versions)
   - all
2. **Aggressiveness** — conservative (skip anything ambiguous), moderate
   (default — propose with rationale, ask before destructive), aggressive
   (suggest more removals, more proactive flagging).
3. **Excluded paths** — anything off-limits even if it looks abandoned?
   (Project archives, encrypted vaults, in-progress experiments, etc.)

Answer 1-3 in one response. I'll inventory and propose.
```

**Write-back:**

| Q | File | Key |
|---|---|---|
| 3. Excluded paths | `technical.md` | `Technical — machine-cleanup excluded paths` (durable across runs) |

Scope + aggressiveness are run-specific.

---

## Multi-Agent Architecture

### Agent Roster

| Agent | File | Focus |
|---|---|---|
| dotfolder-scanner-agent | `agents/dotfolder-scanner-agent.md` | `$HOME/.*` survey — identify owning tool, classify (active/abandoned/orphan/empty), flag auth state |
| runtime-scanner-agent | `agents/runtime-scanner-agent.md` | Language toolchains — `.rustup`, `.cargo`, `go/`, `google-cloud-sdk/`, etc. — and whether the user actively writes that language |
| cache-scanner-agent | `agents/cache-scanner-agent.md` | XDG `.cache/`, `.npm/_cacache`, `.bun/install/cache`, `.cargo/registry` — pure regenerable reclaim |
| package-inventory-agent | `agents/package-inventory-agent.md` | Globals across npm/brew/bun/cargo/go/pipx — flag duplicates (e.g., `codex` installed via 3 channels) and unused |
| orphan-detection-agent | `agents/orphan-detection-agent.md` | Cross-references findings — sibling folders left behind when a tool is removed (`.cache/codex-runtimes` after `.codex` is gone), broken symlinks, dangling shell-rc references |
| safe-nuke-agent | `agents/safe-nuke-agent.md` | Executes deletions — process-check first, fixes shell-rc side effects, verifies post-state |
| critic-agent | `agents/critic-agent.md` | Golden rules compliance, no user-data deletion, no auth surprise |

### Execution Layers

```
Layer 1 (parallel — survey only, no changes):
  dotfolder-scanner-agent ────┐
  runtime-scanner-agent ──────┤── scan simultaneously
  cache-scanner-agent ────────┤
  package-inventory-agent ────┘

Layer 2 (sequential — analysis):
  orphan-detection-agent ─────── correlates Layer 1 outputs

Layer 3 (interactive — execution):
  safe-nuke-agent ──────────── per-target: surface findings → confirm with user → execute
    → critic-agent ───────────── final golden rules review
```

### Dispatch Protocol

1. **Triage** — determine scope from user intent (see Routing Rules below).
2. **Layer 1 dispatch** — send brief to relevant scanner agents in parallel. Each returns a markdown report with classified targets.
3. **Layer 2 orphan correlation** — `orphan-detection-agent` cross-references Layer 1 outputs. Emits a unified "candidates for removal" list with confidence levels.
4. **Layer 3 interactive execution** — `safe-nuke-agent` walks the candidate list **one target at a time**:
   - Surface what it is, why it's a candidate, what user loses if removed (auth re-login, settings, data)
   - Surface risks (running processes, shell-rc references, irreversible data)
   - Recommend with reasoning
   - **Wait for explicit user confirmation** for that target
   - Execute with side-effect fixes
   - Track reclaim
5. **Critic review** — `critic-agent` checks golden rules. If FAIL, restore from backup and report.
6. **Assembly** — compile report. Save to `skills-resources/meta/records/machine-cleanup-*.md`.

### Routing Rules

| Condition | Route |
|-----------|-------|
| User says "clean my home dir" | dotfolder-scanner → orphan-detection → safe-nuke → critic |
| User says "free up disk space" | cache-scanner + dotfolder-scanner → orphan-detection → safe-nuke → critic |
| User says "audit my globals" / "package cleanup" | package-inventory only → safe-nuke → critic |
| User says "remove unused languages" | runtime-scanner → safe-nuke → critic |
| User says "fresh start" / "clean everything" | All four scanners → orphan-detection → safe-nuke → critic |
| User points at a specific folder | Skip Layer 1 broad scan; safe-nuke runs against that folder's classification |
| Critic FAIL | Restore last backup, surface what was wrong, ask user how to proceed |
| Session reclaim >10GB | Generate interim summary, ask if user wants to continue |

---

## Critical Gates (The 6 Golden Rules)

Before delivering, the critic-agent verifies ALL golden rules pass:

1. **Never delete user data without explicit confirmation.** User files in `Desktop/`, `Documents/`, `Downloads/`, `Pictures/`, `Movies/`, `Music/`, `Public/` and any contents under cloud-mount symlinks (`Google Drive`, `OneDrive`, `iCloud`) are off-limits to bulk action. Surface findings; defer execution to the user.
2. **No auth surprise.** Any folder containing tokens, OAuth state, refresh tokens, JWTs, session cookies, or PKCE artifacts must be flagged BEFORE deletion with the exact re-auth command the user will need (`gh auth login`, `gcloud auth login`, `vercel login`, etc.).
3. **Process-check before nuking active state.** If a folder is being written to right now (mtime within 5 minutes, or a `.pid`/`.sock`/`-wal` file exists), check `pgrep` for the owning app. Quit cleanly via AppleScript or warn the user before deletion. Never delete files an open SQLite WAL points to.
4. **Side-effect awareness in shell startup.** Before deleting a directory referenced in `.zshenv`, `.zshrc`, `.bashrc`, `.profile`, `.tcshrc`, etc. (e.g., `. "$HOME/.cargo/env"`), comment out or update the offending line. Otherwise every new terminal will throw errors.
5. **Distinguish regenerable cache from unique state.** Anything inside an XDG-compliant `~/.cache/` is throwaway by definition — surface it for fast nuke. Anything outside `~/.cache/` requires per-target classification: identify the owning tool, then decide.
6. **One target at a time with explicit confirmation.** No bulk multi-target deletion. The user must confirm each target by name (or pick from a coded list). Track cumulative reclaim across targets.

**Additional gate:** Session limits — target ~25 deletions per cleanup session. After 10, generate an interim summary. If the user has rejected 5+ recommendations in a row, stop and ask if the scope is wrong.

**If any golden rule fails:** the critic identifies the specific deletion that violated it, the safe-nuke-agent restores from backup (or instructs reinstall steps if backup isn't possible), and reports.

---

## Single-Agent Fallback

When context window is constrained or the cleanup target is a single folder:

1. Skip multi-agent dispatch.
2. Inspect the target — list contents, sizes, last-modified, identify owning tool.
3. Classify (active / abandoned / orphan / cache / load-bearing).
4. Surface auth/process/side-effect risks.
5. Recommend nuke or keep, with reasoning.
6. Wait for explicit user confirmation.
7. Execute with side-effect fixes.
8. Verify post-state.
9. Save to `skills-resources/meta/records/machine-cleanup-*.md`.

---

## Triage

Determine scope before starting. Parts can be used independently or combined.

| User intent | Scanners to dispatch |
|---|---|
| "Clean my home directory" | dotfolder-scanner-agent |
| "What's taking up disk space?" | cache-scanner-agent + dotfolder-scanner-agent |
| "Audit my npm/brew globals" | package-inventory-agent |
| "Remove unused language toolchains" | runtime-scanner-agent |
| "Fresh start" / "review every folder" | All four scanners |
| User points at one specific folder | Skip Layer 1 scan; single-agent fallback |

---

## Classification Vocabulary

Every target gets one classification. The `safe-nuke-agent` uses these to phrase its recommendation.

| Class | Meaning | Default recommendation |
|---|---|---|
| **active** | Tool is installed AND used recently (mtime <30d, or process running, or referenced from current session) | Keep |
| **load-bearing** | Active and contains unique state (auth, settings, history) — not regenerable | Keep with strong push-back |
| **abandoned** | Tool may be installed but folder hasn't been touched in 30+ days; no recent process activity | Recommend nuke; explain what user loses |
| **orphan** | Owning tool was already removed (CLI not on PATH, app not in `/Applications`, sibling folder gone) | Strong recommend nuke |
| **cache** | Pure regenerable cache (inside `~/.cache/`, or named `cache/`/`_cacache/`) | Recommend nuke without ceremony |
| **empty** | 0-byte directory or only contains `.DS_Store` | Auto-suggest nuke |
| **user-data** | Contains user-created content (recordings, documents, captures) | Never auto-recommend nuke; surface only |

---

## Tool Ownership Heuristics

Don't trust folder names alone. Identify the *owning tool* before classifying:

| Folder pattern | Likely owner | Verification |
|---|---|---|
| `.<toolname>/` | The tool literally named `toolname` | Check if `<toolname>` is on PATH (`which`), in `/Applications`, or in brew/npm/bun/cargo/go global lists |
| `.cache/<toolname>/` | XDG cache for `<toolname>` | If owning tool is gone → orphan |
| `.config/<toolname>/` | XDG config — usually load-bearing | Check for credentials/tokens; preserve unless tool is verifiably gone |
| `.<toolname>-<suffix>` (e.g., `.amazon-q.dotfiles.bak`) | Backup or auxiliary state | Almost always orphan/cruft |
| Folders named `bin`, `tmp`, `cache`, `logs`, `sessions` inside a tool dir | Tool's working dirs | Subordinate to parent's classification |

**Cross-reference signals:**
- Look for `*.pid` and `*.sock` files → check if PID is alive
- Look for SQLite `-wal` files → process is currently writing
- Compare folder mtime to today's date → recency proxy
- Read top-level config files → identify the tool by self-description, not just folder name

See `references/tool-ownership-map.md` for known tools and their footprints.

---

## Anti-Patterns

| Anti-Pattern | Problem | INSTEAD |
|--------------|---------|---------|
| "It's a dotfolder, must be safe to nuke" | Some dotfolders contain auth tokens, session DBs, or active SQLite | Inspect contents and mtime before classifying |
| Bulk-deleting all of `~/.*` | Loses SSH keys, AWS creds, gcloud auth, MCP server auth | Per-target review only |
| Treating `~/.config/<tool>/` like cache | XDG config = load-bearing settings, not throwaway | Classify as `load-bearing` by default; require justification to nuke |
| Nuking while the app is running | Corrupts SQLite, crashes the app, may lose unsaved data | `pgrep` check + clean quit via AppleScript first |
| "I'll just `rm -rf` and tools will recreate it" | Some tools (Codex, Snaply) write encrypted state that doesn't restore on relaunch | Surface what re-login/re-config will be needed |
| Forgetting shell rc side effects | Nuking `.cargo/env` leaves `.zshenv` throwing on every new shell | Update shell rc files in same operation |
| Conflating "old" with "abandoned" | Some load-bearing files (auth tokens, gitconfig) are old by design | Age is one signal, not a verdict |
| Nuking the package manager but keeping its data | Nuking `.cargo` while keeping `~/.rustup` leaves dangling rustup proxies | Treat the runtime as a unit |

---

## Worked Example

**User:** "I've tried 20 AI coding tools this year. Most of them I never use anymore. Clean up my machine."

**Triage:** Broad cleanup — dispatch all four scanners.

**Layer 1 (parallel):**
- `dotfolder-scanner-agent` →
  - 28 dotfolders surveyed
  - **Active (4):** `.claude` `.codex` `.cursor` `.warp`
  - **Load-bearing (5):** `.aws` `.ssh` `.config` `.context7` `.mcp-auth`
  - **Abandoned (12):** `.factory` `.t3` `.kimi` `.kiro` `.windsurf` `.trae` `.codeium` `.snaply` `.pencil` `.browser-use` `.amazon-q.dotfiles.bak` `.antigravity`
  - **Orphan (3):** `.kimi-webbridge` (sibling `.kimi` already deleted), `.semantic_search` (Kiro's model cache), `.icube-remote-ssh` (empty)
  - **Empty (2):** `.kilocode` (0B), `.icube-remote-ssh` (0B)
- `runtime-scanner-agent` →
  - Rust: installed but `cargo install --list` empty + 0 user crates → **toolchain unused**, ~1.5G across `.cargo` + `.rustup`
  - Go: installed (Homebrew), `go/bin/` only contains `dlv` + `gopls` (IDE tooling) → **abandoned for personal use**
  - Google Cloud SDK: 400M curl-pipe-installed, plus 84M auth in `.config/gcloud` → **decision: do you still ship to GCP?**
- `cache-scanner-agent` →
  - `.cache/huggingface` 5.5G — model files for tools that are now abandoned (Kiro, semantic_search) → **orphan cache**
  - `.cache/codex-runtimes` 732M — paired with `.codex` (active) → **regenerable, lower priority**
  - `.npm/_cacache` 604M + `.npm/_npx` 405M → **pure regenerable**
- `package-inventory-agent` →
  - `@openai/codex` installed via 3 channels: brew formula, brew cask (`codexbar`), bun global → **2 redundant copies**
  - `agent-browser` npm-global → still installed even though `.agent-browser/` was nuked; will redownload 700M Chromium on next run

**Layer 2 (sequential):**
- `orphan-detection-agent` → cross-correlates:
  - `.cache/snaply` is orphaned by abandoned `.snaply`
  - `.cache/opencode` is orphaned (no `.opencode/` exists)
  - `.config/browseruse` is orphaned (`.browser-use/` already gone)
  - `.zshenv` references `.cargo/env` — if user nukes `.cargo`, the source line breaks
  - `~/Library/Application Support/snaply` is the *real* user data dir for Snaply (`.snaply/` is auxiliary) — surface separately

**Layer 3 (interactive — `safe-nuke-agent`):**

Walks the candidate list one at a time. For each target:
- Shows: what it is, owner tool, status, contents summary, recommendation
- Surfaces: auth files, running processes, dependent shell-rc lines
- Awaits explicit user confirmation
- Executes with side-effect fixes (e.g., comments out `.cargo/env` line in `.zshenv` before deleting `.cargo`)

**Critic review:** PASS. All 6 golden rules satisfied. No user data touched. All auth surprises were surfaced. Shell rc fixed inline.

**Artifact saved to `skills-resources/meta/records/machine-cleanup-*.md`.**

---

## Artifact Template

On re-run: rename existing artifact to `machine-cleanup-report.v[N].md` and create new with incremented version.

```markdown
---
skill: machine-cleanup
version: 1
date: {{today}}
status: done | done_with_concerns | blocked | needs_context
total_reclaimed: "X.X GB"
---

# Machine Cleanup Report

## Scope
[Home / Caches / Runtimes / Packages / All]

## Summary
- Targets surveyed: N
- Targets nuked: N
- Targets kept: N
- Total disk reclaimed: X.X GB
- Auth re-logins required: [list]
- Reinstall commands queued: [list]

## Targets Nuked
| # | Path | Class | Size | Owner | User loses |
|---|------|-------|------|-------|------------|
| 1 | ~/.foo | abandoned | 200M | foo-cli (uninstalled) | nothing |
...

## Targets Kept
| # | Path | Class | Reason |
|---|------|-------|--------|
| 1 | ~/.aws | load-bearing | AWS credentials |
...

## Side Effects Fixed
- ~/.zshenv: commented out `. "$HOME/.cargo/env"` (target nuked)
- ...

## Re-Auth Commands
After this cleanup, the following tools will need re-authentication:
- `gh auth login` (nuked ~/.config/gh)
- ...

## Manual Follow-ups
[Anything the user opted to defer — usually user-data dirs they want to triage themselves]
```

## Next Step

If the user asks "what package managers should I prune next," dispatch `package-inventory-agent` standalone.
If the user wants to dotfile-track the resulting clean state, suggest `chezmoi` or `dotbot`.

---

## Scripts

- `scripts/inventory.sh` — One-shot inventory script. Outputs:
  - Sizes + mtimes for every `~/.*` dotfolder
  - Package globals across npm/brew/bun/cargo/go/pipx
  - Running AI/dev processes
  - Broken symlinks under `$HOME`
  - Shell-rc files that source non-existent paths

  All four Layer 1 scanners share its output to avoid redundant `du`/`ls` runs.

---

## Completion Status

Every run ends with explicit status:
- **DONE** — all approved removals executed, totals reported (`total_reclaimed`), no orphaned references in shell-rcs
- **DONE_WITH_CONCERNS** — cleanup applied but some folders deferred to manual user triage (user-data dirs, ambiguous ownership); report enumerates what was deferred
- **BLOCKED** — destructive removal would touch user data without confirmation; halted pending explicit user decision
- **NEEDS_CONTEXT** — tool ownership unclear for some folders (no entry in tool-ownership-map.md and the user can't identify the owning tool); ask before removing

---

## References

- `references/tool-ownership-map.md` — Lookup table: folder pattern → owning tool → install method → known data dirs
- `references/auth-credential-patterns.md` — Filename patterns that indicate auth state (so the critic-agent can fail fast on auth-surprise)
