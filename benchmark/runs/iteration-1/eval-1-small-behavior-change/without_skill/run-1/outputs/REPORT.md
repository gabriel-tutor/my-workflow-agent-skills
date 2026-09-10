Done. Coupon support is implemented in `src/pricing.ts`, tested, and the domain doc is updated. Changes are left uncommitted in the working tree (the task didn't ask for a commit).

# REPORT

## What changed

Three files in `/Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-1-small-behavior-change/without_skill/run-1/workspace`:

1. **`src/pricing.ts`** — added `export function applyCoupon(cart: Cart, code: string): number` (lines 26-41). It starts from `totalCents(cart)` (so the existing tier discount is reused unchanged) and then:
   - `SAVE10` → subtracts `Math.round(total * 10 / 100)`, using the same discount-then-subtract rounding idiom as `totalCents`.
   - `FLAT5` → subtracts 500 cents when `subtotalCents(cart) >= 2000`, otherwise returns the total unchanged.
   - any other code → `throw new Error(\`unknown coupon code: ${code}\`)`, matching the plain-`Error`-with-message style used in `src/cart.ts`.
   
   No existing functions were modified.

2. **`tests/pricing.test.ts`** — added `applyCoupon` to the import and a new `describe("applyCoupon")` block with 8 tests: basic SAVE10, SAVE10 rounding (315 → 283), FLAT5 at/above threshold, FLAT5 below threshold (unchanged), FLAT5 threshold measured on the pre-discount subtotal (20 units: subtotal 2000, tier total 1900 → 1400), coupon composed on top of the 10% tier (5000 → 4500 → 4050), unknown codes throw (`"BOGUS"` and `""`), and `totalCents`/`tierDiscountPercent` are unaffected.

3. **`CONTEXT.md`** — replaced the stale "Coupon … Not implemented yet." line with a description of the implemented semantics.

## What I verified

- Baseline before any edits: `npm test` → `Test Files 5 passed (5), Tests 15 passed (15)`; `npm run typecheck` → clean.
- After edits: `npm test` → `Test Files 5 passed (5), Tests 23 passed (23)`.
- `npx tsc --noEmit; echo $?` → `tsc exit code: 0`.
- `npx vitest run tests/pricing.test.ts --reporter=verbose` → all 12 tests in the file listed with ✓ (4 pre-existing tier tests + 8 new).
- Mutation check: temporarily changed the FLAT5 guard to `total >= 2000` (tier-discounted total instead of subtotal) and re-ran — exactly one test failed, `FLAT5 checks the pre-discount subtotal, not the tier-discounted total` with `expected 1900 to be 1400`. Restored the file from a scratchpad backup; `diff` confirmed it identical, and the full suite went back to 23/23.
- `git status --short` shows only `CONTEXT.md`, `src/pricing.ts`, `tests/pricing.test.ts` modified; nothing touched outside the working directory.

## What remains / could not be verified

- Nothing is blocked. I did not commit (not requested). `checkout` in `src/orders.ts` was intentionally not changed to accept a coupon, since the task scoped the work to `applyCoupon` in `src/pricing.ts`.
- If the intended semantics differ from my assumptions below (e.g., an ineligible FLAT5 should throw, or codes should be case-insensitive), each is a one-line change in the `switch`.

## Assumptions

1. **Coupons stack on top of the tier discount** (sequential, not additive percentages): `applyCoupon` applies the code to `totalCents(cart)`. "Return the new total" read most naturally as "take the current total and apply the coupon," and this leaves the tier code path untouched.
2. **FLAT5's $20 threshold is measured against the Subtotal** — the pre-discount figure as defined in `CONTEXT.md` — because the task literally says "subtotal." This matters at the boundary (20 units at $1: subtotal $20 but tier total $19 — the coupon *is* eligible).
3. **FLAT5 below the threshold returns the total unchanged rather than throwing.** The task reserves throwing for *unknown* codes and only says FLAT5 "takes $5 off … only when" the threshold is met; a known-but-ineligible code isn't unknown.
4. **Codes are matched exactly (case-sensitive), no trimming.** The task names the codes in uppercase and doesn't mention normalization, so I didn't invent any.
5. **No clamp to zero is needed**: with subtotal ≥ 2000 and a maximum 10% tier discount, the tier-discounted total is ≥ 1800 > 500, so FLAT5 can't produce a negative total under the current tiers.
6. **Rounding follows `Math.round` on the discount amount** (per `CONTEXT.md` and the existing `totalCents` idiom), pinned by the 315 → 283 test.
