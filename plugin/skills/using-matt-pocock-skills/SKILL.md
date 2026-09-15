---
name: using-matt-pocock-skills
description: Use when starting any conversation - establishes how development work is routed through Matt Pocock's engineering skills
---

<SUBAGENT-STOP>
Dispatched as a subagent for a specific task? Ignore this skill.
</SUBAGENT-STOP>

Matt Pocock's skills lead every development task here. Before your first action on one (a read, a command, an edit), route it below and invoke its skill with the Skill tool; a 1% chance is enough. Between two rows take the lower; mid-task complexity moves down, never up. * marks this plugin's skills (`matt-pocock-workflow:<name>`); bare names are Matt Pocock's.

| Request | First move |
| --- | --- |
| Trivial: copy, typo, comment, unobservable rename | `trivial`* |
| Broken, failing, throwing, slow | `diagnosing-bugs`, even when the fix looks obvious |
| Bounded change to existing code | `grill`*, `tdd` |
| New behavior in one session | `grill`* + `domain-modeling`, then `implement`* |
| Several sessions, or a new app | `grill`*, `to-spec`*, `to-tickets`*, `implement`* per ticket; a new app's ticket 01 is the walking skeleton |
| Sensitive, any size: auth, permissions, secrets, billing, migrations, infra, CI or deploy config, public API, anything destructive | its size row's move, `grill`* on the security and failure axes first, `code-review` required |
| Down or degraded for users now | `incident`* |
| Ship, deploy, release, publish | `release`* |

**Red flags**, meaning invoke now: "it's a quick fix", "the requirements are clear", "let me read the code first".

**Enforced.** A hook refuses project changes until one of these skills is invoked for the request, and refuses to end a turn that changed the project without `verification-before-completion`*; run it before any claim of done, fixed or passing. Finish a branch with `finishing-a-development-branch`*; on the base branch, commit and stop.

**Rules.**
1. Ask through AskUserQuestion, recommended answer first.
2. Seams are settled in the grill; `tdd` and `to-spec` do not ask again.
3. `code-review` runs on features and builds, is offered on bounded changes and bugs.
4. Flow: spec → `to-tickets`*, tickets → `implement`*; each step asks before it starts; a yes covering later steps is not asked again; deploy and publish always ask.
5. Keep grill → spec → tickets in one context. Phase boundaries, durable state, on-ramps, Superpowers overlaps: `${CLAUDE_PLUGIN_ROOT}/skills/using-matt-pocock-skills/references/routing.md`
