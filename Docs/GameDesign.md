# No Humans On Set: game design

The design lives in one place: the Claude Doc "No Humans On Set — concise draft (suggested edits)", <https://claude.ai/artifact/XKrsACU5w4kHFwhztXCoTA>. It is the only source of truth, so the repo keeps no copy of it.

- **Access:** the doc is private. Ask QuantumCalzone for access. Agents read and edit it with the Claude Docs connector.
- **Its tabs:**
  - [Overview](https://claude.ai/artifact/XKrsACU5w4kHFwhztXCoTA#c00ebbbe-ecd4): the premise and how a show works.
  - [Rules](https://claude.ai/artifact/XKrsACU5w4kHFwhztXCoTA#64187ff4-d306): everything in one show, from casting to the last cut.
  - [Tech & Build](https://claude.ai/artifact/XKrsACU5w4kHFwhztXCoTA#c0f38ff2-4ae7): game state, AI access and the build list.
  - [Bot Prompts](https://claude.ai/artifact/XKrsACU5w4kHFwhztXCoTA#26333b7d-0cea): the shared base prompt and the persona prompts. `Content/NHOS/Data/prompts.json` and `personas.json` copy them word for word, because the game reads them at run time.
  - [Art Inspiration](https://claude.ai/artifact/XKrsACU5w4kHFwhztXCoTA#0b64f21d-5f0e): the art direction (style, the bots, costumes, the stage, the UI) and the mood images.
- **To change the design,** edit the doc after QuantumCalzone's OK, never a file here. What is built so far, and what is still to do, is in [Plan.md](Plan.md).
