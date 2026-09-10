Environment: normal repo (no worktree), branch `main`, no remote configured, HEAD `8576864`, changes uncommitted. The integration decision is the user's; since this run must not ask questions, I'm leaving the work as-is (the skill's "keep as-is" outcome) and listing the options below rather than executing any of them.

```text
Changed: applyCoupon(cart, code) added to src/pricing.ts per docs/spec-coupons.md (SAVE10 / FLAT5, case-insensitive, errors for unknown / not-applicable codes), six tests in tests/pricing.test.ts, Coupon glossary line in CONTEXT.md.
Skills applied: SP/using-superpowers (bootstrap) → matt-pocock-superpowers-workflow routing (+ development-loop, coordination, quality-gates refs) → design reused from the approved spec (no SP/brainstorming, no MP interview) → SP/test-driven-development as cycle owner with MP tdd/SKILL.md + tests.md consulted for seam/literal discipline → SP/requesting-code-review dispatched one independent Sonnet reviewer with MP code-review Standards/Spec criteria added (reference consulted, its two-agent orchestration not run) → SP/receiving-code-review to evaluate findings → SP/verification-before-completion → SP/finishing-a-development-branch (environment detected, options presented). MP/domain-modeling consulted for the CONTEXT.md glossary rule.
Verified: npm test → 5 files, 21/21 passed, exit 0; npm run typecheck → exit 0; each new test observed failing for the expected reason before its implementation (except the preservation guard, stated as such); review scope = working tree vs 8576864 (3 files, +64/−2), reviewer verdict "Ready to merge: Yes", 0 Critical / 0 Important / 3 Minor (all dispositioned, no code change).
Remaining: work is uncommitted on main pending your integration choice; no linter/CI exists in the repo to run; applyCoupon is not wired into checkout (spec does not ask for it).
```

# REPORT

## What changed

Working tree of `/Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-5-approved-spec/new_skill/run-1/workspace`, uncommitted, against baseline commit `8576864` (`git diff --stat 8576864`: 3 files changed, 64 insertions, 2 deletions):

- `src/pricing.ts` — added exported `applyCoupon(cart: Cart, code: string): number` (lines 26–48) plus the module-private constant `FLAT5_MIN_SUBTOTAL_CENTS = 2000`. It computes `totalCents(cart)` (post-tier), uppercases the code, and: `SAVE10` → `total - Math.round(total * 10 / 100)`; `FLAT5` → throws `Error("coupon FLAT5 not applicable: …")` when `subtotalCents(cart) < 2000`, else `total - 500`; any other code → throws `Error("unknown coupon: <code>")`. `totalCents` and every other existing function are untouched.
- `tests/pricing.test.ts` — imported `applyCoupon`; added a `describe("coupons")` block with six tests using only the public seam (`createCart`/`addLine` via the existing `cartWithUnits` helper, `applyCoupon`, `totalCents`): unknown code rejected; SAVE10 10% with rounded discount (1000→900, and the spec's 2500→2375→2137 stacking example); FLAT5 qualifies at subtotal exactly 2000 while the post-tier total is 1900 (→1400); FLAT5 rejected at subtotal 1999; case-insensitive `save10`/`Flat5`; cart and `totalCents` unchanged after applying a coupon.
- `CONTEXT.md` — the Coupon glossary entry no longer says "Not implemented yet"; it now describes the concept (applied after the Tier discount, one per Cart, may require a minimum Subtotal, unknown/inapplicable codes rejected) without implementation details.

Process route: the approved spec was reused as the design — no brainstorming or MP interview was run and no clarifying questions were asked; no plan document was manufactured for this bounded task; no worktree was created because the run directory is already an isolated repo. Implementation was inline TDD (SP `test-driven-development` owning the cycle, MP `tdd` references consulted). One independent reviewer subagent (general-purpose, Sonnet, read-only) reviewed the real working-tree diff with SP's checklist plus MP's Standards and Spec criteria; because the branch has a single task, that one review served as both the task review and the whole-branch review (no duplicate seat).

## What I verified

Baseline (before any edit):
- `npm test` → `Test Files 5 passed (5)`, `Tests 15 passed (15)`.
- `npm run typecheck` → clean, no output.
- `git status` → clean tree at `8576864`.

TDD evidence (each run via `npx vitest run tests/pricing.test.ts`):
1. "rejects an unknown code" — RED: `applyCoupon is not a function`; GREEN after adding the throwing stub (5/5).
2. "SAVE10 subtracts 10% …" — RED: `Error: unknown coupon: SAVE10`; GREEN after the SAVE10 branch (6/6).
3. "FLAT5 subtracts 500 cents when the pre-tier subtotal reaches 2000" — RED: `Error: unknown coupon: FLAT5`; GREEN after the FLAT5 branch (7/7).
4. "FLAT5 is rejected when the subtotal is below 2000" — RED: `expected function to throw an error, but it didn't`; GREEN after the subtotal guard (8/8).
5. "matches codes case-insensitively" — RED: `Error: unknown coupon: save10`; GREEN after `toUpperCase()` (9/9).
6. "leaves the cart and totalCents unchanged" — passed on first run by design (preservation guard for the spec sentence "`totalCents` is unchanged"; stated as such, not claimed as red-driven).
7. Refactor (named constant, `switch`, doc comment) — suite stayed green.

Final state (fresh runs after the refactor and the review):
- `npm test` → `Test Files 5 passed (5)`, `Tests 21 passed (21)`, exit 0.
- `npm run typecheck` → `tsc --noEmit` clean, exit 0.
- `npx vitest run tests/pricing.test.ts --reporter=verbose` → all 10 tests in the file listed with ✓ (4 tier tests + 6 coupon tests).
- `git status --porcelain` → ` M CONTEXT.md`, ` M src/pricing.ts`, ` M tests/pricing.test.ts`; `git ls-files --others --exclude-standard` → empty (no stray files).
- Requirements checklist: AC1–AC6, the interface clause, the test-seam clause and the out-of-scope list each map to a specific test or diff hunk (table in the message above).

Independent review (subagent, scope = `git diff 8576864` working tree vs baseline; it re-ran `npm test` → 21/21 and `npm run typecheck` → clean itself): Spec axis — all six ACs correct, no missing/partial/extra behaviour; Standards axis — no hard violations of README/CONTEXT.md/tsconfig conventions; Issues — 0 Critical, 0 Important, 3 Minor; verdict "Ready to merge: Yes". Minor findings and disposition: (1) raw `code` echoed in the unknown-coupon message — accepted as-is, matches the repo's own convention at `src/cart.ts:17-18` and UI is out of scope; (2) `switch` vs a table — disproven, two cases, table would be speculative generality; (3) two `toThrow` calls per error test — kept, `toThrow(Error)` verifies the spec's explicit "throws an `Error`" clause. No code changed after review, so the reviewed diff is the final diff.

## What remains or could not be verified

- Not committed and not merged. Per the harness rule to commit only when asked, the change sits uncommitted on `main`. Integration options (none executed; there is no git remote, so a PR is not possible from this repo): commit on a feature branch (`git checkout -b feat/coupons && git add CONTEXT.md src/pricing.ts tests/pricing.test.ts && git commit`), commit directly on `main`, or keep as-is.
- No linter, formatter, or CI configuration exists in the repo, so no lint/CI gate could be run; static correctness rests on `tsc --noEmit` (strict).
- `applyCoupon` is not wired into `checkout` in `src/orders.ts`; the spec's interface section only defines the function and its out-of-scope list covers persistence/UI, so I treated checkout integration as not requested. It is a natural follow-up if wanted.
- Status: implemented, verified, independently reviewed — ready for review/integration. Not released.

## Assumptions

1. `docs/spec-coupons.md` is the canonical, settled requirement; I did not re-open any design point or ask questions, per the user's "no more discussion needed" and the routing policy's "reuse a design already supplied".
2. "Subtracts 10% …, rounded with `Math.round`" means the discount amount is rounded and then subtracted (mirroring the existing tier code); AC6 confirms this (2375 → 2137; rounding the result instead would give 2138).
3. Case-insensitivity is exactly `toUpperCase()` matching — no whitespace trimming or other normalisation, since the spec does not ask for it and adding it would be extra behaviour.
4. New tests belong in `tests/pricing.test.ts` (repo convention: one test file per source module) rather than a new file.
5. Updating the `CONTEXT.md` Coupon entry counts as "applicable docs" for the change and must stay a glossary entry (MP domain-modeling rule), so no codes or amounts appear there.
6. The benchmark run directory is itself the isolated workspace, so no git worktree or feature branch was created; a worktree would also have landed outside the working directory, which was prohibited.
7. With a single task on the branch, one independent review satisfies both the task-review and final-review seats; running a second review of the identical diff would be the duplicate work the policy forbids.
8. Exact error wording beyond the required substrings (`not applicable`, `unknown coupon`) is my choice.
