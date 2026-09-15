---
name: implement
description: Use when an agreed design, spec or ticket is ready to build
---

# Implement

This skill runs Matt Pocock's `implement`, which only the user can invoke directly.

1. **Gate.** Before reading anything, confirm which spec, ticket or agreed design you're building, and where. Offer a worktree through `matt-pocock-workflow:using-git-worktrees`, which asks for consent, or the current branch. Wait for a yes. Skip this only when the user's last message already names both.
2. **Load it.** Read Matt Pocock's `implement/SKILL.md` from the directory the session bootstrap names. If the bootstrap says his skills were not found, or the file is missing, tell the user Matt Pocock's skills aren't installed, and stop.
3. **Follow it exactly,** with one addition. When it runs `code-review`, pass the merge-base of this branch and its base branch (`git merge-base <base> HEAD`) as the fixed point. `code-review` reads `docs/agents/issue-tracker.md`; if the repo has none, offer `matt-pocock-workflow:foundations` before the review.
4. **Definition of done.** Before claiming the work is done, run `matt-pocock-workflow:verification-before-completion` and confirm each of these, with the command output as evidence:
   - The tests at the agreed seams pass, and the full suite passes.
   - Typecheck passes, and lint passes if the repo has one.
   - Every acceptance criterion on the ticket or spec is met, checked one by one.
   - No debug leftovers: tagged logs, commented-out code, throwaway scripts, `.only` on a test.
   - Docs are updated where behavior changed: the README's run or usage lines, the glossary if a term moved.
   - The commit message says what changed and why, and names the ticket.
   Anything unmet is not done: fix it, or say plainly that it's unmet and why.
5. **Handover.** Your closing message is the handover. It has exactly four sections under these four headings, in this order, and it is not finished until the fourth is written:
   1. **Run it.** The exact commands to start and to check the work, taken from the repo's real scripts or README. If the repo has no run or verify command, give the one-line command that works and offer to add it to the README.
   2. **Try it.** One short walkthrough per acceptance criterion, in the user's words: what to do, and what they should see. Refer to things by their glossary names.
   3. **What changed.** The files and public interfaces touched, in a few lines, and any decision you made that the ticket didn't settle.
   4. **Next.** Name the next unblocked ticket, or say there is none. Then say one of two things: `/clear` before it, because it is unrelated to this one or this session is already heavy; or continue in this session, because it builds on this one. If the work is on a branch, also offer `matt-pocock-workflow:finishing-a-development-branch`. A handover that stops at "What changed" is incomplete.
