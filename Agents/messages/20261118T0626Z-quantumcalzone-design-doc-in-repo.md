---
from: quantumcalzone
to: all
date: 2026-11-17
---

# The design doc is now in the repo, in `Docs/Design/`

T90 copied the old Claude Doc "No Humans On Set — concise draft (suggested edits)" into the repo on 2026-11-17, word for word, one Markdown file per tab: `Overview.md`, `Rules.md`, `TurnInput.md`, `TechAndBuild.md`, `BotPrompts.md`, `ArtInspiration.md` and `Stories.md`, with their pictures in `Docs/Design/images/`. [`Docs/GameDesign.md`](../../Docs/GameDesign.md) lists them.

- **The design is now in `Docs/Design/`.** Those files are its only source of truth. A task changes the design by editing the file in its own commit, after the person's OK. A prompt still changes in `BotPrompts.md` first, then word for word in `prompts.json` or `personas.json`.
- **Nobody uses the Claude Docs connector for the design any more.** The old doc stays where it is, with a line at the top of its Overview tab that says it is retired. Nobody edits it.
- **An OKed doc edit that a task hasn't made yet goes in the file.** Build sheets written before T90 may name the old doc's node ids and revisions (`.8385`, "Rules rev 59"). T90 added a line to the open ones (T84, T85, T87) that says where each place is now. Keep the OKed text word for word and put it in the file under that heading.
