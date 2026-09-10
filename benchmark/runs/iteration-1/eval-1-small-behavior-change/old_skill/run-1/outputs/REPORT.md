Done. Working tree has the three intended files modified, nothing untracked, nothing committed (not asked).

```text
Changed: applyCoupon(cart, code) added to src/pricing.ts (SAVE10 = 10% off the tier-discounted total; FLAT5 = $5 off the tier-discounted total when the pre-discount subtotal is ≥ $20, otherwise unchanged; unknown codes throw), with the rounding rule extracted into one percentOfCents helper shared with totalCents; 7 coupon tests in tests/pricing.test.ts; CONTEXT.md Coupon entry updated.
Skills applied: matt-pocock-workflow (routing), tdd + tests.md/mocking.md (six red→green slices at the applyCoupon seam), domain-modeling + CONTEXT-FORMAT.md (glossary edit, no ADR), code-review (Standards and Spec sub-agents in parallel over git diff 69f75da).
Verified: npm test → 22/22 pass across 5 files; npm run typecheck → clean; 3 mutation checks each caught by the intended test.
Remaining: two spec ambiguities resolved by stated assumption (SAVE10 compounds on the tier discount; ineligible FLAT5 is a no-op, not an error).
```

# REPORT

## What changed

Working directory: `/Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-1-small-behavior-change/old_skill/run-1/workspace` (baseline `69f75da`, all changes uncommitted, no untracked files).

- `src/pricing.ts`
  - New exported `applyCoupon(cart: Cart, code: string): number`, returning integer cents. `SAVE10` subtracts 10% (rounded with `Math.round`) from `totalCents(cart)`; `FLAT5` subtracts 500 from `totalCents(cart)` when `subtotalCents(cart) >= 2000` (`FLAT5_MIN_SUBTOTAL_CENTS`) and otherwise returns the total unchanged; any other code throws `Error("unknown coupon code <code>")`.
  - Review-stage refactor: private `percentOfCents(amountCents, percent)` now holds the single `Math.round` rule; `totalCents` uses it (behaviour unchanged, covered by the existing tier tests). Tier logic (`TIERS`, `tierDiscountPercent`, `totalUnits`) is untouched.
- `tests/pricing.test.ts`: new `describe("coupons")` with 7 tests — SAVE10 basic (1000→900), SAVE10 rounding (1005→904), unknown code throws with the code in the message, FLAT5 at the $20 boundary (2000→1500), FLAT5 below threshold (1999→1999), SAVE10 on a 50-unit tiered cart (5000→4500→4050), FLAT5 on a 20-unit tiered cart (subtotal 2000 qualifies, 1900→1400).
- `CONTEXT.md`: Coupon entry no longer says "Not implemented yet"; it now states the two codes, the subtotal threshold, and that unknown codes are rejected, in the file's existing bullet style.

Skills applied per the routing policy: `matt-pocock-workflow` → `tdd` (with `tests.md`, `mocking.md`) → `domain-modeling` (with `CONTEXT-FORMAT.md`) → `code-review` (two parallel read-only sub-agents, Standards and Spec, briefed as bounded leaf tasks). `codebase-design` was not used because the request fixed the interface.

## What was verified

All commands run from the workspace directory.

- Baseline before edits: `npm test` → `Test Files 5 passed (5), Tests 15 passed (15)`; `npm run typecheck` → clean, exit 0.
- TDD red/green, observed via `npx vitest run tests/pricing.test.ts`:
  - Slice 1 red: `TypeError: applyCoupon is not a function` → green after adding SAVE10 (5 passed).
  - Slice 2 red: `AssertionError: expected [Function] to throw an error` → green after `default: throw` (6 passed).
  - Slice 3 red: `Error: Unknown coupon code: FLAT5` → green after FLAT5 case (7 passed).
  - Slice 4 red: `expected 1499 to be 1999` → green after adding the subtotal threshold (8 passed).
  - Slices 5 and 6 passed on first run (code already matched the spec), so I ran mutation checks with the file backed up to the scratchpad and restored afterwards (`diff` confirmed identical): base changed to `subtotalCents` → 2 failures (`expected 4500 to be 4050`, `expected 1500 to be 1400`); threshold changed to read the discounted total → 1 failure (`expected 1900 to be 1400`); `Math.round`→`Math.floor` → 1 failure (`expected 905 to be 904`). All restored; 11/11 in the file afterwards.
- Review: `git rev-parse 69f75da` → `69f75da3af57fbd057fce101b5bc84fa5ff1d063` (= HEAD); `git diff 69f75da...HEAD` empty (0 bytes), so the working-tree adaptation `git diff 69f75da` was the reviewed scope (3 files, no untracked). Standards: 0 hard violations, 3 judgement-call smells; Spec: 0 missing/creep/wrong findings, 22/22 tests and typecheck confirmed independently by the Spec sub-agent. Addressed: extracted the duplicated rounding rule; matched `cart.ts` lower-case error-message style; tightened the unknown-code assertion to `/coupon code BOGUS/` after a perl substitution briefly dropped `${code}` from the message (caught and fixed before final checks).
- Final on the reviewed code: `npm test` → `Test Files 5 passed (5), Tests 22 passed (22)`; `npm run typecheck` → clean, exit 0; `git status --short` → only `CONTEXT.md`, `src/pricing.ts`, `tests/pricing.test.ts` modified.

## What remains / could not be verified

- Nothing was committed (the task did not ask for a commit).
- `checkout` in `src/orders.ts` does not accept a coupon; the request's only concrete deliverable was `applyCoupon`, so wiring it into checkout was left out as scope creep. Easy follow-up if wanted.
- No issue tracker is configured (`docs/agents/issue-tracker.md` absent); the Spec review used the request text verbatim as the spec. `setup-matt-pocock-skills` was not required for this task.
- A direct `node` smoke run of the module failed only because the project uses extensionless imports (bundler resolution); vitest covers that path, so nothing is unverified as a result.
- The review sub-agents ran as plain subagents (the teammate `name` parameter was rejected once by the harness; the relaunch without it succeeded), so the two axes did run in parallel as the skill specifies.

## Assumptions

1. Coupons act on the total *after* the tier discount (CONTEXT.md: a Coupon "changes the total"; the request says "return the new total"), so SAVE10 compounds with the tier discount (50 units at $1.00 → 4050, not the additive 4000). The Spec reviewer agreed this is the better-grounded reading but flagged it as worth a one-line confirmation since it changes money.
2. FLAT5's $20 threshold is checked against the pre-discount Subtotal, as the request literally says; the $5 comes off the tier-discounted total.
3. FLAT5 below the threshold returns the total unchanged rather than throwing, because the request reserves throwing for unknown codes. Flagged as the other confirmable ambiguity; switching to a throw is a one-line change plus one test.
4. Codes are exact-match and case-sensitive (`"save10"` is an unknown code). No normalisation was added.
5. The function name `applyCoupon` is kept as specified even though the file's other money functions end in `Cents` (a Standards judgement call I declined because the name was given by the request).
6. No ADR was written: the ineligible-FLAT5 choice is trivially reversible, so it fails the "hard to reverse" criterion.
