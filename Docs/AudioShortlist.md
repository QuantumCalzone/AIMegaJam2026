# Audio shortlist (T20 prep, T100 music, T101 sounds and voices)

Files picked for T20, chosen without the editor. The picks and their backups are committed in `SourceAssets/Audio/`, outside `Content/` so Unreal doesn't import them on its own, and every machine gets them with `git pull`. T20 imports them into `Content/NHOS/Audio/` and moves these entries into `Docs/Assets.md`.

The picks were made by name, length and license, without listening. T20's listening pass makes the final choice; swap in the backup or a nearby file from the same pack if a pick sounds wrong.

The music for every phase and every scene card was replaced in T100: see "Music (T100)" first. Every other sound and three of the four robot voice sets were replaced in T101: see "Show, robot and button sounds, and the bots' voices (T101)". The rest of this file is T20's shortlist, kept as the record of how T20 chose. All of its rows are superseded: the music by T100, everything else by T101.

## Music (T100)

Picked by my person by ear on 2026-11-17, one track for each phase and one for each scene card, on a private listening page. These replace T20's title and show loops and T71's eleven loops. T102 imports them into `Content/NHOS/Audio/Music/`, sets the mix and moves these entries into `Docs/Assets.md`. Until then the game still plays the Kenney loops. How T100 got here is in [T100's findings](tasks/T100.md).

- **Source:** Stable Audio 3 (model `stable-audio-3`), Stability AI's text-to-audio model, through the Stability AI API (https://platform.stability.ai), on my person's own account. Claude wrote the prompts, and my person changed them: a Mozart-style title, symphonic film score for the scenes except three, and orchestral for everything else. 46 takes were made in all, at 8 credits ($0.08) each: $3.68. No other audio tool was used.
- **License:** Stability AI's Terms of Service (effective 2026-09-30, https://stability.ai/terms-of-service) say that, as between Stability and the user, "you own the Output (to the extent permitted by applicable law)". Stable Audio's pricing page (https://stableaudio.com/pricing) lists a commercial license on every plan. Only a company that makes over $1M a year needs an enterprise license. No credit is required. The terms forbid removing any watermark or provenance mark that Stability adds, so never process the files to strip one.
- **Files:** `SourceAssets/Audio/music/t100/<NN>_<key>.flac`, named by the music key T102 uses.
  - Each file is the loop as cut: a whole number of bars from the steady middle of a 120 s take, with a 0.25 s blend at the seam, so the end runs straight into the start.
  - 16-bit, 44.1 kHz stereo, lossless FLAC (109 MB for all 16), at the level the model made it (about −14 LUFS).
  - The folder is `music/`, not `Music/`: `SourceAssets/Audio/music/` already exists, and Mac and Windows file systems can't hold both.
  - The full 120 s takes, the 30 takes not picked and each take's note (prompt, seed, generation id) are only in `Local/audio/candidates/` on the Mac.
- **The brief:**
  - Background music under the talk.
  - No vocals.
  - No lead melody that competes with the lines. The title, win and lose screens have no talk, so they may carry a tune.
  - Soft dynamics and a clean loop.
  - It may suggest a film's genre, but never imitates a real film's score. The prompts name no film, composer or artist. Mozart, named for the title, is centuries out of copyright and isn't a film score.
- **The measurements** come from Claude's scripts, not from listening:
  - Loudness is integrated (BS.1770, K-weighted, gated).
  - "Swing" is the spread of 3 s short-term loudness, 5th to 95th percentile.
  - "Clipped" counts samples at full scale in the 120 s take.
  - "Seam" is how well the audio around the loop's end matches the audio around its start.
  My person heard every pick, flags included.

| Key | File | Plays during | What it is | Tempo, loop | Take | Measured | My person's words |
|---|---|---|---|---|---|---|---|
| `title` | `01_title.flac` | Title screen | Mozart-style comic opera overture: strings, oboes and flutes, horns, timpani, harpsichord | 126 BPM, 4/4, 36 bars, 69.1 s | B | -14.4 LUFS; swing 9.1 LU; 0 clipped in the take; seam listen to it | Asked for the title music to be "more like a grand symphony that would be in a play? Maybe even almost Mozart", then picked take B. |
| `scene_prep` | `02_scene_prep.flac` | Scene Prep, every card | Quiet symphonic underscore: pizzicato, sustained strings, woodwinds, celesta | 96 BPM, 4/4, 28 bars, 70.0 s | B | -14.3 LUFS; swing 10.7 LU; 4,692 clipped in the take; seam listen to it | Asked to "Make it orchestral", then picked take B. |
| `space_plans` | `03_space_plans.flac` | The Scene, `space_plans` | Symphonic space-adventure underscore at desert dusk: low strings, soft horns, harp | 78 BPM, 4/4, 20 bars, 62.8 s | B | -17.3 LUFS; swing 10.0 LU; 238 clipped in the take; seam listen to it | Asked for the scenes to be "more soundtrack movie style, so symphonic", then picked take B. |
| `mine_bridge` | `04_mine_bridge.flac` | The Scene, `mine_bridge` | Dark symphonic fantasy underscore: low strings and brass, distant drums, bell tones | 71 BPM, 4/4, 24 bars, 82.3 s | B | -13.7 LUFS; swing 9.7 LU; 350 clipped in the take; seam good | Asked for the scenes to be "more soundtrack movie style, so symphonic", then picked take B. |
| `dino_island` | `05_dino_island.flac` | The Scene, `dino_island` | Adventurous symphonic underscore: horns, pizzicato, marimba, hand percussion | 104 BPM, 4/4, 32 bars, 73.8 s | B | -14.0 LUFS; swing 3.1 LU; 368 clipped in the take; seam good | Asked for the scenes to be "more soundtrack movie style, so symphonic", then picked take B. |
| `favor_father` | `06_favor_father.flac` | The Scene, `favor_father` | Symphonic Italian wedding waltz: strings, mandolin, accordion, clarinet | 90 BPM, 3/4, 42 bars, 84.0 s | B | -13.7 LUFS; swing 6.0 LU; 56 clipped in the take; seam fair | Asked for the scenes to be "more soundtrack movie style, so symphonic", then picked take B. |
| `glowing_briefcase` | `07_glowing_briefcase.flac` | The Scene, `glowing_briefcase` | 1960s surf rock and soul pop: reverb guitar, combo organ, bass, drums | 118 BPM, 4/4, 44 bars, 89.5 s | B | -13.8 LUFS; swing 6.9 LU; 0 clipped in the take; seam listen to it | Asked for this scene to be "like pop music from a Tarantino movie", then picked take B. |
| `league_night` | `08_league_night.flac` | The Scene, `league_night` | 1960s folk: fingerpicked guitar, soft harmonica chords, upright bass, brushed snare | 88 BPM, 4/4, 30 bars, 81.8 s | B | -13.6 LUFS; swing 4.5 LU; 50 clipped in the take; seam listen to it | Asked for this scene to be "almost like folk music", then picked take B. |
| `pick_a_pill` | `09_pick_a_pill.flac` | The Scene, `pick_a_pill` | Cyberpunk drum and bass: rolling breakbeat, sub bass, dark pads, glitches | 172 BPM, 4/4, 44 bars, 61.4 s | B | -13.7 LUFS; swing 2.9 LU; 0 clipped in the take; seam good | Asked for this scene to be "kind of like a cyberpunk drum and bass type thing", then picked take B. |
| `free_talk` | `10_free_talk.flac` | Free Talk | Sneaky chamber-orchestra whodunit: pizzicato, staccato clarinet and bassoon, harp | 100 BPM, 4/4, 34 bars, 81.6 s | C | -14.1 LUFS; swing 11.5 LU; 4,769 clipped in the take; seam good | Asked to "redo everything that isn't a scene to symphonic / orchestral", then picked orchestral take C. |
| `last_word` | `11_last_word.flac` | Last Word | Hushed symphonic tension: low strings, tremolo violins, pizzicato ticks, harp | 84 BPM, 4/4, 24 bars, 68.6 s | F | -13.1 LUFS; swing 11.0 LU; 2,724 clipped in the take; seam good | Asked to "redo everything that isn't a scene to symphonic / orchestral", then picked orchestral take F. |
| `cut` | `12_cut.flac` | The Cut (40% under the drum roll) | Tense symphonic "thinking clock": string ostinato, pizzicato ticks, muted horns, woodblock | 112 BPM, 4/4, 40 bars, 85.7 s | C | -13.8 LUFS; swing 5.3 LU; 514 clipped in the take; seam listen to it | Asked to "redo everything that isn't a scene to symphonic / orchestral", then picked orchestral take C. |
| `reactions` | `13_reactions.flac` | Reactions | Wry, light symphonic underscore: strings, woodwinds, harp, pizzicato | 94 BPM, 4/4, 30 bars, 76.6 s | B | -14.2 LUFS; swing 8.6 LU; 438 clipped in the take; seam good | Asked to "redo everything that isn't a scene to symphonic / orchestral", then picked orchestral take B. |
| `win` | `14_win.flac` | End screen, win | Triumphant symphonic finale: brass fanfare chords, soaring strings, timpani | 124 BPM, 4/4, 40 bars, 77.4 s | D | -14.5 LUFS; swing 8.9 LU; 0 clipped in the take; seam fair | Asked to "Make it orchestral", then "Make it more triumphant.", then picked take D. |
| `lose` | `15_lose.flac` | End screen, lose | Wry, deflated symphonic shrug: slow strings, bassoon and tuba, clarinet | 72 BPM, 4/4, 24 bars, 80.0 s | C | -13.7 LUFS; swing 4.9 LU; 0 clipped in the take; seam good | Asked to "redo everything that isn't a scene to symphonic / orchestral", then picked orchestral take C. |
| `show` | `16_show.flac` | Fallback: a card with no track | Neutral, light symphonic film-set underscore: strings, woodwinds, harp | 100 BPM, 4/4, 33 bars, 79.2 s | B | -13.0 LUFS; swing 8.5 LU; 9 clipped in the take; seam listen to it | Asked to "redo everything that isn't a scene to symphonic / orchestral", then picked orchestral take B. |

### The prompts

For `Docs/Assets.md`, which records the AI tool and the prompt for every generated asset. Each take was 120 s, made with `output_format=wav`.

- `01_title.flac` (take B, seed 3247519507, made 2026-11-18, loop from 17.41 s of the 120 s take): "Grand classical-era symphony in the style of Mozart, a playful opera buffa overture in an elegant 18th-century theater: bright strings, oboes and flutes, French horns, timpani, harpsichord continuo. Festive, witty, a theatrical sense of occasion, steady tempo, instrumental, 126 BPM."
- `02_scene_prep.flac` (take B, seed 3596362908, made 2026-11-18, loop from 40.91 s of the 120 s take): "Quiet symphonic film score underscore, backstage just before the camera rolls on a film set: soft pizzicato strings, warm sustained strings, light woodwinds, gentle celesta, soft ticking percussion. Curious anticipation, quiet and steady, soft dynamics, instrumental, 96 BPM."
- `03_space_plans.flac` (take B, seed 3754550674, made 2026-11-18, loop from 8.41 s of the 120 s take): "Symphonic film score underscore for a space adventure on a desert planet at dusk under two suns: low sustained strings, soft French horns, harp, gentle timpani, distant woodwinds. Mysterious, wide and lonely, quiet and steady, soft dynamics, instrumental, 78 BPM."
- `04_mine_bridge.flac` (take B, seed 288248621, made 2026-11-18, loop from 28.65 s of the 120 s take): "Dark symphonic fantasy film score underscore deep inside an ancient dwarf mine: low strings, muted horns and low brass, soft deep drums like distant footsteps, faint bell tones, cavern reverb. Hushed, tense and ancient, quiet and steady, soft dynamics, instrumental, 70 BPM."
- `05_dino_island.flac` (take B, seed 599893121, made 2026-11-18, loop from 7.01 s of the 120 s take): "Adventurous symphonic film score underscore for a jungle island theme park: pizzicato strings, warm French horns, marimba and hand percussion, soft timpani pulse. Wonder with a hint of comic danger, steady and even, soft dynamics, instrumental, 104 BPM."
- `06_favor_father.flac` (take B, seed 1716905050, made 2026-11-18, loop from 26.89 s of the 120 s take): "Symphonic film score underscore for a sunny Italian garden wedding with a sly shadow: warm strings, mandolin, accordion, soft clarinet, gentle 3/4 waltz. Nostalgic, festive and quietly ominous, steady and even, soft dynamics, instrumental, 90 BPM."
- `07_glowing_briefcase.flac` (take B, seed 1363824617, made 2026-11-18, loop from 13.70 s of the 120 s take): "1960s surf rock and soul pop instrumental, a retro crime-film jukebox in a diner on dance-contest night: twangy spring-reverb electric guitar, vintage combo organ, punchy bass, tight drums. Cool, groovy, a little dangerous, steady and even, instrumental, 118 BPM."
- `08_league_night.flac` (take B, seed 566761696, made 2026-11-18, loop from 29.12 s of the 120 s take): "1960s folk instrumental for a laid-back bowling alley on league night: fingerpicked acoustic guitar, soft harmonica chords, upright bass, light brushed snare. Wry, easygoing and unbothered, steady and even, soft, instrumental, 88 BPM."
- `09_pick_a_pill.flac` (take B, seed 2488681773, made 2026-11-18, loop from 34.78 s of the 120 s take): "Cyberpunk drum and bass in a rain-soaked neon city at midnight: rolling breakbeat, deep sub bass, dark synth pads, glitchy digital textures. Tense, hypnotic, sleek, steady and even, instrumental, 172 BPM."
- `10_free_talk.flac` (take C, seed 2083969685, made 2026-11-18, loop from 16.30 s of the 120 s take): "Light sneaky chamber orchestra underscore, a cast whispering between takes while hunting for an impostor: playful pizzicato strings, staccato clarinet and bassoon, soft muted horn, light harp. Curious, playful, conspiratorial, quiet and steady, soft dynamics, instrumental, 100 BPM."
- `11_last_word.flac` (take F, seed 2298393024, made 2026-11-18, loop from 9.43 s of the 120 s take): "Quiet, tense symphonic underscore, a hushed room just before a vote: sustained low strings, soft tremolo violins, gentle pizzicato like a ticking clock, a faint harp shimmer. Suspended and expectant, quiet and steady, soft dynamics, instrumental, 84 BPM."
- `12_cut.flac` (take C, seed 3704110694, made 2026-11-18, loop from 11.47 s of the 120 s take): "Tense symphonic underscore for a game-show vote, like a thinking clock: a low string ostinato, staccato pizzicato ticks, soft muted horns, light woodblock. Suspenseful but quiet and even, steady, soft dynamics, instrumental, 112 BPM."
- `13_reactions.flac` (take B, seed 2832459487, made 2026-11-18, loop from 22.52 s of the 120 s take): "Wry, light symphonic underscore after a big reveal: warm strings, playful woodwinds, soft harp, gentle pizzicato. Relaxed and a little amused, neither triumphant nor sad, quiet and steady, soft dynamics, instrumental, 94 BPM."
- `14_win.flac` (take D, seed 3144764042, made 2026-11-18, loop from 15.28 s of the 120 s take): "Grand triumphant symphonic victory finale, a standing ovation at the end of a comedy stage play: full orchestra, bold brass fanfare chords, soaring strings, rolling timpani, bright woodwind runs. Jubilant, victorious and a little cheeky, steady and even, instrumental, 124 BPM."
- `15_lose.flac` (take C, seed 3852197593, made 2026-11-18, loop from 30.98 s of the 120 s take): "Wry, deflated symphonic underscore for a comedy game-over screen: slow strings, a mournful but funny bassoon and tuba, soft clarinet, gentle pizzicato. Gently sad and funny, a shrug, steady and even, soft dynamics, instrumental, 72 BPM."
- `16_show.flac` (take B, seed 3480459292, made 2026-11-18, loop from 9.52 s of the 120 s take): "Neutral, light symphonic film score underscore on a film set: soft strings, gentle woodwinds, harp, light pizzicato. Pleasant and unobtrusive, quiet and steady, soft dynamics, instrumental, 100 BPM."

### Credit lines

For `Docs/ItchPage.md`, the game's credits and the jam's "Tools you used" field. T100 doesn't edit those files. No credit is required, so these are courtesy lines, and they also declare the AI tool as the jam asks.

- **Short:** "Music generated with Stable Audio by Stability AI."
- **Long:** "Music: 16 tracks generated with Stable Audio 3 (Stability AI) through the Stability AI API, from prompts written with Claude (Anthropic), picked by the team."

## Show, robot and button sounds, and the bots' voices (T101)

My person picked these by ear on 2026-11-18, one per cue, on a private listening page. Every take there was set to the same loudness, so the sounds were compared, not their volume. They replace every T20 sound in `Content/NHOS/Audio/Show/`, `Robot/` and `UI/`, and three of the four robot voice sets. T102 imports them, sets the mix and moves these entries into `Docs/Assets.md`. Until then the game still plays T20's and T72's files. How T101 got here is in [T101's findings](tasks/T101.md).

- **Sources:** my person chose "both": free libraries (CC0, CC BY and public domain, from Kenney, OpenGameArt and Wikimedia Commons) and Stable Audio 3 (model `stable-audio-3`, Stability AI) through the Stability AI API on my person's own account, the same account and terms as T100. Stable Audio's terms give us the output with a commercial license and need no credit, and they forbid removing a watermark or provenance mark. 22 takes were made in all, at 8 credits ($0.08) each: $1.76. The voices are made by `Tools/make_voices.py`, which needs no license.
- **Files:** the picks are cut, faded and leveled to the same loudness as on the listening page (maximum momentary loudness −20 LUFS, the hover −30), as 16-bit, 44.1 kHz WAV, named for the asset each replaces:
  - `SourceAssets/Audio/show/`, `robot/` and `ui/`. The folders are lowercase, like `music/` and `voices/`: Mac and Windows file systems can't hold `Voice/` beside `voices/`, so the set keeps one style.
  - `SourceAssets/Audio/voices/<Provider>/`, written in place by `python Tools/make_voices.py`. The counts are unchanged (OpenAI 10, Anthropic 10, SpaceXAI 11, Meta 10), so `BPC_ShowAudio.LoadVoices` and `Syllable` need no change. `voices/Me/` is untouched.
  - Every take not picked, each with a note (source, license, prompt or cut, and why it fits), is only in `Local/audio/candidates/t101/` on the Mac.
- **S_TalkBlip has no pick.** Nothing plays it since T73, so T102 deletes it (the asset, `Sfx`'s "blip" branch and its row in `Docs/Assets.md`).

| Asset | File | What it is | Source | License and credit | Length | My person's words |
|---|---|---|---|---|---|---|
| `S_DrumRoll` | `show/S_DrumRoll.wav` | Orchestral snare roll over soft timpani, a crash every 4 s. **A 12 s loop**: three of the take's 4 s bars (0.97 to 12.97 s), with the 50 ms after the end blended into the start | Stable Audio, take B, seed 101021, 20 s take | Ours; no credit needed | 12.0 s, stereo, loops | Picked B over my recommendation of A. In recent shows the vote ran 25 to 50 s, longer than the take, so I cut a loop; my person chose "Use the loop". |
| `S_StingHuman` | `show/S_StingHuman.wav` | Melancholy: strings swell, then sink into a dark minor chord, a low horn sighs, a timpani roll fades | Stable Audio, round 2 take E, seed 101005, 4 s take | Ours; no credit needed | 3.9 s, stereo | Turned down A to C: "It should be on the sad side since it means the player lost." Then picked E over my recommendation of D. |
| `S_StingAI` | `show/S_StingAI.wav` | Cheeky "got away with it": a perky trumpet fanfare, a comic timpani boing, pizzicato, a squeaky clarinet giggle, a happy final chord | Stable Audio, round 2 take F, seed 101016, 4 s take | Ours; no credit needed | 3.1 s, stereo | Turned down A to C: "It should be a mix of triumphant for you and also a little silly for the bots being mistaken, which is funny." Then picked F over my recommendation of D. |
| `S_Applause` | `show/S_Applause.wav` | Applause in a real medium-large theater, 8 s cut with a 2 s fade | "Applause-2" by RHumphries (Freesound 1921), Wikimedia Commons: https://commons.wikimedia.org/wiki/File:Applause-2.ogg | **CC BY 3.0, credit needed** (below) | 8.0 s, stereo | Picked A, as I recommended. |
| `S_ApplauseWin` | `show/S_ApplauseWin.wav` | Standing ovation in an opera house: clapping, cheers, whistles, shouts of bravo; peaks early and tapers | Stable Audio, take B, seed 101041, 25 s take | Ours; no credit needed | 25.0 s, stereo | Picked B, as I recommended. |
| `S_Laughs` | `show/S_Laughs.wav` | A real audience of about 800 laughing, no clapping, 10 s cut with a 2 s fade | "approx 800 laughter only 1" by lonemonk (Freesound pack 4695), Wikimedia Commons: https://commons.wikimedia.org/wiki/File:72843_lonemonk_approx-800-laughter-only-1.wav | **CC BY 3.0, credit needed** (below) | 10.0 s, stereo | Picked A, as I recommended. |
| `S_Step0` to `S_Step4` | `robot/S_Step0.wav` to `S_Step4.wav` | Clay-robot steps on a wooden stage: a muted clay squelch with a light wooden tap. Five hits cut from one take (at 3.93, 5.13, 5.68, 6.22 and 6.94 s), 0.28 s each | Stable Audio, take C, seed 101061, 8 s take | Ours; no credit needed | 0.28 s each, stereo | Picked C, as I recommended. |
| `S_Grab` | `robot/S_Grab.wav` | A clay squeeze and grip, the first squish of the take (from 0.07 s) | Stable Audio, take C, seed 101071, 2 s take | Ours; no credit needed | 0.30 s, stereo | Picked C, as I recommended. |
| `S_Throw` | `robot/S_Throw.wav` | A short, clean swish | `swish-3.wav` from "Swishes sound pack" by artisticdude: https://opengameart.org/content/swishes-sound-pack | CC0; courtesy credit "artisticdude" | 0.13 s, stereo | Picked A, as I recommended. |
| `S_Land` | `robot/S_Land.wav` | A clay lump landing on a wooden floor: a muted squishy thud with a wooden knock (from 0.55 s) | Stable Audio, take C, seed 101091, 2 s take | Ours; no credit needed | 0.65 s, stereo | Picked C, as I recommended. |
| `S_Click` | `ui/S_Click.wav` | A real, short mechanical click | `click.9.ogg` from "10 clicks and switches" by StarNinjas: https://opengameart.org/content/10-clicks-and-switches | CC0; courtesy credit "StarNinjas" | 0.10 s, stereo | Picked B over my recommendation of A. |
| `S_Hover` | `ui/S_Hover.wav` | A tiny rising whoosh of air: white noise through a band-pass swept from 1.5 to 5 kHz over 0.1 s, 25 ms rise and fall | Made by Claude's script (round 3 take I, numpy, seed 10103) | Ours; no credit needed | 0.10 s, mono | Turned down A to C, chose "a softer sibling of the click", turned down D to F, then: "This sound should be a really soft hint. All it's supposed to do is indicate that your mouse is over an interactable element. Nothing mechanical, really, sounding to it. Maybe something airy." Picked I over my recommendation of G. |
| `S_VoiceOpenAI_00` to `_09` | `voices/OpenAI/` | Set B, an airy whistle: few harmonics, a lot of breath, a slightly sharp doubled copy, a slow rise, soft h and w onsets | `python Tools/make_voices.py` (`syl_openai_b`, seed 72731) | Ours | 0.09 to 0.12 s, mono | Picked B, as I recommended. |
| `S_VoiceAnthropic_00` to `_09` | `voices/Anthropic/` | Set A, T72's warm, round vowel, unchanged | `python Tools/make_voices.py` (`syl_anthropic`, seed 72722) | Ours | 0.09 to 0.13 s, mono | Picked A, T72's set, over my recommendation of B. |
| `S_VoiceSpaceXAI_00` to `_10` | `voices/SpaceXAI/` | Set B, an overclocked chiptune: a bare square wave leaping through a fast three-note arpeggio, crushed to 4 bits | `python Tools/make_voices.py` (`syl_spacex_b`, seed 72733) | Ours | 0.08 to 0.11 s, mono | Picked B, as I recommended. |
| `S_VoiceMeta_00` to `_09` | `voices/Meta/` | Set B, a rigid machine monotone: an exactly flat dark saw, ring-modulated at 55 Hz, switched on and off | `python Tools/make_voices.py` (`syl_meta_b`, seed 72734) | Ours | 0.10 to 0.14 s, mono | Picked B over my recommendation of C. |

My person also heard the four picked voice sets and their own voice one line after another, and said each is easy to tell apart ("Yes, keep them").

### The prompts

For `Docs/Assets.md`, which records the AI tool and the prompt for every generated asset. Every take was made on 2026-11-18 with `output_format=wav`.

- `S_DrumRoll` (seed 101021, 20 s): "Orchestral snare drum roll building suspense on a theater stage before a big reveal: a steady, even, tight snare roll that slowly swells, a soft timpani roll underneath, concert hall reverb, steady and sustained throughout, instrumental."
- `S_StingHuman` (seed 101005, 4 s): "Melancholy orchestral game-over sting: strings swell softly then sink into a dark minor chord, a low French horn sighs, a soft timpani roll fades away, short, instrumental."
- `S_StingAI` (seed 101016, 4 s): "Cheeky orchestral got-away-with-it sting: a perky trumpet fanfare in a major key, a comic timpani boing, plucky pizzicato and a squeaky clarinet giggle, ending on a bright, happy chord, instrumental."
- `S_ApplauseWin` (seed 101041, 25 s): "Rapturous standing ovation in a grand opera house: a full house clapping loudly, cheering and whistling, shouts of bravo, sustained enthusiasm, natural hall reverb, field recording."
- `S_Step0` to `S_Step4` (seed 101061, 8 s): "Claymation foley: soft squishy footsteps of a small clay robot walking across a wooden theater stage, each step a gentle muted clay squelch with a light wooden tap, evenly spaced single steps with quiet between them, dry close recording, sound effect."
- `S_Grab` (seed 101071, 2 s): "Claymation foley: a clay hand grabbing a small prop, one soft squishy clay squeeze and a gentle grip, close dry recording, single short sound effect."
- `S_Land` (seed 101091, 2 s): "Claymation foley: a lump of soft modeling clay landing on a wooden stage floor, one muted squishy thud with a light wooden knock, single short sound effect, dry close recording."

### Credit lines

The two CC BY files need a credit wherever the game's credits are shown (the credits screen, `Docs/ItchPage.md`):

- **Applause:** "Applause-2" by RHumphries, CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/), via Wikimedia Commons: https://commons.wikimedia.org/wiki/File:Applause-2.ogg
- **Laughs:** "approx 800 laughter only 1" by lonemonk, CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/), via Wikimedia Commons: https://commons.wikimedia.org/wiki/File:72843_lonemonk_approx-800-laughter-only-1.wav

Courtesy lines, not required:

- "Sound effects generated with Stable Audio by Stability AI." (Together with T100's line: "Music and sound effects generated with Stable Audio by Stability AI.")
- "Throw swish by artisticdude, click by StarNinjas (CC0, via OpenGameArt)."

## Sources

- **Kenney Game Assets All-in-1 3.8.0** (https://kenney.itch.io/kenney-game-assets), bought by the team. The bundle holds Kenney's free packs. Each pack's `License.txt` says **CC0 1.0** (https://creativecommons.org/publicdomain/zero/1.0/), so no credit is needed. Optional credit: "Kenney (www.kenney.nl)". The picks are in `SourceAssets/Audio/kenney/`, each pack folder with its `License.txt`. The bundle's whole Audio folder (1,325 files) is unpacked only on the Windows PC, in `Local/audio/kenney/`, which git ignores. Format: Ogg Vorbis, 44.1 kHz unless noted.
- **Wikimedia Commons** (https://commons.wikimedia.org), in `SourceAssets/Audio/commons/`. Licenses are per file, below.
- No AI audio tools were used for T20's picks. T100's music was made with Stable Audio (see "Music (T100)").

## Picks

T20's picks, all superseded by T100 and T101 (above). Paths are relative to `SourceAssets/Audio/`.

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

T20's lines. None of these files ships once T102 imports T101's picks; T101's own credit lines are under "Show, robot and button sounds, and the bots' voices (T101)". Until then, put these in the credits and the itch.io page if the file ships:

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

The picks are `.ogg`, `.wav` and `.mp3`. `.gitattributes` already sends all three to LFS, so no new rule is needed. Unreal stores the imported sounds as `.uasset`, which is also in LFS. The 32 picks, backups and footstep variants (about 11 MB) are committed in `SourceAssets/Audio/`, so T20 can run on any machine. If the listening pass wants a nearby Kenney file that isn't committed, it is only in `Local/audio/` on the Windows PC (or in the bundle zip): add it to `SourceAssets/Audio/` at the same path before you import it.

## Notes for T20

- Unreal's importer takes `.wav`, `.ogg` and `.flac` for certain. If a `.mp3` won't import, convert it to `.wav` first (the Kenney launcher can convert audio; Audacity also works).
- The Kenney bundle also has `Synth Voice 1/2` and `Voiceover Pack` (robot and announcer lines such as "eliminated", "congratulations", "game over"). They aren't needed for the MVP, but they could add flavor to the reveal.
- The bundle zip (`Kenney Game Assets All-in-1 3.8.0.zip`, 555 MB) is not committed. Keep it out of commits; if you have it, keep it in `Local/`.
