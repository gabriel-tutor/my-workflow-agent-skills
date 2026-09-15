# Changelog

## 2.1.2 — 2026-09-14
- `scripts/install.sh`: one command installs everything on a new machine (Matt Pocock's skills via skills.sh, the marketplace from GitHub, the plugin, the Read permission rules with the resolved skills path, an optional Superpowers disable). Safe to re-run; backs up settings first. Tested in a fixture home (`scripts/tests/test_install.sh`) and by a real GitHub install into a fresh config directory.
- The bootstrap is 100 bytes under budget even with a long plugin-cache path.
- The repo is named Seams (`gabriel-tutor/seams`). The plugin id `matt-pocock-workflow` and the marketplace name `my-workflow-agent-skills` are unchanged, so existing installs are unaffected.
- README: a "Try it in 60 seconds" block, three flow graphs, a case study of one feature end to end on a real repo (`docs/case-study-web-downloader.md`), and five carousel slides (`docs/carousel/`).

## 2.1.1 — 2026-09-14
Two fixes from the first real ticket run through 2.1 (web-downloader, exact resume, ticket 01).
- The bootstrap says unmarked skill names are Matt Pocock's and take no prefix. `implement` had tried `matt-pocock-workflow:code-review` first, got "Unknown skill", then fell back to the bare name.
- `implement`'s handover names its four sections as required headings and says the message is not finished until "Next" is written. The first real handover had Run it, Try it and What changed, and dropped Next.

## 2.1.0 — 2026-09-13
The senior-engineer layer: the rigor around Matt Pocock's method that neither collection carried.
- `grill` checks a **design lens** (`references/design-lens.md`) before calling the frontier empty: data model, interfaces and seams, failure modes, scale, security boundaries, observability, migration and rollout, testing strategy, operability, cost and reversibility. Scaled by path.
- `to-spec` adds alternatives considered, risks and failure modes, rollout and migration, and observability under Further Notes, from what the grill settled.
- `to-tickets` gives every ticket a **How to verify** line: the command or steps that prove its acceptance criteria.
- `implement` ends with a **definition of done** (seam and full-suite tests, typecheck and lint, every acceptance criterion, no debug leftovers, docs, commit message) and a four-part **handover**: run it, try it, what changed, next. The `/clear` decision lives here now, not in the bootstrap.
- New `foundations` skill: surveys a repo for run and verify commands, lint, pre-commit hooks, CI, glossary, issue-tracker config, boundary rules and `.env.example`; reports the gaps scaled to the repo's size; offers to close each through `/setup-matt-pocock-skills`, `setup-pre-commit` and `setup-ts-deep-modules`. Writes nothing without a yes. The bootstrap's setup nudge now points at it.
- Behavior-tested headless: `foundations` 3/3 (correct survey, zero writes), `to-tickets` 9/9 tickets with verify lines, `implement` 3/3 handovers with all four parts.

## 2.0.1 — 2026-09-12
- `to-spec`: when the grill already agreed the test seams, the spec records them instead of asking again. Matt Pocock's `to-spec` asks; the bootstrap says seams are settled in the grill.
- The hook takes its root from `CLAUDE_PLUGIN_ROOT`, so a plugin installed from a local directory points at its own reference files.
- Tested with Superpowers enabled alongside: Matt Pocock's skills still win every overlap (`docs/plugin-behavior-tests.md`).

## 2.0.0 — 2026-09-12
- A Claude Code plugin under `plugin/`, installed from this repo's own marketplace (`.claude-plugin/marketplace.json`). Matt Pocock's skills lead every stage.
- `hooks/session-start`: a SessionStart bootstrap (`startup|clear|compact`) that injects `using-matt-pocock-skills` plus two per-session lines: where Matt Pocock's skill files are, and a setup nudge when the repo has no issue-tracker config. Fails open; ≤ 3,000 bytes.
- `using-matt-pocock-skills`: the routing table (trivial, bug, bounded change, one-session feature, multi-session build, user-only on-ramps), stage owners, red flags and rules, with `references/routing.md` for phase boundaries and on-ramps.
- `grill`: Matt Pocock's grilling method presented one question per turn (facts first, recommended option first, remaining frontier as a count).
- `to-spec`, `to-tickets`, `implement`: model-invocable pointers that let Claude chain into Matt Pocock's user-only flow skills, each gated (asks before starting and before publishing) and each reading his `SKILL.md` at runtime rather than forking it.
- Unmodified copies of Superpowers 6.3.0 `using-git-worktrees`, `verification-before-completion`, `finishing-a-development-branch` and `receiving-code-review`, pinned by checksum in `THIRD_PARTY_NOTICES.md`, so the Superpowers plugin can stay disabled.
- `scripts/behavior_test.py` and `docs/plugin-behavior-tests.md`: headless RED-GREEN tests of the routing (5 runs per arm per scenario); every scenario at 5/5 on the shipped wording.
