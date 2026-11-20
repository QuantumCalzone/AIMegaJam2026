# itch.io media

What the itch.io page uploads. Only the cover and the banner are here: T70, which was to add the screenshots, the video and `description.html`, was dropped on 2026-11-15, after the jam ended.

## The cover

![The cover](cover.png)

`cover.png` is the page's cover image at itch.io's size, 630 × 500. `cover_art/cover_full.png` is the same picture at 1129 × 896, for a sharper upload (itch.io takes any size at the 1.26 : 1 shape and scales it down).

It is key art, not a frame from the game: the five robots from the concept art in `Docs/BotArt/` on a red-curtained stage, left to right OpenAI, Meta, You, Anthropic and SpaceXAI. The four AIs squint at the cardboard costume in the middle, which keeps its real eyes peeking out of the slots, its drawn smile and one drop of sweat, under the spotlight. The name is set in the game's display style. My person asked for it on 2026-11-15, as a prep piece for T70, made from the art references committed so far.

### How it was made

1. **The layout:** `swift Docs/ItchMedia/cover_art/layout.swift Docs/BotArt/cast.png Docs/ItchMedia/cover_art/layout.png` cuts the five robots from `cast.png`'s panels and places them on one 1152 × 896 canvas (one of the edit model's own sizes), with soft edges, You in front, the top third clear for the name. The result is a rough collage: `cover_art/layout.png`.
2. **The repaint:** Leonardo's instruction edit (`gemini-2.5-flash-image`, through `Tools/art_gen.py edit`, private) repainted the collage as one scene: one curtain and floor, a spotlight on the costume, a sweat drop. Four takes; take 2 had the cleanest stage. Take 3 told the story better but kept the collage's blurred band, and turned OpenAI's glowing eyes into cartoon eyes. Log: `cover_art/logs/r1_edit.json`.
3. **The eyes:** a second edit of take 2 changed only the four AIs' eyes to a suspicious squint. Two takes; take 1 is the pick, `cover_art/art.png`. Take 2 gave the costume glowing robot eyes, which gives the joke away. Log: `cover_art/logs/r2_edit.json`.
4. **The name:** `swift Docs/ItchMedia/cover_art/title.swift Docs/ItchMedia/cover_art/art.png "<UE_ROOT>/Engine/Content/Slate/Fonts/Roboto-Black.ttf" Docs/ItchMedia/cover_art/cover_full.png 23` crops the art to 1129 × 896 (from x 23, so SpaceXAI's thumb stays in), shades the top with ink, and sets NO HUMANS / ON SET in Roboto Black: `UIStyle`'s Gold (`#F2C14E`, as a light-to-deep gradient) with an 18 px InkSolid (`#161225`) outline and a soft shadow. Roboto is the engine's font (Apache License 2.0, already in `Docs/Assets.md`).
5. **The cover size:** `sips -z 500 630 Docs/ItchMedia/cover_art/cover_full.png --out Docs/ItchMedia/cover.png`. At 315 × 250, the size of itch.io's game grid, the name, the five robots and the costume's sweat drop still read.

- **Cost:** 156 Leonardo API credits (balance 1,902 before, 1,746 after): 104 for the four repaints, 52 for the two eye edits, so 26 credits per edited image. The replies' `apiCreditCost` is empty for this model; the cost is the balance change on `GET /v1/me`. (`Docs/BotArt.md` says these edits reported no cost: the field is empty, but the balance drops.)
- **Leonardo serves JPEG data under a `.png` name.** `art.png` was converted to a real PNG with `sips -s format png`. The other takes are in `Local/art/cover/` (not in git).

### Before it ships

- **Check it against the game.** The cover shows the concept art. T81 to T83 build the game's cast from the same images, so it should match; if the cast on stage ends up looking different, make the cover the old way instead, as a crop of the theater mid-scene.
- **The AI disclosure and the credits name it.** itch.io's Graphics answer and the page's Art credit must say that the cover (and the banner, cut from the same art) was made with Leonardo.ai's edit model from our concept images, which were themselves made with Leonardo.ai.
- **The parody nods are front and centre here.** The provider bots carry light nods to their companies' leaders (`Docs/BotArt.md`, "Rules the build keeps"). Read the jam's Official Rules for anything on real people's likeness before the cover goes up.

## The banner

![The banner](banner.png)

`banner.png` is the page's banner, 960 × 383: 960 px is the width of an itch.io game page's column. It goes in the page's theme editor, under Images > Banner, and replaces the title text at the top of the page. My person asked for it on 2026-11-19.

It is the cover's art (`cover_art/art.png`) cut to a wide strip, the curtain and the five robots' heads, with the name on one line in the cover's style: Roboto Black, the Gold gradient, the ink outline and the soft shadow. The top is shaded with ink like the cover's. The bottom fades into `#161225`, the page's BG 2 in the theme under "Page settings" in [ItchPage.md](../ItchPage.md), so the banner runs into the column with no edge. If BG 2 changes, change `INK` in the script and make the banner again.

Make it from the repo root, with Python 3.10+ and Pillow (`pip install pillow`):

```bash
python Docs/ItchMedia/cover_art/banner.py Docs/ItchMedia/cover_art/art.png "<UE_ROOT>/Engine/Content/Slate/Fonts/Roboto-Black.ttf" Docs/ItchMedia/banner.png
```

The constants at the top of `cover_art/banner.py` set the strip (`CROP_TOP`, `CROP_BOTTOM`, in `art.png`'s pixels) and the name's size and place. Scaled to 375 px wide, a phone's width, the name and the five faces still read. It costs nothing: it uses no image model, only the art already made for the cover. The cover's "Before it ships" notes apply to the banner too.

## T113: the new cover, screenshots and trailer (draft)

**This section is a first draft, written before my person's art updates landed (T114 and the others in T113's Depends on line).** The shot list and the beat sheet get redone after a look at the new art; the tools and the caption style hold either way. Nothing below is shot yet. Since `5f9b77a` (2026-11-19) a costume goes only on roles where it fits the story, and T121 and T122 make new costumes for the 8 roles left bare-headed: pick the shows and scenes to shoot after both are in, so every role on screen is in costume.

### The tools (`tools/`)

Run each from the repo root. They need Python 3.10+, Pillow (`pip install pillow`) and ffmpeg (`winget install Gyan.FFmpeg`, which puts `ffmpeg.exe` and `ffprobe.exe` in `%LOCALAPPDATA%\Microsoft\WinGet\Links`).

| Script | What it does |
|---|---|
| `mcp.py` | A small JSON-RPC client for Unreal MCP, so a session drives its own second editor (`-ModelContextProtocolPort=<port>`) and never the one on port 8000. `Mcp(port).py(path)` runs an editor Python file through the status bar's console box, the only way MCP runs Python here. |
| `winfind.py` | Finds the PIE window of one editor process, by PID, for ffmpeg. Other editors' PIE windows have the same title. |
| `ue_audio.py` | Editor Python: starts and stops a recording of the PIE world's main submix (the game's own sound and nothing else), and writes the wall-clock time of each call. It also sets `au.DisableAppVolume 1` (the engine mutes a window without focus: `UnfocusedVolumeMultiplier=0`) and `DisableAllScreenMessages` (with four editors on the GPU, the engine printed a red "Video memory has been exhausted" note into the shot). |
| `record.py` | Records the PIE window with its sound. See "How to record" below. |
| `cover_title.py` | The cover's name on the PC: a Pillow port of `cover_art/title.swift`, with every size scaled from that script's 896 px frame to the render's height. On `cover_art/art.png` with `--crop-x 23` it matches `cover_art/cover_full.png` to a mean pixel difference of 0.7 (of 255). `--small` writes the 630 × 500 cover, `--grid` a 315 × 250 copy to judge it at itch.io's grid size. |
| `caption.py` | The trailer's captions as transparent 1920 × 1080 PNGs: `hook`, `quote`, `stamp` and `title`. `sheet` draws all four on a frame, and again at 390 px wide, a phone's width. |

### How to record

1. Open a second editor from your checkout on its own MCP port, with no CPU throttle when its window is in the back: `UnrealEditor.exe "<PROJECT>" -ModelContextProtocolPort=8031 -NoLiveCoding -ini:EditorPerProjectUserSettings:[/Script/UnrealEd.EditorPerformanceSettings]:bThrottleCPUWhenNotForeground=False`. Note its PID. Save no asset in it, and kill only that PID when done.
2. `python Docs/ItchMedia/tools/record.py --pid <pid> --port 8031 --name x --setup` sets the PIE window to 1920 × 1080 (the editor's PlayIn settings, through MCP's `ConfigSettingsToolset`: `LevelEditorPlaySettings` isn't exposed to Python). Start PIE in a floating window: `EditorAppToolset.StartPIE` with `playMode` `PlayMode_InEditorFloating`.
3. `python Docs/ItchMedia/tools/record.py --pid <pid> --port 8031 --name <clip> [--seconds N]` records until N seconds pass, or until `Saved/ItchMedia/<clip>.stop` exists. It writes `Saved/ItchMedia/<clip>.video.mkv` (the picture), `<clip>.wav` (the sound), `<clip>.sync.json` (where the sound starts in the picture) and `<clip>.mp4` (both, trimmed to where both run, at a constant 60 fps).

How it works: ffmpeg's `gfxcapture` (Windows Graphics Capture) grabs the PIE window by its HWND, so windows over it don't matter, with no mouse cursor, and crops off Unreal's own window frame (the picture sits at x 3, y 36 inside it). `setpts=RTCTIME` with `-copyts` stamps every frame with the wall clock; `ue_audio.py` writes `time.time()` when the submix recording starts; the difference lines the sound up. Checked on 2026-11-20: a button click's sound landed 7 ms before its picture changed, inside one frame at 60 fps. This PC has no Stereo Mix, and a loopback device would also pick up other sessions' editors.

The 10-second test clip (2026-11-20, the title screen, from a worktree's second editor on port 8031): 1920 × 1080, 60 fps H.264 and 48 kHz stereo AAC, with the title music on it. The game's mix is quiet in the recording (the music at about −42 dB RMS), so the trailer's mix sets its own levels with `loudnorm`.

### The caption style

From the design doc's "Palette and type" (`Docs/Design/ArtInspiration.md`): Roboto (the engine's font, the game's `F_UI`), ink panels `#161225` with old-gold trim `#A9873A`, white text on ink, teal `#3FD0C9` for "you", Gold `#F2C14E` for "act now", curtain red `#C8202F` for the vote and the cut, each bot's name in its seat color. Nothing is set under 56 px at 1080p (11 px on a phone 390 px wide).

- **Hook:** Roboto Black, 104 px, white with an ink outline and a soft shadow, centred; one stretch may take a seat color or teal. Over a busy shot, an ink veil (`--veil 0.5`).
- **Quote:** a chat line, big: an ink panel at the bottom with the old-gold trim, the speaker's seat bar, the name in Roboto Black in its seat color, the line in Roboto Bold 58 px in curly quotes, word for word from the show's `NHOS:` log line. At most two lines. A quote holds the screen at least 2.5 s, plus 0.3 s a word over eight.
- **Stamp:** a tilted curtain-red slab, white Roboto Black, for CUT! (the game's own reveal stamp stays as the game draws it).
- **End card:** the cover's name (gold gradient, ink outline) with "Free on itch.io" under it, over an ink veil.

### The cover (three candidates to shoot)

All three are staged at run time by a script in a Simulate or PIE world (a cine camera spawned in the world, the robots' emotes set through their own functions), so no asset is saved. Each is rendered at 2520 × 2000 or more, then named with `cover_title.py`. The name sits in the top third, so each shot keeps that third quiet.

- **A. The suspects** (the jam cover's idea, in the engine): low and close at the footlights, the box (you) in the centre under a follow spot, its human eyes in the slots; the four AIs turned in on it with `suspicious` faces; shallow depth of field on the box; the gold proscenium and red curtains frame the top.
- **B. The line-up:** square to the stage, the five in a row like a police line-up against the backdrop, the four AIs side-eyeing the box, the box `worried`. It reads at 315 × 250 because it is five clear shapes in a row.
- **C. Over the shoulder:** from behind and above the box, the four AIs facing it and the camera, glaring, the house's boxes and the chandelier behind them; the box's back and its ping-pong ball antenna in the foreground.

Pick the three angles again after a look at the new seats and arms (T114, the OpenAI arms fix). At 315 × 250, each must show five robots, the box and the name.

### The screenshots (five, in page order)

1. `01-mid-scene.png`: the theater mid-scene, all five robots on stage, a prop in someone's hand, a real AI line on screen. The strongest one: most people see only this. Check that the robots read at 640 wide: the house camera frames the stage small.
2. `02-free-talk.png`: Free Talk, an AI accusing the human, its `suspicious` face, its real line in the chat.
3. `03-the-cut.png`: the reveal stamp, "<PROVIDER> IS AN AI", the cut robot gray: the AIs cut one of their own.
4. `04-scene-prep.png`: Scene Prep: the scene card, the director's note clue on my card, the props flying in from the wing (T110).
5. `05-end-screen.png`: the end screen, each AI's vote and its reason in its own words.

Spares: the title with the three ways to play; a prop in flight mid-scene; "YOU ARE THE HUMAN". A GIF of the best moment (a throw, or the stamp) if it fits under itch.io's limit.

### The trailer (beat sheet, about 57 s)

Cut to `S_MusicTitle` (`SourceAssets/Audio/music/t100/01_title.flac`: 126 BPM, 4/4, so a beat is 0.476 s and a bar 1.905 s), with the game's own sounds under it: 30 bars. Every caption that quotes an AI is a real line from a show on Play, word for word; the bracketed lines below are slots, not lines.

| Bars | Time | Picture | Caption |
|---|---|---|---|
| 1–2 | 0:00–0:04 | Black, then a slow push-in on the cast on stage, no UI, the box in the follow spot | "One of these robots is human." then, on bar 2's downbeat, "It's you." in teal |
| 3–4 | 0:04–0:08 | Four close-ups, two beats each: OpenAI, Anthropic, SpaceXAI, Meta, each turning to look | Each name in its seat color as its face lands |
| 5–6 | 0:08–0:11 | The house wide, the stage lights up, the clapperboard SCENE 1 / 4 | "Four AIs. One fake. Every scene, they vote." |
| 7–8 | 0:11–0:15 | Scene Prep: the card, the clue on my card, props flying in from the wing | "They get a secret note. You get a clue." |
| 9–12 | 0:15–0:23 | The loop at speed: a line typed, Action!, the robots act it out, a prop thrown across the stage, faces changing; every wait for a reply cut | "Act it out. Blend in." |
| 13–18 | 0:23–0:34 | Free Talk: three real accusations, two bars each, the speaker's face behind its quote | [quote 1], [quote 2], [quote 3] |
| 19–22 | 0:34–0:42 | The Cut: ballot tickets, the vote, the stamp "<PROVIDER> IS AN AI", the cut robot falls gray; one real reaction line | [the cut robot's reaction] |
| 23–24 | 0:42–0:46 | The other ending, fast: "YOU ARE THE HUMAN", an AI's gloat | [the gloat] |
| 25–26 | 0:46–0:50 | A montage on the beat: props, faces, the box sweating it out | "Survive to the final two." |
| 27–30 | 0:50–0:57 | The end card over the stage; the house applauds | The name, "Free on itch.io" |

The shots with no UI (bars 1–4, 25–26 and the end card's background) come from a run-time camera in the same PIE world; the rest come from the recordings of real shows on Play.
