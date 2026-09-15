# Routing reference

Read this file when the bootstrap's table is not enough: the path is unclear, a phase has just ended, or the question is how Matt Pocock's skills fit together. The bootstrap's rules still apply.

## Matt Pocock's main flow (from `ask-matt`)

1. **Grill.** Run `grill`, plus `domain-modeling` when working in a repo (together they are Matt's `/grill-with-docs`). The interview sharpens the idea. Resolved terms go into `CONTEXT.md`, and hard-to-reverse decisions become ADRs.
2. **Prototype detour.** Take it when a question needs a runnable answer (state, logic, or UI). `prototype` builds throwaway code and keeps it on a `prototype/<name>` branch as a primary source.
3. **One session or several?**
   - **One:** run `implement` right here.
   - **Several:** run `to-spec`, then `to-tickets` (vertical slices with blocking edges), then `implement` one ticket at a time. Each ticket ends with a handover that says whether to `/clear` before the next.
4. **What `implement` does.** It runs `tdd` one slice at a time at the agreed seams, then typecheck, the full suite, a commit, `code-review` on that commit, the definition of done, and a handover naming the stage reached.
5. **Past the merge.** `release` takes the integrated candidate to its target (readiness, a deploy behind an explicit yes, verification that the exact candidate runs, an operations handover). An outage goes to `incident`: contain and restore before diagnosis.

Keep grill → spec → tickets in one context window. The spec and the tickets build on the grilling verbatim.

## Greenfield

A new app starts with `foundations` (the run and verify commands, CI, the production rows), then the grill and `to-spec` with a Release section (target, environments, the first deploy). `to-tickets` makes ticket 01 the walking skeleton: one trivial path through build, CI, deploy and a smoke check, taken to the named environments through `release` before any feature ticket. Every later ticket then ships on a pipeline that already works.

## On-ramps

- **Issues someone else wrote** → `/triage` (user-only). It moves issues to `ready-for-agent`, which `implement` later picks up. Never triage tickets that `to-tickets` produced.
- **A hard bug** → `diagnosing-bugs`. First build a tight feedback loop that goes red on this bug, then form 3–5 ranked hypotheses. Without the loop, don't form a theory. If there is no correct seam for the regression test, suggest `/improve-codebase-architecture`.
- **Down or degraded for users now** → `incident`. Impact, then the safest reversible containing action behind a yes, restore, and only then `diagnosing-bugs`.
- **A huge, foggy effort** → `/wayfinder` (user-only). It charts a map of decision tickets and resolves one per session. When the way is clear, it hands off to `to-spec`.
- **Unsure where to start** → suggest `/ask-matt` (user-only), Matt's own routing; `/handoff` (user-only) writes the handoff for a new harness, directory or colleague.

## Upkeep

Run `/improve-codebase-architecture` (user-only) every few days. It reports deepening opportunities as an HTML file. Grill the candidate the user picks, and design it with `codebase-design` (its design-it-twice pattern explores alternative interfaces).

## Stage owners

- **Worktrees:** `using-git-worktrees` when feature work needs isolation from the current workspace; `implement` offers it at its gate.
- **Review feedback:** `receiving-code-review` before acting on any review finding: verify it against the code, then fix or push back with reasons.
- **Verify** and **finish** are in the bootstrap: `verification-before-completion` before any claim, `finishing-a-development-branch` on a branch.

## Durable state

The durable state is the spec, the tickets, `CONTEXT.md` and the ADRs (`docs/agents/issue-tracker.md` says where the first two live). A ticket resumed in a fresh context reads them and never relies on chat memory; what a phase decided and did not write down there is lost by design, so write it down there.

## Phase boundaries

A phase ends when a stage is done: the grilling, a ticket, or a review. At that point, ask these questions in order. The first yes wins.

1. **Continue** if the next phase needs this conversation: the spec needs the grilling verbatim, the tickets need the spec, a review fix needs the review.
2. **`/clear`** if the durable state holds what comes next and this context is mostly exploration and tool output.
3. **`/handoff`** only for a new harness, a new directory, a colleague, or a side task forked mid-phase.
4. **Subagent** if the task can run while the user is away (review, research).
5. **`/compact`** otherwise, with an instruction about what to keep.

Mid-phase there is no decision to make: continue, or split the remaining work into subagents.

## Evidence

Evidence belongs to a candidate. Evidence gathered on an unchanged candidate is reused, not re-run: two skills asking for the suite share one run, and `release` reuses what `implement`'s definition of done showed for the same SHA. Any change makes a new candidate, and only the checks it affects are re-run: the test file at one seam for a change in one place, the full suite and the typecheck when more than one file changed.

## Per-path notes

- **TRIVIAL:** the `trivial` declaration carries the test of what is not trivial; no grill and no new tests. `verification-before-completion` still applies before claiming it's done.
- **SENSITIVE:** any size. The grill runs the security and failure axes of the design lens; `code-review` is required, not offered.
- **BUG:** show the ranked hypotheses before testing them. Write the regression test before the fix, at a seam that reproduces the real bug pattern.
- **SMALL:** the grill has only a few questions, but it still settles the seams. Offer `code-review` rather than running it.
- **FEATURE:** `implement` starts in a worktree via `using-git-worktrees`. `code-review` uses the branch's merge-base as its fixed point.
- **BIG:** each ticket is sized for one fresh context window. When all tickets are done, `finishing-a-development-branch` integrates the work.
- **RELEASE:** `release` deploys nothing without a yes that names the target, the environment and the candidate, every time; an earlier "go all the way" never covers a deploy or a publish.
- **Standalone skills:**
  - `research`: a background agent that reads primary sources and writes a cited Markdown file.
  - `resolving-merge-conflicts`: use when already mid-conflict. Resolve by intent, and never `--abort`.
  - `wizard`: a script for the steps only a human can take.
  - `prototype`, `codebase-design`, `domain-modeling`.

## Alongside Superpowers

If Superpowers is also enabled, these win: `grill` over `brainstorming`, `tdd` over `test-driven-development`, `diagnosing-bugs` over `systematic-debugging`, `to-spec`/`to-tickets` over `writing-plans`, `code-review` over `requesting-code-review`. The gate enforces the precedence: a Superpowers skill is not a declaration, so the project stays closed until one of these has been invoked for the request.

## Precondition

Run `foundations` once per repo. It surveys what a well-run repo has (run and verify commands, lint, pre-commit hooks, CI, glossary, issue-tracker config, boundary rules, `.env.example`, the production rows), reports the gaps, and offers to close them through `/setup-matt-pocock-skills`, `setup-pre-commit` and `setup-ts-deep-modules`. `to-spec`, `to-tickets`, `code-review` and `triage` read `docs/agents/issue-tracker.md`.
