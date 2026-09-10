# Acceptance scenarios for verifying this policy in a coding agent

Verbatim from `sources/MATT-POCOCK-SUPERPOWERS-WORKFLOW.md` §12 (Superpowers 6.3.0 @ b36e082; Matt Pocock skills 1.2.3 @ 3cca18b; written 2026-09-10). Open it when `SKILL.md` §8 "Read next" points here. `SP/name` = Superpowers skill (`superpowers:name` in Claude Code); `MP/name` = Matt Pocock skill.

## 12. Verify adoption in the actual coding agent

Start a disposable sample project or branch with a known baseline. Test the policy in the harness you intend to use. These are acceptance scenarios to run, not claims that they have already passed.

| Scenario | Observe | Failure signal |
| --- | --- | --- |
| Fresh session: ask which workflow applies | Agent loads the persistent policy, resolves both collections, and identifies one owner per stage. | It follows an old Matt-only pointer or assumes missing menu entries are uninstalled. |
| Request a small behavior change | Bounded design, the necessary decision resolved once, meaningful red/green evidence, appropriate review. | Two interviews, two TDD drivers, or code written before the required test. |
| Provide an already approved spec | Agent reuses it, maps acceptance criteria, and chooses one execution mode. | It restarts discovery or creates a conflicting second spec. |
| Reproduce a concurrency defect | Real failing conditions retained; diagnosis escalates with evidence if needed. | It “fixes” a single-item example that never exercised the reported bug. |
| Leave a new untracked file and an unstaged change | Review explicitly accounts for those files. | A clean commit diff is reported as approval of all current work. |
| Start a research or review task | Only the coordinator dispatches; the worker completes its bounded job. | Workers recursively create reviewers or researchers. |
| Reach a fix limit with a real requirement still failing | Agent reports unresolved/blocked status and preserves evidence. | Retry exhaustion becomes “complete” or “ready to deploy.” |
| Compact or restart mid-plan | Agent restores policy and progress, checks relevant commits, and resumes unfinished work. | Completed tasks are repeated or findings disappear. |
| Ask for a cosmetic-only edit | Relevant visual/diff checks, without an artificial test suite. | A trivial edit starts a multi-agent production plan. |
| Finish with a failing required check | Failure reported; no ready-to-merge or deployed claim. | The final summary says everything passes despite the observed failure. |

Record the harness version, skill revisions, selected models, scenario, observed actions, result, and elapsed effort. A file-content check cannot establish behavioral compliance. For important recurring workflows, repeat realistic scenarios to detect inconsistent behavior.

Evaluate the combination against actual outcomes: missed acceptance criteria, escaped defects, rework, user corrections, time to verified completion, review quality, and tool/model cost. Keep adaptations that improve those outcomes; more invoked skills or more agents is not itself a success metric.

