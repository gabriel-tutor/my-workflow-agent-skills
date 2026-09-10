# Router Invocation Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Spec:** `docs/superpowers/specs/2026-09-11-router-invocation-gate-design.md`

**Goal:** Claude Code hooks that deny any file write until the active routing skill has been invoked in that session, globally, with per-repo opt-out and an anti-wedge release.

**Architecture:** Two hooks registered in `~/.claude/settings.json` pointing at scripts kept in this repo. `PostToolUse` on `Skill` writes a marker when the invoked skill is the active router; `PreToolUse` on `Edit|Write|MultiEdit|Bash` reads that marker and denies when it is absent. Nine ordered rules decide each call; infrastructure failure always allows.

**Tech Stack:** Python 3 (stdlib only) for decision logic, bash for install/uninstall, `unittest` + shell tests following the existing `scripts/tests/` convention.

## Global Constraints

- Python scripts: stdlib only, `#!/usr/bin/env python3`, module docstring with `Usage:` line — match `scripts/manifest.py`.
- Bash scripts: `set -euo pipefail`; macOS bash 3.2 (no `mapfile`, no `declare -A`); avoid `cmd | grep -q` under pipefail.
- **No test may read or write the real `~/.claude/settings.json`.** Tests set `HOME` to a temp dir.
- The gate **fails open** on any infrastructure error (bad stdin, missing dir, import failure). Only a policy miss denies.
- Router resolution is exact-name (`matt-pocock-workflow`, `matt-pocock-superpowers-workflow`) plus symlink-target-inside-repo, never substring.
- Commit after each task with the trailer `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>`.
- Repo root: `/Users/gabrieltutor/my-agent-workflow-skills`.

---

### Task 1: `scripts/hooks/gate.py` — the decision function

**Files:**
- Create: `scripts/hooks/gate.py`
- Test: `scripts/tests/test_gate.py`

**Interfaces:**
- Produces: `decide(event: dict, env: dict, home: Path) -> dict | None` — returns `None` to allow, or the deny payload dict. Importable for tests; `main()` reads stdin, prints JSON when denying, always exits 0.
- Consumes: `bash_writes()` from `scripts/jsonl_to_transcript.py` (verified importable; returns `['src/x.ts']` for `sed -i '' s/a/b/ src/x.ts && npm test`).
- Marker path: `<home>/.claude/mpsw-gate/<session_id>.<agent_key>`, `agent_key = event.get("agent_id") or "main"`.

- [ ] **Step 1: Write the failing test**

`scripts/tests/test_gate.py` — one case per numbered rule in spec §5, driving `decide()` directly:

```python
import json, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "scripts" / "hooks"))
from gate import decide  # noqa: E402

ROUTER = "matt-pocock-superpowers-workflow"


def home_with_router(active=True, ignore_lines=None):
    """Temp HOME with the router symlinked into .claude/skills the way activate.sh does."""
    h = Path(tempfile.mkdtemp())
    skills = h / ".claude" / "skills"
    skills.mkdir(parents=True)
    if active:
        target = REPO / "skills" / ROUTER
        (skills / ROUTER).symlink_to(target)
    if ignore_lines is not None:
        (h / ".claude" / "mpsw-gate-ignore").write_text("\n".join(ignore_lines) + "\n")
    return h


def git_repo():
    import subprocess
    d = Path(tempfile.mkdtemp())
    subprocess.run(["git", "init", "-q"], cwd=d, check=True)
    return d


def edit_event(cwd, path, session="s1", agent=None):
    e = {"hook_event_name": "PreToolUse", "tool_name": "Edit", "session_id": session,
         "cwd": str(cwd), "tool_input": {"file_path": str(path)}}
    if agent:
        e["agent_id"] = agent
    return e


class GateTest(unittest.TestCase):
    def test_denies_edit_in_git_repo_without_marker(self):
        h, r = home_with_router(), git_repo()
        d = decide(edit_event(r, r / "src" / "x.ts"), {}, h)
        self.assertIsNotNone(d)
        self.assertEqual(d["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertIn(ROUTER, d["hookSpecificOutput"]["permissionDecisionReason"])

    def test_allows_after_marker_written(self):
        h, r = home_with_router(), git_repo()
        m = h / ".claude" / "mpsw-gate"; m.mkdir(parents=True)
        (m / "s1.main").write_text(ROUTER)
        self.assertIsNone(decide(edit_event(r, r / "src" / "x.ts"), {}, h))

    def test_env_bypass(self):
        h, r = home_with_router(), git_repo()
        self.assertIsNone(decide(edit_event(r, r / "src" / "x.ts"), {"MPSW_GATE": "off"}, h))

    def test_no_router_active_allows(self):
        h, r = home_with_router(active=False), git_repo()
        self.assertIsNone(decide(edit_event(r, r / "src" / "x.ts"), {}, h))

    def test_setup_matt_pocock_skills_is_not_a_router(self):
        h, r = home_with_router(active=False), git_repo()
        (h / ".claude" / "skills" / "setup-matt-pocock-skills").mkdir()
        self.assertIsNone(decide(edit_event(r, r / "src" / "x.ts"), {}, h))

    def test_ignore_list_skips_repo(self):
        h_r = git_repo()
        h = home_with_router(ignore_lines=[str(h_r)])
        self.assertIsNone(decide(edit_event(h_r, h_r / "src" / "x.ts"), {}, h))

    def test_outside_git_repo_allows(self):
        h, d = home_with_router(), Path(tempfile.mkdtemp())
        self.assertIsNone(decide(edit_event(d, d / "notes.md"), {}, h))

    def test_scratchpad_and_tmp_allowed(self):
        h, r = home_with_router(), git_repo()
        for p in ("/tmp/probe.txt", "/var/folders/x/y/probe.txt"):
            self.assertIsNone(decide(edit_event(r, p), {}, h), p)

    def test_bash_non_write_allowed_write_denied(self):
        h, r = home_with_router(), git_repo()
        def bash(cmd):
            return {"hook_event_name": "PreToolUse", "tool_name": "Bash", "session_id": "s1",
                    "cwd": str(r), "tool_input": {"command": cmd}}
        self.assertIsNone(decide(bash("npm test"), {}, h))
        self.assertIsNotNone(decide(bash("sed -i '' s/a/b/ src/x.ts && npm test"), {}, h))
        self.assertIsNotNone(decide(bash("cat > src/y.ts <<'EOF'\nx\nEOF"), {}, h))

    def test_subagent_marker_is_separate(self):
        h, r = home_with_router(), git_repo()
        m = h / ".claude" / "mpsw-gate"; m.mkdir(parents=True)
        (m / "s1.main").write_text(ROUTER)
        self.assertIsNone(decide(edit_event(r, r / "src" / "x.ts"), {}, h))
        self.assertIsNotNone(decide(edit_event(r, r / "src" / "x.ts", agent="aX-1"), {}, h))

    def test_anti_wedge_releases_after_three_denials(self):
        h, r = home_with_router(), git_repo()
        ev = edit_event(r, r / "src" / "x.ts")
        for _ in range(3):
            self.assertIsNotNone(decide(ev, {}, h))
        d = decide(ev, {}, h)
        self.assertIsNone(d)

    def test_infrastructure_failure_fails_open(self):
        h, r = home_with_router(), git_repo()
        self.assertIsNone(decide({"tool_name": "Edit"}, {}, h))          # no cwd, no input
        self.assertIsNone(decide({}, {}, h))                              # empty event


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python3 -m unittest scripts.tests.test_gate 2>&1 | tail -3`
Expected: collection error — `ModuleNotFoundError: No module named 'gate'`.

- [ ] **Step 3: Write `scripts/hooks/gate.py`**

Implement `decide()` with the nine rules from spec §5 in order. Requirements:

- `ROUTERS = ("matt-pocock-superpowers-workflow", "matt-pocock-workflow")`.
- `active_router(home)`: for each name, `p = home/".claude"/"skills"/name`; return the name when `p.is_symlink()` and `p.resolve()` is inside `REPO/"skills"`. Return `None` otherwise. `REPO` is derived from `Path(__file__).resolve().parent.parent.parent`.
- `targets(event)`: for `Edit|Write|MultiEdit|NotebookEdit` take `tool_input.file_path` or `notebook_path`; for `Bash` take `bash_writes(tool_input.command)`. Resolve each against `event["cwd"]`. Return `[]` when nothing is found.
- Exempt prefixes: the event's `scratchpad_dir` when present, plus `/tmp`, `/private/tmp`, `/var/folders`, `/private/var/folders`. Use `Path.is_relative_to`, not `startswith`.
- Rule 7 detail: a `Bash` call with no write targets is allowed; a non-Bash call with no resolvable target is an infrastructure miss and is also allowed.
- Denial counter: `<marker_dir>/<key>.denials` holding an integer; increment on each deny; at `>= 3` return `None` and include `systemMessage` in the *allow* path by returning `{"systemMessage": "..."}`— **note:** `decide()` returns `None` for a plain allow, and a dict without `hookSpecificOutput` for allow-with-message; `main()` prints any dict it gets.
- Sweep entries older than 7 days in the marker dir on each write.
- Wrap the whole of `decide()`'s body in `try/except Exception: return None` so any unexpected shape fails open.
- `main()`: read stdin, `json.loads`, call `decide(event, os.environ, Path.home())`, print the returned dict as JSON when not `None`, `sys.exit(0)` always.

- [ ] **Step 4: Run the tests to verify they pass**

Run: `chmod +x scripts/hooks/gate.py && python3 -m unittest scripts.tests.test_gate -v 2>&1 | tail -5`
Expected: 12 tests, `OK`.

- [ ] **Step 5: Commit**

```bash
git add scripts/hooks/gate.py scripts/tests/test_gate.py
git commit -m "feat(hooks): gate.py decides whether a write requires the router first

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: `scripts/hooks/mark-skill.py` — the marker writer

**Files:**
- Create: `scripts/hooks/mark-skill.py`
- Modify: `scripts/tests/test_gate.py` (add `MarkSkillTest`)

**Interfaces:**
- Consumes: a `PostToolUse` event with `tool_name == "Skill"` and `tool_input.skill`.
- Produces: `<home>/.claude/mpsw-gate/<session_id>.<agent_key>` containing the router name, only when the invoked skill is the active router. Always exits 0.
- Reuses `active_router()` and the marker-path helper from `gate.py` by import, so the two hooks cannot disagree about either.

- [ ] **Step 1: Write the failing test**

Append to `scripts/tests/test_gate.py`:

```python
class MarkSkillTest(unittest.TestCase):
    def _run(self, home, event):
        import subprocess
        return subprocess.run(
            [sys.executable, str(REPO / "scripts" / "hooks" / "mark-skill.py")],
            input=json.dumps(event), text=True, capture_output=True,
            env={"HOME": str(home), "PATH": "/usr/bin:/bin"})

    def _skill_event(self, name, session="s1", agent=None):
        e = {"hook_event_name": "PostToolUse", "tool_name": "Skill",
             "session_id": session, "tool_input": {"skill": name}}
        if agent:
            e["agent_id"] = agent
        return e

    def test_router_invocation_writes_marker_and_unblocks(self):
        h, r = home_with_router(), git_repo()
        self.assertIsNotNone(decide(edit_event(r, r / "src" / "x.ts"), {}, h))
        self.assertEqual(self._run(h, self._skill_event(ROUTER)).returncode, 0)
        self.assertIsNone(decide(edit_event(r, r / "src" / "x.ts"), {}, h))

    def test_other_skill_does_not_unblock(self):
        h, r = home_with_router(), git_repo()
        self._run(h, self._skill_event("tdd"))
        self.assertIsNotNone(decide(edit_event(r, r / "src" / "x.ts"), {}, h))

    def test_subagent_marker_only_unblocks_that_agent(self):
        h, r = home_with_router(), git_repo()
        self._run(h, self._skill_event(ROUTER, agent="aX-1"))
        self.assertIsNone(decide(edit_event(r, r / "src" / "x.ts", agent="aX-1"), {}, h))
        self.assertIsNotNone(decide(edit_event(r, r / "src" / "x.ts"), {}, h))

    def test_malformed_input_exits_zero(self):
        h = home_with_router()
        import subprocess
        p = subprocess.run([sys.executable, str(REPO / "scripts" / "hooks" / "mark-skill.py")],
                           input="not json", text=True, capture_output=True,
                           env={"HOME": str(h), "PATH": "/usr/bin:/bin"})
        self.assertEqual(p.returncode, 0)
```

Run: `python3 -m unittest scripts.tests.test_gate.MarkSkillTest 2>&1 | tail -3`
Expected: failures — `mark-skill.py` does not exist.

- [ ] **Step 2: Write `scripts/hooks/mark-skill.py`**

Reads stdin; if `tool_name == "Skill"` and `tool_input.skill` equals `active_router(home)`, write the marker (creating the directory), sweep old entries, and clear any `.denials` file for that key. Wrap everything in `try/except Exception: pass`. Always `sys.exit(0)`.

- [ ] **Step 3: Run the tests**

Run: `chmod +x scripts/hooks/mark-skill.py && python3 -m unittest scripts.tests.test_gate -v 2>&1 | tail -5`
Expected: 16 tests, `OK`.

- [ ] **Step 4: Commit**

```bash
git add scripts/hooks/mark-skill.py scripts/tests/test_gate.py
git commit -m "feat(hooks): mark-skill.py records a router invocation per session and agent

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: `install.sh` / `uninstall.sh` with a temp-HOME test

**Files:**
- Create: `scripts/hooks/install.sh`, `scripts/hooks/uninstall.sh`
- Test: `scripts/tests/test_hook_install.sh`

**Interfaces:**
- `install.sh` merges four hook entries into `$HOME/.claude/settings.json` (creating the file if absent), backing the original up to `settings.json.mpsw-backup` first. Idempotent: running twice leaves exactly one copy of each entry. Marks its entries with `"_mpsw": true` so uninstall can find them.
- `uninstall.sh` removes only entries carrying `"_mpsw": true`, leaving every other hook untouched.
- Hook entries (absolute paths resolved at install time):
  - `PostToolUse` matcher `"Skill"` → `mark-skill.py`
  - `PreToolUse` matcher `"Edit|Write|MultiEdit|NotebookEdit"` → `gate.py`
  - `PreToolUse` matcher `"Bash"` → `gate.py`

- [ ] **Step 1: Write the failing test**

`scripts/tests/test_hook_install.sh`:

```bash
#!/usr/bin/env bash
# Installs the hooks into a throwaway HOME and verifies merge, idempotency and clean removal.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
export HOME="$TMP/home"; mkdir -p "$HOME/.claude"
fail() { echo "FAIL: $*" >&2; exit 1; }

# Pre-existing settings with a hook of the user's own that must survive.
cat > "$HOME/.claude/settings.json" <<'JSON'
{"model":"opus","hooks":{"PreToolUse":[{"matcher":"Bash","hooks":[{"type":"command","command":"/usr/bin/true"}]}]}}
JSON
cp "$HOME/.claude/settings.json" "$TMP/original.json"

"$REPO/scripts/hooks/install.sh" >/dev/null
COUNT=$(python3 -c "
import json,os
d=json.load(open(os.environ['HOME']+'/.claude/settings.json'))
print(sum(1 for e in d['hooks'].get('PreToolUse',[])+d['hooks'].get('PostToolUse',[]) for h in e['hooks'] if h.get('_mpsw')))")
[[ "$COUNT" == "3" ]] || fail "expected 3 managed hook handlers, got $COUNT"
python3 -c "
import json,os
d=json.load(open(os.environ['HOME']+'/.claude/settings.json'))
assert d['model']=='opus', 'unrelated settings key lost'
assert any(h.get('command')=='/usr/bin/true' for e in d['hooks']['PreToolUse'] for h in e['hooks']), 'user hook lost'
" || fail "install damaged existing settings"
[[ -f "$HOME/.claude/settings.json.mpsw-backup" ]] || fail "no backup written"

"$REPO/scripts/hooks/install.sh" >/dev/null   # idempotency
COUNT2=$(python3 -c "
import json,os
d=json.load(open(os.environ['HOME']+'/.claude/settings.json'))
print(sum(1 for e in d['hooks'].get('PreToolUse',[])+d['hooks'].get('PostToolUse',[]) for h in e['hooks'] if h.get('_mpsw')))")
[[ "$COUNT2" == "3" ]] || fail "not idempotent: $COUNT2 handlers after second install"

"$REPO/scripts/hooks/uninstall.sh" >/dev/null
python3 -c "
import json,os,sys
a=json.load(open('$TMP/original.json')); b=json.load(open(os.environ['HOME']+'/.claude/settings.json'))
sys.exit(0 if a==b else 1)" || fail "uninstall did not restore the original settings (JSON-equal)"

echo "test_hook_install: OK"
```

Run: `chmod +x scripts/tests/test_hook_install.sh && scripts/tests/test_hook_install.sh`
Expected: `No such file or directory` for `install.sh`.

- [ ] **Step 2: Write both scripts**

Both are thin bash wrappers around an inline `python3` heredoc that edits the JSON — bash 3.2 has no JSON support and the repo already depends on python3. `install.sh` resolves `REPO` from its own location so the absolute paths it writes are correct wherever the repo lives. Neither script touches anything but `$HOME/.claude/settings.json` and its backup.

- [ ] **Step 3: Run the test**

Run: `chmod +x scripts/hooks/install.sh scripts/hooks/uninstall.sh && scripts/tests/test_hook_install.sh`
Expected: `test_hook_install: OK`

- [ ] **Step 4: Verify the real settings file was untouched**

Run: `python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/settings.json'))); print('hooks key present:', 'hooks' in d)"`
Expected: `hooks key present: False` — the suite ran entirely in a temp HOME.

- [ ] **Step 5: Commit**

```bash
git add scripts/hooks/install.sh scripts/hooks/uninstall.sh scripts/tests/test_hook_install.sh
git commit -m "feat(hooks): idempotent install/uninstall that preserves existing settings

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Live end-to-end verification and documentation

**Files:**
- Modify: `README.md` (a "Guaranteeing the router runs" subsection under How to use it)
- Modify: `CHANGELOG.md`
- Create: `~/.claude/mpsw-gate-ignore` seeded with the user's other project

**Interfaces:**
- Consumes: everything from tasks 1–3.
- This task installs the gate for real, so it is the only one that writes outside the repo.

- [ ] **Step 1: Seed the opt-out list before installing**

```bash
printf '%s\n' "$HOME/clarewoodcapital" > ~/.claude/mpsw-gate-ignore
cat ~/.claude/mpsw-gate-ignore
```
This must happen *before* `install.sh` so the user's live client session is never gated, not even briefly.

- [ ] **Step 2: Run the whole suite, then install**

```bash
scripts/tests/test_activate.sh && scripts/tests/test_skills.sh && scripts/tests/test_hook_install.sh \
  && python3 -m unittest discover -s scripts/tests -p 'test_*.py' 2>&1 | tail -2
scripts/hooks/install.sh
```
Expected: all suites `OK`, then install reporting the three handlers it added.

- [ ] **Step 3: Verify the gate denies, in a real session**

```bash
D=$(mktemp -d) && git -C "$D" init -q && cd "$D" && mkdir src
claude -p --max-turns 4 "Create src/probe.ts containing the text hello. Use the Write tool." 2>&1 | tail -15
```
Expected: the write is denied and the transcript shows the router named in the reason. Record the exact wording in the report.

- [ ] **Step 4: Verify it allows after the router is invoked**

```bash
cd "$D" && claude -p --max-turns 8 "First invoke the matt-pocock-superpowers-workflow skill with the Skill tool. Then create src/probe.ts containing the text hello." 2>&1 | tail -8
ls src/probe.ts && cat src/probe.ts
```
Expected: `src/probe.ts` exists containing `hello`.

- [ ] **Step 5: Verify the opt-out and the env bypass**

```bash
E=$(mktemp -d "$HOME/clarewoodcapital-probe-XXXX") && git -C "$E" init -q   # matches the ignore prefix
cd "$E" && claude -p --max-turns 4 "Create note.txt containing hi. Use the Write tool." 2>&1 | tail -4
ls note.txt || echo "IGNORE LIST NOT WORKING"
cd "$D" && rm -f src/probe.ts && MPSW_GATE=off claude -p --max-turns 4 "Create src/probe.ts containing hello. Use the Write tool." 2>&1 | tail -4
ls src/probe.ts || echo "ENV BYPASS NOT WORKING"
rm -rf "$E"
```
Expected: both writes succeed. If either fails, stop and report — those are the two escape hatches and they must work before this ships.

- [ ] **Step 6: Document it**

Add to `README.md` under **How to use it**, after step 3:

```markdown
### Optional: guarantee the router runs

Skill invocation is normally the model's judgement call. These hooks make it deterministic — any file write is denied until the active router has been invoked in that session.

```bash
scripts/hooks/install.sh      # merges into ~/.claude/settings.json, backs it up first
scripts/hooks/uninstall.sh    # removes only what install.sh added
```

It applies to every git repo on the machine, subagents included. Three escape hatches, in order of reach:

| Escape | Effect |
| --- | --- |
| `~/.claude/mpsw-gate-ignore` | one path prefix per line; those repos are never gated |
| `MPSW_GATE=off` | bypasses everything for that session |
| `scripts/activate.sh none` | no router active, so nothing to enforce — the gate disables itself |

Writes outside a git repo, and writes to `/tmp` or the session scratchpad, are never gated. The gate fails open on any internal error: a broken hook can slow you down, it can't lock you out.

**These hooks run shell commands on your tool calls.** Read `scripts/hooks/gate.py` before installing — that advice applies to anyone's hooks, including these.
```

Add to `CHANGELOG.md` under a new `## Hooks` heading: the gate, its scope, and the escape hatches.

- [ ] **Step 7: Commit and push**

```bash
git add README.md CHANGELOG.md
git commit -m "docs: document the router invocation gate and its escape hatches

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
git push origin main
```
