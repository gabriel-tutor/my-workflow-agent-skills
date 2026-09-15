#!/usr/bin/env bash
# Install the matt-pocock-workflow plugin on this machine, end to end.
#
#   curl -fsSL https://raw.githubusercontent.com/gabriel-tutor/seams/main/scripts/install.sh | bash
#   # or, from a clone:  scripts/install.sh
#
# What it does, in order (each step is skipped when already done, so re-running is safe):
#   1. Checks for the claude CLI, Node, and python3 at 3.9 or newer.
#   2. Installs Matt Pocock's skills into the Claude config directory's skills/ via skills.sh
#      (npx skills add mattpocock/skills) when any required one is missing. Needs a terminal.
#   3. Adds this repo as a plugin marketplace and installs, updates and enables matt-pocock-workflow
#      from it. The first `claude plugin` command that fails stops the installer, with its output.
#   4. Optionally disables the Superpowers plugin (MPW_DISABLE_SUPERPOWERS=1); by default it is left alone.
#
# It changes nothing but the plugin list and, in step 2, the skills directory: it writes nothing
# itself (the `claude plugin` commands record the marketplace and the enabled plugin in
# settings.json, as they do when run by hand), adds no permission rules, never edits Matt Pocock's
# files and never removes anything. It either succeeds or says exactly which step did not. The
# config directory is CLAUDE_CONFIG_DIR, else ~/.claude; the installer, the hook and skills.sh honour it.
set -euo pipefail

REPO="${MPW_REPO:-gabriel-tutor/seams}"
MARKETPLACE="${MPW_MARKETPLACE:-my-workflow-agent-skills}"
PLUGIN="matt-pocock-workflow"
CLAUDE_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
# The Matt Pocock skills the plugin invokes with the Skill tool: the same list as REQUIRED_SKILLS in
# plugin/hooks/session-start, which reports the missing ones at every session start.
REQUIRED_SKILLS=(grilling domain-modeling tdd diagnosing-bugs code-review codebase-design
                 setup-matt-pocock-skills setup-pre-commit setup-ts-deep-modules)
SKILLS_CMD="npx skills@latest add mattpocock/skills --agent claude-code --global"

say()  { printf '\n\033[1m%s\033[0m\n' "$*"; }
ok()   { printf '  ok   %s\n' "$*"; }
skip() { printf '  skip %s\n' "$*"; }
die()  { printf '\n  error: %s\n' "$*" >&2; exit 1; }
# plugin <args...>: `claude plugin <args...>`, output hidden while it succeeds; the first failure
# stops the installer, naming the command, its exit code and everything it printed.
plugin() {
  local out code=0
  out=$(claude plugin "$@" 2>&1) || code=$?
  [[ $code -eq 0 ]] && return 0
  printf '\n  error: `claude plugin %s` failed (exit %s):\n' "$*" "$code" >&2
  printf '%s\n' "$out" | sed 's/^/    /' >&2
  exit 1
}
# status_of <plugin@marketplace>: enabled, disabled, or nothing when it is not installed.
status_of() {
  claude plugin list 2>/dev/null \
    | awk -v id="$1" '$1 == "❯" && $2 == id {found = 1; next} found && $1 == "Status:" {print ($0 ~ /enabled/ ? "enabled" : "disabled"); exit}'
}
missing_skills() { local n; for n in "${REQUIRED_SKILLS[@]}"; do [[ -f "$CLAUDE_HOME/skills/$n/SKILL.md" ]] || printf '%s ' "$n"; done; }

# 1. Prerequisites
say "1. Prerequisites"
command -v claude >/dev/null || die "the claude CLI is not on PATH. Install Claude Code first: https://code.claude.com"
ok "claude $(claude --version 2>/dev/null | head -1)"
command -v node >/dev/null || die "node is not on PATH; skills.sh needs it to install Matt Pocock's skills"
ok "node $(node --version)"
command -v python3 >/dev/null || die "python3 is not on PATH; the plugin's hooks need it"
PY_VERSION="$(python3 --version 2>&1 | awk '{print $2}')"
IFS=. read -r PY_MAJOR PY_MINOR _ <<< "$PY_VERSION"
[[ ${PY_MAJOR:-0} -gt 3 || ( ${PY_MAJOR:-0} -eq 3 && ${PY_MINOR:-0} -ge 9 ) ]] \
  || die "python3 on PATH is $PY_VERSION; the plugin's hooks need Python 3.9 or newer first on PATH"
ok "python3 $PY_VERSION"

# 2. Matt Pocock's skills
say "2. Matt Pocock's skills"
MISSING="$(missing_skills)"
if [[ -z "$MISSING" ]]; then
  skip "all ${#REQUIRED_SKILLS[@]} required skills are at $CLAUDE_HOME/skills"
else
  echo "  missing from $CLAUDE_HOME/skills: $MISSING"
  { : </dev/tty; } 2>/dev/null \
    || die "no terminal to pick skills in. Run \`$SKILLS_CMD\` yourself (add --skill '*' -y to take all of them), then re-run this installer"
  echo "  installing with skills.sh (interactive: pick the skills you want; keep the ones listed above)"
  npx --yes skills@latest add mattpocock/skills --agent claude-code --global </dev/tty \
    || die "skills.sh failed; see https://github.com/mattpocock/skills#installation"
  MISSING="$(missing_skills)"
  [[ -z "$MISSING" ]] || die "still missing from $CLAUDE_HOME/skills after skills.sh: $MISSING. Re-run \`$SKILLS_CMD\` and pick them"
  ok "installed"
fi

# 3. The plugin
say "3. The $PLUGIN plugin"
if claude plugin marketplace list 2>/dev/null | awk -v m="$MARKETPLACE" '$1 == "❯" && $2 == m {found = 1} END {exit !found}'; then
  plugin marketplace update "$MARKETPLACE"; skip "marketplace $MARKETPLACE already known; refreshed"
else
  plugin marketplace add "$REPO"; ok "marketplace $MARKETPLACE added from $REPO"
fi
case "$(status_of "$PLUGIN@$MARKETPLACE")" in
  enabled|disabled) plugin update "$PLUGIN@$MARKETPLACE"; ok "plugin already installed; updated to the latest version" ;;
  *)                plugin install "$PLUGIN@$MARKETPLACE"; ok "plugin installed" ;;
esac
case "$(status_of "$PLUGIN@$MARKETPLACE")" in
  enabled)  skip "plugin already enabled" ;;
  disabled) plugin enable "$PLUGIN@$MARKETPLACE"; ok "plugin enabled" ;;
  *)        die "$PLUGIN@$MARKETPLACE is not in \`claude plugin list\` after the install" ;;
esac

# 4. Superpowers
say "4. Superpowers"
SP="superpowers@claude-plugins-official"
if [[ "${MPW_DISABLE_SUPERPOWERS:-0}" != "1" ]]; then
  skip "left as is (set MPW_DISABLE_SUPERPOWERS=1 to disable it; Matt Pocock's skills lead either way, see the README)"
elif [[ "$(status_of "$SP")" == enabled ]]; then
  plugin disable "$SP"; ok "disabled (one bootstrap per session)"
else
  skip "not installed or already disabled"
fi

say "Done. Restart Claude Code, then in any repo:"
cat <<'TXT'
  - say "check what this repo has and what it's missing"  -> the foundations survey (once per repo)
  - describe a feature, a bug, or a change                -> the workflow routes it
  - to confirm it's live: ask "which skill applies before a bug fix?" (expect: diagnosing-bugs)
Tested platforms: the operating systems, Python, Node and Claude Code versions this was tested with are
listed in docs/compatibility.md (github.com/gabriel-tutor/seams). Windows is not supported.
TXT
