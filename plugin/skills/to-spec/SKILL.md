---
name: to-spec
description: Use when a grilled design is agreed and the build will span more than one session
---

# To spec

This skill runs Matt Pocock's `to-spec`, which only the user can invoke directly.

1. **Gate.** Before reading anything, ask "Write the spec now?" with AskUserQuestion, recommended answer first, and wait for a yes. Skip this only when the user's last message asks for a spec, or says yes to an offer to write one. A general go-ahead such as "let's get going" or "next" is not a request for a spec.
2. **Load it.** Read Matt Pocock's `to-spec/SKILL.md` from the directory the session bootstrap names. If the bootstrap says his skills were not found, or the file is missing, tell the user Matt Pocock's skills aren't installed, and stop.
3. **Follow it exactly,** with three additions:
   - When it says to check the test seams with the user, and the grill already agreed them, write those seams into the spec instead of asking again.
   - Under **Further Notes**, add four short subsections, each from what the grill settled (write "none" where nothing applies, and never invent):
     - **Alternatives considered:** the designs rejected and the one-line reason for each. A decision that is hard to reverse also gets an ADR through `domain-modeling`; the spec links it rather than repeating it.
     - **Risks and failure modes:** what can go wrong in use, and what the design does about each.
     - **Rollout and migration:** what changes shape (data, config, a public interface), how it's rolled out (expand–contract, a flag, a cutover), and how it's reversed.
     - **Observability:** how a person will know it's broken in use, and what gets logged at the boundaries.
   - Before it publishes to the issue tracker, show the user the spec's title and where it will go, and wait for a yes.
4. **Next.** Offer `matt-pocock-workflow:to-tickets` and wait for a yes.
