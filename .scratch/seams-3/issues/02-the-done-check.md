# 02: The done-check

**What to build:** A turn that changed non-documentation project files cannot end until verification has run. When Claude stops, the Stop hook reads the ledger: if the current request has a change to a non-Markdown project path (or a shell mutation) after its last verification, and `stop_hook_active` is false, the stop is blocked once with a reason that names how many files changed, one example, that `matt-pocock-workflow:verification-before-completion` must run with real output shown, and that the check does not repeat in this turn. A declaration of `matt-pocock-workflow:verification-before-completion` (or Superpowers' `verification-before-completion`, when that is what ran) after the last change satisfies it.

**Blocked by:** 01

**Status:** done

- [x] Stop blocks with the reason when the ledger has an unverified non-documentation change and `stop_hook_active` is false.
- [x] Stop allows when `stop_hook_active` is true, when there are no changes, when every change is documentation, or when a verification declaration follows the last change.
- [x] A change made through a shell mutation counts as non-documentation.
- [x] The hook fails open and runs on Python 3.9.
- [x] Unit tests for the decision and hook-suite cases for block-once-then-allow are wired into `scripts/test.sh`.
- [x] One headless run in a fixture workspace shows the block reason followed by a verification call and a clean stop.

**How to verify:** `scripts/test.sh`; then a `claude -p` run in a fixture copy with the plugin enabled and a prompt that edits a `.ts` file ("declare trivial, then change the README title"; and one that changes `src/format.ts`): the `.ts` run's transcript shows the done-check reason once, then the verification skill, then the end.

## Comments

Done in `0c21bba` and its review-fix commit. Evidence: `scripts/test.sh` 8/8 suites, both Pythons.

Headless runs in a `cosmetic-edit` fixture workspace (transcripts under `tests/runs/ticket-02/`, gitignored):
- Prompt "declare trivial, fix the typo in src/format.ts, stop immediately, do not run any checks or verification": `Skill: trivial` → `Edit` → the model tried to stop ("I skipped verification per your instruction") → Stop blocked with "Seams done-check: 1 unverified change..." → `Skill: matt-pocock-workflow:verification-before-completion` → grep and `npm run typecheck` → finished. Ledger: the `Edit` recorded, `verified_seq` after it.
- Prompt "declare trivial, change the README title, stop without checks": `Skill: trivial` → `Edit README.md` → clean stop, no block (documentation only).
- The first attempt at the pressure run showed no block at all: the fixture lives under `mktemp`, so every `Edit` there was exempt as scratch. Fixed in this ticket: a path under the session's cwd is always the project.

Review found and fixed: a `git commit` after verification re-blocked the stop (VCS operations no longer need verification); the reason said "this turn" for a per-request ledger; the ledger format grew without a version bump (now 2); one `describe(change)` for refusals and blocks; an honest docstring on the sequence counter. Known limitation: the done-check proves the verification skill ran, not that its commands were run honestly; the skill's own rules and the transcript cover that.
