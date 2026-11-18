# The theater, its set pieces and the audience (T98)

These are the approved concepts for the stage and everything around it, in T94's direction ([../Direction/README.md](../Direction/README.md)). T106 builds them in `L_Stage`. My person approved the house view and every piece on 2026-11-18. Below: the house, the pieces with their sizes and how T106 makes each, the surfaces, and every round with its prompt, generation and cost.

![The approved house from the house camera: warm brown walls and boxes with big bright gold scrolls, crimson curtains and a gold-swagged valance, a gold chandelier, the five robots on the plank stage, gold cherubs at the corners, and the clay robot audience in top hats and bowlers in the stalls](house.png)

`house.png` (1344 × 768) is the approved house view: round 4's take 1, with the wire frames the edit drew around the robots removed by hand (`house/delines.swift`). It keeps the house camera's frame: the stage in the middle, the two tiers of boxes at the left and right edges, the chandelier at the top center, the cherubs at the apron's corners and the stalls across the bottom.

**What the house view does not settle,** and what does:

- **The robots are placeholders,** pasted from the old cast sheet `Docs/BotArt/cast.png`. T95 draws the cast.
- **The backdrop** (a soft pink sky) is a placeholder. T99 draws the backdrops.
- **The Riser doesn't show.** Two edits failed to add it in place (rounds 2 and 3). Its piece view sets its look, and it stays at its place (300, −300).
- **The cherubs, the chandelier and the audience** in the house view are older versions. My person changed them in the piece round: the cherubs became robots ("The cherubs should be robot versions"), and the audience got screen faces ("More robot, less baby"). The piece views rule.
- **The front rows are drawn bigger** than in the game. T106 keeps T86's rows, seat pitch and bot scale, which already fill the frame without covering the stage.
- **A few hatless audience heads are dark** in the house view. Every audience bot is one of the five muted colors, as the piece view shows.
- **Only the 16:9 frame was drawn.** T106 checks 1440 × 900 too (the camera keeps its 90° horizontal field of view, so a taller window shows more at the top and bottom).

## The pieces T106 makes

![The 14 piece views on one sheet. Row 1: chandelier, robot cherub on its plinth, wall pilaster, theater box, side curtain. Row 2: valance, Riser, prop table, stalls seat, footlight. Row 3: audience robot front and back, top hat, bowler](pieces/sheet.png)

Each view is in `pieces/views/`: one object, whole, on a plain light gray background, ready for image-to-3D (Meshy or Hyper3D). The views were cut from the sheets in `pieces/` (see the rounds below). Their colors are not all final: T106 colors each piece from the swatches below. The brick-red plinth and pilaster are dark wood, and the chandelier and every trim are the bright gold.

Sizes are in centimeters, width × depth × height, at the scale the piece is placed. "Now" is where the piece is in `L_Stage` today (T17, T49, T86). Triangle budgets follow the style guide: 15,000 for a set piece, 8,000 for a simple one.

| Piece | View | Size (cm) | How T106 makes it | Surfaces | Where |
|---|---|---|---|---|---|
| Chandelier | `chandelier.png` | 180 × 180 × 200 | Model, 15,000 tris. The chain is an engine part (or left out), and the candle flames are small emissive engine parts, as glows are. | Bright gold; cream candles | Hangs at (−500, 0, 411), as now, its bottom above the robots' name labels |
| Robot cherub | `cherub_robot.png` | 65 tall; plinth 55 × 55 × 60 | Model of the cherub alone, 15,000 tris. The plinth is an engine cube. The screen face and LED eyes are engine parts (a dark visor and emissive eyes, like the cast's), not painted. | Bright gold; plinth dark wood; screen #14121C, white LED eyes | The apron's front corners, (−243, ±495), turned 20° toward center, as now |
| Wall pilaster | `wall_pilaster.png` | 100 × 50 × 600 | Model of the scroll capital, 15,000 tris, on an engine shaft. The house view's tall gold S-scrolls up the walls beside the boxes are the same scroll, repeated up the shaft as reliefs. | Dark wood shaft; bright gold capital and scrolls | The side walls between the boxes and the curtains |
| Theater box | `theater_box.png` | 300 × 160 × 190 per tier | Model, 15,000 tris, two tiers a side. | Front and arch dark wood with bright gold mouldings and rail; crimson drapes inside | (−450, ±600), tiers at z 152 and 342, turned 25° toward the house, as now |
| Side curtain | `side_curtain.png` | 250 × 80 × 620 | Model, 15,000 tris, one a side (mirrored). The tie-back is a thick gold band, not a thin rope. | Crimson velvet; bright gold tie-back | Either side of the stage opening, in front of the proscenium columns' line (y ±640) |
| Valance | `valance.png` | 1400 × 60 × 180 | Model, 15,000 tris, in two mirrored halves if one piece is too wide. The thin rope in the middle becomes a thick gold band or goes. In the house view it has gold swag bands: give it those. | Crimson velvet; bright gold bands and tassels | Across the top of the stage opening |
| Riser | `riser.png` | 300 × 150 × 45, step 60 × 30 × 22 | Engine boxes with the swatch materials (no model needed). | Dark wood; bright gold top trim | (300, −300), as now |
| Prop table | `prop_table.png` | 120 across × 80 tall | Model, 8,000 tris. Keep the top's height, so `BP_Prop`'s `Prop1` to `Prop4` still sit on it (T45). | Cream cloth | (300, 300), as now |
| Stalls seat | `stalls_seat.png` | 80 × 70 × 80 | Model, 8,000 tris, placed 46 times on T86's rows (100 cm apart). The back's top stays about where T86's seat backs are (75 above the row floor), so only the bots' domes and hats show above it. | Crimson velvet back and seat; dark wood base; bright gold arm caps | T49's and T86's rows, x −470 to −770 |
| Footlight | `footlight.png` | 35 × 25 × 25 | Model (8,000 tris) or engine shapes: a half shell over a sphere. The bulb's glow is an emissive engine part. | Bright gold hood; cream bulb | Nine along the apron's front edge, as now |
| Audience robot | `audience_bot_front.png`, `audience_bot_back.png` | 160 tall as modeled, placed at 0.37 to 0.43 (about 64) | Model of the body and head, 15,000 tris, in place of `BP_AudienceBot`'s engine shapes. The screen face and LED eyes are engine parts. From row B back, hide what can't be seen from behind, as T86 does. | One of the five audience colors per bot (rose #C98B8B shown; plum #7E5A7A, mustard #C9A43F, brick #A65A3E, lilac #A89BC9); cream belly and ear pods; screen #14121C, white LED eyes | 49 bots, as now: 41 in the stalls, 8 in the boxes |
| Top hat | `top_hat.png` | brim about 1.1 × the robot's head width | Model, 8,000 tris. The audience's own hat, so T104 can delete `Stage/Headpieces/` (the dependency in [../README.md](../README.md)). | House black; band dark red #7A1E22 (not a seat color) | On most audience bots |
| Bowler | `bowler_hat.png` | brim about 1.1 × the robot's head width | Model, 8,000 tris. | House black; band dark red #7A1E22 | On some audience bots (T94's board: three bowlers to three top hats) |

**No antennas, no halo.** The audience has none (T94, rounds 4 and 5), and the generated models get no thin parts: no wires, ropes, fringes or chains. Where a piece needs one, it is an engine part.

## The surfaces

![Six surface swatches: crimson velvet with soft pleats, bright gold with a satin band, dark wood, stage planks, cream and house black, each with faint clay thumbprints](swatches/sheet.png)

Each swatch is in `swatches/` (512 × 512), drawn by `swatches/swatches.swift` from the colors below. They show the color and the clay feel only. Every surface is a **Substrate slab** (one slab, no clear coat, no transmission), matte clay with faint thumbprints in the normal and roughness (as `M_Set`'s `ThumbDepth` or `M_Clay`'s noise), no metal and **no baked light** (`r.AllowStaticLighting=False`; Lumen lights it). Single-color pieces use `M_Clay` instances; generated models with painted detail keep their de-lit base-color texture on `M_Set`.

| Swatch | Albedo | Roughness | Note | Used on |
|---|---|---|---|---|
| `velvet_crimson.png` | #9E1B22 | 0.8 | A soft sheen (Substrate fuzz about 0.3) | Curtains, valance, box drapes, stalls seats |
| `gold_bright.png` | #D9B24E | 0.55 | Gold-painted clay with a satin sheen, no metal. Brighter than the style guide's #C9A04A: my person asked for brighter gold trims on 2026-11-18. | Chandelier, cherubs, scrolls, capitals, rails, trims, tie-backs, footlight hoods |
| `wood_dark.png` | #5A3A22 | 0.8 | The style guide's dark wood. My person asked for walls "darker" than cream, and the house view shows them warm brown. | House walls, box fronts, pilaster shafts, plinths, the Riser, seat bases |
| `stage_planks.png` | #A87E4F | 0.75 | Plank seams and butt joints in the albedo and the normal, as `M_Set` draws them now | The stage floor and the apron's face |
| `cream.png` | #F0E3C4 | 0.85 | | Tablecloth, candles, bulbs, the audience's bellies and ear pods |
| `house_black.png` | #17110F | 0.9 | | Masking, the stalls decks, the hats |

The lights stay T17's and T86's (`FrontWash`, `RimPink`, `RimCyan`, `FootGlow`, `BackdropWash`, `SM_HouseGlow` on lighting channel 1 for rows B to D). T106 retunes them for the darker walls: the stage stays the brightest place in the frame.

## How it was made

All images were made with `Tools/art_gen.py`: `image` is Leonardo `lucid-origin`, `edit` is Leonardo's `gemini-2.5-flash-image`. Each folder holds its takes and its log (`leonardo.json` or `edit.json`) with the full prompt. Leonardo serves JPEG data under a `.png` name, so every take was converted with `sips -s format png`.

### The house

The house camera's frame must stay, so every concept started from the house-camera capture in the design doc (`Docs/Design/images/ArtInspiration/stage.jpg`, 2026-11-15). `house/collage.swift` put it on the edit model's 16:9 canvas (1344 × 768) and pasted the five robots from `Docs/BotArt/cast.png` over the old pill robots, at their places (`house/collage.png`).

| Round | Source | What it asked | My person's words | Generation | Takes | Credits | Result |
|---|---|---|---|---|---|---|---|
| 1 | `house/collage.png` | Repaint as clay, in three treatments: A gold and crimson, B crimson and dark wood, C cream and gold | (the cost: "700 credits") | A `1f1e37c4-5e93-6fc0-83b8-fb8e8d386fd9`, B `1f1e37c4-5ce1-66a0-9fcf-632e17663114`, C `1f1e37c4-5e7e-6030-a2ef-819aecf9691f` | 3 × 2 | 156 | Failed: all six held the old render and barely differed. Not shown. |
| 1b | `house/collage.png`, with `Docs/Art/Direction/board.png` as a style reference (same shape) | The same three, in the board's clay style | | A `1f1e37c6-a3f2-68d0-9580-c00657412a7a`, B `1f1e37c6-a111-63f0-9d57-eda60d4cf233`, C `1f1e37c6-a153-62a0-93b1-00ebfd22128b` | 3 × 1 | 78 | Clay at last. B kept the house camera's frame; A and C took the board's low camera, so their audience covered the stage. |
| 1c | `house/r1b_B/edit_1.png` | Restyle B's walls and boxes: gold columns; cream with gold scrolls | | gold `1f1e37c8-4d5f-63e0-9c3d-95de43c1a5f8`, cream `1f1e37c8-4e3d-6690-b45b-f327f4e1f4ee` | 2 × 1 | 52 | Shown as concepts 1 (B), 2 (gold) and 3 (cream). Pick: "3: cream and gold scrolls" |
| 2 | `house/r1c_cream/edit_1.png` | Remove the red blocks behind the robots, add the Riser, give the dark heads domes | | `1f1e37d6-3abd-69e0-9335-1a6bdee60a86` | 2 | 52 | Failed: the blocks stayed, and the Riser came out as steps in front of the stage |
| — | `house/r1c_cream/edit_1.png` | `house/retouch.swift` filled the red blocks' crimson pixels from the backdrop and floor beside them | | none | | 0 | `house/r1_pick_retouched.png` |
| 3 | `house/r1_pick_retouched.png` | Smooth the patched backdrop, add the Riser, the dark heads | | `1f1e37da-72b0-6e70-a6b0-ac6212f77fc1` | 2 | 52 | Failed: wire frames around the robots and a platform in the middle of the stage. Edits stopped here. |
| 4 | `house/r1_pick_retouched.png` | Walls, columns and box fronts darker; the gold trims brighter | "For the stage, instead of cream color, make it darker and make the gold trims brighter." | `1f1e37f2-0212-61b0-b26c-8463bf90e5df` | 2 | 52 | Take 1, with its wire frames removed by `house/delines.swift`: `house.png`. **Approved:** "Approve" |

### The pieces

The pieces were drawn as sheets of several objects on one plain background (1920 × 1080), then cut into one view each with `sips -c`.

| Round | What | My person's words | Generation | Takes | Credits | Result |
|---|---|---|---|---|---|---|
| S1 | Sheet: chandelier, cherub on a plinth, wall pilaster, theater box (`pieces/s1_ornaments/`) | | `1f1e3821-0fc7-6470-b90c-8a8606c81e0e` | 2 | 33 | Take 2's pilaster and box. Both takes drew the chandelier as a standing candelabra. On the cherub: "The cherubs should be robot versions" |
| S4 | Sheet: the audience robot's front, side and back, a top hat and a bowler (`pieces/s4_audience/`) | | `1f1e3821-0f43-6710-a557-10f1a22c5b17` | 2 | 33 | Take 1's top hat, take 2's bowler. Take 1 had no back view; take 2 had antennas. |
| — | | The balance ran out. My person: "Spend what's left now" (S1 and S4), then topped it up. | | | | |
| Cherub | Edit of S1 take 2's cherub, cropped (`pieces/cherub_robot/source_crop.png`): a robot head with a screen face and ear pods | | `1f1e3833-0c65-6040-bb21-994fc0fe83b2` | 2 | 52 | Take 2 |
| Audience fix | Edit of S4 take 2: remove the antennas | | `1f1e3833-0dc7-6050-8848-983fc6bff340` | 1 | 26 | Two antennas gone, one left, and two front views turned to back views. The last antenna was painted out by `pieces/noantenna.swift`. |
| Chandelier | A hanging chandelier (`pieces/chandelier/`, 1024 × 1024) | | `1f1e3833-0508-6400-b28b-7641b7c825cd` | 2 | 17.5 | Take 2 |
| S2 | Sheet: side curtain, valance, Riser, prop table (`pieces/s2_drapes_stage/`) | | `1f1e3833-04ea-6f40-9cf7-77d580c3439a` | 2 | 33 | Take 2 (take 1's valance has a fringe and its Riser is red) |
| S3 | Sheet: stalls seat, footlight (`pieces/s3_seat_footlight/`) | | `1f1e3833-050f-6930-af89-c18bed66affa` | 1 | 16.5 | Take 1 |
| Audience robot | Edit of the fixed audience sheet: a screen face with LED eyes, a smoother capsule body (`pieces/s4_audience_robot/`) | "What are the little red babies?", then "More robot, less baby (Recommended)" | `1f1e3848-63f2-6730-89d5-0d7fb64757de` | 1 | 26 | The front and back views. **All 14 pieces and the swatches approved:** "Approve all (Recommended)" |

The swatches were drawn by a script and cost nothing.

### Cost

**679 Leonardo API credits** of the 700 my person OKed before the first call: 442 for the house and 237 for the pieces. Each edited image cost 26, as in T94. A `lucid-origin` image cost 16.5 at 1920 × 1080: the S1 and S4 pair took the balance from 120 to 54 with no other generation in between. The batch of the robot cherub, the antenna fix, the chandelier, S2 and S3 took it from 6,509 to 6,364 (145), again with no other generation; the chandelier's 17.5 is what is left of that after the others' known rates. The replies' `apiCreditCost` is empty for both models. The balance is shared with T95 and T97, which ran at the same time, so each cost here is counted per generation, with the account's generation list (`GET /v1/generations/user/<id>`) to tell this task's generations from theirs.

### Lessons for T106 and later tasks

- **An edit of a game capture holds the capture.** Round 1 asked for clay and got the old render back. The board as a second image of the same shape (round 1b) carried the style over, but two of three takes also copied the board's camera. Restyling the one take that kept the frame (round 1c) gave three concepts in the right frame.
- **A collage leaves its seams for the edit to draw.** The cast sheet's curtain behind each pasted robot survived as red blocks, and when those were painted out, their faint outlines came back as wire frames in the next two edits. Cut pasted characters out cleanly before the first repaint.
- **Edits can't place a new object.** Two tries put the Riser on the wrong spot or in front of the stage. Draw a piece that must sit in a set place as its own view.
- **Colors and trims change well by edit** (rounds 1c and 4). Shapes and positions don't.
- **A sheet of four objects at 1920 × 1080 is the cheapest clean view:** 16.5 credits for four objects, cut apart for free. The model mostly keeps the objects apart. It drew "chandelier" as a standing candelabra until the prompt said "hanging" and the negative said "standing candelabra".
