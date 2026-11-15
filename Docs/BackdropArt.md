# Backdrop art

The seven painted backdrops, one per story card (T48). Each card's `backdrop.id` in `Content/NHOS/Data/scenes.json` names its picture, `Docs/BackdropArt/<backdrop id>.png`. In the game each one is the texture `T_Backdrop_<id>` in `Content/NHOS/Stage/Backdrops/`, shown on the backdrop flat by `BP_Backdrop.ShowBackdrop(Id)`.

## How they were made

- **Tool:** Leonardo.ai, model `lucid-origin`, through its paid API (v2 generations, `public: false`), on 2026-11-15. The script called `leonardo()` in `Tools/art_gen.py` once per card: one generation of 4 candidates at 2048 × 1024. The candidates are in `Local/art/backdrops/<id>/` (not in git).
- **Pick:** the best of four, by eye, as T40 does. What counted: clay look, warm color, no lettering, the lower third plain (the robots stand in front of it), and the interest in the upper left and right and the middle band (T49's chandelier covers the top center).
- **Prompt:** the card's `backdrop_prompt` from its `Docs/StoryDrafts/` file, then this suffix:

  > Composition for a theater backdrop seen behind actors: the most interesting scenery sits in the upper left, the upper right and the middle band; the top center is calm and simple; the bottom third is a plain, simple, uncluttered floor or ground with no objects. Warm, glowing color palette like a cozy old opera house stage.

- **Negative prompt:** `text, letters, numbers, logo, watermark, signature, people, characters, person, robot, animals, creatures, hands, photorealistic, glossy plastic, frame, border, blurry`
- **Logs:** `Docs/BackdropArt/logs/<id>.json` has each generation's full prompt, parameters, generation id, seed and the API balance before and after.
- **Format:** Leonardo serves JPEG data under a `.png` name. The picks were converted to real PNG with `sips -s format png`.
- **Cost:** 67 API credits per generation of four (the v2 reply's `apiCreditCost` is empty; the cost is the balance change on `GET /v1/me`). 8 generations, 536 credits. The balance went from 4,211 before the first to 3,514 after the last; the other 161 were someone else's generations on the same key in those minutes (see T48's findings). My person OKed a cap of 550.

## The picks

| Backdrop id | Card | Generation | Seed | Pick | Notes |
|---|---|---|---|---|---|
| `desert_planet` | Who Hid the Plans in the Robot? | `1f1e10bd-0d29-6eb0-9a1d-b07a0e91b5f5` | 938795564 | 1 | Two suns and a cratered moon in the sky, the dome hut left, the space truck right, open sand below. |
| `dwarf_mine` | The Ring Is Mine, I Mean Ours | `1f1e10c7-0f3d-6080-ad84-b79fcfa2973d` | 454881306 | 4 | Rows of stone pillars, a thin stone bridge over a chasm with the orange glow below, a plain floor. The darkest of the seven; candidate 2 is a brighter fallback with a wide arch instead of a thin bridge. |
| `jungle_park` | Dino Island Is Mostly Safe | `1f1e10c7-9c38-6570-9823-f05abdbed64c` | 37730394 | 3 | Palms and ferns at both sides, a sagging rope fence, a tilted warning sign (a question mark, no letters), a puffing volcano over the sea, giant footprints in the mud. |
| `garden_wedding` | The Favor Father | `1f1e10c8-3446-61f0-a2e3-840f80b3bf00` | 1578412946 | 1 | The striped tent and lanterns left, the tiered cake center, the pink villa with green shutters right, lemon trees, clouds, a plain lawn. |
| `retro_diner` | What's in the Glowing Briefcase? | `1f1e10cd-c473-6f70-850d-f7596a7b05ef` | 891500441 | 3 (second try) | Counter with pie domes and red stools left, a glowing jukebox, booths right, a clock, round-cornered windows onto the night. The first try (`1f1e10c8-f2e0-6110-bb78-5e8dac7eb10c`) drew fake lettering on every candidate; the second try's prompt is in the log (stronger clay words, no signs or neon). |
| `bowling_lanes` | League Night, Bathrobe Optional | `1f1e10ca-45cd-6340-a457-e34bf9479f25` | 106524277 | 3 | Teal, tangerine and yellow triangle panels over a row of pins, a ball rack, lanes in forced perspective, plain boards in front. |
| `midnight_cubicles` | Pick a Pill, Any Pill | `1f1e10ca-c996-6ff0-bbaf-5bf4488f99d4` | 1613622251 | 4 | Gray cubicles with glowing green-teal monitors at both sides, a rainy window with a blocky skyline in the middle, one cold ceiling light, a plain floor. |

The interiors (diner, bowling alley, office) read more as a miniature set than as lumpy clay: `lucid-origin` drifts toward a model-photo look indoors even with the clay words first.
