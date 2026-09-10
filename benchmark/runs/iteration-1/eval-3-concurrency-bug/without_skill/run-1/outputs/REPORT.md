The investigation and fix are complete. Summary of what I found and did:

**The bug.** `Inventory.reserve` was a check-then-act split across an `await`. It snapshotted `current`, checked it, yielded to the event loop for the simulated DB round trip, then wrote `current - qty` from that stale snapshot. Two concurrent reservations for the same SKU both passed the check against the same undecremented value, both wrote the same result, and both returned `true`. Because each wrote its own stale `current - qty`, the ledger read `0` rather than going negative — which is why the oversell never showed up as an inventory discrepancy. The reproduction showed it's not an off-by-one: 20 concurrent reservations against a stock of 5 all succeeded.

**The fix.** Reservations are now serialized per SKU via a promise queue, so the check-and-decrement is an exclusive critical section even though it spans the I/O gap. This is the in-process analogue of a row lock. I chose this over "decrement before the await" or "re-check after the await" because those depend on there being no yield point between read and write — a property that holds for this in-memory map but not for the real database read the comment says this models, and one that any future `await` inside the section would silently break. The queue is per SKU (different SKUs don't block each other), survives a failing task (a rejected I/O releases the queue rather than wedging later reservations), and cleans up its map entry when a SKU goes idle.

# REPORT

## What changed

- `src/inventory.ts` — added a private `queues: Map<string, Promise<void>>` and a `serialized(sku, task)` helper. `reserve` now runs its existing check → I/O → decrement body inside `serialized`, so reservations of the same SKU execute one at a time in FIFO order. The class doc comment explains the race and notes that a production DB adapter must provide the same guarantee (atomic conditional decrement or `SELECT ... FOR UPDATE`) since an in-process lock does not cover multiple server instances. Public API and existing behavior are unchanged.
- `tests/inventory.test.ts` — four new tests: two racing reservations for the last unit (exactly one wins); 20 concurrent reservations against stock 5 (exactly 5 win, stock ends at 0); mixed quantities `[2, 2, 1]` against stock 3 (total reserved ≤ 3 and ledger equals stock minus reserved); a refused reservation does not block a later one for the same SKU (guards the queue machinery).
- `tests/orders.test.ts` — one new test: two `checkout` calls racing for the last unit yield exactly one order and one `{ ok: false, reason: "out-of-stock", sku: "A" }`, with stock at 0.

Nothing was committed; the working tree has the three modified files.

## What I verified

- Baseline: `npm test` → 15 passed (15); `npm run typecheck` → clean.
- Reproduction on unmodified code (scratchpad vitest file, outside the workspace): `Promise.all([reserve("A",1), reserve("A",1)])` with stock 1 → `[ true, true ]`, `available("A")` = 0; two racing `checkout` calls → both `ok: true` (`ord_1`, `ord_2`).
- Same repro against the fix → `[ true, false ]`; one `ok: true` order and one `out-of-stock` result; stock 0.
- New regression tests against the **baseline** `inventory.ts` (via `git stash push -- src/inventory.ts`, then `git stash pop`): `npx vitest run --reporter=verbose` → 4 failed / 16 passed. Failures: `expected [ true, true ] to have a length of 1 but got 2`; `expected [ true, true, ... ] to have a length of 5 but got 20`; `expected 5 to be less than or equal to 3`; `expected [ { ok: true ... }, ... ] to have a length of 1 but got 2`.
- Fixed code: `npx vitest run` run 10 consecutive times → 20 passed (20) every run (no flakiness with real timers). `npm run typecheck` → clean, exit 0.

## What remains / could not be verified

- The "failed task releases the queue" path in `serialized` is exercised only by reasoning, not by a test: `simulateIo` is a module-private function that never rejects and is not injectable, so a test cannot make a reservation throw without hacks. The code handles it (`run.then(noop, noop)` keeps the tail resolvable), but it is not covered.
- "Different SKUs don't block each other" is not asserted by a test, since doing so deterministically would require fake timers or timing assertions; it follows directly from the per-SKU keying of `queues`.
- Adjacent, out-of-scope defect I noticed but did not change: `checkout` in `src/orders.ts` reserves line by line and does not release earlier reservations when a later line fails, so a multi-line cart that fails on line 2 leaks line 1's stock (an under-sell, not an oversell). Also `setStock` is synchronous and unlocked, so an admin restock issued while a reservation is mid-I/O would be overwritten by that reservation's write. Both are separate from the reported bug and worth their own tickets.

## Assumptions

- "Fix it properly" means making check-and-decrement atomic per SKU across the I/O gap, plus a regression test that reproduces the race — not a re-check-after-await band-aid.
- Serializing same-SKU reservations (throughput bounded by I/O latency under contention for one SKU) is acceptable, since that is the semantic a row lock imposes in production anyway; reservations for other SKUs are unaffected.
- FIFO ordering among queued reservations is a reasonable first-come-first-served semantic, but I asserted only the no-oversell invariant in the mixed-quantity test rather than the exact order, so a deliberate change of policy would not break the test.
- The in-memory `Inventory` is a stand-in for a DB-backed implementation; I documented (rather than implemented) that the real adapter must use an atomic conditional decrement or a row lock, since a process-local lock cannot protect against a second app instance.
