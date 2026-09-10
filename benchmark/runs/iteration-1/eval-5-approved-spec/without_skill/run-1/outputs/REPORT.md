The coupon spec is implemented, tested, and verified.

# REPORT

## What changed

Three files in the working tree (uncommitted — the task did not ask for a commit):

- `/Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-5-approved-spec/without_skill/run-1/workspace/src/pricing.ts` — added `export function applyCoupon(cart: Cart, code: string): number` plus a `COUPONS` data table (same `ReadonlyArray` + `.find` idiom as the existing `TIERS` table) with a small `Coupon` discriminated union (`percent` | `flat`). It uppercases the code, looks it up, throws `unknown coupon: <code>` on a miss, computes the post-tier total via the untouched `totalCents`, then applies the coupon. `FLAT5` gates on `subtotalCents(cart) >= 2000` (pre-tier subtotal, per spec) and throws `coupon FLAT5 not applicable: subtotal must be at least 2000 cents` otherwise. `totalCents`, `tierDiscountPercent`, and `totalUnits` are byte-for-byte unchanged.
- `/Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-5-approved-spec/without_skill/run-1/workspace/tests/pricing.test.ts` — added a `describe("coupons")` block with 6 tests, one per acceptance criterion, built only with `createCart`/`addLine` via the existing `cartWithUnits` helper (per the spec's test seam). Covers: 10% with a `.5` rounding case (525 → 472); `FLAT5` at subtotal exactly 2000 where the post-tier total is 1900 (pins the subtotal-not-total gate and the inclusive boundary); `FLAT5` at 1999 and on an empty cart throwing `/not applicable/`; `BOGUS` and `""` throwing `/unknown coupon/`; `save10`/`Flat5` case-insensitivity; the spec's exact stacking example (25 × 100 → 2137) with `totalCents` still 2375.
- `/Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-5-approved-spec/without_skill/run-1/workspace/CONTEXT.md` — one-line glossary fix: the Coupon entry said "Not implemented yet", which this change made false. Now: "applied after the tier discount. See `docs/spec-coupons.md`."

## What I verified

All commands run from the workspace directory.

- Baseline before changes: `npm test` → `Test Files 5 passed (5), Tests 15 passed (15)`; `npm run typecheck` → clean (no output, exit 0).
- After changes: `npm test` → `Test Files 5 passed (5), Tests 21 passed (21)`; `npm run typecheck` → clean. The 15 pre-existing tests still pass unchanged.
- Mutation check that the new tests are load-bearing (temporarily edited `src/pricing.ts`, ran `npx vitest run tests/pricing.test.ts`, then restored from a scratchpad backup):
  - Gating `FLAT5` on the post-tier `total` instead of `subtotalCents(cart)` → `1 failed | 9 passed` ("FLAT5 subtracts 500 cents when the subtotal is at least 2000 cents").
  - `Math.floor` instead of `Math.round` for `SAVE10` → `2 failed | 8 passed` (`expected 473 to be 472`, `expected 2138 to be 2137`).
  - Restored file confirmed via `git diff --stat` and a final green `npm test` (21/21).
- Hand-checked the spec's example: 2500 → −125 → 2375 → −round(237.5)=238 → 2137. Matches criterion 6.
- `git status --short` shows exactly `M CONTEXT.md`, `M src/pricing.ts`, `M tests/pricing.test.ts`. Nothing outside the working directory was touched (the scratchpad backup was in the session scratchpad, not the repo).

## What remains / could not be verified

- Nothing outstanding against the spec. Changes are left uncommitted in the working tree because the task did not request a commit; say the word if you want one.
- No integration with `checkout`/`Order` was done — the spec's interface is a pure function on `Cart` and `totalCents` is explicitly unchanged, so `orders.ts` was not touched.

## Assumptions

- Case-insensitivity is implemented as `toUpperCase()` only; codes are **not** trimmed (`" save10 "` is an unknown coupon). The spec only asks for case-insensitivity, so I did not widen it.
- The `unknown coupon` message echoes the code as passed (e.g. `unknown coupon: bogus`); the `not applicable` message uses the canonical code (`FLAT5`) and states the 2000-cent minimum. The spec only constrains the substrings, not the full text.
- `FLAT5` never needs clamping to zero: the subtotal ≥ 2000 gate with a maximum 10% tier means the post-tier total is always ≥ 1800 before subtracting 500.
- Empty cart + `FLAT5` throws `not applicable` (subtotal 0 < 2000); empty cart + `SAVE10` returns 0. Both follow directly from the criteria; neither is special-cased.
- Updating the stale `CONTEXT.md` glossary line was treated as part of implementing the feature rather than an out-of-scope doc change, since the file would otherwise contradict the code.
