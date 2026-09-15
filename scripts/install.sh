#!/usr/bin/env bash
# Install the matt-pocock-workflow plugin on this machine, end to end.
#
#   curl -fsSL https://raw.githubusercontent.com/gabriel-tutor/seams/main/scripts/install.sh | bash
#   # or, from a clone:  scripts/install.sh
#
# What it does, in order (each step is skipped when already done, so re-running is safe):
#   1. Checks for the claude CLI and Node.
#   2. Installs Matt Pocock's skills into ~/.claude/skills via skills.sh (npx skills add mattpocock/skills)
#      unless they are already there.
#   3. Adds this repo as a plugin marketplace from GitHub and installs matt-pocock-workflow from it.
#   4. Adds the Read permission rules the plugin needs to ~/.claude/settings.json (backed up first).
#   5. Optionally disables the Superpowers plugin (MPW_DISABLE_SUPERPOWERS=1); by default it is left alone.
#
# It never edits Matt Pocock's files, never removes anything, and prints what to do next.
set -euo pipefail

REPO="${MPW_REPO:-gabriel-tutor/seams}"
MARKETPLACE="${MPW_MARKETPLACE:-my-workflow-agent-skills}"
PLUGIN="matt-pocock-workflow"
CLAUDE_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SETTINGS="$CLAUDE_HOME/settings.json"

say()  { printf '\n\033[1m%s\033[0m\n' "$*"; }
ok()   { printf '  ok   %s\n' "$*"; }
skip() { printf '  skip %s\n' "$*"; }
die()  { printf '\n  error: %s\n' "$*" >&2; exit 1; }

# 1. Prerequisites
say "1. Prerequisites"
command -v claude >/dev/null || die "the claude CLI is not on PATH. Install Claude Code first: https://code.claude.com"
ok "claude $(claude --version 2>/dev/null | head -1)"
command -v node >/dev/null || die "node is not on PATH; skills.sh needs it to install Matt Pocock's skills"
ok "node $(node --version)"
command -v python3 >/dev/null || die "python3 is not on PATH; the plugin's hook needs it"
ok "python3 $(python3 --version 2>&1 | awk '{print $2}')"

# 2. Matt Pocock's skills
say "2. Matt Pocock's skills"
if [[ -f "$CLAUDE_HOME/skills/grilling/SKILL.md" ]]; then
  skip "already installed at $CLAUDE_HOME/skills ($(readlink "$CLAUDE_HOME/skills/grilling" 2>/dev/null || echo 'real directory'))"
else
  echo "  installing with skills.sh (interactive: pick the skills you want; keep setup-matt-pocock-skills)"
  npx --yes skills@latest add mattpocock/skills --agent claude-code --global </dev/tty
  [[ -f "$CLAUDE_HOME/skills/grilling/SKILL.md" ]] || die "grilling/SKILL.md still missing after install; see https://github.com/mattpocock/skills#installation"
  ok "installed"
fi

# 3. The plugin
say "3. The $PLUGIN plugin"
if claude plugin marketplace list 2>/dev/null | grep -q "^ *❯\? *$MARKETPLACE\$\|^ *$MARKETPLACE\$\|❯ $MARKETPLACE"; then
  skip "marketplace $MARKETPLACE already known"
else
  claude plugin marketplace add "$REPO" >/dev/null && ok "marketplace $MARKETPLACE added from github.com/$REPO"
fi
if claude plugin list 2>/dev/null | grep -q "$PLUGIN@$MARKETPLACE"; then
  claude plugin update "$PLUGIN@$MARKETPLACE" >/dev/null 2>&1 && ok "plugin already installed; updated to the latest version" || skip "plugin already installed"
else
  claude plugin install "$PLUGIN@$MARKETPLACE" >/dev/null && ok "plugin installed"
fi
claude plugin enable "$PLUGIN@$MARKETPLACE" >/dev/null 2>&1 || true

# 4. Read permissions
say "4. Read permissions in $SETTINGS"
[[ -f "$SETTINGS" ]] || echo '{}' > "$SETTINGS"
cp "$SETTINGS" "$SETTINGS.pre-mpw-install" && ok "backup: $SETTINGS.pre-mpw-install"
SKILLS_TARGET="$(cd "$CLAUDE_HOME/skills/grilling" 2>/dev/null && pwd -P | sed 's|/grilling$||')"
SETTINGS="$SETTINGS" CLAUDE_HOME="$CLAUDE_HOME" SKILLS_TARGET="$SKILLS_TARGET" python3 - <<'PY'
import json, os, pathlib
p = pathlib.Path(os.environ["SETTINGS"]); home = os.environ["CLAUDE_HOME"]; target = os.environ["SKILLS_TARGET"]
d = json.loads(p.read_text() or "{}")
allow = d.setdefault("permissions", {}).setdefault("allow", [])
def rule(path):
    return f"Read({path}/**)" if path.startswith("~") else f"Read(/{path}/**)"   # leading // makes a Read rule absolute
wanted = [rule("~/.claude/skills"), rule("~/.claude/plugins")]
if target and not target.startswith(os.path.expanduser("~/.claude/skills")):
    wanted.append(rule(target.replace(os.path.expanduser("~"), "~", 1) if target.startswith(os.path.expanduser("~")) else target))
added = [r for r in wanted if r not in allow]
allow.extend(added)
p.write_text(json.dumps(d, indent=2) + "\n")
for r in wanted: print(("  ok   added " if r in added else "  skip present ") + r)
PY

# 5. Superpowers
say "5. Superpowers"
if [[ "${MPW_DISABLE_SUPERPOWERS:-0}" == "1" ]]; then
  claude plugin disable superpowers@claude-plugins-official >/dev/null 2>&1 && ok "disabled (one bootstrap per session)" || skip "not installed"
else
  skip "left as is (set MPW_DISABLE_SUPERPOWERS=1 to disable it; Matt Pocock's skills win the overlaps either way)"
fi

say "Done. Restart Claude Code, then in any repo:"
cat <<'TXT'
  - say "check what this repo has and what it's missing"  -> the foundations survey (once per repo)
  - describe a feature, a bug, or a change                -> the workflow routes it
  - to confirm it's live: ask "which skill applies before a bug fix?" (expect: diagnosing-bugs)
TXT
