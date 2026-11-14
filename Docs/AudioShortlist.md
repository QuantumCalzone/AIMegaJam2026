# Audio shortlist (T20 prep)

Files picked for T20, chosen without the editor. They are in `Local/audio/`, which git ignores. T20 imports them into `Content/NHOS/Audio/` and moves these entries into `Docs/Assets.md` and `Docs/DevLog.md`.

The picks were made by name, length and license, without listening. T20's listening pass makes the final choice; swap in the backup or a nearby file from the same pack if a pick sounds wrong.

## Sources

- **Kenney Game Assets All-in-1 3.8.0** (https://kenney.itch.io/kenney-game-assets), bought by the team. The bundle holds Kenney's free packs. Each pack's `License.txt` says **CC0 1.0** (https://creativecommons.org/publicdomain/zero/1.0/), so no credit is needed. Optional credit: "Kenney (www.kenney.nl)". The bundle's Audio folder is unpacked in `Local/audio/kenney/`. Format: Ogg Vorbis, 44.1 kHz unless noted.
- **Wikimedia Commons** (https://commons.wikimedia.org), in `Local/audio/commons/`. Licenses are per file, below.
- No AI audio tools were used.

## Picks

Paths are relative to `Local/audio/`.

| Sound | Chosen file | Backup | License | Length, format |
|---|---|---|---|---|
| Title music loop | `kenney/Music Loops/Loops/Swinging Pants.ogg` | `kenney/Music Loops/Loops/Cheerful Annoyance.ogg` (12.0 s) | CC0 | 24.2 s, ogg stereo |
| Show music loop (quieter) | `kenney/Music Loops/Loops/Wacky Waiting.ogg` | `kenney/Music Loops/Loops/Mishief Stroll.ogg` (31.8 s) | CC0 | 12.0 s, ogg stereo. Play it at low volume under the scene. |
| Drum roll (vote) | `commons/Long_Drum_Roll_with_Cymbal_Crash_at_End.wav` | `commons/Kevin_MacLeod_assorted_rimshots_-_7-second_roll.wav` (11.0 s, CC BY 3.0) | CC0 | 18.8 s, wav 16-bit 44.1 kHz stereo. Ends on a cymbal crash, so cut or fade it to match the reveal. |
| Reveal stinger: HUMAN | `kenney/Music Loops/Idents/Serious ident.ogg` | `kenney/Music Jingles/Audio (Saxophone)/jingles-saxophone_06.ogg` (1.7 s) | CC0 | 5.3 s, ogg stereo |
| Reveal stinger: AI | `kenney/Music Loops/Retro/Retro Comedy.ogg` | `kenney/Retro Sounds 2/Audio/lose1.ogg` (0.6 s) | CC0 | 6.0 s, ogg stereo 48 kHz |
| Applause (after a cut) | `commons/277021_sandermotions_applause-2.wav` | `commons/619016_mrrap4food_clapping-then-leaving.mp3` (28.7 s, CC0) | CC0 | 6.3 s, wav 16-bit 44.1 kHz |
| Applause (win) | `commons/Thomas_Bresson_-_Applaudissements.mp3` | the after-a-cut file, looped or played twice | CC BY 4.0 | 46.7 s, mp3 |
| Laughs | `commons/72844_lonemonk_approx-800-laughter-and-clapter-1.wav` | `72843_lonemonk_approx-800-laughter-only-1.wav` (13.8 s, CC BY 3.0, not downloaded yet: https://upload.wikimedia.org/wikipedia/commons/5/55/72843_lonemonk_approx-800-laughter-only-1.wav) | CC BY 3.0 | 9.9 s, wav 16-bit 44.1 kHz stereo |
| UI click | `kenney/Interface Sounds/Audio/click_001.ogg` | `kenney/UI Audio/Audio/click1.ogg` | CC0 | 0.1 s, ogg mono |
| UI hover (optional) | `kenney/UI Audio/Audio/rollover1.ogg` | `kenney/Interface Sounds/Audio/tick_001.ogg` | CC0 | 0.2 s, ogg stereo |
| Talk blip (pitched per persona) | `kenney/Interface Sounds/Audio/pluck_001.ogg` | `kenney/Digital Audio/Audio/pepSound1.ogg` (0.5 s) | CC0 | 0.1 s, ogg stereo |
| Robot move (step) | `kenney/Impact Sounds/Audio/footstep_concrete_000.ogg` (variants `_001` to `_004`) | `kenney/Sci-Fi Sounds/Audio/computerNoise_000.ogg` (5.0 s, a servo bed) | CC0 | 0.1 s, ogg stereo |
| Robot grab | `kenney/RPG Audio/Audio/cloth1.ogg` | `kenney/Casino Audio/Audio/dice-grab-1.ogg` (0.7 s) | CC0 | 0.7 s, ogg stereo 48 kHz |
| Robot throw | `kenney/Foley Sounds/Audio/Woosh/woosh1.ogg` | `kenney/Casino Audio/Audio/dice-throw-1.ogg` (0.6 s) | CC0 | 0.4 s, ogg stereo 96 kHz |
| Thrown prop lands | `kenney/Impact Sounds/Audio/impactSoft_medium_000.ogg` | `kenney/Impact Sounds/Audio/impactPlank_medium_000.ogg` (0.8 s) | CC0 | 0.1 s, ogg stereo |

## Attribution text (for the CC BY files in use)

Put these in the credits and the itch.io page if the file ships:

- **Win applause:** "Applaudissements" by Thomas Bresson, CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), via Wikimedia Commons: https://commons.wikimedia.org/wiki/File:Thomas_Bresson_-_Applaudissements.mp3
- **Laughs:** "approx 800 laughter and clapter 1" by lonemonk (https://freesound.org/people/lonemonk/packs/4695/), CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/), via Wikimedia Commons: https://commons.wikimedia.org/wiki/File:72844_lonemonk_approx-800-laughter-and-clapter-1.wav
- **Backup laughs, if used:** "approx 800 laughter only 1" by lonemonk, CC BY 3.0, via Wikimedia Commons: https://commons.wikimedia.org/wiki/File:72843_lonemonk_approx-800-laughter-only-1.wav
- **Backup drum roll, if used:** "7-second roll" from Assorted Rimshots by Kevin MacLeod (incompetech.com), CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/), via Wikimedia Commons: https://commons.wikimedia.org/wiki/File:Kevin_MacLeod_assorted_rimshots_-_7-second_roll.wav

CC0 sources, credited as a courtesy:

- Drum roll: "Long Drum Roll with Cymbal Crash at End" by Ddis tts, CC0: https://commons.wikimedia.org/wiki/File:Long_Drum_Roll_with_Cymbal_Crash_at_End.wav
- Applause: "applause-2" by Sandermotions (Freesound 277021), CC0: https://commons.wikimedia.org/wiki/File:277021_sandermotions_applause-2.wav
- Backup applause: "clapping-then-leaving" by mrrap4food (Freesound 619016), CC0: https://commons.wikimedia.org/wiki/File:619016_mrrap4food_clapping-then-leaving.mp3
- Everything under `kenney/`: Kenney (www.kenney.nl), CC0.

## File types and LFS

The picks are `.ogg`, `.wav` and `.mp3`. `.gitattributes` already sends all three to LFS, so no new rule is needed. Unreal stores the imported sounds as `.uasset`, which is also in LFS. The source files stay in `Local/` and are not committed.

## Notes for T20

- Unreal's importer takes `.wav`, `.ogg` and `.flac` for certain. If a `.mp3` won't import, convert it to `.wav` first (the Kenney launcher can convert audio; Audacity also works).
- The Kenney bundle also has `Synth Voice 1/2` and `Voiceover Pack` (robot and announcer lines such as "eliminated", "congratulations", "game over"). They aren't needed for the MVP, but they could add flavor to the reveal.
- The bundle zip (`Kenney Game Assets All-in-1 3.8.0.zip`, 555 MB) is untracked in the repo root. Keep it out of commits, or move it into `Local/`.
