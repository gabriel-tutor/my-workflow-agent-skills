---
name: using-matt-pocock-skills
description: Use when starting any conversation - establishes how development work is routed through Matt Pocock's engineering skills
---

<SUBAGENT-STOP>
If you were dispatched as a subagent for a specific task, ignore this skill.
</SUBAGENT-STOP>

Matt Pocock's skills lead every development task here. Before your first action on one, classify it below and invoke its skill with the Skill tool; 1% odds are enough. Between two rows take the heavier; complexity found mid-task moves up, not down. * marks this plugin's (`matt-pocock-workflow:<name>`); the rest are Matt Pocock's, bare name.

| Request | First move |
| --- | --- |
| Trivial: copy, typo, comment, unobservable rename | `trivial`* |
| Sensitive, any size: auth, permissions, secrets, billing, migrations, infra, CI or deploy config, public API, anything destructive | `grill`* (security and failure axes), `tdd`, `code-review` required |
| Down or degraded for users now | `incident`* |
| Broken, failing, throwing, slow | `diagnosing-bugs`, even when the fix looks obvious |
| Bounded change to existing code | `grill`*, `tdd` |
| New behavior in one session | `grill`* + `domain-modeling`, then `implement`* |
| Several sessions, or a new app | grill, `to-spec`*, `to-tickets`*, `implement`* per ticket; a new app starts with the walking skeleton |
| Ship, deploy, release, publish | `release`* |

**Red flags** (invoke the skill now): "it's a quick fix", "the requirements are clear", "let me read the code first".

**Enforced.** A hook refuses project changes until a skill is invoked for the request, and a turn that changed the project ends only after `verification-before-completion`*, before any claim of done, fixed or passing. Finish a branch with `finishing-a-development-branch`*; on the base branch, commit and stop.

**Rules.**
1. Ask through AskUserQuestion, recommended answer first; `grill` asks one question per turn.
2. Test seams are settled in the grill, so `tdd` and `to-spec` do not ask again.
3. `code-review` runs on features and builds, is offered on bounded changes and bugs.
4. Each flow step asks before it starts; a yes covering later steps is not asked again; deploy and publish always ask.
5. Keep grill → spec → tickets in one context. Phase boundaries, durable state, on-ramps, Superpowers overlaps: `${CLAUDE_PLUGIN_ROOT}/skills/using-matt-pocock-skills/references/routing.md`
