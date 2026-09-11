---
name: implement
description: Use when an agreed design, spec or ticket is ready to build
---

# Implement

This skill runs Matt Pocock's `implement`, which only the user can invoke directly.

1. **Gate.** Before reading anything, confirm which spec, ticket or agreed design you're building, and where. Offer a worktree through `matt-pocock-workflow:using-git-worktrees`, which asks for consent, or the current branch. Wait for a yes. Skip this only when the user's last message already names both.
2. **Load it.** Read Matt Pocock's `implement/SKILL.md` from the directory the session bootstrap names. If the bootstrap says his skills were not found, or the file is missing, tell the user Matt Pocock's skills aren't installed, and stop.
3. **Follow it exactly,** with one addition. When it runs `code-review`, pass the merge-base of this branch and its base branch (`git merge-base <base> HEAD`) as the fixed point. `code-review` reads `docs/agents/issue-tracker.md`; if the repo has none, suggest `/setup-matt-pocock-skills` before the review.
4. **Finish.** Run `matt-pocock-workflow:verification-before-completion` before claiming the work is done. If the work is on a branch, offer `matt-pocock-workflow:finishing-a-development-branch`.
