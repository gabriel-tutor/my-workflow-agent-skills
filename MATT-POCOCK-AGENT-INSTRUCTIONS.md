# Matt Pocock Skills: Coding Agent Instructions

Use this file as standing development instructions for the coding agent. The skills are already installed. This file explains how to discover them, select the right ones, and apply their actual instructions throughout development.

**Source:** the supplied `https://github.com/mattpocock/skills`, archive revision `3cca18b368ae95cdbdebbff572ccafa662551015`, inspected on 2026-09-10. Its package and plugin manifests declare version `1.2.3`; it also contains pending changesets. This guide describes that snapshot, not a claim about the latest upstream release.

## 1. Activate these instructions

When the user supplies this file as instructions, apply the agent policy in sections 2–7 immediately for the current development session. Section 8 is the complete skill reference; sections 9–11 explain supporting files, practical examples, and source coverage.

An attachment supplies conversation context. It does not, by itself, configure every future session. For persistent use, keep this document in the project and add an explicit pointer from the instruction file or always-applied rule that the active agent actually loads.

### Copyable activation prompt

```text
Read MATT-POCOCK-AGENT-INSTRUCTIONS.md and apply it throughout this project.
Matt Pocock's skills are already installed. Discover their actual locations,
check their invocation metadata, and use every applicable model-invoked skill
before the corresponding development work. Tell me when a user-invoked skill
requires a command from me. Do not reinstall or modify the installed skills.

Save this document as docs/agents/matt-pocock-workflow.md and add a pointer
from the persistent instructions or always-applied rule this agent actually
loads. Preserve existing instructions and avoid duplicate rule blocks.
Report the instruction file you updated, the resolved skill location,
and any missing prerequisite. Then continue my development task.
```

Suggested persistent pointer, adjusted if the document is stored elsewhere:

```markdown
## Matt Pocock development workflow

Before every development task, meaningful change of scope, and completion
review, read `docs/agents/matt-pocock-workflow.md` and apply its routing policy.
Invoke the applicable installed Matt Pocock skills and load their required
references before doing the work. Respect user-only invocation metadata.
Repeat this check after a context reset or handoff.
```

For Claude Code and Codex projects, inspect the existing `CLAUDE.md` and `AGENTS.md` setup. For Cursor, Gemini, Antigravity, and Deep Seek Harness, inspect that installation's supported persistent instruction or rule mechanism. Use the file the active harness actually reads; the existence of another agent's instruction file is insufficient. Verify persistence in a fresh session by checking that the agent can identify this policy and resolve an applicable skill.

## 2. Mandatory policy for the agent

**Every development task gets a skill check. Every applicable skill gets used before its corresponding work.** This applies to planning, implementation, bug fixes, refactoring, UI work, integration changes, tests, reviews, documentation, tooling, and conflict resolution.

1. Classify the task and identify its completion criteria before editing.
2. Resolve the applicable Matt Pocock skills from the installed files or the harness's skill registry. Match the actual skill identity, not just a similar name.
3. Invoke the applicable model-invoked skills through the harness's supported skill mechanism. Load their complete instructions and the references needed for this branch of work.
4. Follow the workflow and its completion criteria. Mentioning a skill name or copying its description is not using it.
5. Reassess when the task changes: an implementation failure may need diagnosis; a new interface may need design; unresolved terminology may need domain modeling.
6. Before completion, review the actual changes, run the relevant checks, and report evidence together with the skills applied and any limitations.

“Always use the skills” means consistent selection and execution of the relevant skills. It does not mean invoking all 37 skills, starting a full interview for a settled typo correction, or creating a spec for every small edit. When no specialized skill fits a phase, say so briefly and use the project's normal procedure. Do not invent a skill or claim one ran.

### Instruction precedence and scope

Follow the harness's governing instructions, access controls, current user direction, and applicable project instructions. This document adds workflow routing; it does not bypass permissions or change the installed skills' invocation settings. Preserve the user's established decisions and authorization instead of repeatedly asking for them.

Keep the scope tied to the request. A skill suggesting a commit, issue update, dependency installation, or other side effect does not independently authorize it. Carry out actions already covered by the user's task and project policy; prepare a concrete result before asking about anything that still requires a decision. Do not modify global agent settings merely because this guide has been loaded.

## 3. Find and load the installed skills

### User-provided skill locations

These are the user's configured lookup locations. Verify them at runtime; this guide does not assert that every installation of each product uses these defaults.

| Coding agent | Skill directory to check |
| --- | --- |
| Claude Code | `~/.claude/skills` |
| Codex | `~/.codex/skills` |
| Cursor | `~/.cursor/skills` |
| Gemini | `~/.gemini/skills` |
| Antigravity | `~/.gemini/antigravity/skills` |
| Deep Seek Harness | `~/.dsh/skills` |

### Discovery procedure

1. Identify the active harness and expand `~` to that machine's actual user home. Keep the project root and skill root distinct.
2. Inspect the harness's advertised skills and its matching directory above. Use file discovery that includes hidden paths and follows installed skill symlinks. Read `SKILL.md` frontmatter and, where present, `agents/openai.yaml`.
3. A typical copied installation is `<skill-root>/<skill-name>/SKILL.md`. A repository checkout may retain `skills/engineering/<skill-name>/SKILL.md`, `skills/productivity/...`, `skills/misc/...`, or `skills/in-progress/...`. Discover the layout rather than assuming either one.
4. If the expected copy is absent, inspect the harness's configured project-local or plugin skill locations. The supplied repository's maintainer script also references `~/.agents/skills`; treat that as an additional candidate only when it exists or the active installation points there. Do not replace the user's paths with it.
5. Record the selected skill's exact name, origin/path, invocation mode, and required references. If duplicate names exist, use the supported qualified name or confirmed path for Matt Pocock's copy. This matters especially for `code-review`, `tdd`, `research`, and `prototype`.
6. Refresh discovery after an installed-skill update or path change. The snapshot catalog below is a routing aid; the actual installed skill governs its current behavior.

**A skill missing from the model-visible menu is not necessarily uninstalled.** User-invoked skills may be hidden from automatic discovery. Check readable installation metadata or the user's command picker before calling them missing. Distinguish “installed but user-invoked,” “installed but inaccessible here,” and “not found.”

### Loading rules

- Prefer the native skill invocation mechanism when the harness exposes it. Use one skill per invocation; load separate dependencies separately.
- Where the harness supports skills as readable instruction files and has no invocation tool, read the complete permitted `SKILL.md` and apply it. Report this as file-based loading. This fallback does not bypass a user-only restriction or a failed access check.
- Resolve reference files relative to the selected skill's directory. Resolve project output paths relative to the project or the explicitly chosen workspace. Never write project docs or lessons into an installed skill directory.
- Load required templates and scripts before using them. Inspect scripts before execution; loading a skill is not a reason to run every bundled script.
- Once an unchanged skill has been loaded in the current context, reuse it. Reload after a context reset or if its instructions are no longer available. Avoid rereading every file for each line edited.
- Do not reinstall, rename, fork, update, or alter managed skill files as part of routine development under this policy.

### User-invoked versus model-invoked

The archive uses two explicit controls:

| Metadata | Meaning |
| --- | --- |
| `disable-model-invocation: true` in `SKILL.md` | The workflow is user-invoked. |
| `policy.allow_implicit_invocation: false` in `agents/openai.yaml` | The paired Codex restriction on implicit invocation. |
| Neither restriction in this archive | The skill is available for model or user invocation when appropriate. |

Honor the active installation and harness enforcement. For a user-invoked workflow, recommend the exact supported command and explain its purpose. Let the user invoke it through the command or skill picker. Do not silently run it, remove its flags, or reconstruct a blocked invocation by another route. Once the user has invoked it, continue that workflow without requesting the same invocation again.

Commands written as `/name` below are human-facing labels from the archive. Use the actual syntax and namespace supported by the current harness; do not assume all six agents accept identical slash commands.

## 4. Start each task with a short routing check

Before the first substantive edit:

1. Read applicable project instructions, the relevant request/spec/issue, and current repository state. Record existing user changes and the task's review baseline.
2. Read `CONTEXT-MAP.md` if present and follow it to the relevant context; otherwise read `CONTEXT.md` if present. Consult relevant ADRs and `docs/agents/domain.md` where available. Missing glossary or ADR files alone do not block work.
3. Determine whether this is a clear implementation task, unresolved design, a defect, review, documentation, tooling, or a human-only setup step.
4. Select and load the matching skills. Announce one short line, for example: “Using Matt Pocock's `diagnosing-bugs` to reproduce the timeout, then `tdd` at the agreed request interface and `code-review` for the final changes.”
5. Identify missing prerequisites before taking the dependent action. Continue other authorized work that does not depend on them.

For tracker-dependent workflows, inspect `docs/agents/issue-tracker.md` and the applicable `docs/agents/triage-labels.md`. If a selected skill requires missing configuration, tell the user to invoke `setup-matt-pocock-skills`. It configures each repository; installed skills alone do not supply that repository's tracker choices. Do not demand setup for a skill whose only dependency is an optional glossary.

The setup skill writes label mappings, not necessarily the actual tracker labels. Verify required labels and dependency operations before publishing. Follow the configured tracker workflow and the user's existing authorization.

## 5. Route the work by scenario

In this table, **automatic** means an applicable model-invoked skill. **User entry** means the human must invoke the named workflow as described in section 3. Arrows describe the work's order, not permission to auto-invoke a user entry.

| Scenario | Skills and order | Concrete result |
| --- | --- | --- |
| A clear feature or behavior change | `codebase-design` if the interface needs design → `tdd` → `code-review`; user entry `implement` can orchestrate the build | Verified behavior at agreed interfaces, with a reviewed diff. |
| A bug, intermittent failure, or performance regression | `diagnosing-bugs` → `tdd` when a correct agreed regression seam exists → `code-review` | Reproduction, supported cause, fix, and rerun of the original scenario. |
| A vague feature in an existing project | User entry `grill-with-docs`, which loads `grilling` and `domain-modeling` | Resolved decisions, agreed language, and appropriate ADRs before implementation. |
| A clear change that fits one session | User entry `implement`, or direct applicable `tdd` and `code-review` | A small completed change without unnecessary ticket decomposition. |
| Agreed work spanning several implementation sessions | User entry `to-spec` → user entry `to-tickets` → user entry `implement` for each ready ticket | Durable spec, independently verifiable slices, and explicit blockers. |
| A large effort with unresolved direction | User entry `wayfinder`; later `to-spec` → `to-tickets` → `implement` | Decisions first; production deliverables follow a buildable plan. |
| An uncertain UI layout | `prototype`, using `UI.md` → user selects direction → normal implementation | Structural alternatives, then production work based on the selected design. |
| Unclear business logic, state transitions, or data shape | `prototype`, using `LOGIC.md`, with `domain-modeling` if terms change | A runnable exploration of one question and a recorded decision. |
| A module is hard to change or test | `codebase-design` → agreed refactor → relevant checks → `code-review` | Less knowledge required by callers and preserved observable behavior. |
| You need to find architectural improvement candidates | User entry `improve-codebase-architecture` | A visual survey and chosen candidate, before redesign or implementation. |
| Wide rename, shared type migration, or schema compatibility change | `codebase-design`; user entry `to-tickets` for expand–migrate–contract if multi-session; `tdd` where behavior warrants it | Staged compatibility changes with explicit integration verification. |
| Unknown API behavior, dependency facts, or external technical decisions | `research` → relevant design or implementation skills | Focused findings grounded in primary sources. |
| Incoming bug reports, requests, or eligible external PRs | User entry `triage` → later user entry `implement` | Verified and categorized work with an actionable brief. |
| A branch, PR, or working tree needs review | `code-review` | Separate Standards and Spec findings over the intended changes. |
| An active merge/rebase is stopped on conflicts | `resolving-merge-conflicts` | Intent-preserving resolutions, checks, and completion of the authorized operation. |
| Agent instructions, prompts, specs, or agent-facing docs change | `writing-for-agents`; `domain-modeling` for glossary or ADR work | Clear triggers, references, ordered steps, and checkable completion criteria. |
| A person must provision access or perform a dashboard procedure | `wizard` | A scoped interactive procedure with verified steps and destinations for captured values. |
| Switching coding agents, directories, or handing work to a teammate | User entry `handoff` | A portable context document with pointers and suggested skills. |
| A stakeholder holds missing business facts | User entry `to-questionnaire` | A focused questionnaire for that one recipient. |
| A copy, formatting, or small static configuration edit | Apply this check; `writing-for-agents` if agent-facing; `code-review` where applicable | The requested edit, inspected with relevant formatting/render/config checks. |

These skills do not supply a complete specialist workflow for every technology. For security, accessibility, database migrations, deployment, or framework details, combine the relevant Matt Pocock discipline with the project's specialized instructions and current primary documentation. Do not label a standards/spec review as a complete security audit.

## 6. Apply the important workflow rules

### Implementation and TDD

- Establish the observable behavior and test seams before tests. A seam is the public interface at which the behavior is exercised. Reuse seams already approved in the current spec or conversation; if a necessary seam is new and unconfirmed, present a concrete proposal for confirmation.
- Read `tdd/tests.md` and `tdd/mocking.md`. Prefer behavior through real interfaces. Mock genuine external boundaries when needed, and keep expected results independent of the implementation.
- Work one vertical slice at a time: a failing test, the minimum implementation that passes it, then the next slice. Confirm the red failure concerns the intended behavior.
- In this snapshot, the detailed TDD instructions place refactoring in the review stage, even though some descriptions say “red-green-refactor.” Follow the detailed installed instructions.
- Run targeted checks during implementation. When using `implement`, run typechecking regularly, individual test files regularly, and the full test suite at the end. Preserve project-required gates and report checks that could not run.
- For a pure refactor, establish behavior-preserving verification at the relevant interface. Avoid tests that merely assert the new internal structure. For static copy or formatting changes, use checks appropriate to the change.

### Diagnosis

- Build a runnable feedback loop that detects the reported symptom before developing a theory. Run it and preserve the useful output with secrets redacted.
- Reproduce and minimize, form ranked falsifiable hypotheses, then instrument one variable at a time. For performance work, measure a baseline before optimization.
- Write a regression test before the fix when a correct seam exists. Rerun the original scenario afterward; a passing minimized example alone is insufficient.
- If no correct seam exists, state that limitation. If no reliable reproduction can be built, report the attempts and request the concrete missing evidence or access required by the skill.
- Remove temporary instrumentation before completion. Explain any skipped phase; do not present an unverified guess as a proven cause.

### Design and domain documentation

- Use `codebase-design` for the module's interface, depth, seams, adapters, and locality. It is a reference, not authorization to redesign the entire application.
- Load `DEEPENING.md` when evaluating dependencies and changing module structure. Load `DESIGN-IT-TWICE.md` only when comparing alternative interfaces is part of the task.
- Reading a glossary is ordinary context gathering. Invoke `domain-modeling` when actively changing terminology, writing the glossary, or recording a decision.
- Keep `CONTEXT.md` focused on domain vocabulary and relationships. Put implementation requirements in specs and meaningful trade-offs in ADRs. Create these documents when there is resolved material to record.
- Offer an ADR when the choice is hard to reverse, surprising without context, and the result of a real trade-off. Respect existing decisions or explicitly identify why they need reconsideration.

### Planning and tickets

- `grilling` works through rounds of currently answerable decisions, with recommendations. Look up facts rather than asking the user to research the codebase. Reuse decisions already settled.
- `to-spec` synthesizes the discussion; it is not another discovery interview. It still explicitly checks the proposed test seams with the user.
- `to-tickets` creates complete vertical slices with blockers. A broad mechanical migration may use expand–migrate–contract instead. Get the breakdown agreed before publication.
- Local implementation tickets are separate files under `.scratch/<feature>/issues/<NN>-<slug>.md`, not one combined tickets file. Follow the configured tracker when it differs.
- Treat `wayfinder` tickets as questions that resolve decisions by default. Charting stops after building the map; work sessions normally resolve one decision ticket, with the skill's research exception. Do not silently convert planning into a production build.
- Do not re-triage tickets already made ready by `to-tickets`, or assume `implement` automatically closes issues. Tracker updates follow the user's requested workflow.

### Review the changes that actually exist

Load Matt Pocock's `code-review`, identify the standards and spec sources, and pin a valid review baseline. If no baseline is already supplied or agreed, propose a concrete one and obtain the required decision before running that review.

**Working-tree adaptation supplied by this guide:** the archive's `git diff <fixed-point>...HEAD` reviews committed changes only. Before claiming a current change was reviewed, check `git status` and include relevant staged, unstaged, and untracked work in the review scope. Resolve the merge-base with the confirmed fixed point; a diff from that base to the working tree captures tracked current changes, while untracked files require explicit inspection. Preserve unrelated user changes. State the exact comparison used. Do not commit merely to make an empty review appear nonempty.

Keep findings in two groups:

- **Standards:** cite a documented repository rule or identify a code smell as a judgment call. The repository's standards override the smell baseline.
- **Spec:** compare against the request, issue, or spec. Report missing, partial, incorrect, and extra behavior. If no spec source exists, state that instead of inventing one from the implementation.

Address actionable findings and verify the affected work. Do not repeat broad review indefinitely to chase a subjective zero-findings result. Report what was checked, what changed, and what remains.

### Delegation and capability limits

Some skills explicitly use subagents: `research`, `code-review`, architecture exploration, interface alternatives, and the beta `implement-spec`. Use them only when the current harness supports and permits that workflow.

**Delegation adaptation supplied by this guide:** make reviewer and researcher briefs bounded leaf tasks: “Perform this assigned work directly. Do not invoke the parent orchestration skill again or spawn additional agents.” Give them the source pointers, scope, required output, and stopping criterion. A worker does not restart the coordinator's workflow.

If parallel agents are unavailable, report the limitation. Where governing instructions permit an equivalent fallback, perform the work sequentially with separate outputs and label it as an adapted workflow. Never claim independent parallel reviews occurred when they did not. If the missing capability is essential to the requested outcome, report that specific blocker.

## 7. Completion and continuity

Before saying the task is complete, establish all of the following:

- The relevant skill instructions and required references were loaded.
- Every acceptance criterion is implemented and verified, or explicitly unresolved.
- Verification covers the final code, including fixes made during review.
- The review covered the intended committed and uncommitted changes.
- Temporary debug material and prototype-only controls are handled appropriately.
- Changed behavior, interfaces, domain terms, or decisions have the necessary documentation updates.
- No installed skill, global setting, or unrelated user file was changed incidentally.

Keep the user-facing report short. A useful format is:

```text
Changed: <the outcome>
Skills applied: <names and concrete purposes>
Verified: <checks and observed results>
Remaining: <specific limitation, or none>
```

At a handoff or context reset, carry the path to this policy, skill locations, current task/spec, agreed test seams and review baseline, verified progress, outstanding questions, and the next applicable skill. Preserve pointers to existing artifacts instead of duplicating them. Use `handoff` when the user invokes a portable handoff workflow; ordinary continuation does not need a new handoff file after every phase.

## 8. Complete skill catalog

**Mode:** `M` = model or user may invoke when relevant; `U` = user-invoked. These modes are verified against both `SKILL.md` and `agents/openai.yaml` in the supplied archive.

### Engineering: 18 promoted skills

| Skill | Mode | Purpose and appropriate scenario | Important boundary or result |
| --- | --- | --- | --- |
| `ask-matt` | U | Help the user choose a skill or flow when the next step is unclear. | A router that recommends what to invoke; it does not execute the whole flow. |
| `code-review` | M | Review a branch, PR, or change against standards and the originating spec. | Two review axes; see section 6 for current working-tree coverage. |
| `codebase-design` | M | Design or improve a known module's interface, test seam, and depth. | Shared design reference; deep functionality behind a small interface. |
| `diagnosing-bugs` | M | Investigate a concrete defect, flake, or performance regression. | Reproduction before hypotheses; original scenario rerun after the fix. |
| `domain-modeling` | M | Resolve overloaded terminology; write/edit `CONTEXT.md` or ADRs. | Active language and decision work, not merely reading existing docs. |
| `grill-with-docs` | U | Clarify a design in a project while capturing language and decisions. | Loads both `grilling` and `domain-modeling` through separate calls. |
| `implement` | U | Build agreed work from a spec or tickets. | TDD where possible at agreed seams, checks, review, then commit within authorized scope. |
| `improve-codebase-architecture` | U | Survey a codebase to find useful deepening candidates. | Visual HTML report first; user selects a candidate before detailed exploration. |
| `prototype` | M | Answer one uncertain UI or logic question with runnable exploratory code. | Choose `UI.md` or `LOGIC.md`; production implementation follows normal quality gates. |
| `research` | M | Resolve a focused technical question using official docs, code, specs, or first-party APIs. | Background research with a cited Markdown artifact. |
| `resolving-merge-conflicts` | M | Resolve an already active merge or rebase conflict. | Trace each side's intent, check the result, finish the authorized operation; respect user changes. |
| `setup-matt-pocock-skills` | U | Configure tracker, triage vocabulary, and domain-document layout per repository. | Installation and project setup are distinct; preserves existing configuration. |
| `tdd` | M | Implement observable behavior with tests first. | Agreed seams, one red-to-green slice at a time, behavior-based assertions. |
| `to-spec` | U | Turn settled discussion and codebase understanding into a durable spec. | Confirms test seams and publishes through the configured tracker. |
| `to-tickets` | U | Split a plan, spec, or discussion into implementable slices. | Explicit blockers; agreement before publication; wide-refactor exception. |
| `triage` | U | Process incoming reports, feature requests, and configured external PR requests. | Verify claims, apply category/state, and produce a durable brief or reasoned outcome. |
| `wayfinder` | U | Plan a large effort whose direction cannot be resolved in one session. | Shared map of decision tickets; planning by default. |
| `wizard` | M | Build a guided procedure for steps only a person can perform. | Uses the bundled Bash template; validate statically and hand it to the human. |

### Productivity: 7 promoted skills

| Skill | Mode | Purpose and appropriate scenario | Important boundary or result |
| --- | --- | --- | --- |
| `grill-me` | U | Stress-test an idea or plan without a project documentation workflow. | Invokes `grilling`; it does not maintain a domain glossary. |
| `grilling` | M | Resolve a decision tree through rounds of questions with recommendations. | Decisions stay with the user; facts are investigated by the agent. |
| `handoff` | U | Transfer work to another harness, directory, teammate, or side session. | Portable Markdown in the OS temporary directory by default; pointers, suggested skills, redaction. |
| `teach` | U | Learn a topic over multiple sessions in a dedicated workspace. | Mission, resources, lessons, references, and learning records; not routine implementation. |
| `to-questionnaire` | U | Gather facts or decisions held by one other person. | Clarifies the recipient and needed answers, then writes a Markdown questionnaire. |
| `wait-what` | U | Re-explain a message the user did not follow. | Adds missing context in plain language using the correct domain vocabulary. |
| `writing-for-agents` | M | Write/edit agent instructions, skills, or other documents agents consume. | Explicit triggers, ordered steps, completion criteria, references, and minimal duplication. |

### Miscellaneous: 4 non-promoted skills

These are present in the ZIP but excluded from its Claude plugin manifest. Confirm they are installed before use. Their model-invoked metadata does not make them default steps for all projects.

| Skill | Mode | Use when | Boundary or dependency |
| --- | --- | --- | --- |
| `git-guardrails-claude-code` | M | The user wants Claude Code hooks to block specified Git operations. | Claude-specific settings and bundled hook; select project/global scope. Not a guarantee against every possible command form. |
| `migrate-to-shoehorn` | M | Migrating TypeScript test fixtures away from `as` assertions to `@total-typescript/shoehorn`. | Test code only; select appropriate helpers and verify typechecking. |
| `scaffold-exercises` | M | Creating a course's exercise sections, problems, solutions, or explainers. | Assumes the AI Hero exercise conventions and `pnpm ai-hero-cli internal lint`; verify availability. |
| `setup-pre-commit` | M | Adding Husky, lint-staged, formatting, typechecking, and test hooks. | Adapt to the existing package manager and scripts; preserve existing settings. |

### In progress: 8 beta skills

All eight are user-invoked and excluded from the supplied Claude plugin manifest. Use only when installed and explicitly selected for their intended task. Beta availability and behavior may differ from this snapshot.

| Skill | Mode | Use when | Boundary or status |
| --- | --- | --- | --- |
| `claude-handoff` | U | Launching a fresh background Claude agent with a handoff prompt. | Assumes the documented Claude CLI background-agent capability; verify the installed CLI supports it. |
| `implement-spec` | U | Implementing a whole spec and its ticket graph as one branch and PR. | Uses implementer worktrees, merger agents, frontier concurrency, review, and cleanup. |
| `loop-me` | U | Discovering and specifying recurring workflows or automations. | Produces implementable `workflows/*.md`; does not execute the workflows it designs. |
| `retro` | U | Reviewing a coding session for possible improvements to the agent's environment. | The bucket README labels it a stub/design notes despite a populated `SKILL.md`; treat as provisional, not a dependable automatic gate. |
| `setup-ts-deep-modules` | U | Enforcing TypeScript package entry points and private internals with dependency-cruiser. | Ships a config template and requires pass → deliberate violation/fail → pass validation. |
| `writing-beats` | U | Turning existing raw material into an article one chosen beat at a time. | Interactive writing workflow; no writing ahead of the user's selected beat. |
| `writing-fragments` | U | Mining ideas and appending raw fragments for a future article. | Exploration without imposing an outline; reread and preserve the user's file edits. |
| `writing-shape` | U | Shaping a raw-material file into a separate article paragraph by paragraph. | Source stays read-only; agree structure and format choices with the user. |

The deprecated bucket has no skill definitions in this archive. Historical names in the changelog are not installed commands unless runtime discovery confirms them.

## 9. Supporting files: when to read them

The full instructions and references belong to the installed skills. Use this table to avoid loading a skill while skipping the file that contains the needed branch.

| Owning skill | Supporting files | Read when |
| --- | --- | --- |
| `ask-matt` | `PHASE-BOUNDARIES.md` | Choosing continuation, clear, compact, delegation, or a portable handoff. |
| `codebase-design` | `DEEPENING.md`; `DESIGN-IT-TWICE.md` | Assessing dependency strategies or comparing alternative module interfaces. |
| `diagnosing-bugs` | `scripts/hitl-loop.template.sh` | A human-operated reproduction loop is genuinely necessary. |
| `domain-modeling` | `CONTEXT-FORMAT.md`; `ADR-FORMAT.md` | Writing the glossary/context map or a decision record. |
| `improve-codebase-architecture` | `HTML-REPORT.md` | Rendering the architecture survey. Its CDN dependencies need network access to render as authored. |
| `prototype` | `LOGIC.md`; `UI.md` | Select the relevant branch before building. UI variants normally number three and differ structurally. |
| `setup-matt-pocock-skills` | `domain.md`; `issue-tracker-github.md`; `issue-tracker-gitlab.md`; `issue-tracker-local.md`; `triage-labels.md` | Configuring the selected tracker, domain layout, and role mapping. |
| `tdd` | `tests.md`; `mocking.md` | Before and during behavior-driven test implementation. |
| `triage` | `AGENT-BRIEF.md`; `OUT-OF-SCOPE.md` | Writing ready-to-implement briefs or recording rejected enhancements. |
| `wizard` | `template.sh` | Creating the manual procedure; keep its library helpers intact and author the stages. |
| `setup-ts-deep-modules` | `dependency-cruiser.config.cjs` | Installing/merging import-boundary rules and proving they detect a violation. |
| `git-guardrails-claude-code` | `scripts/block-dangerous-git.sh` | Inspecting and configuring the requested Git hook. |
| `teach` | `MISSION-FORMAT.md`; `RESOURCES-FORMAT.md`; `LEARNING-RECORD-FORMAT.md`; `GLOSSARY-FORMAT.md` | Creating the respective teaching artifacts; the glossary template exists although the main skill does not directly link it. |
| `writing-for-agents` | `SKILL-MECHANICS.md` | Writing an actual skill, its invocation metadata, or a skill router. |
| Every skill | `agents/openai.yaml` | Verifying UI identity and implicit-invocation policy. |

Other repository files serve different purposes:

- `docs/engineering/*` and `docs/productivity/*`: human-facing explanations, examples, limitations, and workflow context. Use them as supplements to actual skill instructions.
- `.claude-plugin/plugin.json`: the exact promoted bundle in this snapshot, 25 skills. `.claude-plugin/marketplace.json` describes its distribution.
- `README.md` and bucket READMEs: indexes and bucket status. The in-progress README's provisional status is significant.
- `.agents/invocation.md`: the source policy for model/user invocation and explicit cross-skill calls.
- `.agents/adr/*`, `.agents/install-block.md`, and `.agents/writing-docs.md`: maintenance decisions and conventions for contributing to the skills repository. They are not application-development requirements for every consuming project.
- `.changeset/*` and `CHANGELOG.md`: release history and pending changes, useful for understanding renames and documentation drift.
- `.out-of-scope/*`: rejected requests for the skills repository itself. Do not import those product decisions into the user's application.
- `scripts/link-skills.sh`: a maintainer-only linking script; it can replace existing destination folders. It is not needed to use already installed skills and is not part of this guide's activation.
- `scripts/list-skills.sh`, `scripts/sync-plugin-version.mjs`, package files, and release workflow: inventory/release tooling for the source repository, not required development steps in the user's projects.

## 10. Practical examples

### “Add account roles and permissions.”

Read the existing authorization design and relevant ADRs. If role definitions are unresolved, use `domain-modeling` and the appropriate user-invoked design workflow. Use `codebase-design` for the authorization interface and `tdd` for agreed observable access decisions, including denied access. Apply the project's security-specific checks. Review Standards and Spec before completion.

### “The scraper crashes during a bulk run.”

Use `diagnosing-bugs` to reproduce the actual bulk-run failure, including the relevant concurrency or input conditions. Measure resource or timing behavior where implicated. Establish a regression seam that exercises the real pattern, fix the cause, rerun the original scenario, and use `code-review`. A single-item happy-path test is insufficient if the reported problem requires concurrent jobs.

### “Revamp this dashboard.”

If the desired layout is unresolved, use `prototype/UI.md` to compare distinct structures within the project's existing styling and component system. Preserve real read behavior and stub prototype mutations. Once the user chooses a direction, implement it with production checks; the prototype's minimal-quality constraints do not carry into production.

### “Build this six-week sprint.”

If the destination and requirements are settled, use the spec/ticket/implementation route. If major decisions are still unknown across multiple sessions, recommend `wayfinder` first. Model tickets as dependencies. Use the beta `implement-spec` only if the user explicitly selects it and the required worktree, subagent, and PR capabilities are available.

### “Improve our AGENTS.md.”

Use `writing-for-agents`. Keep essential behavior and navigation pointers easy to find. Put detailed reference material behind explicit triggers. Preserve existing rules and use checkable completion criteria. A clearer instruction document should not invent features or imply that a plain Markdown file can override the harness.

## 11. Scan coverage and interpretation

The supplied ZIP contains **164 files**, all text, totaling **666,067 uncompressed bytes**. Every file was enumerated and text-scanned. All **37 `SKILL.md` definitions**, their **37 `agents/openai.yaml` files**, and supporting references/templates were examined. Human-facing docs, manifests, scripts, configuration, and release notes were cross-checked for routing, prerequisites, and known mismatches. Bundled scripts were inspected, not executed as installation steps.

| Bucket | Skill definitions | Model-invoked | User-invoked | Listed in plugin manifest |
| --- | ---: | ---: | ---: | ---: |
| Engineering | 18 | 9 | 9 | 18 |
| Productivity | 7 | 2 | 5 | 7 |
| Miscellaneous | 4 | 4 | 0 | 0 |
| In progress | 8 | 0 | 8 | 0 |
| Deprecated | 0 | 0 | 0 | 0 |
| **Total** | **37** | **15** | **22** | **25** |

The guide deliberately accounts for these snapshot inconsistencies:

1. Some descriptions call TDD “red-green-refactor”; the detailed TDD file puts refactoring in review.
2. The default code-review command excludes uncommitted changes, while `implement` calls review before its final commit. Section 6 supplies an explicit working-tree adaptation.
3. Human docs contain older skill counts and older claims about TypeScript boundary enforcement. The actual plugin list, skill definitions, and bundled dependency-cruiser configuration govern the catalog here.
4. The beta README labels `retro` a stub although its instruction file contains proposed steps. It remains provisional here.
5. The setup skill prefers an existing `CLAUDE.md`, which may not be what another active harness reads. Activation must verify the real instruction-loading path.
6. Source docs flag recursive research/review delegation. Section 6 supplies explicit leaf-task briefs instead of claiming the archive already prevents it.

This is a usage and routing guide derived from the supplied source. It does not certify runtime behavior on all six agents, modify installed skills, or guarantee that an agent will obey an instruction merely because the file exists. Persistent loading, actual skill invocation, and observable verification are the checks that make the workflow reviewable.

