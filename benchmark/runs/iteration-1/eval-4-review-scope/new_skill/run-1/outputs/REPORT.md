Verification is complete and every claim below is tied to output I observed in this session. Here is the review.

## Review: coupon codes vs `docs/spec-coupons.md`

**Scope reviewed (this matters):** branch `main`, base `3d147ba` → HEAD `1c45102` (`feat: coupon codes (SAVE10, FLAT5)`), **plus** two pieces of uncommitted work that a plain `3d147ba...HEAD` diff hides: an unstaged edit to `src/format.ts` and an untracked `src/scratch.ts`. "Current state of this branch" includes all three.

### Strengths
- Interface matches the spec exactly: `applyCoupon(cart: Cart, code: string): number` exported from `src/pricing.ts:27`, computed on top of `totalCents`, and `totalCents` itself is untouched.
- Rounding follows `CONTEXT.md:11` (`Math.round`), and AC6's worked example disambiguates "round the discount, not the result" — the implementation gets 2137, matching the spec.
- AC1, AC2 (happy path), AC4 and AC6 all pass when exercised.
- `tests/coupons.test.ts` honours the spec's test seam (public `createCart`/`addLine`, no internal helpers), and error-message style matches the existing lowercase `\`unknown coupon: ${code}\`` convention in `src/cart.ts:17-18`.
- The spec was committed alongside the code.

### Issues

#### Critical (must fix)
1. **`FLAT5` has no subtotal guard and produces negative money** — `src/pricing.ts:32-33` returns `base - 500` unconditionally. Spec AC2 requires the 500-cent discount only when the pre-tier subtotal is ≥ 2000, and AC3 requires an `Error` containing `not applicable` below that. Observed: `applyCoupon(1×300 cart, "FLAT5")` → `-200`; empty cart → `-500`. A negative total is a data-integrity defect under `CONTEXT.md:11` ("All money is integer cents"), not just a missing message. Fix: check `subtotalCents(cart) < 2000` (the *subtotal*, not `base`) and throw.
2. **Codes are case-sensitive** — `src/pricing.ts:29` switches on the raw `code`. Spec AC5: `save10` must behave like `SAVE10`. Observed: `applyCoupon(cart, "save10")` throws `unknown coupon: save10`. Fix: normalise (`code.toUpperCase()`) before matching; keep the original `code` in the error text if you like.

#### Important (should fix)
3. **Test coverage is one happy path** — `tests/coupons.test.ts:6-9` covers AC1 only. AC2, AC3, AC4, AC5, AC6 have no tests, and the two defects above sit exactly in the untested area. The spec's seam is fine; the coverage isn't. Add one test per criterion, including both failure paths (`toThrow(/not applicable/)`, `toThrow(/unknown coupon/)`) and the AC6 stacking example.
4. **Uncommitted, unrelated leftovers in the working tree**
   - `src/format.ts:5` (unstaged): appends `TODO: tidy this comment.` to a doc comment while leaving the existing `recieve` typo on line 4. It's unrelated to coupons and unfinished.
   - `src/scratch.ts` (untracked): `export const scratch = 1;` — referenced by nothing, but it lives inside `src/`, which `tsconfig.json` includes, so it is compiled and would ship if anyone runs `git add .`.
   Neither belongs in this merge. I did not revert or delete them (they could be someone's in-progress work); that's your call, but the branch isn't merge-ready while they're present.
5. **Domain doc is stale** — `CONTEXT.md:7` still says "**Coupon** — … Not implemented yet." Update the entry (code entered by the customer, case-insensitive, applied after the tier discount; `SAVE10`/`FLAT5` rules).

#### Minor (judgment calls, not violations)
6. Coupon rules are inline literals (`0.1`, `500`) in a `switch`, while the tier rules use a data table (`TIERS`, `src/pricing.ts:4-7`). Once the subtotal guard and case folding land, a small `COUPONS` table or per-code function would keep the switch from accreting logic. Consistency preference only — no documented standard requires it.

### Standards axis (MP criteria)
No documented repository standard is breached: `CONTEXT.md` (integer cents, `Math.round`) is followed; there is no `CODING_STANDARDS.md`/`CONTRIBUTING.md`. From the smell baseline, only item 6 above registers, and it is a judgment call. Typecheck is clean.

### Spec axis (MP criteria)
- Missing: AC3 (`not applicable` error), AC5 (case-insensitivity).
- Incorrect: AC2 — applies `FLAT5` below the 2000-cent threshold.
- Implemented correctly: interface, AC1, AC4, AC6, `totalCents` unchanged.
- Extra/unrequested: the `format.ts` TODO edit and `scratch.ts` (uncommitted, out of spec scope).

### Assessment

**Ready to merge? No.**

**Reasoning:** Two of six acceptance criteria fail with executable evidence, one of them yielding negative totals; the test suite passes only because those criteria have no tests. Even judging the committed HEAD alone it is not ready, and the working tree additionally carries unrelated leftovers that must be reverted, deleted, or split out first. Suggested shape of the fix (not applied — you asked for review only):

```ts
export function applyCoupon(cart: Cart, code: string): number {
  const base = totalCents(cart);
  switch (code.toUpperCase()) {
    case "SAVE10":
      return base - Math.round(base * 0.1);
    case "FLAT5":
      if (subtotalCents(cart) < 2000) throw new Error(`coupon FLAT5 not applicable: subtotal below 2000 cents`);
      return base - 500;
    default:
      throw new Error(`unknown coupon: ${code}`);
  }
}
```
plus tests for AC2–AC6 through the public seam, and the `CONTEXT.md` update.

# REPORT

**What changed:** Nothing in the repository. This was a read-only review; `git status` before and after is identical (`M src/format.ts`, `?? src/scratch.ts`, both pre-existing). Throwaway probe tests were written only to my scratchpad (`/private/tmp/claude-501/-Users-gabrieltutor-my-agent-workflow-skills/970fed02-dc03-46d2-a57b-782439d4e6c7/scratchpad/coupon-probe/`).

**Skills applied:** `matt-pocock-superpowers-workflow` as routing policy (loaded `references/conflict-rules.md`, `quality-gates.md`, catalog entries); `superpowers:using-superpowers` (bootstrap); `superpowers:requesting-code-review` as review owner — its `code-reviewer.md` structure and checks were applied inline by me rather than via a dispatched subagent, because I was dispatched as a worker (§6: workers dispatch no reviewers) — so the review was not performed by a separate agent, though it is independent of whoever implemented the change; `MP/code-review` `SKILL.md` consulted for the Standards/Spec criteria only (no two-agent orchestration ran); `superpowers:verification-before-completion` before the verdict. Conflict rule 9 (review scope) drove the inclusion of unstaged and untracked work.

**Verified (all run in `/Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-4-review-scope/new_skill/run-1/workspace`):**
- `git branch -a; git rev-parse HEAD; git log --oneline --all; git status --porcelain=v1 --untracked-files=all --ignored; git stash list` → branch `main`, HEAD `1c45102`, base `3d147ba`, status `M src/format.ts`, `?? src/scratch.ts`, `!! node_modules`; no stash, no remotes.
- `git diff 3d147ba...HEAD` → `docs/spec-coupons.md` (+22), `src/pricing.ts` (+13), `tests/coupons.test.ts` (+10). `git diff HEAD` → one-line comment change in `src/format.ts`. `git diff --cached --stat` → empty. `cat src/scratch.ts` → `export const scratch = 1;`.
- `grep -rn "scratch\|applyCoupon" src tests` → `scratch` referenced only by itself.
- `npm test` → `Test Files 6 passed (6)`, `Tests 16 passed (16)`, exit 0. `npm run typecheck` → exit 0.
- Scratchpad probe via `./node_modules/.bin/vitest run --dir <scratchpad>/coupon-probe` → 7 tests, **5 passed / 2 failed**: AC3 (`expected [Function] to throw an error`) and AC5 (`Error: unknown coupon: save10` at `src/pricing.ts:35:13`); AC1, AC2, AC4, AC6 passed. Second probe → `applyCoupon(1×300, "FLAT5")` = `-200` and `applyCoupon(empty, "FLAT5")` = `-500` (both assertions passed, exit 0).
- `git status --porcelain=v1 --untracked-files=all` after all probes → unchanged from the start.

**Remaining / could not be verified:**
- Baseline commit `3d147ba` was not checked out or test-run separately (would require `git worktree add` or `git archive`; unnecessary because the current tree has zero failing tests, so there are no failures to attribute).
- No independent second reviewer ran; findings are mine alone.
- No issue tracker configuration (`docs/agents/issue-tracker.md`) exists; irrelevant here because the spec path was given directly.

**Assumptions:**
- Merge base is `3d147ba` (the only other commit; no remote or `origin/main`).
- "Current state of this branch" includes unstaged and untracked files, per the user's wording and conflict rule 9.
- "Ready to merge" was judged against the policy's ready-for-review/ready-to-release definitions: a known failed acceptance criterion blocks it.
- The uncommitted `format.ts`/`scratch.ts` work may belong to someone; I flagged it rather than reverting or deleting it, and made no changes to the repo per the user's instruction.
