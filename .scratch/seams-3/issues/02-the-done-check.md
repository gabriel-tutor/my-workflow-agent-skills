# 02: The done-check

**What to build:** A turn that changed non-documentation project files cannot end until verification has run. When Claude stops, the Stop hook reads the ledger: if the current request has a change to a non-Markdown project path (or a shell mutation) after its last verification, and `stop_hook_active` is false, the stop is blocked once with a reason that names how many files changed, one example, that `matt-pocock-workflow:verification-before-completion` must run with real output shown, and that the check does not repeat in this turn. A declaration of `matt-pocock-workflow:verification-before-completion` (or Superpowers' `verification-before-completion`, when that is what ran) after the last change satisfies it.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] Stop blocks with the reason when the ledger has an unverified non-documentation change and `stop_hook_active` is false.
- [ ] Stop allows when `stop_hook_active` is true, when there are no changes, when every change is documentation, or when a verification declaration follows the last change.
- [ ] A change made through a shell mutation counts as non-documentation.
- [ ] The hook fails open and runs on Python 3.9.
- [ ] Unit tests for the decision and hook-suite cases for block-once-then-allow are wired into `scripts/test.sh`.
- [ ] One headless run in a fixture workspace shows the block reason followed by a verification call and a clean stop.

**How to verify:** `scripts/test.sh`; then a `claude -p` run in a fixture copy with the plugin enabled and a prompt that edits a `.ts` file ("declare trivial, then change the README title"; and one that changes `src/format.ts`): the `.ts` run's transcript shows the done-check reason once, then the verification skill, then the end.
