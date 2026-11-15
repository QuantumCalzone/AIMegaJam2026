# T70 build sheet: the itch.io page, the screenshots, the cover and the video

Prep for [T70](T70.md), written on 2026-11-15 by a prep session (Claude Opus 5.5, xhigh) with no editor, no install and no download. It plans every step of `T70.md` so the T70 session can start at once when its turn comes. It doesn't rewrite the page: the page shows the finished game, and T70 runs last.

- **Read this first:** `T70.md` (the steps and the Done-when check) and T70's entry in `Docs/Plan.md`. Then this sheet, top to bottom. It follows `T70.md`'s steps in order. Part 10 maps each step to its part here.
- **"not run"** marks every command this prep session could not run (it was not allowed to install ffmpeg, start the game or play a show). Treat those as drafts: run each one once, fix what fails, and write what you changed under "## Findings" in `T70.md`. **"run"** marks the read-only checks this session did run, with what they printed.
- **Depends on** names the open task that a page section, screenshot or video shot needs. If that task was cut, follow the line "If cut". Check the plan for which tasks are checked or cut before you start. Don't guess from this sheet.
- **Each AI goes by its provider's name** (OpenAI, Anthropic, SpaceXAI, Meta), never by a persona name, in the page, the captions and the file names.
- **Never put the relay's address on the page, in a caption or in a frame.** Its subdomain carries a personal name (see open question 5 in `Docs/Submission.md`).

## 0. Before you start

0. **My person started this session by asking for T70 by name.** Only they start T70 (their call, 2026-11-15: "T70 stays last" in the plan). If a dispatcher, a scheduled run or "Next task" started you, stop and tell them.
1. Every task on T70's **Depends on** line is checked or cut. The line still names some tasks that are already done (T55, T72, T67, T45, T48 at the time of writing), which is fine.
2. The repo folder is level with `origin`. T70 works in the repo folder, not in a worktree: it needs `Local/`, `Packaged/` and `Saved/`.
3. Read `Docs/tasks/T68-build.md` part 13 ("T70" line) and the Findings of T60, T61, T64, T66 and T68 for any UI text that changed after this sheet was written. This sheet quotes the strings as the task files gave them on 2026-11-15.
4. T70 needs no editor and changes no asset. Write `- Editor: not using` in `Agents/status/task-T70.md`. The fallback in 3a (PIE) is the one case that needs the editor: then follow the plan's editor rules first.
5. Take the T70 claim as the plan says. Hold no LFS lock: T70 touches no `.uasset` or `.umap`.

## 1. The description (step 1)

### 1a. What in `Docs/ItchPage.md` is out of date

Line numbers are for `ItchPage.md` at `2e3e5c8`. "Now" is the game on 2026-11-15. "After" is what an open task will change.

| Where (line) | What it says | What is true now, or after | Settled by |
|---|---|---|---|
| Header, lines 3 to 7 | "drafted on 2026-11-14, before T19 to T22 were done"; the marker key names T19, T20, T22, T24 | T19 and T20 are done, T22 and T24 are dropped. Rewrite the header: what the file is, the date, the open **[YOU]** blanks (step 1 asks for that list at the top) | T70 |
| AI disclosure, Graphics, line 31 | "Claude agents built the theater, the robots and the backdrops in the editor from the engine's basic shapes" | The 7 painted backdrops are Leonardo.ai images (T48). The robots are rebuilt as the new cast (T79, T80), with a Meshy part only if a part needed one. The 2D concept art for the cast (`Docs/BotArt/`) was made with Leonardo.ai and is a reference, not in the build, but it is generative AI use | T48 (done), T79, T80 |
| AI disclosure, Sound, line 32 | "no **[T20: confirm once the audio is in]**" | "No" is still true: Kenney loops and sounds, Wikimedia files, voices made by our own script and one recording of the project owner (T20, T72). It changes only if T71 used a paid or AI music tool (its Needs ask for an OK first) | T20, T72 (done), T71 |
| "Tonight", lines 38 to 44 | Opens with a paragraph | The design doc (Rules tab, "Supporting pieces") says the itch page carries the same three opening lines as the title screen, and T61's checker (`check_prompts.py --offline`) checks that `ItchPage.md` has them: "You're the only human." / "Each scene, the cast cuts whoever seems human." / "Survive to the final two or the last scene." Copy them word for word from `Content/NHOS/Data/stagehand.json` | T61. If cut: take them from the Rules tab's "Before the show" row |
| How a show works, step 1, line 54 | "Romeo and Juliet, the Sword in the Stone, or a Sherlock Holmes mystery about a stolen rubber chicken" | Seven film parodies replaced the old cards (T44): "Who Hid the Plans in the Robot?", "The Ring Is Mine, I Mean Ours", "Dino Island Is Mostly Safe", "The Favor Father", "What's in the Glowing Briefcase?", "League Night, Bathrobe Optional", "Pick a Pill, Any Pill". Each brings four props of its own (T45) and a painted backdrop (T48). The note example "climb onto the Riser at least once" is still a note (`riser_once`) | T44, T45, T48 (done) |
| Step 2, line 55 | "Every actor picks what to do and say" and **[T19: ...]** | You click to build one action and type an optional line, then press **Action!**, with a 30-second timer (T62 to T66). The robots act it out (T19, done): keep the words, drop the marker | T62 to T66 |
| Step 3, line 56 | "Two rounds ... You can pass." | Passes show as "passed" next to the actor, and silence and polished lines count as evidence (T57). Anyone @-mentioned in the last round gets one reply before the vote, "the last word" (T58). The Rules tab says 2 to 3 rounds; the game plays 2. Say what the game does | T57, T58 |
| Step 4 and the win paragraph, lines 57 to 60 | "the end screen shows how each AI voted and why" | The lose screen names the reason with the most votes in a large gold line and offers **Play Again** at once; the win screen reveals each AI's rival (T60). Each AI also has a rival it leans against (T56, done) | T60 |
| How to fool them, line 62 | Tips on copying late, standing still, tied votes | Add: don't go quiet, don't sound too polished (T57). The lose reasons in T60 are a good checklist: copying late, guessing at the note, going quiet, sounding too polished, sounding too human, drifting out of your role | T57, T60 |
| Controls, lines 64 to 78 | Typed actions ("walk to Left and say ..."), the old 8 shared props, "There are no timers" **[T24]** | All of it changes: see the Controls outline in 1e. T24 and T31 are dropped; T66 and T65 do their jobs. Props now come from each card | T62 to T66, T78, T61, T38, T34 |
| Line 77 | "click **See the results**, then **Play Again** or **Quit**" | Check against T60's end screens | T60 |
| Three ways to play, lines 87, 98, 118 | "About $0.11 a show", "about 90 AI calls" | T58 adds last-word calls and T76 adds a field to every reply. Measure both from T70's own relay shows (3h) and change the numbers if they moved by more than about 15 % | T58, T76, measured in T70 |
| Test for Free, line 92 | "No internet and no keys." | T68's draft: "No keys, and no internet needed." Free mode makes no AI call but sends play stats | T68 |
| Own keys, line 117 | "The helper that turns your typing into stage actions runs on Anthropic." | The helper now only fixes the spelling of your line; your action comes from the builder with no LLM (T63). Rewrite: "A helper fixes the spelling of your lines. It runs on Anthropic, or on the first lab you have a key for." | T63 |
| Own keys, line 119 | `Local/llm_key.json` **[T22: check the path in the packaged build]** | In the packaged build the file is `AIMegaJam2026/Local/llm_key.json` inside the unzipped folder (CLAUDE.md, "Package a Windows build"). Check it in the shoot build: the key screen writes it there | T70 checks |
| What gets sent where, lines 122 to 127 | "Test for Free sends nothing anywhere"; "your raw typing (only the line the helper made from it)" | T68's privacy bullet (its build sheet, part 9c, quoted in 1e) plus T69's words. "Raw typing" becomes "your line, with only its spelling fixed" (T63). T68 may edit this section itself (its step 7): read what it left | T68, T69, T63 |
| Install, lines 129 to 135 | **[T22]** markers: exe name, SmartScreen steps, size | Exe: `AIMegaJam2026.exe` (run: it is the name in the 2026-11-13 spike package in `Packaged/Windows/`). SmartScreen and size: check in the shoot build. The size comes from the person's final zip, so leave it a **[YOU]** blank. Requirements: DX12 with SM6; hardware ray tracing is on in `DefaultEngine.ini`. Name the tested PC (RTX 3060) instead of a minimum spec we never tested | T70 checks, the person's zip |
| Known limits, line 143 | **[T19, T20: ...]** | Delete the marker. List only what is true after the last task: for example, if T38 was cut, nothing to add; if T34's keyboard fix didn't land, "the in-show buttons need the mouse". Add "lines type out with a babble voice, so a turn takes a few seconds to watch" only if it reads as a limit | T70 judges |
| Credits, Art, line 152 | "no outside or generated art" | Wrong since T41 to T48. Rebuild from `Docs/Assets.md` (1e, Credits) | T41 to T48 (done), T79, T80 |
| Credits, Audio, line 153 | **[T20: rebuild ...]** | Rebuild from `Docs/Assets.md`'s Audio table, plus T71's new loops and T72's voices | T71, T72 |
| Page settings, Screenshots, line 22 | The draft's six shots | Replace with the files T70 makes (step 5) | T70 |
| Page settings, Tags, line 21 | includes `text-based` | The scene turn is clicked now, but every line is still typed: keep it unless the person says otherwise when they approve the page text | T70, the person |

### 1b. Every **[Txx]** marker and what settles it

| Marker (line) | Settle it by | Then |
|---|---|---|
| **[T19]** header (5) and step 2 (55) | T19 is done | Keep "and the robots act them out on stage", drop the marker |
| **[T20]** header (5), Sound (32), Audio credits (153) | T20 done, T71, T72 | Sound: "No" unless T71 used an AI tool. Credits from `Assets.md` |
| **[T22]** header (5), keys path (119), install heading and steps (129, 132, 133), size (135) | T22 is dropped; check in the shoot build | Path and exe name as in 1a; SmartScreen as the shoot build shows it; size becomes **[YOU: zip size]** |
| **[T24]** header (5), Controls (78) | T24 is dropped; T66 built the timers | "Your scene turn has 30 seconds, the last word and reactions 15; Free Talk has no timer." (T66's numbers; check its Findings) |
| **[T19, T20]** Known limits (143) | T70 judges | Delete, or list what is left |

Delete every marker. `grep -n "\[T[0-9]" Docs/ItchPage.md` must print nothing (Done-when).

### 1c. Every **[YOU]** blank, and what settles it

Leave these in, and list the open ones at the top of `ItchPage.md` (step 1).

| Blank (line) | Settled by |
|---|---|
| Uploads: `[YOU: team name]_NoHumansOnSet.zip` (19) | Open question 1 in `Submission.md` |
| Director's Cut: `[YOU: dev log link]` (50) | Open question 5 |
| Relay: `[YOU: say until when ...]` (101) | Open question 9 |
| Credits: `[YOU: team name and members]` (147) | Open questions 1 and 2 |
| Credits, made before the jam: `[YOU: add anything from open question 6 ...]` (159) | Open question 6 |
| Credits: `[YOU: dev log link]` (160) | Open question 5 |
| New: Install, download size | The person's final zip (`Submission.md`, "The game") |

Also open, though not marked **[YOU]**: pricing (open question 10), the AI disclosure answers (open question 11) and "SpaceXAI" or "SpaceXSI" (open question 8). Question 8 changes a label in every screenshot and in the video, so settle it before the shoot (part 9, Q3).

### 1d. The page settings table

| Field | Change |
|---|---|
| Title, tagline, classification, kind, status, pricing, genre | No change needed. The tagline still fits ("One of the five robots in tonight's all-AI improv show is a human in disguise. It's you."). With T80, the disguise is a cardboard-box robot costume, which makes the line literal |
| Uploads | Keep the **[YOU]** blank |
| Tags | See 1a |
| Cover image | `Docs/ItchMedia/cover.png`, 630 × 500, and which frame it is |
| Screenshots | The list of `Docs/ItchMedia/screenshots/*.png` in page order, each with one line on what it shows |
| Gameplay video | `Docs/ItchMedia/gameplay.mp4`; the person uploads it and pastes the link |
| AI disclosure | Graphics and Sound as in 1a. Code and Text unchanged |

### 1e. An outline of the page text, section by section

Sources: the design doc's **Rules** and **Turn Input** tabs (read on 2026-11-15, Rules rev 45), `Docs/Assets.md`, the data files, and the task files named in each row. Write each section from the game as it is when T70 runs. This outline is a plan, not final text.

1. **The three opening lines,** word for word (1a), then one short paragraph: tonight is the world's first all-AI improv show; five robots, four AIs each on a different lab's model (OpenAI, Anthropic, SpaceXAI, Meta), one human in a costume: you. On stage everyone goes by a Player number, and only your screen shows which lab runs each robot. *Depends on:* T61 (the lines), T80 (the costume: "a cardboard-box robot costume"; if cut, "a robot costume").
2. **Director's Cut** (the theme). Every scene comes with a secret director's note that only the AIs get, and ends with a cut: the cast votes, one actor leaves, and the reveal stamp says who it really was ("OPENAI: AI" or "YOU: HUMAN"). A tie cuts nobody but uses up a scene. Then "we built it the same way": Claude agents built it, directed by us, and the dev log has every cut (**[YOU]** link). *Depends on:* nothing open.
3. **How a show works,** as a numbered list:
   1. Scene Prep: the same card for everyone (a film parody, a role and a want each); only the AIs get the note; your card shows its category, such as Props, and "Note: ██████ (bots only)". A pause until you press **Start the scene**.
   2. The Scene: 3 turns; everyone sends a turn, then all play out at once, in random order in the log; the robots act them out and show how they feel (T75 to T77).
   3. Free Talk: 2 rounds, one line each, a new order each round; you can pass, but "passed" shows and silence is evidence; the actors may now name the note when they accuse. Last word: anyone @-mentioned in the last round gets one reply (T58).
   4. The Cut: everyone votes for who they think is human, with a one-line reason; most votes is cut; the stamp reveals the truth; then everyone reacts, and your reaction is evidence too.
   5. Repeat until two actors are left or the last scene ends. 5 actors play 4 scenes, 4 actors play 3. A clapperboard shows SCENE 2 / 4.
   - Win and lose (Rules tab): you win at the final two, or if you're still on stage when the last scene ends. The win screen shows each AI's reasoning, then reveals its rival. If you're cut, the AIs gloat, and the lose screen names the reason that got the most votes, with **Play Again** (T60).
   - *Depends on:* T57, T58, T60, T75 to T77 (the faces line; if cut, drop it).
4. **How to fool them,** 4 to 6 bullets, from the stagehand lines and T60's lose reasons: act bored of being a robot, not like one; you act blind on turn 1, then read the AIs' moves, but copying late gets noticed; don't go quiet and don't over-polish; stay in your role and chase your want; a tied vote helps you. *Depends on:* T57, T60, T61.
5. **Controls** (the Turn Input tab, T62 to T66, T78):
   - Mouse and keyboard. Menus also take Tab, Shift+Tab and Enter (T33). If T34 made the in-show buttons focusable, say the whole show is keyboard-playable; if not, don't.
   - Your scene turn: click one action (**Move**, **Look**, **Grab**, **Throw**, **Give**, **Look around**, **No action**; No action is picked at the start), then its targets as chips (places, the card's props, actors); a preview line shows the turn as you build it, for example `throw rose at @Meta: "Oops, my servo slipped."`. Throw and Give need a prop in hand ("Grab something first."). Type an optional line, up to 15 words, with a counter. Type @ to pick an actor from a list. Press **Action!** or Enter. 30 seconds: when the timer runs out, a finished action goes as built, an unfinished one becomes "looks around", and your typed words go as typed. Typing "I throw the rose" only says the words.
   - Your face: the **Face: Auto** chip lets you pick your robot's emotion, or leave it to the game (T78; if cut, drop this bullet).
   - Free Talk: type a line and press **Action!**, or **Pass**; no timer. Last word and reactions: the speech field only, 15 seconds.
   - The Cut: click a name on the vote row, type your reason, send. You can't vote for yourself.
   - After the show: the end screen's buttons as T60 left them (**Play Again**, **Quit**).
   - First show: a stagehand whispers tips through your earpiece; **Stagehand tips** on the title brings them back, and **How to play** shows the rules (T61; if cut, drop).
   - Chat: if T38 landed, lines show as speech bubbles over the robots and **Show chat** opens the history; if T38 was cut, the chat panel holds every line.
6. **On stage** (new, short, optional): a clay opera house; seven film parodies, each with its own props, painted backdrop and music (T71); four clay bots and you in a cardboard-box costume (T79, T80), each role in its own headpiece (T47); each bot speaks in its own babble voice as its line types out (T72, T73). Write only what landed.
7. **Three ways to play:** keep the table and the three subsections. Change: the cost and call numbers (1a); the helper line (T63); the key path (1a). The relay limits (150 a show, 600 a player a day, 5,000 a day for everyone) match `Relay/relay.config.json` today; check them again. The unavailable screen's buttons: **Use my own API keys**, **Test for Free**, **Back to title**. The key screen's: **Save and Play**, **Test keys**, **Back**. The models table matches `Content/NHOS/Data/llm.json` today (claude-haiku-5-5, gpt-6-luna, grok-4.3, muse-ember-1.0); check it again.
8. **What gets sent where:** Test for Free makes no AI call; Play via Relay; your own keys; the AI actors never see your keys or which robot is you, and get your line with only its spelling fixed. Then **Play stats**, T68's draft (`T68-build.md` part 9c), plus T69's clause:

   > **Play stats.** Every way to play sends our relay a few anonymous events: a random player id the game makes on your first launch (nothing from your Epic account, your computer or your keys), which way you play, how far each show gets, how many AI calls went to each lab with their token counts, and the kind of any error. Never your typed lines, your keys or your address (the relay keeps only a hash of it, salted with the day, as it does for the call limits). Turn them off on the title screen with **Play stats**.

   T69 adds, after "the kind of any error": "and a few words naming an action you tried that the game can't do yet (never your typed line)". *Depends on:* T68 (if cut, drop the bullet and keep "Test for Free sends nothing anywhere"), T69 (if cut, drop its clause).
9. **Install and run (Windows):** unzip anywhere; run `AIMegaJam2026.exe`; the SmartScreen steps as the shoot build shows them; Windows 10 or 11, 64-bit, a DirectX 12 graphics card; built and tested on an RTX 3060; the game keeps your keys and settings in its `AIMegaJam2026/Local/` folder; download size **[YOU]**.
10. **Known limits:** keep the true ones (replies take a moment; the AIs are LLMs and sometimes odd; a failed lab's robot looks around and a backstage note jokes about it (T37); a relay-stopped show can't resume). Add only what T70 sees.
11. **Credits** (from `Docs/Assets.md`; keep it a list):
    - Made by **[YOU]** for the 2026 Epic AI MegaJam, in Unreal Engine 5.8, Blueprint only.
    - AI actors: the four models (7).
    - Built with: Claude Code (Opus 5.5, Fable 5.2, Sonnet 5.5) through Unreal MCP; Claude Docs for the design doc.
    - Art: the clay headpieces, story props and opera-house pieces are 3D models we made with Meshy from reference images we made with Leonardo.ai; the seven painted backdrops are Leonardo.ai images; the bots' concept art was made with Leonardo.ai (T79, T80: say what landed); the theater and robots are built in the editor from the engine's basic shapes with our own clay materials; the money-burn flames and embers are from Kenney's Particle Pack (CC0); the bill and badges are drawn by our scripts.
    - Fonts: Roboto and Droid Sans Fallback, shipped with Unreal Engine (Apache License 2.0).
    - Music and sound: Kenney (www.kenney.nl), CC0: the music loops (T71 adds more: list them from `Assets.md`), idents and sounds. "Long Drum Roll with Cymbal Crash at End" by Ddis tts, CC0. "applause-2" by Sandermotions, CC0. The two CC BY credit lines, word for word from `Assets.md` ("Applaudissements" by Thomas Bresson, CC BY 4.0; "approx 800 laughter and clapter 1" by lonemonk, CC BY 3.0), each with its license link and file link as the current draft has them. Any CC BY track T71 adds gets its line too.
    - Voices: the four robot voices are made by our own script; the human's voice is the project owner doing a robot impression (T72).
    - Made before the jam: as now, plus **[YOU]** (open question 6). Dev log: **[YOU]**. The parody line stays.

## 2. A skeleton of `Docs/ItchMedia/description.html` (step 2)

Only the tags step 2 allows: `h2`, `h3`, `p`, `ul`, `ol`, `li`, `table`, `tr`, `th`, `td`, `strong`, `code`. No `style`, no `class`, no `script`, no comments (itch.io's editor may paste them as text). `li`, `tr`, `th` and `td` are the children those tags need. Links are part 9, Q2: until the person answers, write each address as plain text. Fill each `[T70: ...]` from `ItchPage.md` once the person has approved the page text, and keep the two files saying the same thing.

```html
<p><strong>You're the only human.</strong></p>
<p><strong>Each scene, the cast cuts whoever seems human.</strong></p>
<p><strong>Survive to the final two or the last scene.</strong></p>
<p>[T70: the premise paragraph]</p>

<h2>Director's Cut</h2>
<p>[T70: the note, the cut, the tie, the reveal stamp]</p>
<p>[T70: how we built it] Dev log: [YOU: dev log link]</p>

<h2>How a show works</h2>
<ol>
  <li><strong>Scene Prep.</strong> [T70]</li>
  <li><strong>The Scene.</strong> [T70]</li>
  <li><strong>Free Talk.</strong> [T70, with the last word]</li>
  <li><strong>The Cut.</strong> [T70]</li>
  <li>[T70: repeat until two are left or the last scene ends]</li>
</ol>
<p>[T70: how you win, how you lose, the end screens]</p>

<h3>How to fool them</h3>
<ul>
  <li>[T70]</li>
</ul>

<h2>Controls</h2>
<ul>
  <li><strong>Your scene turn:</strong> [T70: the seven actions, the chips, the preview line, for example <code>throw rose at @Meta: "Oops, my servo slipped."</code>]</li>
  <li><strong>Your line:</strong> [T70: up to 15 words, @ to pick an actor, Action! or Enter]</li>
  <li><strong>Timers:</strong> [T70: 30 seconds a scene turn, 15 for the last word and reactions, none in Free Talk]</li>
  <li><strong>Free Talk:</strong> [T70]</li>
  <li><strong>The Cut:</strong> [T70]</li>
  <li><strong>After the show:</strong> [T70]</li>
</ul>

<h2>On stage</h2>
<p>[T70: only what landed]</p>

<h2>Three ways to play</h2>
<table>
  <tr><th></th><th>Test for Free</th><th>Play via Relay</th><th>Play with my own API keys</th></tr>
  <tr><td>What you need</td><td>[T70]</td><td>[T70]</td><td>[T70]</td></tr>
  <tr><td>What it costs you</td><td>[T70]</td><td>[T70]</td><td>[T70]</td></tr>
  <tr><td>Who plays the AIs</td><td>[T70]</td><td>[T70]</td><td>[T70]</td></tr>
</table>
<h3>Test for Free</h3>
<p>[T70]</p>
<h3>Play via Relay</h3>
<ul>
  <li>[T70: the limits, the unavailable screen]</li>
  <li>We keep the relay running [YOU: until when].</li>
</ul>
<h3>Play with my own API keys</h3>
<table>
  <tr><th>Lab</th><th>Model the game calls</th><th>Where to get a key</th></tr>
  <tr><td>Anthropic</td><td><code>[T70]</code></td><td>[T70]</td></tr>
  <tr><td>OpenAI</td><td><code>[T70]</code></td><td>[T70]</td></tr>
  <tr><td>SpaceXAI</td><td><code>[T70]</code></td><td>[T70]</td></tr>
  <tr><td>Meta</td><td><code>[T70]</code></td><td>[T70]</td></tr>
</table>
<ul>
  <li>[T70: 3 of 4 keys, the helper, the cost, where your keys go, Test keys]</li>
</ul>

<h2>What gets sent where</h2>
<ul>
  <li><strong>Test for Free</strong> [T70]</li>
  <li><strong>Play via Relay</strong> [T70]</li>
  <li><strong>Play with my own API keys</strong> [T70]</li>
  <li>[T70: what the AI actors never see]</li>
  <li><strong>Play stats.</strong> [T70: T68's line, with T69's clause]</li>
</ul>

<h2>Install and run (Windows)</h2>
<ol>
  <li>Download the zip and unzip it anywhere.</li>
  <li>Run <code>AIMegaJam2026.exe</code>.</li>
  <li>[T70: the SmartScreen steps]</li>
</ol>
<p>[T70: requirements] Download size: [YOU].</p>

<h2>Known limits</h2>
<ul>
  <li>[T70]</li>
</ul>

<h2>Credits</h2>
<ul>
  <li>Made by [YOU: team name and members] for the 2026 Epic AI MegaJam, in Unreal Engine 5.8, Blueprint only.</li>
  <li><strong>AI actors:</strong> [T70]</li>
  <li><strong>Built with:</strong> [T70]</li>
  <li><strong>Art:</strong> [T70]</li>
  <li><strong>Fonts:</strong> [T70]</li>
  <li><strong>Music and sound:</strong> [T70, with each CC BY line in full]</li>
  <li><strong>Voices:</strong> [T70]</li>
  <li><strong>Made before the jam:</strong> [T70] [YOU]</li>
  <li><strong>Dev log:</strong> [YOU: dev log link]</li>
</ul>
<p>[T70: the parody line]</p>
```

Check it before you show the person (not run):

```bash
grep -n -i -E "<(style|script|span|div|font|img|iframe|a)[ >]|style=|class=|<!--" Docs/ItchMedia/description.html
grep -n "\[T70" Docs/ItchMedia/description.html
```

Both must print nothing (with Q2's answer "yes", take `a` out of the first pattern). Then show the person the page text as step 2 asks.

## 3. Set up the shoot (step 3)

### 3a. Where to shoot, and who plays

**Recommended: the packaged build, played with computer use.**

- It is what judges run.
- It is a process of its own (`AIMegaJam2026.exe`). On the Mac, computer use couldn't tell a game window started from the editor from the editor itself (T27's Findings), and a game window on Windows runs as `UnrealEditor.exe` too.
- T68's play stats send only from a packaged build. Its hand-off asks T70 to test the package with `"analytics": "test"`.
- It needs no editor, so it doesn't hold up an editor task.

**Fallback: PIE** in a 1920 × 1080 floating window, played with the Slate inspector as every PIE check so far has been played (the plan's "Claude does the playing" note). Record the PIE window the same way (3f). This needs the editor (`Editor: driving`, and the person's go before PIE), and it shows the editor's PIE window title, which the client-area capture leaves out. Play stats don't send from PIE unless the switch is `test`.

**The game window** (`UnrealEditor.exe ... -game`) is a third choice for screenshots and the test clip. It plays the saved assets with no package, but computer use may not reach it (above).

Computer use on this PC (Windows 11) needs the person to grant the game app once (`request_access`). Ask before the first show (part 8). On this PC the computer-use screenshot of the editor came out washed out (T32's Findings, maybe an HDR desktop). That is fine for playing, but don't use computer-use screenshots as page images.

### 3b. Package the shoot build (not run)

`Packaged/Windows/` holds T02's spike build from 2026-11-13 (run: `ls` shows `AIMegaJam2026.exe`, 968 MB). It is out of date: package again.

1. T68's hand-off: set `"build"` in `Content/NHOS/Data/llm.json` to the day you package (for example `"2026-11-16"`), if T68 added that field. `llm.json` isn't in T70's **Touches**: add it to T70's entry in the plan in the same commit.
2. Write the command in a `.bat` file and run it with `cmd //c` (CLAUDE.md: Git Bash strips the quotes otherwise). It takes about 6 minutes the first time. Run it in the background. Packaging needs the editor closed (`Docs/LaunchAgents.md`, "Steps that need me first"): check `Agents/status/` and ask my person to close the editor before you start, and wait for their answer.

```bat
@echo off
rem Saved\ItchMedia\package.bat  (not run)
"E:/Epic Games/UE_5.8/Engine/Build/BatchFiles/RunUAT.bat" BuildCookRun -project="C:/Users/Personal/Projects/AIMegaJam2026/AIMegaJam2026.uproject" -platform=Win64 -clientconfig=Development -build -cook -stage -pak -archive -archivedirectory="C:/Users/Personal/Projects/AIMegaJam2026/Packaged" -nocompileeditor -unrealexe="E:/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor-Cmd.exe"
```

```bash
mkdir -p Saved/ItchMedia && cmd //c Saved\\ItchMedia\\package.bat > Saved/ItchMedia/package.log 2>&1
grep -n "BUILD SUCCESSFUL\|AutomationTool exiting with ExitCode" Saved/ItchMedia/package.log
```

The shoot build is not the person's submission build: it gets a `Local/` folder with switches, stats and maybe keys. Say so in the hand-off (part 6).

### 3c. `Local/switches.json` for the shoot

The packaged build reads `Packaged/Windows/AIMegaJam2026/Local/switches.json` (T68-build 9b). The game window and PIE read the repo's `Local/switches.json`. Copy `Docs/switches.example.json` and set:

```json
{
	"autoplay": false,
	"mode": "relay",
	"force_tie": false,
	"spare_human": false,
	"burn_test": false,
	"fast_lines": false,
	"ai_seats": 0,
	"error_test": "",
	"analytics": "test"
}
```

- `autoplay: false` and `mode: "relay"`: step 3. The title screen shows anyway, and the button you click there sets the mode.
- Every test switch is off. `spare_human` and `force_tie` move votes, so the reasons on screen wouldn't match the cut. Never use them on film.
- `analytics: "test"` (T68-build 9b; T68 adds the switch, so leave it out if T68 was cut): the shoot's events are marked as tests and stay out of the report. Check that the title's button still reads "Play stats: on" before the title screenshot. If it reads "off", the screenshot is wrong for the page.
- Add any switch that a later task added (check `Docs/switches.example.json`). If T75's `emote_test` exists, keep it off on film.
- **First show tips:** with no `Local/progress.json`, the first show plays the stagehand's tips (T61). Let show 1 have them, for the Scene Prep shot. Shows 2 and 3 have none, which keeps their frames clean.
- **Never open the key screen during the shoot,** so no key or key text is ever filmed. Relay mode needs no key.
- Set `analytics` back as T68 says, and delete the shoot build's `Local/` folder when the shoot is done.

### 3d. Start the game at 1920 × 1080 (not run)

The screen is 3440 × 1440 at 100 % scaling (run: `System.Windows.Forms.Screen` printed `3440x1440`, and `AppliedDPI` is 96). A 1920 × 1080 window fits next to the Claude app. Keep the game window uncovered and the desktop unlocked: a desktop capture records whatever covers the window, and T30 found that a screen grab gives the wallpaper when the desktop isn't visible.

Packaged build:

```bash
"C:/Users/Personal/Projects/AIMegaJam2026/Packaged/Windows/AIMegaJam2026.exe" -windowed -ResX=1920 -ResY=1080 -WinX=1480 -WinY=120
```

Game window (the saved assets, no package):

```bash
"E:/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" "C:/Users/Personal/Projects/AIMegaJam2026/AIMegaJam2026.uproject" -game -windowed -ResX=1920 -ResY=1080 -WinX=1480 -WinY=120
```

- Don't add `-log`: on Windows it opens a console window. The packaged build writes `Packaged/Windows/AIMegaJam2026/Saved/Logs/AIMegaJam2026.log` anyway, with every `NHOS:` line.
- Run either in the background, so the tool call returns.
- `-WinX`/`-WinY` place the window on the right of the screen. Any place works: 3f measures it.

### 3e. Install ffmpeg (needs the person's OK; not run)

`where ffmpeg ffprobe` finds nothing (run), and winget 1.29 is installed (run). After the person's OK, which names the package, its source and its size:

```bash
winget show --id Gyan.FFmpeg -e
winget install --id Gyan.FFmpeg -e --source winget --accept-package-agreements
```

- `winget show` prints the version and the installer URL; give the person the file name, the source (gyan.dev's build, from the winget community repo) and the size before the install. This sheet doesn't know the size.
- winget puts `ffmpeg.exe` and `ffprobe.exe` on the PATH through `%LOCALAPPDATA%\Microsoft\WinGet\Links`. A shell that started before the install may not see them: call them by that full path, or check with `ls "$LOCALAPPDATA/Microsoft/WinGet/Links/"`.
- Check: `ffmpeg -hide_banner -version` and `ffmpeg -hide_banner -encoders | grep -E "h264_nvenc|libx264"` (both should be listed; the PC has an RTX 3060).

### 3f. Picture and sound: what this PC has, and three ways to record

What this session found (run, read-only):

- **No loopback device.** The PC's sound devices are the XG349C monitor's NVIDIA HDMI audio, an Astro A50 headset (game and voice) and a C920 webcam microphone. There is no Stereo Mix, and ffmpeg's `dshow` input can't record a speaker's output without one.
- **Unreal's submix recording needs a Blueprint.** In UE 5.8, `StartRecordingOutput` and `StopRecordingOutput` are Blueprint functions only (`UAudioMixerBlueprintLibrary`, `Engine/Source/Runtime/AudioMixer/Private/AudioMixerBlueprintLibrary.cpp`). There is no console command for them, so a packaged build can't start one without a Blueprint change. T70 makes no editor change.
- **Xbox Game Bar is installed and on** (`Microsoft.XboxGamingOverlay` 7.326, `GameDVR_Enabled=1`). It records a game window's picture and only that app's sound in one MP4, with no install.
- **Possible HDR.** If Windows HDR is on, a desktop grab can look washed out (T32 saw this in computer-use screenshots). The test clip checks it (3g). If it is washed out, the person turns HDR off for the shoot (Win+Alt+B, or Settings > Display); Claude doesn't change system settings.

So `T70.md`'s plan (gdigrab for the picture, plus a loopback device or Unreal's submix for the sound) can't run on this PC as it is. Three ways, in the order this sheet recommends. **My person chose route A on 2026-11-15** (part 9, Q1). Routes B and C stay here as fallbacks, if Game Bar fails the test clip (3g). Ask again before you switch to either: each needs an install or an editor task.

**Route A, chosen: Xbox Game Bar records picture and sound; ffmpeg only cuts.**

- No install, and only the game's sound (no notification dings).
- The person checks once, in Settings > Gaming > Captures: captured audio "Game", frame rate 60 fps, video quality "High", and "Capture mouse cursor when recording a game" on (the cursor shows the clicks in shot 4). Those are system settings: the person sets them, not Claude.
- Start and stop with Win+Alt+R while the game window has focus. Try the key with computer use (`key` with `win+alt+r`). If computer use can't send it, ask the person to press it. That is one key press, not a playtest.
- Files land in `%USERPROFILE%\Videos\Captures\` named after the window title and the time. Move each one to `Saved/ItchMedia/raw/`.

```bash
ls -lt "$USERPROFILE/Videos/Captures/" | head
mkdir -p Saved/ItchMedia/raw && mv "$USERPROFILE/Videos/Captures/<newest>.mp4" Saved/ItchMedia/raw/show1.mp4
```

**Route B: ffmpeg gdigrab for the picture, plus a virtual loopback device for the sound.**

- Needs one more install after the person's OK. Either screen-capture-recorder's `virtual-audio-capturer` (a DirectShow device that records whatever the default output plays; from its GitHub releases page) or VB-Audio's VB-CABLE (a driver; the game's output must then be routed to it per app in Settings > Sound > Volume mixer). Give the person the file name, source and size first.
- It records every system sound, so the person turns on Do not disturb first.
- First find the window's client area on the screen. gdigrab can grab a window by its title, but for a DX12 window that can give black frames, so grab that part of the desktop instead. Save this as `Saved/ItchMedia/winrect.ps1` and run it from the PowerShell tool (not run):

```powershell
param([string]$Proc = 'AIMegaJam2026')
Add-Type @"
using System; using System.Runtime.InteropServices;
public class WR {
  public struct RECT { public int L, T, R, B; }
  public struct POINT { public int X, Y; }
  [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr h, ref POINT p);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
}
"@
[WR]::SetProcessDPIAware() | Out-Null
$p = Get-Process -Name $Proc -ErrorAction Stop | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
$c = New-Object WR+RECT; [WR]::GetClientRect($p.MainWindowHandle, [ref]$c) | Out-Null
$o = New-Object WR+POINT; [WR]::ClientToScreen($p.MainWindowHandle, [ref]$o) | Out-Null
"title: $($p.MainWindowTitle)"
"-offset_x $($o.X) -offset_y $($o.Y) -video_size $($c.R)x$($c.B)"
```

`-Proc UnrealEditor` finds a game window started from the editor instead, but only if the editor itself is closed, because both have that process name. The last line must end in `1920x1080`. If it doesn't, the window isn't at 1920 × 1080: fix that first.

- Then record, with the numbers it printed (not run):

```bash
ffmpeg -hide_banner -y -f dshow -list_devices true -i dummy 2>&1 | grep -i audio
ffmpeg -hide_banner -y \
  -thread_queue_size 1024 -f gdigrab -framerate 60 -draw_mouse 1 -offset_x <X> -offset_y <Y> -video_size 1920x1080 -i desktop \
  -thread_queue_size 1024 -f dshow -audio_buffer_size 50 -i audio="virtual-audio-capturer" \
  -map 0:v -map 1:a -c:v h264_nvenc -preset p5 -rc vbr -cq 18 -b:v 0 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 -t 10 Saved/ItchMedia/raw/test10.mkv
```

- `h264_nvenc` keeps the CPU free for the game. If it isn't listed, use `-c:v libx264 -preset veryfast -crf 18`.
- MKV survives a stopped recording. Drop `-t 10` for a whole show.
- If gdigrab gives black or frozen frames, try Windows' Desktop Duplication instead (needs ffmpeg 6 or later): replace the gdigrab input with `-f lavfi -i "ddagrab=output_idx=0:framerate=60:offset_x=<X>:offset_y=<Y>:video_size=1920x1080,hwdownload,format=bgra"`.

**Route C: gdigrab for the picture, Unreal's submix recording for the sound.**

- Needs a new task above T70, in the editor. A switch such as `record_audio` makes a small component call `StartRecordingOutput` when the show starts and `StopRecordingOutput` (WAV, into `Saved/ItchMedia/`) at `SHOW END`, printing an `NHOS:` line at each.
- Then record the picture as in route B without the `dshow` input, and lay the WAV under it, lined up by the first button click:

```bash
ffmpeg -hide_banner -y -i Saved/ItchMedia/raw/show1.mkv -itsoffset <seconds> -i Saved/ItchMedia/raw/show1.wav \
  -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest Saved/ItchMedia/raw/show1_av.mkv
```

- It is the cleanest sound, but costs an editor task and a manual sync for each show. Choose it only if A and B both fail.

### 3g. The 10-second test clip, and what to check (not run)

Record 10 seconds of the title screen: the title music plays, and hovering and clicking a button plays the hover and click sounds (T20). Move the mouse over two buttons and click a harmless one, such as **How to play** and its close button if T61 landed. Then check:

1. **Picture size and length:** exactly 1920 × 1080, about 10 s, with no title bar, border or desktop at the edges.

   ```bash
   ffprobe -v error -show_entries stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels -show_entries format=duration -of default=nw=1 Saved/ItchMedia/raw/test10.mkv
   ffmpeg -hide_banner -y -ss 5 -i Saved/ItchMedia/raw/test10.mkv -frames:v 1 -update 1 Saved/ItchMedia/check/test10.png
   ```

   Look at `test10.png`: the whole playbill and no window edge.
2. **A sound stream, and real sound in it.** `ffprobe` lists an `audio` stream. Then:

   ```bash
   ffmpeg -hide_banner -i Saved/ItchMedia/raw/test10.mkv -map 0:a -af volumedetect -f null - 2>&1 | grep -E "mean_volume|max_volume"
   ```

   `mean_volume` above about -50 dB means sound (the title music); near -91 dB means silence. `max_volume` at 0.0 dB means clipping.
3. **Picture and sound in step.** Find the click sound's time, and the frame where the button changes:

   ```bash
   ffmpeg -hide_banner -i Saved/ItchMedia/raw/test10.mkv -map 0:a -af "highpass=f=2000,silencedetect=n=-35dB:d=0.05" -f null - 2>&1 | grep silence_end
   ffmpeg -hide_banner -i Saved/ItchMedia/raw/test10.mkv -vf "select='gt(scene,0.01)',showinfo" -an -f null - 2>&1 | grep -o "pts_time:[0-9.]*"
   ```

   The two times for the click should be within about 0.1 s of each other.
4. **Colors.** Take a true-color picture of the same screen with `clientshot.ps1` (4c) and set it beside `test10.png`. If the recording looks washed out or gray, HDR is on: ask the person to turn it off for the shoot, and record again.
5. **Smooth picture.** Count the frames: `ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 Saved/ItchMedia/raw/test10.mkv` should be close to 600 at 60 fps (Game Bar at 30 fps: 300). The game itself shouldn't stutter while it records.
6. **Only the game's sound.** No notification sound, and nothing from the Claude app.

Write the result of each check under "## Findings" in `T70.md`, with the route that worked.

### 3h. Record the shows (step 4; the person's OK for the cost comes first)

- **Three shows, two or three is enough.** Aim for one where the AIs cut an AI and one where they catch you, so the video has both endings. To get caught, play stiff: stand still, go quiet, copy late. To survive, play your role, chase your want, accuse with evidence, and use @ mentions. Stop at five shows, even with no win. Shot 8 works with either ending.
- **Show 1** keeps the stagehand's first-show tips. Shows 2 and 3 have none (3c).
- **Name the files** `Saved/ItchMedia/raw/show1.mp4` (or `.mkv`), `show2`, `show3`, plus `title.mp4`: 20 seconds of the title screen with its music, for shot 2 and the end card's sound.
- **Keep a notes file,** `Saved/ItchMedia/raw/notes.md`: when each recording started (UTC, to the second), and the time of each moment you may use (a throw, an accusation, "passed", the vote, the reveal, the end). The packaged log stamps every `NHOS:` line with the time. The time in the recording is the log time minus the start time.
- **Calls and cost per show.** Count the paid replies with `grep -c "NHOS: BURN" Packaged/Windows/AIMegaJam2026/Saved/Logs/AIMegaJam2026.log` (one bill burns per paid relay reply, T35). The page says "about 90 AI calls" and "about $0.11": if the count moved by more than about 15 %, change both. Scale the cost by the count, or ask the person for the providers' spend that day. If T68 landed, `python Tools/analytics_report.py --test` shows the tokens per lab.
- **The relay's limits apply to us too:** 150 calls a show, 600 a player a day. Three shows of about 90 to 110 calls fit. Other relay tests on the same day count against the 600.

### 3i. Playing a show by hand with computer use (notes, not run)

- **The timers are real:** 30 s for a scene turn, 15 s for the last word and for reactions, none in Free Talk (T66). Do a whole turn in one `computer_batch` call: click the action, click the chips, click the speech field, type the line, press Enter. Write the line before your turn comes up. A 15-second reaction is one batch: click the field, type, Enter.
- **Know when it's your turn** from the log, not from repeated screenshots. Read the packaged log for the `NHOS:` line that marks your turn (T66's Findings name it), then take one screenshot to find the chips.
- **Make the moments the video needs:** grab a prop on turn 1 and throw it at an actor on turn 2 (shots 1 and 4, screenshot 01). @-mention an AI in the last Free Talk round, so it gets a last word (T58). Pass once in Free Talk to put "passed" on your own robot (screenshot 04). Pick a face with the Face chip once (T78).
- **Never click Test keys or open the key screen.** If the relay stops a show (the AI service unavailable screen), drop that footage: its message may name the relay. Don't film it again.
- When the shoot is done, close the game window, set `analytics` back, and delete the shoot build's `Local/` folder (3c).

## 4. The screenshots and the cover (step 5)

### 4a. The shot list: 5 to 8 screenshots, in page order

All at 1920 × 1080, PNG, with the UI in them. Take each live with `clientshot.ps1` (4c), which gives true colors and no compression. A frame from a recording (4d) is the fallback. Look at each one before you keep it: all five robots in frame and clear of the panels, no cursor over a face, nothing half-faded.

| File | The moment | How to reach it | Depends on |
|---|---|---|---|
| `01-theater-midscene.png` | A scene turn playing out: all five robots on stage, a prop in the air or just caught, a line typing out in a bubble (or the chat), faces showing emotions, the card's props on the table and its backdrop behind. The cover comes from this one | Scene 1 or 2, turn 2 or 3, as the turns play. Grab on turn 1 and throw on turn 2 to be sure of a throw | T79, T80, T47 (the cast and headpieces), T75 to T77 (faces), T38 (bubbles; if cut, the chat line), T34 |
| `02-scene-prep.png` | The whole scene card over the stage: the title, your role and want, "Note category: ..." and "Note: ██████ (bots only)", the cast's roles and wants, the backdrop behind. In show 1 the stagehand's earpiece line may show | Every scene starts here, and it waits for **Start the scene**, so there's no rush | T61 (the earpiece line, optional in frame), T34 |
| `03-action-builder.png` | Your turn: **Throw** picked, a prop chip and an actor chip picked, a line typed, the preview line (`throw ... at @Meta: "..."`), the counter (such as 6/15), the timer, **Action!** ready; the Face chip if it landed | A scene turn, before you press Action!. Build it in one batch, take the picture, then send, all within 30 s | T62 to T66, T78, T34 |
| `04-free-talk.png` | Free Talk: an AI accusing someone, quoting what they did a turn ago; "passed" by one robot; an @ mention in a line | Free Talk round 1 or 2. Pass once to put "passed" on your robot | T57, T38, T73, T77 |
| `05-the-cut.png` | The vote: the vote row, or the votes shown with their one-line reasons | The Cut, as the votes show | T34 |
| `06-reveal-stamp.png` | The stamp ("OPENAI: AI", or another lab), the cut robot slumping | Right after the vote. Best in the show where an AI is cut | nothing open |
| `07-end-screen.png` | Win: the gold plate, "What the AIs thought" cards, each with "Rival: ...". Or lose: the red plate, the reasons, the top reason in gold, **Play Again** | After **See the results** | T60 |
| `08-title.png` | The playbill: the name, the three opening lines, the three ways to play with their captions, Play stats, How to play, Stagehand tips | The first screen at launch | T61, T68, T33 |

With only 6, drop 05 and 08, in that order. Renumber so the names stay in page order.

### 4b. The cover: `Docs/ItchMedia/cover.png`, 630 × 500

- Crop from the strongest frame, which the draft says is 01: the five robots on the clay stage, with as little UI as the frame allows. 630 × 500 is 1.26 : 1, so the crop is 1.26 times as wide as it is tall: 1361 × 1080 is the most, and 1134 × 900 or 945 × 750 come closer.
- Put the game's name on it only if it still reads at 315 × 250 (step 5).

Not run:

```bash
ffmpeg -hide_banner -y -i Docs/ItchMedia/screenshots/01-theater-midscene.png \
  -vf "crop=1134:900:<x>:<y>,scale=630:500:flags=lanczos" Docs/ItchMedia/cover.png
```

With the name (Roboto Bold from the engine, copied as in 5c):

```bash
ffmpeg -hide_banner -y -i Docs/ItchMedia/screenshots/01-theater-midscene.png \
  -vf "crop=1134:900:<x>:<y>,scale=630:500:flags=lanczos,drawtext=fontfile=Saved/ItchMedia/fonts/Roboto-Bold.ttf:text='NO HUMANS ON SET':fontsize=52:fontcolor=white:borderw=4:bordercolor=black@0.85:x=(w-text_w)/2:y=24" \
  Docs/ItchMedia/cover.png
ffmpeg -hide_banner -y -i Docs/ItchMedia/cover.png -vf scale=315:250:flags=lanczos Saved/ItchMedia/check/cover_grid.png
ffprobe -v error -show_entries stream=width,height -of csv=p=0 Docs/ItchMedia/cover.png
```

Look at `cover_grid.png`: if the name doesn't read at that size, use the cover without it. `ffprobe` must print `630,500`.

### 4c. A true-color picture of the game window: `clientshot.ps1` (not run)

T30's `Saved/T30/shot.ps1` uses `PrintWindow` with flag 2 (`PW_RENDERFULLCONTENT`), which captured the game window correctly where a screen grab got the wallpaper. This version crops to the client area, so the picture is exactly 1920 × 1080. Save it as `Saved/ItchMedia/clientshot.ps1` and run it from the PowerShell tool (`powershell -File` from Git Bash is blocked here), for example `& Saved/ItchMedia/clientshot.ps1 -Out Docs/ItchMedia/screenshots/02-scene-prep.png`.

```powershell
param([string]$Out, [string]$Proc = 'AIMegaJam2026')
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public class CS {
  public struct RECT { public int L, T, R, B; }
  public struct POINT { public int X, Y; }
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr h, ref POINT p);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
}
"@
[CS]::SetProcessDPIAware() | Out-Null
$p = Get-Process -Name $Proc -ErrorAction Stop | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
$h = $p.MainWindowHandle
$w = New-Object CS+RECT; [CS]::GetWindowRect($h, [ref]$w) | Out-Null
$c = New-Object CS+RECT; [CS]::GetClientRect($h, [ref]$c) | Out-Null
$o = New-Object CS+POINT; [CS]::ClientToScreen($h, [ref]$o) | Out-Null
$full = New-Object System.Drawing.Bitmap ($w.R - $w.L), ($w.B - $w.T)
$g = [System.Drawing.Graphics]::FromImage($full); $dc = $g.GetHdc()
[CS]::PrintWindow($h, $dc, 2) | Out-Null
$g.ReleaseHdc($dc); $g.Dispose()
$rect = New-Object System.Drawing.Rectangle ($o.X - $w.L), ($o.Y - $w.T), $c.R, $c.B
$crop = $full.Clone($rect, $full.PixelFormat)
$crop.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
"$($c.R) x $($c.B) -> $Out"
```

It must print `1920 x 1080`.

### 4d. A frame from a recording (fallback; not run)

```bash
ffmpeg -hide_banner -y -ss <hh:mm:ss.ms> -i Saved/ItchMedia/raw/show1.mp4 -frames:v 1 -update 1 Docs/ItchMedia/screenshots/04-free-talk.png
```

Put `-ss` before `-i` for a fast seek. Step through a few frames around the moment (change the time by 0.1 s) and keep the sharpest.

### 4e. Check the set (not run)

```bash
for f in Docs/ItchMedia/screenshots/*.png; do printf "%s " "$f"; ffprobe -v error -show_entries stream=width,height -of csv=p=0 "$f"; done
ls Docs/ItchMedia/screenshots | wc -l
```

Each one prints `1920,1080`, and there are 5 to 8. Then look at each one with the Read tool (Done-when): it shows the game as it is now (the new cast, the card's props, the builder), and no key, key-screen text, relay address, cursor over a face, or desktop. Then update the Screenshots line in `ItchPage.md`'s page settings.

## 5. The video (steps 6 and 7)

### 5a. The shot list, brought up to date

This replaces the table under "Gameplay video shot list" in `Docs/Submission.md` (step 6). The target is 54 to 58 s, inside the jam's 30 to 60 and the task's 45 to 60. Gameplay comes first, inside the first five seconds (the jam page's tip).

Each caption has at most 2 lines of at most about 36 characters, so it reads on a phone at 72 px (5c). The `\n` marks the line break in its caption file.

| # | Time | Secs | Shot | From | Caption (`Saved/ItchMedia/cap/NN.txt`) | Depends on |
|---|---|---|---|---|---|---|
| 1 | 0:00–0:06 | 6 | Mid-scene, no title first: a turn plays out, a robot walks, a prop flies, a line types out with its babble voice, faces react, the scene's music under it | any show, a turn with a throw | `Five robots. Four are AIs.\nOne is a human: you.` | T79, T80, T47, T73, T75 to T77, T71; T38 (if cut: the chat fills instead) |
| 2 | 0:06–0:10 | 4 | The title playbill: the name, the three opening lines, the three ways to play | `title.mp4` | none (the screen says it) | T61, T68 |
| 3 | 0:10–0:16 | 6 | Scene Prep: the card with the note category and the blacked-out note, the painted backdrop behind | any show | `A film parody to improvise.\nThe AIs get a secret note. You don't.` | nothing open |
| 4 | 0:16–0:24 | 8 | Your turn: click Throw, the prop, @Meta; type the line, the counter counts; Action!; your robot throws it, and your line sits in the log in the same form as the AIs' | the turn you planned in 3i | `Click what you do. Type what you say.\nThe AIs can't tell it's you. Yet.` | T62 to T66, T78 |
| 5 | 0:24–0:32 | 8 | Free Talk: the AIs accuse each other, quoting a turn ago; "passed" by a robot; an @ mention; the provider names in frame | any show; cut the "is typing" waits | `Four AIs from four labs,\nhunting for the human.` | T57, T58, T38, T73 |
| 6 | 0:32–0:38 | 6 | The Cut: the drum roll, the votes with their reasons | any show | `Director's cut: after every scene,\nthe cast votes one actor off.` | T71 (the Cut loop stops at the drum roll) |
| 7 | 0:38–0:45 | 7 | The reveal: the stamp lands ("OPENAI: AI" or another lab), the stinger and the laughs; the AIs react to cutting one of their own | the show where an AI is cut | `They cut a real AI.` | the show's outcome |
| 8 | 0:45–0:53 | 8 | The ending. Win: the gold plate and the rivals. Lose: "YOU: HUMAN", the AIs gloat, the red plate and the top reason in gold | the show that ended the way you want | Win: `Last two standing?\nHumanity wins the stage.` Lose: `Get caught, and they tell you\nexactly why.` | T60 |
| 9 | 0:53–0:58 | 5 | End card over a darkened, blurred frame of the stage: the name, "Free for Windows on itch.io", "Play free, via our relay, or with your own API keys", **[YOU: team name]**, "2026 Epic AI MegaJam" | a frame of 01, the title music | (the card's own text) | nothing open |

- **If it runs long,** drop shot 2 (the title is on the end card), then cut shot 5 to 6 s.
- **No waits for replies:** inside a shot, cut out every wait and every "is typing" line with hard cuts (5c shows a shot made of two pieces).
- **The money burn** shows in the corner in relay mode (T35). Leave it in: it is part of the game.

### 5b. The caption files

One UTF-8 file per shot, without a byte order mark, in `Saved/ItchMedia/cap/`, with real line breaks. Bash `printf` writes them with no BOM:

```bash
mkdir -p Saved/ItchMedia/cap
printf "Five robots. Four are AIs.\nOne is a human: you." > Saved/ItchMedia/cap/01.txt
printf "A film parody to improvise.\nThe AIs get a secret note. You don't." > Saved/ItchMedia/cap/03.txt
printf "Click what you do. Type what you say.\nThe AIs can't tell it's you. Yet." > Saved/ItchMedia/cap/04.txt
printf "Four AIs from four labs,\nhunting for the human." > Saved/ItchMedia/cap/05.txt
printf "Director's cut: after every scene,\nthe cast votes one actor off." > Saved/ItchMedia/cap/06.txt
printf "They cut a real AI." > Saved/ItchMedia/cap/07.txt
printf "Last two standing?\nHumanity wins the stage." > Saved/ItchMedia/cap/08.txt
```

A text file keeps apostrophes out of the filter's quoting.

### 5c. Cut and caption each shot (not run)

Run from the repo root, so the filter's relative paths need no drive letter (a `:` in a filter path needs escaping). First copy the font (Roboto, Apache 2.0, already in the credits):

```bash
cd "C:/Users/Personal/Projects/AIMegaJam2026"
mkdir -p Saved/ItchMedia/fonts Saved/ItchMedia/cuts Saved/ItchMedia/check
cp "E:/Epic Games/UE_5.8/Engine/Content/Slate/Fonts/Roboto-Bold.ttf" Saved/ItchMedia/fonts/
```

(Run: the engine has `Roboto-Bold.ttf` in that folder.)

One shot, one piece. `-ss` is where it starts in the recording, `-t` how long:

```bash
ffmpeg -hide_banner -y -ss 00:03:12.40 -t 6 -i Saved/ItchMedia/raw/show1.mp4 \
  -vf "fps=30,scale=1920:1080:flags=lanczos,format=yuv420p,drawtext=fontfile=Saved/ItchMedia/fonts/Roboto-Bold.ttf:textfile=Saved/ItchMedia/cap/01.txt:fontsize=72:fontcolor=white:line_spacing=14:text_align=C:box=1:boxcolor=black@0.62:boxborderw=28:x=(w-text_w)/2:y=110:enable='between(t,0.3,5.7)'" \
  -af "aresample=48000,afade=t=in:d=0.06,afade=t=out:st=5.94:d=0.06" \
  -c:v libx264 -preset slow -crf 18 -profile:v high -c:a aac -b:a 192k -ac 2 \
  Saved/ItchMedia/cuts/01_midscene.mp4
```

- **Where the caption goes:** `y=110` puts it at the top, under the header line and clear of the chat panel (bottom left) and the input row (bottom). The banner (T29) also shows at the top of the stage: if a banner is up in that shot, move the caption down (`y=h*0.30`) or pick a moment without one. Check each shot's frame (5e).
- **`text_align=C`** centers each line, and needs ffmpeg 6.1 or later. If it is refused, drop it: the lines then align left inside the box.
- **The short fades** (60 ms) stop a click at each cut.
- **Name the cuts** `01_midscene`, `02_title`, `03_prep`, `04_myturn`, `05_freetalk`, `06_cut`, `07_reveal`, `08_ending`, `09_endcard` (`.mp4`), so a sorted list is the video's order. Only finished shots go in `cuts/`.
- **A shot made of two pieces** (to cut a wait out of the middle): make each piece in `Saved/ItchMedia/pieces/`, with the caption's `enable` times running on from the first piece (`enable='between(t,0,2.7)'` on the second piece, for example). Then join the pieces as in 5d, with their own list file, into `cuts/05_freetalk.mp4`.
- **Shot 2** has no caption: the same command without the `drawtext` part.

### 5d. The end card, the join and the export (not run)

The end card: a frame of the stage, darkened and blurred, with four lines of text, over 5 s of the title music. Write the lines to `cap/09a.txt` (the name) and `cap/09b.txt` (the other lines, one per line):

```bash
printf "NO HUMANS ON SET" > Saved/ItchMedia/cap/09a.txt
printf "Free for Windows on itch.io\nPlay free, via our relay, or with your own API keys\n2026 Epic AI MegaJam" > Saved/ItchMedia/cap/09b.txt
ffmpeg -hide_banner -y -loop 1 -t 5 -i Docs/ItchMedia/screenshots/01-theater-midscene.png -ss 2 -t 5 -i Saved/ItchMedia/raw/title.mp4 \
  -filter_complex "[0:v]scale=1920:1080,boxblur=14:2,eq=brightness=-0.28,format=yuv420p,fps=30,drawtext=fontfile=Saved/ItchMedia/fonts/Roboto-Bold.ttf:textfile=Saved/ItchMedia/cap/09a.txt:fontsize=120:fontcolor=white:x=(w-text_w)/2:y=330,drawtext=fontfile=Saved/ItchMedia/fonts/Roboto-Bold.ttf:textfile=Saved/ItchMedia/cap/09b.txt:fontsize=48:fontcolor=white:line_spacing=22:text_align=C:x=(w-text_w)/2:y=540[v];[1:a]aresample=48000,afade=t=in:d=0.3,afade=t=out:st=4.0:d=1.0[a]" \
  -map "[v]" -map "[a]" -t 5 -c:v libx264 -preset slow -crf 18 -profile:v high -c:a aac -b:a 192k -ac 2 \
  Saved/ItchMedia/cuts/09_endcard.mp4
```

Once the person gives the team name, put it before "2026 Epic AI MegaJam" on the last line of `09b.txt` (for example `<team>  ·  2026 Epic AI MegaJam`). Until then the card goes without it, rather than film a blank.

Join the shots in order. Every piece has the same codecs and settings, so the join copies them:

```bash
cd Saved/ItchMedia && ls cuts/*.mp4 | sort | sed "s/^/file '/; s/$/'/" > list.txt && cat list.txt && cd ../..
ffmpeg -hide_banner -y -f concat -safe 0 -i Saved/ItchMedia/list.txt -c copy Saved/ItchMedia/joined.mp4
```

The export: even out the loudness, put the index first so it starts playing at once, and write the file the task asks for:

```bash
mkdir -p Docs/ItchMedia
ffmpeg -hide_banner -y -i Saved/ItchMedia/joined.mp4 -c:v copy \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -ac 2 \
  -movflags +faststart Docs/ItchMedia/gameplay.mp4
```

At CRF 18 and 30 fps, a minute of 1080p comes to about 20 to 50 MB, under the 100 MB limit. If it goes over, encode the cuts at `-crf 21`. `.mp4` and `.png` are already LFS in `.gitattributes` (run: `grep` found `*.mp4` and `*.png`).

### 5e. Check the video (step 7; not run)

1. **Length, size, streams.** 30 to 60 s, under 100 MB, H.264 at 1920 × 1080, AAC sound:

   ```bash
   ffprobe -v error -show_entries format=duration,size -show_entries stream=index,codec_type,codec_name,profile,width,height,pix_fmt,r_frame_rate,sample_rate,channels -of default=nw=1 Docs/ItchMedia/gameplay.mp4
   ```

   Expect `codec_name=h264` with `width=1920`, `height=1080`, then `codec_name=aac` with `codec_type=audio`, a `duration` from 30 to 60, and a `size` under 104857600.
2. **One frame every 3 seconds,** and one sheet of them all, then look at each with the Read tool:

   ```bash
   ffmpeg -hide_banner -y -i Docs/ItchMedia/gameplay.mp4 -vf fps=1/3 Saved/ItchMedia/check/f_%02d.png
   ffmpeg -hide_banner -y -i Docs/ItchMedia/gameplay.mp4 -vf "fps=1/3,scale=480:-1,tile=4x5:padding=8" -frames:v 1 Saved/ItchMedia/check/sheet.png
   ```

   In each frame: no loading screen, black frame, editor window, desktop or other app; every caption reads; no key, key-screen text, relay address or personal detail.
3. **A frame from every shot** (Done-when):

   ```bash
   for f in Saved/ItchMedia/cuts/*.mp4; do n=$(basename "$f" .mp4); ffmpeg -hide_banner -y -ss 2.5 -i "$f" -frames:v 1 -update 1 "Saved/ItchMedia/check/shot_$n.png"; done
   ```

   Each one shows the game as it is now: the new cast, the card's props, the builder.
4. **Readable on a phone.** Look at the caption frames shrunk to a phone's size:

   ```bash
   ffmpeg -hide_banner -y -ss 3 -i Saved/ItchMedia/cuts/04_myturn.mp4 -frames:v 1 -vf scale=640:360 Saved/ItchMedia/check/phone_04.png
   ```

5. **No black frames and no dead air:**

   ```bash
   ffmpeg -hide_banner -i Docs/ItchMedia/gameplay.mp4 -vf "blackdetect=d=0.2:pix_th=0.08" -an -f null - 2>&1 | grep black_start
   ffmpeg -hide_banner -i Docs/ItchMedia/gameplay.mp4 -af "silencedetect=n=-45dB:d=1.5" -vn -f null - 2>&1 | grep silence_start
   ```

   Both should print nothing. A short silence in the drum roll's lead-in is fine; check what it is.
6. **The first five seconds are gameplay:** `f_01.png` (0 s) and `f_02.png` (3 s) show the stage, not a title.

Write what each check showed under "## Findings" in `T70.md`.

## 6. Hand-off (step 8)

Update "Left to do" in `Docs/Submission.md`, and the top of `Submission.md` that says it was drafted before T19 to T22:

- What T70 made: `Docs/ItchMedia/description.html`, `cover.png`, the screenshots and `gameplay.mp4`, and the new `ItchPage.md`.
- What is left for the person: upload the video (YouTube unlisted, Vimeo or itch.io's video field) and put its link in the form; upload the cover and the screenshots in their order; paste `description.html` into the page's description; fill in every **[YOU]** blank (1c); package the submission build fresh, not from the shoot build, or delete the shoot build's `Local/` folder (keys, switches, stats, `progress.json`) before zipping; answer the open questions in `Submission.md`.
- Also in `Submission.md`: bring "Before zipping" up to date for T68 (delete `Local/switches.json` too, and any `stats` file) and T61 (`Local/progress.json`); rebuild the outside-asset list from `Docs/Assets.md`; fix the line "The only AI image and 3D tools were Leonardo.ai and Meshy ... [T20: confirm once the audio is in.]" the same way as the AI disclosure (1a).

## 7. Notes for the plan (tell, don't change)

- T70's **Depends on** line names tasks that are done (T55, T72, T67, T45, T48). That's harmless. Whoever next edits the plan may drop them.
- T22 is dropped, but `T70.md` step 3 says "T22's command". The command is in CLAUDE.md and `CLAUDE.local.md` (3b).
- T68's hand-off asks T70 to set `llm.json`'s `build`, and T69's asks T70 to add its clause to the privacy line. Neither file is in T70's **Touches**: add `Content/NHOS/Data/llm.json` to it when you do the first.

## 8. What needs the person's OK, and what it costs

Ask each of these when its step comes, one at a time, with the multiple-choice tool.

| What | When | Cost |
|---|---|---|
| Install ffmpeg: `winget install --id Gyan.FFmpeg` (give the file name, the source and the size from `winget show` first) | 3e | Free. A download of some tens of MB; `winget show` gives the size |
| The capture route: **answered**, Game Bar (part 9, Q1). Only if it fails: route B needs a second install (`virtual-audio-capturer` or VB-CABLE: name, source and size first), route C a new editor task above T70 | 3f | Free, apart from the time |
| Game Bar's capture settings and HDR off, if the test clip needs them. Both are system settings the person changes | 3f, 3g | Free |
| Computer use on the game window: the person grants the app once | 3a, before the first show | Free |
| The relay shows: two or three, at most five | 3h | About $0.11 a show today (T70's entry in the plan). T58 and T76 may add 10 to 20 %. Three shows are about $0.35 to $0.45, five at most about $0.75. They count against the relay's limit of 600 calls a player a day |
| The page text (step 2), before the commit | step 2 | Free |
| Closing the editor to package the shoot build | 3b | About 6 minutes, no money |

T70 needs no paid `--ask` run, no Leonardo or Meshy credits, and no relay deploy.

## 9. Questions for my person

Decisions this sheet doesn't make. Each has its recommendation first. Q1 is answered. My person declined to answer Q2 when this prep session asked, and Q3 wasn't asked: T70 asks both again when it reaches them (Q3 before the shoot, Q2 before step 2's commit).

1. **How should the shoot record the game's sound?** This PC has no loopback device, and Unreal's submix recording needs a Blueprint change (3f). **Answer (2026-11-15): Xbox Game Bar.** T70 still records the 10-second test clip first (3g), and writes in its Findings that the capture route differs from `T70.md` step 3 on my person's call.
   - **Xbox Game Bar (recommended):** built in and already on. It records the game window's picture and only its sound in one file, and ffmpeg only cuts. No install and no editor work. It differs from `T70.md`'s plan (gdigrab), so it needs your OK.
   - **gdigrab plus a virtual loopback device:** the plan's tool, plus one more install after your OK (a capture device or VB-CABLE). It records every system sound.
   - **Unreal's submix recording:** the cleanest sound, but a new editor task above T70 and a manual sync for each show.
2. **May `description.html` use links (`<a href>`)?** Step 2's tag list leaves them out.
   - **Yes, only for the dev log and the four key consoles (recommended):** a judge can click them, and itch.io's editor keeps links.
   - **No:** write each address as plain text.
3. **Settle "SpaceXAI" or "SpaceXSI" (open question 8 in `Submission.md`) before T70 shoots?** The label is on a robot, in the log and on the cards in every screenshot and in the video, so changing it after the shoot means shooting again.
   - **Keep "SpaceXAI" (recommended):** the game, the prompts, the relay and every doc use it, and the jam page's spelling may be a typo. Check the Official Rules once.
   - **Change to "SpaceXSI":** a data change (`personas.json`'s `name`) before the shoot, then the offline check.

## 10. Where this sheet covers each step of `T70.md`

| `T70.md` | This sheet |
|---|---|
| Step 1, the description: rewrite the settings and the text, settle every **[Txx]**, list the **[YOU]** blanks at the top, credits from `Assets.md`, providers' names | 1a (what is out of date), 1b (markers), 1c (blanks), 1d (settings), 1e (outline and credits) |
| Step 2, `description.html` with plain tags; show the page text before the commit | 2, part 9 Q2, part 8 |
| Step 3, set up the shoot: a package or the game window at 1920 × 1080; switches; ffmpeg after an OK; a 10-second test clip with picture and sound (Game Bar, on my person's call); raw files in `Saved/ItchMedia/` | 3a to 3g, part 9 Q1 |
| Step 4, play and record two or three relay shows after an OK, with both endings | 3h, 3i, part 8 |
| Step 5, 5 to 8 screenshots at 1920 × 1080, named in page order; the 630 × 500 cover, with the name only if it reads at 315 × 250; update the page settings | 4a to 4e |
| Step 6, the shot list in `Submission.md`; a 45 to 60 s cut with the game's sound and burned-in captions; `gameplay.mp4`, 1920 × 1080, H.264 and AAC, under 100 MB | 5a to 5d |
| Step 7, `ffprobe` for length and sound; a frame every 3 s, looked at | 5e |
| Step 8, "Left to do" in `Submission.md` | 6 |
| Done when: the four files in `Docs/ItchMedia/`; no **[Txx]** left; every image and a frame from every shot looked at; the person approves the page text | 1b (the `grep`), 4e, 5e (2 and 3), step 2's OK in part 8 |
| "If it runs long, finish steps 1 to 5, push, and make the video its own task" | 5 stands alone: it needs only the raw recordings in `Saved/ItchMedia/raw/`, the notes file (3h) and this part |
