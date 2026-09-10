# Transcript

## Prompt

<teammate-message teammate_id="team-lead" summary="bench concurrency-bug old_skill">
Execute this task in a benchmark sandbox.

Working directory: /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace
It is a git repository at a baseline commit. Your shell's working directory does not persist between Bash calls: prefix every command with `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace &&` or use absolute paths, and never run git/npm commands anywhere else.

Skill to apply: read /Users/gabrieltutor/my-agent-workflow-skills/skills/matt-pocock-workflow/SKILL.md first and follow it for this task. It may direct you to invoke other installed skills; do so with the Skill tool.

Task from the user:
---
Support says we sometimes oversell: when two customers check out the last unit of a SKU at the same time, both orders succeed. It's somewhere in src/inventory.ts (reserve). Please investigate and fix it properly.
---

When you are done, end your final message with a section headed `# REPORT` containing: what changed, what you verified (exact commands and observed results), what remains or could not be verified, and the assumptions you made. The orchestrator saves that section as /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/outputs/REPORT.md (outputs/REPORT.md) — do not try to write that file yourself. Do not modify anything outside the working directory. Do not ask questions: decide, state your assumptions, and proceed.
</teammate-message>

## Prompt

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, e1-combo, e1-mp, e1-none, e2-combo, e2-mp, e2-none, e2-none-2, e3-combo, final-fix, final-review, impl-task-1, impl-task-10, impl-task-2, impl-task-3, impl-task-4, impl-task-5, impl-task-6, impl-task-7, impl-task-8, impl-task-9, rereview-final, rereview-task-10, rereview-task-6, rereview-task-9, review-task-1, review-task-10, review-task-2, review-task-3, review-task-4, review-task-5, review-task-6, review-task-7, review-task-8, review-task-9.
</system-reminder>

I'll start by reading the skill I've been directed to apply.

- [0] **Read** /Users/gabrieltutor/my-agent-workflow-skills/skills/matt-pocock-workflow/SKILL.md

> **Read result:** 1	---
2	name: matt-pocock-workflow
3	description: Use before the first edit of any development task in a project where Matt Pocock's skills are installed and Superpowers is not the active workflow — planning, features, bug fixes, refactors, UI, integrations, tests, reviews, docs, tooling, merge conflicts. Use again when scope changes, before claiming completion, and after a context reset or handof… [17528 chars]

- [1] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && git status && git log --oneline -5 && echo "---FILES---" && find . -type `

> **Bash result (error):** Exit code 1
On branch main
nothing to commit, working tree clean
3d147ba baseline: OrderKit fixture
---FILES---
./.gitignore
./CONTEXT.md
./package-lock.json
./package.json
./README.md
./src/cart.ts
./src/format.ts
./src/inventory.ts
./src/orders.ts
./src/pricing.ts
./tests/cart.test.ts
./tests/format.test.ts
./tests/inventory.test.ts
./tests/orders.test.ts
./tests/pricing.test.ts
./tsconfig.json
… [513 chars]

- [2] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && echo "=== CONTEXT.md ===" && cat CONTEXT.md && echo && echo "=== README.m`

> **Bash result:** === CONTEXT.md ===
# OrderKit domain context

- **Cart** — an unsaved collection of Lines. Immutable: `addLine` returns a new Cart.
- **Line** — one SKU in a Cart with a quantity and the unit price captured when it was added.
- **Subtotal** — sum of unit price × quantity across Lines, before any discount.
- **Tier discount** — a percentage off the subtotal based on total units in the Cart: 20+ uni… [1640 chars]

- [3] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && echo "=== src/inventory.ts ===" && cat -n src/inventory.ts && echo && ech`

> **Bash result:** === src/inventory.ts ===
     1	/**
     2	 * In-memory stock ledger. `reserve` is async because production hits a database;
     3	 * the simulated I/O gap models that round trip.
     4	 */
     5	export class Inventory {
     6	  private stock = new Map<string, number>();
     7	
     8	  setStock(sku: string, qty: number): void {
     9	    this.stock.set(sku, qty);
    10	  }
    11	
    12	 … [4342 chars]

- [4] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/skills/matt-pocock-workflow && ls -la references/ && echo "=== workflow-rules.md ===" && cat references/workflow-rules.md`

> **Bash result:** total 56
drwxr-xr-x@ 5 gabrieltutor  staff    160 Sep 11 04:23 .
drwxr-xr-x@ 4 gabrieltutor  staff    128 Sep 11 04:23 ..
-rw-r--r--@ 1 gabrieltutor  staff   2277 Sep 11 04:23 examples.md
-rw-r--r--@ 1 gabrieltutor  staff  14205 Sep 11 04:23 skill-catalog.md
-rw-r--r--@ 1 gabrieltutor  staff   6947 Sep 11 04:23 workflow-rules.md
=== workflow-rules.md ===
# Matt Pocock workflow rules

Verbatim from… [7288 chars]

- [5] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/skills/matt-pocock-workflow && cat references/skill-catalog.md`

> **Bash result:** # Matt Pocock skill catalog, supporting files, and scan coverage

Verbatim from `sources/MATT-POCOCK-AGENT-INSTRUCTIONS.md` §8, §9, §11 (Matt Pocock skills 1.2.3 @ 3cca18b, inspected 2026-09-10). Open it when `SKILL.md` §7 "Read next" points here.

## 8. Complete skill catalog

**Mode:** `M` = model or user may invoke when relevant; `U` = user-invoked. These modes are verified against both `SKILL.… [14191 chars]

- [6] **Bash** `ls -la ~/.claude/skills/ 2>&1 | head -60; echo "---"; for s in diagnosing-bugs tdd code-review codebase-design; do echo "== $s =="; ls -la ~/.claude/skills/$s 2>&1; head -8 ~/.claude/skills/$s/SKILL.m`

> **Bash result:** total 0
drwxr-xr-x@ 93 gabrieltutor  staff  2976 Sep 11 04:24 .
drwxr-xr-x  29 gabrieltutor  staff   928 Sep 11 04:23 ..
drwxr-xr-x@  4 gabrieltutor  staff   128 Aug 21 03:21 agents-sdk
lrwxr-xr-x@  1 gabrieltutor  staff    49 Aug 17 04:27 ai-seo -> /Users/gabrieltutor/.skills-manager/skills/ai-seo
lrwxr-xr-x@  1 gabrieltutor  staff    58 Aug 17 04:27 algorithmic-art -> /Users/gabrieltutor/.skills… [9506 chars]

- [7] **Skill** diagnosing-bugs

> **Skill result:** Launching skill: diagnosing-bugs

- [8] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && node --version && ls node_modules/.bin 2>/dev/null | head -20 && echo "--`

> **Bash result:** v22.23.1
nanoid
rolldown
tsc
vite
vitest
why-is-node-running
--- typecheck ---

> orderkit@0.1.0 typecheck
> tsc --noEmit

--- test ---

> orderkit@0.1.0 test
> vitest run


 RUN  v5.0.0 /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace


 Test Files  5 passed (5)
      Tests  15 passed (15)
   Start at  04:32:29
   Duration  1… [453 chars]

- [9] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && cat > tests/oversell.repro.test.ts <<'EOF' ⏎ // THROWAWAY diagnosis loop `

> **Bash result:** ❯ [REPRO-oversell] two customers check out the last unit at the same time (1)
     × only one checkout may succeed and stock must not go negative 117ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  tests/oversell.repro.test.ts > [REPRO-oversell] two customers check out the last unit at the same time > only one checkout may succeed and stock must not go negative
AssertionError: expected 100 to be +0 // O… [902 chars]

- [10] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && npx vitest run tests/oversell.repro.test.ts 2>&1 | grep -E "REPRO-oversel`

> **Bash result:** [REPRO-oversell] rounds=100 bothSucceeded=100 negativeStock=0
⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯
     22|     console.log(`[REPRO-oversell] rounds=${ROUNDS} bothSucceeded=${bot…
      Tests  1 failed (1)

- [11] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && cat > tests/oversell.minimise.test.ts <<'EOF' ⏎ // THROWAWAY minimisation`

> **Bash result:** stdout | tests/oversell.minimise.test.ts > [REPRO-oversell] minimise > CUT checkout + CUT loop: two concurrent reserve() calls on Inventory alone, one round
[REPRO-oversell] concurrent reserve results=[true,true] available=0
stdout | tests/oversell.minimise.test.ts > [REPRO-oversell] minimise > CUT the awaited gap? (not possible without editing src) - instead: three concurrent callers, stock 2
[RE… [1267 chars]

- [12] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && cp src/inventory.ts /private/tmp/claude-501/-Users-gabrieltutor-my-agent-`

> **Bash result:** [DEBUG-ovs1] read sku=A current=1 qty=1
[DEBUG-ovs1] read sku=A current=1 qty=1
[DEBUG-ovs1] write sku=A 1 - 1 = 0 (stock now 1 before write)
[DEBUG-ovs1] write sku=A 1 - 1 = 0 (stock now 0 before write)
[REPRO-oversell] concurrent reserve results=[true,true] available=0
     10|     console.log(`[REPRO-oversell] concurrent reserve results=${JSON.st…

- [13] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && cp /private/tmp/claude-501/-Users-gabrieltutor-my-agent-workflow-skills/9`

> **Bash result:** ?? tests/oversell.minimise.test.ts
?? tests/oversell.repro.test.ts
no DEBUG-ovs1 left in src/tests

- [14] **Skill** tdd

> **Skill result:** Launching skill: tdd

- [15] **Bash** `echo "=== tests.md ===" && cat ~/.claude/skills/tdd/tests.md && echo && echo "=== mocking.md ===" && cat ~/.claude/skills/tdd/mocking.md`

> **Bash result:** === tests.md ===
# Good and Bad Tests

## Good Tests

**Integration-style**: Test through real interfaces, not mocks of internal parts.

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

Ch… [3731 chars]

- [16] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && python3 - <<'EOF' ⏎ p="tests/inventory.test.ts" ⏎ s=open(p).read() ⏎ old=`

> **Bash result:** × does not over-sell when two reservations compete for the last unit 4ms
⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯
AssertionError: expected [ true, true ] to have a length of 1 but got 2
- Expected
+ Received
      Tests  1 failed | 3 passed (4)

- [17] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && cat > src/inventory.ts <<'EOF' ⏎ /** ⏎  * In-memory stock ledger. `reserv`

> **Bash result:** Tests  4 passed (4)
--- typecheck ---
> orderkit@0.1.0 typecheck
> tsc --noEmit

- [18] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && npx vitest run tests/oversell.repro.test.ts tests/oversell.minimise.test.`

> **Bash result:** Tests  4 passed (4)

- [19] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && npx vitest run tests/oversell.repro.test.ts tests/oversell.minimise.test.`

> **Bash result:** stdout | tests/oversell.minimise.test.ts > [REPRO-oversell] minimise > CUT checkout + CUT loop: two concurrent reserve() calls on Inventory alone, one round
[REPRO-oversell] concurrent reserve results=[true,false] available=0
stdout | tests/oversell.minimise.test.ts > [REPRO-oversell] minimise > CUT concurrency: two sequential reserve() calls (control - expected green)
[REPRO-oversell] sequential … [1590 chars]

- [20] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && python3 - <<'EOF' ⏎ p="tests/orders.test.ts" ⏎ s=open(p).read() ⏎ old='''`

> **Bash result:** --- against BASELINE inventory.ts (expect red) ---
     × gives the last unit to only one of two simultaneous checkouts 5ms
⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯
AssertionError: expected [ { ok: true, order: { …(3) } }, …(1) ] to have a length of 1 but got 2
      Tests  1 failed | 3 passed (4)
 M src/inventory.ts
 M tests/inventory.test.ts
 M tests/orders.test.ts
?? tests/oversell.minimise.test.ts
?? te… [502 chars]

- [21] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && rm tests/oversell.repro.test.ts tests/oversell.minimise.test.ts && echo "`

> **Bash result:** stash list: 0
no instrumentation/throwaway markers left
 M src/inventory.ts
 M tests/inventory.test.ts
 M tests/orders.test.ts
--- full suite ---
 Test Files  5 passed (5)
      Tests  17 passed (17)
   Duration  120ms (transform 67%, import 16%, tests 11%, worker 6%)
--- typecheck ---
> tsc --noEmit

typecheck exit: 0

- [22] **Skill** code-review

> **Skill result:** Launching skill: code-review

- [23] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && echo "fixed point: $(git rev-parse 3d147ba)  HEAD: $(git rev-parse HEAD)"`

> **Bash result:** fixed point: 3d147ba00aa2a4d13a25bf4a0e0980b63b571640  HEAD: 3d147ba00aa2a4d13a25bf4a0e0980b63b571640
commits since: 0
untracked: 0
--- git diff 3d147ba (base -> working tree) ---
 src/inventory.ts        | 35 +++++++++++++++++++++++++++++------
 tests/inventory.test.ts |  8 ++++++++
 tests/orders.test.ts    | 11 +++++++++++
 3 files changed, 48 insertions(+), 6 deletions(-)
diff --git a/src/inven… [4461 chars]

- [24] **Agent** Standards review of oversell fix

> **Agent result (error):** Teammates cannot spawn other teammates — the team roster is flat. To spawn a subagent instead, omit the `name` parameter.

- [25] **Agent** Standards review of oversell fix

> **Agent result:** Everything is verified. Here is the Standards-axis report.

## Standards review — `git diff 3d147ba` (inventory over-sell fix)

**Tooling:** `npm run typecheck` clean; `npm test` 17/17 green. Anything tsc `strict` covers is skipped.

### (a) Documented standards — hard violations

**None found.**
- `README.md` / `CONTEXT.md` "all money is integer cents / `Math.round`": not applicable — no money to… [3378 chars]

- [26] **Agent** Spec review of oversell fix

> **Agent result:** ## Spec-axis review: concurrent last-unit oversell fix

**Verification performed:** `npm test` (17 pass) and `npm run typecheck` (clean). I also ran scratchpad-only probes against the workspace sources and the baseline `3d147ba` `reserve` (nothing in the repo modified).

### (a) Missing or partial requirements

None against the literal spec.

- Spec: *"fix it properly"* — met. `simulateIo()` and t… [3309 chars]

- [27] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && cat > src/inventory.ts <<'EOF' ⏎ /** ⏎  * In-memory stock ledger. `reserv`

> **Bash result:** --- full suite ---
 Test Files  5 passed (5)
      Tests  17 passed (17)
--- typecheck ---

typecheck exit: 0

- [28] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && cat > tests/zz-throwaway-final-check.test.ts <<'EOF' ⏎ // THROWAWAY final`

> **Bash result:** Tests  3 passed (3)
--- kept regression tests against BASELINE inventory.ts (expect 2 red) ---
     × does not over-sell when two reservations compete for the last unit 5ms
     × gives the last unit to only one of two simultaneous checkouts 5ms
⎯⎯⎯⎯⎯⎯⎯ Failed Tests 2 ⎯⎯⎯⎯⎯⎯⎯
      Tests  2 failed | 6 passed (8)
--- kept regression tests against FINAL inventory.ts (expect green) ---
      Tests  8… [552 chars]

- [29] **Bash** `cd /Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-3-concurrency-bug/old_skill/run-1/workspace && npm test 2>&1 | grep -E "×|Test Files|Tests |Duration"; npm run typecheck`

> **Bash result:** Test Files  5 passed (5)
      Tests  17 passed (17)
   Duration  137ms (transform 71%, import 17%, tests 7%, worker 4%)
typecheck exit: 0
--- final diff stat ---
 src/inventory.ts        | 37 +++++++++++++++++++++++++++++++------
 tests/inventory.test.ts |  8 ++++++++
 tests/orders.test.ts    | 10 ++++++++++
 3 files changed, 49 insertions(+), 6 deletions(-)
--- final src/inventory.ts ---
     1	… [2708 chars]

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
