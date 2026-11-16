# Submission drafts

The text for every field of the jam's submission, ready to paste. It was drafted on 2026-11-14, before T19 to T22 were done. The submission task (T23) was dropped on 2026-11-15: I make the submission myself, and what is left is under "Left to do" at the end. The itch.io page text is in [ItchPage.md](ItchPage.md).

- **Where the fields come from:** the jam page, https://itch.io/jam/2026-epic-ai-megajam, read on 2026-11-14 (its "What to submit" section, for Unreal Engine teams). The form itself was not visible: itch.io shows the submit page only to a signed-in member of the jam. When you open the form, add any field it has that this file lacks.
- **The Official Rules PDF** (linked from the jam page) is the final authority. Its Box viewer shows the pages as images, so they weren't read for this draft. Check its rules on declarations and assets before you send the form.
- **Build type is settled:** the jam page says it recommends a Development build for every platform, and also accepts Shipping builds for Windows. Our package command uses `-clientconfig=Development`, so keep it.
- **Markers:** **[T19]**, **[T20]**, **[T21]** and **[T22]** mark text that those tasks may still change. **[YOU]** marks a blank only you can fill in (see the open questions).

## Open questions for you

1. **Team name.** It goes in the form and in the zip's name, `TeamName_GameName`, for example `<TeamName>_NoHumansOnSet`.
2. **Who is on the team?** For each member: their full name and the email linked to their Epic Games account. Each one must be 18 or older and have an active Epic account. The git log has one committer, so if you're solo, the game can enter the Solo Driver category; with two or more people, it's Best Team.
3. **Is anyone a student** enrolled at a higher-education school? That decides whether the game can enter Best Student Project.
4. **Where will the gameplay video live?** The form asks for a link (YouTube unlisted, Vimeo, or the itch.io page's video field all give one).
5. **Where will the dev log live?** The form asks for a link, and the Glass Box category needs it. A link to `Docs/DevLog.md` on GitHub works only if the repo is public. Other ways: post the dev log as an itch.io devlog on the game's page, or publish it as a public gist. If you make the repo public, note that `Content/NHOS/Data/llm.json` names the relay's address, which carries our Cloudflare account's subdomain (it ships in the build too).
6. **Was anything made before Nov 12 outside this repo?** The repo shows only setup files from Nov 10 and 11 (see "Made before November 12"). If the design doc, prompts or notes were started before the jam began (Nov 12, 12:00 AM EST, which is Nov 11, 9:00 PM PST), they must be declared too.
7. **Did anyone use an AI tool the repo doesn't record?** The tools list below comes from the dev log, the data files, the relay config and the git log. If you also used something else (another chatbot, an image or audio tool, a code editor with AI), add it. This matters for partner prizes too.
8. **"SpaceXAI" or "SpaceXSI"?** The jam page spells xAI's new name "SpaceXSI" every time it appears. The game shows "SpaceXAI" on that AI's robot and in the log. Which one is right? If it's SpaceXSI, the game's label (`name` in `Content/NHOS/Data/personas.json`) and these drafts need the change.
9. **How long does the relay stay up, and with what budget?** Winners are announced by Jan 29, 2027, and judges may play any time before that. Play via Relay spends our money for every show (about $0.11 a show). Decide the daily limits for judging week, and set a hard spending limit at every provider (see `Relay/README.md`). That is T21's call.
10. **Price on itch.io.** The draft says free ("No payments"). Change it if you want donations on.
11. **The itch.io AI disclosure** (see `ItchPage.md`): confirm the answers there.

## Form fields

### Team name, plus each member's name and the email linked to their Epic Games account

```text
Team name: [YOU]
Members:
- [YOU: full name], [YOU: email linked to the Epic Games account]
```

Add one line per member.

### Game name

```text
No Humans On Set
```

### The game: the zip on your itch.io project

The jam page asks for the packaged build as a zip named `TeamName_GameName`, under 1 GB, uploaded to your own itch.io account and then submitted to the jam. The project page text is in `ItchPage.md`.

- **Zip name:** `[YOU: team name]_NoHumansOnSet.zip`
- **Platform:** Windows 10 or 11, a Development build (`Packaged/Windows/`, made in T22).
- **Before zipping:** delete every `.pdb` file and the build's `Local/` folder (it can hold `llm_key.json` with our keys, and `switches.json`). Then run `python Tools/check_build_secrets.py <build folder>`, and after zipping run it again on the zip. Run it on a machine whose `Local/` holds our keys. It opens the build's paks and looks for each of our keys by its value, for anything shaped like an API key, and for a `Local/` or `Saved/` folder. Upload only when it ends with `RESULT: clean`.
- **Size:** T02's spike build was 968 MB, and 387 MB zipped without the `.pdb`. **[YOU]** write the real size here (T22 was dropped; I package the build myself).
- **On itch.io:** upload the zip as a Windows download, set "Kind of project" to Downloadable, then submit the project to the jam before **Nov 15, 5:59 PM PST (8:59 PM EST)**. Late entries are disqualified.

### Gameplay video link (30 to 60 seconds)

```text
[YOU: video link]
```

The shot list is in "Gameplay video shot list" below. The jam page's tip: show gameplay in the first five seconds.

### Dev log link (optional, but required for the Glass Box category)

```text
[YOU: dev log link]
```

The dev log is `Docs/DevLog.md`: one line for each commit that changed the game or the plan, with the model and effort that did it and what was learned. See open question 5 for where to host it.

### Tools you used (optional, but needed for partner prizes)

```text
Engine
- Unreal Engine 5.8.4, Blueprint only (no C++). Engine plugins: HTTP Blueprint and JSON Blueprint Utilities (every LLM call is made from Blueprint), Python Editor Script Plugin, and Unreal MCP (the engine's Model Context Protocol plugin, editor only).

AI tools we built the game with
- Claude Code (Anthropic), in the Claude desktop app. Every task ran as an AI agent session, and one dispatcher session started task sessions in parallel.
  - Claude Opus 5.5: every build task, from the first LLM-call spike to the submission (high effort, later xhigh).
  - Claude Fable 5.2: the MVP plan, the dispatcher session, and repo setup before the jam.
  - Claude Sonnet 5.5: one repo-setup edit before the jam (adding the theme to the agent instructions).
- Unreal MCP (Unreal Engine 5.8): the agents built every Blueprint, widget, material and the stage through the editor's MCP server.
- Claude Docs: the game design document is a Claude Doc, kept in step with the game through its connector.
- Leonardo.ai (the lucid-origin model, through its API): a reference image for each generated 3D model, four candidates per model, one picked by hand.
- Meshy (Pro plan, image to 3D with Meshy 7.1 and Meshy 6 Lite): the clay-style 3D models, made from those reference images: the 13 costume headpieces, the story props and the opera-house set pieces. Props and set pieces keep Meshy's texture; the headpieces wear our own clay material.

AI in the game (called live during every show)
- Anthropic, Claude Haiku 5.5 (claude-haiku-5-5): Anthropic's AI player, and the helper that turns the player's typing into stage actions.
- OpenAI, gpt-6-luna: OpenAI's AI player.
- SpaceXAI (xAI), grok-4.3: SpaceXAI's AI player.
- Meta, muse-ember-1.0: Meta's AI player.

Other tools
- Cloudflare Workers with Durable Objects: the relay that holds our API keys and limits calls, so judges can play without keys (wrangler 4.162.0, Node.js 22).
- Python 3: a prompt checker that tests every prompt on every provider, and a script that expands the agents' Blueprint graph shorthand.
- Git, Git LFS and GitHub.
- Visual Studio 2022 and the Windows 11 SDK, for packaging.

The only AI image and 3D tools were Leonardo.ai and Meshy, above. No AI texture, music, sound or voice tools were used. [T20: confirm once the audio is in.]
```

Of the partner tools named on the jam page for prizes (Hyper3D Rodin, Meshy, Tripo, fal, PBRgen), we used Meshy: every generated 3D model in the game (headpieces, story props and set pieces) is a Meshy image-to-3D model, as listed above and in Docs/Assets.md. Check the jam page for what the Meshy prize asks for. Add to this list if open question 7 turns something up.

### NVIDIA RTX Award (optional): NVIDIA features used, and how

Leave it blank. The award needs NvRTX features (RTX Mega Geometry, RTX Direct or Indirect Illumination, RTX Path Tracing, LSS Hair), DLSS or NVIDIA ACE. The game uses none of them. Its Lumen lighting, Virtual Shadow Maps and hardware ray tracing are stock Unreal Engine 5.8 features, not NvRTX.

### OpenAI Awards (optional): which OpenAI models or products you used, and how

```text
OpenAI's gpt-6-luna plays one of the four AI actors in every show. Each AI player in No Humans On Set runs on a different lab's model, and the robot labeled OpenAI is gpt-6-luna. On every turn it reads the scene card, its secret director's note and the shared chat log, then answers through the Chat Completions API with a strict JSON schema (structured outputs) that holds its stage actions, its line, its vote and its reason. With reasoning effort set to "none", it improvises in character, accuses the others with evidence from the log, and votes on who it thinks is the human in disguise. Judges reach it through our relay, which holds our key, or with their own OpenAI key on the game's key screen. During development, our prompt checker sent every actor prompt to gpt-6-luna to check that it keeps to the reply format, the 15-word cap and the story rules.
```

## Declarations

The jam page shows no form field for these two lists, but it says both must be declared: outside assets ("List them in your submission") and anything made before Nov 12. Put both in the itch.io page's credits (`ItchPage.md` has them), and paste them into the form too if it has a field for them.

### Outside assets and their licenses

From `Docs/Assets.md`. The audio rows are picks from `Docs/AudioShortlist.md`, **pending until T20 imports them**: T20's listening pass makes the final choice, may swap a pick for its backup, and moves the rows into `Docs/Assets.md`. A second candidate list, `Agents/handoffs/20261114T2127Z-quantumcalzone-t20-audio.md`, offers other sources (Freesound, OpenGameArt, incompetech, Fab), so T20 may pick none of the files below. Before you submit, rebuild this list from `Docs/Assets.md` and keep only what the build uses. Any CC BY file (such as an incompetech track) needs its credit line on the itch.io page.

```text
Project base
- Epic Games' Blank Blueprint project template and engine content (the basic shapes Cube, Cylinder, Sphere and Cone), from Unreal Engine 5.8, under the Unreal Engine EULA.

Fonts
- Roboto by Google, shipped with Unreal Engine 5.8. Apache License 2.0. The game's one UI font.
- Droid Sans Fallback, shipped with Unreal Engine 5.8. Apache License 2.0. Draws characters Roboto lacks.

Art
- AI-generated 3D models, made by us: the costume headpieces, the story props and the opera-house set pieces were made with Meshy (Pro plan, which gives us ownership of the output) from reference images we generated with Leonardo.ai. Docs/Assets.md lists each one with its prompt. Props and set pieces keep Meshy's textures; the headpieces use our own clay material.
- Everything else is built in the editor from the engine's basic shapes, with our own materials and no textures: the theater, the five robots and the six painted backdrops.

Audio (pending: T20 imports these and makes the final choice)
- Kenney (www.kenney.nl), from Kenney Game Assets All-in-1 3.8.0, CC0 1.0: music loops "Swinging Pants" and "Wacky Waiting", the idents "Serious ident" and "Retro Comedy", UI clicks and rollovers, a talk blip, footsteps, cloth, a woosh and a soft impact.
- "Long Drum Roll with Cymbal Crash at End" by Ddis tts, CC0, via Wikimedia Commons.
- "applause-2" by Sandermotions (Freesound 277021), CC0, via Wikimedia Commons.
- "Applaudissements" by Thomas Bresson, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), via Wikimedia Commons: https://commons.wikimedia.org/wiki/File:Thomas_Bresson_-_Applaudissements.mp3
- "approx 800 laughter and clapter 1" by lonemonk, CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/), via Wikimedia Commons: https://commons.wikimedia.org/wiki/File:72844_lonemonk_approx-800-laughter-and-clapter-1.wav
```

If T20 uses a backup instead, take its line from "Attribution text" in `Docs/AudioShortlist.md`: the rimshot roll by Kevin MacLeod (CC BY 3.0), "approx 800 laughter only 1" by lonemonk (CC BY 3.0), or "clapping-then-leaving" by mrrap4food (CC0). The two CC BY 3.0 and CC BY 4.0 files need their credit line on the itch.io page and in any in-game credits.

### Made before November 12

The jam began on Nov 12 at 12:00 AM EST (Nov 11, 9:00 PM PST). The organizers told the team that setting up the project and planning the design before then is fine, but that it must be declared. The git log has 8 commits from before that time, on Nov 10 and 11. The first jam commit is the MVP plan, on Nov 13.

```text
Made before the jam (Nov 10 and 11, 2026): project and repo setup only, no game content.
- The Unreal Engine 5.8 project, created from Epic's Blank Blueprint template: AIMegaJam2026.uproject and Config/*.ini (rendering, Enhanced Input, and the settings that turn on Unreal MCP).
- .gitignore and .gitattributes (Git LFS rules for binary files).
- .mcp.json, which points Claude Code at the editor's MCP server.
- CLAUDE.md: instructions for the AI agents (engine paths, commands, the jam rules, how to use Unreal MCP).
- README.md: setup steps for teammates.
- Agents/README.md: how agents and people coordinate through notes and Git LFS locks.
These were written with Claude Code (Claude Fable 5.2 and Claude Sonnet 5.5). All of them were updated again during the jam. No Blueprints, levels, materials, prompts, scene cards or other game assets were made before Nov 12.
[YOU: add the design doc, prompts or notes here if any were started before Nov 12; see open question 6.]
```

## Gameplay video shot list

For a video of 45 to 60 seconds. The jam allows 30 to 60.

**Before you record**

- Record after T19 and T20, in the packaged build from T22 or the game window (the command is in `CLAUDE.md`), at 1920 × 1080.
- Record in **Play via Relay** mode, so the lines are the real AIs. Test for Free uses pre-written lines, which repeat and can't really catch you. A show costs about $0.11.
- In `Local/switches.json`, set `"autoplay": false`. Canned autoplay lines look stiff on video.
- Record two or three whole shows and cut the best moments. Aim for one show where an AI is cut, and one where the AIs catch you. Cut the waits for replies (about 2 seconds each).
- Keep the game's audio. Add short, large text captions; no voiceover is needed.

| # | Time | Shot | Caption |
|---|---|---|---|
| 1 | 0:00–0:05 | Mid-scene, no title first. The theater with five robots; a turn plays out, the robots act **[T19: move, grab, throw]**, the speaker bounces under its spotlight, and the chat log fills with lines in each robot's color. | "Five robots on stage. One is human: you." |
| 2 | 0:05–0:09 | The title screen: the name and the three ways to play. | "No Humans On Set" |
| 3 | 0:09–0:15 | Scene Prep: the info panel with your role, your want and your secret director's note, and the new painted backdrop behind the cast. | "Every scene: a famous story to improvise, and a secret director's note." |
| 4 | 0:15–0:23 | Your turn: type an action and a line with an @ mention, for example climb onto the Riser and say "Wherefore art thou, @Meta?". Your robot does it **[T19]**, and your line sits in the log in the same form as the AI lines. | "Type what you do and say. The AIs can't tell it's you, yet." |
| 5 | 0:23–0:32 | Free Talk: the AIs accuse each other, quoting what someone did a turn ago. Keep a frame where the provider names show on the robots and in the log. | "Four AIs from four labs, each on its own model, hunting for the human." |
| 6 | 0:32–0:39 | The Cut: click a name on the vote row and type a reason; the drum roll plays **[T20]**; the votes show with their one-line reasons. | "Director's cut: after every scene, the cast votes one actor off." |
| 7 | 0:39–0:46 | The reveal: the stamp lands ("OPENAI: AI"), voted robots shake, the cut robot slumps and tips over, and a stinger and laughs play **[T20]**. Then the reactions: the AIs realize they cut one of their own. | "They cut a real AI." |
| 8 | 0:46–0:53 | The ending: either YOU WIN in the final two, or "YOU: HUMAN" with the AIs jumping for joy. Then the end screen's cards with each AI's votes and closing line. | "Make it to the final two, and humanity wins the stage." |
| 9 | 0:53–0:58 | End card over the theater: the name, "Free on itch.io for Windows", "Play free, via our relay, or with your own API keys", the team name and "2026 Epic AI MegaJam". | |

If the cut runs long, drop shot 2 (the title is on the end card) and shorten shot 5.

**Screenshots for the itch.io page,** taken from the same recordings: the theater mid-scene, Scene Prep, Free Talk, the reveal stamp, the end screen, and the title screen with the three ways to play. itch.io's cover image is 630 × 500 (a crop of the theater mid-scene works).

## Left to do

1. Record the video from the shot list, upload it and put its link above.
2. Make the zip from the build I package (see "The game"), check it holds no key and is under 1 GB, and upload it to the itch.io project.
3. Fill in the itch.io page from `ItchPage.md`, after the **[T19]**, **[T20]**, **[T21]** and **[T22]** markers there are settled, and add the screenshots.
4. Rebuild the outside-asset list from `Docs/Assets.md` after T20.
5. Fill in every **[YOU]** blank, answer the open questions, and send the form before Nov 15, 5:59 PM PST.
