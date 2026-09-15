"""The gate: the rules the matt-pocock-workflow hooks share.

A change to the project is refused until the current request has a declaration: a Skill
invocation of a process skill, or a slash command the user typed for one. This module holds
the pure parts (what counts as a change, what counts as a declaration, what a continuation
is, the ledger's shape and the decisions) so the hooks stay thin and the routing harness can
score a shell write the same way the gate does. Python 3.9: macOS's system interpreter runs
the hooks when nothing newer is first on PATH.
"""
from __future__ import annotations

import os
import re
import shlex
import tempfile
from typing import Optional

# --- Shell commands -----------------------------------------------------------------------

FILE_COMMANDS = {"rm", "rmdir", "unlink", "mv", "cp", "touch", "mkdir", "ln", "chmod", "chown",
                 "truncate", "tee", "install", "dd", "patch", "shred"}
GIT_WRITES = {"add", "commit", "rm", "mv", "checkout", "switch", "restore", "reset", "rebase",
              "merge", "cherry-pick", "revert", "apply", "am", "clean", "push", "pull", "init",
              "clone"}
GIT_READ_FLAGS = {"stash": {"list", "show"}, "tag": {"-l", "--list"}, "worktree": {"list"}}
GIT_BRANCH_WRITE_FLAGS = {"-d", "-D", "-m", "-M", "--delete", "--move", "--force"}
NODE_MANAGERS = {"npm", "pnpm", "yarn", "bun"}
NODE_WRITES = {"install", "i", "add", "remove", "rm", "uninstall", "un", "update", "up", "upgrade",
               "link", "unlink", "init", "create", "ci", "dedupe", "prune"}
OTHER_MANAGERS = {"pip": {"install", "uninstall"}, "pip3": {"install", "uninstall"},
                  "uv": {"add", "remove", "sync", "pip"}, "poetry": {"add", "remove", "install", "update"},
                  "cargo": {"add", "remove", "install"}, "go": {"get", "install"},
                  "gem": {"install", "uninstall"}}
WRAPPERS = {"sudo", "env", "time", "nice", "nohup", "command", "exec", "xargs"}
INTERPRETERS = re.compile(r"^(python[0-9.]*|node|ruby|perl|deno|bun)$")
INLINE_FLAGS = {"-c", "-e", "--eval", "-p", "--print", "-"}
WRITE_PATTERNS = re.compile(
    r"open\([^)]*['\"][wax]b?\+?['\"]|mode\s*=\s*['\"][wax]|\.write_text\(|\.write_bytes\(|\.writelines\("
    r"|writeFile(Sync)?\(|appendFile(Sync)?\(|os\.remove\(|os\.unlink\(|\.unlink\(|os\.rename\("
    r"|\.rename\(|shutil\.|os\.makedirs\(|\.mkdir\(|rmSync\(|rmdirSync\(|unlinkSync\(|renameSync\("
    r"|mkdirSync\(|copyFile|File\.write|File\.open\([^)]*['\"][wa]|IO\.write|\.truncate\(")
FD_DUP = re.compile(r"^\d*>&")
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


def _tokens(command: str) -> list:
    """Shell words with quotes kept, so a quoted '>' is not an operator."""
    lexer = shlex.shlex(command, posix=False, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError:                        # unbalanced quotes: fall back to a rough split
        return re.findall(r"&&|\|\||[;|]|>>|>|<<|<|\S+", command)


def _segments(tokens: list) -> list:
    """The simple commands of a pipeline or list, each a token list."""
    out, current = [], []
    for token in tokens:
        if token in {";", "&&", "||", "|", "&", "|&"}:
            if current:
                out.append(current)
            current = []
        else:
            current.append(token)
    if current:
        out.append(current)
    return out


def _unquote(token: str) -> str:
    if len(token) >= 2 and token[0] == token[-1] and token[0] in "'\"":
        return token[1:-1]
    return token


def _words(segment: list) -> list:
    """The command and its arguments, after leading assignments and wrappers."""
    words = list(segment)
    while words and ASSIGNMENT.match(words[0]):
        words.pop(0)
    while words and os.path.basename(_unquote(words[0])) in WRAPPERS:
        words.pop(0)
        while words and words[0].startswith("-"):
            words.pop(0)
    return words


def _redirect_target(segment: list) -> Optional[str]:
    for i, token in enumerate(segment):
        if token in {">", ">>", "&>", "&>>"} or (token.endswith(">") and token[:-1].isdigit()):
            target = segment[i + 1] if i + 1 < len(segment) else None
            if target and not target.startswith("&") and _unquote(target) != "/dev/null":
                return _unquote(target)
        elif FD_DUP.match(token):
            continue
    return None


def _git_label(words: list) -> Optional[str]:
    rest = words[1:]
    while rest and rest[0].startswith("-"):
        takes_value = rest[0] in {"-C", "-c", "--git-dir", "--work-tree"}
        rest = rest[2:] if takes_value and len(rest) > 1 else rest[1:]
    if not rest:
        return None
    sub, flags = _unquote(rest[0]), [_unquote(r) for r in rest[1:]]
    if sub in GIT_WRITES:
        return f"git {sub}"
    if sub == "branch":                       # a write only with a delete or move flag
        return "git branch -d" if any(f in GIT_BRANCH_WRITE_FLAGS for f in flags) else None
    if sub in GIT_READ_FLAGS:                 # stash, tag, worktree: writes unless listing
        return None if any(f in GIT_READ_FLAGS[sub] for f in flags) else f"git {sub}"
    return None


def _inline_program_writes(words: list, command: str) -> bool:
    if not INTERPRETERS.match(os.path.basename(_unquote(words[0]))):
        return False
    inline = any(_unquote(w) in INLINE_FLAGS for w in words[1:]) or "<<" in command
    return bool(inline and WRITE_PATTERNS.search(command))


def classify_segment(segment: list, command: str) -> Optional[str]:
    target = _redirect_target(segment)
    if target is not None:
        return "a redirect to a file"
    words = _words(segment)
    if not words:
        return None
    base = os.path.basename(_unquote(words[0]))
    args = [_unquote(w) for w in words[1:]]
    if base in {"bash", "sh", "zsh"} and "-c" in args:
        inner = args[args.index("-c") + 1] if args.index("-c") + 1 < len(args) else ""
        return classify_command(inner)
    if base in FILE_COMMANDS:
        return base
    if base == "sed" and any(a in {"-i", "--in-place"} or a.startswith("-i") and a[1:2] == "i" or a.startswith("--in-place=") for a in args):
        return "sed -i"
    if base in {"perl", "ruby"} and any(re.match(r"^-[a-zA-Z]*i", a) for a in args):
        return f"{base} -i"
    if base == "git":
        return _git_label(words)
    if base in NODE_MANAGERS:
        sub = args[0] if args else ("install" if base == "yarn" else "")
        if sub in NODE_WRITES:
            return f"{base} {sub}"
    if base in OTHER_MANAGERS and args and args[0] in OTHER_MANAGERS[base]:
        return f"{base} {' '.join(args[:2]) if base == 'uv' and args[0] == 'pip' else args[0]}"
    if "--write" in args:
        return "a --write flag"
    if "--fix" in args:
        return "a --fix flag"
    if "-w" in args and any(a in {"prettier", "biome"} for a in [base] + args):
        return "a --write flag"
    if base == "curl" and any(a in {"-o", "-O", "--output", "--remote-name"} or a.startswith("-o") and len(a) > 2 for a in args):
        return "a download to a file"
    if base == "wget" and not any(a in {"-O-", "-qO-"} or (a in {"-O", "--output-document"} and args[args.index(a) + 1:args.index(a) + 2] == ["-"]) for a in args):
        return "a download to a file"
    if base == "find":
        if "-delete" in args:
            return "find -delete"
        if "-exec" in args or "-execdir" in args:
            flag = "-exec" if "-exec" in args else "-execdir"
            after = args[args.index(flag) + 1:]
            if after and os.path.basename(after[0]) in FILE_COMMANDS:
                return f"find -exec {os.path.basename(after[0])}"
    if _inline_program_writes(words, command):
        return "an inline program that writes"
    return None


def classify_command(command: str) -> Optional[str]:
    """The label for what a shell command changes, or None when it looks read-only.

    A best-effort mesh: the common ways of changing files from a shell. It never proves a
    command has no side effects, and the label is what a refusal names.
    """
    if not command or not command.strip():
        return None
    for segment in _segments(_tokens(command)):
        label = classify_segment(segment, command)
        if label:
            return label
    return None


# --- Declarations and requests ------------------------------------------------------------

PLUGIN_PREFIX = "matt-pocock-workflow:"
# Matt Pocock's process skills, by bare name. Domain skills (frontend-design, pdf, ...) and
# other plugins' process skills (superpowers:brainstorming) do not open the gate.
PROCESS_SKILLS = {
    "grilling", "grill-me", "grill-with-docs", "domain-modeling", "tdd", "diagnosing-bugs",
    "code-review", "codebase-design", "prototype", "resolving-merge-conflicts", "research",
    "wizard", "setup-matt-pocock-skills", "setup-pre-commit", "setup-ts-deep-modules",
    "wayfinder", "triage", "improve-codebase-architecture", "handoff", "ask-matt",
    "implement", "to-spec", "to-tickets",
}
GO_WORDS = {"y", "yes", "yep", "yeah", "yup", "ok", "okay", "k", "sure", "go", "continue",
            "proceed", "next", "approved", "approve", "confirmed", "confirm", "agreed", "lgtm",
            "fine", "correct", "right", "carry", "keep", "do", "sounds", "looks", "option",
            "please"}
OPTION = re.compile(r"^(option\s+)?[a-d1-9]$")


def is_declaration(skill: str) -> bool:
    """Whether invoking this skill declares a route for the current request."""
    if not skill:
        return False
    if skill.startswith(PLUGIN_PREFIX):
        return len(skill) > len(PLUGIN_PREFIX)
    return skill in PROCESS_SKILLS


def slash_declaration(prompt: str) -> Optional[str]:
    """The process skill a typed slash command names, or None."""
    text = (prompt or "").strip()
    if not text.startswith("/"):
        return None
    name = text[1:].split()[0] if text[1:].split() else ""
    return name if is_declaration(name) else None


def is_continuation(prompt: str) -> bool:
    """A short go-ahead ("yes", "ok, do that", "option 2") that keeps the current request."""
    text = re.sub(r"[^\w\s-]", " ", (prompt or "").lower()).strip()
    if not text or len(text) > 40:
        return False
    words = text.split()
    if len(words) > 5:
        return False
    return OPTION.match(text) is not None or words[0] in GO_WORDS


# --- The ledger ---------------------------------------------------------------------------
# One JSON file per session: the current request's declarations, changes and last
# verification. Skill names, tool names and paths only; never command or prompt text.

import json
import time

LEDGER_VERSION = 1


def _safe_name(session_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", session_id or "unknown")[:120]


def ledger_root(root: Optional[str] = None) -> str:
    return root or os.path.join(tempfile.gettempdir(), "seams")


def ledger_path(session_id: str, root: Optional[str] = None) -> str:
    return os.path.join(ledger_root(root), _safe_name(session_id) + ".json")


def empty_ledger(session_id: str) -> dict:
    return {"version": LEDGER_VERSION, "session": session_id, "started": time.time(),
            "declarations": [], "changes": [], "verified_at": None}


def load_ledger(session_id: str, root: Optional[str] = None) -> dict:
    """The session's ledger, or an empty one when there is none or it cannot be read."""
    try:
        with open(ledger_path(session_id, root), encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and data.get("version") == LEDGER_VERSION:
            for key in ("declarations", "changes"):
                data.setdefault(key, [])
            data.setdefault("verified_at", None)
            return data
    except (OSError, ValueError):
        pass
    return empty_ledger(session_id)


def save_ledger(session_id: str, ledger: dict, root: Optional[str] = None) -> None:
    """Write atomically, readable by this user only."""
    path = ledger_path(session_id, root)
    directory = os.path.dirname(path)
    os.makedirs(directory, mode=0o700, exist_ok=True)
    os.chmod(directory, 0o700)
    tmp = f"{path}.{os.getpid()}.tmp"
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(ledger, f)
    os.replace(tmp, path)


def reset_ledger(session_id: str, root: Optional[str] = None) -> None:
    try:
        os.remove(ledger_path(session_id, root))
    except OSError:
        pass


def new_request(ledger: dict) -> dict:
    ledger["started"] = time.time()
    ledger["declarations"] = []
    ledger["changes"] = []
    ledger["verified_at"] = None
    return ledger


def add_declaration(ledger: dict, skill: str, agent_id: Optional[str] = None) -> None:
    ledger["declarations"].append({"skill": skill, "at": time.time(), "agent": agent_id})


def add_change(ledger: dict, change: dict) -> None:
    ledger["changes"].append(dict(change, at=time.time()))


def mark_verified(ledger: dict) -> None:
    ledger["verified_at"] = time.time()


def cleanup_ledgers(root: Optional[str] = None, days: int = 7) -> None:
    """Remove ledgers no session has touched for `days`."""
    directory = ledger_root(root)
    cutoff = time.time() - days * 24 * 3600
    try:
        names = os.listdir(directory)
    except OSError:
        return
    for name in names:
        path = os.path.join(directory, name)
        try:
            if name.endswith(".json") and os.stat(path).st_mtime < cutoff:
                os.remove(path)
        except OSError:
            pass


# --- Project changes and the decision ------------------------------------------------------

EDITOR_TOOLS = {"Edit": "file_path", "Write": "file_path", "MultiEdit": "file_path",
                "NotebookEdit": "notebook_path"}
DOC_SUFFIXES = (".md", ".markdown", ".mdx")
TEMP_ROOTS = ("/tmp", "/private/tmp")     # plus tempfile.gettempdir(), which honors TMPDIR


def config_dir(explicit: Optional[str] = None) -> str:
    return explicit or os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")


def _under(path: str, root: str) -> bool:
    root = os.path.realpath(root)
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


def is_exempt_path(path: str, config: Optional[str] = None) -> bool:
    """Temp directories and the Claude config directory are not the project."""
    real = os.path.realpath(path)
    if real == "/dev/null":
        return True
    roots = (tempfile.gettempdir(), config_dir(config)) + TEMP_ROOTS
    return any(_under(real, root) for root in roots)


def change_for_event(event: dict, config_dir: Optional[str] = None) -> Optional[dict]:
    """The project change a PreToolUse event would make, or None when it makes none.

    Editor tools: the file, unless it is under a temp or config directory. Bash: the
    classifier's label. Anything else: nothing.
    """
    tool = event.get("tool_name") or ""
    tool_input = event.get("tool_input") or {}
    if tool in EDITOR_TOOLS:
        path = tool_input.get(EDITOR_TOOLS[tool]) or ""
        if not path:
            return None
        if not os.path.isabs(path):
            path = os.path.join(event.get("cwd") or os.getcwd(), path)
        path = os.path.normpath(path)
        if is_exempt_path(path, config_dir):
            return None
        return {"tool": tool, "path": path, "doc": path.lower().endswith(DOC_SUFFIXES)}
    if tool == "Bash":
        label = classify_command(tool_input.get("command") or "")
        if label:
            return {"tool": "Bash", "label": label, "doc": False}
    return None


ROUTES = ("Route it first, with the Skill tool: `diagnosing-bugs` for something broken, "
          "`matt-pocock-workflow:grill` for a change to behavior, `tdd` or "
          "`matt-pocock-workflow:implement` to keep building an agreed design, "
          "`matt-pocock-workflow:trivial` for a change with no effect on behavior, data shape "
          "or security. Then retry this call.")


def deny_reason(change: dict) -> str:
    what = f"`{change['label']}`" if change["tool"] == "Bash" else f"editing `{change['path']}`"
    return (f"Seams gate: {what} changes the project, and no workflow skill has been declared "
            f"for this request. {ROUTES}")


def decide_pre_tool_use(event: dict, ledger: dict, config_dir: Optional[str] = None) -> dict:
    """Allow, or deny with a reason. The change to record travels with an allow."""
    change = change_for_event(event, config_dir)
    if change is None:
        return {"decision": "allow", "reason": None, "change": None}
    if not ledger.get("declarations"):
        return {"decision": "deny", "reason": deny_reason(change), "change": None}
    return {"decision": "allow", "reason": None, "change": change}
