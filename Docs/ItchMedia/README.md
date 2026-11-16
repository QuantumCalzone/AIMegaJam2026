# itch.io media

What the itch.io page uploads. Only the cover is here: T70, which was to add the screenshots, the video and `description.html`, was dropped on 2026-11-15, after the jam ended.

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
- **The AI disclosure and the credits name it.** itch.io's Graphics answer and the page's Art credit must say that the cover was made with Leonardo.ai's edit model from our concept images, which were themselves made with Leonardo.ai.
- **The parody nods are front and centre here.** The provider bots carry light nods to their companies' leaders (`Docs/BotArt.md`, "Rules the build keeps"). Read the jam's Official Rules for anything on real people's likeness before the cover goes up.
