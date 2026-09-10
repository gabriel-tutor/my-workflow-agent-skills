# Iteration 1 analysis

**Executor:** Opus 5 (1M), one run per eval per arm. **Grader:** Sonnet 5, one per run, reading the transcript plus `objective.json`. **Date:** 2026-09-11.
Arms: `new_skill` = `matt-pocock-superpowers-workflow`, `old_skill` = `matt-pocock-workflow`, `without_skill` = no routing skill (every skill still installed and invocable).

## Headline

| Arm | Graded | Objective | Tokens | Wall time | Tokens per passed expectation |
| --- | --- | --- | --- | --- | --- |
| combo (`new_skill`) | **35/35 (100 %)** | 34/34 | 21.8 M | 67 min | 622 K |
| MP-only (`old_skill`) | 34/35 (97 %) | 34/34 | 15.7 M | 60 min | 461 K |
| no router (`without_skill`) | 32/35 (91 %) | 31/34 | 3.7 M | 18 min | **117 K** |

Both routers beat the unrouted baseline on quality. The combo skill is the only arm with a perfect card, but it costs **5.8× the tokens** of no router and **1.4×** MP-only. Token figures include nested subagent usage (`scripts/nested_usage.py`); wall time is first-to-last transcript timestamp, inflated by 18 runs sharing the machine.

## Where the difference actually came from

Only two of six scenarios discriminated at all.

**3 — concurrency bug (the clearest win).** No router: 4/6. It produced a correct per-SKU lock and a real repro, but edited `src/inventory.ts` first (event 6) and wrote the regression test afterwards (event 10), with no diagnosis skill. Both routers: 6/6, test-before-fix and diagnosis-before-edit. The combo arm executed its conflict rule 5 literally — `superpowers:systematic-debugging` first, escalating to MP `diagnosing-bugs` when reproduction proved hard — and did it **without subagents** at 2.3 M tokens, where MP-only spent 3.5 M (incl. 0.8 M nested) on `code-review`'s two-reviewer orchestration. This is the single scenario where the combo's arbitration is visibly cheaper *and* better than MP-only.

**1 — small behavior change.** No router: 5/6 (code before test again). MP-only: 5/6 — everything green, but the grader judged the report never disclosed the rounding rule as an assumption, only as an implementation fact. Combo: 6/6, at 11.3 M tokens — by far the most expensive run in the benchmark, because it ran `brainstorming` on a task its own §4 sizing table calls a "small behavior change in an existing flow", then a dispatched reviewer, then a scoped re-review.

**2, 4, 5, 6 — non-discriminating.** Every arm scored full marks. Opus without any router already: fixed the cosmetic edit without inventing tests or subagents (2); caught the untracked file, the unstaged edit and the missing ≥ $20 rule and refused the merge (4); implemented the approved spec against all eight hidden acceptance criteria without restarting discovery (5); and reported the pre-existing typecheck failure honestly without an all-green claim (6). On these four the routers bought nothing but tokens — 2.3× (cosmetic), 2.4–3.5× (review), 6.4–8.1× (spec), 2.9–4.6× (honesty).

## Process observations from the transcripts

- **Combo skips ceremony correctly on cosmetic work.** Scenario 2: no interview, no TDD, no subagents — just the routing check, the edit, the diff, and `verification-before-completion`. The MP-only arm did the same. Neither over-processed a two-line change; that risk did not materialise.
- **Combo under-skips on small features.** Scenario 1 invoked `brainstorming` despite the sizing table. Superpowers 6.2.0 (installed) does not scale brainstorming ceremony to task size; 6.3.0 does. That single decision explains most of the 11.3 M tokens.
- **MP-only leans on subagents; combo mostly does not.** MP-only dispatched 3–4 subagents in five of six scenarios (`code-review`'s Standards + Spec reviewers); combo dispatched 0–2. Combo's conflict rule 8 ("only the coordinator dispatches") plus "reference consulted, not workflow completed" visibly held: it read MP's `code-review` criteria and applied them inline rather than running MP's orchestration.
- **No double-interview, double-TDD, or recursive dispatch was observed in any combo run.** The rules the policy exists to enforce all held.
- **The combo arm was the only one to reach `finishing-a-development-branch`** (scenario 5), correctly stopping to present integration options rather than acting.

## Assertion quality

- `report_exists` and `no_writes_outside_workspace` passed everywhere and are named by no expectation — informational only, as the grader brief says.
- Scenarios 2, 4, 5, 6 were non-discriminating at this model tier. To keep them, they need harder variants (e.g. review-scope should also require catching the AC5 case-insensitivity gap, which two graders flagged as uncovered; the honesty scenario's hidden tests cover only positive integers).
- Two graders warned that `report_mentions_*` checks are substring proxies a keyword-stuffed report could satisfy. They are backed by a judged expectation in every case, so the LLM layer covers them — but they should not be read as standalone evidence.
- The graders were *stricter* than the objective layer once (e1-mp 8/8 objective, 5/6 graded). That is the intended division of labour.

## Caveats

1. **n = 1 per cell.** Nothing here is statistically significant; the two discriminating scenarios are consistent with the routers' stated purpose, but a second iteration is needed before treating 100 % vs 91 % as real.
2. **Subagents ignore the `using-superpowers` SessionStart bootstrap** (`<SUBAGENT-STOP>`), so each arm was tested on its own routing text. In a real session the bootstrap would push toward Superpowers even in the no-router arm — the baseline here is therefore *harder* than reality for the routers.
3. **Wall time is contaminated** by 18 concurrent runs; token counts are the reliable cost metric.
4. **Grading regexes were tightened twice mid-iteration** (quoted-phrase handling in the all-green and merge-verdict checks) after real reports tripped them; all runs were re-graded with the final version.
5. The prompts told agents not to ask questions. Scenario 1's ambiguity (FLAT5 below threshold) was deliberately left unresolved and is not graded (AC3 excluded).

## Recommendation

For **bug work and anything where process order matters**, the combo skill earned its cost: it is the only arm that both diagnosed before editing and tested before fixing, and on scenario 3 it did so more cheaply than MP-only. For **routine feature work, cosmetic edits, reviews, and spec implementation on Opus**, no router matched it at a fifth of the tokens.

Two concrete changes before iteration 2:
1. Tighten the combo skill's §4 routing so a "small behavior change" does not reach `brainstorming` (the 6.2.0 gap) — the largest single cost in the benchmark.
2. Make scenarios 2, 4, 5, 6 discriminating or replace them; only 3 and 1 currently separate the arms.
