---
name: using-matt-pocock-skills
description: Use when starting any conversation - establishes how development work is routed through Matt Pocock's engineering skills
---

<SUBAGENT-STOP>
If you were dispatched as a subagent for a specific task, ignore this skill.
</SUBAGENT-STOP>

Matt Pocock's skills lead every development task here. Before your first action on a development request (reading code, running commands, editing), classify it and invoke its skill with the Skill tool. A 1% chance that a skill applies is enough. Between two rows, take the heavier; complexity found mid-task moves you up a row, never down. Skills marked * live in this plugin: invoke them as `matt-pocock-workflow:<name>`.

| Request | First move |
| --- | --- |
| Trivial: copy, typo, config, rename | edit, then verify |
| Broken, failing, throwing, slow | `diagnosing-bugs`, even when the fix looks obvious |
| Bounded change to existing code | `grill`* (short), then `tdd` |
| New behavior that fits one session | `grill`* + `domain-modeling`, then `implement`* |
| A build spanning several sessions | the grill, then `to-spec`*, `to-tickets`*, and `implement`* per ticket |
| User-only commands to suggest by name | `/wayfinder` (foggy effort), `/triage` (others' issues), `/improve-codebase-architecture` (upkeep), `/handoff`, `/ask-matt` |

**Red flags** that mean "invoke the skill now": "the cause is obvious", "it's a quick fix", "the requirements are already clear", "let me read the code first".

**Stage owners.** verify = `verification-before-completion`*, before any claim of done, fixed or passing. finish = `finishing-a-development-branch`* on a branch; on the base branch, commit and stop. Worktrees: `using-git-worktrees`*. Review feedback: `receiving-code-review`*. If Superpowers is also enabled, these win: `grill` over `brainstorming`, `tdd` over `test-driven-development`, `diagnosing-bugs` over `systematic-debugging`, `to-spec`/`to-tickets` over `writing-plans`, `code-review` over `requesting-code-review`.

**Rules.**
1. Ask the user through AskUserQuestion, recommended answer first. `grill` asks one question per turn.
2. Test seams are settled in the grill, so `tdd` and `to-spec` do not ask again.
3. Ceremony scales with the change: trivial work gets no process skill; `code-review` runs on features and builds, is offered on bounded changes and bugs.
4. Flow order: grill → `to-spec` (several sessions) or `implement`; spec → `to-tickets`; tickets → `implement`, one at a time. Each step asks before it starts.
5. Keep grill → spec → tickets in one context, and `/clear` between tickets. Phase boundaries and on-ramps: `${CLAUDE_PLUGIN_ROOT}/skills/using-matt-pocock-skills/references/routing.md`
