# 08: Installer that tells the truth

**What to build:** On a new machine the one-command install either succeeds or says exactly why it did not, and it changes nothing but the plugin list. The installer checks the `claude` CLI, Node, and `python3` at 3.9 or newer (naming the version found when too old); installs Matt Pocock's skills through skills.sh when missing; adds the marketplace, installs, updates and enables the plugin, stopping with a message the moment any `claude plugin` command fails; no longer writes settings.json at all (no Read rules, no backup); keeps the optional Superpowers disable; and prints the tested platforms and the next steps. `docs/compatibility.md` records the tested combinations: operating systems, Python, Claude Code version, Matt Pocock's skills commit and file hashes, Superpowers version alongside. The README's install section matches.

**Blocked by:** 04

**Status:** ready-for-agent

- [ ] A run in a fixture home with a stub `claude` leaves settings.json byte-identical and issues marketplace add, install and enable.
- [ ] A stub whose `plugin install` fails makes the installer exit non-zero with a message naming the step; nothing after it runs.
- [ ] A second run changes nothing and exits 0.
- [ ] A fixture home without Matt Pocock's skills and no tty exits non-zero with a message.
- [ ] A `python3` older than 3.9 on PATH exits non-zero naming the version.
- [ ] `docs/compatibility.md` exists with the fields above filled from this machine and CI.
- [ ] A real install from this local repo into a fresh `CLAUDE_CONFIG_DIR` succeeds and a session there shows the bootstrap.

**How to verify:** `scripts/test.sh` (the installer suite); then `CLAUDE_CONFIG_DIR=$(mktemp -d) MPW_REPO=$PWD scripts/install.sh` followed by `CLAUDE_CONFIG_DIR=<that dir> claude -p 'which skill applies before a bug fix?'` answering `diagnosing-bugs`.
