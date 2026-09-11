# Routing reference

Read this file when the bootstrap's table is not enough: the path is unclear, a phase has just ended, or the question is how Matt Pocock's skills fit together. The bootstrap's rules still apply.

## Matt Pocock's main flow (from `ask-matt`)

1. **Grill.** Run `grill`, plus `domain-modeling` when working in a repo (together they are Matt's `/grill-with-docs`). The interview sharpens the idea. Resolved terms go into `CONTEXT.md`, and hard-to-reverse decisions become ADRs.
2. **Prototype detour.** Take it when a question needs a runnable answer (state, logic, or UI). `prototype` builds throwaway code and keeps it on a `prototype/<name>` branch as a primary source.
3. **One session or several?**
   - **One:** run `implement` right here.
   - **Several:** run `to-spec`, then `to-tickets` (vertical slices with blocking edges), then `implement` one ticket at a time, with `/clear` between tickets.
4. **What `implement` does.** It runs `tdd` one slice at a time at the agreed seams, then typecheck, the full suite, `code-review`, and a commit.

Keep grill → spec → tickets in one context window. The spec and the tickets build on the grilling verbatim.

## On-ramps

- **Issues someone else wrote** → `/triage` (user-only). It moves issues to `ready-for-agent`, which `implement` later picks up. Never triage tickets that `to-tickets` produced.
- **A hard bug** → `diagnosing-bugs`. First build a tight feedback loop that goes red on this bug, then form 3–5 ranked hypotheses. Without the loop, don't form a theory. If there is no correct seam for the regression test, suggest `/improve-codebase-architecture`.
- **A huge, foggy effort** → `/wayfinder` (user-only). It charts a map of decision tickets and resolves one per session. When the way is clear, it hands off to `to-spec`.

## Upkeep

Run `/improve-codebase-architecture` (user-only) every few days. It reports deepening opportunities as an HTML file. Grill the candidate the user picks, and design it with `codebase-design` (its design-it-twice pattern explores alternative interfaces).

## Phase boundaries

A phase ends when a stage is done: the grilling, a ticket, or a review. At that point, ask these questions in order. The first yes wins.

1. **Continue** if the next phase needs this one verbatim, or if there is room left in the context (about 150k tokens).
2. **`/clear`** if nothing here matters to what comes next.
3. **`/handoff`** only for a new harness, a new directory, a colleague, or a side task forked mid-phase.
4. **Subagent** if the task can run while the user is away (review, research).
5. **`/compact`** otherwise, with an instruction about what to keep.

Mid-phase there is no decision to make: continue, or split the remaining work into subagents.

## Per-path notes

- **TRIVIAL:** no grill and no new tests unless behavior changes. `verification-before-completion` still applies before claiming it's done.
- **BUG:** show the ranked hypotheses before testing them. Write the regression test before the fix, at a seam that reproduces the real bug pattern.
- **SMALL:** the grill has only a few questions, but it still settles the seams. Offer `code-review` rather than running it.
- **FEATURE:** `implement` starts in a worktree via `using-git-worktrees`. `code-review` uses the branch's merge-base as its fixed point.
- **BIG:** each ticket is sized for one fresh context window. When all tickets are done, `finishing-a-development-branch` integrates the work.
- **Standalone skills:**
  - `research`: a background agent that reads primary sources and writes a cited Markdown file.
  - `resolving-merge-conflicts`: use when already mid-conflict. Resolve by intent, and never `--abort`.
  - `wizard`: a script for the steps only a human can take.
  - `prototype`, `codebase-design`, `domain-modeling`.

## Precondition

Run `/setup-matt-pocock-skills` once per repo. It configures the issue tracker, the triage labels and the domain-doc layout. `to-spec`, `to-tickets`, `code-review` and `triage` read `docs/agents/issue-tracker.md`.
