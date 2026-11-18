# T102 build sheet: import the music, three new music keys, the mix and the recordings

Back to [T102](T102.md). A Mac prep session wrote this on 2026-11-18, without the editor. It is a plan, not a record: nothing here was written to the editor or to `Graphs/`. When T102 writes a graph, it updates that graph's file in `Graphs/` as usual. Every loudness number here comes from a run of [`Tools/measure_loudness.py`](../../Tools/measure_loudness.py) on 2026-11-18 (part 3 has the command).

## Written against, and what to re-check

**Written against `dev` at `bcd21ce`** (the plan with T107 added). At that commit:

- **T101 is still running** (`t101-audio-picks`): the show, robot and UI sounds and the bots' new voices aren't picked yet. Part 2b is a marked gap for them.
- **T107 is building** (`WBP_Stage`, `BP_StageDirector`, `BPC_LLMClient`, `BPC_LinePlayer`). None of them is in this sheet.
- **T84** comes before T102 in the editor lane and changes `BP_Show`. Its sheet doesn't touch `OpenPrep`.

Before T102 writes anything:

1. `git log --oneline bcd21ce..HEAD -- Graphs/BPC_ShowAudio Graphs/BP_Show/OpenPrep.txt Graphs/BP_Show/RunCue.txt` should print nothing. If it prints a commit, merge that change into the drafts in part 1 by meaning.
2. `git log --oneline bcd21ce..HEAD -- SourceAssets/Audio/music/t100` should print nothing. If the loops changed, run part 3's command again and take the new wave volumes.
3. T101's picks: read "For T102" in `Docs/tasks/T101.md` and its rows in `Docs/AudioShortlist.md`, then fill part 2b.
4. `git lfs locks`: no lock on `BPC_ShowAudio.uasset`, `BP_Show.uasset`, `Content/NHOS/Audio/**` or `SC_*.uasset` that some other session holds.

## In short

| T102 step | Where in this sheet |
|---|---|
| 1. Read first | This sheet holds it. `Docs/tasks/T101.md` "For T102" is the only other thing to read |
| 2. Even loudness | Part 3 (the numbers, the targets, the wave volumes) |
| 3. Import in place | Part 2 (the list and the import script) |
| 4. The three new music keys | Part 1 (the three graphs), part 4a (the log check) |
| 4. The Reactions loop under the stinger | Part 4b (it does start under it today: a later start is drafted) |
| 5. The mix | Part 3c (class and wave volumes), part 4d (a duck while lines type, only if needed) |
| 6. Record the game | Part 4c |
| 7. Record it in the docs | Not in this sheet. Part 3 has the targets and levels to write in `Docs/AudioShortlist.md` |

- **Assets that change:** 13 reimports and 3 new sound waves in `Content/NHOS/Audio/Music/`, `SC_Music`, `SC_Effects`, `SC_Voice`, `BPC_ShowAudio` (`PhaseKey`, `TrackFor`, and if part 4b is built, `PlayPhase`, `Reveal`, `EndCheer` and a new `ReactLater`), and `BP_Show` (one pin in `OpenPrep`). Plus T101's sounds (part 2b).
- **Graphs with splices** (`SwapMusic`, `StopMusic`, `DuckMusic`): nothing in this sheet rewrites them. Part 4d would add a splice to `Syllable` only if the duck is built.
- **No new `NHOS:` line** except the three new values of `NHOS: SOUND music <key>`.
- **Costs money:** nothing. Every show in this sheet is a free show.

## Decisions this sheet makes (open to change)

1. **Raise the talk, don't only lower the music.** The measured numbers (part 3b) show that the music plays 9 to 16 dB **louder** than the syllables today, not under them. The targets put the syllables up 10 dB and the music down about 9 dB. The game as a whole stays at about the loudness it has now.
2. **One music target for all 16 loops**, the title and end screens too (Done-when 2). If the title sounds too quiet with nothing over it, raise it by ear and write that down as the one exception.
3. **Levels go on the wave's Volume, not into the files.** The FLAC files stay as T100 made them, and every reference stays. The class volumes are the master faders, so step 6's changes by ear are one number each.
4. **The Reactions loop starts later** (part 4b): the old logs show that the `REACTIONS` header comes 0.3 s after the stinger at a fast pace.
5. **The recorder lives in `BPC_ShowAudio` and runs only with `-NHOSRec` on the command line** (part 4c), so it can't run in a player's game.

## 0. The order of the build

T18, T20 and T63: a call node made before a compile has the old pins, so create each function and variable first, compile, then write the graphs callee first. `TrackFor` names the three new assets as literals, so import them before you write it.

1. Do the checks under "Written against". Claim T102 (`git lfs lock Docs/claims/T102`), and lock `Content/NHOS/Core/BPC_ShowAudio.uasset`, `Content/NHOS/Core/BP_Show.uasset`, the 13 `Content/NHOS/Audio/Music/S_Music*.uasset`, `Content/NHOS/Audio/SC_Music.uasset`, `SC_Effects.uasset`, `SC_Voice.uasset`, and the T101 assets part 2b names. Set `Editor: driving` in your status file.
2. **Import** the 16 loops (part 2a), then T101's sounds (part 2b). Set each one's settings and Volume (part 3c). Save.
3. **`BPC_ShowAudio`:** add the variables and the empty functions of part 4b (`RevealAt`, `ReactDelay`, `ReactLater`) and part 4c (`RecN`, `RecName`, `RecLive`, `RecMax`, `RecPhase`, `RecStop`), if you build them. Compile.
4. Write `PhaseKey` and `TrackFor` (part 1), then `ReactLater`, `PlayPhase`, `Reveal` and `EndCheer` (part 4b), then `RecStop`, `RecPhase` and `PlayMusic` (part 4c). Compile with warnings as errors. Save.
5. **`BP_Show.OpenPrep`:** the one pin (part 1c). Compile. Save.
6. **The class volumes** (part 3c). Save.
7. The checks: part 4a's log check on a free autoplay show with `fast_lines`, then part 4c's recordings without `fast_lines`.

**How to write a graph from this sheet** (T71's rules): copy the source into `Saved/T102/<Graph>.txt` with a `;;; GRAPH <Graph>` line in front, expand it with `python Tools/dslpp.py`, read the expanded file inside `execute_tool_script` with `AssetTools.read_file` and pass it to `BlueprintTools.write_graph_dsl`. Then put the source in `Graphs/<Blueprint>/<Graph>.txt` without the `;;; GRAPH` line. `write_graph_dsl` leaves the old nodes behind, cut off from the entry. That is harmless (T50, T71).

## 1. The three graphs of step 4

None of the three has a splice, so each can be written again whole from its source.

### 1a. `BPC_ShowAudio.PhaseKey`

What changes:

- **`SCENE PREP`**: the `return` after `StartsWith "SCENE PREP"` gives `"scene_prep"` in place of `"card"`. No `phase` cue carries this header today: `ShowPrep` sets the Scene Prep header straight on the stage, and `OpenPrep` asks for `"scene_prep"` itself (part 1c). The line keeps a later `phase` cue right.
- **New: `LAST WORD`** gives `"last_word"`. It goes before `THE CUT`, and the order doesn't matter, because no header starts with two of the prefixes.
- **New: `REACTIONS`** gives `"reactions"`.
- `THE SCENE` still gives `"card"`, `FREE TALK` gives `"free_talk"`, and `THE CUT` gives `"cut"`.
- These headers still give `""`, so the loop that plays goes on: `SCENE n: FREE TALK IS OVER` (it starts with "SCENE ", not "SCENE PREP"), `THE SHOW IS OVER` and T87's `THE REVEAL`. The log of 2026-11-18 shows that `SCENE n: FREE TALK IS OVER` comes **after** `LAST WORD: SCENE n`, so the Last Word loop plays until `THE CUT`.

```
; T71: the music key for the header a "phase" cue carries (BP_Show.CueHeader).
; "card" means the card in play. "" means no track of its own: the loop that plays goes on.
; Headers: "SCENE PREP: SCENE n", "THE SCENE: SCENE n, ...", "FREE TALK: SCENE n...", "LAST WORD: SCENE n",
; "SCENE n: FREE TALK IS OVER", "THE CUT: ...", "REACTIONS: SCENE n", "THE SHOW IS OVER", "THE REVEAL" (T87).
; T102: Scene Prep, Last Word and Reactions have their own loops. No phase cue carries "SCENE PREP" today:
; OpenPrep asks for "scene_prep" itself. "SCENE n: FREE TALK IS OVER", "THE SHOW IS OVER" and "THE REVEAL" give "".
(fn PhaseKey (Text)
  (if (Utilities|String|StartsWith :SourceString Text :InPrefix "SCENE PREP")
    (return "scene_prep"))
  (if (Utilities|String|StartsWith :SourceString Text :InPrefix "THE SCENE")
    (return "card"))
  (if (Utilities|String|StartsWith :SourceString Text :InPrefix "FREE TALK")
    (return "free_talk"))
  (if (Utilities|String|StartsWith :SourceString Text :InPrefix "LAST WORD")
    (return "last_word"))
  (if (Utilities|String|StartsWith :SourceString Text :InPrefix "THE CUT")
    (return "cut"))
  (if (Utilities|String|StartsWith :SourceString Text :InPrefix "REACTIONS")
    (return "reactions"))
  (return ""))
```

### 1b. `BPC_ShowAudio.TrackFor`

What changes: three new `if` nodes that return the three new assets. The cook packs only the assets something references, and these literals are that reference.

- `"scene_prep"` gives `/Game/NHOS/Audio/Music/S_MusicScenePrep.S_MusicScenePrep`, after `"title"`.
- `"last_word"` gives `/Game/NHOS/Audio/Music/S_MusicLastWord.S_MusicLastWord`, after `"free_talk"`.
- `"reactions"` gives `/Game/NHOS/Audio/Music/S_MusicReactions.S_MusicReactions`, after `"cut"`.
- The other 12 keys and the `S_MusicShow` fallback don't change. The comment changes.

Import the three assets first (part 2a). A literal for an asset that doesn't exist yet doesn't resolve.

```
; T71: the loop for each music key. A key with no track of its own ("show", or a card added later) gets the show loop.
; Every track is named here, so the cook packs each one.
; T102: Scene Prep, Last Word and Reactions have their own loops (T100's picks): 15 keys, 15 tracks, plus the fallback.
(fn TrackFor (Key)
  (if (streq Key "title")
    (return "/Game/NHOS/Audio/Music/S_MusicTitle.S_MusicTitle"))
  (if (streq Key "scene_prep")
    (return "/Game/NHOS/Audio/Music/S_MusicScenePrep.S_MusicScenePrep"))
  (if (streq Key "space_plans")
    (return "/Game/NHOS/Audio/Music/S_MusicSpacePlans.S_MusicSpacePlans"))
  (if (streq Key "mine_bridge")
    (return "/Game/NHOS/Audio/Music/S_MusicMineBridge.S_MusicMineBridge"))
  (if (streq Key "dino_island")
    (return "/Game/NHOS/Audio/Music/S_MusicDinoIsland.S_MusicDinoIsland"))
  (if (streq Key "favor_father")
    (return "/Game/NHOS/Audio/Music/S_MusicFavorFather.S_MusicFavorFather"))
  (if (streq Key "glowing_briefcase")
    (return "/Game/NHOS/Audio/Music/S_MusicGlowingBriefcase.S_MusicGlowingBriefcase"))
  (if (streq Key "league_night")
    (return "/Game/NHOS/Audio/Music/S_MusicLeagueNight.S_MusicLeagueNight"))
  (if (streq Key "pick_a_pill")
    (return "/Game/NHOS/Audio/Music/S_MusicPickAPill.S_MusicPickAPill"))
  (if (streq Key "free_talk")
    (return "/Game/NHOS/Audio/Music/S_MusicFreeTalk.S_MusicFreeTalk"))
  (if (streq Key "last_word")
    (return "/Game/NHOS/Audio/Music/S_MusicLastWord.S_MusicLastWord"))
  (if (streq Key "cut")
    (return "/Game/NHOS/Audio/Music/S_MusicCut.S_MusicCut"))
  (if (streq Key "reactions")
    (return "/Game/NHOS/Audio/Music/S_MusicReactions.S_MusicReactions"))
  (if (streq Key "win")
    (return "/Game/NHOS/Audio/Music/S_MusicWin.S_MusicWin"))
  (if (streq Key "lose")
    (return "/Game/NHOS/Audio/Music/S_MusicLose.S_MusicLose"))
  (return "/Game/NHOS/Audio/Music/S_MusicShow.S_MusicShow"))
```

### 1c. `BP_Show.OpenPrep`: one pin

What changes: **the `Key` pin of the `BPC_ShowAudio.PlayMusic` call** takes the literal `"scene_prep"` in place of the `CardId` getter `(V CardId)`. The getter that fed it is then left with no link: delete it. The comment's T71 line changes to match. Nothing else in `BP_Show` changes (my person's call on 2026-11-17).

- **In the editor:** break the link from `Get CardId` to `Play Music`'s `Key`, type `scene_prep` into `Key`, and delete the loose `Get CardId` node. Or write the whole graph again from the source below (it has no splice). Either way, the file in `Graphs/BP_Show/OpenPrep.txt` becomes the source below.
- **Why it's enough:** the card's loop then starts at the first `THE SCENE` cue through `PlayPhase`, which already sends `"card"` to `PlayMusic` with `CardId`. Before T102, `THE SCENE` asked for the same key that was already playing and did nothing; now it swaps, with T71's 1 s cross-fade.
- **Play Again within 3 s of the end screen:** `RestartShow` reaches `OpenPrep` in the same frame, so `MusicKey` is `"scene_prep"`, not empty, and `EndMusic` stays out of the way as before.

```
; T28: Scene Prep shows the whole card. T71: a music loop starts here, for every scene (scene 1 too, whose
; Scene Prep doesn't come through a "prep" cue). T102: it's Scene Prep's own loop ("scene_prep"); the card's loop
; starts at the first "THE SCENE" cue (BPC_ShowAudio.PlayPhase). ScenePrep has set CardId before it calls OpenPrep.
; T68: each Scene Prep sends its analytics phase (and the call counts so far).
; T77: a new scene starts with no kept emotion (closing lines keep one that never plays).
(fn OpenPrep ()
  (clear (V SeatEmo))
  (Class|WBPStage|SetPrepMode :self (Variables|Default|GetStage) :Prep true)
  (Class|BPCShowAudio|PlayMusic :self (V Audio) :Key "scene_prep")
  (Development|PrintString (Utilities|String|Append "NHOS: PREP shown scene=" (Utilities|String|ToString(Integer) (Variables|Default|GetSceneNum))) false)
  (Class|BPCAnalytics|SendPhase :self (V Analytics) :Key "scene_prep" :Scene (Variables|Default|GetSceneNum))
  (CallFunction|LoadSwitches)
  (if (Variables|Default|GetAutoplay)
    (CallFunction|StartFromPrep)))
```

A string literal on `PlayMusic`'s `Key` pin is the form `ShowTitle` already uses (`:Key "show"` and `:Key "title"`).

## 2. The import list

### 2a. T100's 16 loops

All are `SourceAssets/Audio/music/t100/<file>`: 16-bit, 44.1 kHz stereo FLAC, cut on bar lines with the seam blended (T100). Every asset is in `/Game/NHOS/Audio/Music/`.

**Settings to check on every one:** `Looping` on, `Sound Class` = `/Game/NHOS/Audio/SC_Music`, `Volume` = the column below (part 3c says where it comes from). Leave the other settings at what the reimport keeps, or at the defaults for the three new ones. Pitch stays 1.0.

| # | Source file | Key | Asset | New or replaces | Length | Measured LUFS | Volume |
|---|---|---|---|---|---|---|---|
| 1 | `01_title.flac` | `title` | `S_MusicTitle` | replaces | 69.1 s | -14.5 | 0.167 |
| 2 | `02_scene_prep.flac` | `scene_prep` | `S_MusicScenePrep` | **new** | 70.0 s | -14.5 | 0.168 |
| 3 | `03_space_plans.flac` | `space_plans` | `S_MusicSpacePlans` | replaces | 62.8 s | -17.3 | 0.232 |
| 4 | `04_mine_bridge.flac` | `mine_bridge` | `S_MusicMineBridge` | replaces | 82.3 s | -13.7 | 0.154 |
| 5 | `05_dino_island.flac` | `dino_island` | `S_MusicDinoIsland` | replaces | 73.8 s | -14.0 | 0.159 |
| 6 | `06_favor_father.flac` | `favor_father` | `S_MusicFavorFather` | replaces | 84.0 s | -13.8 | 0.154 |
| 7 | `07_glowing_briefcase.flac` | `glowing_briefcase` | `S_MusicGlowingBriefcase` | replaces | 89.5 s | -13.8 | 0.154 |
| 8 | `08_league_night.flac` | `league_night` | `S_MusicLeagueNight` | replaces | 81.8 s | -13.6 | 0.152 |
| 9 | `09_pick_a_pill.flac` | `pick_a_pill` | `S_MusicPickAPill` | replaces | 61.4 s | -13.7 | 0.152 |
| 10 | `10_free_talk.flac` | `free_talk` | `S_MusicFreeTalk` | replaces | 81.6 s | -14.3 | 0.165 |
| 11 | `11_last_word.flac` | `last_word` | `S_MusicLastWord` | **new** | 68.6 s | -13.2 | 0.145 |
| 12 | `12_cut.flac` | `cut` | `S_MusicCut` | replaces | 85.7 s | -13.9 | 0.158 |
| 13 | `13_reactions.flac` | `reactions` | `S_MusicReactions` | **new** | 76.6 s | -14.3 | 0.164 |
| 14 | `14_win.flac` | `win` | `S_MusicWin` | replaces | 77.4 s | -14.6 | 0.169 |
| 15 | `15_lose.flac` | `lose` | `S_MusicLose` | replaces | 80.0 s | -13.8 | 0.155 |
| 16 | `16_show.flac` | `show` (the fallback) | `S_MusicShow` | replaces | 79.2 s | -13.1 | 0.142 |

- **Old settings that go away:** T71's wave volumes (0.62 to 2.11) are replaced by the column above. Check one old asset first (`S_MusicCut`: `Looping` on, `SC_Music`, Volume 0.62) to confirm the Python property names in the script below.
- **No old music asset is left over:** all 13 old ones are replaced. The Kenney `.ogg` files in `SourceAssets/Audio/music/` are T101's to keep or drop, not T102's.
- **Size:** about 109 MB of FLAC in all. The cook compresses sound waves, so expect far less in the pak. Note the pak size before and after in the task's findings.

**The import, in the editor's Python** (inside `execute_tool_script`, or as an editor script). It imports from `SourceAssets/` straight into each asset by name, so the auto-import note T20 and T71 hit never comes up, and every reference stays. Run it in four calls of four files each (`PICKS[0:4]`, `PICKS[4:8]`, and so on), since a long call stops Claude Code waiting.

```python
import os, unreal
ROOT = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
SRC = os.path.join(ROOT, "SourceAssets/Audio/music/t100")
PICKS = [  # (source file stem, asset name, Volume)
    ("01_title", "S_MusicTitle", 0.167), ("02_scene_prep", "S_MusicScenePrep", 0.168),
    ("03_space_plans", "S_MusicSpacePlans", 0.232), ("04_mine_bridge", "S_MusicMineBridge", 0.154),
    ("05_dino_island", "S_MusicDinoIsland", 0.159), ("06_favor_father", "S_MusicFavorFather", 0.154),
    ("07_glowing_briefcase", "S_MusicGlowingBriefcase", 0.154), ("08_league_night", "S_MusicLeagueNight", 0.152),
    ("09_pick_a_pill", "S_MusicPickAPill", 0.152), ("10_free_talk", "S_MusicFreeTalk", 0.165),
    ("11_last_word", "S_MusicLastWord", 0.145), ("12_cut", "S_MusicCut", 0.158),
    ("13_reactions", "S_MusicReactions", 0.164), ("14_win", "S_MusicWin", 0.169),
    ("15_lose", "S_MusicLose", 0.155), ("16_show", "S_MusicShow", 0.142),
]
DEST = "/Game/NHOS/Audio/Music"
SC_MUSIC = unreal.load_asset("/Game/NHOS/Audio/SC_Music")

def run(batch, ext=".flac", src=SRC):
    tasks = []
    for stem, asset, _ in batch:
        t = unreal.AssetImportTask()
        t.filename = os.path.join(src, stem + ext)
        t.destination_path = DEST
        t.destination_name = asset
        t.replace_existing = True          # reimport into the old asset: same object, same references
        t.replace_existing_settings = False
        t.automated = True                 # no dialogs
        t.save = False
        tasks.append(t)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    for (stem, asset, vol), t in zip(batch, tasks):
        got = list(t.imported_object_paths)
        if not got:
            print("NOT IMPORTED", stem)
            continue
        w = unreal.load_asset(f"{DEST}/{asset}")
        w.set_editor_property("looping", True)
        w.set_editor_property("sound_class_object", SC_MUSIC)
        w.set_editor_property("volume", vol)
        print(asset, round(w.get_editor_property("duration"), 1), "s", w.get_editor_property("num_channels"), "ch",
              w.get_editor_property("sound_class_object").get_name(), w.get_editor_property("volume"))

run(PICKS[0:4])
```

- **Check each print:** the length matches the table within 0.1 s, 2 channels, `SC_Music`, the Volume. Then `save_assets` with the 16 paths (an empty list saves every dirty asset, `L_Stage` included: T20).
- **If it prints `NOT IMPORTED`** (the importer refuses FLAC, which T100 couldn't check), make WAVs outside `Content/` and run the same batch on them. The command is bit-identical (T100, checked on one file):

  ```bash
  mkdir -p Saved/T102/wav && for f in SourceAssets/Audio/music/t100/*.flac; do afconvert -f WAVE -d LEI16 "$f" "Saved/T102/wav/$(basename "${f%.flac}").wav"; done
  ```

  Then `run(PICKS[0:4], ".wav", os.path.join(ROOT, "Saved/T102/wav"))`. On Windows, `afconvert` doesn't exist: there, use `ffmpeg -i in.flac -c:a pcm_s16le out.wav` if it's installed, or import on the Mac.
- **If a property name fails** (`looping`, `sound_class_object`, `volume`, `duration`, `num_channels`), read the names on `S_MusicCut` first with `get_editor_property` and fix the script. These are the Python names of `bLooping`, `SoundClassObject`, `Volume`, `Duration` and `NumChannels`.
- **Afterwards:** `BPC_ShowAudio` compiles with no warning, and `find_package_referencers_for_asset` on two replaced assets (`S_MusicCut`, `S_MusicTitle`) still lists `BPC_ShowAudio`.

### 2b. GAP: T101's picks (the show, robot and UI sounds and the bots' voices)

**T101 hadn't picked them when this sheet was written.** Fill this table from "For T102" in `Docs/tasks/T101.md` and T101's rows in `Docs/AudioShortlist.md`. Then run part 3's command on T101's folders (`SourceAssets/Audio/Show`, `Robot`, `UI` and `voices/<provider>`, as T101 names them) and take each Volume from part 3c's formula.

| Asset (all exist today) | Sound class | Looping | Plays from | Group in part 3c |
|---|---|---|---|---|
| `Show/S_DrumRoll` | `SC_Effects` | off | `StartDrum` | Drum roll |
| `Show/S_StingHuman`, `Show/S_StingAI` | `SC_Effects` | off | `Reveal` → `Sfx` | Show |
| `Show/S_Applause`, `Show/S_ApplauseWin`, `Show/S_Laughs` | `SC_Effects` | off | `Crowd`, `EndCheer`, the `tie` cue → `Sfx` | Show |
| `UI/S_Click`, `UI/S_Hover` | `SC_Effects` | off | every button (`UIStyle.MakeButton`) | Robot and UI |
| `Robot/S_Step0` to `S_Step4`, `S_Grab`, `S_Throw`, `S_Land` | `SC_Effects` | off | `BP_Robot.Snd` | Robot and UI |
| `Robot/S_TalkBlip` | `SC_Voice` | off | `Sfx "blip"`, `BP_Show.LineBlip` | Voice, or delete (below) |
| `Voice/<Provider>/S_Voice<Provider>_NN` (41 clips) | `SC_Voice` | off | `Syllable` | Voice |
| `Voice/Me/S_VoiceMe_00` to `_11` | `SC_Voice` | off | `Syllable` | Voice: **the files stay as they are** (Done-when 1) |

- **Import in place** with the same `AssetImportTask` as part 2a (`replace_existing` on, the asset's folder and name), with `looping` off and the sound class above.
- **A new clip count for a bot's voice** changes `Syllable`'s offsets (`_start`, `_count`: OpenAI 0-9, Anthropic 10-19, SpaceXAI 20-30, Meta 31-40, me 41-52) and `LoadVoices`. If T101 changes a count, rewrite both from their files and fix the numbers.
- **Delete an asset T101 left out only after a reference check** (`find_package_referencers_for_asset`). `S_TalkBlip` is still named in `Sfx`'s `"blip"` branch, and `Sfx` has no splice. If nothing calls `Sfx "blip"` or `Blip` any more, take out that branch and the `Blip` call first, then delete the asset.

## 3. Loudness

### 3a. The command and what it measures

```bash
python3 Tools/measure_loudness.py --md Saved/T102/loudness.md --json Saved/T102/loudness.json SourceAssets/Audio/music SourceAssets/Audio/commons SourceAssets/Audio/kenney SourceAssets/Audio/voices
```

- The script is ITU-R BS.1770-4 in plain Python 3 with no packages: K-weighting, 400 ms blocks, the gates at -70 LUFS and -10 LU. It reads PCM WAVs itself and decodes the other formats with `afconvert`, which every Mac has, or with `ffmpeg` where that is on the PATH. It runs on every core: the 128 files above took 8 s on this Mac.
- **The check:** a 997 Hz sine at full scale in one channel reads -3.0 LUFS, and a -20 dBFS sine in both channels reads -20.0, as BS.1770 says. T100's loops read within 0.3 LU of the numbers in `Docs/AudioShortlist.md`. The clipped-sample counts differ, because the shortlist counted the whole takes and this counts the loops.
- **Short sounds** (under 400 ms: syllables, clicks, steps) have no gated loudness. Their `ungated` column is the K-weighted loudness of the whole clip, and that is the number the targets use for them.
- **Mono:** BS.1770 measures a mono file as one channel. The targets assume that Unreal plays a 2D mono wave equal-power to both speakers (-3 dB each), so a mono clip and a stereo loop at the same number sound equally loud. The recordings in part 4c check that: if the talk comes out 3 dB hotter than part 3c predicts, that assumption is wrong. Lower `SC_Voice` by 3 dB (× 0.71).

### 3b. The numbers (2026-11-18)

**T100's loops** (all stereo, 44.1 kHz). "M max" is the loudest 400 ms.

| File | LUFS | M max | Peak dBFS | Clipped samples |
|---|---|---|---|---|
| `01_title` | -14.5 | -7.4 | -1.2 | 0 |
| `02_scene_prep` | -14.5 | -6.3 | 0.0 | 1516 |
| `03_space_plans` | -17.3 | -9.8 | -4.0 | 0 |
| `04_mine_bridge` | -13.7 | -9.4 | 0.0 | 111 |
| `05_dino_island` | -14.0 | -9.7 | -0.5 | 0 |
| `06_favor_father` | -13.8 | -6.7 | 0.0 | 8 |
| `07_glowing_briefcase` | -13.8 | -9.9 | -4.9 | 0 |
| `08_league_night` | -13.6 | -8.3 | 0.0 | 46 |
| `09_pick_a_pill` | -13.7 | -11.5 | -0.7 | 0 |
| `10_free_talk` | -14.3 | -7.2 | 0.0 | 2694 |
| `11_last_word` | -13.2 | -5.5 | 0.0 | 2628 |
| `12_cut` | -13.9 | -7.7 | 0.0 | 360 |
| `13_reactions` | -14.3 | -7.7 | 0.0 | 114 |
| `14_win` | -14.6 | -9.2 | -1.5 | 0 |
| `15_lose` | -13.8 | -8.6 | -0.7 | 0 |
| `16_show` | -13.1 | -7.2 | 0.0 | 9 |

All 16 sit within 1.4 LU of each other, except `03_space_plans` (-17.3). The clipped samples are in the files: lowering the volume doesn't remove them. The swells (the gap from LUFS to M max) are large in `scene_prep`, `last_word`, `title` and `free_talk`, about 7 to 8 LU.

**What the game plays now** (source loudness + 20·log10(wave × class), with the volumes T20, T71 and T72 recorded; `SC_Music` 0.35, `SC_Effects` 0.8, `SC_Voice` 0.5). "u" marks an `ungated` number.

| Asset | Source file | Source LUFS | Wave | In the game |
|---|---|---|---|---|
| `S_MusicTitle` | `kenney/Music Loops/Loops/Swinging Pants.ogg` | -16.0 | 1.0 | -25.1 |
| `S_MusicShow` | `kenney/Music Loops/Loops/Wacky Waiting.ogg` | -15.8 | 0.7 | -28.0 |
| `S_MusicSpacePlans` | `music/Space Cadet.ogg` | -13.5 | 1.23 | -20.8 |
| `S_MusicMineBridge` | `music/Infinite Descent.ogg` | -17.3 | 0.85 | -27.8 |
| `S_MusicDinoIsland` | `music/Drumming Sticks.ogg` | -17.4 | 0.91 | -27.3 |
| `S_MusicFavorFather` | `music/Italian Mom.ogg` | -15.2 | 0.75 | -26.9 |
| `S_MusicGlowingBriefcase` | `music/Cheerful Annoyance.ogg` | -14.9 | 0.77 | -26.3 |
| `S_MusicLeagueNight` | `music/Alpha Dance.ogg` | -16.4 | 0.85 | -26.9 |
| `S_MusicPickAPill` | `music/Retro Mystic.ogg` | -25.2 | 2.11 | -27.8 |
| `S_MusicFreeTalk` | `music/Mishief Stroll.ogg` | -17.6 | 0.91 | -27.6 |
| `S_MusicCut` | `music/Mission Plausible.ogg` | -15.0 | 0.62 | -28.3 (-36.3 ducked) |
| `S_MusicWin` | `music/Polka Train.ogg` | -17.1 | 0.95 | -26.7 |
| `S_MusicLose` | `music/Game Over.ogg` | -13.6 | 1.10 | -21.9 |
| `S_DrumRoll` | `commons/Long_Drum_Roll_with_Cymbal_Crash_at_End.wav` | -14.1 | 0.8 | -18.0 |
| `S_StingHuman` | `kenney/Music Loops/Idents/Serious ident.ogg` | -19.2 | 1.0 | -21.1 |
| `S_StingAI` | `kenney/Music Loops/Retro/Retro Comedy.ogg` | -24.9 | 1.0 | -26.8 |
| `S_Applause` | `commons/277021_sandermotions_applause-2.wav` | -18.4 | 0.9 | -21.2 |
| `S_ApplauseWin` | `commons/Thomas_Bresson_-_Applaudissements.mp3` (mono) | -19.4 | 0.8 | -23.2 |
| `S_Laughs` | `commons/72844_lonemonk_approx-800-laughter-and-clapter-1.wav` | -13.8 | 0.7 | -18.8 |
| `S_Grab` | `kenney/RPG Audio/Audio/cloth1.ogg` | -22.9 | 0.6 | -29.2 |
| `S_Throw` | `kenney/Foley Sounds/Audio/Woosh/woosh1.ogg` | -20.6 u | 0.7 | -25.6 |
| `S_Land` | `kenney/Impact Sounds/Audio/impactSoft_medium_000.ogg` | -22.3 u | 0.7 | -27.3 |
| `S_Step0` to `S_Step4` | `kenney/Impact Sounds/Audio/footstep_concrete_000` to `_004.ogg` | -34.0, -37.5, -42.1, -29.6, -44.7 u | 0.5 | -41.9 to -52.7 |
| `S_Hover` | `kenney/UI Audio/Audio/rollover1.ogg` | -40.8 u | 0.4 | -50.7 |
| `S_Click` | `kenney/Interface Sounds/Audio/click_001.ogg` | -63.4 u (peak -44.5 dBFS) | 0.6 | -69.8 |
| `S_TalkBlip` | `kenney/Interface Sounds/Audio/pluck_001.ogg` | -23.1 u | 0.6 (`SC_Voice`) | -33.6 |
| Voices, OpenAI (10) | `voices/OpenAI/` (mono) | -26.0 to -26.1 u | 0.6 (`SC_Voice`) | -36.5 |
| Voices, Anthropic (10) | `voices/Anthropic/` | -25.4 to -25.9 u | 0.6 | -36.1 |
| Voices, SpaceXAI (11) | `voices/SpaceXAI/` | -25.4 to -26.1 u | 0.6 | -36.4 |
| Voices, Meta (10) | `voices/Meta/` | -25.2 to -25.4 u | 0.6 | -35.8 |
| Voices, me (12) | `voices/Me/` | -23.8 to -26.1 u (peak -9.2 dBFS) | 0.6 | -35.5 |

What the numbers say:

- **The music plays 9 to 16 dB above the talk today**, not under it: the loops play at -21 to -28, the syllables at about -36. That fits my person's request of 2026-11-15.
- The drum roll, the laughs and the stingers are the loudest things in the game (-18 to -21).
- `S_Click`'s file is almost silent (peak -44.5 dBFS). The click may not be heard at all. T101 replaces it.
- Each voice set is within 1 LU of the others (T72 leveled them), and my own clips have the widest spread, 2.3 LU.

### 3c. The targets (step 2), and the volumes that reach them

"In the game" = the source's loudness + 20·log10(wave Volume × class Volume), as in part 3b. Each group's target is in the game, then turned into a wave-level target by taking off its class volume.

| Group | Sound class, volume | In the game | Wave-level target | Measured on |
|---|---|---|---|---|
| **Voice** (the syllables; the blip, if kept) | `SC_Voice` **1.0** (was 0.5) | **-26** | -26 | `ungated` per clip |
| **Show** (stingers, applause, laughs) | `SC_Effects` **0.71** (was 0.8; -3 dB) | **-30** | -27 | integrated `LUFS` |
| **Drum roll** | `SC_Effects` 0.71 | **-32** | -29 | integrated `LUFS` |
| **Robot and UI** (steps, grab, throw, land, click, hover) | `SC_Effects` 0.71 | **-34** | -31 | `ungated` per clip |
| **Music** (all 16 loops) | `SC_Music` **0.5** (was 0.35) | **-36** | -30 | integrated `LUFS` |

- **Wave Volume = 10^((wave-level target − measured) / 20).** The music column in part 2a is that formula at -30.
- **The music sits 10 dB under the voices**, as step 2 asks for a start, and the effects sit between the two. Under the drum roll, T71's duck to 0.4 puts the Cut loop at -44.
- **The voices:** the four bot sets measure -25.2 to -26.1, and mine -25.0 on average, so with `SC_Voice` at 1.0 every voice wave takes **Volume 1.0**. That's +10 dB on today's talk, and the loudest peak (my clip `_08`, -9.2 dBFS) stays far from clipping. T101's new bot sets should land at -26 ± 0.5 `ungated` on this script before import; then they take Volume 1.0 too.
- **The swells:** the loudest 400 ms of the music at this level reaches -28 (`scene_prep`) to -34 (`pick_a_pill`), 2 to 8 dB under a syllable. If a recording shows a swell covering the talk, lower `SC_Music` first, or build part 4d.
- **A Volume over 1.0** is allowed (T71 kept 2.11 on `S_MusicPickAPill`), but check the peak: measured peak + 20·log10(Volume × class) must stay under -1 dBFS. If it doesn't, ask T101 for a louder file.
- **What to write in `Docs/AudioShortlist.md`** (step 7): this table, the final class volumes and every wave Volume after step 6's changes by ear.

## 4. The checks

### 4a. The order of `NHOS: SOUND music <key>` (step 4)

The keys come from `SwapMusic`'s print (`NHOS: SOUND music <key>`), which runs only when the key changes (`PlayMusic` drops a repeat). Each scene's lines, in order:

1. **`scene_prep`**: at `PREP shown scene=n`, in the same frame (`OpenPrep`). In an autoplay show the first line of all is `show` (`ShowTitle` skips the title and asks for `show`); scene 1's `scene_prep` follows in a frame or so. In a show played by hand it's `title`.
2. **the card id** (one of the seven): at `CUE phase THE SCENE: SCENE n, TURN 1 OF 3`. Turns 2 and 3 print nothing.
3. **`free_talk`**: at `CUE phase FREE TALK: SCENE n, ROUND 1 OF 2`. Round 2 prints nothing.
4. **`last_word`**, only when `LASTWORDS scene=n named=` names someone (`named=none` means no Last Word): at `CUE phase LAST WORD: SCENE n`. Then `CUE phase SCENE n: FREE TALK IS OVER` comes and prints nothing.
5. **`cut`**: at `CUE phase THE CUT: SCENE n`, then in the same frame `SOUND duck` and `SOUND drum` (`votes show`). Then the stinger at `CUE cut`, or the laughs at `CUE tie`. Both stop the music, so no music key prints there.
6. **`reactions`**: at `CUE phase REACTIONS: SCENE n`, or later if part 4b is built.

At the end: `CUE phase THE SHOW IS OVER` and, on a win, `CUE phase THE REVEAL` print nothing. Then `CUE end` (`EndCheer` stops the music, `SOUND applause_win` or `SOUND laughs`), and 3 s later **`win`** or **`lose`**, the last music key of the show.

**The script.** On this Mac, the editor's and the game window's logs are in `~/Library/Logs/Unreal Engine/AIMegaJam2026Editor/`, not `Saved/Logs/`. A log may hold several shows: the second argument starts at the Nth `title` or `show` line (0 is the first).

```python
# T102 step 4: the order of "NHOS: SOUND music <key>" lines in one show's log. Run from the repo folder.
import json, re, sys
log = open(sys.argv[1], encoding="utf-8", errors="replace").read()
if len(sys.argv) > 2:                      # start at the Nth "SOUND music title|show" line
    log = log[[m.start() for m in re.finditer(r"NHOS: SOUND music (title|show)\b", log)][int(sys.argv[2])]:]
cards = {c["id"] for c in json.load(open("Content/NHOS/Data/scenes.json"))["cards"]}
keys = re.findall(r"NHOS: SOUND music (\w+)", log)
toks = ["CARD" if k in cards else k for k in keys]
print("keys:", " ".join(keys))
scene = r"scene_prep CARD free_talk (last_word )?cut (reactions )?"
ok = re.fullmatch(rf"((title|show) )*({scene})+(win|lose)( title| show| scene_prep.*)?", " ".join(toks))
print("scenes:", toks.count("scene_prep"), "last_word:", toks.count("last_word"), "reactions:", toks.count("reactions"))
print("ORDER OK" if ok else "ORDER BAD")
```

- This prep session tested it on a made-up log in the new order (`ORDER OK`) and on the editor log of 2026-11-18, which is in T71's old order (`ORDER BAD`, as it should be).
- **Pass:** `ORDER OK`, `reactions` equal to `scenes` (the Reactions loop starts in every scene; the last scene's may be cut short by the end), and `last_word` equal to the number of `LASTWORDS ... named=` lines that name someone. A show where nobody names anyone never plays `last_word`. Run a second show if the first has no Last Word.

### 4b. The Reactions loop under the stinger: a later start (step 4)

**It does start under the stinger today**, by the logs of 2026-11-18 (`~/Library/Logs/Unreal Engine/AIMegaJam2026Editor/AIMegaJam2026-backup-2026.11.18-08.13.43.log`):

| Pace | `CUE cut` + stinger | `CUE phase REACTIONS` | `SOUND applause` (`Crowd`) | `REACTIONS DONE` |
|---|---|---|---|---|
| fast (autoplay, about 07:32) | 0.0 s | **+0.3 s** | +1.5 s | +6.7 s |
| by hand (about 07:48) | 0.0 s | **+3.0 s** | +1.7 s | +29 s |

With T102's key, `REACTIONS` swaps in the reactions loop at once, with a 1 s fade-in. At a fast pace that's 0.3 s into a stinger 5 to 6 s long (T20's stingers; T101's may differ). At the by-hand pace the loop comes in after the crowd has started.

**Where the later start goes:** in `BPC_ShowAudio` only, with no change to `BP_Show`. `Reveal` writes down when the stinger played. `PlayPhase` starts the reactions loop at once if `ReactDelay` seconds have passed since then, or else sets a timer for the rest. A tie has no `Reveal`, so after a tie the loop starts at once, under the laughs, which is fine because there's no stinger.

New variables on `BPC_ShowAudio`: **`RevealAt`** (Float, default 0.0) and **`ReactDelay`** (Float, default **3.0**: at the by-hand pace nothing changes, and at a fast pace the loop waits for the crowd). New function: **`ReactLater`** (no inputs). Create them and compile before you write the graphs.

```
; T71: the one call RunCue's "phase" cue makes. The card id comes from BP_Show's CardId, which only
; changes inside ScenePrep, and ScenePrep runs at its own cue's turn (T30), so it is never ahead of the queue.
; T102: the Reactions loop waits until ReactDelay s after the stinger (Reveal sets RevealAt), so it doesn't
; start under it. At a slow pace the header comes later than that, and the loop starts at once.
(fn PlayPhase (Text CardId)
  (bind _k (CallFunction|PhaseKey :Text Text))
  (bind _wait (- (+ (V RevealAt) (V ReactDelay)) (Utilities|Time|GetRealTimeSeconds)))
  (if (streq _k "card")
    (CallFunction|PlayMusic :Key CardId)
    (return))
  (if (and (streq _k "reactions") (> _wait 0.05))
    (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "ReactLater" :Time _wait :bLooping false)
    (return))
  (if (not (Utilities|String|IsEmpty _k))
    (CallFunction|PlayMusic :Key _k)))
```

```
; T102: starts the Reactions loop late (PlayPhase). If other music started first (the next Scene Prep), it stays out of the way.
(fn ReactLater ()
  (if (Utilities|String|IsEmpty (V MusicKey))
    (CallFunction|PlayMusic :Key "reactions")))
```

`Reveal`: one new line, the first, `(set RevealAt (Utilities|Time|GetRealTimeSeconds))`. Its other lines and comment stay, plus a T102 comment line:

```
; T20: the cut: the drum stops, the stinger says who it was, the crowd follows 1.5 s later.
; T71: the Cut loop stops with the drum, so nothing plays under the stinger.
; T102: notes when the stinger played, so the Reactions loop can wait for it (PlayPhase).
(fn Reveal (IsHuman)
  (set RevealAt (Utilities|Time|GetRealTimeSeconds))
  (set LastHuman IsHuman)
  (CallFunction|StopDrum)
  (CallFunction|StopMusic)
  (CallFunction|Sfx :Key (select IsHuman "sting_human" "sting_ai") :Pitch 1.0)
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "Crowd" :Time 1.5 :bLooping false))
```

`EndCheer`: one new line, the first, clears a pending `ReactLater`. Without it, a timer that fires after `EndCheer` stopped the music would start the reactions loop, and `EndMusic` would then find `MusicKey` set and play no win or lose loop.

```
; T20: the end screen: the music stops; a win gets the long applause, a loss the laughs.
; T71: 3 s in, the win or lose loop starts (EndMusic). T102: a Reactions loop still waiting (ReactLater) never starts.
(fn EndCheer (Win)
  (Utilities|Time|ClearTimerbyFunctionName :Object self :FunctionName "ReactLater")
  (CallFunction|StopMusic)
  (set EndWin Win)
  (CallFunction|Sfx :Key (select Win "applause_win" "laughs") :Pitch 1.0)
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "EndMusic" :Time 3.0 :bLooping false))
```

- Every node here is one the graphs already use: `GetRealTimeSeconds` (`WBP_Stage.TimerStart`), `SetTimerbyFunctionName` and `ClearTimerbyFunctionName` (`BPC_Stagehand.Hush`). `and` (over 100 uses in `Graphs/`) and `>` on floats are the DSL's own. `bind` stays at the top of the function, as in `Syllable`, so no local is made inside a branch.
- **The check:** in a fast autoplay log, `SOUND music reactions` comes about 3.0 s after `SOUND sting_ai` or `sting_human`; at a by-hand pace it comes at `CUE phase REACTIONS`.
- **Tune `ReactDelay` by ear** in step 6 (the Reactions recording). Write the value in the findings.

### 4c. Recording the game's own audio on this Mac (step 6)

**What this Mac has:** no `ffmpeg`, no `sox`, and no loopback audio device (`system_profiler SPAudioDataType` lists no BlackHole, Soundflower or aggregate device). macOS can't record its own output without one. So the recording has to come from inside Unreal: the audio mixer can record its main submix, which is everything the game plays, before the system volume.

- **The nodes:** `Start Recording Output` (`ExpectedDuration`, `SubmixToRecord` left empty = the main submix) and `Finish Recording Output` (`ExportType` = `Wav File`, `Name`, `Path`, `SubmixToRecord` empty). Both are in `UAudioMixerBlueprintLibrary`. In the DSL, make them with `create_node`, `declaring_class` `/Script/AudioMixer.AudioMixerBlueprintLibrary`, the way T71 made the Audio Component's fades.
- **Where the file goes:** with `Path` empty, the engine writes `<Name>.wav` to its own folder for bounced files, expected at `Saved/BouncedWavFiles/`. Check that with the first recording. If it's not there, run `find ~/Library "<repo>/Saved" -name "1_*.wav" -mmin -10`.
- **Console commands:** this prep session couldn't confirm any without the editor. If you want one, type `help` in the editor's console (it lists every command) and search for "Record". Don't build on a name you haven't seen there.

**The recorder (recommended):** one WAV per music phase, named `<NN>_<key>.wav`, made by `BPC_ShowAudio` itself, only when the game was started with `-NHOSRec`. That way a free autoplay show in a game window records every phase with no clicks, and a player's game never records.

- New variables on `BPC_ShowAudio`: `RecN` (Integer, 0), `RecName` (String), `RecLive` (Boolean, false), `RecMax` (Float, **60.0**: The Cut's recording must reach the reveal, 22 to 27 s after `THE CUT` at the by-hand pace). New functions `RecPhase(Key: String)` and `RecStop()`.
- The `HasLaunchOption` node is `UKismetSystemLibrary::HasLaunchOption` (`create_node`, `declaring_class` `/Script/Engine.KismetSystemLibrary`, if the DSL path below doesn't resolve). The two recording nodes are written below as `AudioMixer|...` placeholders: replace each with its `create_node` node.

```
; T102: records the game's own audio, one WAV per music phase, only in a game started with -NHOSRec (step 6's recordings).
; A recording stops at the next phase or after RecMax s. The end screen's recording starts at EndCheer and keeps going under
; the win or lose loop. A player's game never records.
(fn RecPhase (Key)
  (if (not (Utilities|HasLaunchOption :OptionToCheck "NHOSRec"))
    (return))
  (if (or (streq Key "win") (streq Key "lose"))
    (return))
  (CallFunction|RecStop)
  (set RecN (+ (V RecN) 1))
  (set RecName (cat (str (V RecN)) "_" Key))
  (AudioMixer|StartRecordingOutput :ExpectedDuration (V RecMax))
  (set RecLive true)
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "RecStop" :Time (V RecMax) :bLooping false))
```

```
; T102: ends the recording RecPhase started and writes it as <RecName>.wav.
(fn RecStop ()
  (if (V RecLive)
    (set RecLive false)
    (Utilities|Time|ClearTimerbyFunctionName :Object self :FunctionName "RecStop")
    (AudioMixer|FinishRecordingOutput :ExportType "WavFile" :Name (V RecName) :Path "")))
```

`PlayMusic` calls it when the key changes (`PlayMusic` has no splice). `EndCheer` calls `(CallFunction|RecPhase :Key "end")` as its second line, after part 4b's `ClearTimerbyFunctionName`.

```
; T20: one music loop at a time. The same key twice does nothing, so every header cue can ask for the show music.
; T102: a new key also starts a new recording in a game started with -NHOSRec (RecPhase).
(fn PlayMusic (Key)
  (if (not (streq Key (V MusicKey)))
    (CallFunction|RecPhase :Key Key)
    (CallFunction|SwapMusic :Key Key)))
```

**The run** (no `fast_lines`, `"mode": "free"`, autoplay on, `"analytics": "off"` in `Local/switches.json`):

```bash
"/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor" "<PROJECT>" -game -windowed -ResX=1600 -ResY=900 -log=T102rec.log -NHOSRec
```

- **What it gives:** `1_show`, `2_scene_prep`, `3_<card>` (a scene turn with lines typing out), `4_free_talk`, `5_last_word` (if this show has one), `6_cut` (the drum roll, the duck, the stinger and the crowd), `7_reactions`, ... and `N_end` (the applause or laughs, then the win or lose loop). Trim each to about 30 s with `afconvert`'s or Python's `wave`, keeping the interesting part (The Cut's reveal, the end screen's first seconds).
- **Scene Prep may be short in autoplay:** in the log of 2026-11-18 the autoplay Scene Preps of scene 2 lasted 0.4 s; scene 1's lasted 8 s. If no `scene_prep` recording is 20 s or longer, record scene 1's Scene Prep by hand: in PIE (Test for Free, autoplay off), which waits for Start. PIE has no `-NHOSRec`, so call the two nodes from the editor's Python on the PIE world instead (`unreal.AudioMixerBlueprintLibrary.start_recording_output(world, 30.0)`, then `finish_recording_output(world, unreal.AudioRecordingExportType.WAV_FILE, "prep_by_hand", "")`, with `world` from `unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()`). Bring the editor to the front first: in the background it runs at about 3 frames a second (T71).
- **Check the mix with numbers before my person listens:** `python3 Tools/measure_loudness.py Saved/BouncedWavFiles` (or wherever they landed). Scene Prep has no talk, so its recording should read about **-36 LUFS** (part 3c) with the master volume at 1.0. A difference of more than 2 dB means the gain chain isn't what part 3 assumes (the mono rule, a class volume that didn't save). Find the cause before you send the recordings.
- **For the Artifact page:** artifacts don't serve `.m4a`, but AAC renamed `.mp4` works, and the `assets` capability takes no audio, so publish the files with the page (T100). `afconvert -f mp4f -d aac -b 160000 in.wav out.mp4` makes one (or `-f m4af` and rename).
- **Keep or remove the recorder?** It never runs without `-NHOSRec`, and the next mix pass can use it. Keep it unless my person says otherwise, and say so in the findings.

### 4d. A duck while a line types (step 5, only if the recordings need it)

Step 5 allows ducking the music a bit more while a line types, if the talk still competes. Build this only if the recordings or my person say the music covers the talk at part 3c's levels.

- **Where:** in `Syllable`, which runs once per syllable as a line types out (T73). After the `SpawnSound2D`, if `MusicKey` isn't `"cut"` (the drum roll's duck stays T71's), call the Audio Component's `AdjustVolume` on `Music` (0.2 s, to 0.7, about -3 dB). Then set a timer `TalkUp` for 0.6 s, which runs `AdjustVolume` (1.0 s, back to 1.0). Every syllable restarts the timer, so the music comes back 0.6 s after the line ends.
- **The splice:** `AdjustVolume` comes only from `create_node` with `declaring_class` `/Script/Engine.AudioComponent` (T20, T71), so `Syllable`'s and `TalkUp`'s files get the same splice note `DuckMusic` has.
- **Watch for:** a `FadeIn` from `SwapMusic` that runs at the same time (a new phase with a line typing) is overridden by the duck's `AdjustVolume`. That is harmless, because `TalkUp` brings it back to 1.0.

## Questions for my person

None before the build. The mix is approved by ear in step 6, and every level here is a start for that. If my person wants the title or the end screens louder than the other loops, that breaks Done-when 2's "one target". Ask then, with the multiple-choice tool.
