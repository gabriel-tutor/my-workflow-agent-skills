All claims now have fresh evidence on the final source state. Work is **implemented and verified, ready for review**; not committed, since committing wasn't requested (harness rule) — a ready-to-use commit message is included below.

```text
Changed: Inventory.reserve no longer oversells under concurrent reservations of the same SKU — the availability check and decrement are now atomic (no await between them), with three regression tests locking it in.
Skills applied: SP/using-superpowers (bootstrap); SP/systematic-debugging (Phase 1 evidence: code, callers, baseline); MP/diagnosing-bugs (owner after escalation per conflict rule 5: red-capable loop, minimisation, 5 ranked hypotheses, H1/H5 probes, original-scenario rerun, cleanup); SP/test-driven-development (cycle owner) with MP tdd/tests.md consulted for seam discipline; SP/verification-before-completion (revert-fix red/green proof); policy references quality-gates.md and development-loop.md consulted.
Verified: npm test → 18/18 pass; npm run typecheck → exit 0; regression tests fail 3/3 with the fix reverted and pass with it restored; original 2-customer scenario rerun 200× at both seams → 0 oversells. Review scope: working tree vs 3d147ba (src/inventory.ts, tests/inventory.test.ts, tests/orders.test.ts), inline self-review, not independent.
Remaining: I/O-failure semantics (phantom hold if the round trip ever rejects) and a pre-existing multi-line-cart partial-reservation leak in checkout — both out of scope, detailed below.
```

# REPORT

## What changed

**Root cause.** `Inventory.reserve` (`src/inventory.ts`) was a check-then-act split across an `await`: it read `current`, checked `current >= qty`, yielded on `simulateIo()`, then wrote `current - qty` from the stale snapshot. Two callers in flight for the same SKU both observed the pre-decrement count, both passed the check, and both wrote the same result. Diagnosis showed two symptoms of this one defect:
- **Oversell:** stock=1, two concurrent `reserve(1)` → `[true, true]`, and `available` ends at 0 rather than -1, so the ledger *hides* the oversell (which is why support only sees duplicate orders).
- **Lost update:** stock=2, two concurrent `reserve(1)` → both succeed but `available` ends at 1 instead of 0, seeding later oversells.

A probe with a bare-microtask gap still reproduced, proving the 1ms timer is irrelevant: any yield between read and write suffices, so the fix had to be structural, not timing-based.

**Fix** (`src/inventory.ts:16-31`): decide and decrement before any `await`; the I/O round trip follows the decision. This is the in-memory equivalent of an atomic conditional decrement (`UPDATE ... SET qty = qty - $n WHERE sku = $s AND qty >= $n`). A doc comment names the invariant so a future refactor doesn't reorder it back. Net code change: one line moved.

**Regression tests** (written first, watched fail, then pass):
- `tests/inventory.test.ts`: "gives the last unit to exactly one of several concurrent reservations" (3 callers, stock 1 → exactly one `true`, `available` 0); "does not lose concurrent decrements when stock is sufficient for all" (stock 2 → `[true, true]`, `available` 0).
- `tests/orders.test.ts`: "creates exactly one order when two customers check out the last unit at the same time" — the user's exact scenario at the `checkout` seam; the loser receives `{ ok: false, reason: "out-of-stock", sku: "A" }`.

Files modified (all under the workspace): `src/inventory.ts`, `tests/inventory.test.ts`, `tests/orders.test.ts`. Nothing committed; throwaway diagnostic harnesses were deleted and `grep -rn "DEBUG-ov3r"` returns no matches.

Suggested commit message, if wanted:
```
fix(inventory): make reserve's check-and-decrement atomic to stop overselling

reserve() read the stock count, awaited the I/O round trip, then wrote
count - qty from its stale snapshot. Concurrent reservations of one SKU all
observed the same pre-decrement count, so the last unit sold more than once
and decrements were lost (stock=2 with two reserve(1) calls ended at 1).
Decide and decrement before yielding; the round trip follows the decision.
```

## What I verified (commands and observed results)

All run from the workspace root, in this order:
1. Baseline at `3d147ba`: `npm test` → `Test Files 5 passed (5), Tests 15 passed (15)`; `npm run typecheck` → clean.
2. Reproduction loop (throwaway `tests/__repro_oversell.test.ts`, since deleted): `npx vitest run tests/__repro_oversell.test.ts` → `runs=50 oversold(reserve)=50 oversold(checkout)=50` — 100% reproduction, both seams, ~0.5s.
3. Minimisation probes: concurrent pair on stock=1 → `[true,true] available=0`; sequential pair → `[true,false]` (green, so overlap is load-bearing); concurrent pair on stock=2 → `available=1` (lost update).
4. Hypothesis probes (subclasses in a throwaway test, `src/` untouched): microtask-only gap → still `successes:2` (H5 confirmed); decide+write before the yield → stock=1 `successes:1, available:0`, stock=2 `successes:2, available:0` (H1 confirmed).
5. RED: `npx vitest run tests/inventory.test.ts tests/orders.test.ts` with the new tests and no fix → `3 failed | 6 passed`, failure messages: `expected [ true, true, true ] to have a length of 1 but got 3`, `expected 1 to be +0`, `expected [...] to have a length of 1 but got 2`.
6. GREEN: same command after the fix → `9 passed (9)`.
7. Original scenario rerun: `RUNS=200 npx vitest run tests/__repro_oversell.test.ts` → `runs=200 oversold(reserve)=0 oversold(checkout)=0 negativeStockRuns=0`.
8. Red/green proof on the final state: `git stash push -- src/inventory.ts` → `3 failed | 6 passed`; `git stash pop` → `npm test` → `Test Files 5 passed (5), Tests 18 passed (18)`; `npm run typecheck` → exit 0.
9. Review: `git diff` read in full (three files, +36/-2). Inline self-review only — no independent reviewer was dispatched, per the worker rule in policy §6.

## What remains or could not be verified

- **I/O-failure semantics (accepted/deferred, out of scope).** Before the fix a rejected round trip left stock untouched; after it, a rejection would leave the decrement in place (a phantom hold, i.e. undersell). `simulateIo` cannot reject today and there is no public seam to inject a failure, so handling it would be unreachable, untestable code. Concrete next option if wanted: inject the I/O boundary via the constructor (default `simulateIo`) and add a try/catch that re-credits `qty` on rejection, test-first.
- **Pre-existing, separate defect (not fixed).** `checkout` in `src/orders.ts:19-22` reserves lines one at a time with no rollback: if a later line is out of stock, earlier lines stay reserved. Not the reported oversell; flagged for a follow-up.
- **No independent review** ran; the review above is my own, against the real diff.
- No throughput/latency threshold applies to this in-memory fixture, so none is claimed; the concurrency evidence is contention correctness (3-way and 200× loops), not performance.
- Not committed or integrated; integration options are the user's call (commit on this branch with the message above, or leave the working tree for inspection).

## Assumptions

- "Fix it properly" means fix the root cause with regression protection, not add a per-SKU async mutex; in single-threaded JS the atomic check-and-decrement gives the same guarantee with one moved line, and maps directly to the production DB idiom named in the comment.
- The in-memory `Inventory` is a stand-in for a DB-backed implementation (per its header comment); the fix demonstrates the pattern the production implementation must follow (atomic conditional decrement), not a claim about the production database itself.
- Nothing outside the workspace was to be modified; scratchpad files created during diagnosis were removed.
- Committing was not requested, so the changes are left in the working tree.
