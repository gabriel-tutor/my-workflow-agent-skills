# Compatibility

What Seams was tested with, and where. "Tested" means `scripts/test.sh` passed on that combination: the gate module's unit tests, the hook suites fed JSON on stdin, the session-start suite against fixture homes, the installer suite against a stub `claude`, the static plugin checks (where the `claude` CLI exists) and the sandbox-workspace suite. The live headless runs (the model choosing a route) are recorded separately in [plugin-behavior-tests.md](plugin-behavior-tests.md). A combination not listed here is untested, not unsupported; Windows is unsupported (the hooks are Python executables run through `env`).

The plugin under test is this repository at the commit that last changed this file (`git log -1 --format=%h -- docs/compatibility.md`). The installer prints a pointer to this file at the end of every run.

## Observed

The developer's machine, 2026-09-16. Every suite `scripts/test.sh` can run there ran and passed; the exact counts are in the ticket records under `.scratch/seams-3/issues/`.

| Field | Value |
| --- | --- |
| Operating system | macOS 15.7.9 (24G830), arm64 |
| Python | 3.14.6 at `/usr/local/bin/python3` (first on PATH: the hooks run under it) and 3.9.6 at `/usr/bin/python3` (the system interpreter: the gate unit tests, the hook suite and the session-start suite run under it as well, `scripts/test.sh` adds those runs whenever it differs from the default `python3`) |
| Node | v22.23.1 (skills.sh and the sandbox fixture) |
| Shell | bash 3.2.57 at `/bin/bash` (the shell suites run under the system bash; nothing in them needs bash 4) |
| Claude Code | 2.1.272 (`claude plugin validate --strict`, `claude plugin` install, update, enable and disable against a throwaway `CLAUDE_CONFIG_DIR`, the headless runs) |
| Matt Pocock's skills | github.com/mattpocock/skills at commit `3cca18b368ae95cdbdebbff572ccafa662551015` (2026-09-04), every skill at that one commit; installed through skills-manager as symlinks from `~/.claude/skills/<name>` to its store (the installer's own path, skills.sh 1.5.26, lays them out the same way); file hashes below |
| Superpowers alongside | 6.3.0, enabled, from the `claude-plugins-official` marketplace; the four copied skills are byte-identical to its cache (`scripts/tests/test_plugin.sh` checks) |

The nine Matt Pocock skills the plugin invokes with the Skill tool, as installed (SHA-256 of each `SKILL.md`; the hook and the installer check that every one of them exists, not their hashes):

```text
10ff989e7498b23b5acb49d5048f11dcd906757d2f79c5cdf8a00001381296f2  grilling/SKILL.md
327a2b50620e2fd70abc6893cd6965e76b20f8d0adb0dc2c8d5eb3845efb643e  domain-modeling/SKILL.md
cb01f66bebfaa25fa1f88e6b7e769cd9fd9f35b1120b8563749820738814c927  tdd/SKILL.md
77f3cf31bc99b2f49af943222526531fcc9fc41d047626d3640e875e85af3e84  diagnosing-bugs/SKILL.md
47f4e52c21694def9c7c11cbfbf891ca35eac7a93e395797515be3c8a409ae50  code-review/SKILL.md
2c20617f87ec8af6a434859f381b2f061a69b530444e74eb39e78bb016a6d1e2  codebase-design/SKILL.md
2bcd89e97777cdb705914424e39c97d5db524c8eb4eafac8120778a07774f0ec  setup-matt-pocock-skills/SKILL.md
c9819d7f1e3b198064edc1faa3154224ed67395e9f07f5d3cea4b67cf0a11a98  setup-pre-commit/SKILL.md
29acca66ac99d4532e2a6f0370d8125d7cba1e87c9ac66573203c75189d3e6c7  setup-ts-deep-modules/SKILL.md
```

To compare your install: `cd "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills" && shasum -a 256 -c` with the block above on stdin. A differing hash means his skill moved on since this record; the plugin invokes it by name and does not depend on its text. The three skills Seams adapted from his (`to-spec`, `to-tickets`, `implement`) are recorded with their upstream hashes in `plugin/THIRD_PARTY_NOTICES.md`, and `test_plugin.sh` warns when the installed copies differ.

## Declared, not yet observed

`.github/workflows/test.yml` runs `scripts/test.sh` on every push to `main` and on pull requests, on `ubuntu-latest` and `macos-latest` with Node 22 and Python 3.12 (`actions/setup-python`; on the macOS runner the system Python 3.9 suites run as well, since it differs). The `claude` CLI is not installed there, so the static plugin checks are skipped on CI and count only from a machine with the CLI. No run has happened yet: the workflow was added after the last push, and the 3.0.0 push (ticket 10) is the first one. This section becomes an observed row, with the runner images and the counts, once that run is green.

## Not tested

- Windows, in any form (WSL included).
- Linux distributions other than the Ubuntu runner image, Python 3.10, 3.11 and 3.13, Node other than 22, Claude Code versions other than the one above.
- A Matt Pocock skills install made by his official `mattpocock-skills` plugin instead of skills.sh (the README says not to install both).
- The thirteen-scenario outcome matrix the 2026-09-15 review proposed (a greenfield app to a test deployment, a migration, tenant isolation, a failed release, and the rest): not evidenced anywhere in this repository.
