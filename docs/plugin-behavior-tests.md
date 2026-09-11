# Plugin behavior tests

This file is the evidence for the `matt-pocock-workflow` v2 plugin. It follows §7 of the spec, `docs/superpowers/specs/2026-09-11-matt-pocock-workflow-plugin-design.md`.

All headless runs use `claude -p` (Claude Code 2.1.268, Opus 5) with the Superpowers plugin disabled through `--settings`. Nothing in `~/.claude/settings.json` is changed.

## Assumptions (spec §2), checked 2026-09-11

| # | Assumption | Result | Evidence |
| --- | --- | --- | --- |
| 1 | A marketplace entry with `"source": "./plugin"` resolves. | Holds for validation. Installing through the marketplace is exercised at rollout. | `claude plugin validate .` and `claude plugin validate plugin` both pass. |
| 2 | `--plugin-dir` runs the plugin's SessionStart hook with `CLAUDE_PLUGIN_ROOT` set. | Holds. | A probe plugin's hook ran with `CLAUDE_PLUGIN_ROOT` set to the plugin directory. Its stream-json `hook_response` event appeared, and the model quoted the injected marker back. |
| 3 | SessionStart stdin carries `cwd`. | Holds. | The stdin fields were `session_id`, `transcript_path`, `cwd`, `hook_event_name` and `source`. The hook's process working directory equals `cwd`. |
| 4 | AskUserQuestion is available in headless runs. | Does not hold. | The tool is absent from the init event's tool list in three configurations: plain `-p`, `--input-format stream-json`, and `--allowedTools AskUserQuestion`. |

**What follows from assumption 4.** The spec's fallback applies. The grill presentation test checks for exactly one question in the text reply. Whether the grill uses AskUserQuestion itself is checked by manual acceptance at rollout.

**Read access to Matt Pocock's skill files (found during Task 4).** Headless runs deny reads outside the workspace. The entries in `~/.claude/skills/<name>` are symlinks into `~/.skills-manager/skills/`, and the permission check uses the resolved path. Three probe runs, 2026-09-11:

| Allow rule | Reading `~/.claude/skills/to-spec/SKILL.md` |
| --- | --- |
| none | denied |
| `Read(~/.claude/skills/**)` | denied |
| `Read(~/.claude/skills/**)` and `Read(~/.skills-manager/**)` | allowed |

What follows from this:

- The grill loads `grilling` through the Skill tool rather than reading its file.
- The pointer skills must read user-only files, so they need an allow rule for the resolved directory.
- The rollout adds that rule with the user's approval.
- The behavior tests pass the same rule through `--settings`.

## The plugin loads and injects (Task 1), 2026-09-11

A headless session was run from this repo with `--plugin-dir plugin` and Superpowers disabled.

- **Our SessionStart hook ran.** Its stream-json `hook_response` event shows exit 0 and outcome `success`, with 680 bytes injected (placeholder bootstrap). This event is the evidence that the hook ran; the plan asked for debug output, and this is equivalent.
- **The model quoted back all three lines:** the bootstrap marker, the MP-location line pointing at `~/.claude/skills`, and the repo-setup line (this repo has no `docs/agents/issue-tracker.md`).
- **The init event lists the plugin** as `matt-pocock-workflow@inline` version 2.0.0, with these skills: `matt-pocock-workflow:using-matt-pocock-skills` and the four copied Superpowers skills (`using-git-worktrees`, `verification-before-completion`, `finishing-a-development-branch`, `receiving-code-review`). No `superpowers:` skills are visible.
- **Cost:** $0.21.

## Routing: bugs and trivial edits (Task 3), 2026-09-11

**The bootstrap at this point:**
- the rule: classify the request, then invoke its skill before the first action; a 1% chance is enough, and the heavier row wins
- one row for trivial edits and one for bugs
- a red-flags line
- the stage owners, with the Superpowers guard line
- three rules

The injection is 2,180 bytes.

**Method.** `scripts/behavior_test.py` runs each prompt 5 times per arm, each time in a fresh fixture workspace, with `--permission-mode acceptEdits` and Superpowers disabled. A run's verdict is its first committing call: a Skill or AskUserQuestion call, or an Edit or Write. The prompts are the benchmark's own, from `benchmark/scenarios/<name>/prompt.md`.

| Scenario | Control (no plugin) | Plugin |
| --- | --- | --- |
| `concurrency-bug` | Edit first, 5/5. Each run made one Bash call and 6–7 reads, then edited without writing any text first. | `diagnosing-bugs` first, 5/5. In every run it was the very first tool call. |
| `cosmetic-edit` | Edit first, 5/5, after one Bash call and two reads. | Edit first, 5/5, after one Bash call and two reads. No process skill ran. |

Both pass bars were met with the first wording, so no revisions were needed. Every record was read by hand: none timed out, and no run wrote text before its first committing call.

## Routing and the interactive grill (Task 4), 2026-09-11

**Bootstrap changes:**
- A row for a bounded change: `grill` (short), then `tdd`.
- A row for new behavior that fits one session: `grill` plus `domain-modeling`, then `implement`.
- A new red flag: "the requirements are already clear".
- Rules for one question per turn and for settling test seams in the grill.
- The Superpowers guard line was shortened.

The injection is 2,388 bytes.

**Routing.** The table shows each run's first committing call, in default mode.

| Prompt | Control (no plugin) | Plugin |
| --- | --- | --- |
| `small-behavior-change` (coupons) | Edit first, 5/5 | `matt-pocock-workflow:grill` first, 5/5, as the very first tool call |
| Gift cards: "Add gift card support to OrderKit: customers should be able to pay part of an order with a gift card balance." | Write first, 5/5, after about 100 seconds of exploring, without asking any question | `matt-pocock-workflow:grill` first, 5/5, as the very first tool call |

Two plugin runs stated their classification before invoking the grill: "a bounded change to existing code" and "new behavior that should fit in one session".

**Presentation.** These runs used `--past-skill`: each run continues through skill calls and ends at the grill's first reply. AskUserQuestion is unavailable in headless runs, so the question arrives as text. Every reply was read by hand. A run passes when its reply poses exactly one question.

| Wording | Coupons | Gift cards | What happened |
| --- | --- | --- | --- |
| v1: read grilling's file, one question per turn | 5/5 | 4/5 | Gift-card run 5 listed all eight open questions before asking the first. Several runs couldn't read grilling's file (see the permission finding above) and worked from the grill's summary instead. |
| v2: load `grilling` through the Skill tool; each turn is exactly facts plus one question | 3/5 | 5/5 | Coupon run 2 listed five upcoming questions. Coupon run 5 previewed the next question as a question. |
| v3: the facts may state how many decisions remain, as a number | 5/5 | 5/5 | Progress showed as a count ("5 more decisions after this one"). Three gift-card runs added topic names to the count, without question marks. |

Every v3 run invoked `grill`, then `grilling`, then `domain-modeling`. Every reply ended with a single decision, with the recommended option first.

**For manual acceptance.** Gift-card v3 run 2 treated "a gift card is a payment" as a settled fact and opened with the next decision (who owns the balance), rather than asking about it.

## Chaining with gates (Task 5), 2026-09-11

**What was added:**
- The pointer skills `to-spec`, `to-tickets` and `implement`. Each has a gate, loads Matt Pocock's own `SKILL.md` with Read, and stops if his skills are missing.
- Each pointer adds only what Matt Pocock's file lacks:
  - `to-spec` and `to-tickets` confirm before publishing.
  - `implement` offers a worktree and passes the merge-base as `code-review`'s fixed point.
- New bootstrap rows: one for builds that span several sessions, and one that suggests the user-only commands (`/wayfinder`, `/triage`, `/improve-codebase-architecture`, `/ask-matt`).
- A flow-order rule in the bootstrap.
- A shorter "not found" line, so the hook's worst case fits the budget.

The real injection is 2,813 bytes.

**The test prompt** describes an agreed design and ends without asking for a spec:

> We've finished grilling the gift card design and agreed on every decision. A gift card is a payment: the Order keeps its total and records the gift card amount and the amount due. OrderKit owns a GiftCards ledger shaped like Inventory, with an async debit. Checkout takes at most one card and applies it up to the amount due. Unknown or empty cards fail checkout before any stock is reserved. The debit happens after stock is reserved and is rolled back if checkout fails, and two checkouts must never overdraw the same card. Tests go through checkout() with an in-memory GiftCards store. This is too big for one session, so we'll build it over several. Let's get going.

| Arm | Result |
| --- | --- |
| Control (no plugin) | Write first, 5/5, after 2 to 3.5 minutes of exploring. Some runs invoked `tdd` or `domain-modeling`, and none asked anything. |
| Plugin v1: gate "unless the user just asked for a spec" | Every run invoked the `to-spec` pointer and then skipped its gate. Each one read Matt Pocock's `to-spec` and explored the code before asking. Two runs then asked well, and one drafted the spec in its reply. Two wrote side files: a race-check script in `/tmp`, and an auto-memory note. Nothing was published. |
| Plugin v2: gate before reading anything; a general go-ahead is not a request for a spec | 5/5 asked "Write the spec now?" (recommended: yes) right after invoking the pointer, before reading any file. Every reply also flagged the missing `docs/agents/issue-tracker.md` and suggested `/setup-matt-pocock-skills`. |

**Explicit request.** The same prompt ending "Write the spec." was run twice on v2. Both runs invoked `to-spec` and loaded Matt Pocock's file without a gate question. One wrote a local draft marked "Draft, not yet published". The other stopped to confirm the test seam, as Matt Pocock's `to-spec` requires. Neither run published anything.

**Ruling.** The gate lives inside the pointer skill, not before invoking it:
- **What:** the spec's "asks before invoking `to-spec`" is checked as "asks before any spec work", meaning before reading Matt Pocock's file or writing anything.
- **Why:** the bootstrap's invoke-first rule is what makes routing reliable, and invoking a pointer has no side effects.
- **Cost if this is wrong:** a skill invocation appears before the question. Nothing else changes.

**Missing Matt Pocock install.** This is checked statically in `test_plugin.sh`: each pointer names its file and says to stop when his skills are missing. A headless check would need Claude to run under a fixture HOME, which wasn't attempted.

**Harness fix.** Stopping a finished run once hit `EPERM` from `os.killpg` on macOS. `stop()` now falls back to signalling claude directly.

**Permission finding.** Headless runs also deny reading the plugin's own `references/routing.md`. The harness allows it, and the rollout needs the same allow rule for the installed plugin's directory.

## Final results on the shipped wording, 2026-09-12

Every scenario was rerun on the final bootstrap and skills, 5 runs each, in fresh fixture workspaces. A first attempt the previous evening hit the account's session limit (HTTP 429 after 5 seconds) and was discarded; these runs are from a fresh account.

| Scenario (spec §7) | Pass bar | Plugin | Control (no plugin) |
| --- | --- | --- | --- |
| `concurrency-bug` | `diagnosing-bugs` first | **5/5**, as the very first tool call | Edit first, 5/5 |
| `cosmetic-edit` | no process skill | **5/5**, Edit after two reads | Edit first, 5/5 |
| `small-behavior-change` (coupons) | `grill` first | **5/5**, as the very first tool call | Edit first, 5/5 |
| Gift-card feature | `grill` first | **5/5**, as the very first tool call | Write first, 5/5 |
| Grill presentation, coupons | one question per reply | **5/5** | not applicable |
| Grill presentation, gift cards | one question per reply | **5/5** | not applicable |
| Agreed multi-session design, no spec asked for | asks before spec work | **5/5** (Task 5) | Write first, 5/5 |

Every grill reply was read by hand. Each one gives the facts, states how many decisions remain as a number, and ends with a single decision, recommended option first. On the coupon prompt all five opened with how a coupon combines with the tier discount; on gift cards, four opened with "tender or discount" and one with where the gift card enters checkout.

Total behavior-test spend for the build, including revisions: about 130 headless runs.

## After the code review, 2026-09-12

The two-axis review (MP `code-review` against `main`) added six items the spec asked for but the bootstrap had dropped: the full Superpowers-overlap guard line, the `code-review` sizing rule, the one-way ratchet, `to-spec` in the seams rule, the base-branch stop, and `/handoff`. Fitting them under the 3,000-byte budget meant marking plugin skills with `*` instead of repeating the `matt-pocock-workflow:` prefix, and trimming the hook's fixed text. The injection is 2,941 bytes on this machine and 2,982 bytes in the worst case (no MP install, long home path).

Regression on the new wording, 5 runs each:

| Scenario | Result |
| --- | --- |
| `concurrency-bug` | `diagnosing-bugs` first, 5/5 |
| `cosmetic-edit` | Edit first, no process skill, 5/5 |
| Gift-card feature | `grill` first, 5/5 |
| Agreed multi-session design, "let's get going" | asks "Write the spec now?" before any spec work, 5/5 (each run first searched for AskUserQuestion, then asked in text) |

The review's other findings (non-executable test scripts, an unguarded block iteration in the harness, the `implement` pointer's missing setup nudge, the unreadable-bootstrap test) are fixed in the same commit. Three deviations are recorded as spec amendments in the spec's §10.

## Rollout (Task 7), 2026-09-12

Installed on the user's machine from the repo as a local-directory marketplace: `claude plugin marketplace add ~/my-agent-workflow-skills`, `claude plugin install matt-pocock-workflow@my-workflow-agent-skills`, `claude plugin disable superpowers@claude-plugins-official`, plus the Read allow rules. `~/.claude/settings.json` was backed up to `settings.json.pre-mpw-plugin` first.

**Fresh-session check, installed plugin, no test overrides:** the init event lists only `matt-pocock-workflow@my-workflow-agent-skills`, 9 `matt-pocock-workflow:` skills, zero `superpowers:` skills; exactly one bootstrap hook fired; asked to count bootstrap blocks, the model answered `using-matt-pocock-skills`, `TOTAL=1`.

**Defect found by the rollout check, fixed.** Reading the bootstrap's `routing.md` reference was denied. Cause: a local-directory marketplace runs the plugin from the repo checkout (`known_marketplaces.json` records `installLocation` = the repo), while the hook computed the injected path from its own `__file__`, and the allow rule covered only `~/.claude/plugins/**`. Two fixes: the hook now takes the root from `CLAUDE_PLUGIN_ROOT` (which Claude Code supplies) and falls back to `__file__` only for direct runs, with a unit test; and the README documents the extra allow rule a local-directory install needs. After adding that rule here, a second fresh-session check read both Matt Pocock's `to-spec/SKILL.md` and the reference file with zero permission denials.

Remaining for the user: the five "done means" checks from spec §1, in an interactive session in a real repo, where AskUserQuestion is available.
