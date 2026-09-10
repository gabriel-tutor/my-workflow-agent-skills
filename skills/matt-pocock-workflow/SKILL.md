---
name: matt-pocock-workflow
description: Use before the first edit of any development task in a project where Matt Pocock's skills are installed and Superpowers is not the active workflow — planning, features, bug fixes, refactors, UI, integrations, tests, reviews, docs, tooling, merge conflicts. Use again when scope changes, before claiming completion, and after a context reset or handoff. Also use whenever the user mentions Matt Pocock's skills or asks which skill applies. If Superpowers is installed, use matt-pocock-superpowers-workflow instead.
---

# Matt Pocock Skills: Routing Policy

Standing development instructions for a coding agent in a project where Matt Pocock's skills are installed. This skill explains how to discover them, select the right ones, and apply their actual instructions throughout development. It adds routing; it does not change the installed skills or bypass permissions.

**Source snapshot:** `github.com/mattpocock/skills` @ `3cca18b` (package/plugin version 1.2.3). The installed skill governs its current behaviour; this policy is a routing aid.

## 1. Mandatory policy

**Every development task gets a skill check. Every applicable skill gets used before its corresponding work.** Planning, implementation, bug fixes, refactoring, UI, integrations, tests, reviews, documentation, tooling, conflict resolution — all of it.

1. Classify the task and identify its completion criteria before editing.
2. Resolve the applicable skills from the installed files or the harness's skill registry. Match the actual skill identity, not a similar name.
3. Invoke the applicable model-invoked skills through the harness's skill mechanism. Load their complete instructions and the references needed for this branch of work.
4. Follow the workflow and its completion criteria. Mentioning a skill name or copying its description is not using it.
5. Reassess when the task changes: an implementation failure may need diagnosis; a new interface may need design; unresolved terminology may need domain modeling.
6. Before completion, review the actual changes, run the relevant checks, and report evidence together with the skills applied and any limitations.

"Always use the skills" means consistent selection and execution of the *relevant* skills. It does not mean invoking all 37, starting a full interview for a settled typo, or writing a spec for every small edit. When no specialised skill fits a phase, say so briefly and use the project's normal procedure. Never invent a skill or claim one ran.

**Precedence and scope.** Harness instructions, access controls, current user direction, and project instructions come first. Preserve the user's established decisions instead of re-asking. A skill suggesting a commit, issue update, or dependency install does not authorise it on its own: do what the user's task and project policy already cover, and prepare a concrete result before asking about anything that still needs a decision. Do not modify global agent settings or installed skills because this policy loaded.

## 2. Find and load the installed skills

Check the harness's advertised skills and its skill directory — Claude Code `~/.claude/skills`, Codex `~/.codex/skills`, Cursor `~/.cursor/skills`, Gemini `~/.gemini/skills`, Antigravity `~/.gemini/antigravity/skills`, Deep Seek Harness `~/.dsh/skills` — following symlinks. A copied install is `<root>/<skill>/SKILL.md`; a repository checkout keeps `skills/engineering/…`, `skills/productivity/…`, `skills/misc/…`, `skills/in-progress/…`. `~/.agents/skills` is a candidate only when it exists. Record each selected skill's exact name, path, invocation mode, and required references; where names collide (`code-review`, `tdd`, `research`, `prototype`), use the confirmed Matt Pocock copy.

| Metadata | Meaning |
| --- | --- |
| `disable-model-invocation: true` in `SKILL.md` | User-invoked. Recommend the exact command and its purpose; let the user run it. Never run it silently, strip its flags, or reconstruct it by another route. Once the user has invoked it, continue without asking again. |
| `policy.allow_implicit_invocation: false` in `agents/openai.yaml` | The paired Codex restriction. |
| Neither | Model or user may invoke when relevant. |

A skill missing from the model-visible menu is not necessarily uninstalled — user-invoked skills may be hidden. Distinguish "installed but user-invoked", "installed but inaccessible here", and "not found". Commands written as `/name` are human-facing labels; use the syntax the current harness supports.

Loading rules: one skill per invocation; load dependencies separately. Where the harness has no invocation tool, read the complete permitted `SKILL.md` and report file-based loading (this never bypasses a user-only restriction). Resolve reference files relative to the skill directory and project outputs relative to the project; never write project docs or lessons into an installed skill directory. Inspect bundled scripts before running them; loading a skill is not a reason to run every script. Reuse an unchanged loaded skill; reload after a context reset. Do not reinstall, rename, fork, or alter managed skill files.

## 3. Start each task with a routing check

Before the first substantive edit:

1. Read applicable project instructions, the request/spec/issue, and repository state. Record existing user changes and the task's review baseline.
2. Read `CONTEXT-MAP.md` if present and follow it to the relevant context; otherwise `CONTEXT.md` if present. Consult relevant ADRs and `docs/agents/domain.md`. Missing glossary or ADR files alone do not block work.
3. Classify: clear implementation, unresolved design, defect, review, documentation, tooling, or human-only setup.
4. Select and load the matching skills. Announce one line — "Using Matt Pocock's `diagnosing-bugs` to reproduce the timeout, then `tdd` at the agreed request interface and `code-review` for the final changes."
5. Identify missing prerequisites before the dependent action; continue other authorised work that does not depend on them.

Tracker-dependent workflows (`to-spec`, `to-tickets`, `triage`, `implement`) read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`. If a selected skill needs configuration that is missing, tell the user to invoke `setup-matt-pocock-skills`; do not demand setup for a skill whose only dependency is an optional glossary. Setup writes label mappings, not the tracker's labels — verify required labels before publishing.

## 4. Route the work by scenario

**Automatic** = an applicable model-invoked skill. **User entry** = the human must invoke the named workflow. Arrows describe order, not permission to auto-invoke a user entry.

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

These skills do not supply a complete specialist workflow for every technology. For security, accessibility, database migrations, deployment, or framework details, combine the relevant discipline with the project's specialised instructions and current primary documentation. Do not label a standards/spec review a security audit.

## 5. Workflow rules that change outcomes

Full text: `references/workflow-rules.md`. The load-bearing rules:

**TDD.** Establish the observable behaviour and the test seam (the public interface at which it is exercised) before writing tests; reuse seams already agreed, propose new ones for confirmation. Read `tdd/tests.md` and `tdd/mocking.md`: prefer real interfaces, mock genuine external boundaries, keep expectations independent of the implementation. One vertical slice at a time — failing test, minimum implementation, next slice — and confirm the red failure concerns the intended behaviour. In this snapshot refactoring belongs to the review stage even where descriptions say "red-green-refactor". Run targeted checks during implementation and the full suite at the end; under `implement`, typecheck regularly. A pure refactor gets behaviour-preserving verification at the interface, not tests that assert the new internal structure.

**Diagnosis.** Build a runnable feedback loop that detects the reported symptom before forming a theory; keep useful output with secrets redacted. Reproduce and minimise, rank falsifiable hypotheses, instrument one variable at a time; measure a baseline before optimising. Write the regression test before the fix when a correct seam exists and rerun the original scenario afterwards — a passing minimised example alone is insufficient. State it when no seam or no reliable reproduction exists and ask for the missing evidence. Remove temporary instrumentation. Never present an unverified guess as a proven cause.

**Design and domain.** `codebase-design` covers a module's interface, depth, seams, adapters, and locality — it is a reference, not authorisation to redesign the application. Load `DEEPENING.md` for dependency strategy and module structure; `DESIGN-IT-TWICE.md` only when comparing alternative interfaces is part of the task. Reading a glossary is context gathering; invoke `domain-modeling` when changing terminology, writing the glossary, or recording a decision. Keep `CONTEXT.md` to vocabulary and relationships, requirements in specs, trade-offs in ADRs. Offer an ADR when a choice is hard to reverse, surprising without context, and a real trade-off.

**Planning and tickets.** `grilling` runs rounds of currently answerable decisions with recommendations; look facts up rather than asking the user to research the codebase. `to-spec` synthesises the discussion — not another interview — but still checks the proposed test seams. `to-tickets` makes complete vertical slices with blockers (expand–migrate–contract for broad mechanical migrations), agreed before publication; local tickets are separate files under `.scratch/<feature>/issues/<NN>-<slug>.md`. `wayfinder` tickets are decisions by default; do not silently convert planning into a production build. Do not re-triage tickets already made ready, or assume `implement` closes issues.

**Review.** Load `code-review`, identify the standards and spec sources, and pin a valid baseline — propose a concrete one if none is agreed. **Working-tree adaptation:** the archive's `git diff <fixed-point>...HEAD` covers committed changes only; check `git status` and include relevant staged, unstaged, and untracked work, resolve the merge-base with the confirmed fixed point, and state the exact comparison used. Never commit merely to make an empty review non-empty. Keep findings in two groups — **Standards** (cite a documented repository rule, or name a code smell as a judgment call; repository standards override the smell baseline) and **Spec** (missing, partial, incorrect, extra behaviour against the request/issue/spec; say so if no spec source exists rather than inventing one). Address actionable findings, verify the affected work, and stop; do not chase a subjective zero-findings result.

**Delegation.** `research`, `code-review`, architecture exploration, interface alternatives, and the beta `implement-spec` use subagents only where the harness supports and permits them. Brief workers as bounded leaf tasks with source pointers, scope, required output, and a stopping criterion: "Perform this assigned work directly. Do not invoke the parent orchestration skill again or spawn additional agents." If parallel agents are unavailable, do the work sequentially with separate outputs, label it an adapted workflow, and never claim independent parallel reviews happened. If the missing capability is essential, report that specific blocker.

## 6. Completion and continuity

Before saying the task is complete, all of these hold:

- The relevant skill instructions and required references were loaded.
- Every acceptance criterion is implemented and verified, or explicitly unresolved.
- Verification covers the final code, including fixes made during review.
- The review covered the intended committed and uncommitted changes.
- Temporary debug material and prototype-only controls are handled.
- Changed behaviour, interfaces, domain terms, or decisions have their documentation updates.
- No installed skill, global setting, or unrelated user file changed incidentally.

Keep the user-facing report short:

```text
Changed: <the outcome>
Skills applied: <names and concrete purposes>
Verified: <checks and observed results>
Remaining: <specific limitation, or none>
```

At a handoff or context reset, carry the path to this policy, skill locations, current task/spec, agreed test seams and review baseline, verified progress, outstanding questions, and the next applicable skill. Point to existing artefacts instead of duplicating them. Use `handoff` only when the user invokes it; ordinary continuation does not need a new handoff file after every phase.

## 7. Read next

| Situation | Open |
| --- | --- |
| Which of the 37 skills exists, its invocation mode, what it is for, and which supporting file to load (`tests.md`, `DEEPENING.md`, `UI.md`, `template.sh`, …) | `references/skill-catalog.md` |
| The full TDD, diagnosis, design, planning, review, or delegation rules | `references/workflow-rules.md` |
| Worked examples — roles and permissions, a crashing scraper, a dashboard revamp, a six-week sprint, an AGENTS.md rewrite | `references/examples.md` |
