The coupon spec is implemented, tested, documented, and reviewed. Changes are left uncommitted in the working tree since a commit wasn't requested.

```text
Changed: applyCoupon(cart, code) added to src/pricing.ts per the approved spec; six spec-derived tests in tests/pricing.test.ts; CONTEXT.md Coupon entry updated (was "Not implemented yet").
Skills applied: matt-pocock-workflow (routing), tdd (+tests.md, mocking.md) for red→green slices at the spec's seam, domain-modeling (+CONTEXT-FORMAT.md) for the glossary edit, code-review (parallel Standards/Spec subagents, working-tree adaptation).
Verified: npm test → 21/21 pass (was 15); npm run typecheck → exit 0; each slice observed red before green except AC6, which was mutation-checked.
Remaining: none blocking; two review judgement calls deliberately left (see below).
```

# REPORT

## What changed

Working directory: `/Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-5-approved-spec/old_skill/run-1/workspace` (uncommitted; baseline commit `8576864` untouched; no untracked files).

- `src/pricing.ts` — added exported `applyCoupon(cart: Cart, code: string): number`. Computes `totalCents(cart)`, uppercases the code, then: `SAVE10` → `total - Math.round((total * 10) / 100)`; `FLAT5` → throws `Error("coupon … not applicable: subtotal must be at least 2000 cents")` when `subtotalCents(cart) < 2000`, else `total - 500`; anything else throws `Error("unknown coupon: …")`. `totalCents` is byte-identical to baseline.
- `tests/pricing.test.ts` — new `describe("coupons")` block with one test per acceptance criterion, all through the spec's seam (`applyCoupon` on carts from `createCart`/`addLine` via the existing `cartWithUnits` helper). Expected values are spec literals, not recomputed. The AC2 test uses the discriminating boundary (subtotal exactly 2000, post-tier total 1900) so a `total`-based threshold would fail.
- `CONTEXT.md` — Coupon glossary entry rewritten in the file's existing style: what it is, applied after the Tier discount, the two codes, case-insensitivity. No ADR (decision is spec-settled, reversible, unsurprising).

## Process (skills applied)

1. `matt-pocock-workflow` SKILL.md + `references/skill-catalog.md`, `workflow-rules.md`, `examples.md` read. Routing: clear feature with approved spec → `tdd` → `code-review`; `codebase-design` skipped (interface fixed by spec); `implement` is user-invoked and was not invoked, so not run.
2. `tdd` (Skill tool) + `tests.md` + `mocking.md`. Six vertical slices; each test written first and run:
   - AC1 red: `TypeError: applyCoupon is not a function` → green.
   - AC4 red: `expected [Function] to throw an error` → green.
   - AC2 red: `Error: unknown coupon: FLAT5` → green.
   - AC3 red: `expected [Function] to throw an error` → green.
   - AC5 red: `Error: unknown coupon: save10` → green.
   - AC6 green on arrival (implementation already stacks on `totalCents`); mutation check (rounding the total instead of the discount) produced `expected 2138 to be 2137`, then reverted → 10/10.
3. `domain-modeling` (Skill tool) + `CONTEXT-FORMAT.md` for the glossary edit.
4. `code-review` (Skill tool; Matt Pocock's `~/.claude/skills/code-review`, not the plugin). Fixed point `8576864` resolved; HEAD equals it, so the comparison used was `git diff 8576864` (fixed point → working tree) plus `git status --porcelain --untracked-files=all` (no untracked files). Spec source: `docs/spec-coupons.md`. Standards sources: `README.md`, `CONTEXT.md` (no CODING_STANDARDS/CONTRIBUTING/lint config) + smell baseline. Two parallel general-purpose subagents ran as read-only leaf tasks (first attempt failed only because the `name` parameter is disallowed for teammates; re-spawned without it).
   - **Standards:** 0 documented-standard violations; 3 judgement calls (inline rules vs. `TIERS` table precedent; two lines longer than the repo's prior max; possible duplicated "rounded percent" shape with `totalCents`).
   - **Spec:** 0 findings; interface, all six ACs, `totalCents` unchanged, and test seam confirmed.
   - Addressed: wrapped the two long lines (`src/pricing.ts` throw; shortened the AC2 test name). Deliberately not addressed: shared rounding helper (would require editing `totalCents`, which the spec pins as unchanged); `COUPONS` data table (two heterogeneous rules — a percentage and a conditional flat amount — don't justify it yet; would be speculative generality).

## What I verified (commands and observed results)

Run from the working directory:

- Baseline before edits: `npm test` → `Test Files 5 passed (5)`, `Tests 15 passed (15)`; `npm run typecheck` → clean, exit 0.
- Per-slice: `npx vitest run tests/pricing.test.ts` — red/green outputs listed above.
- Final: `npm test` → `Test Files 5 passed (5)`, `Tests 21 passed (21)`; `npm run typecheck` → `tsc --noEmit` clean, `typecheck exit: 0`. Run after the post-review line-wrap edits, so verification covers the final code.
- `git diff 8576864 --stat` → `3 files changed, 44 insertions(+), 2 deletions(-)`; `git status --porcelain --untracked-files=all` → only `CONTEXT.md`, `src/pricing.ts`, `tests/pricing.test.ts` modified.
- Longest lines after wrap: 105 chars (pre-existing `TIERS` comment), 98, 93.
- Mutation backup lived in the session scratchpad, not the project; source reverted and confirmed 10/10.

## What remains / could not be verified

- Nothing blocking. Changes are uncommitted (no commit was requested).
- `docs/agents/issue-tracker.md` does not exist; `code-review` mentions it, but no issue lookup was needed because the spec path was supplied directly. Not treated as a setup blocker.
- Two Standards judgement calls left open as noted above (rounding helper; rules-as-data). Both are refactors, not behaviour gaps.
- Case-insensitivity is tested with `save10` (the spec's example) only; `flat5` shares the single normalization and is not separately tested.

## Assumptions

- "`totalCents` is unchanged" was read as code-and-behaviour unchanged, so no refactor touched it.
- "Rounded with `Math.round`" means round the discount then subtract (matches `totalCents`'s existing pattern and the spec's 2137 worked example; rounding the total would give 2138).
- Error messages may carry detail beyond the required substrings ("contains" wording); messages include the code as entered.
- Tests belong in `tests/pricing.test.ts` (repo convention: one test file per module).
- The team lead's direction to follow `matt-pocock-workflow` overrides that skill's own note to prefer `matt-pocock-superpowers-workflow` when Superpowers is installed.
- Updating the stale `CONTEXT.md` Coupon entry is in scope as the documentation update the completion criteria require, even though the spec doesn't mention it.
