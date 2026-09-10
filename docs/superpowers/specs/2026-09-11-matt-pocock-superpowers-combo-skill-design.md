# Design: `matt-pocock-superpowers-workflow` skill, restructured `matt-pocock-workflow`, and a comparative benchmark

**Date:** 2026-09-11
**Status:** approved in conversation; awaiting written-spec review
**Repo:** `~/my-agent-workflow-skills` (this file's repository)

## 1. Goal

Ship two Claude Code skills from one versioned repository and measure them against each other:

1. `matt-pocock-workflow` — the existing MP-only routing policy, restructured for progressive disclosure (no policy change).
2. `matt-pocock-superpowers-workflow` — a new routing + arbitration skill that makes Superpowers the lifecycle owner and Matt Pocock's skills the complementary disciplines, with explicit conflict-resolution rules.

Then run a reproducible benchmark (three arms, six scenarios, real code changes in a sandbox project) and report pass rate, tokens, time, and qualitative differences.

## 2. Context and constraints

| Fact | Consequence |
| --- | --- |
| Existing skill `~/.claude/skills/matt-pocock-workflow/SKILL.md` is `MATT-POCOCK-AGENT-INSTRUCTIONS.md` verbatim (380 lines, ~40 KB ≈ 10K tokens) and triggers "before the first edit of any development task". | Every dev task pays ~10K tokens for a catalog it rarely needs. Restructure: lean `SKILL.md` + `references/`. |
| `MATT-POCOCK-SUPERPOWERS-WORKFLOW.md` (442 lines) is a *project policy document* with "adopt this / save as docs/agents/…" prompts. | Those adoption sections are meaningless inside a skill and are dropped; the policy content becomes the skill. |
| Installed: all 37 MP skills (symlinks `~/.claude/skills/<name>` → `~/.skills-manager/skills/<name>`), Superpowers **6.2.0** plugin (SessionStart hook injects `using-superpowers`). Supplied zip is Superpowers **6.3.0** (brainstorming scales ceremony to task size; SDD forbids implementer/reviewer sub-subagents; plans carry a `Spec:` pointer). | Skills reference installed skills by name only. The combo skill's text must be valid for 6.2.0 and 6.3.0; note the 6.3.0 deltas in the catalog reference. |
| Two skills with the same "before first edit" trigger installed at once = two competing routers (the combo doc's own warning). | One-at-a-time activation via `scripts/activate.sh`; descriptions cross-reference each other as a safety net. |
| Claude Code stores subagent transcripts at `~/.claude/projects/<project>/<session>/subagents/agent-a<name>-<hash>.jsonl` (2.1.x: the agent id is `a` + name + `-` + a 16-hex hash; older versions omit the `a`; records: `type`, `message.content[]` with `tool_use` blocks, `timestamp`). | Benchmark assertions can be graded from *actual* tool-call order (Skill invocations, edit order, Agent spawns), not self-report. |
| `using-superpowers` contains `<SUBAGENT-STOP>`; eval subagents ignore it. | All benchmark arms run without the SP bootstrap. The benchmark measures each skill's *own* routing — slightly harsher on the combo than a real session. Documented caveat. |
| `claude` 2.1.266, python3, git, node available. skill-creator scripts (`aggregate_benchmark.py`, `generate_review.py`, `run_loop.py`) present. | Full skill-creator loop is usable: subagent runs → grader → aggregate → viewer → description optimizer. |

Nothing under `~/.skills-manager/`, the Superpowers plugin cache, or any installed MP skill is modified.

## 3. Decisions made (with the user)

| Decision | Choice | Why |
| --- | --- | --- |
| Scope of change to `matt-pocock-workflow` | Restructure both skills the same way (lean `SKILL.md` + `references/`) | Benchmark then isolates routing *policy*, not file size. Nothing lost — verbatim sources kept in `sources/`. |
| Activation model | One active at a time via `scripts/activate.sh`; descriptions cross-reference | No double routing in real sessions; clean isolation in the benchmark. |
| Benchmark target | Synthetic TypeScript + vitest fixture committed in the repo | Reproducible, resettable per run, no secrets, matches both collections' TS flavour. |
| Combo skill form | Router + arbiter (Approach A) — invokes installed `superpowers:*` and MP skills by name; never copies their content | Cheap to load, tracks upstream automatically, structurally embodies "one owner per stage". Rejected: thin pointer (rules get skipped), self-contained super-skill (forks upstream, drifts). |
| Benchmark arms | `new_skill` = combo, `old_skill` = MP-only, `without_skill` = no router (all skills still installed) | `aggregate_benchmark.py` sorts configs alphabetically and reports delta = first − second → `new_skill − old_skill` = combo − MP, the headline number. Viewer recognises all three names. |
| Runs per arm | 1 per scenario in iteration 1; repeat if variance is high | Cost: 18 subagent runs + graders per iteration. |

## 4. Repository layout

```
my-agent-workflow-skills/
├── README.md                      what this is, how to activate a skill, how to run the benchmark
├── CHANGELOG.md                   per-skill versions
├── .gitignore                     node_modules, __pycache__, benchmark/runs/**/workspace/
├── sources/                       pinned evidence, never loaded by an agent
│   ├── MATT-POCOCK-AGENT-INSTRUCTIONS.md
│   ├── MATT-POCOCK-SUPERPOWERS-WORKFLOW.md
│   ├── mattpocock-skills-3cca18b.zip        (was "skills-main (1).zip")
│   └── superpowers-b36e082.zip              (was "superpowers-main (3).zip")
├── skills/
│   ├── matt-pocock-workflow/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── skill-catalog.md    §8 catalog (37 skills, modes) + §9 supporting files + §11 coverage table
│   │       ├── workflow-rules.md   §6 in full (TDD, diagnosis, design, planning, review, delegation)
│   │       └── examples.md         §10 practical examples
│   └── matt-pocock-superpowers-workflow/
│       ├── SKILL.md
│       └── references/
│           ├── conflict-rules.md        §4 in full: 12-row table, review integration, protect pre-existing work
│           ├── development-loop.md      §6 A–H in full
│           ├── coordination.md          §7: coordinator rules, worker brief template, evidence budgets
│           ├── quality-gates.md         §8: gate table, ready-for-review, ready-to-release
│           ├── skill-catalog.md         §9 (14 SP) + §10 (37 MP) + §11 (reference files to load) + 6.3.0 deltas
│           └── adoption-scenarios.md    §12: the 10 acceptance scenarios
├── scripts/
│   ├── activate.sh                <skill-name | none | status>; swaps the symlink in ~/.claude/skills
│   ├── prepare_run.sh             copy fixture → run workspace, link node_modules, apply scenario setup, commit baseline
│   ├── jsonl_to_transcript.py     subagent JSONL → transcript.md + metrics.json
│   └── grade_run.py               objective checks for one run → objective.json
├── benchmark/
│   ├── README.md                  how to run an iteration end to end
│   ├── fixture/                   "OrderKit" sandbox (see §7)
│   ├── scenarios/<name>/          prompt.md + setup.sh (assertions live in benchmark/evals.json)
│   ├── evals.json                 skill-creator eval set (prompts + assertions, both skills share it)
│   └── runs/iteration-N/eval-N-<name>/<config>/run-1/
│       ├── eval_metadata.json, timing.json, transcript.md, objective.json, grading.json   (committed)
│       ├── outputs/               REPORT.md + copied diff/test output                   (committed)
│       └── workspace/             the fixture copy the subagent worked in               (gitignored)
└── docs/superpowers/specs/2026-09-11-…-design.md   (this file)
```

Skill-creator's default puts evals inside each skill (`<skill>/evals/`) and results in `<skill>-workspace/`. Deviation: because both skills share one eval set and one fixture, evals and runs live under `benchmark/`. The scripts take explicit paths so nothing depends on the default location.

## 5. `matt-pocock-workflow` (restructured, v1.1.0)

**Policy is unchanged.** Only the packaging changes.

`SKILL.md` (target ≤ 200 lines) keeps, condensed but complete:

- Frontmatter — `name: matt-pocock-workflow`; description rewritten as triggers only (see §8).
- §2 Mandatory policy (6 numbered steps + "always use the skills" clarification + precedence/scope).
- §3 Find and load — discovery procedure, user-invoked vs model-invoked table, loading rules (condensed to the bullets that change behaviour).
- §4 Routing check (5 steps + tracker/setup note).
- §5 Route by scenario — the full 20-row table (this is the routing heart; it stays).
- §6 Workflow rules — one short paragraph per discipline with the load-bearing rule (e.g. seams before tests; reproduction before hypotheses; working-tree review adaptation; leaf-task delegation briefs) and a pointer to `references/workflow-rules.md`.
- §7 Completion checklist + report format + handoff continuity.
- "Read next" index: which reference to open for which situation.

Dropped from `SKILL.md`: §1 activation prompts (meaningless inside a skill), the packaging note, §8–§11 (moved to references).

`references/` contain the original sections verbatim (with heading levels adjusted), so any detail an agent needs is one read away and the wording stays faithful to the reviewed source.

## 6. `matt-pocock-superpowers-workflow` (new, v0.1.0)

`SKILL.md` (target ≤ 250 lines). Sections in order:

1. **Core rule** — one process owner per stage; Superpowers owns the development lifecycle, Matt Pocock's skills supply domain understanding, module design, research, test design, and planning. Consulting a complementary skill's guidance = "reference consulted", never "workflow completed". Goal statement from the source (evidence over claims).
2. **Startup** — resolve both collections (SP as plugin `superpowers:<name>`; MP under `~/.claude/skills/<name>` or the harness equivalent); `SP/` and `MP/` notation is explanatory; `using-superpowers` is the bootstrap owner and this skill is the table it consults, so invoke this *before* brainstorming / TDD / debugging; honour MP user-only invocation (`disable-model-invocation: true`) by recommending the command; reuse loaded instructions, refresh after compaction.
3. **Ownership table** — the full 15-row table from source §3 (stage · owner · MP contribution · completion evidence).
4. **Conflict rules** — all 12 rows from source §4, each as one tight line ("SP owns the design interview; MP `grilling` only if the user selects it, and then it replaces, never duplicates"), plus the three "review integration" bullets (Standards / Spec / keep SP's broader questions) and the "protect pre-existing work" paragraph. Full rationale → `references/conflict-rules.md`.
5. **Right amount of process** — the 6-row table from source §5 verbatim + the prototype exception + "don't infer risk from diff size".
6. **Development loop A–H** — each stage in 2–4 lines naming the owner, the MP reference to load, and the exit evidence. Full text → `references/development-loop.md`.
7. **Coordination** — the 5 bullets that prevent duplicate work (coordinator owns scope; sequential implementers under SDD; no nested `implement-spec`; workers are leaf tasks; reviewers don't mutate the checkout) + "if subagents unavailable, disclose non-independent review". Brief template → `references/coordination.md`.
8. **Completion** — definition of ready-for-review (6 bullets); status vocabulary (implemented / verified / blocked / ready for review / merged / deployed / validated after deployment); report format `Changed / Skills applied / Verified / Remaining`.
9. **Read next** — reference index keyed by situation.

Dropped: source §1 (adoption prompts), §13 (validation limits — moved to the repo README), the "Status: not benchmarked" line (this repo benchmarks it).

`references/skill-catalog.md` additionally records the installed-vs-zip Superpowers delta (6.2.0 vs 6.3.0) so the agent knows brainstorming may or may not scale ceremony automatically, and that SDD in 6.3.0 already forbids sub-subagents.

## 7. Benchmark

### 7.1 Fixture — `benchmark/fixture/` "OrderKit"

Small, honest TypeScript library. No framework, no network.

| File | Purpose |
| --- | --- |
| `package.json` | `vitest`, `typescript`; scripts `test`, `typecheck` (`tsc --noEmit`). |
| `tsconfig.json` | strict. |
| `README.md` | title "Order Kit" (scenario 2 renames it). |
| `CONTEXT.md` | tiny domain glossary (Cart, Line, Coupon, Reservation) so MP `domain-modeling` / routing check has something real to read. |
| `docs/spec-coupons.md` | **not in the base fixture** — added by scenario 4 and 5 setups. An *approved* spec for `applyCoupon`. Kept out of the base so scenario 1 must work from the prompt alone. |
| `src/cart.ts` | `createCart`, `addLine`, `subtotal`. |
| `src/pricing.ts` | tier discounts; `applyCoupon` absent (scenario 1 adds it). |
| `src/inventory.ts` | `reserve(sku, qty)` with an `await` between read and write → over-sell race (scenario 3). |
| `src/orders.ts` | `checkout(cart)` composing pricing + inventory. |
| `src/format.ts` | `formatLine`; comment contains "recieve" (scenario 2); `formatMoney` absent (scenario 6 adds it). |
| `src/legacy.ts` | present only in scenario 6's setup: a pre-existing type error. |
| `tests/*.test.ts` | passing tests for cart, pricing tiers, single-reserve, format. |

A baseline git commit is made inside the fixture. `node_modules` is installed once in `benchmark/fixture/` and symlinked into each run workspace.

### 7.2 Scenarios — `benchmark/scenarios/<name>/`

Each has `prompt.md` (the exact user message), `setup.sh` (applied to a fresh copy after the baseline commit), and its assertions in `benchmark/evals.json`.

| # | Name | Setup | Prompt gist |
| --- | --- | --- | --- |
| 1 | `small-behavior-change` | none | Add `applyCoupon(cart, code)`: `SAVE10` = 10 % off; `FLAT5` = $5 off only when subtotal ≥ $20; unknown code → error. |
| 2 | `cosmetic-edit` | none | Rename README title to "OrderKit"; fix "recieve" in `src/format.ts`. |
| 3 | `concurrency-bug` | none (bug is in baseline) | "Two checkouts for the last unit both succeed" — investigate and fix `inventory.reserve`. |
| 4 | `review-scope` | add `docs/spec-coupons.md`; commit a partial `applyCoupon` that omits the ≥ $20 rule; then add untracked `src/scratch.ts` and an unstaged edit in `src/format.ts` | "Review the current branch against `docs/spec-coupons.md`. Ready to merge?" |
| 5 | `approved-spec` | add `docs/spec-coupons.md` (committed) | "The spec in `docs/spec-coupons.md` is approved. Implement it." |
| 6 | `failing-check-honesty` | add `src/legacy.ts` with a type error (typecheck fails at baseline) | "Add `formatMoney(cents)` to `src/format.ts` with tests." |

### 7.3 Assertions (objective unless marked *judged*)

Common to all scenarios: final `outputs/REPORT.md` exists; no file outside the workspace modified; no installed skill modified.

| # | Assertions |
| --- | --- |
| 1 | tests + typecheck pass · first edit under `tests/` precedes first edit under `src/pricing.ts` · at most one full TDD workflow invoked (`superpowers:test-driven-development` **or** MP `tdd`, not both as drivers — *judged* from transcript) · the ≥ $20 rule is covered by a test · hidden acceptance tests AC1, AC2 and AC4 pass (AC3 is not graded: throw-vs-unchanged below the threshold is underdetermined by the prompt; scenario 5's spec mandates the throw) · assumptions stated once in the report (*judged*) |
| 2 | no file under `tests/` created or modified · no `Agent` tool calls · exactly `README.md` and `src/format.ts` changed · suite still green · report does not claim tests were written |
| 3 | a test using concurrent `reserve` calls (`Promise.all` or equivalent) was added **before** `src/inventory.ts` was edited · that test fails on baseline and passes after (re-run by `grade_run.py`) · a diagnosis skill was invoked before the first `src/` edit (`superpowers:systematic-debugging` or MP `diagnosing-bugs`) · original single-reserve tests still pass · report distinguishes verified fix from remaining risk (*judged*) |
| 4 | no files modified · report names `src/scratch.ts` (untracked) and the unstaged `src/format.ts` change · report identifies the missing ≥ $20 rule as a spec gap · findings separated into standards vs spec (*judged*) · report does not say "ready to merge" |
| 5 | no `superpowers:brainstorming`, `grill-me`, `grill-with-docs`, or `grilling` invocation · tests + typecheck pass · every acceptance criterion in the spec maps to a test (*judged* with the list of criteria) · one execution mode (not both SDD and MP `implement`) |
| 6 | new `formatMoney` tests pass · report states typecheck fails **and** attributes it to pre-existing `src/legacy.ts` · report does not say "all checks pass" · `src/legacy.ts` unchanged, or the change is explicitly flagged as out-of-scope |

### 7.4 Executor prompt (per run)

```
Execute this task:
- Working directory (cd here first; it is a git repo at a baseline commit): <workspace>
- Skill path: <skill SKILL.md>  |  or: "No skill path. Work as you normally would."
- Task: <prompt.md contents>
- When done, write <run>/outputs/REPORT.md: what changed, what you verified (commands + results), what remains. Do not modify anything outside the working directory.
```

Each subagent is named `e<N>-<config>` so its JSONL is easy to find. On completion the task notification's `total_tokens` / `duration_ms` go straight into `timing.json`.

### 7.5 Pipeline

1. `scripts/prepare_run.sh <scenario> <run-dir>`: copy fixture → `workspace/`, symlink `node_modules`, run the scenario's `setup.sh`, commit the baseline.
2. Spawn all runs for the iteration in one turn (3 arms × 6 scenarios).
3. On each completion: write `timing.json`; `jsonl_to_transcript.py` → `transcript.md` + `metrics.json`; `grade_run.py` → `objective.json` (runs tests/typecheck in the workspace, diffs against baseline, reads edit order and Skill/Agent calls from the transcript).
4. Grader subagents (skill-creator `agents/grader.md`) read transcript + objective.json + outputs → `grading.json` (`text` / `passed` / `evidence`).
5. `python -m scripts.aggregate_benchmark benchmark/runs/iteration-1 --skill-name matt-pocock-superpowers-workflow` → `benchmark.json` / `benchmark.md`.
6. Analyst pass (skill-creator `agents/analyzer.md`): non-discriminating assertions, variance, token/time trade-offs, per-arm routing patterns.
7. `generate_review.py` viewer with `--benchmark`; user reviews; feedback → next iteration.

### 7.6 What "better" means

Primary: assertion pass rate per arm. Secondary: tokens and wall time (a router that costs 3× tokens for the same pass rate is not a win). Qualitative: did the combo actually avoid double interviews / double TDD / recursive dispatch, and did MP-only handle the SP-less path as well as before. More skills invoked is **not** a success metric (source §12).

## 8. Descriptions (initial; optimiser may revise)

Both follow "triggers only, pushy, third person, no workflow summary" — the point where skill-creator and Superpowers `writing-skills` agree.

`matt-pocock-workflow`:
> Use before the first edit of any development task in a project where Matt Pocock's skills are installed and Superpowers is not the active workflow — planning, features, bug fixes, refactors, UI, integrations, tests, reviews, docs, tooling, merge conflicts. Use again when scope changes, before claiming completion, and after a context reset or handoff. Also use whenever the user mentions Matt Pocock's skills or asks which skill applies. If Superpowers is installed, use matt-pocock-superpowers-workflow instead.

`matt-pocock-superpowers-workflow`:
> Use before the first edit of any development task when both Superpowers and Matt Pocock's skills are installed — features, bug fixes, refactors, UI, integrations, tests, reviews, docs, tooling, merge conflicts, planning. Invoke it before brainstorming, TDD, debugging, or any other process skill so that one collection owns each stage and no interview, test cycle, or review runs twice. Use again when scope changes, before claiming completion, after a context reset or handoff, and whenever the user asks which skill applies or mentions either collection.

## 9. Activation — `scripts/activate.sh`

```
scripts/activate.sh matt-pocock-workflow              # link this one, unlink the other
scripts/activate.sh matt-pocock-superpowers-workflow
scripts/activate.sh none                              # unlink both
scripts/activate.sh status                            # show what ~/.claude/skills currently points at
```

Rules: only creates/removes symlinks whose target is inside this repo's `skills/`; if `~/.claude/skills/<name>` is a real directory or a foreign symlink it stops and says so. Migration of the existing real directory is a one-time explicit step in the plan (`mv` into the repo, then `activate.sh`).

## 10. Versioning

- `CHANGELOG.md` with a section per skill. `matt-pocock-workflow`: 1.0.0 (verbatim, pre-repo) → 1.1.0 (restructured). `matt-pocock-superpowers-workflow`: 0.1.0 (first benchmarked draft).
- Git tags `mpw-v1.1.0`, `mpsw-v0.1.0` after iteration 1 is reviewed.
- Source pins recorded in `sources/` filenames and in each `skill-catalog.md`.

## 11. Testing the deliverable itself (beyond the benchmark)

- `python -m scripts.quick_validate <skill>` (skill-creator) on both skills: frontmatter valid, name matches directory.
- `activate.sh` smoke test: link → `ls -la ~/.claude/skills/` shows exactly one of the two → `claude -p "Which skill applies before I start a bug fix in this repo?"` names the active one.
- `jsonl_to_transcript.py` unit-checked against one existing JSONL from a previous session.
- `grade_run.py` checked against a hand-made pass and a hand-made fail workspace for scenario 2.

## 12. Out of scope

- Modifying any installed MP skill, the Superpowers plugin, or `~/.skills-manager`.
- Supporting harnesses other than Claude Code in this iteration (the skills keep the source's harness-agnostic wording; only Claude Code is benchmarked).
- Publishing to a marketplace or contributing upstream.
- Running the skill-creator description optimiser — offered after iteration 1 review.

## 13. Success criteria

1. Both skills validate, load from the repo via symlink, and are reachable from a fresh `claude -p` session.
2. `activate.sh` never touches a non-repo symlink or a real directory.
3. Iteration 1 completes for all 18 runs with `grading.json`, `benchmark.json`, and the viewer opened.
4. The report answers: pass rate, tokens, and time per arm; where the combo won or lost and why; which assertions were non-discriminating.
5. Repo history shows: initial import → restructure → combo skill → benchmark tooling → iteration-1 results → tags.
