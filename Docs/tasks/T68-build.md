# T68 build sheet: the game sends its analytics events

Back to [T68](T68.md). A PC prep session wrote this on 2026-11-15, without the editor. It is written against **`noHumansOnSet` at `944978c`**. Every place below is named by its text first; line numbers are "at `944978c`", from the files in `Graphs/`. Find each line by its text before you change it.

**What lands before T68 and may move these places:** T71, T72 and T73 (audio; T71 changes `RunCue`'s music calls and may give the `"phase"` cue a key of its own, T73 changes `BPC_LinePlayer`), T57, T58, T62 to T66 (the chain on `BP_Show` and `WBP_Stage`), T79 and T80 (`BP_Robot` only), and **T67** (the relay's `POST /event`). The sheet was first written from [T67.md](T67.md); before the push, **T67 landed on `origin` (`69988c5`, "waits for the deploy OK and the live checks")**, and the route, the body, every event's fields and caps, the limit and the report were checked against it (`Relay/src/index.js` `checkEvent`, `Relay/relay.config.json` `events`, `Tools/analytics_report.py`, `Relay/README.md`'s new section, `T67.md`'s Findings). Everything below matches it. Where a line still says **check against T67**, re-check only if T67 changed after `69988c5`.

**My person changed T68 on 2026-11-15, in T67's session** (T67's closing commit `c0ae863` added two bullets to step 5 of `T68.md` and a "Builds only" line to T68's plan entry), and this sheet follows both:
- **Builds only.** The game sends events only when it runs as a packaged build. PIE and game windows started from the editor send nothing, whatever the other settings say, except when the `analytics` switch is `test` (then every event is marked `"test": true`, so the checks still work). Part 2b's `Init` tests for a packaged build with **`Content/Paks/` exists**: on this PC the packaged build has `Packaged/Windows/AIMegaJam2026/Content/Paks/AIMegaJam2026-Windows.pak` (and no `.uproject`), and the project folder has no `Content/Paks/`. `Is Packaged for Distribution` is true only for Shipping, and the jam build is Development (the task says so).
- **Our own machines.** The game prints its player id once at launch, `NHOS: ANALYTICS player <id>`, so each of our machines' ids can go in `ignore_players` in `Local/stats.json` (T67's report leaves those players out).

**Sources read:** `T68.md` and its plan entry; `T69.md` (what it needs from T68); `T67.md` and T67's commit `69988c5`; `T71-build.md` (`1c52b3a`: its own `PhaseKey` for the music and its `RunCue`), `T65-build.md` and `T66-build.md` (`54d81d9`, `20da1e2`: no change to `CueHeader`, `RunCue`, `OpenPrep`, `DrawCast` or the header texts); `T61-build.md` part 5 and 7 (the title toggle and the per-moment hooks, the model for part 6 here); `T57-build.md`, `T58-build.md` (the last word's header), `T64-build.md` (the turn header and `SetPhase`), `T71.md`, `T66.md`; findings in `T05.md` (`BPC_LLMRequest`), `T18.md`, `T21.md` (`BPC_HttpGet`, relaunch), `T28.md` (`OpenPrep`), `T30.md` (the cue queue), `T37.md` (`ErrorKind`, `errors.json`), `T53.md` (the header texts), `T54-build.md` (`WinReason`, `SHOW END`); the `Graphs/` sources of `BP_Show` (`RunCue`, the six `Cue*`, `OpenPrep`, `DrawCast`, `ShowTitle`, `EndShow`, `SetWinReason`), `BPC_LLMClient` (`SetMode`, `Ask`, `SendReq`, `HandleHttp`, `Deliver`, `ParseReply`, `FlushLocal`, `FlushOne`, `ErrorTestFail`, `ErrorKind`, `BackstageNote`, `HealthFail`, `CheckRelay`, `GoDown`, `ShowUnavailable`, `LoadConfig`, `StartShowSession`, `Relaunch`), `BPC_LinePlayer` (`Cue`, `CueHoldFor`, `Pump`), `WBP_Title`, `WBP_Unavailable`, `WBP_Keys`, `UIStyle`; `Tools/check_prompts.py` (the `llm.json` checks); `CLAUDE.md`, `Docs/ItchPage.md`, `Relay/README.md`, `Content/NHOS/Data/llm.json`, `Docs/switches.example.json`; the `NHOS: CUE` lines of this PC's last game logs (`Saved/Logs/`). The design doc (Tech & Build rev 28, Rules rev 45) was read, not changed: it says nothing about analytics or the title screen, and T68 doesn't touch it.

## In short

- **`SG_Player`** (new SaveGame, slot `player`): `PlayerId` (32 lowercase hex, no dashes, from `New Guid`), `FirstSeen` (`YYYY-MM-DD`, UTC), `Launches`, `AnalyticsOn` (true at first). Three tiny functions (`Fill`, `Bump`, `SetOn`) so no other Blueprint sets its variables directly.
- **`BPC_Analytics`** (new component on `BP_Show`, as `Analytics`): `Send(Event, Fields)` builds T67's body and posts it to `<relay>/event` through a **`BPC_LLMRequest`**, the request component every LLM ask already uses. The reply comes back through **`BPC_LLMClient.HandleHttp`**, which hands any `event-` tag straight to `BPC_Analytics.OnSent` (one new block at its top). No retry and no queue of its own: a failed event is printed and dropped. Named wrappers keep each caller to one node: `Launch`, `ModePicked`, `ShowStart`, `CuePhase`, `SendPhase`, `ShowEnd`, `Error`, `SetOn`, `IsOn`.
- **Prints:** `NHOS: ANALYTICS <event> <fields JSON>` for every send, `NHOS: ANALYTICS ok <event>` when the relay answers `ok`, `NHOS: ANALYTICS fail <event> <why>` when it doesn't. At load, `NHOS: ANALYTICS player <id> test=... build=... packaged=...` when events will go out, or only `NHOS: ANALYTICS off why=<switch|editor|autoplay|player> player=<id> packaged=...` when nothing will be sent (the id is on that line too, so an off run still prints one `NHOS: ANALYTICS` line).
- **Who sends:** a packaged build (`Content/Paks/` exists), unless the switch is `off`, autoplay is on, or the player turned Play stats off; and any game, editor included, when the switch is `test`.
- **When it sends (one node per caller):**
  - `launch`: `BP_Show.ShowTitle`, after `LoadSwitches` (the title **and** autoplay both pass there; `WBP_Title` alone would miss autoplay, and the Done-when needs `launch` in an autoplay show).
  - `mode`: `BPC_LLMClient.SetMode`, right before its `(return true "")`; and from `ShowStart` when nothing was picked in this level (autoplay, a relaunch).
  - `show_start`: `BP_Show.DrawCast`, right before its last `(return true)`, after `StartShowSession` made the show's session id.
  - `phase`: the phase headers all go through `BP_Show.CueHeader`. It gets one node that queues a `"stat"` cue right before the header, carrying the phase key (worked out from the header and the turn and round counters while they are still right). `RunCue` gets a `"stat"` branch that sends it when the queue reaches it, so the event goes out when I see the header. Scene Prep doesn't use `CueHeader`: `OpenPrep`, which already runs at screen time for every Scene Prep (the first one too), sends `scene_prep` itself.
  - `show_end`: `RunCue`'s `"end"` branch, after `ShowEndScreen`, with `ShowWin` and `WinReason`.
  - `error`: in `BPC_LLMClient`, next to each `NHOS: ERROR` print that comes with a backstage note or the unavailable screen (`BackstageNote`, `HandleHttp`'s down branch, `HealthFail`), with the `errors.json` case the player saw.
  - `calls`: `BPC_LLMClient` counts each ask by provider and model (`NoteModel` in `Ask`, `CountCall` in `Deliver`), and `FlushCalls` sends one event per provider and model, then clears. `BPC_Analytics` calls it at each Scene Prep and at the end (question 1).
- **The opt-outs:** a "Play stats: on/off" button with the caption "Sends anonymous play stats" on the title's playbill (`WBP_Title`), and the `analytics` switch (`off`, `test`, or missing/`""`). Autoplay sends only with `test`.
- **Docs:** `CLAUDE.md` (Test for free; packaging), `Docs/ItchPage.md` (Test for Free, What gets sent where), `llm.json` (`build`, `_readme`), `Docs/switches.example.json` (`analytics`, `_readme`), `Relay/README.md` (the game's free mode; what the game sends, next to T67's drop-off sentence). **A push that touches `Relay/` redeploys the relay**, so it needs my person's OK typed in the T68 session (T55, T58 found the same).
- **Runs:** two short launches (`launches` 1 then 2, same id), a free autoplay show with `"analytics": "test"` (every event, `ok` acks, no `LogScript`), the same with `"off"` and with `""` (the editor sends nothing), a PIE title check with screenshots and the toggle, `python Tools/analytics_report.py --test`, and one packaged build that prints `packaged=true`.

## Questions for my person

Two questions. The recommended answer is first in each. The T68 session asks them with the multiple-choice tool, one at a time, before part 2, unless my person answered them on this sheet first.

1. **How often `calls` is sent: the event count per show.** T67 caps each address at 500 real events a day (`limits.ip_daily_events`; `"test"` events are counted apart, so our checks don't use it up) and calls that "about 20 shows", so about 25 events a show. T68's own spec gives far more. A full 5-actor show has about 35 phase headers (each scene: Scene Prep, 3 turns, 2 Free Talk rounds, maybe a last word, the vote, the reactions; then the closing). Each `calls` flush sends one event per provider and model asked since the last flush, about 4 (the four AI providers; the input ask runs on Anthropic's actor model).
   - **Send `calls` at each Scene Prep and at the end, not at every phase (Recommended).** About 60 events a show (3 launch/mode/start, about 35 phases, about 20 `calls`, 1 end), so 500 is about 8 shows a day per address, plenty for a judge. The totals per provider and model are the same; only a show quit mid-scene loses that scene's counts (it still has every scene before). One `if` in `SendPhase` (part 3d).
   - At every phase, as T68.md says. About 185 events a show, so 500 is under 3 shows a day: T67's `limits.ip_daily_events` must go up to about 2000 (a `relay.config.json` change and a relay deploy, with my person's OK), and the store takes about 3 times the writes.
2. **A check of the new `build` field in `Tools/check_prompts.py`.** The relay refuses any event whose `build` is over 20 characters (T67), and the game can't tell; every event would just print `fail`. The checker ignores keys it doesn't know, so a missing or long `build` passes today. T68's Touches don't name the checker, and another session holds it now.
   - **Add the four-line check (part 8) and widen T68's Touches to `Tools/check_prompts.py` (Recommended).** `--offline` then fails a missing, empty or too-long `build`.
   - No checker change. The free autoplay show's `fail` lines would show it, but only once T67's relay is up.

## Decisions this sheet makes (open to change)

The T68 session shows this list to my person when it closes the task.

1. **`launch` is sent from `BP_Show.ShowTitle`, not `WBP_Title`.** Autoplay skips the title, and the Done-when's autoplay show must print `launch`. `ShowTitle` runs once per level load on both paths. `WBP_Title` gets only the toggle.
2. **A relaunch is not a launch.** A mode switch mid-show reloads the level with `nhosmode=` (`BPC_LLMClient.IsRelaunch`). Then `Launch` sends nothing and doesn't count. A **Back to title** from the unavailable screen reloads with no mode (`Relaunch("")`), so it does count as a launch; that is rare (only after a relay failure mid-show) and is left as it is.
3. **`Launches` counts even with analytics off.** It is the local count; turning stats back on later reports the true number.
4. **`mode` is `""` until a mode is picked** (T67 allows `""`), so `launch` goes out with `mode: ""`. `SetMode` sends `mode` after it succeeds; `ShowStart` sends it first when nothing was picked in this level (autoplay, a relaunch). A Play Again in the same level sends no second `mode`.
5. **`session` is `BPC_LLMClient.Session`.** `LoadConfig` makes one at load (the events before a show use it), and `StartShowSession` makes a new one per show. Both are `New Guid` as 32 hex digits, which T67's session rule allows (8 to 64 letters, digits, `-` or `_`). A fallback id made at launch is used only if the client's is empty.
6. **The player id is lowercase** (`ToLower` on the GUID), the form the relay stores it in. T67 accepts upper case too (`checkEvent`: `[0-9a-fA-F]{32}`, stored lower case), so this is only tidiness.
7. **Phase keys, with `scene` the scene number:** `scene_prep`, `turn_1` to `turn_3`, `free_talk_1` and `free_talk_2`, `last_word`, `vote`, `reactions`, `closing` (the "THE SHOW IS OVER" header; `scene` is the last scene's number). Turn-level keys show where in a scene a player stops; T61's tips use the same split (`scene_turn_<n>`, `free_talk_<r>`). The longest key is 11 characters, under T67's cap of 40. T67's report needs no list of them: it groups events by session (a show is a session with a `show_start`) and orders the phases by where they come in the shows.
8. **"SCENE n: FREE TALK IS OVER" is not a phase.** It is a one-line header between Free Talk and the vote. `PhaseKey` returns `""` for it and for any header it doesn't know, and `CuePhase` then queues nothing.
9. **Phase events go out at screen time.** The show's logic runs ahead of the line queue (T30), so a phase sent from the logic could be one I never saw. The `"stat"` cue sits right in front of its header in the queue.
10. **The phase key comes from the header text plus `BP_Show`'s counters**, read when `CueHeader` runs (logic time, when `TurnNum`, `TalkRound` and `SceneNum` are right). The header texts are the ones this PC's last logs print (part 0, step 6). A later task that renames a header must keep `PhaseKey` in step; part 11 tells T34.
11. **In Test for Free, `model` is `"free"`** and the tokens are 0; the event's `mode` says free as well.
12. **An ask that fails before it is sent** (no provider, no key, client not ready) isn't counted: no model was noted for it, and no provider was called. An ask that brings the relay down is counted as failed.
13. **`error`'s `kind` is the `errors.json` case the player saw:** `<kind>` for a backstage note (`rate_limited`), `down_<kind>` for the unavailable screen mid-show (`down_budget_used_up`), `health_<kind>` for a failed relay check on the title. These are the keys `ErrorLine` already reads. The key screen's own errors (`where=keytest`) aren't sent: they are about the player's keys and show on that screen. The longest, `down_provider_unavailable`, is 25 characters, under T67's cap of 40.
14. **Every failed actor ask after its retry sends `error`**, at the `NHOS: ERROR ... where=turn` print, including the ones whose note is held (once per lab per scene).
15. **No retry and no queue.** Each event is its own fire-and-forget request; a failure prints once and the event is lost. Offline, every event fails quietly. The game never waits on an answer.
16. **The toggle is a button, not a check box,** as T61 found for its tips toggle (decision 13 there): `UIStyle` has no check box style, and a button takes T33's focus ring and keyboard. Label "Play stats: on" / "Play stats: off" (Secondary), caption "Sends anonymous play stats" (the task's words), on the playbill right under the three mode buttons.
17. **Turning stats back on sends nothing**; the next event goes out as usual.
18. **`build` is the build day, `YYYY-MM-DD`,** starting at `"2026-11-15"`. T70 sets it to the day it packages the submission build.
19. **An autoplay run sends only when the switch is `test`;** a missing switch with autoplay on is off (`why=autoplay`). In the editor that case is already off (`why=editor`), so `autoplay` matters only in a packaged build.
20. **A packaged build is one whose content folder has `Paks/`** (`Utilities|Paths|DirectoryExists` on `GetProjectContentDirectory` + `Paks`). It is set at `Init` as `Packaged` and printed on the load line, so a check can see it. Every build T70 makes uses `-pak` (`CLAUDE.md`'s package command), so it always has the folder; the editor's project folder never has one (git doesn't track one, and nothing writes there).
21. **The id print is the load line.** With events going out it is `NHOS: ANALYTICS player <id> ...`, the task's words. With nothing going out the one `off` line carries `player=<id>`, because the Done-when allows only `NHOS: ANALYTICS off` in an off run. Either way the id prints once per level load, and a packaged build with no switches file prints the first form. The title toggle's own print is `NHOS: ANALYTICS toggle on|off`, so it never looks like an id.

## Wording that comes from the task or the doc

- **"Sends anonymous play stats"**: the task's words for the title's line. "Play stats: on" / "Play stats: off" is new, in the form of T61's "Stagehand tips: on".
- **The privacy line** (part 9c) is new wording, built from T67 step 6's list of what is stored ("an anonymous player id, the mode, the phases, call counts and tokens, error kinds ... Never typed text, keys or the address").
- **The free-mode sentences** (part 9) follow the task's step 6: free mode "makes no LLM call, and sends only analytics events unless they are turned off".

## 0. Before you start (after T66 and T67 are pushed)

1. `git log --oneline -20` shows T71 to T73, T57, T58, T62 to T66 and T67. `git lfs locks` shows no lock on `BP_Show.uasset`, `BPC_LLMClient.uasset` or `WBP_Title.uasset`. Claim T68 and lock those three. The two new assets need no lock until they exist; lock them after the first save (`git lfs lock Content/NHOS/Core/BPC_Analytics.uasset`, `.../SG_Player.uasset`).
2. **The questions are answered** (above). With question 2's first answer, add `Tools/check_prompts.py` (the `build` check) to T68's **Touches** in `Docs/Plan.md` in a `Plan: T68 touches the checker` commit. With question 1's second answer, tell my person and leave a note in `Agents/` for `all` that T67's `limits.ip_daily_events` must go up to about 2000 (a relay deploy, my person's OK); T68 doesn't change `Relay/relay.config.json`.
3. **T67 as pushed.** This sheet was checked against `69988c5`: the route is `POST <relay>/event`, it answers `{"ok": true}`; the body keys are `player` (32 hex, either case), `session` (8 to 64 of `A-Za-z0-9_-`), `build` (≤ 20), `mode` (`free`, `relay`, `keys`, `""`), `event`, `fields`, `test` (boolean), and nothing else; every field is optional, and a wrong type, an extra field or an over-long string is `bad_request`; the caps are `launches` 1 to 1,000,000, `first_seen` 10, `phase` 40, `scene` 0 to 99, `result` 20, `reason` 40, `provider` 20, `model` 60, the counts 0 to 100,000 and the tokens 0 to 100,000,000, `kind` 40; the body cap is 2 KB. If `git log -- Relay/ Tools/analytics_report.py` shows T67 changes after `69988c5`, check those against parts 2 and 10. Also:
   - T67's deploy: its commit "waits for the deploy OK and the live checks". The relay must have the route before part 10 (step 4 below tests it).
   - `Local/stats.json` exists on this PC (the report reads its key from it; `python Tools/analytics_report.py --new-key` writes one, and my person puts the same key in the Worker's `STATS_KEY` secret, T67). Without it, the report check waits for my person.
4. **The relay route is live.** From Git Bash, with the relay address from `llm.json` (never paste it into chat or a doc outside the repo):

   ```bash
   R=$(python -c "import json;print(json.load(open('Content/NHOS/Data/llm.json'))['relay'])")
   curl -s -X POST "$R/event" -H "content-type: application/json" -d '{"player":"0123456789abcdef0123456789abcdef","session":"t68probe01","build":"2026-11-15","mode":"","event":"mode","fields":{},"test":true}'
   ```

   Expected `{"ok":true}` (with or without spaces). Anything else: T67 isn't deployed or the shape differs; stop and fix the shape from part 3 first.
5. `python Tools/check_prompts.py --offline` passes before you start.
6. **The headers as T66 leaves them.** Run one free autoplay show in a game window (part 10, run C's switches but `"analytics": "off"`) before any change, or use the last chain task's log, and list every header:

   ```bash
   grep -ho "NHOS: CUE phase .*" Saved/Logs/<log>.log | sed 's/[0-9]\+/n/g' | sort | uniq -c
   ```

   This PC's logs at `944978c` print exactly these (T53's form): `THE SCENE: SCENE n, TURN n OF n`, `FREE TALK: SCENE n, ROUND n OF n`, `SCENE n: FREE TALK IS OVER`, `THE CUT: SCENE n`, `REACTIONS: SCENE n`, `THE SHOW IS OVER`; T58 adds `LAST WORD: SCENE n`. If a chain task changed one, change `PhaseKey` (part 3d) to match before you write it.
7. **T71's phase key.** T71's sheet (`T71-build.md`, `1c52b3a`) gives `BPC_ShowAudio` its own `PhaseKey(Text)`: header → music key (`card`, `free_talk`, `cut` or `""`), called from `RunCue`'s `"phase"` branch through `PlayPhase(Text, CardId)`. It doesn't change `CueHeader`. T68's `BPC_Analytics.PhaseKey` stays separate: it needs turn-level keys and the counters, which only `CueHeader` has right. The two tables read the same headers, so a header rename must change both (part 13). Read `T71.md`'s Findings in case the build differed from its sheet; if T71 did change `CueHeader`, part 4b's node goes into its new form.
8. **Survey in the editor, in this order** (each a separate `call_tool`; tool calls stop at about 120 s; read only, never write a read-back):
   1. `BPC_LLMRequest`: list its functions and read **`Setup`**'s signature (`read_graph_dsl` of `Setup` only; T05 says never rewrite its Event Graph). Record the types of `InClient` (expected a `BPC_LLMClient` object reference) and `InHeaders` (the HttpBlueprint `HttpHeader` struct, T18), and that `Finish` calls `InClient.HandleHttp(Tag, SentAt, TransportOk, Response)` and destroys the component (T05). Part 3 relies on both.
   2. `BPC_LLMClient` **`ClearReply`** (no file): does it reset `UsageIn` and `UsageOut`? If it doesn't, a reply with no `usage` would count the last reply's tokens again; then add `(set UsageIn "0") (set UsageOut "0")` at the top of `HandleHttp`'s normal path (after the `event-` block), and say so under Findings.
   3. `ObjectTools.list_properties` on `BPC_LLMClient`: the types of `UsageIn`, `UsageOut` (expected String: `FlushOne` sets `"0"`, `Deliver` concatenates them), `Model`, `Mode`, `Session` (String), `FreeHeaders` (`HttpHeader`), `TmpObj` (the JSON object type that `Json|LoadJsonfromString` returns; `Send`'s `Fields` input and `FlushCalls`' local use it), and whether `Session`, `Mode` and `FreeHeaders` can be read from another object (`Class|BPCLLMClient|GetSession :self ...`, the form `WBP_Title` uses for `Class|BPShow|GetLLMClient`). If not, add three pure getter functions to the client (`GetSessionId`, `GetModeNow`, `GetHeaders`) and use those.
   4. `find_nodes` in `BP_Show` for `K2Node_VariableGet` titled `Get TurnNum`, `Get TalkRound`, `Get SceneNum`, `Get ShowWin`, `Get WinReason` (use the full node class path, T30). `TurnNum` and `TalkRound` are T61-build's names (from T06, T08); if they differ, use the real ones in part 4b.
   5. **`WBP_Title`'s widget tree** (the UMG toolset from `list_toolsets`; T33 built it with it): the playbill's `VerticalBox` inside `Bill`, the slots of `PlayRing`, `FreeRing`, `KeysRing` and their captions `PlayCap`, `FreeCap`, `KeysCap`, then `ModeNote` and `CreditText`; their slot paddings (for part 6a's spacing).
   6. **Node names the DSL hasn't used yet** (`BlueprintTools` describes the DSL; `get_node_type_pins` leaves no nodes behind, T18): the Blueprint Paths library's Directory Exists (written `Utilities|Paths|DirectoryExists`, next to the `Utilities|Paths|GetProjectContentDirectory` the files already use), the SaveGame nodes (written here as `Game|SaveGame|DoesSaveGameExist`, `LoadGamefromSlot`, `SaveGametoSlot`, `CreateSaveGameObject`), the cast to `SG_Player` (written `Utilities|Casting|CastToSG_Player`, the form of `CastToStaticMesh` in `BP_Prop/SetProp.txt`), String to Int (written `Utilities|String|StringToInt`), `Utilities|String|ToLower`, and the date parts (written `Math|DateTime|GetYear`, `GetMonth`, `GetDay`). Use the real names in parts 1 to 3.

## 1. `SG_Player` (new SaveGame)

`/Game/NHOS/Core/SG_Player`, a Blueprint class whose parent is `SaveGame`.

| Variable | Type | Default |
|---|---|---|
| `PlayerId` | String | `""` |
| `FirstSeen` | String | `""` |
| `Launches` | Integer | 0 |
| `AnalyticsOn` | Boolean | true |

Three functions, so `BPC_Analytics` never sets another object's variables (only reads them, with the getter form `Class|SGPlayer|GetPlayerId :self (V Save)`). Write them as `Graphs/SG_Player/Fill.txt`, `Bump.txt` and `SetOn.txt`:

```lisp
; T68: the first launch's save: a new anonymous id, the UTC date, no launches yet, stats on.
(fn Fill (Id First)
  (set PlayerId Id)
  (set FirstSeen First)
  (set Launches 0)
  (set AnalyticsOn true))
```

```lisp
; T68: one more launch (BPC_Analytics.Launch; a relaunch doesn't count).
(fn Bump ()
  (set Launches (+ (V Launches) 1)))
```

```lisp
; T68: the title's Play stats toggle (BPC_Analytics.SetOn).
(fn SetOn (On)
  (set AnalyticsOn On))
```

- **Where it lives:** slot `player`, user index 0. In the editor, PIE and a `-game` window it is `Saved/SaveGames/player.sav` in the project folder (git ignores `Saved/`); in the packaged game it is under the user's local app data. Nothing in it comes from the Epic account, the machine or the keys.
- **The id:** `New Guid` → `To String (Guid)` gives 32 hex digits with no dashes (the default `Digits` format; `LoadConfig`'s `Session` is the same) → `ToLower`.

## 2. `BPC_Analytics` (new component)

`/Game/NHOS/Core/BPC_Analytics`, an Actor Component. Add it to `BP_Show`'s components as **`Analytics`**, the way T20 added `BPC_ShowAudio` as `Audio`, and leave the component variable readable from outside (`WBP_Title` reads it with `Class|BPShow|GetAnalytics`, as it reads `GetLLMClient`).

### 2a. Variables

| Variable | Type | Default | What it holds |
|---|---|---|---|
| `Ready` | Boolean | false | `Init` has run |
| `Active` | Boolean | false | events go out: `SwitchOk` and `PlayerOn` |
| `SwitchOk` | Boolean | false | sending is allowed: `test`, or a packaged build with the switch not `off` and autoplay off |
| `Packaged` | Boolean | false | this is a packaged build (`Content/Paks/` exists) |
| `PlayerOn` | Boolean | true | the player's own setting (the save's `AnalyticsOn`) |
| `Test` | Boolean | false | the switch is `test`: every event says `"test": true` |
| `AutoOn` | Boolean | false | `autoplay` in `Local/switches.json` |
| `Picked` | Boolean | false | a mode was reported in this level |
| `Switch` | String | `""` | the `analytics` switch |
| `Url` | String | `""` | `<relay>/event`, or `""` with no relay address |
| `Build` | String | `""` | `llm.json`'s `build` |
| `LaunchId` | String | `""` | a fallback session id, made at `Init` |
| `PlayerId` | String | `""` | from the save |
| `CurPhase` | String | `""` | the last phase key sent (T69 sends it with `unsupported`) |
| `CurScene` | Integer | 0 | its scene |
| `TmpStr` | String | `""` | scratch for JSON reads |
| `Client` | `BPC_LLMClient` object reference | none | the client on the same owner |
| `Save` | `SG_Player` object reference | none | the loaded save |

### 2b. Functions and their files

Each in its own file in `Graphs/BPC_Analytics/`, named after the function. The forms come from files that already work: JSON reads from `BPC_LLMClient/LoadConfig.txt`, JSON building from `Ask.txt` (`Json|LoadJsonfromString "{}"` then `Json|SetField`), the request from `SendReq.txt`, the component lookup from `BackstageNote.txt`, the cast from `BP_Prop/SetProp.txt`.

**`Init()`**: reads its settings, the switch and the save. `Launch` calls it first; every other entry point calls it if `Ready` is false.

```lisp
; T68: settings (llm.json relay and build), the analytics and autoplay switches, whether this is a packaged
; build, and the player's save. Builds only (my person's call): only a packaged build sends, unless the switch
; is "test". It runs once per level load, from Launch (BP_Show.ShowTitle); the other entry points call it if it hasn't.
(fn Init ()
  (set Ready true)
  (bind _cl (Actor|GetComponentbyClass :self (Components|GetOwner) :ComponentClass "/Game/NHOS/Core/BPC_LLMClient.BPC_LLMClient_C"))
  (set Client _cl)
  (set LaunchId (Utilities|String|ToLower (Guid|ToString(Guid) (Guid|NewGuid))))
  (set Url "")
  (set Build "")
  (bind (_o _ok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat (Utilities|Paths|GetProjectContentDirectory) "NHOS/Data/llm.json"))))
  (if _ok
    (bind _hr (Json|HasField _o "relay"))
    (if _hr
      (bind _r (Json|GetField _o "relay"))
      (set TmpStr _r)
      (if (not (Utilities|String|IsEmpty (V TmpStr)))
        (set Url (cat (V TmpStr) "/event"))))
    (bind _hb (Json|HasField _o "build"))
    (if _hb
      (bind _b (Json|GetField _o "build"))
      (set Build _b)))
  (set Switch "")
  (set AutoOn false)
  (bind (_so _sok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat (Utilities|Paths|GetProjectDirectory) "Local/switches.json"))))
  (if _sok
    (bind _ha (Json|HasField _so "analytics"))
    (if _ha
      (bind _sa (Json|GetField _so "analytics"))
      (set Switch _sa))
    (bind _hp (Json|HasField _so "autoplay"))
    (if _hp
      (bind _sp (Json|GetField _so "autoplay"))
      (set AutoOn _sp)))
  (set Test (streq (V Switch) "test"))
  (set Packaged (Utilities|Paths|DirectoryExists (cat (Utilities|Paths|GetProjectContentDirectory) "Paks")))
  (set SwitchOk (or (V Test) (and (V Packaged) (and (not (streq (V Switch) "off")) (not (V AutoOn))))))
  (bind _ex (Game|SaveGame|DoesSaveGameExist :SlotName "player" :UserIndex 0))
  (if _ex
    (bind _sg (Game|SaveGame|LoadGamefromSlot :SlotName "player" :UserIndex 0))
    (bind _p (Utilities|Casting|CastToSG_Player :Object _sg)
      (:then
        (set Save _p))
      (:CastFailed
        (print "NHOS: ANALYTICS save unreadable, a new player id"))))
  (Utilities|IsValid (V Save)
    (:"Is Valid")
    (:"Is Not Valid"
      (CallFunction|NewSave)))
  (set PlayerId (Class|SGPlayer|GetPlayerId :self (V Save)))
  (set PlayerOn (Class|SGPlayer|GetAnalyticsOn :self (V Save)))
  (set Active (and (V SwitchOk) (V PlayerOn)))
  (set TmpStr (cat " packaged=" (Utilities|String|ToString(Boolean) (V Packaged))))
  (if (V Active)
    (print (cat "NHOS: ANALYTICS player " (V PlayerId) " test=" (Utilities|String|ToString(Boolean) (V Test)) " build=" (V Build) " relay=" (Utilities|String|ToString(Boolean) (not (Utilities|String|IsEmpty (V Url)))) (V TmpStr)))
    (else
      (print (cat "NHOS: ANALYTICS off why=" (select (V SwitchOk) "player" (select (streq (V Switch) "off") "switch" (select (V Packaged) "autoplay" "editor"))) " player=" (V PlayerId) (V TmpStr))))))
```

- The `why` order: `switch` (the switch is `off`), then `editor` (not packaged, switch not `test`), then `autoplay` (packaged, autoplay on), then `player` (Play stats off).
- If `Utilities|Paths|DirectoryExists` isn't the node's name (survey 6), the Blueprint Paths library's "Directory Exists" is the one. A second test that also works: `<project dir>/AIMegaJam2026.uproject` exists only outside a packaged build (`FileExists`); use it only if the first fails, and write which under Findings.

- **The `off` line is the only `NHOS: ANALYTICS` line an off run prints** (the Done-when), once the save exists. A first launch also prints `NHOS: ANALYTICS new player` (`NewSave`), even when off; run B (part 10) comes after run E made the save, so it prints only the off line.
- `Utilities|IsValid` on a variable that was never set is the `IsValid` macro `BackstageNote` uses.

**`NewSave()`**: the first launch.

```lisp
; T68: the first launch: a new anonymous id (32 lowercase hex digits, no dashes) and today's UTC date.
(fn NewSave ()
  (bind _sg (Game|SaveGame|CreateSaveGameObject :SaveGameClass "/Game/NHOS/Core/SG_Player.SG_Player_C"))
  (bind _p (Utilities|Casting|CastToSG_Player :Object _sg)
    (:then
      (set Save _p))
    (:CastFailed
      (print "NHOS: ANALYTICS cannot make a save")
      (return)))
  (bind _now (Math|DateTime|UTCNow))
  (bind _mo (Math|DateTime|GetMonth _now))
  (bind _dy (Math|DateTime|GetDay _now))
  (set TmpStr (cat (str (Math|DateTime|GetYear _now)) "-" (select (< _mo 10) (cat "0" (str _mo)) (str _mo)) "-" (select (< _dy 10) (cat "0" (str _dy)) (str _dy))))
  (Class|SGPlayer|Fill :self (V Save) :Id (Utilities|String|ToLower (Guid|ToString(Guid) (Guid|NewGuid))) :First (V TmpStr))
  (Game|SaveGame|SaveGametoSlot :SaveGameObject (V Save) :SlotName "player" :UserIndex 0)
  (print "NHOS: ANALYTICS new player"))
```

- If `return` inside a cast's `:CastFailed` doesn't write, drop it: the `IsValid` that follows in `Init` reads `Save` again, and a failed cast leaves it unset. Then add an `IsValid` before `Fill`.

**`Launch()`**: from `BP_Show.ShowTitle`.

```lisp
; T68: once per level load, from BP_Show.ShowTitle, which the title screen and autoplay both pass.
; A relaunch (a mode switch mid-show reloads the level, BPC_LLMClient.IsRelaunch) is the same launch:
; no event and no count.
(fn Launch ()
  (CallFunction|Init)
  (bind _rl (Class|BPCLLMClient|IsRelaunch :self (V Client)))
  (if _rl
    (return))
  (Class|SGPlayer|Bump :self (V Save))
  (Game|SaveGame|SaveGametoSlot :SaveGameObject (V Save) :SlotName "player" :UserIndex 0)
  (bind _f (Json|LoadJsonfromString "{}"))
  (Json|SetField _f "launches" (Class|SGPlayer|GetLaunches :self (V Save)))
  (Json|SetField _f "first_seen" (Class|SGPlayer|GetFirstSeen :self (V Save)))
  (CallFunction|Send :Event "launch" :Fields _f))
```

**`Send(Event, Fields)`**: the one entry point (T69 calls it too). `Fields` is the JSON object type from survey 3.

```lisp
; T68: posts one analytics event to <relay>/event (T67) and never waits for the answer: the reply comes back
; through BPC_LLMClient.HandleHttp, which hands any event- tag to OnSent. Nothing goes out from the editor
; (PIE, a game window) unless the analytics switch is "test", nor when it is "off", when autoplay runs
; without "test", or when the player turned Play stats off (Init sets Active).
(fn Send (Event Fields)
  (if (not (V Ready))
    (CallFunction|Init))
  (if (not (V Active))
    (return))
  (if (Utilities|String|IsEmpty (V Url))
    (print (cat "NHOS: ANALYTICS fail " Event " no relay address in llm.json"))
    (return))
  (bind _ses (Class|BPCLLMClient|GetSession :self (V Client)))
  (bind _b (Json|LoadJsonfromString "{}"))
  (Json|SetField _b "player" (V PlayerId))
  (Json|SetField _b "session" (select (Utilities|String|IsEmpty _ses) (V LaunchId) _ses))
  (Json|SetField _b "build" (V Build))
  (Json|SetField _b "mode" (select (V Picked) (Class|BPCLLMClient|GetMode :self (V Client)) ""))
  (Json|SetField _b "event" Event)
  (Json|SetField _b "fields" Fields)
  (Json|SetField _b "test" (V Test))
  (bind _body (Json|GetJsonString _b))
  (bind _fs (Json|GetJsonString Fields))
  (print (cat "NHOS: ANALYTICS " Event " " _fs))
  (bind _req (Game|AddComponentbyClass (Components|GetOwner) "/Game/NHOS/Core/BPC_LLMRequest.BPC_LLMRequest_C"))
  (Class|BPCLLMRequest|Setup :self _req :InTag (cat "event-" Event) :InUrl (V Url) :InHeaders (Class|BPCLLMClient|GetFreeHeaders :self (V Client)) :InBody _body :InClient (V Client))
  (Class|BPCLLMRequest|Send :self _req))
```

- **Why `BPC_LLMRequest`:** it is the request the game already sends (T05: one component per request, so replies in flight never mix), and its Http Request node is wired by hand; a new request Blueprint would need that wiring again. Its `Finish` calls `InClient.HandleHttp`, so the client routes the reply back by tag, as it already does for `health` and `keytest-` (part 5c).
- **Headers:** the client's `FreeHeaders` holds only `content-type: application/json` (`LoadConfig`), which is all `/event` needs. No key ever goes with an event.
- **`mode`:** `""` until `Picked` (decision 4). `Picked` turns true in `ModePicked`.
- **If `Json|GetJsonString` pretty-prints** (the `NHOS: ANALYTICS` line breaks over several lines), look for a pretty-print pin with `get_node_type_pins` and set it false. If there is none, print `Event` alone here and add a one-line summary to each wrapper's own print (`phase=<key> scene=<n>`, `launches=<n>`).
- Read-backs may name `BPC_LLMRequest.Setup` as `Class|BPRobot|Setup` (T18); the node is right.

**`OnSent(Tag, TransportOk, Response)`**: from `BPC_LLMClient.HandleHttp` (part 5c).

```lisp
; T68: the relay's answer to one event. Only a failure matters to the game, and it only prints.
(fn OnSent (Tag TransportOk Response)
  (set TmpStr (Utilities|String|RightChop :SourceString Tag :Count 6))
  (if (not TransportOk)
    (print (cat "NHOS: ANALYTICS fail " (V TmpStr) " no reply " (Utilities|String|GetSubstring :SourceString Response :StartIndex 0 :Length 120)))
    (return))
  (bind (_o _ok) (Json|LoadJsonfromString Response))
  (if (not _ok)
    (print (cat "NHOS: ANALYTICS fail " (V TmpStr) " not JSON " (Utilities|String|GetSubstring :SourceString Response :StartIndex 0 :Length 120)))
    (return))
  (bind _hk (Json|HasField _o "ok"))
  (if (not _hk)
    (print (cat "NHOS: ANALYTICS fail " (V TmpStr) " " (Utilities|String|GetSubstring :SourceString Response :StartIndex 0 :Length 160)))
    (return))
  (print (cat "NHOS: ANALYTICS ok " (V TmpStr))))
```

- The relay's error shape (`{"type":"error","error":{"type":"bad_request",...}}`) has no `ok`, so a refused event prints its type and message. The relay's messages hold no secret (T67 builds them), unlike a provider's.

**`ModePicked()`**: from `BPC_LLMClient.SetMode`, and from `ShowStart`.

```lisp
; T68: a mode was picked (BPC_LLMClient.SetMode, after it succeeds), or a show starts with no pick in this
; level (autoplay, a relaunch). The event's own mode field carries the mode.
(fn ModePicked ()
  (set Picked true)
  (bind _f (Json|LoadJsonfromString "{}"))
  (CallFunction|Send :Event "mode" :Fields _f))
```

**`ShowStart()`**: from `BP_Show.DrawCast`.

```lisp
; T68: each show's start, restarts included, from BP_Show.DrawCast after StartShowSession made the show's
; session id.
(fn ShowStart ()
  (set CurPhase "")
  (set CurScene 0)
  (if (not (V Picked))
    (CallFunction|ModePicked))
  (bind _f (Json|LoadJsonfromString "{}"))
  (CallFunction|Send :Event "show_start" :Fields _f))
```

**`PhaseKey(Header, Turn, Round)` → String**: the header → key table (decisions 7, 8, 10).

```lisp
; T68: the analytics key of a phase header (BP_Show.CueHeader's text, as T53 and T58 left them):
; "THE SCENE: SCENE 2, TURN 1 OF 3" -> turn_1, "FREE TALK: SCENE 2, ROUND 2 OF 2" -> free_talk_2,
; "LAST WORD: SCENE 2" -> last_word, "THE CUT: SCENE 2" -> vote, "REACTIONS: SCENE 2" -> reactions,
; "THE SHOW IS OVER" -> closing. Any other header ("SCENE 2: FREE TALK IS OVER") is no phase: "".
; A task that renames a header changes this table too.
(fn PhaseKey (Header Turn Round)
  (if (Utilities|String|StartsWith :SourceString Header :InPrefix "LAST WORD")
    (return "last_word"))
  (if (Utilities|String|Contains :SearchIn Header :Substring ", TURN ")
    (return (cat "turn_" (str Turn))))
  (if (Utilities|String|Contains :SearchIn Header :Substring ", ROUND ")
    (return (cat "free_talk_" (str Round))))
  (if (Utilities|String|StartsWith :SourceString Header :InPrefix "THE CUT: SCENE")
    (return "vote"))
  (if (Utilities|String|StartsWith :SourceString Header :InPrefix "REACTIONS")
    (return "reactions"))
  (if (Utilities|String|StartsWith :SourceString Header :InPrefix "THE SHOW IS OVER")
    (return "closing"))
  (return ""))
```

**`CuePhase(Header, Turn, Round, Scene)`**: from `BP_Show.CueHeader`.

```lisp
; T68: queues a phase's analytics event in the line queue, right before its header (BP_Show.CueHeader calls
; this first). The key is worked out now, while the show's counters are right; the event goes out when the
; queue reaches it (RunCue's "stat" branch -> SendPhase), so it is sent when the header shows on screen.
(fn CuePhase (Header Turn Round Scene)
  (bind _k (CallFunction|PhaseKey :Header Header :Turn Turn :Round Round))
  (if (Utilities|String|IsEmpty _k)
    (return))
  (bind _lp (Actor|GetComponentbyClass :self (Components|GetOwner) :ComponentClass "/Game/NHOS/Core/BPC_LinePlayer.BPC_LinePlayer_C"))
  (Utilities|IsValid _lp
    (:"Is Valid"
      (Class|BPCLinePlayer|Cue :self _lp :Kind "stat" :Text _k :Num Scene))
    (:"Is Not Valid"
      (print "NHOS: ANALYTICS no line player"))))
```

- The `"stat"` cue doesn't hold the queue: `pacing.json`'s `cue_hold` has no `stat` entry, so `CueHoldFor` returns 0 and `Pump` goes straight on to the header (`Graphs/BPC_LinePlayer/CueHoldFor.txt`). **Re-check after T73**, which changes `BPC_LinePlayer` and `pacing.json`.
- Each `"stat"` cue prints `NHOS: CUE stat <key>` (`Pump`), in every run, on or off. That is not an `NHOS: ANALYTICS` line.
- It is queued even when analytics is off, so the line queue does the same thing on and off, and `CurPhase` stays right for T69.

**`SendPhase(Key, Scene)`**: from `RunCue`'s `"stat"` branch and from `OpenPrep`.

```lisp
; T68: a phase starts on screen. At each Scene Prep it first sends the call counts since the last one
; (BPC_LLMClient.FlushCalls; question 1), then the phase.
(fn SendPhase (Key Scene)
  (set CurPhase Key)
  (set CurScene Scene)
  (if (streq Key "scene_prep")
    (Class|BPCLLMClient|FlushCalls :self (V Client)))
  (bind _f (Json|LoadJsonfromString "{}"))
  (Json|SetField _f "phase" Key)
  (Json|SetField _f "scene" Scene)
  (CallFunction|Send :Event "phase" :Fields _f))
```

- With question 1's second answer, drop the `if` line (keep its `FlushCalls` call).
- At the first Scene Prep the counts are empty, so `FlushCalls` sends nothing.

**`ShowEnd(Win, Reason)`**: from `RunCue`'s `"end"` branch.

```lisp
; T68: the end screen: the last call counts, then show_end with T54's WinReason (caught, final_two,
; last_scene). show_end is the show's last event.
(fn ShowEnd (Win Reason)
  (Class|BPCLLMClient|FlushCalls :self (V Client))
  (bind _f (Json|LoadJsonfromString "{}"))
  (Json|SetField _f "result" (select Win "win" "lose"))
  (Json|SetField _f "reason" Reason)
  (CallFunction|Send :Event "show_end" :Fields _f))
```

- `result` is `win` or `lose`, the words of `NHOS: SHOW END result=` (T54).

**`Error(Kind)`**: from `BPC_LLMClient`.

```lisp
; T68: an error the player saw: a backstage note or the unavailable screen, as its errors.json case.
(fn Error (Kind)
  (bind _f (Json|LoadJsonfromString "{}"))
  (Json|SetField _f "kind" Kind)
  (CallFunction|Send :Event "error" :Fields _f))
```

**`SetOn(NewOn)`** and **`IsOn()` → Boolean**: from `WBP_Title`.

```lisp
; T68: the title's Play stats toggle. Turning it off sends one last analytics_off event, then nothing.
; Turning it back on sends nothing. The switch still wins: with "analytics": "off" nothing goes out either way.
(fn SetOn (NewOn)
  (if (not (V Ready))
    (CallFunction|Init))
  (if (== NewOn (V PlayerOn))
    (return))
  (if (not NewOn)
    (bind _f (Json|LoadJsonfromString "{}"))
    (CallFunction|Send :Event "analytics_off" :Fields _f))
  (set PlayerOn NewOn)
  (Class|SGPlayer|SetOn :self (V Save) :On NewOn)
  (Game|SaveGame|SaveGametoSlot :SaveGameObject (V Save) :SlotName "player" :UserIndex 0)
  (set Active (and (V SwitchOk) (V PlayerOn)))
  (print (cat "NHOS: ANALYTICS toggle " (select NewOn "on" "off"))))
```

```lisp
; T68: the player's own setting, for the title's label (not the switch).
(fn IsOn ()
  (if (not (V Ready))
    (CallFunction|Init))
  (return (V PlayerOn)))
```

- `(if (not NewOn) ...)` with no `return` joins the code after it (T01), so both ways reach the save.
- `Send` runs before `PlayerOn` turns false, so `analytics_off` goes out; everything after it is dropped by `Active`.

### 2c. Compile order

`BPC_Analytics` calls `BPC_LLMClient` (`IsRelaunch`, `FlushCalls`, the getters), and the client calls `BPC_Analytics` (`OnSent`, `ModePicked`, `Error`, `Send`). `BPC_LLMRequest` and the client already reference each other the same way. Build in this order so no call node goes stale (T18: a stale node blocks every compile):

1. `SG_Player` (variables, three functions), compile, save.
2. `BPC_Analytics`: variables, then empty functions with their inputs and outputs (`Send`, `OnSent`, `ModePicked`, `ShowStart`, `CuePhase`, `PhaseKey`, `SendPhase`, `ShowEnd`, `Error`, `SetOn`, `IsOn`, `Init`, `NewSave`, `Launch`), compile, save.
3. `BPC_LLMClient`: the new variables and functions (part 5), compile, save.
4. `BPC_Analytics`: write each function's DSL, compile, save.
5. `BP_Show` (part 4), then `WBP_Title` (part 6).

## 3. The `analytics` switch

Read by `BPC_Analytics.Init`, once per level load, from `Local/switches.json` (the other readers stay as they are: `BPC_LLMClient.LoadConfig` reads `mode`, `burn_test` and `error_test` once at load; `BP_Show.LoadSwitches` reads `autoplay`, `force_tie` and `spare_human` at each scene and Cut; `DrawCast` reads `ai_seats`; `BPC_LinePlayer.LoadPacing` reads `fast_lines`).

| `analytics` | Editor (PIE, a game window from the editor) | Packaged, `autoplay` false | Packaged, `autoplay` true |
|---|---|---|---|
| missing or `""` | off (`why=editor`) | sends (a player's game) | off (`why=autoplay`) |
| `"test"` | sends, `"test": true` | sends, `"test": true` | sends, `"test": true` |
| `"off"` | off (`why=switch`) | off (`why=switch`) | off (`why=switch`) |

- **This PC:** add `"analytics": "off"` to `Local/switches.json` as part of T68 (step 5 of the task), and leave it there. The editor sends nothing without `test` anyway; the switch makes it plain, and it covers a package run that finds the file. Write a note in `Agents/` for `all` (a new file, `<UTC timestamp>-quantumcalzone-analytics-switch.md`): "T68 is in. The editor sends no analytics events unless `Local/switches.json` has `"analytics": "test"` (for checks). A packaged build sends real events: before you test one, put `{"analytics": "off"}` or `"test"` in its `Local/switches.json`, or add its id (the log's `NHOS: ANALYTICS player <id>`) to `ignore_players` in `Local/stats.json`."
- **A packaged build** has no `Local/switches.json`, so it sends normally: part 9b's `CLAUDE.md` line covers test runs of a package.
- **Our ids for `ignore_players`:** the packaged build keeps its own save (under the user's local app data), apart from the editor's `Saved/SaveGames/player.sav`, so it has its own id. Run F prints it; give it to my person for `Local/stats.json` (the file is per machine and not in git; the T68 session may add it itself if `Local/stats.json` exists, since it is this PC's own file).

## 4. `BP_Show`

### 4a. Graphs and files

| Graph | File | Change |
|---|---|---|
| `CueHeader` | yes | one node before its `Cue` (4b) |
| `RunCue` | yes | a new `"stat"` branch; one node in the `"end"` branch (4c) |
| `OpenPrep` | yes | one node after the `NHOS: PREP shown` print (4d) |
| `DrawCast` | yes | one node before its last `(return true)` (4e) |
| `ShowTitle` | yes | one node after `LoadSwitches` (4f) |
| components | — | add `BPC_Analytics` as `Analytics` |

All five have sources in `Graphs/BP_Show/`. Start from each file **as the chain tasks left it** (T71 changes `RunCue`; T57 adds `"passed"` and `"unpass"` branches to it; T58 doesn't change `CueHeader` but calls it for the last word), write the whole function with `write_graph_dsl`, and commit the updated file. No graph without a file is touched.

### 4b. `CueHeader`

At `944978c`, the whole file (`Graphs/BP_Show/CueHeader.txt`) is one line inside the function. New file:

```lisp
; T30: a header that waits for the lines in front of it.
; T68: first queues the phase's analytics event (a "stat" cue; BPC_Analytics.CuePhase), so the event goes out
; when this header shows. TurnNum, TalkRound and SceneNum are right here, at logic time.
(fn CueHeader (Text)
  (Class|BPCAnalytics|CuePhase :self (V Analytics) :Header Text :Turn (V TurnNum) :Round (V TalkRound) :Scene (V SceneNum))
  (Class|BPCLinePlayer|Cue :self (Variables|Default|GetLinePlayer) :Kind "phase" :Text Text :Num 0))
```

- Every phase header passes here: `StartTurn`, `StartTalkRound`, `EndFreeTalk`, `StartCut`, `StartReactions`, `EndShow` (T30's swaps) and T58's `StartLastWords`. None of those graphs changes.
- `StartTurn` and `StartTalkRound` add 1 to their counter before `CueHeader` (T06, T08), so turn 1 is 1.
- If the queue is idle, the `"stat"` cue and the header both run at once, inside the calling graph, in that order (T64-build's note on `StartTurn`).

### 4c. `RunCue`

Two edits to `Graphs/BP_Show/RunCue.txt` as T71 and T57 left it.

1. **A new first branch,** right after the function line, before `  (if (streq Kind "phase")` (line 5 at `944978c`):

   ```lisp
     ; T68: a phase's analytics event, queued by CueHeader right before its header (BPC_Analytics.CuePhase).
     (if (streq Kind "stat")
       (Class|BPCAnalytics|SendPhase :self (V Analytics) :Key Text :Scene Num)
       (return))
   ```

2. **The `"end"` branch** (line 33): after `(CallFunction|ShowEndScreen)`, before its `(return)`:

   ```lisp
       (Class|BPCAnalytics|ShowEnd :self (V Analytics) :Win (V ShowWin) :Reason (V WinReason))
   ```

   T61 adds its stagehand call to the same branch later (T61-build part 7a); the two don't depend on each other.

- Add `; T68: the "stat" cue (analytics phase events) and show_end at the end screen.` to the comment block at the top.

### 4d. `OpenPrep`

After the `NHOS: PREP shown scene=` print (line 3), before `(CallFunction|LoadSwitches)`:

```lisp
  (Class|BPCAnalytics|SendPhase :self (V Analytics) :Key "scene_prep" :Scene (Variables|Default|GetSceneNum))
```

- `OpenPrep` is the last node of `ScenePrep` (T28), and `ScenePrep` runs from the `"prep"` cue for scenes 2 on and straight from `SetupShow` for scene 1 (T30), so every Scene Prep passes here, at screen time. `RunCue`'s `"prep"` branch would miss scene 1.
- Comment line: `; T68: each Scene Prep sends its analytics phase (and the call counts so far).`
- T61 later adds its stagehand calls at the same place (T61-build 7a).

### 4e. `DrawCast`

Before the last `(return true))` (line 36), after the `(if (< (len (V PersonaArr)) 3) ...)` block:

```lisp
  (Class|BPCAnalytics|ShowStart :self (V Analytics))
```

- `DrawCast` runs first in `SetupShow` (T18), and Play Again runs `SetupShow` (T10), so every show, restarts included, sends `show_start` after `StartShowSession` set the show's session id. A show whose draw fails (`SetUnavailable`) never starts, so it sends no `show_start`.
- T58 also edits `DrawCast` (T58-build); start from the file as T58 left it.

### 4f. `ShowTitle`

After `(CallFunction|LoadSwitches)` (line 2), before the `bind _rl`:

```lisp
  (Class|BPCAnalytics|Launch :self (V Analytics))
```

- It must come before the title widget is made, so `WBP_Title`'s Construct finds the save loaded (`IsOn`). `BPC_LLMClient.LoadConfig` has run by then: this PC's logs print `NHOS: CLIENT ready` before `NHOS: SHOW READY` and the first `NHOS: SWITCHES` (`T45a.log`).

## 5. `BPC_LLMClient`

All edited graphs have files in `Graphs/BPC_LLMClient/`; start from each as pushed (T63-build touches `Deliver`'s neighbours, not `Deliver`; re-check `git log -- Graphs/BPC_LLMClient` for T57 to T66).

### 5a. New variables

| Variable | Type | What it holds |
|---|---|---|
| `Stats` | `BPC_Analytics` object reference | the analytics component on the same owner (set in `LoadConfig`) |
| `AskTags`, `AskModels` | String arrays | each sent ask's tag and model, until it is delivered |
| `CntKey`, `CntProv`, `CntModel` | String arrays | one entry per provider and model since the last flush (`CntKey` is `<provider>\|<model>`) |
| `CntCalls`, `CntFailed`, `CntIn`, `CntOut` | Integer arrays | its asks, failures, tokens in and out |
| `CIdx` | Integer | scratch |
| `CKey`, `CModel` | String | scratch |

### 5b. `LoadConfig`: one line

Before `(set Ready true)` (line 96):

```lisp
  (set Stats (Actor|GetComponentbyClass :self (Components|GetOwner) :ComponentClass "/Game/NHOS/Core/BPC_Analytics.BPC_Analytics_C"))
```

and a comment line at the top: `; T68: also finds the analytics component (Stats).` If the `set` won't take the return value straight, `bind` it first, as `CheckRelay` does with `AddComponentbyClass`.

### 5c. `HandleHttp`: a new first block

Right after the function line, **before** `(bind _now (Math|DateTime|UTCNow))` (line 4), so nothing of the ask state (`ClearReply`, `ErrType`, the pending arrays, `Down`) is touched by an event's reply:

```lisp
  ; T68: an analytics event's reply (BPC_Analytics.Send tags its request event-<event>) goes straight back.
  (if (Utilities|String|StartsWith :SourceString Tag :InPrefix "event-")
    (Class|BPCAnalytics|OnSent :self (V Stats) :Tag Tag :TransportOk TransportOk :Response Response)
    (return))
```

and, in the **down branch** (the `(if (and (streq (V Mode) "relay") (or (V HDown) (not TransportOk)))` block, lines 59 to 69), two nodes:

- after `(print (cat "NHOS: LLM " Tag " fail " ...))` (line 60): `(CallFunction|CountCall :Tag Tag :Ok false)`. This ask never reaches `Deliver`.
- after `(print (cat "NHOS: ERROR " _dk " provider=" (V CurProv) " where=down"))` (line 62): `(Class|BPCAnalytics|Error :self (V Stats) :Kind (cat "down_" _dk))`.

Comment line at the top: `; T68: an event- tag goes to BPC_Analytics.OnSent; the down branch counts the ask and reports the error.`

### 5d. `SetMode`: one line

Between `(print (cat "NHOS: MODE " InMode))` (line 13) and `(return true ""))` (line 14):

```lisp
  (Class|BPCAnalytics|ModePicked :self (V Stats))
```

- Only a pick that succeeds reports. The title's three buttons, the key screen's Save and Play, and the unavailable screen's Test for Free (before a show) call `SetMode`; a mid-show switch relaunches instead, and the new level's `ShowStart` reports the mode (`WBP_Unavailable`'s `FreeButton`: `Relaunch` first, `SetMode` only when no show started).
- The `too_few_keys` path returns before it, and is not sent (decision 13: a key screen error).

### 5e. `Ask`: two lines

1. **The free path** (`(if (streq (V Mode) "free")`, line 24): first line inside it, before `(add (V LocalTags) Tag)`:

   ```lisp
       (CallFunction|NoteModel :Tag Tag :Model "free")
   ```

2. **The sent path:** right before the last line, `(CallFunction|SendReq :Tag Tag :Prov (V CurProv) :Url (V AskUrl) :Payload (V AskBody) :Try 0))` (line 50):

   ```lisp
     (CallFunction|NoteModel :Tag Tag :Model (V Model))
   ```

   `BuildBody` (line 36) set `Model` for this ask a moment before, with the role's own model for the input ask. A retry (`HandleHttp` → `SendReq`) doesn't pass `Ask` again, so the note stays until `Deliver`.

Comment line: `; T68: each ask notes its model for the analytics call counts (NoteModel).`

### 5f. `Deliver`: one line

First line inside the function, before `(set TmpStr2 ...)` (line 3):

```lisp
  (CallFunction|CountCall :Tag Tag :Ok Ok)
```

- Every finished ask passes `Deliver`: a reply, a failed reply after its retry, a free reply (`FlushOne`), an `error_test` failure (`ErrorTestFail` → `HandleHttp`), and the early failures in `Ask` (not counted: no note).
- It comes before `ClearReply` on the failure path, and on success `UsageIn` and `UsageOut` hold this reply's usage (`ParseReply`; `"0"` in free mode). Survey 2 checks that they are reset between replies.

Comment line: `; T68: counts the ask for the analytics call counts (CountCall).`

### 5g. `BackstageNote` and `HealthFail`: one line each

- `BackstageNote`: after `(print (cat "NHOS: ERROR " _k " provider=" (V CurProv) " where=turn"))` (line 17), before the `NoteSeen` check, so a held note still reports:

  ```lisp
    (Class|BPCAnalytics|Error :self (V Stats) :Kind _k)
  ```

- `HealthFail`: after its print (line 5):

  ```lisp
    (Class|BPCAnalytics|Error :self (V Stats) :Kind (cat "health_" Kind))
  ```

Comment line in each: `; T68: also sends the analytics error event.`

### 5h. New functions

`Graphs/BPC_LLMClient/NoteModel.txt`:

```lisp
; T68: remembers an ask's model by its tag, until Deliver counts it (CountCall). "free" in Test for Free.
(fn NoteModel (Tag Model)
  (add (V AskTags) Tag)
  (add (V AskModels) Model))
```

`Graphs/BPC_LLMClient/CountCall.txt`:

```lisp
; T68: counts one finished ask for the analytics "calls" event: its provider (CurProv), the model Ask noted
; for its tag, and a failure or the reply's tokens (UsageIn, UsageOut). An ask that failed before it was sent
; (no provider, no key) has no note and isn't counted.
(fn CountCall (Tag Ok)
  (set CIdx (Utilities|Array|FindItem (V AskTags) Tag))
  (if (< (V CIdx) 0)
    (return))
  (set CModel (get (V AskModels) (V CIdx)))
  (set CKey (cat (V CurProv) "|" (V CModel)))
  (Utilities|Array|RemoveIndex (V AskTags) (V CIdx))
  (Utilities|Array|RemoveIndex (V AskModels) (V CIdx))
  (set CIdx (Utilities|Array|FindItem (V CntKey) (V CKey)))
  (if (< (V CIdx) 0)
    (add (V CntKey) (V CKey))
    (add (V CntProv) (V CurProv))
    (add (V CntModel) (V CModel))
    (add (V CntCalls) 0)
    (add (V CntFailed) 0)
    (add (V CntIn) 0)
    (add (V CntOut) 0)
    (set CIdx (- (len (V CntKey)) 1)))
  (Utilities|Array|SetArrayElem (V CntCalls) (V CIdx) (+ (get (V CntCalls) (V CIdx)) 1))
  (if (not Ok)
    (Utilities|Array|SetArrayElem (V CntFailed) (V CIdx) (+ (get (V CntFailed) (V CIdx)) 1))
    (return))
  (Utilities|Array|SetArrayElem (V CntIn) (V CIdx) (+ (get (V CntIn) (V CIdx)) (Utilities|String|StringToInt (V UsageIn))))
  (Utilities|Array|SetArrayElem (V CntOut) (V CIdx) (+ (get (V CntOut) (V CIdx)) (Utilities|String|StringToInt (V UsageOut)))))
```

`Graphs/BPC_LLMClient/FlushCalls.txt`:

```lisp
; T68: one analytics "calls" event per provider and model asked since the last flush, then clears the
; counts. BPC_Analytics calls it at each Scene Prep (SendPhase) and at the end screen (ShowEnd).
; With analytics off, Send drops each event and the counts still clear.
(fn FlushCalls ()
  (for _i (range (len (V CntKey)))
    (bind _f (Json|LoadJsonfromString "{}"))
    (Json|SetField _f "provider" (get (V CntProv) _i))
    (Json|SetField _f "model" (get (V CntModel) _i))
    (Json|SetField _f "calls" (get (V CntCalls) _i))
    (Json|SetField _f "failed" (get (V CntFailed) _i))
    (Json|SetField _f "tokens_in" (get (V CntIn) _i))
    (Json|SetField _f "tokens_out" (get (V CntOut) _i))
    (Class|BPCAnalytics|Send :self (V Stats) :Event "calls" :Fields _f))
  (clear (V CntKey))
  (clear (V CntProv))
  (clear (V CntModel))
  (clear (V CntCalls))
  (clear (V CntFailed))
  (clear (V CntIn))
  (clear (V CntOut)))
```

- If a `Json|SetField` value pin stays a wildcard on an array `get`, put the value into a typed scratch variable first (`TmpStr` for strings, a new Integer `TmpN` for numbers), as `FreeReply` does for reads.
- `provider` is the relay's provider id (`anthropic`, `openai`, `xai`, `meta`: `llm.json` `providers`), not the name on screen.

## 6. `WBP_Title`: the Play stats toggle

Start from `Graphs/WBP_Title/EventGraph.txt` and `ShowRing.txt` (T33). T61 later adds How to play and its tips toggle in `HowFrame` (T61-build part 5); T68 puts its toggle on the playbill, so the two never share a slot.

### 6a. Tree change inside `Bill` (read it first: survey 5)

Right after `KeysCap` (the caption under Use my own API keys), before `ModeNote`:

```
StatsRow        HorizontalBox, top padding as between KeysCap and ModeNote (T33's S-step)   (new)
├ StatsRing     Border (ShowRing), vertically centered                                        (new)
│ └ StatsButton Button, focusable
│   └ StatsLabel TextBlock "Play stats: on"
└ StatsCap      TextBlock, Caption, PaperQuiet, left padding S2, vertically centered: "Sends anonymous play stats"   (new)
```

- **Tab order** (widget order): Play via Relay, Test for Free, Use my own API keys, Play stats. Play via Relay keeps first focus (T33). T61 then adds How to play and Stagehand tips after it.
- At 1280 × 720 the playbill must still fit (T33's screenshots); if it doesn't, put `StatsRow` after `CreditText` instead, and say so under Findings.

### 6b. Graph changes (in `EventGraph.txt`)

PreConstruct, after T33's `KeysCap` lines:

```lisp
  (Class|UIStyle|StyleButton :Button (Variables|WBP_Title|GetStatsButton) :Label (Variables|WBP_Title|GetStatsLabel) :Kind "Secondary")
  (Class|Text|SetFont :self (Variables|WBP_Title|GetStatsCap) :Font fCap)
  (Class|Text|SetColorandOpacity :self (Variables|WBP_Title|GetStatsCap) :ColorAndOpacity cPaperQuiet)
  (CallFunction|ShowRing :Ring (Variables|WBP_Title|GetStatsRing) :On false)
```

Construct, after the focus line:

```lisp
  (CallFunction|ShowStats)
```

Tick, with the other three rings:

```lisp
  (CallFunction|ShowRing :Ring (Variables|WBP_Title|GetStatsRing) :On (Widget|HasKeyboardFocus :self (Variables|WBP_Title|GetStatsButton)))
```

A new event:

```lisp
(event OnClicked(StatsButton)
  (bind _show (Actor|GetActorOfClass "/Game/NHOS/Core/BP_Show.BP_Show_C"))
  (bind _an (Class|BPShow|GetAnalytics :self _show))
  (bind _on (Class|BPCAnalytics|IsOn :self _an))
  (Class|BPCAnalytics|SetOn :self _an :NewOn (not _on))
  (print (cat "NHOS: TITLE click stats=" (select _on "off" "on")))
  (CallFunction|ShowStats))
```

Header comment line: `; T68: the Play stats toggle (StatsButton) under the three ways to play.`

New function, `Graphs/WBP_Title/ShowStats.txt`:

```lisp
; WBP_Title.ShowStats (T68): the Play stats toggle's label says what the game does now.
(fn ShowStats ()
  (bind _show (Actor|GetActorOfClass "/Game/NHOS/Core/BP_Show.BP_Show_C"))
  (bind _on (Class|BPCAnalytics|IsOn :self (Class|BPShow|GetAnalytics :self _show)))
  (Widget|SetText(Text) :self (Variables|WBP_Title|GetStatsLabel) :InText (Utilities|Text|ToText(String) (select _on "Play stats: on" "Play stats: off"))))
```

- The toggle doesn't change the mode note or start anything.
- PreConstruct runs at design time too, with no show in the level; it only styles, so `StatsLabel` keeps its design-time "Play stats: on".

## 7. `llm.json`

Not edited by this prep session; the T68 session makes these edits.

- **`build`**, a new top-level field after `"relay"`: `"build": "2026-11-15",` (decision 18; at most 20 characters, T67).
- **`_readme`:** replace

  > Test for Free makes no network call (the game builds replies from free_mode.json)

  with

  > Test for Free makes no LLM call (the game builds replies from free_mode.json)

  and add at the end of the `_readme`:

  > build: the game's version (the build day, YYYY-MM-DD), sent with every analytics event; at most 20 characters. In a packaged build, every mode, Test for Free included, sends a few anonymous analytics events to the relay's /event (BPC_Analytics, T68): an id made on the first launch, the mode, how far each show gets, call counts and tokens per provider and model, and error kinds. Nothing goes when the player turns Play stats off on the title, or when Local/switches.json has "analytics": "off". The editor sends none unless that switch is "test".

- `free_mode.json`'s `_readme` line "(BPC_LLMClient.FreeReply, no network)" stays: `FreeReply` itself still makes no network call. Changing that file would redeploy the relay.

## 8. `Tools/check_prompts.py` (question 2's first answer)

In the `# llm.json` block, after the `for k in ["endpoint", "api_version"]:` check (line 611 at `944978c`, 610 after T45's `611b1f8`):

```python
    # T68: build goes with every analytics event; the relay refuses one over 20 characters (T67).
    build = llm.get("build")
    if not isinstance(build, str) or not build or len(build) > 20:
        errors.append("llm.json: build must be a string of 1 to 20 characters (T68: the relay refuses longer)")
```

- The 20 is T67's, written in `Relay/src/index.js` (`checkEvent`: "build must be text of up to 20 characters"), not in `relay.config.json`, so the checker keeps the literal.
- Add `build` to the docstring's list of what `--offline` checks, one line, in the style of the others.
- No `--log` change: `analytics_report.py` (T67) checks the events, and part 10's script checks the log.

## 9. The docs (step 6, step 4, step 7)

### 9a. `CLAUDE.md`, "Test for free" (line 171 at `944978c`)

Replace the last sentence

> In free mode the game makes no network call at all: `BPC_LLMClient` builds each reply itself from the pre-written lines in `Content/NHOS/Data/free_mode.json`, the same way the relay's own free mode does.

with

> In free mode the game makes no LLM call: `BPC_LLMClient` builds each reply itself from the pre-written lines in `Content/NHOS/Data/free_mode.json`, the same way the relay's own free mode does. A packaged build still sends analytics events to the relay in free mode, as in every mode (`BPC_Analytics`, T68), unless they are turned off. The editor (PIE, and game windows started from it) sends none unless `Local/switches.json` has `"analytics": "test"`, which marks every event as a test; use that only for a check that needs the events, and keep `"analytics": "off"` otherwise.

### 9b. `CLAUDE.md`, "Package a Windows build"

Replace

> It reads the API keys from `Packaged/Windows/AIMegaJam2026/Local/llm_key.json`. Delete that file before you zip a build.

with

> It reads the API keys from `Packaged/Windows/AIMegaJam2026/Local/llm_key.json`, and the switches from `Local/switches.json` in the same folder. A packaged build sends real analytics events (T68), so before you test one, put `{"analytics": "off"}` (or `"test"`) in that `switches.json`, or add the package's player id (its log prints `NHOS: ANALYTICS player <id>`) to `ignore_players` in `Local/stats.json`. Delete both files before you zip a build.

### 9c. `Docs/ItchPage.md`

- **"#### Test for Free"** (line 92): "No internet and no keys." → "No keys, and no internet needed."
- **"### What gets sent where"** (line 122): replace the first bullet

  > - **Test for Free** sends nothing anywhere.

  with

  > - **Test for Free** makes no AI call. It sends only the play stats below.

  and add this bullet after the AI-actors bullet:

  > - **Play stats.** Every way to play sends our relay a few anonymous events: a random player id the game makes on your first launch (nothing from your Epic account, your computer or your keys), which way you play, how far each show gets, how many AI calls went to each lab with their token counts, and the kind of any error. Never your typed lines, your keys or your address (the relay keeps only a hash of it, salted with the day, as it does for the call limits). Turn them off on the title screen with **Play stats**.

- T69 adds "a few words naming an action the game can't do yet" to what is sent; part 11 tells it.

### 9d. `Relay/README.md`, the relay's free mode (line 36)

After the **Free mode** paragraph (it ends with the canned reply's description), add a paragraph:

> The game's own **Test for Free** doesn't use this flag: it builds its replies itself and makes no LLM call. A packaged build still sends analytics events to `/event` in Test for Free, as in every mode, unless the player turns Play stats off or `Local/switches.json` has `"analytics": "off"` (T68).

### 9e. `Relay/README.md`, T67's `/event` section (step 4)

T67's section, "## Analytics events (`POST /event`, `GET /stats`)", already says the drop-off part of step 4, after the events table: "A show's drop-off point is the last `phase` it sent, so there is no quit event (the game can't send anything when its window closes)." So step 4 needs only what the game sends. Two edits:

1. Right after that paragraph, a new one:

   > **What the game sends (T68).** A show's events are `mode` (when no mode was picked on the title), `show_start`, a `phase` as each phase shows on screen, `calls` and `show_end`. The phases, in show order, are `scene_prep`, `turn_1` to `turn_3`, `free_talk_1` and `free_talk_2`, `last_word` (only when someone was named in Free Talk's final round), `vote` and `reactions` for each scene, then `closing`, each with its `scene`. A show with a `show_start` and no `show_end` stopped at its last `phase`. `calls` events come at each Scene Prep and at the end screen, one per provider and model, so a show that stops mid-scene still has the counts of every scene before it. `launch` uses the session id the game made at launch; every other event uses the show's.

   (With question 1's second answer: "`calls` events come at every phase and at the end screen, ...")

2. In the example body above the table, `"fields": { "phase": "free_talk", "scene": 2 }` → `"fields": { "phase": "free_talk_1", "scene": 2 }`, and `"build": "0.9"` → `"build": "2026-11-15"`, so the example is a real event.

T67's opening paragraph ("Test for Free makes no network call to it for asks") is right as it stands.

### 9f. `Docs/switches.example.json`

- Add `"analytics": "off"` after `"error_test": ""`.
- In `_readme`, replace "free makes no network call:" with "free makes no LLM call:", and add at the end:

  > analytics (T68): "off" sends no analytics event; "test" sends them marked "test": true, from the editor too, and Tools/analytics_report.py leaves them out unless given --test; missing or "" sends them only from a packaged build, as a player's game does (the editor sends none). An autoplay run sends only when it is "test". It is read once when the game loads. Keep it "off" on a dev machine.

### 9g. The relay deploy

`Relay/README.md` is under `Relay/`, so the push redeploys the relay (unchanged code). Before the closing push, ask my person with the multiple-choice tool: "Push Relay/README.md with T68 (Recommended)": the push redeploys the relay, but nothing it does changes; or "Not now": then T68 pushes without the README and leaves a `Waiting:` line in its plan entry for that file, as T55 did. An OK passed on by another session can't approve it (the dispatcher's ledger); my person types it in the T68 session.

## 10. The check

All runs in a game window on the saved assets, from the repo folder, with this PC's editor command (`CLAUDE.local.md`) plus `-log=<name>.log`; the log is `Saved/Logs/<name>.log`. Close each game window by its own process id (`tasklist` to find it), never by image name: `taskkill /IM UnrealEditor.exe` would also kill the editor. Set the switches in `Local/switches.json` before each run (the file is per machine and not in git).

### Run E first: two launches (same id, `launches` 1 then 2)

1. Delete `Saved/SaveGames/player.sav` if it exists (T68's own; nothing else writes that slot).
2. Switches: `"autoplay": false`, `"mode": "free"`, `"analytics": "test"`.
3. Launch with `-log=T68e1.log`, wait for `NHOS: TITLE shown` in the log, close it. Launch again with `-log=T68e2.log`, same.
4. Expected:

   ```bash
   grep -h "NHOS: ANALYTICS" Saved/Logs/T68e1.log Saved/Logs/T68e2.log
   ```

   `T68e1`: `new player`, `player <32 hex> test=true build=2026-11-15 relay=true packaged=false`, `launch {"launches":1,"first_seen":"<today>"}`, `ok launch`. `T68e2`: `player <the same id> ...`, `launch {"launches":2,...}`, `ok launch`. No `fail`. (JSON spacing may differ.)

### Run A: a free autoplay show, analytics on (the Done-when's first check)

1. Switches: `"autoplay": true`, `"mode": "free"`, `"fast_lines": true`, `"spare_human": true` (I am never cut, so the show runs to the final two or the last scene and passes every phase several times), `"analytics": "test"`, `"error_test": "overloaded"` (one failed actor ask per turn, so the report's errors heading and `calls`' `failed` get rows; see T37), the rest as in `Docs/switches.example.json`.
2. Launch with `-log=T68on.log`; wait for `NHOS: SHOW END`; wait 5 s more for the last acks; close it.
3. Expected:

   ```bash
   grep -hE "NHOS: (ANALYTICS|CUE stat|PREP shown|SHOW END)" Saved/Logs/T68on.log
   grep -c "LogScript" Saved/Logs/T68on.log
   ```

   - In order: `player <id> ... packaged=false`, `launch` (`launches` 3 after run E), `mode {}`, `show_start {}`, `phase {"phase":"scene_prep","scene":1}`, then per scene `turn_1` to `turn_3`, `free_talk_1`, `free_talk_2`, `last_word` (only if `NHOS: LASTWORDS ... named=` isn't `none`), `vote`, `reactions`, the next `scene_prep` preceded by its `calls` events (one per provider: `"model":"free"`, `tokens_in` 0, `failed` ≥ 1 for the providers `error_test` hit), ..., `closing`, the last `calls`, `show_end {"result":"win","reason":"final_two"}` (or `last_scene`; with `spare_human` the human is never cut, and T54's runs ended at the final two after 3 scenes). `reason` matches the `NHOS: SHOW END reason=` line.
   - `error {"kind":"overloaded"}` lines (the `errors.json` case `ErrorKind` gave; check it against the `NHOS: ERROR ... where=turn` lines).
   - An `ok <event>` for every sent event, and no `fail` line.
   - `LogScript`: 0.
4. **The order check:** this script prints each show's phase list and fails on a missing phase, an `ok` count short of the sends, or a `fail`:

   ```bash
   python - Saved/Logs/T68on.log <<'EOF'
   import json, re, sys
   lines = open(sys.argv[1], encoding="utf-8", errors="replace").read().splitlines()
   sent, ok, fail, phases = [], 0, 0, []
   for l in lines:
       m = re.search(r"NHOS: ANALYTICS (\S+) ?(.*)$", l)
       if not m: continue
       ev, rest = m.groups()
       if ev == "ok": ok += 1
       elif ev == "fail": fail += 1; print("FAIL", rest)
       elif ev in ("player", "off", "new", "toggle"): pass
       else:
           sent.append(ev)
           if ev == "phase": f = json.loads(rest); phases.append((f["scene"], f["phase"]))
   print("sent", len(sent), "ok", ok, "fail", fail)
   for e in ["launch", "mode", "show_start", "calls", "show_end"]:
       print(e, sent.count(e))
   scenes = sorted({s for s, p in phases if p != "closing"})
   bad = 0
   for s in scenes:
       got = [p for sc, p in phases if sc == s and p != "closing"]
       want = ["scene_prep", "turn_1", "turn_2", "turn_3", "free_talk_1", "free_talk_2"] + (["last_word"] if "last_word" in got else []) + ["vote", "reactions"]
       print("scene", s, " ".join(got), "" if got == want else "  <-- want " + " ".join(want))
       bad += got != want
   print("closing", [p for s, p in phases].count("closing"))
   sys.exit(1 if bad or fail or ok != len(sent) or sent[-1] != "show_end" else 0)
   EOF
   ```

5. **The report** (run it after run D, so its `analytics_off` is in too): `python Tools/analytics_report.py --test --since <today>` shows run A's show (and run E's launches) under every heading T67 prints: `players` (the id, counted under "came back", launches over 1), `modes` (`free`), `drop-off` (the show reaching `scene <n>, closing`, and its `show_end` result), `calls` (four providers, model `free`, with failures), `errors` (`overloaded`) and `turned off` (run D). `unsupported actions` stays `(none)` until T69. Without `--test` none of it appears.

### Run B: analytics off (the Done-when's second check)

1. Switches as run A, but `"analytics": "off"` and `"error_test": ""`.
2. Launch with `-log=T68off.log`, wait for `NHOS: SHOW END`, close it.
3. Expected: `grep -h "NHOS: ANALYTICS" Saved/Logs/T68off.log` prints exactly one line, `NHOS: ANALYTICS off why=switch player=<run E's id> packaged=false`. `NHOS: CUE stat` lines still print (the queue runs the same). `SHOW END` reached, `LogScript` 0.
4. **Run C (builds only):** the same with `"analytics": ""` prints only `NHOS: ANALYTICS off why=editor player=<id> packaged=false`: a game window from the editor sends nothing without `test`. A short run is enough: close it after `NHOS: PREP shown scene=1`.

### Run D: PIE, the title and the toggle (the Done-when's third check)

1. Switches: `"autoplay": false`, `"analytics": "test"`, `"error_test": ""`, `"fast_lines": false`, `"spare_human": false`. Follow your brief's rule for starting PIE, and check `Agents/status/` that nobody else drives the editor.
2. PIE in a 1600 × 900 floating window. Screenshot the title: `Saved/T68/shots/title_p16.png` (not in git): the "Play stats: on" button with its caption under the three ways to play, in the playbill's paper style, no clipping. Also at 1280 × 720: `title_p12.png`.
3. Tab to Play stats (four Tabs from Play via Relay; the gold ring shows on it: `stats_focus.png`), press Enter: the label reads "Play stats: off" (`stats_off.png`), and the log prints `NHOS: TITLE click stats=off`, `NHOS: ANALYTICS analytics_off {}`, `NHOS: ANALYTICS toggle off`, then `NHOS: ANALYTICS ok analytics_off`.
4. Click Test for Free and play into turn 1 (or the whole scene). The log has **no** `NHOS: ANALYTICS <event>` line after `analytics_off` (no `mode`, `show_start` or `phase`), and the `NHOS: CUE stat` lines still print.
5. Stop PIE. Start PIE again: the title reads "Play stats: off" (the save kept it), and the log prints `NHOS: ANALYTICS off why=player player=<id> packaged=false` and no `launch`. Press Enter on Play stats again: "Play stats: on", `NHOS: ANALYTICS toggle on`, nothing sent for it. Stop PIE.
6. **As a first-time player** (write it under Findings): is the line findable but quiet, does "Play stats" read as a choice and not a mode, does the playbill still read top to bottom.

### Run F: a packaged build knows it is one (the task's "Builds only" finding)

1. Package a Windows build with `CLAUDE.local.md`'s command, from a `.bat` file run with `cmd //c` (`CLAUDE.md`), in the background (about 6 minutes the first time). It cooks with `UnrealEditor-Cmd.exe` in its own process, so the open editor can stay open; if the cook complains about a locked file, tell my person and wait.
2. Put `{"analytics": "off", "autoplay": false}` in `Packaged/Windows/AIMegaJam2026/Local/switches.json` (make the folder), so this run sends nothing real.
3. Start `Packaged/Windows/AIMegaJam2026.exe -windowed -ResX=1600 -ResY=900`, wait for `NHOS: TITLE shown` in `Packaged/Windows/AIMegaJam2026/Saved/Logs/AIMegaJam2026.log`, close it by its process id.
4. Expected: `NHOS: ANALYTICS off why=switch player=<a new id> packaged=true`, and `NHOS: ANALYTICS new player` (the package keeps its own save). Write the test (`Content/Paks/` exists) and this line under Findings. The id is this PC's packaged id for `ignore_players` (part 3).
5. Delete `Packaged/Windows/AIMegaJam2026/Local/switches.json` afterwards (and never zip it; part 9b). `Packaged/` is ignored by git.

### Clean up

Set `"analytics": "off"`, `"autoplay": false`, `"error_test": ""`, `"spare_human": false`, `"fast_lines": false` in `Local/switches.json`. Close every game window. `python Tools/check_prompts.py --offline` passes.

## 11. The commit

One commit, `T68: The game sends its analytics events` (or two, the second for the README after my person's OK, part 9g): `Content/NHOS/Core/BPC_Analytics.uasset`, `Content/NHOS/Core/SG_Player.uasset`, `Content/NHOS/Core/BP_Show.uasset`, `Content/NHOS/Core/BPC_LLMClient.uasset`, `Content/NHOS/UI/WBP_Title.uasset`, `Content/NHOS/Data/llm.json`, `Docs/switches.example.json`, `Docs/ItchPage.md`, `CLAUDE.md`, `Relay/README.md` (after the OK), `Tools/check_prompts.py` (question 2), the `Graphs/` files (`BPC_Analytics/*` new; `SG_Player/*` new; `BP_Show/CueHeader.txt`, `RunCue.txt`, `OpenPrep.txt`, `DrawCast.txt`, `ShowTitle.txt`; `BPC_LLMClient/LoadConfig.txt`, `HandleHttp.txt`, `SetMode.txt`, `Ask.txt`, `Deliver.txt`, `BackstageNote.txt`, `HealthFail.txt`, `NoteModel.txt`, `CountCall.txt`, `FlushCalls.txt` new; `WBP_Title/EventGraph.txt`, `ShowStats.txt` new), `Docs/tasks/T68.md` (Result, Findings: the answers to the two questions, the decisions above as built, the header texts found in part 0 step 6, every place a name differed from this sheet, the event count of run A's show), `Docs/Plan.md` (the box, the entry moved to Done), `Docs/DevLog.md` (one line), and the note in `Agents/` (part 3). Stage each by path. Unlock the five assets after the push.

## 12. What T69 gets from T68

- **`BPC_Analytics.Send(Event, Fields)`**, callable from `BP_Show` and `BPC_LLMClient` (their `Analytics` / `Stats` references) and from a widget (`Class|BPShow|GetAnalytics` on the `BP_Show` actor, as `WBP_Title` does). T69's `unsupported` event: `Fields` with `words`, `source`, `phase`.
- **`BPC_Analytics.CurPhase`** (and `CurScene`): the key of the phase on screen, for `unsupported`'s `phase`. It is set when the phase shows (screen time), which is when the player types or clicks.
- Off, test and autoplay behave for `unsupported` as for every event: `Send` decides.
- The privacy line (part 9c) needs T69's words added; T69's Touches don't name `Docs/ItchPage.md` (part 13).

## 13. Knock-on: tell, don't change

- **T67 (the Mac):** question 1's event count against `limits.ip_daily_events` (500 real events, "about 20 shows"). The rest of T67 fits as pushed (`69988c5`).
- **T69:** `ItchPage.md`'s Play stats bullet should add "and a few words naming an action you tried that the game can't do yet (never your typed line)" once T69 sends them; T69's Touches don't name that file, so either T69 widens them or T70 adds it.
- **T34 (after T68):** if it renames a phase header ("the header needs only the turn", T53), it must change `BPC_Analytics.PhaseKey` (T68) and `BPC_ShowAudio.PhaseKey` (T71) to match, or the phase events and the music stop following the phases. Its check: a free autoplay run with `"analytics": "test"` and part 10's order script.
- **T61 (after T68):** its tips toggle goes in `HowFrame` (T61-build 5a); T68's Play stats button sits on the playbill under the mode buttons, so Tab order becomes: three modes, Play stats, How to play, Stagehand tips. T61's `RunCue` `"end"` branch and `OpenPrep` calls go next to T68's nodes.
- **T73 (before T68):** if it gives every cue a default hold in `pacing.json` or `CueHoldFor`, the `"stat"` cue must stay at 0.
- **T70:** set `llm.json`'s `build` to the day it packages; test the package with `{"analytics": "test"}` in its `Local/switches.json` and delete that file before zipping (part 9b); the itch page's privacy line is in (part 9c).
- **Both machines:** `"analytics": "off"` in each `Local/switches.json` (the `Agents/` note, part 3).

## 14. The task's steps and checks, and where this sheet covers them

| T68.md | This sheet |
|---|---|
| Step 1, the player id (`SG_Player`) | Part 1; `Init`, `NewSave`, `Launch` in 2b; decisions 2, 3, 6 |
| Step 2, `BPC_Analytics` and `Send` (body, relay address, no wait, the prints, `session`, `build`, `mode`) | Part 2; decisions 4, 5, 15, 18 |
| Step 3, `launch` | 2b `Launch`; 4f; decision 1 |
| Step 3, `mode` | 2b `ModePicked`, `ShowStart`; 5d |
| Step 3, `show_start` | 2b `ShowStart`; 4e |
| Step 3, `phase` (where every phase passes) | 2b `PhaseKey`, `CuePhase`, `SendPhase`; 4b, 4c, 4d; decisions 7 to 10 |
| Step 3, `show_end` with `WinReason` | 2b `ShowEnd`; 4c |
| Step 3, `error` with `ErrorKind`'s case | 2b `Error`; 5c, 5g; decisions 13, 14 |
| Step 3, `calls` (per provider and model, tokens, flush and clear) | 5a, 5e, 5f, 5h; 2b `SendPhase`, `ShowEnd`; question 1; decisions 11, 12 |
| Step 4, drop-off in T67's README section | 9e |
| Step 5, the title toggle and `analytics_off` | Part 6; 2b `SetOn`, `IsOn`; decisions 16, 17 |
| Step 5, the `analytics` switch, `switches.example.json`, this machine, autoplay | Part 3; 9f; decision 19 |
| Step 5, builds only (a check true only in a packaged build, in Findings) | `Init` in 2b; part 3's table; decision 20; runs C and F |
| Step 5, our own machines (`NHOS: ANALYTICS player <id>`, `ignore_players`) | `Init` in 2b; part 3; decision 21; runs E and F |
| Step 6, the docs on free mode | 7 (`llm.json`), 9a, 9d, 9f |
| Step 7, the itch page's privacy line | 9c |
| Done when: the free autoplay show with `test` | Part 10, run A |
| Done when: `off` prints only the off line | Run B (and run C) |
| Done when: PIE screenshot, the toggle, nothing after `analytics_off` | Run D |
| Done when: a second launch shows `launches` 2 | Run E |
| Done when: switches back | Clean up |
