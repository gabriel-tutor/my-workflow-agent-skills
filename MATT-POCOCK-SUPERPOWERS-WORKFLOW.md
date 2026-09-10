# Matt Pocock + Superpowers: Combined Development Workflow

**Recommendation:** use Superpowers to coordinate development, and Matt Pocock's skills to strengthen domain understanding, module design, research, test design, and planning. Give every stage one process owner.

**Goal:** software that satisfies explicit requirements, has meaningful verification, is maintainable, and is safe to operate within its agreed constraints. No prompt, skill bundle, model, or test suite guarantees perfect software. Treat quality claims as statements that need evidence.

**Status:** a proposed project instruction policy based on inspection of the supplied archives. Its combined behavior has not been benchmarked in your six local coding agents. The adoption checks below make that limitation testable.

## 1. Adopt this policy

Drag this file into your coding agent and use this prompt:

```text
Adopt MATT-POCOCK-SUPERPOWERS-WORKFLOW.md as this project's combined
development policy, including its explicit conflict-resolution rules.

Matt Pocock's skills are already installed. Verify whether Superpowers
is installed and whether its startup instructions actually load.
Do not reinstall, update, fork, or modify either skill collection.

Save this document as docs/agents/development-workflow.md. Add a short
pointer from the persistent instruction file or always-applied rule
this coding agent actually loads. Preserve existing instructions.

If my previous Matt-only guide is active, keep it as a skill reference
and replace its workflow pointer with this combined policy. Do not run
two competing default workflows.

Report the resolved skill locations, the active instruction file,
and any missing capabilities. Then apply this workflow to my task.
Respect user-only skill invocation and the harness's permissions.
```

Suggested persistent pointer:

```markdown
## Development workflow

Before development work, after a context reset, and before completion,
read `docs/agents/development-workflow.md`. It assigns Superpowers the
development lifecycle and Matt Pocock the complementary disciplines.
Apply the relevant skills and explicit conflict rules. Use one owner
per stage. Report verification evidence before claiming completion.
```

This is a project instruction document, not a new installed skill or an upstream plugin modification. The policy becomes operative when the user adopts it. The routing and adaptations below are the user's project policy; they are not claims that either upstream author ships this combination.

Higher-priority harness instructions, permissions, explicit user direction, and applicable project requirements remain binding. Within that framework, this policy resolves overlaps between the two collections. If an instruction cannot be reconciled, state the specific conflict instead of silently pretending to follow both.

## 2. Discover capabilities before relying on them

### Skill locations supplied by the user

| Agent | Directory to inspect |
| --- | --- |
| Claude Code | `~/.claude/skills` |
| Codex | `~/.codex/skills` |
| Cursor | `~/.cursor/skills` |
| Gemini | `~/.gemini/skills` |
| Antigravity | `~/.gemini/antigravity/skills` |
| Deep Seek Harness | `~/.dsh/skills` |

These are lookup locations for this user's setup, not universal product defaults. Superpowers may live in a plugin or extension location instead. Inspect the active skill registry and installation configuration. Follow symlinks and consider configured project-local or shared skill locations, including `~/.agents/skills` where the installation actually uses it.

At session start:

1. Identify the active agent and repository. Keep the project directory, skill directories, and any isolated worktree distinct.
2. Resolve each required skill's actual file or native identifier. Verify provenance when names collide. In this guide, `SP/name` means a Superpowers skill and `MP/name` means a Matt Pocock skill. These are explanatory labels, not literal commands.
3. Verify that Superpowers' `using-superpowers` bootstrap is loaded through the installation's supported startup mechanism. Files on disk alone do not prove automatic activation. If it is unavailable, report the limit and load permitted instructions explicitly for the current session.
4. Check skill invocation metadata, subagent support, native worktree support, test runners, and relevant browser or integration tools. Use what the harness actually provides.
5. Invoke selected skills through the native skill mechanism. Where the harness supports file-based skills instead, read the complete permitted instructions and identify that loading method accurately. Load references before their branch of work.
6. Reuse unchanged instructions already present in context. Refresh after compaction, a new session, or skill updates. Read only the relevant reference branches, not all 51 skills on every turn.

For Matt's skills, `disable-model-invocation: true` and `policy.allow_implicit_invocation: false` mark user-only entry points in the inspected snapshot. Recommend the actual supported command when one is needed; do not auto-invoke it, alter its flags, or use file access to bypass a restriction. A user-only skill absent from the model-visible menu may still be installed.

Resolve source references relative to the skill folder. Write application artifacts relative to the project or the explicitly chosen workspace. Never write project specs, tests, or lessons into installed skill folders.

Native skill invocation, bootstrap behavior, and subagent support differ by harness. This guide does not assume that Deep Seek Harness or any other installation supports capabilities merely because another agent does.

## 3. Ownership: who controls each stage

**One owner controls the sequence, approval points, and completion rule for a stage. Complementary skills supply defined inputs or references. They do not start a second copy of that stage.**

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

Run a complementary skill as a workflow only when its own task is actually needed. If reading its guidance as a reference, say “reference consulted,” not “workflow completed.”

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

## 5. Choose the right amount of process

The skill check is mandatory. The amount of planning and verification follows the actual change.

| Work type | Minimum appropriate route |
| --- | --- |
| Human-facing copy, formatting, or static cosmetic change | Inspect context, make the edit, inspect the diff and relevant render/build result. No unrelated behavioral tests or multi-agent plan. |
| Small behavior change in an existing flow | Bounded design with the relevant decision approved, agreed test seam, TDD, focused review, verification. |
| New feature or subsystem | Approved design, canonical requirements, concrete plan, isolated execution, tests, task/final review, integration verification. |
| Bug | Diagnosis before fix, meaningful regression reproduction, relevant tests, review, original scenario rerun. |
| Authorization, billing, data migration, shared concurrency, or operationally sensitive change | Feature/bug route plus the specific security, data, failure, and operational checks in section 8. |
| Throwaway prototype | One explicit design question and agreed exploratory scope. Use MP's prototype branch. Production promotion is a separate implementation step with normal quality gates. |

**Prototype adaptation:** when the user requests or approves an exploratory prototype, that authorization covers its throwaway implementation without production TDD. This is the explicit prototype exception for this policy. Generated output and static configuration use an appropriate generator/configuration check; changed runtime behavior still needs behavioral verification.

Do not infer low risk from a short diff. A one-line authorization condition or retry limit can change critical behavior. Do not infer high risk solely from file count when a change is mechanically verifiable.

## 6. Run the development loop

### A. Establish the task contract

Read the request, applicable instructions, relevant code, existing changes, and current verification commands. Read `CONTEXT-MAP.md` or `CONTEXT.md` and relevant ADRs where present.

Capture the following in the existing task/spec/plan, or briefly in the conversation for a small task:

- The user-visible outcome and what is out of scope.
- Observable acceptance criteria, including relevant failure behavior.
- Affected interfaces and external dependencies.
- Agreed test seams and validation commands.
- The review baseline and the workspace being changed.
- Any unresolved decision that prevents a correct implementation.

Investigate facts yourself. Bring a recommendation when a user decision is needed. Use the latest explicit direction and prior approvals; do not ask the user to approve the same resolved point repeatedly.

### B. Design with the appropriate owner

Use `SP/brainstorming` for new design decisions. Reuse the design already supplied for an implementation request. Load `MP/domain-modeling` when terms or relationships are being resolved, and `MP/codebase-design` when deciding a module's shape or test interface.

For uncertainty that evidence can settle:

- Use `MP/research` for a narrow external fact, version contract, or technical comparison grounded in primary sources.
- Use `MP/prototype/LOGIC.md` for state transitions or business logic the user needs to exercise.
- Use `MP/prototype/UI.md` for structurally different UI alternatives, grounded in the project's design system.

Keep one interview active. Make material decisions and test seams concrete before asking for approval. Capture durable domain terms as they resolve. Use ADRs selectively for consequential, non-obvious trade-offs.

### C. Plan at two resolutions when necessary

For a bounded task, proceed from the approved short design without manufacturing a large plan.

For larger work, use `SP/writing-plans` from the canonical approved design. Use MP ticket planning only when the user needs durable backlog/sprint units. Each ticket is a complete behavioral slice; each plan task is an independently testable deliverable worth reviewing. A small test-writing action is a step, not automatically a separate ticket or worker.

Before execution, check:

- Each requirement is covered by a task and a verification method.
- Tasks agree about produced and consumed interfaces.
- Shared files, data, and dependencies have an explicit ordering.
- The instructions fit the current checkout.
- Constraints from the canonical spec are carried into worker briefs.

Tracker-dependent MP workflows need the project's issue-tracker and label configuration. If required configuration is missing, tell the user to invoke `setup-matt-pocock-skills`; continue independent work. Do not treat installation as repository setup.

### D. Prepare the workspace

Use `SP/using-git-worktrees` when isolation is needed by the selected execution mode. Detect existing isolation and use native workspace tools where available. Respect the user's existing preference; do not create nested or duplicate worktrees.

Record the source baseline and run relevant baseline checks. Separate pre-existing failures from introduced failures. A failing baseline is a known limitation to resolve or explicitly account for, never evidence that new failures can be ignored.

Use the repository's existing package manager and lockfile workflow. Installing dependencies is a task-specific action, not an automatic reason to upgrade packages.

### E. Implement one coherent slice

Use `SP/test-driven-development` as the cycle owner:

1. Name the behavior and the defect the proposed test can catch.
2. Test at the agreed public interface, using MP's seam discipline.
3. Derive expectations from the spec, hand-checked examples, or fixtures independent of the implementation.
4. Run the test and observe the intended failure.
5. Implement the minimum behavior needed to pass.
6. Run the targeted check and relevant regression checks.
7. Perform small behavior-preserving cleanup if useful, keeping the checks green.

Consult MP's `tdd/tests.md` and `tdd/mocking.md`, and SP's `test-driven-development/writing-good-tests.md`. Test real behavior; mock the external boundary when justified. Do not create tests merely to satisfy a numeric coverage target or a rule that every private helper must have its own test.

A pure refactor may start with characterization tests that pass on the existing behavior. They establish a preservation baseline, not a fake feature regression. New behavior and corrected defects require the appropriate failing evidence before the change. State which kind of evidence you have.

### F. Diagnose instead of guessing

When a check fails, use `SP/systematic-debugging` before proposing a fix. Read the actual error, reproduce, compare working cases and recent changes, and test a supported hypothesis with one changed variable.

Escalate to `MP/diagnosing-bugs` when reproduction itself is difficult, the failure is intermittent or concurrent, or a performance baseline needs a tighter loop. Carry the existing evidence forward. MP then owns the diagnosis sequence: build a red-capable loop, minimize, rank falsifiable hypotheses, probe individually, fix, and rerun the original scenario.

If repeated fixes fail, revisit the model and architecture rather than attempting more of the same. A missing regression seam is a documented gap, not permission to call the bug fully protected.

Redact secrets from commands, logs, traces, and reports. Prefer presence checks or redacted values when investigating configuration. Do not copy diagnostic examples that dump entire environments or authentication payloads.

### G. Review with explicit scope

Use the active SP review process, with MP's criteria as described in section 4. Pin the base before a task starts, preserve all task commits in its review range, and include current uncommitted work when relevant. Reviewers read the real diff and required context, not only the implementer's summary.

Use `SP/receiving-code-review` before applying suggestions. Verify claims against the code and requirements. Fix valid blocking findings; support disagreement with concrete evidence. Reviewer preferences do not create new requirements.

Re-review the fix and its effects. Do not restart a whole-codebase review for every minor adjustment. When a retry budget is exhausted, report the unresolved state and a concrete next option. A workflow limit does not waive the release gate.

### H. Verify, integrate, and report

Use `SP/verification-before-completion` on the final source state. Use `SP/finishing-a-development-branch` for the integration action covered by the user's instructions. If integration direction is already explicit, follow it; otherwise present the prepared options when the work is ready for that decision.

Publishing, pushing, merging, modifying shared environments, and messaging people must remain within the user's authorization. Producing a release plan does not execute a release.

If a merge/rebase conflicts, `MP/resolving-merge-conflicts` can own conflict resolution. Preserve each side's intended behavior, run the applicable checks on the integrated result, and complete the authorized operation.

Report the actual status using precise terms: implemented, verified, blocked, ready for review, merged, deployed, or validated after deployment. These are different states. Include the evidence and any remaining limitations.

## 7. Agent coordination without duplicate work

Use subagents only when allowed by the active harness and useful for the task. Default SP SDD uses a fresh implementer per meaningful task, one task reviewer covering spec and quality, scoped re-reviews, and a final whole-branch review. The inspected source's detailed templates govern this, even where a README uses an older description.

Rules for the combined policy:

- The coordinator owns scope, dependencies, workspace assignments, reviews, and integration.
- Under SP SDD, implementation workers run sequentially. Parallel investigations must be independently scoped and must not race on shared files, databases, ports, or mutable fixtures.
- Do not nest MP `implement-spec` inside SP SDD. Its separate-worktree concurrency model is an explicitly chosen alternative.
- Workers receive a task brief, relevant constraints/interfaces, needed skill pointers, and a report destination. Give them sufficient evidence to challenge a faulty plan; do not instruct them to suppress possible findings.
- Workers perform their assigned job directly. They do not dispatch another coordinator or reviewer. This also applies to MP research workers.
- Reviewers inspect without changing the checkout under review. If a separate revision is needed, use an isolated read/review location.
- Use models actually available to the harness. Match capability to task difficulty and follow applicable model-selection rules; do not invent supported model names or escalate every trivial task to the most expensive tier.
- Preserve per-plan progress and findings across compaction. Verify recorded completed work against the relevant source state instead of repeating it from memory.

A compact worker brief includes:

```text
Role and task:
Workspace and owned files:
Task/spec reference and acceptance criteria:
Required interfaces and project constraints:
Required skills/references and process owner:
Verification commands and evidence to record:
Report destination:

Perform this assigned work directly. Do not spawn additional agents.
Preserve unrelated changes. Report a missing fact or blocker explicitly.
```

If subagents are unavailable, select the permitted inline execution mode, retain separate implementation and review steps, and disclose that review was not independent. Never simulate the existence of separate reviewers in the report.

### Evidence and review budgets

Reuse completed verification when it covers the same code state, inputs, environment, and scope. Reviewers inspect that evidence and request a focused rerun for a named doubt. The final integrated state still needs the required final checks.

Track open findings through fixed, disproven, accepted/deferred, or blocked states. A concrete correctness or acceptance failure cannot be relabeled Minor to make the workflow pass. Non-blocking improvements can remain as explicit follow-up work.

Before cleaning temporary coordination data, preserve unresolved findings, rulings, their consequences, and unique evidence in a durable project record or final handoff. Do not delete the only record of a decision because the source code was committed.

## 8. Quality gates that the skill bundles do not supply by themselves

These are engineering checks added by this proposed policy, selected according to the actual change. They are not claims that either bundle automatically installs or performs them.

| Gate | Evidence to require when relevant |
| --- | --- |
| Requirements | Each acceptance criterion maps to implemented behavior and a verification result. |
| Static correctness | The project's formatter/linter, typecheck, and build checks pass on the final state. Record pre-existing noise separately. |
| Behavioral correctness | Meaningful tests of success, failure, and relevant edge cases at real interfaces. |
| Integration | Changed API, storage, queue, auth, and frontend paths work together in the representative environment. |
| UI and accessibility | Actual screen inspection, relevant viewport checks, keyboard behavior, labels/focus, and user-flow validation. A screenshot alone does not prove behavior. |
| Authorization and sensitive data | Tests for allowed and denied access, correct ownership/tenant boundaries, and safe treatment of secrets and sensitive fields where the change touches them. |
| External integrations | Contract and failure checks for the changed dependency, including malformed responses, timeouts, retries, or duplicate delivery where applicable. |
| Schema/data changes | Migration behavior tested against representative data; compatibility and recovery strategy documented. Use expand–migrate–contract when required. |
| Concurrency and performance | Measurements against agreed workloads and thresholds, including contention, duplicate work, resource growth, or rate limits implicated by the change. |
| Operations | Relevant logs/metrics, failure visibility, recovery behavior, configuration, and health checks are present and verified. |
| Release | Exact source/build identified, required CI checks satisfied, deployment/recovery steps prepared, and the user's release authorization followed. |
| Post-release behavior | If deployment is authorized, smoke checks and relevant monitoring verify the deployed state. Local success is not deployment evidence. |

Discover thresholds from the project's requirements. When a decision depends on an unknown threshold, propose a concrete target and resolve it; do not invent a performance promise or claim an unmeasured SLA.

Use specialist tooling and current primary documentation when the domain requires it. Neither skill collection replaces a security review, accessible UI evaluation, database expertise, infrastructure checks, or product acceptance.

### Definition of ready for review

- The requested behavior is implemented within scope.
- Relevant checks ran on the current source state, with results available.
- The actual diff has been reviewed and blocking findings are resolved.
- Any remaining limitation is explicit and correctly classified.
- Applicable docs, configuration, and migration notes are updated.
- The user can inspect a concrete result and decide the next integration step.

### Definition of ready to release

Ready for review is not sufficient. The applicable CI, integration, security, data, operational, and product-acceptance gates must also be satisfied. A known failed acceptance criterion, data-integrity defect, or material security issue blocks this status. If the user changes scope or accepts a specific risk within permitted policy, record that decision and reassess the claim against the revised contract.

## 9. All 14 Superpowers skills in this combination

| Skill | When it applies | Role in this policy |
| --- | --- | --- |
| `using-superpowers` | Session startup and skill routing | Bootstrap and discovery. |
| `brainstorming` | New or unresolved design/behavior decisions | Default design owner. |
| `writing-plans` | Approved multi-step work needing an execution plan | Concrete task planning. |
| `using-git-worktrees` | Isolation required before execution | Workspace preparation and baseline. |
| `subagent-driven-development` | Approved plan and permitted subagent capability | Default coordinated multi-task execution. |
| `executing-plans` | Inline plan execution when selected/permitted | Capability-aware fallback, not a simultaneous second coordinator. |
| `dispatching-parallel-agents` | Two or more truly independent investigations/tasks | Scoped parallel work compatible with the selected execution owner. |
| `test-driven-development` | Changed production behavior and defect fixes | Default test-cycle owner. |
| `systematic-debugging` | Failure or unexpected behavior | Default diagnosis owner. |
| `requesting-code-review` | Task, feature, and integration review stages | Review dispatch and whole-branch assessment. |
| `receiving-code-review` | Feedback arrives | Verify suggestions before changing code. |
| `verification-before-completion` | Any completion or passing claim | Evidence gate. |
| `finishing-a-development-branch` | Verified work needs integration handling | User-directed merge/PR/keep workflow. |
| `writing-skills` | Creating or modifying actual skills | Separate skill-authoring/evaluation workflow; not run for every application change. |

## 10. Where all 37 Matt Pocock skills fit

`M` means model or user invocation when appropriate. `U` means user-only entry in the supplied snapshot. Verify installed metadata before use.

| Skill | Mode | Combined use |
| --- | --- | --- |
| `ask-matt` | U | Optional advice about the MP catalog; this policy governs the combined default route. |
| `code-review` | M | Default: consult its Standards/Spec criteria. Full separate workflow only when selected as review owner. |
| `codebase-design` | M | Active reference for deep modules, interfaces, seams, adapters, and testability. |
| `diagnosing-bugs` | M | Escalated difficult-bug diagnosis, replacing the SP diagnosis driver for that investigation. |
| `domain-modeling` | M | Actively resolve domain language and maintain relevant glossary/ADRs. |
| `grill-with-docs` | U | Alternative design interview with domain documentation, explicitly selected by the user. |
| `implement` | U | Alternative simple MP implementation orchestrator; not nested with SP execution. |
| `improve-codebase-architecture` | U | Deliberate architecture survey, not a mandatory sweep after every change. |
| `prototype` | M | One-question UI or logic exploration before production implementation. |
| `research` | M | Focused primary-source research with a bounded leaf worker. |
| `resolving-merge-conflicts` | M | Intent-preserving resolution inside an authorized merge/rebase. |
| `setup-matt-pocock-skills` | U | Repository-specific tracker, label, and domain-doc setup when needed. |
| `tdd` | M | Its test references supplement SP TDD; full MP cycle only when the user selects MP as TDD owner. |
| `to-spec` | U | Publish/synthesize agreed requirements without creating a competing specification. |
| `to-tickets` | U | Durable vertical slices and blockers for multi-session delivery. |
| `triage` | U | Incoming requests and reports; not re-triage of already specified implementation tickets. |
| `wayfinder` | U | Large uncertain decision space before conventional specification and implementation. |
| `wizard` | M | Guided human-only setup procedure; never a substitute for steps the agent can perform. |
| `grill-me` | U | Optional interview for a plan without repository domain-doc work. |
| `grilling` | M | Interview primitive only under the selected MP interview/decision workflow. |
| `handoff` | U | Portable transfer between agents, workspaces, or teammates. |
| `teach` | U | Dedicated learning task; not automatically inserted into development. |
| `to-questionnaire` | U | Gather missing business facts from one stakeholder. Drafting does not authorize sending. |
| `wait-what` | U | Re-explain a confusing message with the missing context. |
| `writing-for-agents` | M | Agent instructions, briefs, and documents with clear triggers and completion rules. |
| `git-guardrails-claude-code` | M | Optional requested Claude Git-hook setup; verify scope. Non-promoted. |
| `migrate-to-shoehorn` | M | Requested TypeScript test-fixture migration. Test-only use. Non-promoted. |
| `scaffold-exercises` | M | Course exercise scaffolding with the required tooling. Non-promoted. |
| `setup-pre-commit` | M | Requested commit-hook setup, preserving existing tooling. Non-promoted. |
| `claude-handoff` | U | Beta Claude background-agent handoff, only with supported CLI capability. |
| `implement-spec` | U | Beta concurrent task-graph execution in separate worktrees; explicit alternative to SP SDD. |
| `loop-me` | U | Beta specification of recurring workflows/automations. |
| `retro` | U | Provisional environment-improvement suggestions; bucket README calls it a stub. |
| `setup-ts-deep-modules` | U | Beta dependency-cruiser enforcement of agreed TypeScript package interfaces. |
| `writing-beats` | U | Beta article development through selected narrative beats. |
| `writing-fragments` | U | Beta capture of raw writing material. |
| `writing-shape` | U | Beta shaping of raw material into an article. |

The four miscellaneous and eight beta skills are not in the supplied Matt Claude plugin bundle. Their presence in the source ZIP does not establish that the user installed them. The deprecated bucket contains no skill definitions.

## 11. Reference files to load on demand

| Selected work | Required relevant references |
| --- | --- |
| Cross-harness behavior | SP `using-superpowers/references/*-tools.md` for the active supported harness; actual tool registry wins over stale examples. |
| SP task execution | SP SDD `implementer-prompt.md`, `task-reviewer-prompt.md`, `re-review-prompt.md`, and referenced workspace/brief/review-package helpers. |
| Whole-branch review | SP `requesting-code-review/code-reviewer.md`; MP `code-review/SKILL.md` for the explicitly scoped supplementary rubric. |
| Tests | SP `test-driven-development/writing-good-tests.md`; MP `tdd/tests.md` and `tdd/mocking.md`. |
| Difficult module design | MP `codebase-design/DEEPENING.md`; `DESIGN-IT-TWICE.md` when alternative interfaces are needed. |
| Diagnosis | SP `systematic-debugging/root-cause-tracing.md`, `condition-based-waiting.md`, or `defense-in-depth.md` for the named issue; MP's HITL loop template when human reproduction is essential. |
| Domain changes | MP `domain-modeling/CONTEXT-FORMAT.md` and `ADR-FORMAT.md`. |
| Prototypes | MP `prototype/LOGIC.md` or `prototype/UI.md`; do not load both branches without need. |
| Architecture survey | MP `improve-codebase-architecture/HTML-REPORT.md`. |
| Tracker setup/triage | MP tracker templates, role mapping, `triage/AGENT-BRIEF.md`, and `OUT-OF-SCOPE.md`. |
| Human procedure | MP `wizard/template.sh`, inspected and adapted at the stage section. |
| Skill authoring | MP `writing-for-agents/SKILL-MECHANICS.md`; SP `writing-skills` and its evaluation references. |

Read helpers before running them. Do not run maintainer install/link/release scripts as part of routine application development. Repository contribution instructions govern contributions to that repository; they are not automatically rules for the user's products.

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

## 13. Source scope and validation limits

| Source | Snapshot inspected |
| --- | --- |
| `skills-main (1).zip` | Matt Pocock revision `3cca18b368ae95cdbdebbff572ccafa662551015`; package/plugin version `1.2.3` plus pending changesets; 164 files; 37 skill definitions. |
| `superpowers-main (3).zip` | Superpowers revision `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`; plugin version `6.3.0`; 195 files; 14 skill definitions. |
| GitHub repository | [obra/superpowers README](https://github.com/obra/superpowers/blob/main/README.md), accessed through the GitHub connector and public repository page on 2026-09-10. |

All 195 Superpowers archive files were inventoried and hashed; 194 decoded as text and one was binary. All 14 skill definitions were reviewed, together with the execution/review templates central to this comparison. The prior Matt review covered its 37 definitions, invocation metadata, and supporting material. The recommendation uses the supplied source bodies when summaries and READMEs differ.

This document was checked for catalog coverage and internal consistency. It was not installed into the user's local agents, and no application was built or deployed to benchmark the combined policy. Neither collection was modified. Follow the adoption scenarios to verify the behavior in the actual environment.
