---
name: using-matt-pocock-skills
description: Use when starting any conversation - establishes how development work is routed through Matt Pocock's engineering skills
---

<SUBAGENT-STOP>
If you were dispatched as a subagent for a specific task, ignore this skill.
</SUBAGENT-STOP>

Matt Pocock's skills lead every development task here. Before your first action on a development request (reading code, running commands, editing), classify it and invoke its skill with the Skill tool. A 1% chance that a skill applies is enough. Between two rows, take the heavier.

| Request | First move |
| --- | --- |
| Trivial: copy, typo, config, rename | edit, then verify |
| Broken, failing, throwing, slow | `diagnosing-bugs`, even when the fix looks obvious |
| Bounded change to existing code | `matt-pocock-workflow:grill` (short), then `tdd` |
| New behavior that fits one session | `matt-pocock-workflow:grill` + `domain-modeling`, then `matt-pocock-workflow:implement` |

**Red flags** that mean "invoke the skill now": "the cause is obvious", "it's a quick fix", "the requirements are already clear", "let me read the code first". The skill's first phase is how you read the code.

**Stage owners.** verify = `matt-pocock-workflow:verification-before-completion`, before any claim of done, fixed or passing. finish = `matt-pocock-workflow:finishing-a-development-branch` when the work is on a branch. Worktrees: `matt-pocock-workflow:using-git-worktrees`. Review feedback: `matt-pocock-workflow:receiving-code-review`. If Superpowers is also enabled, Matt Pocock's skills win every overlap (grill, tdd, diagnosing-bugs, to-spec, to-tickets, code-review).

**Rules.**
1. Ask the user through AskUserQuestion, recommended answer first. `grill` asks one question per turn.
2. Test seams are settled in the grill, so `tdd` does not ask again.
3. Ceremony scales with the change: trivial work gets no process skill.
4. Keep grill → spec → tickets in one context, and `/clear` between tickets. Phase boundaries and on-ramps: `${CLAUDE_PLUGIN_ROOT}/skills/using-matt-pocock-skills/references/routing.md`.
