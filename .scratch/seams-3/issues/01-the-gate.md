# 01: The gate

**What to build:** Claude can no longer change a project without a declaration. In any session with the plugin enabled, an `Edit`, `Write`, `MultiEdit` or `NotebookEdit` to a file outside the temp and Claude config directories, or a shell command the classifier labels a mutation, is refused with a reason that names the classification and the routes to take, until a process skill (a Seams skill, one of Matt Pocock's process skills, or a slash command the user typed for one) has been invoked for the current request. A new prompt starts a new request unless it is a short go-ahead. `trivial` exists as the cheap declaration and carries the not-trivial checklist. The ledger lives per session in the temp directory, survives compaction and resume, and is reset on startup and clear. Every hook runs on Python 3.9 and fails open.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] The gate module exposes, as pure functions: classify a shell command (label or none), decide a PreToolUse event against a ledger (allow, or deny with the reason), whether a prompt is a continuation, whether a skill name is a declaration, and the ledger read/write/reset.
- [ ] PreToolUse refuses an editor change to a project path without a declaration and allows it with one; a path under the temp directory or the Claude config directory is never refused.
- [ ] PreToolUse refuses a shell mutation without a declaration (redirect to a file, `sed -i`, `rm`, `git commit`, `npm install`, `prettier --write`, an inline Python program that writes a file) and allows read-only commands (`cat`, `grep`, `git status`, `git diff`, `npm test`, `tsc --noEmit`, `python3 -c 'print(1)'`).
- [ ] PostToolUse on `Skill` records a declaration for `matt-pocock-workflow:*` and for Matt Pocock's process skills by bare name, and records nothing for a Superpowers or other plugin's skill.
- [ ] UserPromptSubmit starts a new request for an ordinary prompt, keeps the request for a short go-ahead ("yes", "ok", "go ahead", "continue", a bare option letter), and records a declaration when the prompt is a slash command naming a process skill.
- [ ] SessionStart resets the ledger on `startup` and `clear`, keeps it on `compact`, and removes ledgers older than seven days.
- [ ] A subagent's tool call (input carrying `agent_id`) is judged against the same session ledger.
- [ ] Allowed changes are recorded in the ledger with the tool name and the path (or the label for shell mutations), and Markdown paths are marked as documentation. No command text and no prompt text is ever written.
- [ ] Every hook exits 0 with no output on malformed input or an internal error, writing the traceback to stderr.
- [ ] All hooks and the module import and run under Python 3.9 (`/usr/bin/python3` on macOS) and under the current `python3`.
- [ ] `hooks.json` registers the new hooks with the matchers above; `claude plugin validate --strict` passes.
- [ ] Unit tests cover the classifier table, each decision, the continuation rule and the ledger; a hook suite pipes JSON through each executable for the cases above; both are wired into `scripts/test.sh`.
- [ ] One headless run in a fixture workspace shows a refusal followed by a declaration and the retried edit going through.

**How to verify:** `scripts/test.sh` (the new unit and hook suites run inside it, once under the default `python3` and once under `/usr/bin/python3` when present); then `claude -p` in a copy of `tests/fixture` with the plugin enabled and a prompt such as "append a line to README.md with a shell command", and read the transcript: the first attempt is refused with "Seams gate", the second follows a `Skill` call.
