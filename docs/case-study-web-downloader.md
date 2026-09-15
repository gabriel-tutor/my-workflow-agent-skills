# Case study: one feature, end to end, on a real repo

What Seams did on a real project, in the order it happened, with the actual artifacts. The project is `web-downloader`, a 6,600-line TypeScript Chrome extension that mirrors a section of a website to disk (Markdown or HTML). Two days old, 26 commits, a `CONTEXT.md` glossary, a spec and 15 tickets already worked through, and a Playwright e2e suite.

Everything below was produced by Claude Code with Seams installed, in interactive sessions, with the user answering the questions. Nothing was staged.

## 1. Foundations: the first hour in a repo

Prompt: `/matt-pocock-workflow:foundations`

The survey read the repo's history, not only its file list. Three examples from its findings:

| Gap | Its reason, verbatim |
| --- | --- |
| Lint and format missing | "6,600 lines of TypeScript, formatted by hand so far; the review agents kept flagging style drift (arrow vs function, naming) that a linter would catch" |
| Pre-commit hooks missing | "every commit so far ran typecheck and tests by hand; a hook makes that automatic, so a hurried commit can't land red" |
| Boundary enforcement missing | "the rule has held through 26 commits because each review checked it by hand; a rule file would check it in seconds" |

It also scaled to the repo: CI was "not applicable yet, no remote", environment was "not applicable, nothing reads env", and the summary read "everything else is in place, which is unusual for a two-day-old repo." It asked which gaps to close, and waited.

The user chose three. What followed, each proven before it was called done:

- **Prettier + oxlint**, tree formatted once (22 files, one commit). typescript-eslint was dropped after it failed on TypeScript 7; oxlint took its place. Four warnings on intentional code were annotated rather than silenced globally.
- **Husky + lint-staged**, running format, lint, typecheck, boundaries and unit tests on commit; the e2e suite was kept out because 28 seconds per commit is too slow. One trap caught: oxlint exits 0 on warnings by default, so a hook using it would never block anything; `--deny-warnings` was added. Proven by staging an unused variable: the hook refused the commit.
- **dependency-cruiser**, with the repo's own layering rule ("dependencies flow downward") written as an ordered `LAYERS` list that generates one rule per layer. The `setup-ts-deep-modules` skill wants a `src/packages/` layout; the repo is one small `src/lib`, so only the dependency-cruiser piece was taken and the layout left alone. Proven with five planted violations, each caught by the intended rule, then a clean pass.

## 2. The grill: seven decisions, one at a time

Prompt: *"Add exact resume: when a Run is stopped or the tab closes, a later Run into the same folder picks up exactly where it left off, including a Page's half-fetched Assets."*

Before its first question the grill read the code and reported two facts: today's skip-existing logic causes both problems the user named, and the crawler's in-memory state (URLs, redirects, asset destinations) cannot be recovered from the saved files. Then seven decisions, each a clickable question with the recommended answer first and a count of what remained:

1. **Where does the resume record live?** Journal file in the Mirror (recommended) · derived from saved files · browser storage. The options came with the reason each loses: derived is lossy ("URLs cannot be recovered from a Markdown Page's assets/"), browser storage "is lost with the profile".
2. **How does resume relate to the existing "Skip files already in the folder" switch?** One switch, reworded, with a fallback for old Mirrors.
3. **What does a Run do into a folder whose Journal says the earlier Run finished?** Re-read the Start URL and sitemaps, skip the rest. (This turned "resume" into cheap incremental updates, which the prompt never asked for.)
4. **On resume, what happens to URLs that failed last time?** Fetch everything not saved again.
5. **A Run's output format differs from the Journal's.** Refuse to start, name the folder's format. (A failure mode the user had not raised; the grill found it in the code.)
6. **What does the run pane show on resume?** Counters continue from the Journal, plus a notice.
7. **Where do the tests go?** Journal unit, crawler seam with the memory sink, two e2e.

Between questions 1 and 2, `domain-modeling` added the new term to the glossary:

> **Journal**: The record a Run keeps inside its Mirror of everything it has admitted: each Page and Asset, where it goes, whether it is saved yet, and which addresses turned out to be the same file. A later Run into the same folder continues from the Journal rather than from what it can see in the folder. *Avoid*: State file, checkpoint, manifest, ledger, cache

After question 7 the grill wrote ADR-0003 (the decision, the two rejected alternatives, the one consequence) and closed with: *"The frontier is empty and the design lens has nothing unsettled."* Its summary included guards nobody had asked for: an unreadable Journal gives a notice, falls back to the file check, and is rewritten fresh; a Journal read from disk is validated as data (shape and safe paths) before use.

The user was asked to confirm the shared understanding and how to build it. The grill's own recommendation: "more than one sitting", so spec and tickets rather than a single implement pass.

## 3. Spec and tickets

`to-spec` produced 41 user stories, the agreed seams, and the four sections the design lens feeds: alternatives considered, risks and failure modes, rollout and migration, observability. It asked before publishing.

`to-tickets` proposed three tracer-bullet tickets, quizzed the user on the breakdown, and published them. Each ticket carries acceptance criteria and a **How to verify** line. Ticket 01, in part:

> **What to build:** Every Run leaves a Journal at `.web-downloader/journal.json` inside its Mirror … written once the sitemap phase ends, then at most every two seconds while something has changed, at once on pause, on Stop once the requests in flight have settled … The journal module also reads a Journal back, and calls anything unreadable by its reason: wrong version, unknown format, a path that is not a safe Mirror-relative name (`..`, `.`, empty segment, forbidden character), a URL that is not http(s), an Asset without a destination, an alias to an unknown URL, or text that is not JSON.
>
> **How to verify:** `pnpm test` (journal and crawler suites), `pnpm lint:boundaries`, `pnpm test:e2e`; or load `dist/` unpacked, run against any site, Stop, and open `.web-downloader/journal.json` in the Mirror folder.

## 4. Implement: ticket 01

Red before green on every slice. The first test failed with `Cannot find module './journal.js'` before the module existed; the crawler test failed with "no Journal was written" before the crawler wrote one. Sixteen ways a Journal file can be unreadable became sixteen table-driven test cases, each asserting the reason string, because the grill had decided a Journal is untrusted input.

The new module was placed in `LAYERS` and `pnpm lint:boundaries` passed: the boundary rule set up an hour earlier was already checking new code.

Then Matt Pocock's two-axis review (Standards and Spec, two subagents in parallel), one fix commit from its findings, and the definition of done with evidence:

| Check | Evidence |
| --- | --- |
| Seam tests pass | `tests/format.test.ts`: 5/5, and the two negative cases proven red without the fix |
| Full suite passes | `pnpm test`: 330/330 |
| Typecheck | `tsc --noEmit` exit 0; oxlint clean; boundaries 26 modules clean |
| No debug leftovers | no `.only`, `console.log`, `debugger` or `TODO` in src or e2e |
| Commit | `7c48301` (feat) + `8514b4e` (fix after review), both hook-verified |

## 5. The handover

The closing message, abridged:

> **Run it**
> `pnpm check` (typecheck, lint, boundaries, format, 330 unit tests) · `pnpm test:e2e` (38 Playwright tests incl. e2e/journal.spec.ts) · `pnpm build` then load dist/ unpacked
>
> **Try it**
> · Finished Run's Journal: run against any docs site into a folder, open `<folder>/<scope>/.web-downloader/journal.json`: `"finished": true`, every Page as `[url, path, true]` …
> · Stopped Run: press Stop while URLs are in flight: `"finished": false`, the cut-off items as `[url, path, false]`; the README still lists them under "Not saved".
> · Cadence: re-open the file every few seconds during a long Run: it changes at most every ~2 s, at once on Pause.
> · Unreadable Journal: edit the file so a path contains `..` or the version is 2: `readJournal` names the fault. Nothing in the app reacts to it yet; that is ticket 02.

That last line is the point of the handover: what this ticket delivers, and what it doesn't, so the user doesn't go looking for behaviour that lands next ticket.

## What this shows

- The design lens surfaced four things the user did not ask about: the format collision, the corrupt-journal fallback, the untrusted-input validation, and the migration path for Mirrors written before Journals existed. All four were decided before any code existed.
- The glossary and ADR were written *during* the design, so the spec, tickets and code all use one word, "Journal", with one meaning.
- Foundations work compounds immediately: the boundary rule and the pre-commit hook set up in step 1 checked the feature code in step 4.
- Every "done" claim came with the command that proves it, and the handover told the user what to run, what to try, and what to expect.

Two defects in the plugin were found by this run and fixed in 2.1.1: a wrong skill-name prefix on the first `code-review` attempt, and a handover that dropped its "Next" section. The evidence for those is in [`plugin-behavior-tests.md`](plugin-behavior-tests.md).
