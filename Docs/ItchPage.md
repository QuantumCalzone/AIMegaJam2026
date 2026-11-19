# itch.io page draft

The text for the game's itch.io page: T21's step 3 in [Plan.md](Plan.md), used for the submission. It was drafted on 2026-11-14, before T19 to T22 were done. The jam's submission drafts were in `Docs/Submission.md` until 2026-11-17; git history has them (`git show 465cf9f:Docs/Submission.md`).

- **Markers:** **[T19]** (robots act out their actions), **[T20]** (audio), **[T22]** (the packaged build) and **[T24]** (timers, if done) mark text those tasks may change. **[YOU]** marks a blank only you can fill in. Settle every marker, then delete the markers before you paste.
- Each AI player goes by its provider here, as in the game: OpenAI, Anthropic, SpaceXAI and Meta. The jam page spelled that provider "SpaceXSI". If the game's name for it changes (`name` in `Content/NHOS/Data/personas.json`), change it here too.
- Everything between the two rules under "Page text" goes into the page's description. The sections before it are the page's settings.

## Page settings

| Field | Value |
|---|---|
| Title | No Humans On Set |
| Short description or tagline | One of the five robots in tonight's all-AI improv show is a human in disguise. It's you. |
| Classification | Games |
| Kind of project | Downloadable |
| Release status | Prototype |
| Pricing | No payments (free). Change it if you want donations on. |
| Uploads | `no-humans-on-set-windows.zip`, from butler's channel `windows`, marked Windows: each push that changes the game replaces it (T89; see "Deploys to itch.io" in `Docs/Builds.md`). A Mac file, channel `mac`, comes when the Mac is a runner. Since 2026-11-17 the page holds no jam zip (`QuantumCalzone_NoHumansOnSet_Windows.zip`); never replace one that goes up through the web form. |
| Genre | Other |
| Tags | social-deduction, ai, llm, improv, comedy, robots, text-based, unreal-engine |
| Cover image | 630 × 500, a crop of the theater mid-scene |
| Screenshots | The theater mid-scene, Scene Prep, Free Talk, the reveal stamp, the end screen, and the title screen with the three ways to play |
| Gameplay video | The gameplay video made for the jam |

**AI generation disclosure.** itch.io asks whether a project has content made with generative AI. Suggested answers (match them to the wording on the edit page, and confirm them: open question 11):

- **Yes, it does.**
- **Text and dialogue:** yes. Four LLMs write the AI actors' lines live during every show. The prompts, scene cards and director's notes were written with Claude.
- **Code:** yes. Claude agents built the Blueprints through Unreal MCP.
- **Graphics:** yes. The costume headpieces, the story props and the opera-house set pieces are 3D models we made with Meshy (image to 3D) from reference images we made with Leonardo.ai. Claude agents built the theater, the robots and the backdrops in the editor from the engine's basic shapes.
- **Sound:** no **[T20: confirm once the audio is in]**.

---

## Page text

### Tonight: the world's first all-AI improv show

Five robots take the stage. Four of them are AIs, each running on a different lab's model: **OpenAI**, **Anthropic**, **SpaceXAI** and **Meta**. The fifth is a human in a robot costume. That's you.

The AIs know one of the cast isn't one of their own. After every scene, they vote one actor off the show. Improvise, blend in and cast suspicion on someone else. Make it to the final two, or to the end of the last scene, and humanity wins the stage.

On stage, everyone goes by a Player number, so a name can't give you away. Only your screen shows which lab runs each robot.

### Director's Cut

Every scene comes with a secret note from the director, which only the AIs get, and every scene ends with a cut: the cast votes, and one actor leaves the show. When the vote ties, nobody is cut, but the scene still counts. The reveal stamp says who it really was: an AI, or the human.

We built it the same way. A small crew of Claude agents did the work, directed by us: they wrote the Blueprints, built the stage and tested every prompt on four labs' models. The dev log has every cut we made: [YOU: dev log link].

### How a show works

1. **Scene Prep.** Everyone gets the same scene card: a comedy take on a famous story, like Romeo and Juliet, the Sword in the Stone, or a Sherlock Holmes mystery about a stolen rubber chicken. You get a role and a want. The AIs also get a secret director's note, such as "climb onto the Riser at least once". You don't, and they know it: your card shows only a clue to it, the note's category in scene 1, then a new kind of clue each scene, such as only its vowels or a riddle from the director.
2. **The Scene.** Three turns. Every actor picks what to do and say, and then all the turns play out at once **[T19: and the robots act them out on stage]**.
3. **Free Talk.** Two rounds around the table, one line each, in a new order every round. This is where the accusations fly. You can pass.
4. **The Cut.** Everyone votes for who they think is human and gives a one-line reason. The most votes is cut, and the stamp reveals the truth. Then each actor reacts, and how you react is evidence too.
5. Repeat until two actors are left or the last scene ends. A cast of five has four scenes, a cast of four has three.

You win if you make the final two, or if you're still on stage when the last scene ends. If you're cut, you lose, and the AIs gloat. Either way, the end screen shows how each AI voted and why.

**How to fool them:** play your role and chase your want. On turn 1 you act blind, with only the note's clue to go on. Then watch what the AIs do and work out the note, but copy too late and they'll notice. Don't stand still for a whole scene. Watch what the AIs accuse each other of, because they're looking for the same things in you. A tied vote cuts nobody and uses up a scene, so a split vote helps you.

### Controls

Mouse and keyboard.

- **Type** in the box at the bottom of the screen, and press **Enter** (or click **Send**).
- **Your scene turn:** say what your robot does and says, in your own words. For example: `walk to Left and say "Hi, @Meta!"`
  - You can **move** to a place, **look** at someone or something, **grab** a prop, **throw** a prop at someone, or **give** a prop to someone.
  - Places: Center, Left, Right, Front, Back, Riser and Prop Table.
  - Props: a cardboard sword, a paper crown, a plastic rose, a toy ray gun, a teacup, a cape, a rubber chicken and a scroll.
  - Words in quotes are what you say. Every line is capped at 15 words.
- **Speak to one actor** with @ and the name on your screen: `@Meta, why did you grab the rose?`
- **Free Talk and reactions:** type a line, or click **Pass**.
- **The Cut:** click a name on the vote row, then type your reason and send it. You can't vote for yourself.
- **After the show:** click **See the results**, then **Play Again** or **Quit**.
- When it isn't your turn, the input box says who the game is waiting for. There are no timers, so take your time **[T24: unless timers go in]**.

### Three ways to play

Pick one on the title screen.

| | Test for Free | Play | Play with my own API keys |
|---|---|---|---|
| What you need | Nothing | An internet connection | API keys for at least 3 of the 4 labs |
| What it costs you | Nothing | Nothing (we pay) | About $0.11 a show, on your own accounts |
| Who plays the AIs | Pre-written lines | The four real AIs | The real AIs, on your keys |

#### Test for Free

No keys, and no internet needed. The AIs answer with pre-written lines and vote at random, so they don't really read what you type and can't really catch you. Use it to learn the controls and see how a show runs. For the real game, pick one of the other two.

#### Play

The real game, with nothing to set up. Your game talks to our relay, a small server that holds our API keys and passes each request on to the four labs. Your keys aren't needed, and the calls are on us.

- A show is about 90 AI calls. To keep the bill sane, the relay has daily limits: up to 150 calls per show, 600 calls per player per day (about 6 shows), and 5,000 calls a day for all players together. The limits reset at midnight UTC.
- **Play** works when at least 3 of the 4 AIs answer and today's budget isn't used up. The title checks the relay when it opens and every minute after. Until the first answer, Play is greyed out with "Checking the AI actors...". If too few AIs answer, the budget is used up or the relay doesn't answer, Play stays greyed out with a short line on why, and **Test for Free** or **Play with my own API keys** still work.
- When you click **Play**, the game checks once more. If the answer changed since the last check, an **AI service unavailable** screen says why and offers **Use my own API keys**, **Test for Free** or **Back to title**.
- If the relay goes down or hits a limit in the middle of a show, the show stops and the same screen shows the relay's message. Picking another way to play starts a new show.
- We keep the relay running while our budget lasts **[YOU: say until when. Each show via the relay costs us about $0.11; the limits are in `Relay/README.md`]**.

#### Play with my own API keys

The real game, on your own accounts. Click **Play with my own API keys** and paste a key for each lab you have. The game calls each lab directly with your keys. They never go to our relay or to us.

- **You need keys for at least 3 of the 4 labs:**

  | Lab | Model the game calls | Where to get a key |
  |---|---|---|
  | Anthropic | `claude-haiku-5-5` | platform.claude.com |
  | OpenAI | `gpt-6-luna` | platform.openai.com |
  | SpaceXAI | `grok-4.3` | console.x.ai |
  | Meta | `muse-ember-1.0` | dev.meta.ai |

- With all 4 keys, the cast is four AIs and you, over up to four scenes. With 3 keys, the lab without a key sits out, and the show has three AIs and you, over up to three scenes. With fewer than 3, the game names the missing keys. Every robot's label is always true: no AI ever runs on another lab's key.
- The helper that turns your typing into stage actions runs on Anthropic. Without an Anthropic key, it uses the first lab you have a key for.
- **Cost:** about $0.11 for a full show with all four labs, most of it (about $0.08) for SpaceXAI, whose model costs more per call. Set a spending limit at each lab's console to be safe.
- **Where your keys go:** **Save and Play** writes them to `Local/llm_key.json` inside the game's folder **[T22: check the path in the packaged build]**, as plain text, so they're filled in next time. Delete that file to remove them. Don't share the game folder with your keys in it.
- **Save and Play** first sends one short test call to each lab you gave a key for, and starts the show only if every key works. If one doesn't, the screen names the lab, and you can fix the key and try again. **Test keys** runs the same check without starting a show. The test costs a fraction of a cent.

### What gets sent where

- **Test for Free** makes no AI call. It sends only the play stats below.
- **Play** sends the game's prompts, the scene, the chat log and your typed lines to our relay, which passes them on to the four labs. The relay doesn't store your lines. To count calls for the daily limits, it keeps your address only as a hash salted with the day. Each lab's own data policy applies to what it receives.
- **Play with my own API keys** sends the same requests straight to each lab, under your own account and that lab's policy.
- The AI actors never see your keys, your raw typing (only the line the helper made from it) or which robot is you.
- **Play stats.** Every way to play sends our relay a few anonymous events: a random player id the game makes on your first launch (nothing from your Epic account, your computer or your keys), which way you play, how far each show gets, how many AI calls went to each lab with their token counts, the kind of any error, and a few words naming an action you tried that the game can't do yet (never your typed line). Never your typed lines, your keys or your address (the relay keeps only a hash of it, salted with the day, as it does for the call limits). Turn them off on the title screen with **Play stats**.

### Install and run (Windows) [T22]

1. Download the zip and unzip it anywhere.
2. Run `AIMegaJam2026.exe` **[T22: check the name]**.
3. Windows may warn that the app isn't recognized, because it isn't signed. Click **More info**, then **Run anyway** **[T22: check]**.

Needs Windows 10 or 11 (64-bit) and a DirectX 12 graphics card. The game uses Unreal Engine 5's Lumen lighting. Download size: **[T22]**.

### Known limits

- Replies take a second or two, and each turn waits for every actor's reply.
- The AIs are LLMs. Now and then one says something odd, repeats itself or misreads the scene. That is part of the show, mostly.
- With your own keys, if a lab fails in the middle of a show (for example, your account runs out of credit), that robot just looks around for that turn. The game doesn't stop for it.
- A show the relay stopped can't be picked up again: picking another way to play starts a new show.
- **[T19, T20: list whatever these tasks leave undone, or delete this line.]**

### Credits

Made by **[YOU: team name and members]** for the 2026 Epic AI MegaJam, in Unreal Engine 5.8, Blueprint only.

- **AI actors:** Anthropic's Claude Haiku 5.5, OpenAI's gpt-6-luna, SpaceXAI's grok-4.3 and Meta's muse-ember-1.0.
- **Built with** Claude Code (Claude Opus 5.5, Claude Fable 5.2 and Claude Sonnet 5.5) driving the Unreal Editor through Unreal MCP.
- **Font:** Roboto by Google and Droid Sans Fallback, shipped with Unreal Engine (Apache License 2.0).
- **Art:** made in the editor from the engine's basic shapes, with no outside or generated art.
- **Audio** (from `Docs/Assets.md`, T102):
  - Music and most sound effects generated with Stable Audio by Stability AI, from prompts written with Claude, picked by the team.
  - "Applause-2" by RHumphries, CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/), via Wikimedia Commons: https://commons.wikimedia.org/wiki/File:Applause-2.ogg
  - "approx 800 laughter only 1" by lonemonk, CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/), via Wikimedia Commons: https://commons.wikimedia.org/wiki/File:72843_lonemonk_approx-800-laughter-only-1.wav
  - Throw swish by artisticdude, click by StarNinjas (CC0, via OpenGameArt).
  - The robots' gibberish voices are made by our own script; the human's is the team's own recording.
- **Made before the jam:** only the project and repo setup (the Unreal project from Epic's Blank Blueprint template, its config, the git setup and the agents' instruction files), on Nov 10 and 11. No game content. **[YOU: add anything from open question 6 in `Submission.md`]**
- **Dev log:** [YOU: dev log link]

The scenes send up famous stories. Public-domain stories stay close to the original; modern films are parodied with new names and no quotes.

---
