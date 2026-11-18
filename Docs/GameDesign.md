# No Humans On Set: game design

The game design document lives in [Docs/Design/](Design/), one Markdown file per part, and those files are the design's only source of truth.

1. [Overview](Design/Overview.md): the premise and how a show works.
2. [Rules](Design/Rules.md): everything in one show, from casting to the last cut.
3. [Turn Input](Design/TurnInput.md): how you click to build an action and type a line on each scene turn.
4. [Tech & Build](Design/TechAndBuild.md): game state, AI access and the build list.
5. [Bot Prompts](Design/BotPrompts.md): the shared base prompt and the persona prompts. `Content/NHOS/Data/prompts.json` and `personas.json` copy them word for word, because the game reads them at run time.
6. [Art Inspiration](Design/ArtInspiration.md): the art direction (style, the bots, costumes, the stage, the UI) and the mood images.
7. [Stories](Design/Stories.md): the seven film parodies, each with its roles, wants, headpieces, props and backdrop.

**To change the design,** edit its file in the commit of the task that changes it, after QuantumCalzone's OK. A prompt changes in `BotPrompts.md` first, then word for word in `prompts.json` or `personas.json`. What is built so far, and what is still to do, is in [Plan.md](Plan.md).

These files were copied word for word from the old Claude Doc "No Humans On Set — concise draft (suggested edits)" on 2026-11-17 (task T90).
