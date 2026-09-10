Both sub-agent reports are consistent with my independent probe. Two light corrections applied while aggregating (marked as aggregator notes): nothing in the codebase calls `applyCoupon` yet, so the negative total is returned by the public function but does not currently reach `Order.totalCents`; and the glossary-drift finding has no written rule behind it, so it is a judgement call rather than a hard breach. The workspace is unchanged after the sub-agents ran.

# Verdict: not ready to merge

**Exact comparison used:** committed changes `git diff 3d147ba...HEAD` (one commit, `1c45102 feat: coupon codes (SAVE10, FLAT5)`; merge-base is `3d147ba` itself) **plus** the working tree: unstaged `src/format.ts` (`git diff`) and untracked `src/scratch.ts` (inspected directly). Nothing is staged. Spec source: `docs/spec-coupons.md`. Standards sources: `README.md`, `CONTEXT.md` (no `CONTRIBUTING.md`/lint config exists).

`npm test` (16/16) and `npm run typecheck` are green — but only because the single coupon test covers the one criterion that works.

## Standards

**Standards confirmed:** README.md ("All money is integer cents"), CONTEXT.md ("All money is integer cents. Rounding uses `Math.round`."; "**Coupon** — … Not implemented yet"). No lint/format config. `npm run typecheck` and `npm test` pass (16/16); tsc-enforced items skipped.

**Committed: `src/pricing.ts` (`applyCoupon`)**

Documented standards
- Money/rounding: compliant. `Math.round(base * 0.1)` and `base - 500` produce integer cents via `Math.round`.
- Documentation drift: CONTEXT.md still reads "Coupon — … Not implemented yet." README designates CONTEXT.md as the vocabulary source; this commit makes that entry false and doesn't touch it. No rule literally says "update the glossary", but the documented reference now contradicts the code. Fix: update the entry. *[aggregator note: the reviewer labelled this "hard"; since no written rule requires it, treat it as a judgement call — the contradiction itself is real.]*

Baseline smells (judgement calls)
- Possible Duplicated Code: `base - Math.round(base * 0.1)` repeats the shape of `totalCents`'s `subtotal - Math.round((subtotal * pct) / 100)`. Extract one `percentOffCents(cents, percent)` and call it from both.
- Inconsistent convention: the file expresses percentages as integers in a named, documented `TIERS` table (`percent: 10`); the new code inlines `0.1` and `500` in a `switch`. A `COUPONS` table mirroring `TIERS` would fix this and the possible Primitive Obsession for coupon definitions. (The `code: string` parameter is pinned by `docs/spec-coupons.md` — suppressed.)
- Naming note: cents-returning functions here are `*Cents` (`subtotalCents`, `totalCents`); `applyCoupon(): number` departs from that. The spec pins the name, so suppressed — raise with the spec owner, not the author.
- Doc comment omits "in integer cents" and the throw behaviour, unlike `totalCents`'s comment.

**Committed: `tests/coupons.test.ts`**
- Judgement call: existing convention is one `<module>.test.ts` per source module; `pricing.ts` is now tested from two files. Consider folding into `pricing.test.ts`.
- Judgement call: only the `SAVE10` branch is exercised; `FLAT5` and the `default` throw aren't. Existing tests cover every branch of their modules (pricing 0/5/10; checkout all three outcomes).

**Committed: `docs/spec-coupons.md`** — nothing to flag.

**Unstaged: `src/format.ts`**
- Not a standards breach; judgement call. Adds `TODO: tidy this comment.` to an exported function's JSDoc (leaks into hover text) while leaving the typo it refers to (`recieve`). Unrelated to the coupon feature — Divergent Change if it rides along. Fix the typo and drop the TODO, or revert the hunk.

**Untracked: `src/scratch.ts`**
- `export const scratch = 1;` — possible Mysterious Name / dead code; nothing imports it. It lives under `src/`, which tsconfig `include`s, so it typechecks into the library. Delete it (or keep it out of `src/`) before any `git add -A`.

## Spec

Verified by bundling `src/pricing.ts` to the scratchpad and probing each criterion; the suite (`npm test`, 16 tests) passes only because the one coupon test covers the one criterion that works.

**(a) Missing or partial requirements**

1. **AC2/AC3 — FLAT5 eligibility gate is absent.** Spec: "`FLAT5` subtracts 500 cents ... **only when the cart subtotal (before the tier discount) is at least 2000 cents**" and "on a cart whose subtotal is below 2000 cents throws an `Error` whose message contains `not applicable`." `src/pricing.ts:32-33` unconditionally returns `base - 500` and never calls `subtotalCents`. Observed: subtotal 1999 → 1499; subtotal 300 → **-200**; empty cart → **-500**. Negative totals violate the domain invariant ("All money is integer cents"). *[aggregator note: nothing calls `applyCoupon` yet — `checkout` still uses `totalCents` — so the negative value is returned by the public API but does not currently reach `Order.totalCents`.]*

2. **AC5 — case-insensitivity not implemented.** Spec: "Codes are case-insensitive: `save10` behaves like `SAVE10`." `switch (code)` at `pricing.ts:29` compares raw input. Observed: `save10` → throws `unknown coupon: save10`; `Flat5` → throws.

3. **Test coverage at the stated seam** ("Tests exercise `applyCoupon` through the public module interface with carts built via `createCart` / `addLine`"). `tests/coupons.test.ts` has one test, correctly at the seam, covering AC1 only:

| AC | Covered |
|---|---|
| 1 SAVE10 10% | yes |
| 2 FLAT5 when subtotal ≥ 2000 | no |
| 3 FLAT5 below 2000 throws `not applicable` | no |
| 4 unknown code throws `unknown coupon` | no |
| 5 `save10` ≡ `SAVE10` | no |
| 6 stacking example 25×100 → 2137 | no |

AC2, AC3 and AC5 tests would fail today; AC4 and AC6 would pass but are unasserted.

**(b) Scope creep / unrequested changes**
- **`src/format.ts` (uncommitted, unstaged):** JSDoc edit appending "TODO: tidy this comment." Spec touches only `src/pricing.ts` ("`applyCoupon(...)`, exported from `src/pricing.ts`"; "Out of scope: ... UI"). Unrelated to coupons; should be dropped or committed separately.
- **`src/scratch.ts` (untracked):** `export const scratch = 1;` — referenced nowhere, not in the spec, and inside `tsconfig` `include: ["src"]` so it would ship if `git add -A` is run. Delete.
- Committed diff itself contains no extra behaviour; `totalCents` is unchanged as required ("`totalCents` is unchanged").

**(c) Implemented but wrong**
- **AC2 FLAT5** looks implemented but is incorrect for the below-threshold case (see a.1) — it silently discounts instead of throwing.
- Correct as-is: AC1 (`Math.round(base * 0.1)`, verified 9000), AC4 (message `unknown coupon: X`), AC6 (verified 2137, stacking after tier), interface/signature/export location.

## Summary

Standards: 8 findings (1 documentation drift, 7 judgement calls); worst is `src/scratch.ts` — dead code under `src/` that would ship on the next `git add -A`. Spec: 5 findings; worst is the missing `FLAT5` subtotal gate (AC2/AC3), which returns negative totals instead of throwing `not applicable`.

**What has to happen before merge:** implement the `FLAT5` ≥ 2000-subtotal gate with the `not applicable` error (AC2/AC3), normalise code case (AC5), add seam-level tests for AC2–AC6, revert or separate the `src/format.ts` comment edit, delete `src/scratch.ts`, and update the `Coupon` entry in `CONTEXT.md`. The table-driven `COUPONS` refactor and folding the test into `pricing.test.ts` are optional.

---

```text
Changed: nothing — review only, no files in the workspace were created, modified, or staged.
Skills applied: matt-pocock-workflow (routing: classified as a review, pinned baseline and working-tree scope); code-review (Matt Pocock's, ~/.claude/skills/code-review — two-axis Standards/Spec review via two parallel read-only sub-agents, aggregated above).
Verified: see # REPORT below.
Remaining: docs/agents/issue-tracker.md is absent (harmless here — the spec path was supplied directly; run setup-matt-pocock-skills only if you want tracker-linked reviews later). Baseline 3d147ba was assumed, not user-confirmed.
```

# REPORT

**What changed:** Nothing in the workspace. This was a read-only review. Final `git status --short` is identical to the starting state: ` M src/format.ts` and `?? src/scratch.ts` (both pre-existing, both part of the review scope, neither touched). One throwaway probe was written to the session scratchpad (`/private/tmp/claude-501/.../scratchpad/coupon-probe/probe.ts`), outside the workspace.

**What I verified (commands run in `/Users/gabrieltutor/my-agent-workflow-skills/benchmark/runs/iteration-1/eval-4-review-scope/old_skill/run-1/workspace`):**
- `git rev-parse 3d147ba` → `3d147ba00aa2a4d13a25bf4a0e0980b63b571640` (fixed point resolves; `git merge-base 3d147ba HEAD` is the same SHA).
- `git log 3d147ba..HEAD --oneline` → `1c45102 feat: coupon codes (SAVE10, FLAT5)` (single commit, no issue reference).
- `git diff 3d147ba...HEAD --stat` → `docs/spec-coupons.md +22`, `src/pricing.ts +13`, `tests/coupons.test.ts +10`; 65 diff lines; `totalCents` untouched.
- `git status` / `git diff` / `git diff --cached` / `git ls-files --others --exclude-standard` → unstaged one-line JSDoc change in `src/format.ts`; untracked `src/scratch.ts` (`export const scratch = 1;`); nothing staged.
- `npm test` → `Test Files 6 passed (6)`, `Tests 16 passed (16)`.
- `npm run typecheck` → `tsc --noEmit` produced no errors.
- Scratchpad probe bundled with `npx rolldown probe.ts --format esm --file probe.mjs` (run from the workspace so it resolves the workspace's `node_modules`), executed with `node probe.mjs` → 5 of 11 checks failing, exit 1: AC3a (subtotal 1999 + FLAT5 returned 1499, no throw), AC3b (subtotal 300 + FLAT5 returned -200), AC5a/b/c (`save10`, `Save10`, `flat5` all throw `unknown coupon: …`). Passing: AC1a/b (9000; rounding case 904), AC2a/b (1400 at the 2000 boundary; 4500), AC4 (`unknown coupon: BOGUS`), AC6 (2137).
- `grep -rn "applyCoupon\|scratch" src tests` → `applyCoupon` is referenced only by its definition and `tests/coupons.test.ts`; `scratch` is imported nowhere; `src/orders.ts` still uses `totalCents`.
- Two parallel `general-purpose` sub-agents (Standards, Spec) ran read-only briefs; their reports are reproduced above and agree with the probe. `git status --short` after they finished was unchanged.
- Search for standards sources (`find` for CODING_STANDARDS/CONTRIBUTING/CLAUDE.md/AGENTS.md/eslint/prettier/biome/vitest config) → none; `docs/agents/` does not exist.

**What remains / could not be verified:**
- No issue-tracker configuration exists (`docs/agents/issue-tracker.md`), so step 2.1 of `code-review` (fetch the originating issue) was skipped; the user-supplied spec path was used instead.
- No merge target branch exists (the work is on `main` itself, two commits total), so "ready to merge" was evaluated as "ready to ship against the approved spec", not as a mergeability check against another branch.
- Running `npm test` uses the fixture's symlinked `node_modules` (a `.vite` cache directory already existed there before this run).

**Assumptions:**
- Review baseline is `3d147ba` ("baseline: OrderKit fixture"), the only fixed point on the branch; the orchestrator's no-questions rule meant I pinned it rather than asking, as the skill would otherwise require.
- "The current state of this branch" includes the uncommitted working tree, so the `src/format.ts` edit and `src/scratch.ts` were reviewed as part of the change set.
- `docs/spec-coupons.md` is the sole acceptance source; `README.md` and `CONTEXT.md` are the only documented standards, with the skill's Fowler smell baseline applied as judgement calls.
