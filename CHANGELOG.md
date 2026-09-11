# Changelog

## matt-pocock-workflow (plugin)

### 2.0.0 — 2026-09-12
- Rebuilt as a Claude Code plugin under `plugin/`, installed from this repo's own marketplace (`.claude-plugin/marketplace.json`). Matt Pocock's skills lead every stage; the v1 router skill and the combo router are now legacy.
- `hooks/session-start`: a SessionStart bootstrap (`startup|clear|compact`) that injects `using-matt-pocock-skills` plus two per-session lines: where Matt Pocock's skill files are, and a `/setup-matt-pocock-skills` nudge when the repo has no issue-tracker config. Fails open; ≤ 3,000 bytes.
- `using-matt-pocock-skills`: the routing table (trivial, bug, bounded change, one-session feature, multi-session build, user-only on-ramps), stage owners, red flags and rules, with `references/routing.md` for phase boundaries and on-ramps.
- `grill`: Matt Pocock's grilling method presented one question per turn (facts first, recommended option first, remaining frontier as a count).
- `to-spec`, `to-tickets`, `implement`: model-invocable pointers that let Claude chain into Matt Pocock's user-only flow skills, each gated (asks before starting and before publishing) and each reading his `SKILL.md` at runtime rather than forking it.
- Unmodified copies of Superpowers 6.3.0 `using-git-worktrees`, `verification-before-completion`, `finishing-a-development-branch` and `receiving-code-review`, pinned by checksum in `THIRD_PARTY_NOTICES.md`, so the Superpowers plugin can stay disabled.
- `scripts/behavior_test.py` and `docs/plugin-behavior-tests.md`: headless RED-GREEN tests of the routing (5 runs per arm per scenario); every scenario at 5/5 on the shipped wording.

## matt-pocock-superpowers-workflow

### 0.1.0 — 2026-09-11
- First version. Router + arbiter built from `sources/MATT-POCOCK-SUPERPOWERS-WORKFLOW.md`: ownership table (15 stages), 12 conflict rules, process sizing, development loop A–H, coordination rules, completion gates. References extracted verbatim.

## matt-pocock-workflow (v1 router skill, legacy)

### 1.1.0 — 2026-09-11
- Restructured for progressive disclosure: `SKILL.md` keeps policy, discovery, routing check, the scenario table, condensed workflow rules, and completion; catalog, full workflow rules, and examples moved to `references/`. Policy unchanged.
- Description rewritten as triggers only; cross-references the combo skill.
- Now lives in this repo and is installed by `scripts/activate.sh`.

### 1.0.0 — 2026-09-10
- `MATT-POCOCK-AGENT-INSTRUCTIONS.md` installed verbatim as `~/.claude/skills/matt-pocock-workflow/SKILL.md`. Archived as `sources/matt-pocock-workflow-v1.0.0.SKILL.md`.

## Benchmark

### Iteration 1 — 2026-09-11
- Six scenarios × three arms (combo / MP-only / no router) on Opus 5, graded objectively plus one LLM grader per run.
- Result: combo 35/35, MP-only 34/35, no router 32/35; token cost 21.8 M / 15.7 M / 3.7 M.
- Only the concurrency-bug and small-feature scenarios discriminated. See `benchmark/runs/iteration-1/analysis.md` and `benchmark.md`.

## Hooks

### 2026-09-11
- `scripts/hooks/session-start` — a `SessionStart` hook that injects the active router's policy
  into every session, so invocation no longer depends on the model noticing the skill. Mirrors the
  mechanism Superpowers uses for `using-superpowers`.
- Injects a ~450-token pointer rather than the 23 KB skill: Claude Code inlines only ~2 KB of hook
  context and writes the remainder to a file, which would have delivered a truncated preamble.
- `install.sh` / `uninstall.sh` merge and remove the entry without touching hooks you configured
  yourself; the original settings file is backed up to `settings.json.mpsw-backup`.
