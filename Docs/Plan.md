# Plan: No Humans On Set

The living plan for our game: the tasks in priority order, how to run one and how to add one. The design is a private Claude Doc, linked from [GameDesign.md](GameDesign.md). Say **"Next task"** to build the next step.

In this file, "I" and "my" mean the person at the keyboard. "Claude" means the agent doing the task.

**Next up:** Since 2026-11-15 no task waits for me to play: Claude plays the shows itself (see "Claude does the playing" under "Build notes for every task"). T29 (the chat holds only chat) is done. T32 (the UI audit, `UIStyle` and the shared pieces) is done: later UI tasks style their widgets with `UIStyle` (see `Docs/tasks/T32.md`). T30 (the lines play one at a time) is done: every line plays one at a time, and `Content/NHOS/Data/pacing.json` sets the pace. The design doc stays as it is, so its Rules tab still says each turn's lines play out at once. Next in the editor: T38 (every line in a speech bubble, and the chat opens on a click) and T34 (the in-show screen); T34 starts with the vote bug T32 found (the fourth vote button votes for the third name), and T33 left it two rows (T33-1: the in-show buttons can't take keyboard focus; T33-2: the robots' tags show through full-screen panels). T33 (the title, key entry and end screens) is done: they are styled from `UIStyle` and play by keyboard. T20 (audio) is done: music, the vote's drum roll, the reveal stingers, applause and laughs, talk blips, robot sounds and button clicks, from the new `BPC_ShowAudio` component on `BP_Show`. Every one of these tasks changes `BP_Show` or `WBP_Stage`, so they go one at a time in the editor. T39 (the art batch tool) is done. T40 (the headpieces) is done. T41 (the story props) is done. T42 (the opera-house pieces) is done (90 credits, balance 60). T43 (the imports and `M_Clay`) is done: all 43 generated models are assets (`Stage/Headpieces/`, `Stage/Props/<card id>/`, `Stage/Set/`), each with its scale and yaw (90 for every Meshy model) in `Docs/PropArt/manifest.json`, and `M_Clay` with `MI_Clay_Neutral` is in `Stage/Materials/`; T45, T46, T47 and T49 build on them. The design's rules changed on 2026-11-15 (only the bots get the director's note, no decoy, a tie cuts nobody, a scene clock, no Director AI, rivals, visible passes, a last word, a 15-word cap, new end screens and a stagehand who teaches the rules); T50 to T61 build them, one task per change. T56 (the rivals) is done: each persona's prompt ends with its rival line, and `personas.json` has a `rival` field for T60. T51 (no decoy note) is done: every actor gets the same note, and each of the 10 notes has a category (Movement, Props, Looks or Speech) that T50 shows to everyone. T46 (the clay pill bots) is done, ahead of T45 on my call: every robot is a two-tone clay capsule (seat color over cream) with a curved screen face, a mouth that stretches when it talks and its old topper, and the five robots in `L_Stage` were re-placed; T47 and T49 build on it. T50 (only the bots get the director's note) is done: my seat gets no note, my card shows the note's category and a blacked-out note ("Note: ██████ (bots only)"), every AI's state carries `scene_card.note_category`, and the prompts tell the bots to follow the note subtly and name it only in Free Talk. T59 (the 15-word cap) is done: every line, mine too, is cut at 15 words (`BP_Show`'s `MaxWords`), and the relay's free mode cuts at 15 too. T49 (the clay opera house) is done: the theater is matte clay (`M_Set` gained a world-space thumbprint normal, off by default, and the set wears new `MI_Theater_*` instances), a gold chandelier hangs at the top of the house camera's frame, gold cherubs blow trumpets on plinths at the apron's corners, two tiers of horseshoe boxes sit at the frame's edges and a row of stalls fills the bottom, all holding small top-hat capsule bots (`Stage/Set/BP_AudienceBot`); the robots, places, prop table, Riser and backdrop stay clear. T53 (the scene clock) is done: a show has one scene fewer than the cast (4 with 5 actors, 3 with 4), `show.scenes` says so, a clapperboard under the header shows "SCENE 2 / 4", the banner reads "Scene 2: <title>" or "Last scene: <title>", and a new `BP_Show.LastSceneDone()` ends the show after the last scene (T52 calls it after a tie). The header still names the scene ("THE SCENE: SCENE 2, TURN 1 OF 3"); T34 can drop it. The `ai_seats` switch seats 3 AIs for a 4-actor test show. T52 (a tie cuts nobody) is done: a tie for the most votes cuts nobody, the AIs read "The vote is tied between Player 2 and Player 5, with 2 votes each. Nobody is cut.", the banner says "The vote is tied, so nobody is cut. The scene still counts.", the reactions run with no reveal, and the scene counts (the next Scene Prep, or the end after the last scene); the Director is no longer asked, so T55 can remove it. T54 (the new win condition) is done: I win at the final two or by still being on stage when the last scene ends, the bots' goal 1 says both and that a tie helps me, the banner and the end screen's subtitle say "You made the final two." or "You were still on stage when the last scene ended." under the same "YOU WIN" plate, `BP_Show` keeps `WinReason` and `WinLine` for T60, and the log prints `NHOS: SHOW END result=win reason=<final_two|last_scene>`. The title screen's How to play still says "Make it to the final two without being caught, and you win." (T33's widget, T61 replaces it). T55 (no Director AI) is done: nothing asks, pays for or mentions an AI outside the cast, the director's note keeps its name, `NHOS: CUT` no longer has a `tiebreak=` field, and free mode (in the game and the relay) has no `tiebreak` phase and reaction lines that fit a tie. The others go in this order: the audio tasks first (T71 music for each card and each part of the show, T72 a voice for each robot and mine, T73 lines that type out with one voice sound per syllable; moved to the top on my call on 2026-11-15), then T58, then T62 to T66, all before T38 and T34. T57 (silence and polish are tells) is done, ahead of the audio tasks on my call: a Free Talk pass puts "(passed)" by that actor's name over its robot in `UIStyle`'s `Quiet` lavender until its next line or the end of that Free Talk (`BP_Robot.SetPassed`, `BP_Show.PassCue`, `PassClear`, `MarkPass`, two new `RunCue` kinds), the log prints `NHOS: PASSED <id> scene=<n> round=<r>`, and the bots' rules now say silence and too-polished lines are evidence; T58's last word goes through the same `ShowLine` while `Phase` is still "free talk". Steps 1 and 2 of T71 (picking the tracks) and of T72 (making the voices) need no editor and can run as prep now. T62 to T66 (added 2026-11-15, my input spec in `Docs/tasks/T62.md`) change how I take a turn: I click to build one action and type an optional line of up to 15 words, the AIs follow the same action rules (one action a turn, throw or give only what you hold), the input LLM only fixes spelling, and a 30-second timer sends the turn. T24 (timers) and T31 (Tab completion) were dropped then: T66 and T65 take over what they did. T60 and T61 can build on T33's end and title screens. T36 (each burning bill names who it paid) is done, ahead of T34 on my call: the round medallion on every burning bill shows a badge with the initial of the provider that was paid (A, O, S, M; the companies' brand rules rule out their logos), and the input LLM's bills show Anthropic's; T34 should keep `WBP_MoneyBurn.Burn(Prov)` and `WBP_BurningBill.SetLogo` if it changes the burn. T44 (the seven film-parody cards) is done, ahead of T34 and T37 on my call: `scenes.json` holds the seven clay-era cards, each bringing four props of its own (one a spare no want needs), the `favorite_prop` note (Speech) replaces `say_chicken`, the game prompt calls the set a clay opera-house stage, and the checker has the new story terms and a per-card props check. T45 (each card's props on the prop table) is done: each scene's card puts its own four props on the prop table (`props.json`, `BP_Prop.SetProp`, `BP_StageDirector.ResetStage`, four props in `L_Stage`), and `BP_Show.StagePrep` sends them to the AIs as the state's `set.props`, so their grabs, throws and gives use them; `scenes.json` has no shared props list any more. T47 can use the card ids. T48 (the seven painted backdrops) is done: each card's backdrop id shows its own painted clay picture (`Stage/Backdrops/T_Backdrop_<id>`, from `Docs/BackdropArt/`) on the flat, as emission so the stage lights don't wash it out (`M_Backdrop`'s `Art`, `UseArt`, `ArtGlow` 4); `BP_Backdrop.ShowBackdrop` hides T17's cutouts for those ids, and an unknown id keeps the plain dark flat. T37 (error messages with a joke) is done, on the Mac and with no `BP_Show` change on my call: every error the player sees comes from `Content/NHOS/Data/errors.json` through `BPC_LLMClient.ErrorKind` and `ErrorLine`, and a failed actor reply puts a backstage note on the banner (once per lab per scene) straight from the client through `BPC_LinePlayer.Cue`. The `error_test` switch fakes each failure in Test for Free. The banner holds a note only 3.5 s (`WBP_Stage.NextBanner`); T34 can lengthen it for long lines. T79 and T80 (added 2026-11-15, the cast I chose in `Docs/BotArt.md`) replace T46's pill bots: one round head shared by OpenAI, Anthropic and SpaceXAI, with sockets for props and headpieces, then Meta's doll-like android and my cardboard costume. They touch `BP_Robot` and `L_Stage`, not `BP_Show`, so they belong to the non-chain machine; T47 and T75 now build on them. T72 (a voice for each robot, and mine) is done: each provider has its own set of 10 or 11 gibberish syllables made by `Tools/make_voices.py` (a bright chirp for OpenAI, a warm round vowel for Anthropic, a bit-crushed buzz for SpaceXAI, a low wobbly drone for Meta), my own set is 12 clips of my recorded robot impression, and `BPC_ShowAudio.Syllable(Name, IsMe)` plays one from the speaker's set, never the same twice in a row, at a slightly random pitch; T73 calls it. T67 (analytics, part 1) is done: the live relay takes `POST /event` (nine allowed events, 500 a day per address, test events counted apart) and keeps them in a new `Stats` store, and `python Tools/analytics_report.py` prints the report with the `STATS_KEY` from `Local/stats.json` (copy that file to each machine that runs it; `ignore_players` there leaves our own machines out). T68 and T69 can send to it; on my call, only packaged builds count, never the editor. T71 (music for each place and each scene) is done: each of the seven cards has its own Kenney loop from Scene Prep through its turns (scene 1 too), Free Talk, The Cut and the end screen (a win and a loss) have their own, the Cut loop drops to 40% under the drum roll and stops at the reveal or a tie, and the loops cross-fade over 1 s (`BPC_ShowAudio.TrackFor`, `PhaseKey`, `PlayPhase`, `StopMusic`, `DuckMusic`, `EndMusic`; `BP_Show.OpenPrep` starts the card's loop). T73 (lines type out, one voice sound per syllable) is done: every line's name and action show at once and its speech types out at 30 letters a second in a box already at its full size, with one `Syllable` sound per syllable (at most 12 a second) and short pauses after punctuation, then T30's hold, retuned so scene 1 takes about as long as before (167 s against 170 s); T20's per-line blip is gone (`BP_Show.LineBlip`, `BPC_ShowAudio.Blip`). The design doc's Art Inspiration tab (the Chat row) now says how a line types out. `BPC_LinePlayer.PlayCur` is where T38's bubble and T77's emote hook in, right after `StartType`. T79 (the new cast, part 1) is done: OpenAI, Anthropic and SpaceXAI wear one round head on their own bodies (a hovering teardrop in a sweater, a round body with gold glasses, a lime body on springs), every robot has `HeadSocket`, `BackSocket` and `HandSocket`, and the face parts sit on a `Face` group; T80 (Meta's android and my costume) is done: Meta is a doll-like android with gold eyes behind black wayfarers, a blue tee and a gold chain, my robot is a person in a teal cardboard costume (box head with eye slots and real eyes, a ping-pong ball antenna, the scarf, striped sleeves, jeans), and their `HeadSocket`s (Meta (0, 0, 158) at 0.9, my box (−2, 0, 162) at 1.1) fit T47's headpieces; T47 and T75 are next on the Mac, and T75 should read T79's note on the arm roll signs. T58 (the last word) is done: after the final Free Talk round, every actor on stage that someone else named with @ in it gets one reply before the vote, one at a time in a random order, under the header "LAST WORD: SCENE n" (`BP_Show.StartLastWords`, `NextLastWord`, `EndLastWords`); a mention of a cut actor or inside a last word gives nothing, my own last word opens the input row and goes through the input step (`autoplay.json`'s `last_word` list in autoplay), the shared log's `when` is "scene n, last word", the bots answer the new `asks.last_word`, and the log prints `NHOS: LASTWORDS scene=<n> named=<ids|none>`, `NHOS: LASTWORD <id>` and `NHOS: LASTWORDS DONE`. Free mode (the game and the relay) has a `last_word` phase, and two of its Free Talk lines open with an @ mention. T62 (one rule set for every action) is done: every actor, mine included, takes at most one action a scene turn and none in a reaction; a grab takes only a prop nobody holds, a throw or give needs a prop the actor holds, a give goes only to an actor, a move only to a place, a look may take a prop, and nobody holds more than two props. One check serves everyone (`BP_StageDirector.CanDo`, with `ItemsFor` and `TargetsFor` for T64), run when each line enters the shared log (`BP_Show.CheckTurn`), so a broken rule is logged as "looks around"; who holds what is game state in the director, and every AI reads `holding` in each cast entry and in `you`. Seven card wants and one note were reworded to fit, and the design doc (Rules, Bot Prompts, Turn Input, Stories) says the same. T62 also fixed every card prop being invisible in shows (`L_Stage` had saved `BP_Prop.PropsLoaded` set; `LoadProps` now always reads `props.json`). T63 (my turn sends a built action and a spoken line) is done: `BP_Show.SendHumanTurn(Verb, Item, Target, Line)` sends my scene turn, the action pre-checked with `CanDo` and written into the shared log like an AI's with no LLM, and every line of mine (scene turn, Free Talk, last word, reaction, vote reason) goes through the input LLM for spelling only, under `spelling_wait` seconds from the new `input.json` (4), or as typed when that call is off, fails or is late (`NHOS: SPELLING skipped <why>`); each scene turn prints `NHOS: HUMAN <verb> <item> <target> says=<line>`, the input box sends its text with Verb none until T64's builder, and autoplay picks a random allowed action. The design doc's Bot Prompts tab has the new "Input LLM prompt" section. T64 (the action builder) is done: in each of my scene turns an action builder sits above the input box (a mono preview line such as `> throw cannoli tray at @Meta: "Oops, my servo slipped."`, the seven actions with the ones that have no valid choice greyed and a tip on hover, and the picked action's chips from T62's rules), the old Send is Action!, Action! and Enter send the built action through `HandleSend` → `WBP_Stage.TakeAction` → `SendHumanTurn` and refuse an unfinished one, no button or chip takes the keyboard focus, and the turn line and hint point at the builder; its notes for T65, T66, T34 and T61 are in `Docs/tasks/T64.md` ("Knock-on notes"). T65 (the speech field) is done: a live word counter ("12/15", a red pill at 15) sits right of the input box, a 16th word is refused and a paste is cut to 15, the box keeps the keyboard focus after any click in the game window, typing "@" opens a list of the actors still on stage over the box (letters filter it; Up, Down, Enter, Tab, a click or Esc), a picked name goes in as "@Meta " (one Backspace removes it) and every mention is a chip in its seat color in the builder's preview line (`WBP_Word`); its notes for T66, T61 and T34 are in `Docs/tasks/T65.md` ("For later tasks"), the first being that the row is cramped at 640 wide. T66 (the turn timer) is done: each scene turn has 30 seconds and sends itself as it stands (an unfinished action as a look around), a last word and a reaction have 15 (an empty field is a pass), Free Talk and the vote have none, autoplay never waits, and no time reaches the AIs (`input.json` `timers`, `WBP_Stage.TickTimer`, `BP_Show.TimerFor`); its notes for T77, T78, T84, T34 and T61 are in `Docs/tasks/T66.md` ("For later tasks"); the design doc's Rules and Turn Input tabs say the same. T77 (the faces as lines play) is done: each reply's emotion rides on its shared-log entry as `feels` (the word from `emotes.json`, none for neutral), the seat's robot shows it as the line starts to type (`BP_Show.StageLine` calls `BP_Robot.Emote`), and my emotion is the input LLM's pick, or `free_mode.json` `emotion_keywords` when that call is skipped, fails or gives none; every line of mine goes through `BP_Show.HumanFeels`, where T78's pick goes. T78 (I can pick my robot's emotion) is done: a Face chip after Show chat in the input row reads "Face: Auto" or the picked emotion (in paper) and opens a list of the emotions in `emotes.json` (`WBP_Stage.SyncFace`, `FaceShow`; the pick and the list's chips in `WBP_ActionBuilder`); a pick goes with my next send only, a pass and a timeout too, and prints `NHOS: HUMAN emotion=<id> from=pick` (`BP_Show.TakeFace`, `ApplyFace`); the chip goes back to Auto at each of my turns and hides in the vote and in Scene Prep. The design doc's Turn Input tab now has the chip. Its notes for T34 (in a reaction the speech field is only 265 wide), T84, T85 and T61 are in `Docs/tasks/T78.md`. Next in the editor: T88. T60 (the end screens) is done: every vote names its tell (`llm.json` reply_schema `tell`, `tells.json`), the lose screen shows the top reason in large gold under the cards (`BP_Show.TopLine`, which T61's earpiece can say), and the win screen shows each AI's rival on its card, with "(not in this show)" when the rival has no seat. T47 (a headpiece for each role) is done, with no `BP_Show` change on my call: each seat in `scenes.json` names a headpiece and a color, `Content/NHOS/Data/costumes.json` holds the 14 headpieces' meshes and fits, and each robot takes its headpiece off at Scene Prep and puts on its seat's when the scene starts by watching `BP_Show`'s `SceneNum` and `Phase` itself (`BP_Robot.WatchShow`, `DressFromShow`, `SetHeadpiece`); a cut robot keeps its own. A task that renames `BP_Show`'s `SceneNum`, `Phase`, `Robots`, `SeatRole`, `CardId` or `CardArr` must update those two functions. T75 builds on `BP_Robot` next. New since 2026-11-15, as soon as possible on my call: the cast in Hyper3D (T81 to T83). T81 generates the models from the concept art with no editor, on the Mac, where the `hyper3d` MCP server is set up; T82 and T83 swap them into `BP_Robot` after T75. T61's new pieces are done on the Mac (a second editor, from a worktree): `stagehand.json`, `BPC_Stagehand`, `WBP_Earpiece` with the friendly AI stagehand's portrait, and `WBP_HowToPlay`; the PC's chain only has to call them (T61.md, "Part 1"). T81 (the cast in Hyper3D, part 1) is done and checked: all 13 parts are in `Docs/CastArt/` (a shared head shell with no ear pods or collar so it takes each seat color, a body and one arm per bot that the engine mirrors, Meta's head, my box head and box body), with their logs and `Assets.md` rows; T82 and T83 start from them once T75 is done. T82 (the cast in Hyper3D, part 2) is done: OpenAI, Anthropic and SpaceXAI wear the Hyper3D head shell, bodies and arms on the textured `M_CastModel` (`RShell`, `OModel`, `AModel`, `SModel`, `OArmXL`/`R`, `AArmXL`/`R`, `SArmXL`/`R`, all tagged `seat`), T79's engine shapes for them are deleted, `Visor` and `Face` sit 5 cm back and 4 cm down in the model's screen recess, and T83 does Meta and my robot the same way (its notes are in `Docs/tasks/T82.md`, "For T83"). T75 (each robot can show an emotion) is done: `BP_Robot.Emote(Emotion)` (one String, an id from the new `Content/NHOS/Data/emotes.json`) poses each robot's own face and plays a gesture, `"emote_test": true` cycles every emotion on every robot, and T76 to T78 build on it; T82 and T83 must keep `Face` and its parts and update `FaceParts` and `FaceRest` if the models replace the screen or the shell (`Docs/tasks/T75.md`, "For later tasks"). T83 (the cast in Hyper3D, part 3) is done: Meta wears the Hyper3D body and jointed doll arms with T80's own round doll head (the Hyper3D mannequin head read further from meta.png, so it is imported but unused), and my robot wears the Hyper3D box head, body box and striped arms, with my eyes behind the model's slots and the dark shades moved down on my box (`costumes.json`'s `on`); T80's 45 engine shapes they replace are deleted, and T38's `BP_Robot` part can start. T75 (each robot can show an emotion) is done: `BP_Robot.Emote(Emotion)` (one String, an id from the new `Content/NHOS/Data/emotes.json`) poses each robot's own face and plays a gesture, `"emote_test": true` cycles every emotion on every robot, and T76 to T78 build on it; T82 and T83 must keep `Face` and its parts and update `FaceParts` and `FaceRest` if the models replace the screen or the shell (`Docs/tasks/T75.md`, "For later tasks"). T74 (re-shooting the design doc's pictures) was dropped on my call on 2026-11-15: it changed no gameplay. T70 (the itch.io page) was dropped on my call on 2026-11-15 too: the jam is over. T68 (analytics, part 2) is done: a packaged build sends T67's relay anonymous events (`launch`, `mode`, `show_start`, a `phase` as each phase shows, `calls` per provider and model at each Scene Prep and the end, `error`, `show_end`) from `BPC_Analytics` on `BP_Show` (`Analytics`), with a player id in `SG_Player`; the editor sends only with `"analytics": "test"` in `Local/switches.json` (keep it `"off"`), and the title's Play stats button turns it off. T69 calls `BPC_Analytics.Send` and reads `CurPhase`; a task that renames a phase header must change `BPC_Analytics.PhaseKey` too. T69 (analytics, part 3) is done: the input LLM's reply has its own schema, `llm.json`'s `input_schema` (`reply_schema` plus `attempt`, and T76's `emotion`), a typed stage direction sends its few words as an `unsupported` event (`BPC_Analytics.Unsupported`), and so does a click on a greyed action in the builder (`WBP_ActionBuilder.OnPreviewMouseButtonDown`, once per verb per turn); on my call it closed without the report run. A task that rewords a builder tip in `WhyNot` must change `WBP_ActionBuilder.BlockWords` too. T76 (the bots send an emotion with every reply) is done: every reply in both schemas (`llm.json` `reply_schema` and T69's `input_schema`) now carries a required `emotion`, one id from `emotes.json`, the last line of `prompts.json` `base` (word for word from the Bot Prompts tab) asks every bot for the face it acts, and the relay's free mode picks one by weight from each phase's new `emotions` list in `free_mode.json` (`neutral` for the input step) and now also sends T60's `tell`. The game reads no new field yet; T77 plays the emotion on the robots, and `BPC_LLMClient.FreeReply` should pick from the same lists. T88 (added on my call on 2026-11-15) makes the director's note clue change each scene, drawn from twelve kinds (the category, the vowels only, a riddle and more); it changes `BP_Show` and `WBP_Stage`, so it goes to the chain machine after T78, and T84, T34 and T61 build on it. T38 (every line in a speech bubble, and the chat opens on a click) is done: each line plays in a bubble over its speaker (`WBP_SpeechBubble`, `BP_Robot.Say`, `Typing`, `Hush`, called from `BPC_LinePlayer.PlayCur`), typed out with the chat line, with three dots before an AI's line in Free Talk and the reactions and the cut robot's last words over where it fell; the chat is hidden at each show's start behind a Show chat / Hide chat button at the left end of the input row (`WBP_Stage.ShowChat`, `ChatButton`); the lower panel is 1080 wide in every phase on my call; the design doc's Art Inspiration tab has the bubble and the hidden chat. The closing check fixed the cut robot's last words at normal pace (`BPC_LinePlayer.QPhase`, the phase the line queue is playing). Its notes for T84 and T34 are in `Docs/tasks/T38.md` ("For later tasks"): a bubble covers the name tags beside it, and `BPC_LinePlayer.BubbleKeep` walks from `TurnText`, `MeText` and `LowerSize`. T86 (a full house) is done: three raked rows of stalls behind T49's row (33 seats, 30 bots) and four more bots in T49's row fill the bottom of the house camera's frame at 1600 × 900 and 1440 × 900, the near rows dim on their own lighting channel with a faint glow that can't reach the stage; the design doc's Art Inspiration tab now has the stalls, and a free autoplay show in a game window on the saved assets reached `SHOW END` with the house in, so T34 judges the screen with the full house. T89 (added 2026-11-15 on my call) makes each push to `noHumansOnSet` that changes the game build a Windows build on this PC and push it to the itch.io page with butler, as a second file marked post-jam. The jam's file stays as it is. T89 needs no editor and changes no asset, so it can run beside the chain. T90 (added 2026-11-15 on my call) copies the design doc into the repo as Markdown files in `Docs/Design/`, makes them the only source of truth and removes every link to the Claude Doc. It needs no editor, so it can run beside the chain too. T88, T84, T85, T87 and T61 wait for it, because each of them edits the design doc.

## Goal

Finish **No Humans On Set**. The "Open" tasks below are what we know is still to do. I add tasks as the game needs them, and a new task goes wherever it belongs in that list (see "Changing the plan").

**How the plan began.** It started as the plan for an MVP (T01 to T12), which had to answer one question as fast as possible: is it fun to fool an all-AI cast, and do the AIs catch a human at a fair rate (not every time, not never)? The gate (T12, 2026-11-14) said go. I liked it. Since then the plan covers the whole game. Until 2026-11-14 this file was `Docs/MVPPlan.md`. Finished tasks' files and older notes in `Agents/` still use that name. Until 2026-11-14 this file also held every task's full text and a Findings section; since then each task has its own file in `Docs/tasks/` (see "Tasks").

## Cut order

If I decide to cut scope, cut in this order: T38 (speech bubbles; the chat stays as it is now, and T34 polishes that), then T19 to Move and Look only, then T20 to music and three sounds, then T17's robot motion.

## How to run a task

When I say **"Next task"** or **"Next ask"**:

1. `git pull` (if the branch is not on the remote yet, say so and go on). Read `Agents/`. Open this file and run `git lfs locks`. Take the first task in "Open" that is free (see "Claiming a task") and whose **Depends on** tasks are all checked, or wait only for my check (see "When only my check is left"). Then read the task's file, `Docs/tasks/Txx.md` (its **Details** link): it holds the Why, the Steps, the Done-when check and what earlier work found. Read another task's file only when yours points to it.
2. Tell me the task and its recommended model and effort. If this session runs a different model, say so and ask whether to go on.
3. Check its Needs. If something is missing (for example, Unreal MCP is not connected), tell me what to do and stop.
4. Claim the task (see "Claiming a task"). Write a status file, `Agents/status/task-T07.md`, and lock assets as `Agents/README.md` says.
5. Do the work, then run the Done-when check. If the check fails, do not mark the task done: write what blocks it under the task's entry in this file (a `Blocked:` line, never only in the task's file) and tell me. If the only part of the check left is mine (my verdict, my OK on a doc edit, or a run that needs something from me), follow "When only my check is left" instead of step 6.
6. Make one commit that holds the work; the task's entry in this file with its box checked, moved to the end of "Done" and cut down to its title line and its **Details** line; the task's file with the lines cut from the entry (**Model and effort**, **Depends on**, **Needs**, **Touches**) moved to the top of its "## Task" section, the line under its title changed to say the task is done, a **Result:** line at the end of "## Task", and what the task found under "## Findings" at the end of the file; and the updated "Next up" line. Message: `T07: <title>`. Then push it with `git push`. You don't need to ask. If the push is rejected, don't pull or rebase while other sessions have uncommitted work in this folder; tell me.
7. Delete the status file. Once the commit that checks the box is pushed, release the claim. Unlock the assets the task changed too, unless another running session still has uncommitted changes in them (`git status`, `Agents/status/`). End by naming the next task with its model and effort, so I can switch before I send "Next task".

## Claiming a task

A claim is an LFS lock on the task's claim file. Everyone sees it at once, on every machine, with no push.

- **Claim:** `git lfs lock Docs/claims/T07`
- **See all claims:** `git lfs locks`
- **Release:** `git lfs unlock Docs/claims/T07`, after the commit that checks the task's box is pushed. Until the push, other machines see neither the work nor the checked box, so the lock is what tells them the task is taken. A task that waits for my verdict or OK keeps its claim until its box is checked. Whoever pushes releases the claims of every checked task that went up.
- A task is free when its box is unchecked here, it has no `Waiting:` line, and `git lfs locks` shows no lock on its claim file.
- If the lock fails because a teammate holds it, take the next free task.
- If my own account holds the lock on an unchecked task and there is no status file for it in `Agents/status/`, an earlier session may have stopped halfway. Ask me before taking it.
- If you stop without finishing, add a `Blocked:` line under the task and commit it as `Plan: T07 blocked`. Release the claim only if someone else should take the task.

Never edit the claim files. They exist only to be locked.

## When only my check is left

Some tasks end with my verdict, my OK on a doc edit, or a run that needs something from me. A playtest is never one of them: Claude plays the shows itself (see "Claude does the playing" under "Build notes for every task"). The next task doesn't wait for my check:

1. **Push the work first.** When the work is built and the Done-when check passes except for the part only I can do, commit and push now. The commit holds the work, its `Graphs/` files, the task's file with what it found so far, a `Waiting:` line under the task's entry in this file (it ends `Left: <what I must do>`) and the "Next up" line. Message: `Txx: <title> (waits for <what>)`. The box stays unchecked.
2. **Free what you hold.** Unlock the assets the task changed, keep the claim, and set the `Editor:` line in your status file to `not using`. Keep the status file: it says what you wait for.
3. **The next task can start.** A task may start when each task in its **Depends on** line is checked, or has its work pushed with a `Waiting:` line that leaves only my check. It builds on that work as pushed.
4. **If my check passes,** make the closing commit as step 6 of "How to run a task" says: check the box, remove the `Waiting:` line, move the entry to "Done", and add the Result and the findings. Message: `Txx: <title> (checked)`. Push it, release the claim and delete the status file.
5. **If my check finds a problem,** the fix goes first in the editor lane, but only once no running session holds the task's assets (`git lfs locks`, `Agents/status/`). Until then, tell me, and wait. When they are free, lock them again, fix the problem, push with the `Waiting:` line kept. Tell me what the fix changed, so that later tasks that built on your work can check it.

## Changing the plan

I add tasks as the game needs them, and a task can go anywhere in the list. Every change to the plan outside a task's own commit is a commit too, `Plan: <what changed>`. One example is a verdict that changes the design.

To add a task:

1. **Number it.** Take the highest number in `Docs/claims/` plus one. A number is only a name: it says nothing about order. Never renumber a task, and never reuse a number.
2. **Place it.** "Open" is in priority order, and "Next task" takes from the top. Two things decide where the task goes:
   - **Architecture:** it goes below every task it builds on, and above the tasks that build on it. Name the first kind in its **Depends on** line, and add it to the **Depends on** line of each task of the second kind.
   - **Priority:** among tasks that don't depend on each other, the one that matters more for the finished game goes higher.
3. **Write it** like the other open tasks, in two places. In this file, under "Open": the title line, then **Model and effort**, **Depends on**, **Needs**, **Touches** and **Details** (a link to its file). In a new file, `Docs/tasks/Txx.md`: a `# Txx Title` heading, the line back to the plan, then "## Task" with **Why** (if there is one), **Steps** and **Done when**. A task fits in one session and one commit, so split a bigger one.
4. **Add its claim file,** `Docs/claims/Txx`, with the same two lines as the other claim files and the new number.
5. **Commit** the plan, the task's file and the claim file together as `Plan: add Txx <title>`. Update "Next up" if the new task changes what is next.

To move a task, cut its entry in this file and paste it at its new place. Its number and its file stay. To drop a task, delete its entry and its file, and say why in the commit message. Its claim file stays, so that the number is never used again. To change a task's steps, edit its file; to change its **Depends on**, **Needs** or **Touches**, edit its entry here.

**Keep the form.** Every task is an entry here plus a file, `Docs/tasks/Txx.md`. An open task's entry holds its title line and the short lines that other readers need (**Model and effort**, **Depends on**, **Needs**, **Touches**, any **Waiting:** or **Blocked:** line, and **Details**); its file holds the rest. A done task's entry holds only its checked title line and its **Details** line; its file holds everything else, its findings included. Findings that belong to no one task are in `Docs/tasks/Background.md`. The task-list pane (`Tools/ClaudeMods/task-list`) reads only this file, never the task files, and lists the tasks in this file's order. It finds a task only under `## Tasks`, as a line that starts `- [ ] **Txx Title**`, or `- [x]` when the task is done. It reads the boxes, not the "Open" and "Done" headings. Under a task, it reads these indented lines:

- `- **Depends on:**` and the task numbers in it. A task that waits for an unfinished one shows as "after Txx".
- `- **Waiting:**` on a task whose work is committed but still needs me. End the line with `Left: <what I must do>`, because that is the part the pane shows.
- `- **Blocked:**` with what blocks the task.

## Model and effort rubric

- **Opus 5.5, high:** the spike, architecture, AI prompt design, Blueprint systems with many parts, debugging.
- **Sonnet 5.5, medium:** well-specified Blueprint or UMG work that follows a pattern already in the project.
- **Haiku 5.5, low:** docs, config and small mechanical edits.
- **Since 2026-11-14, every task runs on Opus 5.5 at xhigh**, whatever its own "Model and effort" line says. That is my choice. Never use **max**.
- Start a session for any work that conflicts with no running session, rather than leave it waiting (see `Docs/LaunchAgents.md`, step 3).

## Build notes for every task

These hold for every task, and for editor work outside the task list too. If one changes, change it here in a `Plan:` commit.

- **Blueprint-only.** No C++ unless the spikes show it is needed. The choice goes in `Agents/decisions/`.
- **Where things live.** Assets go under `Content/NHOS/` (`Maps/`, `Core/`, `UI/`, and `Stage/` for the 3D set from T11 on). Files the game reads at runtime go in `Content/NHOS/Data/` as `.json`. The API key and local switches go in `Local/` in the project root, which git ignores. The key file is `Local/llm_key.json`; copy it from `Docs/llm_key.example.json`. Blueprint reads it at `Get Project Directory` + `Local/llm_key.json`.
- **API keys never go in git, and never into chat.** I paste my key into the key file myself.
- **Prompts are files, not Blueprint strings.** The opening game prompt, the base prompt, the personas, the input LLM prompt and the scene cards live in `Content/NHOS/Data/`, so they diff in git. Store long text as an array of lines.
- **One provider.** All calls go to the Claude Messages API. The model, effort and token limit for each role (actor, input LLM) are values in `Content/NHOS/Data/llm.json`. T01 and T02 ran `claude-opus-5-5` at low effort. Since 2026-11-13 every role runs `claude-haiku-5-5` at low effort, the cheapest model at its lowest level. Haiku 5.5 has no server-side fallback, so `beta` and `fallbacks` in `llm.json` are empty; a refusal comes back as `stop_reason: "refusal"`.
- **One provider per persona, from T16 and T18 on.** Each persona runs on its own provider, as in the design's table, with a key per provider (no router). T16 sets up the prompts and the keys; T18 makes the game call them. Since 2026-11-14 each bot goes by its provider's name on screen, in the log and in the cast list the AIs read (OpenAI, Anthropic, SpaceXAI, Meta: the `name` fields in `personas.json`), not by a persona name such as "The Worrier". Persona ids (`worrier`) stay as they are in files and `NHOS:` lines. Real people's names and product names stay out of prompts and off the screen.
- **The design doc follows the game.** The Claude Doc is the only source of truth for the design, and the repo keeps no copy of it: [GameDesign.md](GameDesign.md) only links it. When a task changes the design (the speech style, the sets, the providers), it shows me the matching edit to the Claude Doc, and after my OK it makes the edit with the Claude Docs connector. A prompt changes in the doc's Bot Prompts tab first, then word for word in `prompts.json` or `personas.json`. No script checks the two against each other.
- **Legibility first.** Everything an AI says reads like a normal chat, the way Claude or ChatGPT write: plain sentences, no brackets or tags, no beeps or sound effects, no emoji, no ALL-CAPS words. Each persona's personality comes through what it says, not how it is typed.
- **Outside and generated assets.** Record every art, audio or font asset in `Docs/Assets.md` when you add it: what it is, where it came from (a Fab link, a site, or the AI tool and prompt) and its license.
- **One reply shape.** Every ask (scene turn, Free Talk line, vote, reaction, closing line, input conversion) gets back the same small JSON object, with unused fields empty. One parser serves the whole game.
- **The shared log** is what the AIs read. Every actor's lines have the same form, human or AI. It never holds my raw input, times, errors or anyone's note. Game messages reach the AIs in a separate field that actors can't write to.
- **Check lines.** Anything a Done-when check reads is printed with the prefix `NHOS:` to the editor log (`Saved/Logs/AIMegaJam2026.log`). It never goes in the shared log.
- **Autoplay.** From T07 on, a local switch makes the human seat play canned lines, so an agent can run a whole show unattended and read the result in the log. The switch file is `Local/switches.json` (copy `Docs/switches.example.json`), with `"autoplay": true`. The canned lines are in `Content/NHOS/Data/autoplay.json`, one list per phase, and they go through the input LLM like typed lines. Later switches (such as T09's `force_tie`) go in the same file. Set autoplay back to `false` before a person plays.
- **Unreal MCP.** Do editor work through Unreal MCP. One call at a time, each short enough that the client doesn't stop waiting. Split long work, and save after each step. Write graphs with `BlueprintTools.write_graph_dsl`, and batch calls with `ProgrammaticToolset.execute_tool_script`. Read "T01: spike results" in [Docs/tasks/T01.md](tasks/T01.md) first: it lists the DSL rules that cost time to find. Later tasks' files add more, each under "Unreal MCP rules found in this task". MCP can't create a level, so a person makes new levels in the editor (File > New Level > Empty Level).
- **Read only the graphs you need.** List a Blueprint's graphs, then read only the ones the task changes or calls. Never dump every graph of `BP_Show`: a full dump in T18 and T26 was a very large read, and one was too big for a tool result.
- **Graph sources live in `Graphs/`.** `Graphs/<Blueprint>/<Graph>.txt` holds the DSL source last written to each graph, one file per graph, as written (shorthand, before `Tools/dslpp.py`). To change a graph, start from its file and push it. If it has no file yet, read the graph from the editor and write your source from that. Commit the updated files with the task. A read-back is for reading only, because writing one back drops data (T06). If you change a graph some other way, like a pin value or a hand edit in the editor, make the same change in its file, or delete the file. The per-task copies in `Saved/Txx/src/` from before 2026-11-14 may be out of date.
- **Worktrees, for sessions that don't need the editor.** The editor has the repo folder open, so a session that drives the editor or runs PIE works there. A session that doesn't need the editor may work in its own git worktree, on its own branch, when its files could clash with another session's uncommitted work in the repo folder (for example `Content/NHOS/Data/*.json` or `Docs/`).
  - Never change a `.uasset` or `.umap` in a worktree, because binary assets can't be merged.
  - A worktree has no `Local/` folder, and nothing gets copied into it, the key file least of all. Run `Tools/check_prompts.py` there with `--offline`, `--free` or `--relay`. A run that calls the providers with direct keys waits until after the merge, in the repo folder.
  - When the work is committed, merge `noHumansOnSet` into your branch and fix any conflicts there. Then merge your branch into the repo folder with `git -C <repo folder> merge --no-ff <branch>`, and push. If that merge stops because it would overwrite uncommitted changes in the repo folder, leave it and tell me.
- **New systems get their own Blueprint.** Put new logic in a new Blueprint or component, or in the actor it belongs to (such as `BP_Robot`), and have `BP_Show` call it from one node. Every editor task so far has needed the `BP_Show` lock.
- **Claude does the playing; I don't playtest (since 2026-11-15).** No task waits for me to play, and no session asks me to. Where a check needs a show played, Claude plays it: one show by hand in PIE (Test for Free, a 1600 × 900 floating window, clicks and typing through the Slate inspector, autoplay off) with a screenshot of each phase the task changed, and a free autoplay show in a game window on the saved assets that reaches `SHOW END`. Claude judges what my playtest used to judge (can I read it, can I follow it, does the screen feel blocked, does it look finished) from those screenshots, as a critical first-time player would, and writes what it saw under "## Findings". What screenshots can't show (sound, for example) is written there as unchecked, and the task still closes. Set `autoplay` back to false and close each game window when done. T27's findings in [Docs/tasks/T27.md](tasks/T27.md) have the Mac command, the Mac log paths and how to screenshot a game window.
- **Each task leaves the game runnable.** One task = one session = one commit (two when it waits for my check).

## Tasks

"Open" holds the tasks still to do, in priority order: "Next task" takes the first free one from the top. A new task goes wherever it belongs in that order, so the numbers are not in order. "Done" holds the finished tasks, oldest first. When a task's box is checked, its entry moves to the end of "Done" (see "How to run a task", step 6). Each entry links its file in `Docs/tasks/`, which holds the task's Why, Steps, Done-when check, Result and findings.

### Open


- [ ] **T90 The design doc moves into the repo as Markdown files**
  - **Model and effort:** Opus 5.5, high. A word-for-word copy of every tab, with its tables and pictures, checked against the doc by a diff; then every pointer to the doc rewritten. A dropped line is easy to miss.
  - **Depends on:** none. It needs no editor and changes no asset, so it can run beside the chain, in its own worktree (see the "Worktrees" build note).
  - **Needs:** the Claude Docs connector, to read the doc (the doc is edited only in T90's step 7, with my OK); no session editing the doc while T90 copies it (`Agents/status/`); my answers on the doc's open suggestions and comments; my OK on the retirement line in step 7.
  - **Touches:** new `Docs/Design/` (one `.md` per tab, and `images/`), `Docs/GameDesign.md` (becomes the index), `CLAUDE.md`, `README.md`, `Docs/Plan.md` (the build note "The design doc follows the game"), `Docs/UIStyle.md`, `Docs/tasks/T25.md` (its link), `Content/NHOS/Data/personas.json` and `prompts.json` (`_readme` only), `Docs/Submission.md` if it describes how we work now, the open tasks' files and build sheets that say to use the connector (T88, T84, T85, T87, T61, T34), a new note in `Agents/messages/`, `Docs/tasks/T90.md`; outside the repo: my memory notes that point at the Claude Doc.
  - **Details:** [Docs/tasks/T90.md](tasks/T90.md)

- [ ] **T88 The director's note clue changes each scene**
  - **Model and effort:** Opus 5.5, high. A new component that builds twelve kinds of clue, the bots told which one I got, my card, and 50 new note fields. Big for one task: on my call it is one task, not two.
  - **Depends on:** T50 (the note box on my card, `scene_card.note_category` and the doc's note lines), T51 (the 10 notes and their categories), T53 (a show's scene count, which the draw covers with no repeat), T60 (`tells.json`'s `note` tell, which names the category), T90 (its design doc edits go in the files in `Docs/Design/`)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, the relay for a `--relay --free` check and one relay show that Claude plays by hand, my answer on scene 1's clue, my OK on the design doc edit (Rules and Bot Prompts), my OK on the 50 new note fields, my pick of an emoji fallback if the UI font draws no emoji.
  - **Touches:** new `Content/NHOS/Core/BPC_NoteClue.uasset`, `Content/NHOS/Core/BP_Show.uasset` (`ScenePrep`, `ActorState`, `ShowPrep`, `PrepPrompt`'s turn line), `Content/NHOS/UI/WBP_Stage.uasset` (my card's note box), new `Content/NHOS/Data/clues.json`, `Content/NHOS/Data/scenes.json` (each note's `key`, `emoji`, `opposite`, `riddle`, `autocorrect`), `Content/NHOS/Data/prompts.json` (`game`, `_readme`), `Content/NHOS/Data/tells.json` (the `note` tell), `Content/NHOS/Data/stagehand.json` (the category line), an emoji font or icon set with its `Docs/Assets.md` row if one is needed, `Tools/check_prompts.py`, `Docs/switches.example.json`, `Docs/ItchPage.md`, the design doc, `Graphs/` files for the graphs it writes, `Docs/tasks/T88.md`.
  - **Details:** [Docs/tasks/T88.md](tasks/T88.md)

- [ ] **T84 Scene Prep shows the scene and Start the scene in the middle**
  - **Model and effort:** Opus 5.5, high. A layout change across Scene Prep's widgets, judged from screenshots at two sizes.
  - **Depends on:** T38 (the chat hidden at each show's start and its Show chat button: this task decides what the lower panel shows in scene 1's Scene Prep; if T38 is cut, take it off this line), T78 (the lower panel's width, which the middle panel must clear in scenes 2 on), T88 (the clue rows in the card's note box, and `PrepPrompt`'s turn line), T90 (its design doc edit goes in the files in `Docs/Design/`)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, my OK on the design doc edit.
  - **Touches:** `Content/NHOS/UI/WBP_Stage.uasset` (a new prep panel with `PrepBox`'s scene and stage parts, `StartButton` moved into it, the lower panel hidden in scene 1's Scene Prep, `SetPrepMode`), `Content/NHOS/Core/BP_Show.uasset` (`PrepPrompt`'s turn line), `Graphs/WBP_Stage/SetPrepMode.txt`, `Graphs/BP_Show/PrepPrompt.txt`, `Docs/tasks/T32.md` (row 13), `Docs/tasks/T84.md`.
  - **Details:** [Docs/tasks/T84.md](tasks/T84.md)

- [ ] **T85 The cast's roles and wants show when I point at a robot**
  - **Model and effort:** Opus 5.5, high. A new hover card placed over moving robots, a screen test each frame, and the robots named from scene 1's Scene Prep on.
  - **Depends on:** T84 (the card without the scene, and the middle panel the hover card must keep clear of), T38 (the bubbles ride on the name tags the hover card sits beside; if T38 is cut, take it off this line), T83 (the cast's final models, whose size sets the hover area), T90 (its design doc edit goes in the files in `Docs/Design/`)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows, computer use on the PIE window or the test switch in T85.md to show a card, my OK on the design doc edit.
  - **Touches:** new `Content/NHOS/UI/WBP_CastTip.uasset`, `Content/NHOS/UI/WBP_Stage.uasset` (the hover test, the cast off the card), `Content/NHOS/Core/BP_Show.uasset` (the names in scene 1's Scene Prep, `PrepPrompt`'s hint, the cast data if the card needs it), `Content/NHOS/Stage/BP_Robot.uasset` only if the names or the hover need it, `Docs/switches.example.json` if the test switch is added, `Graphs/` files for the graphs it writes, `Docs/tasks/T85.md`.
  - **Details:** [Docs/tasks/T85.md](tasks/T85.md)

- [ ] **T87 When I win, every AI reacts to the reveal, the cut ones too**
  - **Model and effort:** Opus 5.5, high. A new ask with its free-mode lines, cut robots that get back up, and a short reaction phase before the end screen.
  - **Depends on:** T77 (each line's emotion reaches its robot in `StageLine`), T38 (the bubbles, and `Say`'s `EvenCut` for a cut robot; if T38 is cut, take it off this line), T60 (the end screen and `EndReveal`, which the reactions play before), T54 (the two wins and their line in `game_messages`), T75 (`Emote`, and its rule that a cut robot doesn't emote), T76 (free mode's emotion lists), T90 (its Bot Prompts and Rules edits go in the files in `Docs/Design/`)
  - **Needs:** editor + Unreal MCP running, Test for Free with `spare_human` and `force_tie` for the PIE shows, the relay for a `--relay --free` check, my OK on the Bot Prompts and Rules tab edits, my OK before the relay is deployed again (`free_mode.json`), my OK for a paid `--ask reaction_win` run (a few cents).
  - **Touches:** `Content/NHOS/Core/BP_Show.uasset` (the new ask sent with the closing ask on a win, one call that plays the reactions before `ShowEndScreen`; new logic in its own component if it grows), `Content/NHOS/Core/BPC_LinePlayer.uasset` (the reaction lines, a cut robot's bubble), `Content/NHOS/Stage/BP_Robot.uasset` (a cut robot gets back up, `Emote` for a risen robot), `Content/NHOS/Core/BPC_LLMClient.uasset` only if `FreeReply` needs a change, `Content/NHOS/Data/prompts.json` (`asks.reaction_win`, `_readme`), `Content/NHOS/Data/free_mode.json` (the `reaction_win` phase), `Relay/src/index.js` only if its free mode needs it, `Tools/check_prompts.py`, the design doc, `Graphs/` files for the graphs it writes, `Docs/tasks/T87.md`.
  - **Details:** [Docs/tasks/T87.md](tasks/T87.md)

- [ ] **T34 Fix the in-show screen**
  - **Model and effort:** Opus 5.5, high. Hierarchy and state judgment on the busiest screen.
  - **Depends on:** T32, T30, T38 (the line pacing, its typing line, the speech bubbles and the chat button are in, so this task polishes the final screen). If T38 is cut, take it off this line. Also T50, T53, T57 (the note category on my card, the clapperboard and the "passed" marker are on the screen it polishes), and T64, T65, T66, T78 (the action builder, the preview line, the speech field, the timer and the emotion chip are in the input row it polishes), and T73 (the lines type out on the screen it polishes), and T84, T85 (Scene Prep's middle panel and the cast's hover cards; they settle T34-build's 2.9 and the names in Scene Prep from its 2.1), and T87 (the reactions to a win play on the screen it polishes), and T88 (each scene's clue on my card).
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows.
  - **Touches:** `Content/NHOS/UI/WBP_Stage.uasset`, `WBP_SpeechBubble.uasset`, `WBP_ChatLine.uasset` and `WBP_MoneyBurn.uasset` if T32 left a row for either, `Content/NHOS/Core/BP_Show.uasset` only if a widget's call must change (for example `SetPrompt`), `Graphs/WBP_Stage/` files, `Docs/tasks/T34.md` and the audit table in `Docs/tasks/T32.md`.
  - **Details:** [Docs/tasks/T34.md](tasks/T34.md)

- [ ] **T61 Stagehand onboarding: earpiece tips, a tips toggle and How to play**
  - **Model and effort:** Opus 5.5, high. A new system with its own data file, component and widgets, called from the show at eight moments.
  - **Depends on:** T33 (the title screen), T34 (the in-show screen), T84 (the middle panel now sits about where the earpiece's Scene Prep spot was; T84's findings say where it can go), T50, T52, T53, T57, T58, T62, T66 (the rules its lines teach, how I take a turn among them), T60 (the lose and win screens it speaks on), T88 (the clue that its scene 1 line names), T90 (its palette row goes in `Docs/Design/ArtInspiration.md`)
  - **Needs:** editor + Unreal MCP running, Test for Free for the PIE shows.
  - **Touches:** new `Content/NHOS/Data/stagehand.json`, new `Content/NHOS/Core/BPC_Stagehand.uasset`, new `Content/NHOS/UI/WBP_Earpiece.uasset` and `WBP_HowToPlay.uasset`, `Content/NHOS/UI/WBP_Title.uasset` (the How to play button and the tips toggle), `Content/NHOS/UI/WBP_Stage.uasset` (the earpiece's place), `Content/NHOS/Core/BP_Show.uasset` (one call per moment), a new file in `Local/` for the first-show flag, new `Content/NHOS/UI/Stagehand/T_Stagehand_Portrait.uasset` with `Docs/StagehandArt/` and a row in `Docs/Assets.md` (the portrait), `Tools/check_prompts.py`, `Docs/ItchPage.md`, `Graphs/` files for the graphs it writes, `Docs/tasks/T61.md`.
  - **Details:** [Docs/tasks/T61.md](tasks/T61.md)
  - **Waiting:** the Mac built and pushed T61's new pieces (see "Part 1" in T61.md): `Content/NHOS/Data/stagehand.json`, `BPC_Stagehand` (`BeginShow`, `Say(Key)`, `EndShow(Win, Reason)`, `TipsNext`, `SetTipsNext(On)`), `WBP_Earpiece` (now with the friendly AI stagehand's portrait, `Content/NHOS/UI/Stagehand/T_Stagehand_Portrait`, on my call) and `WBP_HowToPlay` (`OpenOver(InBack)`, the six bullets I OKed). The Rules tab now calls the stagehand a friendly AI (rev 48). The claim stays for the PC's session. Left: the PC's chain adds the calls in BP_Show, the earpiece's place in WBP_Stage, the button and toggle on WBP_Title, the checker and itch page lines, then the full check

- [ ] **T89 Post-jam builds go to itch.io with butler on every push**
  - **Model and effort:** Opus 5.5, high. A CI pipeline on a self-hosted runner, with the secrets check as its gate. It is mostly scripts and config, but a mistake here can ship a key or touch the jam's file.
  - **Depends on:** none. It needs no editor and changes no asset, so it can run beside the chain. Run it on the PC, which has the engine, Visual Studio 2022 and the Windows 11 SDK.
  - **Needs:** this PC; my itch.io API key, which I save myself as the repo's `BUTLER_API_KEY` Actions secret and use for `butler login` (Claude never sees it); my OK to download butler and the GitHub Actions runner and to register this PC as a runner; my OK on the post-jam file's label and before the hidden first push is made visible; a free autoplay run of a copy of the build.
  - **Touches:** new `.github/workflows/itch-windows.yml`, new `Tools/deploy_itch.py`, `Tools/check_build_secrets.py` (a `--local` option), `CLAUDE.md` (Commands: deploys and the post-jam zip names), `README.md`, `Docs/ItchPage.md` (the Uploads row), `Docs/tasks/T89.md`; outside the repo: butler, the runner in `C:/actions-runner` and the deploy worktree. The itch.io page gets one new file, `windows-postjam`; the jam's file stays as it is.
  - **Details:** [Docs/tasks/T89.md](tasks/T89.md)

### Done

- [x] **T01 Spike: one Claude call from Blueprint, in PIE**
  - **Details:** [Docs/tasks/T01.md](tasks/T01.md)
- [x] **T02 Spike: the same call in a packaged Windows build, and record the decision**
  - **Details:** [Docs/tasks/T02.md](tasks/T02.md)
- [x] **T03 Prompt and data files**
  - **Details:** [Docs/tasks/T03.md](tasks/T03.md)
- [x] **T04 Stage screen: a log and an input box**
  - **Details:** [Docs/tasks/T04.md](tasks/T04.md)
- [x] **T05 One AI reply on screen**
  - **Details:** [Docs/tasks/T05.md](tasks/T05.md)
- [x] **T06 Show setup and Scene Prep**
  - **Details:** [Docs/tasks/T06.md](tasks/T06.md)
- [x] **T07 The Scene: three simultaneous turns**
  - **Details:** [Docs/tasks/T07.md](tasks/T07.md)
- [x] **T08 Free Talk**
  - **Details:** [Docs/tasks/T08.md](tasks/T08.md)
- [x] **T09 The Cut: votes, tiebreak and reveal**
  - **Details:** [Docs/tasks/T09.md](tasks/T09.md)
- [x] **T10 Reactions, the final two, end screens and restart**
  - **Details:** [Docs/tasks/T10.md](tasks/T10.md)
- [x] **T11 The cast on stage: four box robots**
  - **Details:** [Docs/tasks/T11.md](tasks/T11.md)
- [x] **T12 Go/no-go gate: I play 3 shows**
  - **Details:** [Docs/tasks/T12.md](tasks/T12.md)
- [x] **T13 The AIs talk like a normal chat**
  - **Details:** [Docs/tasks/T13.md](tasks/T13.md)
- [x] **T14 UI/UX polish**
  - **Details:** [Docs/tasks/T14.md](tasks/T14.md)
- [x] **T15 Story scenes on an improv stage**
  - **Details:** [Docs/tasks/T15.md](tasks/T15.md)
- [x] **T16 One LLM per AI player: prompts and keys**
  - **Details:** [Docs/tasks/T16.md](tasks/T16.md)
- [x] **T18 One LLM per AI player: in the game, and three ways to play**
  - **Details:** [Docs/tasks/T18.md](tasks/T18.md)
- [x] **T26 Five actors: one AI per provider, plus me**
  - **Details:** [Docs/tasks/T26.md](tasks/T26.md)
- [x] **T17 Stage art and personality**
  - **Details:** [Docs/tasks/T17.md](tasks/T17.md)
- [x] **T19 Robots act out their actions**
  - **Details:** [Docs/tasks/T19.md](tasks/T19.md)
- [x] **T27 The screen floats over the stage**
  - **Details:** [Docs/tasks/T27.md](tasks/T27.md)
- [x] **T25 The design docs point to the Claude Doc**
  - **Details:** [Docs/tasks/T25.md](tasks/T25.md)
- [x] **T35 A bill burns in the bottom-right corner for every relay call**
  - **Details:** [Docs/tasks/T35.md](tasks/T35.md)
- [x] **T21 How a judge plays: the relay's limits on screen, and the itch.io page**
  - **Details:** [Docs/tasks/T21.md](tasks/T21.md)
- [x] **T39 Art batch tool and asset list**
  - **Details:** [Docs/tasks/T39.md](tasks/T39.md)
- [x] **T29 The chat holds only chat**
  - **Details:** [Docs/tasks/T29.md](tasks/T29.md)
- [x] **T28 Scene Prep shows the whole card, the scene shows only mine**
  - **Details:** [Docs/tasks/T28.md](tasks/T28.md)
- [x] **T32 UI/UX audit, style guide and shared pieces**
  - **Details:** [Docs/tasks/T32.md](tasks/T32.md)
- [x] **T40 Generate the 13 headpieces**
  - **Details:** [Docs/tasks/T40.md](tasks/T40.md)
- [x] **T56 The bots want to survive, and each has a rival**
  - **Details:** [Docs/tasks/T56.md](tasks/T56.md)
- [x] **T41 Generate the story props**
  - **Details:** [Docs/tasks/T41.md](tasks/T41.md)
- [x] **T33 Fix the title, key entry and end screens**
  - **Details:** [Docs/tasks/T33.md](tasks/T33.md)
- [x] **T42 Generate the opera-house pieces**
  - **Details:** [Docs/tasks/T42.md](tasks/T42.md)
- [x] **T20 Audio**
  - **Details:** [Docs/tasks/T20.md](tasks/T20.md)
- [x] **T30 The lines play one at a time**
  - **Details:** [Docs/tasks/T30.md](tasks/T30.md)
- [x] **T43 Import the generated models and make the clay material**
  - **Details:** [Docs/tasks/T43.md](tasks/T43.md)
- [x] **T51 No decoy note, and every note gets a category**
  - **Details:** [Docs/tasks/T51.md](tasks/T51.md)
- [x] **T46 The two-tone capsule pill bots**
  - **Details:** [Docs/tasks/T46.md](tasks/T46.md)
- [x] **T50 Only the bots get the director's note**
  - **Details:** [Docs/tasks/T50.md](tasks/T50.md)
- [x] **T59 Every line is capped at 15 words, mine too**
  - **Details:** [Docs/tasks/T59.md](tasks/T59.md)
- [x] **T49 The clay opera-house stage**
  - **Details:** [Docs/tasks/T49.md](tasks/T49.md)
- [x] **T53 Scene clock: one scene fewer than the cast, on a clapperboard**
  - **Details:** [Docs/tasks/T53.md](tasks/T53.md)
- [x] **T36 Each burning bill shows the logo of the provider it paid**
  - **Details:** [Docs/tasks/T36.md](tasks/T36.md)
- [x] **T52 A tie cuts nobody**
  - **Details:** [Docs/tasks/T52.md](tasks/T52.md)
- [x] **T44 The seven film-parody cards in the data files**
  - **Details:** [Docs/tasks/T44.md](tasks/T44.md)
- [x] **T37 Error messages say what went wrong, with a joke**
  - **Details:** [Docs/tasks/T37.md](tasks/T37.md)
- [x] **T54 New win condition: the final two, or on stage when the last scene ends**
  - **Details:** [Docs/tasks/T54.md](tasks/T54.md)
- [x] **T55 Remove the Director AI**
  - **Details:** [Docs/tasks/T55.md](tasks/T55.md)
- [x] **T48 The seven painted backdrops**
  - **Details:** [Docs/tasks/T48.md](tasks/T48.md)
- [x] **T45 Each card's props on the prop table**
  - **Details:** [Docs/tasks/T45.md](tasks/T45.md)
- [x] **T72 A voice for each robot, and mine: the syllable sounds**
  - **Details:** [Docs/tasks/T72.md](tasks/T72.md)
- [x] **T57 Silence and polish are tells: a pass shows as "passed"**
  - **Details:** [Docs/tasks/T57.md](tasks/T57.md)
- [x] **T67 Analytics, part 1: the relay takes events and reports them**
  - **Details:** [Docs/tasks/T67.md](tasks/T67.md)
- [x] **T71 Music for each place and each scene**
  - **Details:** [Docs/tasks/T71.md](tasks/T71.md)
- [x] **T73 Lines type out, one voice sound per syllable**
  - **Details:** [Docs/tasks/T73.md](tasks/T73.md)
- [x] **T79 The new cast, part 1: one round head and three bodies**
  - **Details:** [Docs/tasks/T79.md](tasks/T79.md)
- [x] **T58 Last word: a reply for anyone @-mentioned in the final round**
  - **Details:** [Docs/tasks/T58.md](tasks/T58.md)
- [x] **T80 The new cast, part 2: Meta's android and my cardboard costume**
  - **Details:** [Docs/tasks/T80.md](tasks/T80.md)
- [x] **T47 A headpiece for each role**
  - **Details:** [Docs/tasks/T47.md](tasks/T47.md)
- [x] **T62 One rule set for every action, mine and the AIs'**
  - **Details:** [Docs/tasks/T62.md](tasks/T62.md)
- [x] **T63 My turn sends a built action and a spoken line**
  - **Details:** [Docs/tasks/T63.md](tasks/T63.md)
- [x] **T81 The cast in Hyper3D, part 1: generate the models from the concept art**
  - **Details:** [Docs/tasks/T81.md](tasks/T81.md)

- [x] **T75 Each robot can show an emotion: its face and a gesture**
  - **Details:** [Docs/tasks/T75.md](tasks/T75.md)
- [x] **T82 The cast in Hyper3D, part 2: the round-head bots get their models**
  - **Details:** [Docs/tasks/T82.md](tasks/T82.md)
- [x] **T60 Win and lose screens: the reasoning, the top reason and the rivals**
  - **Details:** [Docs/tasks/T60.md](tasks/T60.md)
- [x] **T83 The cast in Hyper3D, part 3: Meta and my costume get their models**
  - **Details:** [Docs/tasks/T83.md](tasks/T83.md)
- [x] **T64 The action builder, the preview line and Action!**
  - **Details:** [Docs/tasks/T64.md](tasks/T64.md)
- [x] **T65 The speech field: a word counter, focus and @ mentions**
  - **Details:** [Docs/tasks/T65.md](tasks/T65.md)
- [x] **T68 Analytics, part 2: the game sends its events**
  - **Details:** [Docs/tasks/T68.md](tasks/T68.md)
- [x] **T76 The bots send an emotion with every reply**
  - **Details:** [Docs/tasks/T76.md](tasks/T76.md)
- [x] **T69 Analytics, part 3: the actions players try that the game can't do**
  - **Details:** [Docs/tasks/T69.md](tasks/T69.md)
- [x] **T66 The turn timer, the auto-send and the other phases**
  - **Details:** [Docs/tasks/T66.md](tasks/T66.md)
- [x] **T77 Each robot shows its emotion as its line plays, mine too**
  - **Details:** [Docs/tasks/T77.md](tasks/T77.md)
- [x] **T38 Every line plays in a speech bubble, and the chat opens on a click (optional)**
  - **Details:** [Docs/tasks/T38.md](tasks/T38.md)
- [x] **T86 A full house: more rows of audience at the bottom of the screen**
  - **Details:** [Docs/tasks/T86.md](tasks/T86.md)
- [x] **T78 I can pick my robot's emotion**
  - **Details:** [Docs/tasks/T78.md](tasks/T78.md)

## Not planned yet

Ideas that are not tasks yet, and only if time is left after the last open task: a fifth persona (since T26, that is a sixth actor and a fourth scene), more scene cards and more notes, and from my input spec (`Docs/tasks/T62.md`): clicking a prop, a place or an actor on the stage to fill the builder's target, and number keys 1 to 7 to pick an action. To plan one, add it as a task (see "Changing the plan").
