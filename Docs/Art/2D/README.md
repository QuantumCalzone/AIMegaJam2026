# The 2D art: backdrops, the stagehand and the burning bills (T99)

These are the approved 2D pictures, in T94's direction ([../Direction/README.md](../Direction/README.md)). In 2D the concept and the final image are the same thing: what my person approved is what the game imports. My person approved every image on 2026-11-18. Each file replaces the texture of the same name, so no widget or material changed. Below: the files, every round with my person's words, how the scripts made the final files, and the cost.

![The seven backdrops in a 4 × 2 grid: desert planet, dwarf mine, jungle park, garden wedding, retro diner, bowling lanes, midnight cubicles](backdrops/sheet.png)

![The stagehand, a little gray trash-can droid with one lens eye and a headset on its lid; the clay bill with an Anthropic badge; the charred bill; the four badges O, A, S, M; the eight flame frames and the ember](ui_sheet.png)

## The files

| File | Imported over | Size | What it is |
|---|---|---|---|
| `backdrops/desert_planet.png` | `Stage/Backdrops/T_Backdrop_desert_planet` | 2048 × 1024 | Dusk under two suns, one gold and one coral, a rusty dome hut, a battered space truck on landing legs, a sly-faced moon |
| `backdrops/dwarf_mine.png` | `T_Backdrop_dwarf_mine` | 2048 × 1024 | Carved stone walls lit by candles, stone stairs, a glowing arched mine mouth in the middle |
| `backdrops/jungle_park.png` | `T_Backdrop_jungle_park` | 2048 × 1024 | Palms and ferns, a bare rope fence on posts, a yellow sign with a dinosaur on it, a smoking volcano, giant footprints in the mud |
| `backdrops/garden_wedding.png` | `T_Backdrop_garden_wedding` | 2048 × 1024 | A striped party tent, lanterns on a string, a tiered cake, lemon trees, a pink villa with green shutters |
| `backdrops/retro_diner.png` | `T_Backdrop_retro_diner` | 2048 × 1024 | A counter with red stools, red booths, a checkered floor, night windows onto a lit city and a full moon |
| `backdrops/bowling_lanes.png` | `T_Backdrop_bowling_lanes` | 2048 × 1024 | Honey lanes with red balls and white pins, bold triangle panels in teal and tangerine, a starburst-lit ceiling |
| `backdrops/midnight_cubicles.png` | `T_Backdrop_midnight_cubicles` | 2048 × 1024 | Dim green cubicles under one buzzing light, glowing green screens, a rainy window onto a dark skyline |
| `stagehand/portrait_256.png`, cropped from `stagehand/stagehand.png` (1024 × 1024) | `UI/Stagehand/T_Stagehand_Portrait` | 256 × 256 | The friendly AI stagehand in the earpiece: a little dented trash-can droid with a domed lid, one big lens eye, two small red indicator lights and a black headset over the lid. An old machine that is still friendly to humans. |
| `moneyburn/bill.png` | `UI/MoneyBurn/T_Bill` | 256 × 128 | A sage clay play-money bill: a double border, corner studs, a little robot in the center medallion, "100" pressed into the two rosettes. No real currency's design, portrait or symbol. Transparent outside its rounded corners (2 px margin, as before). |
| `moneyburn/bill_char.png` | `T_BillChar` | 256 × 128 | The same bill charred to ash, with a faint ghost of the relief. Same outline, for the wipe. |
| `moneyburn/flame_sheet.png` | `T_FlameSheet` | 1024 × 128 | The flame flipbook: one row of 8 frames, 128 × 128 each, frame 0 at the left, each flame standing on a base 10 px above its frame's bottom. Chunky clay flames in red, orange and gold with a cream core. |
| `moneyburn/ember.png` | `T_Ember` | 32 × 32 | One orange clay ember (a flame's loose tip), shown at 6 to 10 px |
| `moneyburn/logo_openai.png`, `logo_anthropic.png`, `logo_xai.png`, `logo_meta.png` | `T_Logo_openai`, `_anthropic`, `_xai`, `_meta` | 128 × 128 | The provider badges: a clay disc in the provider's seat color with a raised rim and its initial pressed in, in dark ink #2B1D12, in Roboto Bold. O on #A8CCFF, A on #E8894A, S on #D8F04A, M on #C8AC12. Not the companies' logos (T36's brand rules still hold). Transparent outside the disc. |

`backdrops/sheet.png` and `ui_sheet.png` are pictures for the docs, not for import. `moneyburn/preview.png` is the look check at game size, shown 2×. `rounds/` holds the contact sheets my person picked from (JPEG). The other candidates stayed outside git, in `Local/art/T99/` on the Mac that made them.

**Each badge is its bot's seat color.** Meta's is T108's mustard, #C8AC12. T108 hadn't picked it yet when the badges were made, so my person first chose #B8860B, the darkest of three mustards; when T108 landed with #C8AC12 during the import, my person chose to match it ("Match #C8AC12 (Recommended)"), and the badge was redrawn and reimported. If a seat color changes again, redraw that badge with `scripts/mb.swift` (below) and reimport its texture; it takes seconds and no credits.

## How they were made

All images were made with `Tools/art_gen.py`: `image` is Leonardo `lucid-origin`, `edit` is Leonardo's `gemini-2.5-flash-image`. Every prompt starts with T94's style line. Each log in `*/logs/` has the full prompt, the negative prompt, the generation id and the seed. Leonardo serves JPEG data under a `.png` name, so each pick was converted with `sips -s format png`.

### The backdrops

`scripts/backdrops.py` made four candidates per card at 2048 × 1024, seven generations at once. Each prompt is the style line, the card's scene (from T48's prompts in `Docs/BackdropArt/logs/`, with the thin bridge made thick, the wire fence made rope, and the signs and neon left out), then the composition: the scenery in the upper left, upper right and middle band, the top center calm, the bottom third a plain floor, soft even frontal light with no strong direction, colors a little softer than the actors. The negative prompt adds people, robots, animals, text, signs, curtains, a stage and a frame to the style guide's.

My person picked card by card. I had recommended a set and named each take's problem: lettering (jungle 2's WARNING sign, diner 3's jukebox, diner 4's ROAD DINER, bowling 2), small figures (dwarf 1 and 2, jungle 3, garden 1) or carved monster faces (dwarf 4).

| Card | Generation | Seed | Pick | My recommendation | Notes |
|---|---|---|---|---|---|
| `desert_planet` | `1f1e393b-564d-6d20-acb1-dc66e725d563` | 407903158 | 2 | 2 | |
| `dwarf_mine` | `1f1e393b-553e-6d30-be54-04698981bec2` | 1482392112 | 3 | 3 | Some rubble on the floor, low enough that the robots cover it |
| `jungle_park` | `1f1e393b-7525-6540-bbc6-e91d5f6afd42` | 303557663 | 2, with two edits | 1 | My person: "2, with an edit" (blank the WARNING sign). Edit 1 (`1f1e3a24-64db-61a0-bf68-c3fa3ee0a2d9`, 1 take) removed the sign altogether. My person then asked to "Replace the sign that has a foot symbol on it with a warning for a dinosaur symbol." Edit 2 (`1f1e3a2f-b4d9-69d0-8944-eb576f258530`, 2 takes): take 1, "chunkier dino". |
| `garden_wedding` | `1f1e393b-580c-6990-a519-b301b89004b6` | 969987495 | 2 | 2 | |
| `retro_diner` | `1f1e393b-7375-6330-b15f-1aa442ac0bbf` | 1925215905 | 2 | 3, with an edit | A small toy sits on the right booth |
| `bowling_lanes` | `1f1e393b-549d-6b10-9b26-e5fec9c0d4ef` | 1661808870 | 1 | 4 | |
| `midnight_cubicles` | `1f1e393b-57f1-6be0-a1b0-1fece6e8037c` | 748082591 | 1 | 4 | |

**The jungle edits, pasted back by hand.** The edit model returns 1472 × 704, softer than the 2048 × 1024 source and 4% wider. Stretched back to 2048 × 1024, it lines up with the source, so `scripts/patch.swift` pasted only the changed patch (the fence sign, then the yellow sign) into the full-size source, with a 24 to 28 px feathered edge. The rest of the picture is the original generation.

### The stagehand

It took six rounds to find the stagehand. Each round was four takes at 1024 × 1024, except round 3 (two prompts, two takes each). The sheets are in `rounds/portrait_r1.jpg` to `portrait_r6.jpg`.

| Round | Generation | What it asked | My person's words |
|---|---|---|---|
| 1 | `1f1e393c-640c-6ff0-8c90-96b1e98bfd38` | T61's stagehand redrawn in clay: a round cream head with a dark screen face and rose-pink LED eyes, a beanie and a headset | "Can we change the concept to an older-school, cuter robot, maybe like Wally or something retro? The idea is that the old AI is still friendly to humans." |
| 2 | `1f1e3a3b-84b4-60f0-b8ed-476ec7dc6974` | A 1950s robot with a rounded radio-set head and glowing bulb eyes, worn and patched | "Those are all very creepy." |
| 3 | `1f1e3a40-4c3a-6b70-be60-c5e47e4ee7d1` (dome head), `1f1e3a40-4d20-6350-9aae-ca12a596dcec` (egg head) | Round tin-toy heads, cartoon eyes with no glow, blush cheeks | (They turned into porcelain dolls with noses; I advised skipping them.) "Look to Wall-E or like a Star Wars droid for reference." |
| 4 | `1f1e3a46-2834-6db0-9ccd-172221de10b9` | An original old utility droid: a battered spotlight-like head, a big lens eye with a shutter lid, no face | "Maybe look to concept art from Ralph McQuarrie as inspiration." |
| 5 | `1f1e3a4c-5fc8-6b40-b991-1f1a69d7f215` | His design language described, not named: a smooth retro-futurist shell, one round photoreceptor lens, no face | "Make it not so anthropomorphized. Maybe it just has one eye that's a lens, and then it has other sensors or something, but it definitely still has a headset on top, which is kind of funny. Maybe it kind of resembles a trash can." |
| 6 | `1f1e3a4f-84bb-6990-82fc-e23f96310e5a` | A dented trash-can robot: a ribbed bin, one lens eye, small sensors, the headset worn on the lid; no face, mouth or arms | Take 1. **Approved.** |

The references stayed references: the prompts never named WALL-E, a Star Wars droid or the artist, and asked for an original design, because the game copies no known character's look (T94's style guide). I had recommended round 6's take 4 (a flat lid), because takes 1 to 3 have domed lids; my person chose take 1. Its dome sits on a ribbed gray-green bin with a handle, two red lights and a headset, which keeps it clear of any one droid.

`portrait_256.png` is a 720 × 720 crop of take 1 (from x 165, y 190), scaled to 256 × 256: the whole droid, for the earpiece's 66 px frame inside its rose ring.

### The burning bills

| Image | Generation | Seed | Takes | Pick | My recommendation |
|---|---|---|---|---|---|
| The bill (2048 × 1024) | `1f1e393c-63d4-6d80-8b37-eb8b1b4d1b75` | 1519402606 | 4 | 1 | 1 |
| The flames, a sheet of 8 on black (1920 × 1080, returned 1920 × 1072) | `1f1e393c-636b-6dd0-a0e4-9209fd3ef5e5` | 768288461 | 4 | 2 | 4 (varied shapes) |

Everything else was drawn by `scripts/mb.swift` from those two picks, with no outside art and no more credits:

- **`bill`**: the bill cut from its background (x 264 to 1862, y 148 to 882 in the source). The generated medallion sat about 6 px left of center at game size, where the widget draws the badge, so the script mirrors the bill's left half about the medallion's axis (x 985). It scales the result to 252 × 124 on the 256 × 128 canvas, presses "100" in Roboto Bold (cap height 11 px, ink #2E3A2C with a light lip) into the two rosettes, and masks the rounded corners (radius 7).
- **`char`**: the same bill as ash: #16110F with a little warm brown, plus the bill's own relief at 55% for a ghost of the design. Same alpha.
- **`flames`**: each flame keyed off the dark background by its chroma and brightness, with the background taken back out of its edges, and fitted 104 px tall in its frame. The eight frames alternate the two rows of the sheet, mirror every other frame and vary the height (0.91 to 1.08) and width, so the loop flickers in shape and color. My person picked a sheet of near-identical flames, so this variation is what makes the flicker.
- **The ember**: the first flame's loose tip, the smaller of its two blobs, fitted 24 px inside 32 × 32.
- **`badge`**: a 128 × 128 disc in the seat color, lit from the upper left, with a raised rim and a groove inside it, clay grain from a high-pass of the bill picture's background, and the letter (cap height 60 px) pressed in with a light lip below right.

My person chose seat colors for the badges ("Seat colors (Recommended)"), then Meta's mustard ("5: #B8860B dark mustard (Recommended)"), then approved the set: "Approve all (Recommended)". When T108 set Meta's seat to #C8AC12, my person chose to match it.

To make the money burn files again (Swift on a Mac; the font is the engine's):

```bash
swiftc -O Docs/Art/2D/scripts/mb.swift -o /tmp/mb
```

```bash
/tmp/mb bill <bill pick>.png bill.png "<UE_ROOT>/Engine/Content/Slate/Fonts/Roboto-Bold.ttf" 264 148 985 882 570 520
```

```bash
/tmp/mb char bill.png bill_char.png
```

```bash
/tmp/mb flames <flame pick>.png flame_sheet.png ember.png
```

```bash
/tmp/mb badge <bill pick>.png logo_meta.png "<UE_ROOT>/Engine/Content/Slate/Fonts/Roboto-Bold.ttf" "#C8AC12" M 40 400
```

The other scripts in `scripts/`: `grid.swift` (the contact sheets), `patch.swift` (the feathered paste), `overlay.swift` (the previews), `backdrops.py` and `others.py` (the round 1 calls) and `import_t99.py` (the reimport, run in the editor).

## Cost

**About 890 Leonardo API credits** of the 900 my person OKed before the first call ("Cap 900 (Recommended)"). The replies' `apiCreditCost` is empty for both models, and T96 spent credits on the same account at the same time, so each cost is counted per generation, at the rates T48, T94 and T98 measured: 16.75 a `lucid-origin` image at 2048 × 1024, 16.5 at 1920 × 1080, about 8.75 at 1024 × 1024, and 26 an edited image.

| Group | Generations | Credits |
|---|---|---|
| Backdrops | 7 × 4 images at 2048 × 1024 | 469 |
| Jungle edits | 3 edited images | 78 |
| Stagehand | 6 rounds, 24 images at 1024 × 1024 | 210 |
| Bill | 4 images at 2048 × 1024 | 67 |
| Flames | 4 images at 1920 × 1080 | 66 |
| **Total** | | **890** |

## Lessons for later tasks

- **Glowing eyes read as menacing, and cartoon eyes read as a doll.** For a friendly robot face at small size, no face at all worked: one lens and a silhouette (round 6). Five of six stagehand rounds went to finding that.
- **A negative prompt doesn't stop a nose or a mouth.** Rounds 3 and 5 grew human faces despite "nose, mouth, doll" in the negative. Only a subject with no head-like shape (a trash can) avoided it.
- **"Blank the sign" can come back as "no sign".** The edit model removes more readily than it repaints. Ask for the replacement outright ("replace X with a blank Y") and check.
- **Paste an edit's patch back into the full-size source.** The edit model returns about 1472 × 704 for a 2:1 source. Stretched back, it lines up, and a feathered paste keeps the rest of the picture sharp.
- **A generated layout doesn't keep a widget's anchor.** The bill's medallion came back off center; the badge is drawn at the center. Check generated art against the widget's fixed positions before the pick, or fix it in a script as here.
- **A sprite sheet of "different" flames came back as one flame eight times** in three of four takes. Ask for the variation explicitly, or add it in a script.
