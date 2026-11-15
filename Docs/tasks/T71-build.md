# T71 build sheet: music for each place and each scene

Back to [T71](T71.md) and [the plan](../Plan.md).

A prep session wrote this on 2026-11-15, on the Mac, without the editor. It covers T71's steps 1 and 2 (the track list and the picks, done: the files are in `SourceAssets/Audio/music/`) and gets steps 3 to 6 and the check ready to run. **Written against `noHumansOnSet` at `944978c`.** Every `Graphs/` source quoted here is the one pushed at that commit.

**What T71 must re-check before it writes anything:**

- **`BPC_ShowAudio` will have changed.** T72 (a voice for each robot: a new `Syllable` function) and T73 (one voice sound per syllable) also change it, and T72 held its lock while this sheet was written. Before step 4, list the component's graphs and diff `Graphs/BPC_ShowAudio/` against `944978c` (`git diff 944978c -- Graphs/BPC_ShowAudio`). If `SwapMusic`, `PlayMusic`, `StartDrum`, `Reveal` or `EndCheer` changed, merge those changes into the sources in part 4 instead of pasting them as they are.
- **`RunCue` may have changed.** Diff `Graphs/BP_Show/RunCue.txt` against `944978c`, and merge the same way.
- **The header texts** (part 5a). Since T58, a Last Word header exists. Since T34, the header may lose its scene number. Search again if either has landed.
- **Where `CardId` is set** (part 5b), and **how long The Cut's loop plays before the drum roll** (part 5c). Both decide a branch in this sheet.

## 1. The track list

Eleven new loops, one for each key, and no loop used twice. The title keeps `S_MusicTitle` (`Swinging Pants`, the task's default). `S_MusicShow` (`Wacky Waiting`) stays as the fallback for a card with no track of its own and for the key `show`, so no new key uses it. T20's two stingers (`Serious ident`, `Retro Comedy`) aren't used for music either.

All eleven come from Kenney's **Music Loops 1.1** pack (CC0), in the bundle the team bought. Each file's name is Kenney's. "Length" and "tempo" are measured (see "How the picks were measured" below). **Wave vol.** is the volume to set on the imported sound wave (part 3).

| Key | File in `SourceAssets/Audio/music/` | Length, tempo | Wave vol. | Why it fits | Second choice |
|---|---|---|---|---|---|
| `space_plans` | `Space Cadet.ogg` | 24.2 s, about 159 BPM | 1.23 | A space western on a desert planet: the only space name in the pack. It measures sparse and airy (little bass, few hard hits) and stays quiet (peaks at −7 dBFS), so it reads as wide open space. **Listen first** (the seam, below). | `Loops/Flowing Rocks.ogg` (30.8 s, 125 BPM, a clean 64-beat loop; desert rocks) |
| `mine_bridge` | `Infinite Descent.ogg` | 12.0 s, 120 BPM | 0.85 | An old dwarf mine with a sleeping fire monster: the name says going down. Bass-heavy and fairly dark (85% of its energy under 200 Hz), steady, a clean 24-beat loop. | `Loops/Sad Descent.ogg` (24.0 s, about 84 BPM, the darkest and quietest loop; a hush for the sleeping monster; its seam is uncertain) |
| `dino_island` | `Drumming Sticks.ogg` | 14.8 s, 130 BPM | 0.91 | A jungle theme park on opening day: jungle drums. It has one of the strongest, steadiest beats in the pack, at a lively tempo for a big day. A clean 32-beat loop. | `Loops/Farm Frolics.ogg` (10.7 s, 90 BPM, bright and bouncy; animals) |
| `favor_father` | `Italian Mom.ogg` | 29.5 s, 130 BPM | 0.75 | A crime family's garden wedding: the name is the story. It is long (it repeats the least of the scene loops), exactly 64 beats, and the most varied in level (5 dB between its quiet and loud seconds), so it has an arrangement rather than one riff. Mellow in tone. | `Retro/Retro Polka.ogg` (7.8 s, 123 BPM, a wedding dance; short, and from the Retro set) |
| `glowing_briefcase` | `Cheerful Annoyance.ogg` | 12.0 s, 160 BPM | 0.77 | A retro diner on dance-contest night. 160 BPM is a twist and rock-and-roll tempo, and it is one of the two brightest loops in the pack, with a strong beat. A clean 32-beat loop. **A guess:** I'd rather have taken `Retro Beat`, but the Retro set measures like one family (48 kHz, 4 to 10 dB quieter than the other loops), and `pick_a_pill` takes `Retro Mystic`; the diner and the computer office should not sound alike. | `Retro/Retro Beat.ogg` (15.4 s, 125 BPM, a strong dance beat, a clean 32-beat loop) |
| `league_night` | `Alpha Dance.ogg` | 14.8 s, 130 BPM | 0.85 | A retro bowling alley on semifinal night, under a starry ceiling: a dance loop for a disco-lit lane. Light on bass and bright, a clean 32-beat loop. **A guess**: the slacker in the bathrobe could also want something laid back (the second choice). | `Retro/Retro Reggae.ogg` (8.0 s, 120 BPM; laid back for the slacker, but short) |
| `pick_a_pill` | `Retro Mystic.ogg` | 48.0 s, 120 BPM | 2.11 | A gray office inside a computer program. "Retro" for the old green screens, "Mystic" for the secret. The longest loop in the pack (exactly 96 beats), so it repeats the least, and mostly sustained sound with few hard hits: it hums like the buzzing ceiling light. It is quiet (−25 dBFS), so it needs the highest wave volume. | `Loops/Time Driving.ogg` (8.0 s, 120 BPM, a steady driving pulse) |
| `free_talk` | `Mishief Stroll.ogg` | 31.8 s, about 120 BPM | 0.91 | The robots talk over who the human is: a sneaky stroll. Long (it repeats the least of the in-show loops) and mid-level. T20 chose it as the show loop's backup. | `Loops/German Virtue.ogg` (8.0 s, 120 BPM, a clean 16-beat loop) |
| `cut` | `Mission Plausible.ogg` | 10.5 s, about 114 BPM | 0.62 | The vote: a spy-movie name for a hunt. The loudest file in the pack and the flattest in level (1 dB between its seconds), so it works as a steady tension bed under the vote lines and the drum roll. | `Loops/Time Driving.ogg` (shared with `pick_a_pill`'s second choice; a ticking-clock pulse) |
| `win` | `Polka Train.ogg` | 16.0 s, 120 BPM | 0.95 | The human fooled the cast: a party. Bright, steady, a clean 32-beat loop. | `Loops/Farm Frolics.ogg` (shared with `dino_island`'s second choice) |
| `lose` | `Game Over.ogg` | 9.6 s, about 156 BPM | 1.10 | The cast caught the human: the name. Sparse, darker in tone, and quieter at its peaks than the other loops. | `Loops/Sad Town.ogg` (18.3 s, about 70 BPM, slow; its seam is uncertain) |
| `title` | keep `S_MusicTitle` (`kenney/Music Loops/Loops/Swinging Pants.ogg`) | 24.2 s, about 160 BPM | 1.0 (T20) | The task's default. **Listen to its seam** (below); if it hiccups, `Loops/Flowing Rocks.ogg` is the closest free loop in length. | |

**The second choices** are not in the repo. They are in the bundle: `Local/audio/kenney/Music Loops/` on the PC, or `Audio/Music Loops/` inside `Kenney Game Assets All-in-1 3.8.0.zip` (in the Mac's Downloads folder). Add a second choice to `SourceAssets/Audio/music/` before you import it, and give it a row in `Docs/Assets.md`.

**Not picked: Music Jingles as win or lose stings.** The pack has 85 jingles (Hit, Pizzicato, Retro, Saxophone, Steeldrum; 0.3 to 1.8 s each). `EndCheer` already plays the long applause or the laughs as the end's sting, and the win or lose loop starts 3 s later (part 4), so a jingle on top would crowd it.

### Which picks my person should listen to

Claude can't hear any of this. In order of doubt:

1. **`Space Cadet` (`space_plans`)**: its seam. Its beat is sparse, so the tempo measure is unsure (159 or 160 BPM), and at 160 BPM the loop point falls about 0.17 s off the beat. If the loop stumbles when it wraps, use `Flowing Rocks`.
2. **`Swinging Pants` (the title, from T20)**: the same doubt. At its best-fitting 160 BPM, its 24.21 s are 64.5 beats, so the loop may wrap half a beat early. T20 never heard it either.
3. **`Cheerful Annoyance` (`glowing_briefcase`) and `Alpha Dance` (`league_night`)**: whether each sounds like its place. Swap in `Retro Beat` or `Retro Reggae` if not.
4. **`Mishief Stroll` (`free_talk`)**: its last 50 ms are nearly silent (−55 dBFS), so there may be a short gap at each wrap. The rest of its seam measures clean at 120.6 BPM.
5. **`Retro Mystic` (`pick_a_pill`)** at wave volume 2.11: whether it now sits level with the others. RMS loudness misjudges bass-heavy, sustained music.

The other six (`Infinite Descent`, `Drumming Sticks`, `Italian Mom`, `Mission Plausible`, `Polka Train`, `Game Over`) measure as clean loops whose names match their story. They are still picks by numbers and names.

### How the picks were measured

Each loop was decoded with `afconvert` (to 22.05 kHz mono) and measured with a standard-library Python script (in the prep session's scratchpad, not committed):

- **Loudness:** RMS and peak in dBFS over the whole file, and the RMS of each 1-second window (the spread shows how much the arrangement changes).
- **Tone:** the share of energy under 200 Hz (bass weight) and the zero-crossing rate (brightness).
- **Tempo and seam:** an onset envelope (rises in level, every 11.6 ms), a beat grid fitted to it, and then where the file's end falls on that grid. A loop cut on the beat ends a whole number of beats after it starts, so the beat goes on across the wrap. Within ±30 ms counts as clean. `Space Cadet`, `Swinging Pants`, `Sad Town`, `Sad Descent` and `Night at the Beach` were 0.15 to 0.3 s off; the rest were within ±45 ms (`Mishief Stroll` at its whole-beat tempo of 120.6 BPM).

| File | Length | RMS, peak (dBFS) | Bass share | Brightness (ZCR/s) | Tempo | Seam |
|---|---|---|---|---|---|---|
| Space Cadet | 24.16 s | −20.5, −7.1 | 0.64 | 728 | 159 to 160 | unsure, +0.17 s at 160 |
| Infinite Descent | 12.00 s | −17.3, −0.6 | 0.85 | 813 | 120.0 | 24 beats, −3 ms |
| Drumming Sticks | 14.75 s | −17.9, −0.7 | 0.81 | 1432 | 130.0 | 32 beats, −22 ms |
| Italian Mom | 29.54 s | −16.2, −0.7 | 0.82 | 550 | 130.0 | 64 beats, +2 ms |
| Cheerful Annoyance | 12.00 s | −16.4, −1.2 | 0.81 | 2896 | 160.0 | 32 beats, −1 ms |
| Alpha Dance | 14.78 s | −17.3, −1.9 | 0.66 | 1670 | 130.0 | 32 beats, +12 ms |
| Retro Mystic | 47.98 s (48 kHz) | −25.2, −9.9 | 0.88 | 846 | 120.0 | 96 beats, −29 ms |
| Mishief Stroll | 31.84 s | −17.9, −0.9 | 0.83 | 983 | 120.2 to 120.6 | 64 beats at 120.6 |
| Mission Plausible | 10.50 s | −14.5, −1.0 | 0.80 | 518 | 114 | 20 beats, −39 ms |
| Polka Train | 16.03 s | −17.8, −0.7 | 0.67 | 1635 | 119.9 | 32 beats, +13 ms |
| Game Over | 9.62 s | −19.0, −5.0 | 0.66 | 575 | 155 to 156 | 25 beats, −45 ms |
| Wacky Waiting (T20 show loop) | 12.00 s | −15.6, −1.3 | 0.84 | 5499 | 160.0 | 32 beats, +11 ms |
| Swinging Pants (T20 title) | 24.21 s | −18.2, −2.8 | 0.78 | 852 | 160.0 | unsure, −0.17 s |

## 2. The files and their license rows

The eleven picks are committed in `SourceAssets/Audio/music/`, with the pack's `License.txt` (CC0 1.0). They are Ogg Vorbis, stereo, 44.1 kHz (`Retro Mystic` is 48 kHz), 3.4 MB in all. `.gitattributes` already sends `.ogg` to LFS. `Cheerful Annoyance.ogg` and `Mishief Stroll.ogg` are byte-for-byte the same as T20's copies in `SourceAssets/Audio/kenney/Music Loops/Loops/`, so LFS stores them once.

**Rows for `Docs/Assets.md`,** ready to paste under T20's audio rows. T71 adds them when it imports the files (the prep session doesn't edit `Docs/Assets.md`, because T72 has it):

```markdown
Imported in T71 from `SourceAssets/Audio/music/` (see `Docs/tasks/T71-build.md`) into `Content/NHOS/Audio/Music/`. No AI audio tools were used. Kenney's packs are CC0, so no credit is needed; optional credit: "Kenney (www.kenney.nl)".

| Asset | What it is | Source | License |
|---|---|---|---|
| `Content/NHOS/Audio/Music/S_MusicSpacePlans` | Music loop for the `space_plans` card (24 s) | Kenney Game Assets All-in-1 3.8.0 (https://kenney.itch.io/kenney-game-assets), pack "Music Loops", `Loops/Space Cadet.ogg` | CC0 1.0 |
| `Content/NHOS/Audio/Music/S_MusicMineBridge` | Music loop for the `mine_bridge` card (12 s) | Kenney Game Assets All-in-1 3.8.0 (https://kenney.itch.io/kenney-game-assets), pack "Music Loops", `Loops/Infinite Descent.ogg` | CC0 1.0 |
| `Content/NHOS/Audio/Music/S_MusicDinoIsland` | Music loop for the `dino_island` card (15 s) | Kenney Game Assets All-in-1 3.8.0 (https://kenney.itch.io/kenney-game-assets), pack "Music Loops", `Loops/Drumming Sticks.ogg` | CC0 1.0 |
| `Content/NHOS/Audio/Music/S_MusicFavorFather` | Music loop for the `favor_father` card (30 s) | Kenney Game Assets All-in-1 3.8.0 (https://kenney.itch.io/kenney-game-assets), pack "Music Loops", `Loops/Italian Mom.ogg` | CC0 1.0 |
| `Content/NHOS/Audio/Music/S_MusicGlowingBriefcase` | Music loop for the `glowing_briefcase` card (12 s) | Kenney Game Assets All-in-1 3.8.0 (https://kenney.itch.io/kenney-game-assets), pack "Music Loops", `Loops/Cheerful Annoyance.ogg` | CC0 1.0 |
| `Content/NHOS/Audio/Music/S_MusicLeagueNight` | Music loop for the `league_night` card (15 s) | Kenney Game Assets All-in-1 3.8.0 (https://kenney.itch.io/kenney-game-assets), pack "Music Loops", `Loops/Alpha Dance.ogg` | CC0 1.0 |
| `Content/NHOS/Audio/Music/S_MusicPickAPill` | Music loop for the `pick_a_pill` card (48 s) | Kenney Game Assets All-in-1 3.8.0 (https://kenney.itch.io/kenney-game-assets), pack "Music Loops", `Retro/Retro Mystic.ogg` | CC0 1.0 |
| `Content/NHOS/Audio/Music/S_MusicFreeTalk` | Music loop under Free Talk (32 s) | Kenney Game Assets All-in-1 3.8.0 (https://kenney.itch.io/kenney-game-assets), pack "Music Loops", `Loops/Mishief Stroll.ogg` | CC0 1.0 |
| `Content/NHOS/Audio/Music/S_MusicCut` | Music loop under The Cut, low under the drum roll (11 s) | Kenney Game Assets All-in-1 3.8.0 (https://kenney.itch.io/kenney-game-assets), pack "Music Loops", `Loops/Mission Plausible.ogg` | CC0 1.0 |
| `Content/NHOS/Audio/Music/S_MusicWin` | Music loop on the end screen after a win (16 s) | Kenney Game Assets All-in-1 3.8.0 (https://kenney.itch.io/kenney-game-assets), pack "Music Loops", `Loops/Polka Train.ogg` | CC0 1.0 |
| `Content/NHOS/Audio/Music/S_MusicLose` | Music loop on the end screen after a loss (10 s) | Kenney Game Assets All-in-1 3.8.0 (https://kenney.itch.io/kenney-game-assets), pack "Music Loops", `Loops/Game Over.ogg` | CC0 1.0 |
```

If a second choice replaces a pick, change that row's file name.

## 3. Import (editor)

Do this in the repo folder, where the editor has the project open. Lock nothing for new assets.

1. **T20's auto-import rule** (`Docs/tasks/T20.md`, "Unreal MCP rules found in this task"): first set `bPromptBeforeAutoImporting` = false and `bAutoDeleteAssets` = false on `/Script/UnrealEd.Default__EditorLoadingSavingSettings` (in memory, for this editor session). Then copy each `.ogg` into `Content/NHOS/Audio/Music/` **under its asset name**, and the editor makes a `SoundWave` named after the file within a second or two:

   ```bash
   cd /Users/personal/Projects/AIMegaJam2026   # or the PC's repo folder
   M=SourceAssets/Audio/music; C=Content/NHOS/Audio/Music
   cp "$M/Space Cadet.ogg"        "$C/S_MusicSpacePlans.ogg"
   cp "$M/Infinite Descent.ogg"   "$C/S_MusicMineBridge.ogg"
   cp "$M/Drumming Sticks.ogg"    "$C/S_MusicDinoIsland.ogg"
   cp "$M/Italian Mom.ogg"        "$C/S_MusicFavorFather.ogg"
   cp "$M/Cheerful Annoyance.ogg" "$C/S_MusicGlowingBriefcase.ogg"
   cp "$M/Alpha Dance.ogg"        "$C/S_MusicLeagueNight.ogg"
   cp "$M/Retro Mystic.ogg"       "$C/S_MusicPickAPill.ogg"
   cp "$M/Mishief Stroll.ogg"     "$C/S_MusicFreeTalk.ogg"
   cp "$M/Mission Plausible.ogg"  "$C/S_MusicCut.ogg"
   cp "$M/Polka Train.ogg"        "$C/S_MusicWin.ogg"
   cp "$M/Game Over.ogg"          "$C/S_MusicLose.ogg"
   ```

   Wait until all eleven assets exist (`list_assets` or `does_asset_exist`), then delete the eleven `.ogg` copies from `Content/` (never commit an `.ogg` under `Content/`).
2. **On each new wave** (one editor Python call): `looping` = True, `sound_class_object` = `/Game/NHOS/Audio/SC_Music.SC_Music` (check the path with T20's waves: `S_MusicShow` uses it), and `volume` from the table in part 1. `SC_Music` is at 0.35, so the effective volume is the wave's × 0.35.
   - **Why these volumes:** each puts its loop at the same measured loudness (RMS) as a reference. The scene, Free Talk and Cut loops match T20's show loop (`Wacky Waiting`, RMS −15.6 dBFS at wave 0.7): volume = 0.7 × 10^((−15.6 − RMS) / 20). The win and lose loops match the title loop (`Swinging Pants`, RMS −18.2 dBFS at wave 1.0): volume = 10^((−18.2 − RMS) / 20). That makes the end loops about as loud as the title, which is about 0.5 dB louder than the show loop. RMS is a rough guide; write each value under "## Findings" so a listening pass can tune it.
   - **`Retro Mystic` at 2.11:** a sound wave's `volume` takes values above 1 (the mixer caps it at 4). If the editor clamps it to 1.0, leave it at 1.0, write that down, and note the loop will be about 6.5 dB quieter than the others.
3. Save the eleven new assets by path (`save_assets` with the list; an empty list saves every dirty asset, T20).

## 4. `BPC_ShowAudio`: a track for each key

Lock `Content/NHOS/Core/BPC_ShowAudio.uasset` first (`git lfs lock`). Re-check the diff named at the top.

**Why an `if` chain and not a `Name` to `SoundBase` map:** no graph in this project has used a map node through the DSL, and T20's `Sfx` proves the `streq` and `return` chain with object literals. `TrackFor` keeps every asset path in one graph, so each track is still referenced by a Blueprint and the cook packs it (the task's reason not to read paths from JSON).

**Order of work** (T20: a new function's inputs exist for the DSL only after a compile):

1. Add the variable `EndWin` (Boolean, default false).
2. Add six function graphs with their params, empty: `TrackFor` (input `Key` String; output `Sound`, a `SoundBase` object reference), `PhaseKey` (input `Text` String; output `Key` String), `PlayPhase` (inputs `Text` String, `CardId` String), `StopMusic` (none), `DuckMusic` (none), `EndMusic` (none). None of these names exists in `BP_Show` or `BPC_ShowAudio` today (byte search at `944978c`), so T20's name clash can't happen.
3. `compile_blueprint`.
4. Write the graphs below, leaves first: `TrackFor`, `PhaseKey`, `StopMusic`, `DuckMusic`, then `SwapMusic`, `PlayPhase`, `EndMusic`, `StartDrum`, `Reveal`, `EndCheer`. Compile with `warnings_as_errors` = true (T06: a pruned impure node only warns).
5. Save each source to its `Graphs/BPC_ShowAudio/<Graph>.txt`.

`PlayMusic` doesn't change: the same key twice still does nothing, and `StopMusic` clears `MusicKey`, so a key asked for after a stop always starts its loop.

These sources are the hard-cut version. Step 6 (part 6) splices the fades into `StopMusic`, `SwapMusic` and `DuckMusic` afterwards.

```lisp
;;; GRAPH TrackFor
; T71: the loop for each music key. A key with no track of its own ("show", or a card added later) gets T20's show loop.
; Every track is named here, so the cook packs each one.
(fn TrackFor (Key)
  (if (streq Key "title")
    (return "/Game/NHOS/Audio/Music/S_MusicTitle.S_MusicTitle"))
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
  (if (streq Key "cut")
    (return "/Game/NHOS/Audio/Music/S_MusicCut.S_MusicCut"))
  (if (streq Key "win")
    (return "/Game/NHOS/Audio/Music/S_MusicWin.S_MusicWin"))
  (if (streq Key "lose")
    (return "/Game/NHOS/Audio/Music/S_MusicLose.S_MusicLose"))
  (return "/Game/NHOS/Audio/Music/S_MusicShow.S_MusicShow"))
```

**Re-check:** T20 found that an object literal works on an object pin (`PlaySound2D :Sound`). A function's return pin of type `SoundBase` should take it the same way. If it doesn't (the pin stays empty, or `get_node_infos` shows no default object), drop `TrackFor` and put one `SpawnSound2D` per key in `SwapMusic`'s chain, the way T20's `SwapMusic` spawns its two loops.

```lisp
;;; GRAPH PhaseKey
; T71: the music key for the header a "phase" cue carries (BP_Show.CueHeader).
; "card" means the card in play. "" means no track of its own: the loop that plays goes on.
; Headers at 944978c: "SCENE PREP: SCENE n", "THE SCENE: SCENE n, ...", "FREE TALK: SCENE n...",
; "...: FREE TALK IS OVER", "THE CUT: ...", "REACTIONS: SCENE n", "THE SHOW IS OVER". T58 adds "LAST WORD: SCENE n".
(fn PhaseKey (Text)
  (if (Utilities|String|StartsWith :SourceString Text :InPrefix "SCENE PREP")
    (return "card"))
  (if (Utilities|String|StartsWith :SourceString Text :InPrefix "THE SCENE")
    (return "card"))
  (if (Utilities|String|StartsWith :SourceString Text :InPrefix "FREE TALK")
    (return "free_talk"))
  (if (Utilities|String|StartsWith :SourceString Text :InPrefix "THE CUT")
    (return "cut"))
  (return ""))
```

What each header gets:

| Header | Key | What plays |
|---|---|---|
| `SCENE PREP: SCENE n` | the card | The card's loop starts at Scene Prep (scene 1 too: see part 5b) |
| `THE SCENE: SCENE n, TURN t` | the card | Already playing, so nothing changes. A safety net if the prep header was missed. |
| `FREE TALK: SCENE n` | `free_talk` | The Free Talk loop |
| `...: FREE TALK IS OVER` | none | The Free Talk loop goes on (it doesn't start with "FREE TALK") |
| `LAST WORD: SCENE n` (T58) | none | The Free Talk loop goes on, as the task asks |
| `THE CUT: ...` | `cut` | The Cut loop, until the drum roll |
| `REACTIONS: SCENE n` | none | Nothing: the reveal stopped the Cut loop, and the crowd carries the reactions |
| `THE SHOW IS OVER` | none | Nothing, until the end screen's loop |

```lisp
;;; GRAPH PlayPhase
; T71: the one call RunCue's "phase" cue makes. The card id comes from BP_Show's CardId, which only
; changes inside ScenePrep, and ScenePrep runs at its own cue's turn (T30), so it is never ahead of the queue.
(fn PlayPhase (Text CardId)
  (bind _k (CallFunction|PhaseKey :Text Text))
  (if (streq _k "card")
    (CallFunction|PlayMusic :Key CardId)
    (return))
  (if (not (Utilities|String|IsEmpty _k))
    (CallFunction|PlayMusic :Key _k)))
```

```lisp
;;; GRAPH StopMusic
; T71: stops the loop that plays and forgets its key, so the next PlayMusic always starts a loop.
; Step 6 replaces StopDelayed with the Audio Component's FadeOut (1.0 s, to 0.0), spliced in by create_node.
(fn StopMusic ()
  (if (not (Utilities|String|IsEmpty (V MusicKey)))
    (Audio|Components|Audio|StopDelayed :self (V Music) :DelayTime 0.0))
  (set MusicKey ""))
```

```lisp
;;; GRAPH DuckMusic
; T71: the Cut loop drops to 40% under the drum roll; Reveal and the tie stop it (part 5c).
; Step 6 splices the Audio Component's AdjustVolume (1.0 s, to 0.4) in after the print, by create_node.
(fn DuckMusic ()
  (if (streq (V MusicKey) "cut")
    (print "NHOS: SOUND duck")))
```

If part 5c finds that the Cut loop plays long enough before the drum (5 s or more), or the `AdjustVolume` splice fails, `DuckMusic` isn't used: `StartDrum` calls `StopMusic` instead (the task's first option).

```lisp
;;; GRAPH SwapMusic
; T20: one music loop at a time. T71: each key has its own loop (TrackFor); a key with no track gets the show loop.
; Step 6 replaces SpawnSound2D with CreateSound2D and splices the Audio Component's FadeIn (1.0 s, to 1.0) after the set.
(fn SwapMusic (Key)
  (CallFunction|StopMusic)
  (set MusicKey Key)
  (print (cat "NHOS: SOUND music " Key))
  (bind _snd (CallFunction|TrackFor :Key Key))
  (bind _m (Audio|SpawnSound2D :Sound _snd))
  (set Music _m))
```

```lisp
;;; GRAPH StartDrum
; T20: the drum roll under the vote. StopDrum fades it at the reveal.
; The vote row's cue can come twice in a scene, so a drum already playing stops first.
; T71: the Cut loop drops low under the drum (DuckMusic), or stops (StopMusic) if part 5c says so.
(fn StartDrum ()
  (CallFunction|StopDrum)
  (CallFunction|DuckMusic)
  (print "NHOS: SOUND drum")
  (bind _d (Audio|SpawnSound2D :Sound "/Game/NHOS/Audio/Show/S_DrumRoll.S_DrumRoll"))
  (set Drum _d))
```

```lisp
;;; GRAPH Reveal
; T20: the cut: the drum stops, the stinger says who it was, the crowd follows 1.5 s later.
; T71: the Cut loop stops with the drum, so nothing plays under the stinger.
(fn Reveal (IsHuman)
  (set LastHuman IsHuman)
  (CallFunction|StopDrum)
  (CallFunction|StopMusic)
  (CallFunction|Sfx :Key (select IsHuman "sting_human" "sting_ai") :Pitch 1.0)
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "Crowd" :Time 1.5 :bLooping false))
```

```lisp
;;; GRAPH EndCheer
; T20: the end screen: the music stops; a win gets the long applause, a loss the laughs.
; T71: 3 s in, the win or lose loop starts (EndMusic).
(fn EndCheer (Win)
  (CallFunction|StopMusic)
  (set EndWin Win)
  (CallFunction|Sfx :Key (select Win "applause_win" "laughs") :Pitch 1.0)
  (Utilities|Time|SetTimerbyFunctionName :Object self :FunctionName "EndMusic" :Time 3.0 :bLooping false))
```

```lisp
;;; GRAPH EndMusic
; T71: the end screen's loop. If other music started first (Play Again within 3 s), it stays out of the way.
(fn EndMusic ()
  (if (Utilities|String|IsEmpty (V MusicKey))
    (CallFunction|PlayMusic :Key (select (V EndWin) "win" "lose"))))
```

`Reveal` isn't in T71's Touches line, but it is in the same asset and needs one node so that nothing plays under the stinger. Name it in the commit.

## 5. `BP_Show.RunCue`: the show asks for the right key

Lock `Content/NHOS/Core/BP_Show.uasset` (and check `git lfs locks` first: the chain machine holds it most of the time). Three changes, all in `RunCue`, all music calls:

```lisp
;;; GRAPH RunCue
; T30: a cued screen change, run by BPC_LinePlayer when its turn in the queue comes.
; T20: the cues also carry the sound: the show music under every header, the drum roll with the vote row,
; the stinger and the crowd at the cut, the applause or laughs at the end screen.
; T71: each header asks BPC_ShowAudio for its phase's music (PlayPhase), and Scene Prep for the card's.
(fn RunCue (Kind Text Num)
  (if (streq Kind "phase")
    (Class|BPCShowAudio|PlayPhase :self (V Audio) :Text Text :CardId (V CardId))
    (Class|WBPStage|SetPhase :self (Variables|Default|GetStage) :Phase Text)
    (return))
  (if (streq Kind "banner")
    (Class|WBPStage|ShowBanner :self (Variables|Default|GetStage) :Line Text)
    (return))
  (if (streq Kind "votes")
    (if (Utilities|String|IsEmpty Text)
      (Class|WBPStage|SetVoteOptions :self (Variables|Default|GetStage) :Names (Variables|Default|GetNoNames))
      (return))
    (Class|BPCShowAudio|StartDrum :self (V Audio))
    (CallFunction|ShowVotePick)
    (return))
  (if (streq Kind "cut")
    (Class|BPCShowAudio|Reveal :self (V Audio) :IsHuman (== Num (V HumanSeat)))
    (CallFunction|CutActor :Seat Num)
    (return))
  ; T52: a tie cuts nobody. The drum roll stops with no stinger, the audience laughs, and the reactions start.
  ; T71: the Cut loop stops with the drum.
  (if (streq Kind "tie")
    (Class|BPCShowAudio|StopDrum :self (V Audio))
    (Class|BPCShowAudio|StopMusic :self (V Audio))
    (Class|BPCShowAudio|Sfx :self (V Audio) :Key "laughs" :Pitch 1.0)
    (CallFunction|EndCut)
    (return))
  ; T71: ScenePrep picks the card first, then the card's loop starts.
  (if (streq Kind "prep")
    (CallFunction|ScenePrep)
    (Class|BPCShowAudio|PlayMusic :self (V Audio) :Key (V CardId))
    (return))
  (if (streq Kind "end")
    (Class|BPCShowAudio|EndCheer :self (V Audio) :Win (V ShowWin))
    (CallFunction|ShowEndScreen)
    (return))
  (print (cat "NHOS: CUE unknown " Kind)))
```

Write it after `BPC_ShowAudio` compiles with the new functions (T20: inputs exist for the DSL only after a compile). Save it to `Graphs/BP_Show/RunCue.txt`.

### 5a. The header texts (re-check)

Found by a byte search of `BP_Show.uasset` at `944978c` (no `Graphs/` file holds them): `SCENE PREP: SCENE `, `THE SCENE: SCENE `, `FREE TALK: SCENE `, `: FREE TALK IS OVER`, `THE CUT: SCENE `, `THE CUT: `, `REACTIONS: SCENE `, `THE SHOW IS OVER`. If T34 or T58 has landed, search again (`find_nodes` for `CueHeader` calls in `BP_Show`, then `get_node_infos` for each `Text` pin, or `strings` on the `.uasset`), and fix `PhaseKey`'s prefixes to match.

### 5b. When the card's loop starts, and `CardId` (decides one line)

- **Scene 1** doesn't come through a `prep` cue: `SetupShow` calls `ScenePrep` directly (T30: node 25). Its music comes from the `SCENE PREP: SCENE 1` header, which `ShowPrep` sends from inside `ScenePrep`. The queue is idle then, so the header runs at once, and `PlayPhase` asks for `CardId`.
- **Scenes 2 and on** come through the `prep` cue: `RunCue` runs `ScenePrep`, then asks for `CardId`. The `SCENE PREP` header that `ShowPrep` queues inside it runs next and asks for the same key, which does nothing.
- **Check:** `BP_Show` has a `CardOrder` variable, so the show likely shuffles the cards up front and `ScenePrep` sets `CardId` from it. Run `find_nodes` in `BP_Show` for `Set CardId` (`/Script/BlueprintGraph.K2Node_VariableSet`). Confirm that it is in `ScenePrep` and **before** the `ShowPrep` call.
  - If yes: everything above stands.
  - If `CardId` is set after `ShowPrep`'s header: remove `PhaseKey`'s `SCENE PREP` line. Scene 1's card loop then starts at its first turn's header (`THE SCENE: SCENE 1`), and the title loop plays under scene 1's Scene Prep, as it does today. Scenes 2 and on still start at Scene Prep through the `prep` cue.
  - If `CardId` is set anywhere outside `ScenePrep` (for example in `EndReactions`), then it can run ahead of the queue. Stop and rethink: the card id must then ride on the `prep` cue's `Text` (`CuePrep` would send it), which changes `CuePrep` too.

### 5c. How long the Cut loop plays before the drum (decides one function)

At `944978c`, `StartCut` queues The Cut's header (`CueHeader`) and then the vote row (`CueVotes("show")`, twice) in the same call (T09, T30). Only `banner` and `stamp` cues hold the queue, so the vote row's cue, and `StartDrum` with it, runs right after The Cut's header. **A Cut loop that stops at `StartDrum` would play for only a moment.** So the sheet uses the task's other option: the Cut loop drops low (to 40%) under the drum roll, and stops at the reveal or the tie.

- **Check** in the first fast autoplay log: the time between `NHOS: SOUND music cut` and the next `NHOS: SOUND drum`. If it is 5 s or more, change `StartDrum`'s `(CallFunction|DuckMusic)` to `(CallFunction|StopMusic)` and drop `DuckMusic`.
- With the duck, the Cut loop plays at about 0.62 × 0.35 × 0.4 ≈ 0.09 effective under the drum roll (0.64). That should be a bed, not a rival. Write it under "## Findings" as unchecked by ear.

## 6. The fade between tracks (about 1 s)

T20 found that the DSL picks the Synth Component's `FadeOut`, `FadeIn` and `AdjustVolume`, which can't wire to an Audio Component. T01 found the way around it: `create_node` with `declaring_class`, then `connect_pins`, after the last DSL write to that graph (`write_graph_dsl` replaces the whole graph). So do step 6 after part 4's graphs compile and the hard-cut check has passed once.

| Graph | Splice | Node (`declaring_class` `/Script/Engine.AudioComponent`) | Pins |
|---|---|---|---|
| `StopMusic` | Replace the `StopDelayed` node: the branch's True exec → `FadeOut` → the `Set MusicKey` node | `FadeOut` | `self` ← a `Get Music` node; `FadeOutDuration` 1.0; `FadeVolumeLevel` 0.0; `FadeCurve` Linear |
| `SwapMusic` | Replace `SpawnSound2D` with `CreateSound2D` (the DSL can write that one: `(Audio|CreateSound2D :Sound _snd)`; set `bAutoDestroy` true if the pin shows), then after `Set Music`, add `FadeIn` | `FadeIn` | `self` ← a `Get Music` node; `FadeInDuration` 1.0; `FadeVolumeLevel` 1.0; `StartTime` 0.0; `FadeCurve` Linear |
| `DuckMusic` | After the `print`, add `AdjustVolume` | `AdjustVolume` | `self` ← a `Get Music` node; `AdjustVolumeDuration` 1.0; `AdjustVolumeLevel` 0.4; `FadeCurve` Linear |

- Old and new loops then cross-fade over 1 s: `StopMusic` fades the old one out while `SwapMusic`'s `FadeIn` brings the new one up. A component spawned by `SpawnSound2D` or `CreateSound2D` destroys itself after it stops (auto-destroy), so the faded loop goes away on its own.
- For `SwapMusic`, an easier splice works too, if `CreateSound2D` gives trouble: keep `SpawnSound2D` and add `FadeIn` after `Set Music`. `FadeIn` restarts the sound from 0 with the fade, in the same frame, so nothing should be heard at full volume.
- **Keep the `Graphs/` files true.** The DSL can't write these three nodes, so after the splice, add a line at the top of each of the three files: `; After this source is written, T71 step 6 splices <node> in by create_node (see Docs/tasks/T71-build.md part 6). A rewrite from this file must redo the splice.` (`Graphs/README.md`: change the file to match, or delete it.)
- **If `create_node` fails** for these nodes, keep the hard cut, keep `StopMusic` in `StartDrum` (part 5c), and write why under "## Findings", as the task says.

## 7. The check runs

1. **Free autoplay show with `fast_lines`**, in a game window on the saved assets (Mac command and log path: T27's findings in `Docs/tasks/T27.md`; on the PC, the `-game -windowed` command in `CLAUDE.md`). Use `-log=T71fast.log`, `"mode": "free"`, `"autoplay": true`, `"fast_lines": true` in `Local/switches.json`, and set `autoplay` back to false afterwards.
2. **Read the log** for the music lines and what's around them:

   ```bash
   grep -E "NHOS: (SOUND (music|duck|drum|sting|laughs|applause)|ACT reset card=|PREP shown|CUE|SHOW END)" T71fast.log
   ```

   Expected, for a 5-actor show (4 scenes) that the human loses in scene 3 (the shape of T20's run):

   ```
   NHOS: SOUND music show                 (autoplay skips the title: the fallback loop)
   NHOS: ACT reset card=<card 1>
   NHOS: SOUND music <card 1>             (SCENE PREP: SCENE 1)
   NHOS: PREP shown scene=1
   NHOS: SOUND music free_talk
   NHOS: SOUND music cut
   NHOS: SOUND duck
   NHOS: SOUND drum
   NHOS: SOUND duck                       (the vote row's second cue: the drum restarts, and the duck runs again harmlessly)
   NHOS: SOUND drum
   NHOS: SOUND sting_ai
   NHOS: SOUND applause / laughs
   NHOS: ACT reset card=<card 2>
   NHOS: SOUND music <card 2>             (the prep cue)
   ... the same for scenes 2 and 3 ...
   NHOS: SOUND sting_human
   NHOS: SOUND laughs                     (the end screen, a loss)
   NHOS: SOUND music lose                 (3 s later)
   NHOS: SHOW END result=lose ...
   ```

   The `ACT reset` line may come just before or just after its card's music line, depending on where `StagePrep` sits in `ScenePrep`; the order check below doesn't depend on it.
3. **The order check** (Python 3, no packages). It checks that each scene's card loop is the card in play, and that Free Talk and The Cut follow it, in that order:

   ```python
   import re, sys
   lines = open(sys.argv[1], encoding="utf-8", errors="replace").read().splitlines()
   ev = []
   for l in lines:
       m = re.search(r"NHOS: ACT reset card=(\S+)", l)
       if m: ev.append(("card", m.group(1)))
       m = re.search(r"NHOS: SOUND music (\S+)", l)
       if m: ev.append(("music", m.group(1)))
   cards = [v for k, v in ev if k == "card"]
   music = [v for k, v in ev if k == "music"]
   print("cards:", cards)
   print("music:", music)
   ok = True
   for c in cards:
       if c not in music:
           print("MISSING music for", c); ok = False
   seq = [m for m in music if m not in ("show", "title")]
   for c in cards:
       i = seq.index(c) if c in seq else -1
       if i < 0 or seq[i + 1:i + 3] != ["free_talk", "cut"]:
           print("ORDER?", c, seq[i:i + 3]); ok = False
   print("end key:", seq[-1] if seq else None)
   print("OK" if ok and seq and seq[-1] in ("win", "lose") else "CHECK BY HAND")
   ```

   `ACT reset card=` comes from `BP_StageDirector.ResetStage` (T45). If it no longer prints, use `NHOS: STAGE backdrop <id>` (the backdrop ids differ from the card ids; map them with `scenes.json`).
4. **No new `LogScript` warning** (`grep -c LogScript T71fast.log`, compared with a run before the change if there is one). An "Accessed None" on `Music` would mean `StopMusic` ran with a key but no component.
5. **One PIE show by hand** (Test for Free, autoplay off, as the plan's "Claude does the playing" note says): `NHOS: SOUND music title` on the title screen, then `NHOS: SOUND music <card 1>` when the first Scene Prep opens. Then press Play Again on the end screen within 3 s of it opening, and check that no `SOUND music win` or `lose` line comes after `SOUND music title` (or the first card).
6. **Each card id has its own track and no track is used twice:** `TrackFor`'s source has 12 keys and 12 different assets, plus the fallback. Check that `scenes.json` has no card id `TrackFor` lacks:

   ```bash
   python3 -c "import json,re;ids=[c['id'] for c in json.load(open('Content/NHOS/Data/scenes.json'))['cards']];src=open('Graphs/BPC_ShowAudio/TrackFor.txt').read();keys=re.findall(r'streq Key \"(\w+)\"',src);paths=re.findall(r'(S_Music\w+)\.S_Music',src);print('missing',[i for i in ids if i not in keys]);print('dupes',len(paths)-len(set(paths)))"
   ```

   Expect `missing []` and `dupes 0`.
7. **Not checkable by Claude:** how anything sounds: the seams flagged in part 1, the volumes, the cross-fade, the duck under the drum. Write them under "## Findings" as unchecked, with the volume set on each wave.

## 8. Findings to copy into `T71.md`

The task's Done-when asks for why each track was picked: copy part 1's table (the key, file, length, tempo, why) and the volume set on each wave, and say which picks are guesses (part 1, "Which picks my person should listen to").

## Decisions made for my person

These were mine to make for you. Each is the task's default or my recommendation; say if you want another.

1. **The title keeps `S_MusicTitle`** (`Swinging Pants`), the task's default. Its seam measures doubtful (part 1); if you hear a hiccup, `Flowing Rocks` is the closest free loop.
2. **No Music Jingle stings** at the end: the applause or laughs already do that job, and the end loop starts 3 s into them.
3. **The Cut loop drops to 40% under the drum roll** instead of stopping, because the drum starts right after The Cut's header (part 5c). It stops at the reveal and at a tie. If the log shows 5 s or more before the drum, T71 stops it instead (the task's first option).
4. **The reactions after a cut get no music**: the reveal stopped the Cut loop, and the applause and laughs fill that moment. The next card's loop starts at the next Scene Prep.
5. **The end loop starts 3 s** into the applause or laughs.
6. **`Cheerful Annoyance` for the diner, not `Retro Beat`**, so that the diner and the computer office (`Retro Mystic`) don't share the Retro set's sound.
7. **`Alpha Dance` for the bowling alley**, a dance loop under the starry ceiling, over a laid-back loop for the slacker (`Retro Reggae` is the second choice).
8. **An `if` chain (`TrackFor`), not a map variable**, for the key-to-track lookup: the DSL has no tested map node in this project, and the chain still references every track for the cook.
9. **Volumes matched by measured loudness** to T20's show loop (scene, Free Talk, Cut) and title loop (win, lose), not tuned by ear.
