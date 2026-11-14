---
from: quantumcalzone
to: quantumcalzone
---

# T20 audio shortlist: candidates for every sound, with licenses

Research only, done on 2026-11-14 about 21:30 UTC. Nothing is downloaded, nothing in `Content/` is touched, and nobody has listened to any of these files. Every license below was read from the source page itself (Freesound, OpenGameArt, Kenney, Fab's API, incompetech), not from a search snippet. Where I could not read something, it says so.

For the task, the sounds are: music (title loop, show loop), vote drum roll, two reveal stingers, applause and laughs, UI clicks, talk blip, robot move/grab/throw.

## How the design uses these sounds

- The cut reveal is a big red rubber stamp. If the cut bot is an AI it reads "[PROVIDER]: AI" (the cast voted out one of its own). If it is you it reads "YOU: HUMAN" and you lose while the AIs gloat. So the AI stinger is the funny or relieved one, and the HUMAN stinger is the dramatic one.
- `Docs/GameDesign.md` line 239 lists applause under "Cut for the jam". `Docs/MVPPlan.md` T20 and this task keep it. It is only a few cheap clips, so I kept it. Your call.
- The design also has a hook that yanks the cut bot offstage and a costume yank. Cheap optional sounds for those are at the end.

## Picks in one table

Two plans. "Plan A" gives the best fit. "Plan B" is all CC0, needs no credit line, and needs no accounts except Freesound.

| Sound | Plan A | Plan B (all CC0) |
|---|---|---|
| Title loop | incompetech "Happy Happy Game Show" (CC BY 4.0) | OpenGameArt "Wacky Idlings" |
| Show loop | incompetech "Investigations" (CC BY 4.0) | OpenGameArt "Crowded Pub" |
| Vote drum roll | Freesound 201211 "Drum Roll Please" | same |
| AI stinger | Freesound 878609 "Ta-Da Fanfare" | same |
| HUMAN stinger | Freesound 879280 "Dramatic Piano Sting" | same |
| Cut: laughs and applause | Freesound 371562 "Sitcom Laughter with Applause" | same |
| Win: applause | Freesound 478411 "Concert audience applause 4" | same |
| UI clicks | Kenney "Interface Sounds" | same |
| Talk blip | OpenGameArt "Dialog vocal samples" | same |
| Robot move | Freesound 875419 "Robotic Servo Short Arm Movement" | Kenney "Sci-fi Sounds" |
| Grab | Kenney "RPG Audio" or "Impact Sounds" | same |
| Throw | Freesound 346373 "Throwing / Whip Effect" | OpenGameArt "Swishes Sound Pack" |

Only Plan A's two incompetech tracks need a credit line. Everything else in both plans is CC0 and needs none.

## Things T20 has to know

1. **Freesound needs a login to download.** Each sound page says "Login to download". An agent cannot sign in. You make a free Freesound account and download, or approve a different route. Kenney, OpenGameArt and incompetech files download with no login. Fab free items need your Epic login to add them to your Fab library.
2. **Unreal's audio import is untested here.** `.gitattributes` already stores `.wav`, `.mp3`, `.ogg` and `.flac` in LFS (lines 38 to 41). It has no rule for `.aif` or `.aiff`, so skip the one AIFF candidate (Freesound 132418) or add a rule. I did not check which formats the UE 5.8 Sound Wave importer accepts, and `ffmpeg` is not installed on this machine. First step of T20: import one OGG, one FLAC and one MP3 and see which work. If MP3 fails, the incompetech tracks need converting to WAV (for example with Audacity). Prefer WAV, FLAC or OGG for the two loops, because MP3 adds a small gap at the loop point.
3. **Credits screen.** incompetech's own FAQ says for video games, credits usually go on a Credits screen found in the settings menu. The game has none yet. If Plan A is used, put the two credit lines in `Docs/Assets.md`, on the itch.io page, and on a small text line on the title screen or a credits panel.
4. **`Docs/Assets.md` needs one row per file used**: what it is, the page URL, the author, the license and the license URL. The Audio section currently says "None yet (T20)".
5. **The jam's own audio partner.** The jam page lists WeLoveIndies ("Sound and music for non-commercial use ... If you release your game commercially later, you'll need a commercial license for those assets"). Its own page says 3,200+ music tracks and 250,000+ sounds, a project-based license, and an account. That conflicts with "a game we distribute" if the game ever earns money, so I kept it as a last resort, not a candidate.

## License terms, as written at the sources

- **Kenney.** Each pack page shows "License: Creative Commons CC0" linking https://creativecommons.org/publicdomain/zero/1.0/. No attribution is needed. No login is needed ("Continue without donating...").
- **Freesound CC0.** The sound page says: "Creative Commons 0. You can copy, modify, distribute and perform the sound, even for commercial purposes, all without the need of asking permission to the author." Legal code: https://creativecommons.org/publicdomain/zero/1.0/. I checked that each Freesound file listed below says "Creative Commons 0" and nothing else. I rejected the ones that said Attribution (for example 182442 drum roll with cymbals, 100904 crowd, 99966 crowd roar, 85893 long applause).
- **OpenGameArt CC0.** Each page lists "CC0". The "Dialog vocal samples" page adds: "Licensed under the Public Domain, crediting is appreciated but not obligatory."
- **incompetech (Kevin MacLeod), Creative Commons Attribution 4.0.** From https://incompetech.com/music/royalty-free/faq.html, the credit to place is:

  `"Title" Kevin MacLeod (incompetech.com)` then `Licensed under Creative Commons: By Attribution 4.0 https://creativecommons.org/licenses/by/4.0/`

  The FAQ says to replace the word Title with the real title of the piece. It says the credit must be placed so that a person who wants to know where the music came from has no difficulty finding it. The track pages are built by script, so I could not read a license line on each track page. The FAQ text covers the whole catalog. Look at the track page when you download.
- **Fab Standard License** (https://www.fab.com/eula, summary on the page). You may use the assets commercially, modify them, and "commercially distribute your Projects with the Fab assets incorporated into it". You may not "resell or redistribute the asset for free on a standalone basis". "Both pricing tiers (Personal and Professional) grant you the same scope of rights." "You are not required to give credit to the publisher." The summary says it is "not legally binding"; the full EULA on that page is. Items marked CC-BY on Fab are governed by Creative Commons instead and need credit.
- **ElevenLabs** (AI sound effects and music), from its help center article "Can I publish the content I generate on the platform?": "The free plan does not include a commercial license and cannot be used for any commercial purpose." Content made outside a paid subscription "always requires attribution when shared non-commercially". Paid plans include a commercial license. Beta services may not be used for any commercial purpose or in any production environment. Not needed, because there are enough CC0 files, so I did not shortlist it.

## 1. Music: title loop

1. **incompetech "Happy Happy Game Show"** by Kevin MacLeod. https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1600006
   - License: CC BY 4.0, credit text above.
   - MP3, 2:39, 230 BPM, 5.08 MB (from the file's HTTP header). Direct file: https://incompetech.com/music/royalty-free/mp3-royaltyfree/Happy%20Happy%20Game%20Show.mp3
   - Why it fits: organ, drums, bass, piano and horns on a 12-bar blues. The name and the feel are a game show, which is the exact joke of a show with robot actors. His note says the uncompressed download also includes a perfectly loopable version. I could not tell whether that is free, so check on the page.
2. **Fab "Cartoon Adventures Vol. 1 - 18 Music Tracks"** by MoodFrog. https://www.fab.com/listings/1c764866-1815-4b3f-8e80-657c86fb80df
   - License: Fab Standard, Personal tier $0.00 (Professional is $0.99; same rights). No credit needed.
   - 18 WAV files plus MP3 previews. Lengths not listed. The listing says "Royalty-free license for commercial use" and "No attribution required".
   - Why it fits: track names include "Welcome to Toonland" (cheerful intro), "Toy Store Swing" (playful jazz) and "Popcorn Parade" (circus march). Cartoon, jazz and circus is close to a comic stage.
3. **OpenGameArt "Wacky Idlings"** by Fupi. https://opengameart.org/content/wacky-idlings
   - License: CC0.
   - OGG, 166.2 KB. Length not listed. File: https://opengameart.org/sites/default/files/wackyidlings_0.ogg
   - Why it fits: the author's words are "Wacky loop with slap bass and swing for any kind of humorous game, made in Beepbox." It is a small chiptune-style loop, so it is the weakest of the three on polish and the strongest on zero friction. Another CC0 option from the same search is "Quirky Jazz" by Spring Spring (https://opengameart.org/content/quirky-jazz, MP3 11.8 MB; the page lists both OGA-BY 3.0 and CC0, so pick CC0).

## 2. Music: quieter loop for the show

1. **incompetech "Investigations"** by Kevin MacLeod. https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1100646
   - License: CC BY 4.0, credit text above.
   - MP3, 1:34, 94 BPM, 3.75 MB. File: https://incompetech.com/music/royalty-free/mp3-royaltyfree/Investigations.mp3
   - Why it fits: pizzicato strings, English horn, bassoon, marimba, glockenspiel and cowbells. The author's words: "a loafing comedic piece for all of your amusing scenes with dialog that does not need to move the story." That describes a show where the bots talk most of the time.
2. **incompetech "Easy Lemon"** (MP3, 2:06, 82 BPM, 5.06 MB, guitar, bass, drum kit, celesta, marimba; "Takes voice-over very well") https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1200076, or **"Thinking Music"** (MP3, 3:16, 6.27 MB, cello, viola, violin, harp; "comedic hard thinking music", good for the vote) https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1600060. Both CC BY 4.0.
3. **OpenGameArt "Crowded Pub"** by Bobjt. https://opengameart.org/content/crowded-pub
   - License: CC0.
   - OGG 1.3 MB (`crowded_pub_2025_1.ogg`), also MP3 684.8 KB. Length not listed. File: https://opengameart.org/sites/default/files/crowded_pub_2025_1.ogg
   - Why it fits: "A short looping tune originally envisioned for a pub. 2025 remix ... adds a drumbeat plus parts B and C to enhance loopability." It should read as a lively theater bar. More CC0 backups: "Ragtime! Jazz" by Tarush Singhal (MP3 4.5 MB, https://opengameart.org/content/ragtime-jazz) and "jazz improvisation looped" by Pro Sensory (MP3 3.2 MB, https://opengameart.org/content/jazz-improvisation-looped, "all my music is public domain").
   - Also on Fab: the same "Cartoon Adventures" pack has "Mischief in the Closet" (sneaky) for a quieter bed.

## 3. Drum roll for the vote

All Freesound, all CC0, all WAV, all checked on their pages.

1. **201211 "Drum Roll Please.wav"** by Scheffler. https://freesound.org/s/201211/
   - 12.3 s, 4.5 MB, 48 kHz 32-bit stereo.
   - Fit: the page description says "Combined a orchestral snare with a Timpani and a crashing cymbal at the end for the, 'Drum roll please...'" The crash lands on the reveal. Trim the front if 12 s is too long for the vote.
2. **77305 "buzz roll.wav"** by bigjoedrummer. https://freesound.org/s/77305/
   - 4.8 s, 821 KB, 44.1 kHz 16-bit stereo.
   - Fit: the page says "Just a short snare drum buzz roll ending in a rimshot." A rimshot is a joke beat.
3. **151819 "Orch 006 cymbal roll.wav"** by Karma-Ron. https://freesound.org/s/151819/ 3.8 s, 1.3 MB, 44.1 kHz 32-bit stereo. A cymbal swell to layer under a roll, not a roll itself. Weak fallback: 191718 "drumroll.wav" (6.0 s, 116 KB, 8-bit 19.9 kHz mono, lo-fi).

## 4. Reveal stingers

All Freesound CC0 WAV unless noted.

**AI reveal ("[PROVIDER]: AI"):**
1. **878609 "Ta-Da Fanfare"** by Qvantor. https://freesound.org/s/878609/ 3.1 s, 864 KB, 48 kHz 24-bit stereo. A theatrical "ta-da" for a reveal.
2. **878602 "Success Vibraphone Triad"** by Qvantor. https://freesound.org/s/878602/ 2.4 s, 681 KB, 48 kHz 24-bit stereo. Gentler and shorter.
3. **175409 "wah wah sad trombone.wav"** by kirbydx. https://freesound.org/s/175409/ 5.2 s, 897 KB, 44.1 kHz 16-bit stereo. Use this one if you want the joke to be the bots' mistake ("the machines realize they voted out one of their own"). Another: 181351 "Fail Jingle (stereo mix)" by unfa, FLAC, 7.1 s, 1.1 MB, https://freesound.org/s/181351/.

**HUMAN reveal ("YOU: HUMAN"):**
1. **879280 "Dramatic Piano Sting"** by Qvantor. https://freesound.org/s/879280/ 5.5 s, 1.5 MB, 48 kHz 24-bit stereo. Dramatic, then the AIs gloat.
2. **578382 "Shock Stab 12"** by nomiqbomi. https://freesound.org/s/578382/ MP3, 3.7 s, 75.9 KB. A hard stab for a gotcha.
3. **578358 "Dissonant Piano Sting 8"** by nomiqbomi. https://freesound.org/s/578358/ MP3, 5.4 s, 110 KB. Or a comic bell for the opposite joke, 538147 "Correct Bell" by Fupicat (WAV, 1.6 s, 275 KB, https://freesound.org/s/538147/).

Same-family fallbacks: **Kenney "Music Jingles"** (85 short jingles, CC0, https://kenney.nl/assets/music-jingles) and the Fab pack above, which has "Ta-Daaa! - Victory fanfare" and "Oops, Banana Peel - Silly mishap" (lengths not listed).

Suggested pair: AI = 878609, HUMAN = 879280. Swap AI for 175409 if you want the sad-trombone joke.

## 5. Applause and laughs (after a cut and at the win)

All Freesound, all CC0, all WAV.

**Cut (laughs, with some applause):**
1. **371562 "Sitcom Laughter with Applause, Small Audience"** by Kinoton. https://freesound.org/s/371562/ 5.8 s, 1.6 MB, 48 kHz 24-bit stereo. A sitcom laugh track with applause at the end, which is the right joke for robot actors. Best single pick.
2. **383207 "Sitcom Laughter 9x, Small Audience"** by Kinoton. https://freesound.org/s/383207/ 43.4 s, 11.9 MB, 48 kHz 24-bit stereo. Nine separate laughs, to slice into variations so it doesn't repeat every cut.
3. **264499 "Crowd Ooohs and Ahhhs in Excitement"** by noah0189. https://freesound.org/s/264499/ 25.8 s, 9.4 MB, 48 kHz 32-bit mono. An "ooh" for the stamp landing.

**Win (applause):**
1. **478411 "Concert audience applause 4"** by thaighaudio. https://freesound.org/s/478411/ 16.4 s, 4.5 MB, 48 kHz 24-bit stereo. Long enough for the win screen.
2. **277022 "Applause 1.WAV"** by Sandermotions. https://freesound.org/s/277022/ 6.6 s, 1.2 MB, 48 kHz 16-bit stereo.
3. **432333 "Medium Crowd Clapping 6"** by jentlemen. https://freesound.org/s/432333/ 6.7 s, 1.1 MB, 44.1 kHz 16-bit stereo.

Another route: Fab "Free Crowd Cheering Sounds" (10 recordings) is CC-BY, so it needs credit. Not recommended when CC0 is available.

## 6. UI clicks

1. **Kenney "Interface Sounds"** (100 files, CC0). https://kenney.nl/assets/interface-sounds Page previews are OGG. Zip size is not shown on the page. I expect clicks, ticks, selects, confirmations, errors and toggles, but I have not seen the file list. Check the names after unzipping.
2. **Kenney "UI Audio"** (50 files, CC0). https://kenney.nl/assets/ui-audio Click and rollover style sounds. A second family if "Interface Sounds" feels too electronic.
3. **Freesound 878245 "UI Bubble Pop"** by Qvantor. https://freesound.org/s/878245/ CC0, 0.24 s, 68 KB, 48 kHz 24-bit stereo. A soft, comic pop. Fab also has free UI packs, such as "Essential UI Sound Effects - 150 Clean Interface SFX (Free)" by Willosuna, but I did not open it.

## 7. Talk blip, one per AI bot, pitched

1. **OpenGameArt "Dialog vocal samples"** by MirceaKitsune. https://opengameart.org/content/dialog-vocal-samples
   - License: CC0 ("Licensed under the Public Domain, crediting is appreciated but not obligatory").
   - `vocal_samples.zip`, 176.7 KB, 32 samples (I did not open the zip, so the audio format is unconfirmed). File: https://opengameart.org/sites/default/files/vocal_samples.zip
   - The page says it is "4 tone sets representing: Standard male, deep male, standard female, light female, demon voice, quick voice, whisper sound, robot beeping", made with eSpeak and Audacity. One blip per letter is how the page says it is meant to be used.
   - Why it fits: four bots need four different voices, and this has eight voice types, including robot beeping and a quick voice. A pitch multiplier then separates them further.
2. **Freesound 468927 "Medium Text Blip"** by malakme. https://freesound.org/s/468927/ CC0, OGG, 8.8 s, 78.7 KB, stereo. Probably several blips in one file, so slice it.
3. **Kenney "Digital Audio"** (60 files, CC0). https://kenney.nl/assets/digital-audio Short synth tones and blips. Pitchable. I have not seen the file list.

## 8. Robot moves, grabs and throws

**Move and look (about a second):**
1. **875419 "MOTRSrvo_Robotic Servo Short Arm Movement"** by harrisonlace. https://freesound.org/s/875419/ CC0 WAV, 1.07 s, 277 KB, 44.1 kHz 24-bit stereo. A short servo for a turn or a hop.
2. **740247 "Servo 9"** by JoontheFloof. https://freesound.org/s/740247/ CC0 WAV, 1.6 s, 277 KB, 16-bit stereo.
3. **729437 "Robot walk, looped"** by Magnesus (https://freesound.org/s/729437/, CC0 FLAC, 1.2 s, 104 KB) and **415566 "mehackit_robot_3.flac"** by hullum (https://freesound.org/s/415566/, CC0 FLAC, 1.2 s, 117 KB).
   - Bigger pools: **Kenney "Sci-fi Sounds"** (70 files, CC0, https://kenney.nl/assets/sci-fi-sounds). **Fab "Core Sci Fi Sounds"** by Neon Audio, 58 WAV files at 44.1 kHz 16-bit, including "Robots (12): servos, movement, mechanical hits" and "Metal Footsteps (10)". Personal tier $0, Professional $4.99, no credit needed. https://www.fab.com/listings/18d121c5-6a73-40e4-8600-164141d8233a

**Grab:**
1. **Kenney "RPG Audio"** (50 files, CC0, https://kenney.nl/assets/rpg-audio) for cloth and leather handling, a soft "got it". I have not seen the file list.
2. **Freesound 643874 "take1.ogg"** by Kneeling. https://freesound.org/s/643874/ CC0, OGG, 0.34 s, 11.9 KB, mono. A very short pick-up.
3. **Freesound 447581 "Pickup Sound"** by Banzai_Bonsai. https://freesound.org/s/447581/ CC0, MP3, 1.2 s, 9.2 KB, mono. A cartoon pickup chirp. Also **Kenney "Impact Sounds"** (130 files, CC0, https://kenney.nl/assets/impact-sounds) for a clunk when a prop meets a metal hand.

**Throw:**
1. **346373 "Throwing / Whip Effect"** by denao270. https://freesound.org/s/346373/ CC0 WAV, 0.33 s, 84 KB, 44.1 kHz 24-bit stereo. A snappy throw.
2. **419341 "Swoosh.ogg"** by WizardOZ (https://freesound.org/s/419341/, CC0 OGG, 1.0 s, 12.7 KB, stereo) or **394873 "Throw 1.mp3"** (https://freesound.org/s/394873/, CC0 MP3, 0.51 s, 12.2 KB, stereo).
3. **OpenGameArt "Swishes Sound Pack"** (13 swishes, WAV, CC0, `swishes.zip` 385.2 KB, https://opengameart.org/content/swishes-sound-pack, https://opengameart.org/sites/default/files/swishes.zip). Or Freesound **463763 "throw swish x12"** by hz37 (https://freesound.org/s/463763/, CC0 WAV, 9.9 s, 2.7 MB, 12 throws to slice).
   - Landing: a Kenney "Impact Sounds" thud.

## Optional extras the design mentions

- Rubber stamp landing: a Kenney "Impact Sounds" thud, under the AI and HUMAN stingers.
- Hook yanking the bot offstage: Freesound 346373 (whip) pitched down, or a Kenney "Impact Sounds" metal hit.
- Costume yanked off: Kenney "RPG Audio" cloth.

## What is not verified

- Nobody has listened to any file. Loop quality, volume and how the comic tone lands are for your ears. I found nothing that clips or sounds unusable from the metadata alone.
- Kenney pack sizes and file names: the pack pages show file counts and the license but not sizes or the list of files. I stopped short of asking Kenney's download endpoint for sizes.
- OpenGameArt track lengths are not listed on the pages.
- Descriptions of what a clip contains come from its page text. Nothing says how clean the tail or loop point is.
- The Fab licenses and prices come from Fab's own listing data today. Free offers on Fab can end, so claim them before relying on them.
- AI audio tools: not used. ElevenLabs terms are quoted above. Suno's free plan is described by several secondary sources as non-commercial only, which I did not confirm at the source. The jam's fal credits can run audio models, but I did not check any model's output license.

## Proposed downloads (waiting for your OK)

Nothing below is downloaded. Sizes are from the pages or headers above.

No login needed:
- OpenGameArt: `vocal_samples.zip` 176.7 KB; `wackyidlings_0.ogg` 166.2 KB; `crowded_pub_2025_1.ogg` 1.3 MB; `swishes.zip` 385.2 KB.
- incompetech (Plan A): `Happy Happy Game Show.mp3` 5.08 MB; `Investigations.mp3` 3.75 MB.
- Kenney zips (size shown when saved): Interface Sounds, Sci-fi Sounds, Impact Sounds, RPG Audio.

You must log in:
- Freesound (about 15 MB in total for the Plan A files, about 27 MB with the optional 383207): 201211 4.5 MB; 77305 0.82 MB; 878609 0.86 MB; 879280 1.5 MB; 371562 1.6 MB; 478411 4.5 MB; 277022 1.2 MB; 875419 0.28 MB; 346373 0.08 MB; 419341 0.01 MB; optional 383207 11.9 MB.
- Fab (your Epic account, add to library): Cartoon Adventures Vol. 1; Core Sci Fi Sounds.
