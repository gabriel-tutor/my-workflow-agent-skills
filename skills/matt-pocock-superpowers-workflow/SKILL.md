---
name: matt-pocock-superpowers-workflow
description: Use before the first edit of any development task when both Superpowers and Matt Pocock's skills are installed — features, bug fixes, refactors, UI, integrations, tests, reviews, docs, tooling, merge conflicts, planning. Invoke it before brainstorming, TDD, debugging, or any other process skill so that one collection owns each stage and no interview, test cycle, or review runs twice. Use again when scope changes, before claiming completion, after a context reset or handoff, and whenever the user asks which skill applies or mentions either collection. If only Matt Pocock's skills are installed, use matt-pocock-workflow instead.
---

# Matt Pocock + Superpowers: Combined Routing Policy

**Superpowers coordinates development. Matt Pocock's skills strengthen domain understanding, module design, research, test design, and planning. Every stage has exactly one process owner.**

Goal: software that satisfies explicit requirements, has meaningful verification, is maintainable, and is safe to operate within its agreed constraints. No skill bundle guarantees that — treat every quality claim as a statement that needs evidence.

Notation: `SP/name` is a Superpowers skill (`superpowers:name` in Claude Code); `MP/name` is a Matt Pocock skill. These are labels, not commands. Harness instructions, permissions, explicit user direction, and project requirements stay binding; within them, this policy resolves the overlaps between the two collections. If two instructions cannot be reconciled, name the conflict instead of pretending to follow both.

## 1. Startup

1. Resolve both collections. Superpowers is normally a plugin (`superpowers:*`); Matt Pocock's skills normally sit in the harness's skill directory (Claude Code `~/.claude/skills/<name>`, following symlinks). Verify provenance where names collide (`tdd`, `code-review`, `research`, `prototype`).
2. `SP/using-superpowers` is the bootstrap owner; this skill is the routing table it consults. Consult it **before** invoking brainstorming, TDD, debugging, or any other process skill. If the bootstrap did not load, say so and load permitted instructions explicitly for this session.
3. Check invocation metadata, subagent support, worktree support, test runners, and browser or integration tools. Use what the harness actually provides — never assume one harness's capability exists in another.
4. MP skills marked `disable-model-invocation: true` are user-only: recommend the exact command and its purpose; never auto-invoke, alter flags, or bypass the restriction through file access. A user-only skill absent from the menu may still be installed.
5. Load a skill's references before their branch of work, relative to the skill folder. Write project artefacts relative to the project — never into a skill folder. Reuse unchanged loaded instructions; refresh after compaction, a new session, or a skill update. Read only the relevant branches, not all 51 skills.

## 2. Ownership: who controls each stage

**One owner controls the sequence, approval points, and completion rule for a stage. Complementary skills supply defined inputs or references; they never start a second copy of that stage.** Run a complementary skill as a full workflow only when its own task is actually needed. When you read its guidance, say "reference consulted", not "workflow completed".

| Stage | Default process owner | Matt Pocock contribution | Completion evidence |
| --- | --- | --- | --- |
| Startup and skill selection | `SP/using-superpowers` with this policy | Verified MP catalog and invocation metadata | Correct skills resolved and loaded. |
| Requirements and design | `SP/brainstorming` | `MP/domain-modeling`, `MP/codebase-design`, focused `MP/research` and `MP/prototype` | Agreed behavior, scope, interfaces, and design. |
| Long-range decision planning | User-invoked `MP/wayfinder`, when needed | Its decision map and supporting research | Decisions sufficient to define a buildable scope. |
| Durable spec and issue breakdown | User-invoked `MP/to-spec` and `MP/to-tickets`, when tracker artifacts are needed | Behavioral requirements, vertical slices, and blockers | One canonical spec and agreed ticket graph. |
| Executable implementation plan | `SP/writing-plans`, for work needing a plan | Domain vocabulary, deep module design, ticket acceptance criteria | Tasks cover the spec and define interfaces, concrete edits, and checks. |
| Workspace isolation | `SP/using-git-worktrees` | Existing project conventions | Correct workspace, preserved user changes, known baseline. |
| Multi-task execution | `SP/subagent-driven-development` when permitted; `SP/executing-plans` for inline fallback | Domain/design references attached to each relevant brief | Implemented tasks, review evidence, and recoverable progress. |
| Production TDD | `SP/test-driven-development` | MP public-interface test guidance and `tdd/tests.md`, `tdd/mocking.md` | Relevant failing test before behavior change, then green. |
| Ordinary debugging | `SP/systematic-debugging` | MP domain context and design vocabulary | Evidence-supported cause and verified fix. |
| Difficult reproduction, concurrency, or performance diagnosis | `MP/diagnosing-bugs` as an explicit escalation | Tight reproduction loop, minimization, ranked hypotheses | Original failure resolved and regression protection or a stated gap. |
| Task and final review | SP execution/review workflow | MP Standards and Spec evaluation criteria | Review of the actual changes, actionable findings resolved. |
| Feedback evaluation | `SP/receiving-code-review` | Repo standards and domain/design context | Accepted fixes verified; rejected suggestions supported by evidence. |
| Completion claim | `SP/verification-before-completion` | Acceptance criteria from MP specs/tickets | Current verification tied to the final source state. |
| Integration and branch handling | `SP/finishing-a-development-branch` | `MP/resolving-merge-conflicts` if an authorized merge/rebase conflicts | Requested integration verified; work preserved appropriately. |
| Agent-facing documentation | `MP/writing-for-agents` | Clear triggers, steps, references, and completion criteria | An unambiguous instruction document. |

## 3. Conflict rules

Deliberate adaptations for the combination. They supersede overlapping lower-priority skill process text; they never override permissions or invocation restrictions. Rationale for each: `references/conflict-rules.md`.

1. **Design interview** — `SP/brainstorming` owns it. Never also run `MP/grill-with-docs` or `MP/grilling` automatically. If the user selects the MP interview, it replaces SP's; carry its approved decisions into the next stage without re-interviewing.
2. **One canonical spec** — SP's approved design document by default. `MP/to-spec` publishes or synthesises those same decisions when the user asks for tracker artefacts; make the canonical source explicit and link any projection to it. Never two independently edited specs.
3. **Tickets versus plans** — MP tickets describe durable behaviour and avoid fragile paths; SP plans describe the current checkout with exact paths. Link the plan to its ticket or spec and revalidate paths before execution. Different purposes, not a contradiction.
4. **TDD cycle** — `SP/test-driven-development` owns it; MP supplies agreed seams and assertion quality (`tdd/tests.md`, `tdd/mocking.md`). Small behaviour-preserving cleanup may follow green; larger structural refactors get their own agreed scope. Never run two full TDD workflows on one slice.
5. **Diagnosis** — `SP/systematic-debugging` owns ordinary bugs. Escalate to `MP/diagnosing-bugs` when reproduction itself is hard, the failure is intermittent or concurrent, or a performance baseline needs a tighter loop — hand over the evidence once; MP's ranked hypotheses are then tested individually. Do not restart a second diagnosis after every failed test.
6. **Execution orchestrators** — SP owns execution by default. `MP/implement` and the beta `MP/implement-spec` are alternate modes the user selects explicitly; never nest them inside SP's coordinator.
7. **Concurrency** — SP SDD runs implementation workers sequentially. Parallelise only independent reading and research. `MP/implement-spec`'s concurrent worktree graph is a whole-mode switch, chosen explicitly, with separate worker worktrees.
8. **Dispatch** — only the coordinator dispatches review workers; workers are leaf tasks. Use the review the active execution owner already requires; do not add another review seat for the same stage because another skill exists.
9. **Review scope** — `MP/code-review` diffs `<fixed-point>...HEAD`, which excludes uncommitted work. Confirm the complete scope, including relevant staged, unstaged, and untracked files, through a working-tree comparison or an authorised commit. An empty diff never means uncommitted work was reviewed.
10. **Retry caps** — SP SDD's retry limit bounds the attempt; it does not satisfy a failed requirement. Record "blocked" or "implemented with unresolved findings". Known correctness, security, data-integrity, or acceptance failures block a ready-to-merge claim.
11. **Repeated asks** — reuse existing approvals and fresh evidence for the same source state and scope. Ask about unresolved decisions with material consequences. Re-verify when code, environment, scope, or a required gate makes the prior evidence insufficient.
12. **Examples are not contracts** — discover the actual CLI, model, test command, and package manager. Never copy unavailable model names, outdated commands, or one package manager's commands into another's project.

**Review integration.** Keep SP's task reviewer and final whole-branch reviewer; add MP's criteria to their briefs — **Standards** (cite the relevant repository rule; separate violations from code-smell judgment calls; repository conventions override generic smell heuristics) and **Spec** (missing, partial, incorrect, or extra behaviour against a reachable requirement) — and preserve SP's correctness, integration, security, and production-readiness questions. Reading `MP/code-review/SKILL.md` for these criteria is a reference consultation, not its two-agent orchestration; never claim independent MP Standards and Spec reviewers ran unless they did. If the user explicitly requests standalone `MP/code-review`, it becomes the review owner and there is no duplicate SP review of the same scope.

**Protect pre-existing work.** "Delete and restart", "stage everything", and "clean up the worktree" apply only within work the user authorised and the agent actually owns. Preserve pre-existing code, user changes, other workers' files, and unique uncommitted artefacts; track provenance directly — a folder name does not prove ownership. Never reset or discard someone else's work to satisfy a workflow ritual.

## 4. The right amount of process

The skill check is mandatory; the amount of planning and verification follows the actual change.

| Work type | Minimum appropriate route |
| --- | --- |
| Human-facing copy, formatting, or static cosmetic change | Inspect context, make the edit, inspect the diff and relevant render/build result. No unrelated behavioral tests or multi-agent plan. |
| Small behavior change in an existing flow | Bounded design with the relevant decision approved, agreed test seam, TDD, focused review, verification. |
| New feature or subsystem | Approved design, canonical requirements, concrete plan, isolated execution, tests, task/final review, integration verification. |
| Bug | Diagnosis before fix, meaningful regression reproduction, relevant tests, review, original scenario rerun. |
| Authorization, billing, data migration, shared concurrency, or operationally sensitive change | Feature/bug route plus the specific security, data, failure, and operational checks in `references/quality-gates.md`. |
| Throwaway prototype | One explicit design question and agreed exploratory scope. Use MP's prototype branch. Production promotion is a separate implementation step with normal quality gates. |

**Prototype exception:** a user-requested or user-approved exploratory prototype is authorised without production TDD. Generated output and static configuration get generator or configuration checks; changed runtime behaviour still needs behavioural verification. Do not infer low risk from a short diff — one authorisation condition or retry limit can change critical behaviour — or high risk from file count alone when the change is mechanically verifiable.

## 5. Development loop

Full text and the pre-execution checklist: `references/development-loop.md`.

**A. Task contract** — read the request, applicable instructions, relevant code, existing changes, current verification commands, `CONTEXT-MAP.md` or `CONTEXT.md`, and relevant ADRs. Capture — in the task, spec, or plan, or briefly in conversation for a small task — the user-visible outcome and what is out of scope; observable acceptance criteria including failure behaviour; affected interfaces and external dependencies; agreed test seams and validation commands; the review baseline and the workspace being changed; any unresolved decision that prevents a correct implementation. Investigate facts yourself; bring a recommendation when a decision is needed; never re-ask a settled point.

**B. Design** — `SP/brainstorming` for new design decisions; reuse a design already supplied with an implementation request. Load `MP/domain-modeling` when terms or relationships are being resolved and `MP/codebase-design` when deciding a module's shape or test interface. For uncertainty that evidence can settle: `MP/research` for a narrow external fact grounded in primary sources; `MP/prototype/LOGIC.md` for state transitions or business logic the user needs to exercise; `MP/prototype/UI.md` for structurally different UI alternatives in the project's design system. Keep one interview active. Make material decisions and test seams concrete before asking for approval. Capture durable domain terms as they resolve; use ADRs selectively.

**C. Plan** — for a bounded task, proceed from the approved short design without manufacturing a large plan. For larger work, `SP/writing-plans` from the canonical approved design; MP ticket planning only when the user needs durable backlog units. Before execution confirm: every requirement has a task and a verification method; tasks agree about produced and consumed interfaces; shared files, data, and dependencies have an explicit ordering; the instructions fit the current checkout; constraints from the canonical spec reach worker briefs. Tracker-dependent MP workflows need the project's issue-tracker and label configuration — point the user to `setup-matt-pocock-skills` if it is missing and continue independent work.

**D. Workspace** — `SP/using-git-worktrees` when the selected execution mode needs isolation; detect existing isolation and native workspace tools; no nested or duplicate worktrees. Record the source baseline and run baseline checks; separate pre-existing failures from introduced ones — a failing baseline is a known limitation to resolve or account for, never permission to ignore new failures. Use the repository's package manager and lockfile; installing a dependency is a task-specific action, not a reason to upgrade packages.

**E. Implement one slice** — `SP/test-driven-development` owns the cycle: name the behaviour and the defect the test can catch → test at the agreed public interface using MP's seam discipline → derive expectations from the spec or hand-checked examples, independent of the implementation → run and observe the intended failure → implement the minimum → run the targeted check and relevant regressions → small behaviour-preserving cleanup with checks green. Consult `MP/tdd/tests.md`, `MP/tdd/mocking.md`, and `SP/test-driven-development/writing-good-tests.md`. Mock only a justified external boundary. No tests to hit a coverage number or because every private helper "must" have one. A pure refactor may begin with characterisation tests that pass on existing behaviour — a preservation baseline, not a fake regression; state which kind of evidence you have.

**F. Diagnose instead of guessing** — when a check fails, `SP/systematic-debugging` before proposing a fix: read the actual error, reproduce, compare working cases and recent changes, test one supported hypothesis with one changed variable. Escalate to `MP/diagnosing-bugs` per conflict rule 5, carrying the existing evidence; MP then owns the sequence — red-capable loop, minimise, rank falsifiable hypotheses, probe individually, fix, rerun the original scenario. If repeated fixes fail, revisit the model and architecture rather than trying more of the same. A missing regression seam is a documented gap, not permission to call the bug fully protected. Redact secrets from commands, logs, traces, and reports.

**G. Review with explicit scope** — the active SP review process with MP's criteria from §3. Pin the base before a task starts, keep all task commits in the review range, include current uncommitted work when relevant; reviewers read the real diff and required context, not the implementer's summary. `SP/receiving-code-review` before applying suggestions: verify claims against the code and requirements, fix valid blocking findings, support disagreement with concrete evidence — reviewer preferences do not create requirements. Re-review the fix and its effects, not the whole codebase. When a retry budget is exhausted, report the unresolved state and a concrete next option; a workflow limit does not waive the release gate.

**H. Verify, integrate, report** — `SP/verification-before-completion` on the final source state. `SP/finishing-a-development-branch` for the integration action the user's instructions cover; if direction is not explicit, present the prepared options when the work is ready. Pushing, merging, modifying shared environments, and messaging people stay within the user's authorisation — a release plan does not execute a release. `MP/resolving-merge-conflicts` may own conflict resolution inside an authorised merge or rebase: preserve each side's intent, run the checks on the integrated result, complete the operation. Report status precisely — implemented, verified, blocked, ready for review, merged, deployed, or validated after deployment are different states — with the evidence and remaining limitations.

## 6. Coordination without duplicate work

Use subagents only when the harness allows and the task benefits. Default SP SDD: a fresh implementer per meaningful task, one task reviewer covering spec and quality, scoped re-reviews, and a final whole-branch review. Worker brief template and evidence budgets: `references/coordination.md`.

- The coordinator owns scope, dependencies, workspace assignments, reviews, and integration.
- Under SP SDD, implementation workers run sequentially. Parallel investigations must be independently scoped and must not race on shared files, databases, ports, or mutable fixtures.
- Never nest `MP/implement-spec` inside SP SDD; its separate-worktree concurrency is an explicitly chosen alternative.
- Workers receive a brief — role, workspace and owned files, task/spec reference and acceptance criteria, required interfaces and constraints, skills and process owner, verification commands, report destination — and enough evidence to challenge a faulty plan. They do the assigned work directly and dispatch no coordinator, reviewer, or researcher of their own. This applies to MP research workers too.
- Reviewers inspect without changing the checkout under review; a separate revision uses an isolated location.
- Use models the harness actually has; match capability to difficulty rather than escalating every task to the most expensive tier.
- Preserve per-plan progress and findings across compaction; verify recorded completed work against the source state instead of repeating it from memory.

If subagents are unavailable, select the permitted inline execution mode, keep implementation and review as separate steps, and **disclose that review was not independent**. Never simulate separate reviewers in the report. Reuse completed verification only when it covers the same code state, inputs, environment, and scope; reviewers may request a focused rerun for a named doubt; the final integrated state still needs the required final checks. Track findings as fixed, disproven, accepted/deferred, or blocked — a concrete correctness or acceptance failure is never relabelled Minor to make the workflow pass. Before cleaning temporary coordination data, preserve unresolved findings, rulings, and unique evidence in a durable record.

## 7. Completion

The engineering gates neither bundle performs on its own — requirements mapping, static correctness, integration, UI and accessibility, authorisation and sensitive data, external contracts, schema and data changes, concurrency and performance, operations, release, post-release — and the evidence each needs: `references/quality-gates.md`. Neither collection replaces a security review, an accessibility evaluation, database expertise, infrastructure checks, or product acceptance. When a decision depends on an unknown threshold, propose a concrete target and resolve it; never claim an unmeasured SLA.

**Ready for review** means all of: the requested behaviour is implemented within scope · relevant checks ran on the current source state with results available · the actual diff was reviewed and blocking findings are resolved · every remaining limitation is explicit and correctly classified · applicable docs, configuration, and migration notes are updated · the user can inspect a concrete result and decide the next integration step.

**Ready to release** additionally requires the applicable CI, integration, security, data, operational, and product-acceptance gates. A known failed acceptance criterion, data-integrity defect, or material security issue blocks it. If the user changes scope or accepts a specific risk within permitted policy, record that decision and reassess the claim against the revised contract.

```text
Changed: <the outcome>
Skills applied: <SP owner per stage; MP references consulted; each with its concrete purpose>
Verified: <commands, observed results, and the exact review scope used>
Remaining: <specific limitation, or none>
```

## 8. Read next

| Situation | Open |
| --- | --- |
| Why a conflict rule exists, the precise review-integration rule, or the pre-existing-work rule in full | `references/conflict-rules.md` |
| The full A–H loop with its capture list and pre-execution checklist | `references/development-loop.md` |
| The worker brief template, evidence and review budgets, and the no-subagents fallback | `references/coordination.md` |
| Which extra gate applies (auth, data, concurrency, operations, release, post-release) and the evidence it needs; definitions of ready for review and ready to release | `references/quality-gates.md` |
| What each of the 14 Superpowers and 37 Matt Pocock skills does in this policy, their invocation modes, which reference file to load for which work, and the installed 6.2.0 vs 6.3.0 differences | `references/skill-catalog.md` |
| The ten acceptance scenarios that verify this policy in a harness | `references/adoption-scenarios.md` |
