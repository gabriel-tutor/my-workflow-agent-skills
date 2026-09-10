# SDD ledger — plan: docs/superpowers/plans/2026-09-11-mp-sp-combo-skill-and-benchmark.md
Branch: build/combo-skill-and-benchmark (in-place, no worktree: activate.sh symlinks and the claude -p smoke tests need the repo at its real path)
Start: 2026-09-10T16:41:11Z
Task 1: complete (commits 16d26e5..d166c88, review clean; ⚠️ trailer verified by controller via git log; minor: report line counts off by one — no code impact)
Task 2: plan deviation — brief step-3 test used `status | grep -q` which SIGPIPEs under pipefail on bash 3.2; controller-approved fix captures output first (a1d53e1). activate.sh unchanged.
Task 2: minor (deferred): unlink_managed is not transactional across the two managed slots (owned link removed before a later foreign path triggers exit 2) — inherent to the specified algorithm, safety invariant holds
Task 2: complete (commits d166c88..a1d53e1, review clean; trailers verified by controller)
Task 3: minor (deferred): test_skills.sh line 19 `head -5 | grep -q` pipeline (safe: head exits on its own); embedded frontmatter parser splits on first colon (latent; descriptions have none)
Task 3: note — commit trailer attributed to Claude Sonnet 5 (implementer harness override); accepted
Task 3: complete (commits a1d53e1..19b63d5, review clean; ⚠️ RED-before-GREEN accepted from report evidence)
Task 4: minor (deferred): skill-catalog.md has a doubled blank line before "## Installed-version notes" (brief concatenation artefact); cosmetic
Task 4: complete (commits 19b63d5..52e4a46, review clean)
Task 5: note — brief smoke test needs --max-turns 4 (Skill tool consumes a turn); combo skill confirmed discoverable; trailer attributed to Sonnet 5 (accepted)
Task 5: complete (commits 52e4a46..fafcc59, review clean, no findings)
Task 6: minor (deferred): quoted paths with spaces mis-captured by bash_writes; fixture does not cover Write/Read/cp/touch/truncation branches; non-text tool_result renders blank
Task 6: fix round 1/5 dispatched (2 open — sed last-token misfires on compound commands; unguarded json.loads aborts on truncated line) — both plan-authored code, controller-adjudicated as bugs not design choices
Task 6: fix round 1/5 (2 addressed, 0 open; commits b21e809..ccef834)
Task 6: minor (deferred): valid-JSON non-object JSONL line would raise AttributeError (only JSONDecodeError guarded)
Task 6: complete (commits fafcc59..ccef834, review clean after 1 fix round)
Task 7: complete (commits ccef834..7a9207d, review clean, no findings; typescript ^7.0.2 / vitest ^5.0.0 installed)
Task 8: minor (deferred): test_prepare_run.sh lines 48-49 `porcelain | grep -q` under pipefail (35-byte output, harmless); prepare_run.sh not hardened against run-dir=/
Task 8: complete (commits 7a9207d..e69c729, review clean; ⚠️ scenario-3 race reproducibility verified by controller in Task 7 and by test_prepare_run)
Task 9: pre-review fix dispatched — run_hidden_tests recorded name-filtered tests as "skipped", failing hidden_acceptance_all_pass for correct scenario-1 implementations (plan-authored bug, reproduced by controller)
Task 9: fix round 1/5 dispatched (2 Important open — report_not_ready_to_merge default-pass/"non-blocking" flip; tests/-prefix assumption across 6 checks; plus cheap minors 3,4,6,7,8,9,11 folded in)
Task 9: minor (deferred): ordering checks default-pass when the src edit is invisible (cd/heredoc/git apply) and a debug-instrumentation edit to inventory.ts counts as the src edit — documented heuristic, LLM grader reads transcript; diff.patch omits untracked files and shows setup-dirtied hunks (files_changed is authoritative — say so in the grader brief); unused imports in test; read() evaluated twice
Task 9: fix round 1/5 (8 addressed, 0 open; commits f1e9df1..1cf6dc5)
Task 9: minor (deferred): dead `else: raise SystemExit` after the upfront SCENARIOS guard; a few regex alternatives (don't merge, yet, floor) are harmless supersets of the requested wording
Task 9: complete (commits e69c729..1cf6dc5, review clean after 1 pre-review fix + 1 fix round)
Task 10: fix round 1/5 dispatched (2 Important open — finalize_run.sh session discovery SIGPIPE under pipefail; unanchored agent-name glob grabs e1-mp-r2 for e1-mp; plus minors: grader brief files_changed note, empty --configs guard; adds test_finalize_run.sh with BENCH_PROJECT_DIR override)
Task 10: minor (deferred): init_iteration --only "abc" raises raw ValueError; capture_output hides prepare_run diagnostics on failure
Task 10: fix round 1/5 (4 addressed, 0 open; commits 60f9cc9..e9a4f93)
Task 10: minor (deferred): finalize_run.sh for-loops word-split unquoted ls output (names are UUIDs/hashes today); ${candidate%-*} assumes a trailing -<hash>
Task 10: complete (commits 1cf6dc5..e9a4f93, review clean after 1 fix round)
All tasks 1-10 complete. Final whole-branch review next.
Final review (opus): With fixes — 1 Critical (finalize_run.sh transcript naming: real files are agent-a<name>-<hash>.jsonl), 6 Important (viewer eval_metadata location; CLAIMS_GREEN negation; NOT_READY "no blockers"; scenario-1 AC3 ambiguity → ruling: filter ^AC[124]; executor cwd caveat + scaffold commit; usage/steps double-count from split assistant records), minors. Deferred-minor triage: all CAN SHIP except the two folded into #1/#4.
Final fix wave dispatched (opus) with final-fix-brief.md; one scoped re-review to follow.
Final fix wave re-review (opus): all 8 items addressed, no new Critical/Important. Minor (deferred): real-transcript test reads a live file twice without copying (flake only if the alphabetically-first transcript is live); spec §7.4 prompt sketch and the plan doc carry historical wording (cd here first, diff.patch, ^AC[1-4]); CLAIMS_GREEN misses negation-before-subject ("Not everything passes"); PROJ derivation maps only "/"; benchmark/README Tests lists benchmark suites only.
Branch complete: 16 commits 16d26e5..c2a34c6, 4 shell suites + 27 unit tests green.
