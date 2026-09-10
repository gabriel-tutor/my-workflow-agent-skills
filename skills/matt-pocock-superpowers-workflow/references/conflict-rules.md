# Conflict-resolution rules, review integration, and protecting pre-existing work

Verbatim from `sources/MATT-POCOCK-SUPERPOWERS-WORKFLOW.md` §4 (Superpowers 6.3.0 @ b36e082; Matt Pocock skills 1.2.3 @ 3cca18b; written 2026-09-10). Open it when `SKILL.md` §8 "Read next" points here. `SP/name` = Superpowers skill (`superpowers:name` in Claude Code); `MP/name` = Matt Pocock skill.

## 4. Explicit conflict-resolution rules

These are deliberate adaptations for the combined policy. They supersede overlapping lower-priority skill process instructions only after the user adopts this document. They never override tool permissions or invocation restrictions.

| Overlap in the supplied source | Combined decision |
| --- | --- |
| SP brainstorming asks one question at a time; MP grilling asks a round of independent questions. | SP owns the default design interview. Do not also run MP `grill-with-docs` or `grilling` automatically. If the user explicitly selects the MP interview, it replaces that interview; carry its approved decisions into the next stage without re-interviewing. |
| SP brainstorming and MP `to-spec` can both write a spec. | Maintain one canonical requirements source. Default to SP's approved design document. If MP tracker publication is explicitly requested, use it to publish/synthesize those same decisions, make the canonical source explicit, and link any local projection to it. Never maintain two independently edited specs. |
| MP tickets avoid fragile file paths; SP plans require exact paths and implementation detail. | Tickets describe durable behavior. A task's execution plan describes the current checkout. Link the plan to its ticket/spec and revalidate paths before execution. These are different document purposes. |
| MP TDD defers refactoring to review; SP TDD includes refactoring after green. | SP owns the test cycle. Use MP guidance for agreed test seams and assertion quality. Small behavior-preserving cleanup may follow green; larger structural refactors get their own agreed scope. Do not invoke both full TDD workflows for the same slice. |
| SP debugging tests one hypothesis at a time; MP diagnosis first generates several ranked hypotheses. | SP owns ordinary diagnosis. Escalate to MP for a difficult bug and hand over the evidence once. MP's ranked hypotheses are then tested individually. Do not restart a second diagnosis after every failed test. |
| MP `implement`, MP beta `implement-spec`, and SP execution skills all orchestrate coding. | SP owns execution by default. MP implementation orchestrators are alternate modes, selected explicitly by the user, never nested inside SP's coordinator. |
| SP SDD forbids concurrent implementation workers; MP beta `implement-spec` uses separate worktrees and concurrency. | Default to SP's sequential implementation model. Parallelize independent reading/research where permitted. To use MP's concurrent implementation graph, explicitly switch the whole execution mode and use separate worker worktrees. |
| Overlapping execution, research, and review skills can each dispatch subagents. | Only the coordinator dispatches review workers. Workers are leaf tasks. Use the review already required by the active execution owner; do not add another review seat for the same stage merely because another skill exists. |
| MP `code-review` uses `<fixed-point>...HEAD`, which excludes current uncommitted changes. | Confirm the complete review scope, including relevant staged, unstaged, and untracked files. Use a supported working-tree comparison or an authorized commit before a commit-based review. Empty diff never means uncommitted work was reviewed. |
| SP SDD can park findings at its retry limit and mark a task complete with rulings. | A retry cap bounds the attempt; it does not satisfy a failed requirement. Record “blocked” or “implemented with unresolved findings” where appropriate. Known correctness, security, data integrity, or acceptance failures block a ready-to-merge claim. |
| Broad skill wording can demand repeated questions, tests, or setup actions. | Reuse existing approvals and fresh evidence for the same source state and scope. Ask about unresolved decisions with material consequences. Repeat verification when code, environment, scope, or a required gate makes the prior evidence insufficient. |
| A skill's example assumes a CLI, model, test command, or framework. | Discover the actual tool and project contract. Do not copy unavailable model names, outdated command examples, or npm commands into a different package-manager project. |

### Review integration, precisely

For the default SP execution path, retain SP's task reviewer and final whole-branch reviewer. Add MP's evaluation criteria to those briefs:

- **Standards:** cite the relevant repository rule. Separate violations from code-smell judgment calls. Repository conventions override generic smell heuristics.
- **Spec:** identify missing, partial, incorrect, or extra behavior against a reachable requirement.
- Preserve SP's broader correctness, integration, security, and production-readiness questions when they apply to the change.

Reading MP's `code-review/SKILL.md` for these criteria is a reference consultation, not running its separate two-agent orchestration. Do not claim independent MP Standards and Spec reviewers ran unless they actually did. If the user explicitly requests standalone MP `code-review`, use that workflow as the selected review mode and avoid a duplicate SP review of identical scope.

### Protect pre-existing work

Skill instructions such as “delete and restart,” “stage everything,” or “clean up the worktree” apply only within the work the user has authorized and the agent actually owns. Preserve pre-existing code, user changes, other workers' files, and unique uncommitted artifacts. Track workspace provenance directly; a folder name alone does not prove ownership. Never reset or discard someone else's work to satisfy a workflow ritual.

