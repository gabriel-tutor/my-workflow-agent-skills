#!/usr/bin/env bash
# Activate exactly one of this repo's skills in Claude Code by symlinking it into the skills directory.
#
#   scripts/activate.sh matt-pocock-workflow
#   scripts/activate.sh matt-pocock-superpowers-workflow
#   scripts/activate.sh none      # remove both managed links
#   scripts/activate.sh status    # show what the skills dir currently points at
#
# Safety: only symlinks whose target is inside this repo's skills/ are ever created or removed.
# A real directory or a symlink to anywhere else stops the script with exit 2.
# Override the skills directory for tests: CLAUDE_SKILLS_DIR=/tmp/x scripts/activate.sh ...
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
MANAGED=(matt-pocock-workflow matt-pocock-superpowers-workflow)

owned_link() {  # true when $1 is a symlink pointing inside $REPO/skills
  [[ -L "$1" ]] || return 1
  local target
  target="$(readlink "$1")"
  [[ "$target" == "$REPO/skills/"* ]]
}

status() {
  local s p
  for s in "${MANAGED[@]}"; do
    p="$SKILLS_DIR/$s"
    if [[ -L "$p" ]]; then
      echo "$s -> $(readlink "$p")"
    elif [[ -e "$p" ]]; then
      echo "$s : REAL DIRECTORY (not managed by this script)"
    else
      echo "$s : not installed"
    fi
  done
}

unlink_managed() {  # remove both managed links; refuse anything that is not ours
  local s p
  for s in "${MANAGED[@]}"; do
    p="$SKILLS_DIR/$s"
    if [[ -e "$p" || -L "$p" ]]; then
      if owned_link "$p"; then
        rm "$p"
        echo "unlinked $s"
      else
        echo "refusing to touch $p: it is not a symlink into $REPO/skills" >&2
        exit 2
      fi
    fi
  done
}

case "${1:-}" in
  status) status ;;
  none) unlink_managed ;;
  matt-pocock-workflow|matt-pocock-superpowers-workflow)
    if [[ ! -d "$REPO/skills/$1" ]]; then
      echo "missing $REPO/skills/$1" >&2
      exit 1
    fi
    unlink_managed
    mkdir -p "$SKILLS_DIR"
    ln -s "$REPO/skills/$1" "$SKILLS_DIR/$1"
    echo "activated $1 -> $REPO/skills/$1"
    ;;
  *)
    echo "usage: $0 <matt-pocock-workflow|matt-pocock-superpowers-workflow|none|status>" >&2
    exit 1
    ;;
esac
