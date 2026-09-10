Work complete. Summary in the routing policy's format, then the orchestrator's `# REPORT`.

```text
Changed: Inventory.reserve no longer over-sells under concurrency — reservations
         for the same SKU are serialised through a per-SKU async lock; two
         regression tests added (reserve seam + checkout seam).
Skills applied: matt-pocock-workflow (routing), diagnosing-bugs (feedback loop,
         minimise, hypotheses, one probe, fix, cleanup), tdd (red-first
         regression tests at existing seams), code-review (Standards + Spec
         sub-agent reviews of the working tree vs 3d147ba; findings addressed).
Verified: npm test 17/17, npm run typecheck exit 0, both new tests red on the
         baseline and green on the fix, 100/100 rounds of the original scenario
         now yield exactly one order.
Remaining: two pre-existing adjacent defects flagged, not fixed (see report).
```

# REPORT

## What changed

Three files, uncommitted in the working tree (no commit was requested; diff is `git diff 3d147ba`, 49 insertions / 6 deletions):

- `src/inventory.ts` — **Root cause:** `reserve` was check-then-act across an `await`: it read `current`, checked it, awaited the simulated I/O, then wrote `current - qty`. Two concurrent callers both read `current = 1` before either wrote, so both returned `true`, and both wrote `1 - 1 = 0` — a lost update that leaves the ledger looking correct (stock 0, not -1), which is why support only hears about it from customers. **Fix:** a private `withSkuLock(sku, task)` serialises reservations per SKU (a FIFO promise queue with explicit acquire/release; entries are dropped when a SKU's queue drains), so each reservation's check → I/O → decrement completes before the next one for that SKU starts. This is the in-memory analogue of holding a row lock (`SELECT ... FOR UPDATE`) across the round trip the module says it models. The public interface (`reserve(sku, qty): Promise<boolean>`) is unchanged; the modelled I/O gap is retained; rejections from a task propagate to its caller and do not block later reservations. Doc comment updated to state the guarantee and that `setStock` is a setup call outside the lock.
- `tests/inventory.test.ts` — new test `does not over-sell when two reservations compete for the last unit` (two concurrent `reserve("A", 1)` on stock 1 → exactly one `true`, `available === 0`).
- `tests/orders.test.ts` — new test `gives the last unit to only one of two simultaneous checkouts` (the reported scenario at the `checkout` seam → one order, one `{ ok: false, reason: "out-of-stock", sku: "A" }`, stock 0).

Rejected alternatives: removing the I/O gap (defeats the module's stated purpose) and merely re-checking stock after the `await` (correct only while nothing else awaits between the check and the write; regresses silently on the next edit).

## What was verified (commands run in the workspace, observed results)

- Baseline before any change: `npm run typecheck` clean; `npm test` → 5 files, 15/15 passed.
- Diagnosis loop (throwaway `tests/oversell.repro.test.ts`, 100 rounds of two concurrent `checkout`s of the last unit): `npx vitest run tests/oversell.repro.test.ts` → **FAIL**, `rounds=100 bothSucceeded=100 negativeStock=0`.
- Minimisation (throwaway `tests/oversell.minimise.test.ts`): two concurrent `reserve("A",1)` on stock 1 → `[true,true] available=0` (red, `checkout` not load-bearing); sequential control → `[true,false]` (green, concurrency load-bearing); 3 callers on stock 2 → `[true,true,true] available=1`.
- One tagged probe (`[DEBUG-ovs1]`) confirmed hypothesis 1: log order `read current=1`, `read current=1`, `write 1-1=0`, `write 1-1=0 (stock now 0 before write)`. Probe removed; `grep -rn "DEBUG-" src tests` → none.
- TDD slice 1: `npx vitest run tests/inventory.test.ts` before the fix → `AssertionError: expected [ true, true ] to have a length of 1 but got 2`; after the fix → 4/4 passed.
- Slice 2 red-capability: `git stash push -- src/inventory.ts && npx vitest run tests/orders.test.ts` → `× gives the last unit to only one of two simultaneous checkouts ... to have a length of 1 but got 2`; after `git stash pop` → 4/4 passed. Repeated for both kept tests against the final code: 2 failed on baseline, 8/8 passed on fix.
- Rerun of the original un-minimised loop after the fix: `rounds=100 bothSucceeded=0 negativeStock=0`; 3 callers on stock 2 → `[true,true,false] available=0`.
- Code review (Matt Pocock `code-review`, working-tree adaptation: `git diff 3d147ba`, 0 commits, 0 untracked files): two independent sub-agent reviews run sequentially (not in parallel — my first parallel spawn was rejected by the harness). Standards: 0 documented-standard violations; judgement calls on naming (`serialised`/`pending`), duplicated cart literals in the test, and a swallowed-rejection nit. Spec: 0 missing requirements, 0 scope creep; reviewer's own probes confirmed mixed quantities, 20 callers on stock 5, independent SKUs, and interleaved checkouts are correct. All actionable findings were applied (rename to `withSkuLock`/`locks`, explicit acquire/release so rejections propagate as before, `noop` removed, comment tightened, single immutable cart in the test).
- Post-review verification on the final code (throwaway `tests/zz-throwaway-final-check.test.ts`, deleted afterwards): 100 rounds of the original scenario → assertion `bothSucceeded === 0` passed; `[reserve(A,2), reserve(A,2), reserve(A,1), reserve(B,1), reserve(B,1)]` on A=3, B=1 → `[true,false,true,true,false]`, both at 0; 20 callers on stock 5 → exactly 5 successes, stock 0; a throwing task → its caller sees `boom`, the next `reserve` resolves `true`, `locks.size === 0` after drain.
- Final state: `npm test` → 5 files, **17/17 passed** (137ms); `npm run typecheck` → **exit 0**; `git status --short` → only `M src/inventory.ts`, `M tests/inventory.test.ts`, `M tests/orders.test.ts`; `git stash list` empty; no `DEBUG-`/`REPRO-`/`THROWAWAY` markers in `src` or `tests`.

## What remains / could not be verified

- **Not fixed (pre-existing, out of the reported scope):** (1) `setStock` bypasses the lock — a restock landing during a reservation's I/O gap is overwritten by the stale `current - qty` write; (2) `checkout` reserves line-by-line and never releases earlier lines when a later line is out of stock, so two multi-line carts contending in opposite order can both fail while each holds a unit (under-sell, and `Inventory` has no release method). Both need a product/interface decision; recommend separate tickets.
- N concurrent reservations of one SKU now cost ~N sequential round trips instead of ~1 — inherent to the lock and consistent with the row-lock model.
- The post-review edits were verified by tests and probes but were not re-submitted for a second sub-agent review (the policy says not to chase zero findings indefinitely).
- Not committed. Suggested commit message: `fix(inventory): serialise reservations per SKU to stop over-selling — reserve read stock, awaited I/O, then wrote a stale decrement, so concurrent callers both saw the last unit (lost update). Reservations for a SKU now run as a critical section via a per-SKU async lock.`

## Assumptions

- Test seams: the existing public `Inventory.reserve` and `checkout` are the agreed seams (both were already the repo's test seams; no interface change was needed, so `codebase-design` was not invoked).
- Spec source: the user's request text plus the `Reservation`/over-selling definition in `CONTEXT.md`; no issue tracker (`docs/agents/issue-tracker.md`) or spec file exists, and none was required for this task.
- Review baseline: commit `3d147ba` (HEAD, the only commit), compared to the working tree.
- The in-memory `Inventory` is a model of a production database path, so the correct fix must preserve the asynchronous I/O gap rather than eliminate it.
- Who wins the last unit (first-come-first-served) is not specified; the tests assert only "exactly one succeeds", which is what `CONTEXT.md` defines as correct.
