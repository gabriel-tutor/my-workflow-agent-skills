---
name: to-spec
description: Use when a grilled design is agreed and the build will span more than one session
---

# To spec

This skill runs Matt Pocock's `to-spec`, which only the user can invoke directly.

1. **Gate.** Before reading anything, ask "Write the spec now?" with AskUserQuestion, recommended answer first, and wait for a yes. Skip this only when the user's last message asks for a spec, or says yes to an offer to write one. A general go-ahead such as "let's get going" or "next" is not a request for a spec.
2. **Load it.** Read Matt Pocock's `to-spec/SKILL.md` from the directory the session bootstrap names. If the bootstrap says his skills were not found, or the file is missing, tell the user Matt Pocock's skills aren't installed, and stop.
3. **Follow it exactly,** with one addition. Before it publishes to the issue tracker, show the user the spec's title and where it will go, and wait for a yes.
4. **Next.** Offer `matt-pocock-workflow:to-tickets` and wait for a yes.
