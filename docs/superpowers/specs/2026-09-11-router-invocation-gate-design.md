# Design: router invocation gate (Claude Code hooks)

**Date:** 2026-09-11
**Status:** approved in conversation; awaiting written-spec review
**Repo:** `~/my-agent-workflow-skills`

## 1. Problem

Skill invocation is probabilistic. `matt-pocock-superpowers-workflow` declares "use before the first edit of any development task", but whether it actually fires is the model's judgement call, and skills are known to under-trigger. Iteration 1 of the benchmark never tested this: all twelve routed runs were *told* to read the skill file. So the cascade is verified and the trigger is not.

Two collections behave differently here, and the asymmetry is real:

- **Superpowers** ships `hooks/hooks.json` with a `SessionStart` handler that injects `using-superpowers` into every session.
- **Matt Pocock's skills** ship no hooks at all (verified: no hook file anywhere in the archive). Additionally 22 of its 37 skills carry `disable-model-invocation: true` and can never auto-fire by design.

The user's goal: the combined router runs every time, deterministically, not when the model happens to notice it.

## 2. What a hook can and cannot do

A hook **cannot** override `disable-model-invocation: true`. That restriction is enforced by the harness; a hook can inject context and deny tool calls, nothing more. Matt Pocock's user-invoked skills (`implement`, `to-spec`, `wayfinder`, …) still require the human to type the command. The gate's job is narrower and achievable: guarantee the *router* is consulted before any file is written.

## 3. Verified mechanics

Established by a log-only probe hook installed globally, exercised with a real `claude -p` session and a real subagent, then removed (`settings.json` confirmed byte-identical to its backup afterwards).

| Fact | Evidence |
| --- | --- |
| The `Skill` tool fires both `PreToolUse` and `PostToolUse` | captured `{"event":"PostToolUse","tool":"Skill","tool_input":{"skill":"tdd"}}` |
| Subagents are identifiable | `agent_id: "ahookprobe-1aed0c0fb5d748f5"`, `agent_type: "hookprobe"`; both `null`/absent in the main session |
| Hooks hot-reload into running sessions | a session started before install began emitting events without a restart |
| Available input fields | `cwd`, `session_id`, `agent_id`, `agent_type`, `scratchpad_dir`, `permission_mode`, `transcript_path`, `tool_input`, `tool_use_id`, `prompt_id`, `effort`, `hook_event_name`, `tool_name` |
| `PreToolUse` fires even for calls later denied | 5 `PreToolUse` Bash vs 3 `PostToolUse` Bash in the probe |
| Global hooks reach every concurrent session | the probe fired in an unrelated live session in another project |

Rejected on this evidence: reading `transcript_path` to detect the invocation. The docs state the transcript "is written asynchronously and may lag the in-memory conversation", so a router invoked earlier in the same turn may not appear yet — a false block. A marker written by `PostToolUse` is synchronous with the event.

## 4. Decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Scope | Global `~/.claude/settings.json` | User wants it in every project, not per-repo opt-in. |
| Coverage | `Edit`/`Write`/`MultiEdit` **and** write-shaped `Bash` | Both cosmetic-edit runs in iteration 1 edited via `sed -i`; a tool-only gate has a hole those runs would have walked through. |
| Subagents | Gated, keyed separately from the parent | User's explicit choice. A parent's invocation does not unlock its children. |
| Exempt: outside a git work tree | Skip | Notes, dotfiles, scratch files are not development work a routing policy should govern. |
| Exempt: scratchpad, `/tmp`, `/var/folders` | Skip | Agents legitimately write probes and backups there constantly. |
| Per-repo opt-out | `~/.claude/mpsw-gate-ignore`, one path prefix per line | Live client work (`clarewoodcapital/underwriting-engine`) must not be gated mid-flight. Editable without a restart. |
| Which router is required | Whichever `scripts/activate.sh` has installed, resolved by exact name plus symlink-target ownership | Keeps the gate consistent with the repo's existing model, and makes `activate.sh none` a global off switch. |
| Anti-wedge | After 3 denials for one agent, allow with a warning | A global gate that can deadlock a session is unacceptable for a convenience feature. |
| Infrastructure failure | Fail **open** | Missing interpreter, unreadable marker dir, unexpected input: never block. Policy failure still denies. |

## 5. Architecture

```
PostToolUse  matcher "Skill"                    → mark-skill.py   (writes marker if skill == active router)
PreToolUse   matcher "Edit|Write|MultiEdit"  ─┐
PreToolUse   matcher "Bash"                  ─┴→ gate.py         (denies when no marker)
```

### Decision order in `gate.py` (first match wins)

1. `MPSW_GATE=off` in the environment → allow.
2. No router active → allow (nothing to enforce). *Active* means `~/.claude/skills/matt-pocock-superpowers-workflow` or `~/.claude/skills/matt-pocock-workflow` is a symlink whose target resolves inside this repo's `skills/` — the same ownership test `activate.sh` uses. The name must match exactly: `setup-matt-pocock-skills` is a different, unrelated skill that is also installed, and a substring match would mistake it for a router.
3. `cwd` matches a prefix in `~/.claude/mpsw-gate-ignore` → allow.
4. Denial count for this agent ≥ 3 → allow, with `systemMessage` noting the gate gave up.
5. `cwd` not inside a git work tree → allow.
6. Every target path is under the scratchpad, `/tmp`, or `/var/folders` → allow.
7. Tool is `Bash` and the command is not write-shaped → allow.
8. Marker exists for this `session_id`+agent → allow.
9. Otherwise → **deny**, increment the denial count.

### Marker identity

`~/.claude/mpsw-gate/<session_id>.<agent_key>` where `agent_key` is `agent_id` when present and `main` otherwise. Denial counts live beside it as `<same>.denials`. Both are created by the hooks; a sweep deletes entries older than 7 days on each write, so no `SessionEnd` handler is needed.

### Write-shaped Bash detection

Reuses `bash_writes()` from `scripts/jsonl_to_transcript.py` — already hardened during the benchmark against compound commands (`sed -i '' s/a/b/ f && npm test` correctly yields `f`, not `test`). Relative paths resolve against the hook's `cwd`.

**Known gap:** `git checkout`, `git stash`, `git reset` modify files without matching a write shape. Out of scope for v1 and recorded here rather than silently omitted.

### Denial payload

```json
{"hookSpecificOutput": {
  "hookEventName": "PreToolUse",
  "permissionDecision": "deny",
  "permissionDecisionReason": "matt-pocock-superpowers-workflow has not been invoked in this session. Invoke it with the Skill tool, then retry."}}
```

Exit 0 with no output everywhere else: per the docs, that is "no decision", and the normal permission flow continues. The hook can deny; staying silent never approves.

## 6. Files

| Path | Responsibility |
| --- | --- |
| `scripts/hooks/gate.py` | the decision function above; stdlib only |
| `scripts/hooks/mark-skill.py` | `PostToolUse` marker writer |
| `scripts/hooks/install.sh` | merge hook entries into `~/.claude/settings.json`; back up first; idempotent |
| `scripts/hooks/uninstall.sh` | remove only entries tagged `_mpsw`; never touch the user's own hooks |
| `scripts/tests/test_gate.py` | crafted JSON on stdin → asserted decision, one case per numbered rule |
| `scripts/tests/test_hook_install.sh` | install into a temp `HOME`, assert merge and idempotency, uninstall, assert JSON-equal restore |

Hook scripts live in the repo and the global settings file references them by absolute path, so the code stays version-controlled and visible in the portfolio. If the repo moves, the missing script triggers rule "fail open" rather than breaking every project.

## 7. Testing

Each numbered rule in §5 gets a test case asserting the decision, plus:

- A correct run: no marker → deny; `mark-skill.py` fed a `Skill` event for the active router → allow.
- A wrong-skill run: `mark-skill.py` fed `{"skill":"tdd"}` → no marker → still denied.
- Subagent isolation: marker for `main` does not unlock `agent_id=aX`.
- Router resolution: with only `setup-matt-pocock-skills` present, no router is active → allow; with a router symlink pointing outside this repo, no router is active → allow.
- Anti-wedge: three denials then allow, with the warning present.
- Infrastructure failure: malformed stdin, unreadable marker dir → exit 0, no decision.

Install/uninstall is verified against a temp `HOME` so the real settings file is never involved in a test run.

## 8. Out of scope

- Overriding `disable-model-invocation` (impossible; §2).
- `SessionStart` context injection (tier 1 of the earlier proposal) — separate change, useful but not what "run every time" requires.
- Skill-frontmatter hooks enforcing test-first ordering (tier 2) — deferred; the gate is the prerequisite.
- Re-benchmarking with the gate installed. Worth doing, and it needs a `claude -p` harness that does not yet exist.

## 9. Success criteria

1. With the gate installed and no router invoked, an `Edit` and a `sed -i` in a git repo are both denied with the router named in the reason.
2. After the router is invoked, both succeed.
3. A repo listed in `mpsw-gate-ignore` is never gated.
4. `MPSW_GATE=off` bypasses everything.
5. `activate.sh none` disables the gate.
6. Uninstall leaves `~/.claude/settings.json` **JSON-equal** to its pre-install content: every unrelated key and every hook the user configured themselves survives, and no `_mpsw` entry remains. Byte-identity is not promised — install rewrites the file through a JSON serializer, so whitespace and key order may differ. A pre-install copy is kept at `settings.json.mpsw-backup` for manual recovery.
7. No test touches the real `~/.claude/settings.json`.
