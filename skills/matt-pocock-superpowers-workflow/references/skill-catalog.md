# Skill catalog: 14 Superpowers skills, 37 Matt Pocock skills, and reference files

Verbatim from `sources/MATT-POCOCK-SUPERPOWERS-WORKFLOW.md` §9–§11 (Superpowers 6.3.0 @ b36e082; Matt Pocock skills 1.2.3 @ 3cca18b; written 2026-09-10). Open it when `SKILL.md` §8 "Read next" points here. `SP/name` = Superpowers skill (`superpowers:name` in Claude Code); `MP/name` = Matt Pocock skill.

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


## Installed-version notes (Claude Code, checked 2026-09-11)

The locally installed Superpowers plugin is **6.2.0**; the archive this policy was written from is **6.3.0**. Differences that affect routing:

- 6.3.0 `brainstorming` classifies requests as spike / bounded / architectural and scales ceremony accordingly; 6.2.0 always runs the full design flow. Under 6.2.0, apply this policy's process-sizing table yourself.
- 6.3.0 `subagent-driven-development` forbids implementers and reviewers from spawning their own subagents, batches small same-shape tasks into one dispatch, and reads a `Spec:` pointer from the plan. Under 6.2.0, conflict rule 8 (only the coordinator dispatches) is the operative guard.
- 6.3.0 `finishing-a-development-branch` stops and asks instead of force-removing a worktree that still holds uncommitted work. Under 6.2.0, the "protect pre-existing work" rule is the operative guard.
- `test-driven-development`, `systematic-debugging`, `verification-before-completion`, `receiving-code-review`, `executing-plans`, `dispatching-parallel-agents`, and `using-git-worktrees` are unchanged between the two versions.

Re-check after a plugin update: `ls ~/.claude/plugins/cache/superpowers-marketplace/superpowers/`.
