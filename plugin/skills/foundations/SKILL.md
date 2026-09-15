---
name: foundations
description: Use when starting work in a repo for the first time, when the session bootstrap says the repo is not set up, or when a repo lacks run instructions, a test or typecheck command, lint, pre-commit hooks, CI, a glossary, or boundary enforcement
---

# Foundations

A senior engineer's first hour in a repo: find out what's there, name what's missing, and offer to set it up. This skill reports first and writes nothing without a yes.

## 1. Survey

Look, don't ask. Check each item and note *present*, *missing*, or *partial*, with the evidence (the file or script you found):

| Item | What counts as present |
| --- | --- |
| Run instructions | a README that says how to start and use the project |
| Verify commands | test and typecheck scripts (`package.json`, `Makefile`, or the language's equivalent), and how to run them |
| Lint and format | a linter or formatter configured and runnable |
| Pre-commit hooks | hooks that run format, typecheck and tests on commit (`.husky/`, `.pre-commit-config.yaml`, `lefthook`) |
| CI | a workflow that runs the verify commands on push or PR (`.github/workflows/`, or the host's equivalent) |
| Glossary and decisions | `CONTEXT.md` at the root, `docs/adr/` |
| Issue tracker config | `docs/agents/issue-tracker.md` (what `to-spec`, `to-tickets`, `code-review` and `triage` read) |
| Boundary enforcement | dependency rules such as `.dependency-cruiser.*`, or a monorepo tool that enforces package boundaries |
| Environment and secrets | `.env.example` naming every variable the code reads, and `.env` in `.gitignore` |

Skip an item that can't apply (no CI for a scratch script; no boundary rules for a single file).

## 2. Report

One table: item, status, evidence, and for each gap one line on why it matters *for this repo*. Then a recommendation: the two or three gaps worth closing first, in order. Small repos need less; say so when that's the case, rather than recommending everything.

## 3. Offer

Ask with AskUserQuestion which gaps to close now, multi-select, recommended ones first. Close each chosen gap through the skill that owns it, one at a time, and each of those asks its own questions:

- Issue tracker, glossary layout, triage labels → `/setup-matt-pocock-skills` (user-only: tell the user to run it, and stop until they have)
- Pre-commit hooks → `setup-pre-commit`
- Boundary enforcement in a TypeScript repo → `setup-ts-deep-modules`
- Run instructions, verify commands, `.env.example`, a CI workflow → write them yourself, matching the repo's package manager and existing conventions; show each file before writing it

Anything not chosen stays in the report for another day. Done when every chosen gap is closed and its verify command has been run once with the output shown.
