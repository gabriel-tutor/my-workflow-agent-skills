# Matt Pocock skill catalog, supporting files, and scan coverage

Verbatim from `sources/MATT-POCOCK-AGENT-INSTRUCTIONS.md` §8, §9, §11 (Matt Pocock skills 1.2.3 @ 3cca18b, inspected 2026-09-10). Open it when `SKILL.md` §7 "Read next" points here.

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

