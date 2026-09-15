# 07: Bootstrap 3.0

**What to build:** The routing policy routes by size and by risk, states the gate, and stays within budget. The table gains `trivial`* for trivial changes, a Sensitive row (auth, permissions, secrets, billing, migrations, infrastructure/CI/deploy config, public API, destructive operations; any size → `grill`* with the security and failure axes, then `tdd`, `code-review` required), `incident`* for a live outage, "several sessions or a new app" (new app: walking skeleton first), and `release`* for shipping. One sentence states that a hook refuses project changes until a skill has been invoked for the request and that verification must follow every change. Rule 4 adds that a yes covering later steps is not asked again while deploy and publish always ask. The Superpowers-overlap sentence and the worktree/review-feedback owners move to `routing.md`, which also gains the judgment rule for phase boundaries (no token figure), the named durable state (spec, tickets, `CONTEXT.md`, ADRs; a resumed ticket reads them), evidence reuse for an unchanged candidate, and the greenfield path. The injected bootstrap is at most 3,000 bytes with a cache-length plugin path and at least 100 bytes of headroom.

**Blocked by:** 01, 04, 05, 06

**Status:** ready-for-agent

- [ ] The table has the rows above and every Seams skill (`trivial`, `grill`, `foundations`, `to-spec`, `to-tickets`, `implement`, `release`, `incident`, the four Superpowers copies) is named in the bootstrap or in `routing.md`.
- [ ] The gate sentence and the authorization-reuse rule are present; the red flags still include "it's a quick fix" and "the requirements are clear".
- [ ] `routing.md` contains the moved sentences, the judgment rule, the durable-state rule, the evidence-reuse rule and the greenfield path; the string "150k" is gone.
- [ ] The hook suite injects the bootstrap with a 120-character plugin path and asserts ≤ 2,900 bytes; the static test asserts every Seams skill directory is named.
- [ ] The routing scenarios still route as expected in one headless run each (the full rerun belongs to ticket 10).

**How to verify:** `scripts/test.sh`; `wc -c` on the injected context from `echo '{"cwd":"'$PWD'"}' | CLAUDE_PLUGIN_ROOT=/a/b/... plugin/hooks/session-start` shows ≤ 2,900.

## Comments

Landed early, in ticket 03 (`fd311a1`): the Superpowers-overlap sentence moved from the bootstrap to `routing.md` (section "Alongside Superpowers", with one added sentence: the gate enforces the precedence because a Superpowers skill is not a declaration); rule 5 points at `routing.md` for the overlaps; the static test fails if the sentence returns to the bootstrap. The worktree and review-feedback owners are still in the bootstrap. Budget numbers to plan the trim: on a real home the injection is 2,619 bytes installed at this machine's 93-character cache path; partial install plus the setup nudge is 2,962 at 93 characters and 2,996 at 127. The hook suite's partial fixture (grilling alone, eight names, on an ~88-character temp path) measures 2,977 at the repo path and about 3,050 at a 120-character path, so ≤ 2,900 there needs roughly 150 bytes off the body, or a realistic partial fixture (two missing names), or a cap on the names listed.
