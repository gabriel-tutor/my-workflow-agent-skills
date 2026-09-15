# Seams

A Claude Code plugin (`plugin/`) that makes Matt Pocock's engineering skills lead every session. Run `scripts/test.sh` before claiming anything passes.

## Agent skills

### Issue tracker

Issues and specs are local markdown under `.scratch/<feature>/` (spec.md, issues/NN-slug.md). See `docs/agents/issue-tracker.md`.

### Triage labels

The five default labels, each string equal to its role name. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the root. See `docs/agents/domain.md`.
