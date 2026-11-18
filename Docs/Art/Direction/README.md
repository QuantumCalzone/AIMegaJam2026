# The art direction (T94)

This is the one direction that all the new art follows: T95 to T99 draw the concepts, and T103 to T106 make the models. My person approved it on 2026-11-17. Below are the approved board, how it was reached, and the style guide that the later tasks start from. The list of assets they replace is in [../README.md](../README.md).

![The approved direction board: the five robots in clay on the opera stage, a prop table with a milkshake and a toy ray gun, clay robot audience in top and bowler hats, a plum UI panel, a paper card and a speech bubble](board.png)

**The direction: the clay opera house, done better.** It is a stop-motion claymation look. The robots, the theater, the costumes and the props all look hand-sculpted from matte modeling clay, in one grand 19th-century opera house of gold, crimson and cream. Four polished clay bots share the stage with one person in a homemade cardboard costume, and the house is full of small clay robots in hats.

`board.png` (1344 × 768) is round 6's take, approved. It is a direction board, not a layout: the UI scrap only shows that ink panels, paper cards and bubbles sit over the clay world. The UI's real layout is in the design doc's UI section.

## How it was chosen

1. **Three boards of the same scene,** made with `Tools/art_gen.py image` (Leonardo `lucid-origin`, 1920 × 1080 asked, 1920 × 1072 returned, four takes each). The best take of each is in `boards/`, with its log:
   - `A_clay_opera.jpg`: the current clay opera house, done better (generation `1f1e31b8-fe27-6080-bb76-8c81eac210f1`, seed 198590084, take 1).
   - `B_tin_toy_soundstage.jpg`: enamel tin-toy robots on a 1960s live-studio TV soundstage (`1f1e31b9-1b0e-6ef0-9ac9-2fab0dd03666`, seed 347259226, take 1).
   - `C_vinyl_improv_club.jpg`: smooth vinyl art-toy robots in a late-night improv club (`1f1e31b8-fd3c-6a80-9498-fcc1b09a337a`, seed 1225523682, take 1).

   All three mixed up the cast, as `Docs/BotArt.md` warned group shots do. The boards were judged on the look alone. The other nine takes stayed outside git, in `Saved/T94/` of the worktree that made them.
2. **My person's pick:** "A: clay opera house". I had recommended B, for its tie to the theme.
3. **Refinement,** round by round, each with `Tools/art_gen.py edit` (Leonardo's `gemini-2.5-flash-image`) on the round before. Each round's folder in `rounds/` holds its takes and `edit.json`, with the full prompt. `rounds/r0_board.png` is board A converted to a real PNG. Leonardo serves JPEG data under a `.png` name, so every take was converted with `sips -s format png`.

| Round | Source | What it changed | My person's words | Generation | Takes | Credits | Pick |
|---|---|---|---|---|---|---|---|
| 1 | `r0_board.png`, with `Docs/BotArt/cast.png` as a second image | Swap the mixed-up characters for the real cast, and make the human audience into clay robots | "Go: cast + audience" | `1f1e31db-67ed-6c40-9472-b27c1e76b629` | 2 | 52 | none: failed (see the lessons) |
| 1b | `r1b/collage.png` (`rounds/collage.swift`: the five robots cut from `cast.png` and pasted over the board) | Repaint the collage as one clay scene, and make the audience into clay robots | "Go: repaint the collage" | `1f1e31e2-f7b2-6680-b22a-d6888a6b3135` | 2 | 52 | take 2 (take 1 gave OpenAI wings) |
| 2 | `r1b/edit_2.png` | Robot audience in top hats; the prop table with a giant milkshake and a toy ray gun; a speech bubble and a paper card | "Go with take 2" | `1f1e31e8-068c-6570-a3f2-0941ade44ae3` | 2 | 52 | take 1 (fuller house) |
| 3 | `r2/edit_1.png` | Ear pods and antennas so the audience reads as robots; move the bubble over Anthropic | "Round 3 on take 1" | `1f1e31f4-3523-6b70-bdc9-8b7284f02456` | 2 | 52 | take 1 (the hats were lost, and the bubble didn't move) |
| 4 | `r3/edit_1.png` | Antennas off and top hats back; OpenAI without its halo and floor ring | "Robot audience but no antennas", then "Top hats on. And make the OpenAI bot not have a halo or a glow ring below them." | `1f1e31fd-c106-67b0-858a-f3534e94a4a4` | 2 | 52 | take 1 |
| 5 | `r4/edit_1.png` | Remove the last antennas, and add bowler hats | "Remove the remaining antennas. Add some boiler hats." (read as bowler hats) | `1f1e3201-4f2e-6f80-84c3-08d23b2607ae` | 1 | 26 | take 1 (antennas gone, but three top hats dropped and no bowlers added) |
| 6 | `r5/edit_1.png` | Hats only: three bowlers and three top hats | "Round 6, hats only", with the OK to go 10 credits over the cap | `1f1e3203-9f6f-62e0-b4b3-c96d0abff2f3` | 1 | 26 | take 1, **approved**: "Approve round 6" |

**Cost:** 510 Leonardo API credits in all, measured as the change in the balance on `GET /v1/me`, from 1,712 to 1,202. The boards took 198, at 66 per generation of four. Each edited image took 26. My person OKed a cap of 500 before the first call, and 10 more before round 6. The replies' `apiCreditCost` is empty for both models.

### Lessons for the later tasks

- **The edit takes its output shape from a second image of a different shape.** Round 1 passed the 3500 × 1152 cast sheet as a reference. The output came back 1792 × 576 and pasted the cast beside the old characters. Give every image in an edit the same shape, or build a collage first.
- **Collage, then repaint,** is the way to get several set characters into one image (round 1b, as the itch cover did: `Docs/ItchMedia/README.md`). A text prompt can't hold five specified characters. An edit with a reference sheet pastes rather than replaces.
- **Edits drop what they aren't told to keep.** Round 3 removed the hats and round 5 removed three of them, though neither prompt asked for that. Name everything that must stay, and ask for one change per round.
- **Edits are poor at moving things.** The bubble didn't move in two tries. Move a flat element by hand, or leave it.
- **Each pass softens the image a little.** By round 6 the board is visibly softer than round 1b. Six passes is about the limit. For a sharper final, ask for all the fixes in fewer rounds.
- **Change a picked image with `edit`,** never by drawing it again from text (my person's rule).

## The style guide

These are the rules T95 to T99 and T103 to T106 follow. Where the design doc's sections on the bots, costumes, stage or UI disagree with these, the section's own task decides, after my person's OK.

### Palette

The **seat colors are fixed**, because the UI uses them too: each bot's name, chat bar, name tag and ballot ticket match its body (the design doc's UI section, "Palette and type"). Each bot's seat color is its main body color.

| Seat | Body color |
|---|---|
| OpenAI | #A8CCFF pale blue |
| Anthropic | #E8894A orange |
| SpaceXAI | #D8F04A lime |
| Meta | #C8AC12 mustard (its top, with black) |
| You | #3FD0C9 teal (the painted box) |

The **world colors** are albedo targets for the clay materials. The board is a dim, warm-lit house, so its pixels read much darker than these. Pick a material's color from this table, not from the board.

| Role | Albedo | Where |
|---|---|---|
| Crimson velvet | #9E1B22 | curtains, valance, stalls seats, box drapes |
| Old gold | #C9A04A | proscenium, cherubs, rails, chandelier, trims; on the bots only as accents (the round heads' collars, Meta's chain, Anthropic's glasses) |
| Cream | #F0E3C4 | the bots' bellies and ear pods, the audience's heads and ear pods, box fronts |
| Dark wood | #5A3A22 | box walls, the house walls, the Riser |
| Stage planks | #A87E4F | the stage floor |
| House black | #17110F | masking, the stalls decks, the hats |
| Audience bodies | muted rose #C98B8B, plum #7E5A7A, mustard #C9A43F, brick #A65A3E, lilac #A89BC9 | one per audience bot. Muted, so the five seat colors stay the brightest things on stage |
| Screen | #14121C, with white LED eyes (emissive) | the round heads' screens and visors |

- **Keep the seat colors for the five bots.** No set piece, prop or audience bot uses a seat color at full strength. A prop that must be blue or orange is muted or darker.
- **Gold means act now in the UI.** The theater may be gold, but nothing gold lands on the stage floor near the bots, beyond their own small accents.
- SpaceXAI stays lime and never drifts to yellow, so it never reads as gold. Meta's mustard stays green-leaning and darker than the gold, and the audience's mustard (#C9A43F) stays muted beside it.

### Materials and surfaces

- **Matte modeling clay everywhere.** Roughness is high (about 0.7 to 0.9) and there is no metal. The gold is clay painted gold, with a satin sheen and no mirror shine. The velvet is clay with a soft sheen.
- **Faint thumbprints and tool marks belong in the textures** (normal and roughness), never in the silhouette.
- **One shared clay material** (`M_Clay`, as T47 built it), with each instance changing only the color, for anything with a single color: headpieces, simple props, audience bots. Generated models with painted detail keep their base-color texture on `M_CastModel` or `M_Set`.
- **Glow is for few things:** the LED eyes and mouths, the screens, the footlights, the chandelier candles and the backdrop's own light. Nothing else is emissive, glossy or see-through.
- **Substrate materials,** as the project requires: one slab, no clear coat, no transmission.
- **De-lit textures.** A generated model's base-color texture holds no painted shadows, highlights or rim light. Lumen does the lighting.

### Detail at the house camera's distance

- From the house camera at 1600 × 900, a bot is about 125 px tall, its head about 55 px, and a prop 25 to 50 px. This was measured on the house shot in the design doc, at 1920 × 1080, and scaled. Everything must read at those sizes.
- **Outline and two or three colors carry a thing.** A prop is known by its silhouette. A bot is known by its seat color, its body shape and one signature trait (glasses, a chain, spring legs, the box).
- **No detail smaller than about 1/20 of the thing's height:** no small buttons, stitching, fine patterns, writing or tiny gems. If it matters, make it big. If it doesn't, leave it out.
- **Faces:** big LED eyes and a mouth that read on a 55 px head. The mouth always shows under any costume, as `Docs/BotArt.md` rules.
- **Triangle budgets,** as T40 to T42 and T81 used them: up to 15,000 for a bot part, a set piece or a detailed prop, and 8,000 for a simple prop.

### Shapes and proportions

- **Round for the bots, square for me.** The four AIs are soft, rounded, toy-like forms. The player's costume is the one boxy, homemade shape on stage. That contrast is the premise in one picture: keep it.
- **Toy proportions:** a big head, about a third of the bot's height, on a short, chunky body. Every bot is about 1.6 m tall, as now, so the labels, the prop sockets and the bubbles keep their places.
- **The theater is classical but chunky:** thick columns, rounded mouldings, plump cherubs, heavy drapes. Nothing is thin or spindly.
- **The audience:** small clay capsule robots seen mostly from behind. Each has a smooth hairless dome head with two round cream ear pods and **no antenna**, and most wear a black top hat or a bowler. My person decided this in rounds 4 and 5.
- **OpenAI has no halo and no floor ring.** My person decided this in round 4. It stands on the floor like the others.
- **Thick, joined parts.** Image-to-3D breaks thin, loose or overlapping parts. No wires, no hair, no fringes, no thin antennas or rings in a generated model. Where the design needs one (Anthropic's antenna light, my ping-pong antenna), it is an engine part, added in the Blueprint.

### Lighting it assumes

- **Lumen** for global illumination and reflections, with Virtual Shadow Maps and no baked light (`r.AllowStaticLighting=False`).
- **Warm footlights from below,** a soft warm key from the front and above, and pink and cyan rim lights that lift the bots off the backdrop. This is the setup of the existing `FootGlow`, `FrontWash`, `RimPink` and `RimCyan` lights.
- **A dim house:** the stalls and boxes sit darker than the stage, warmed by the chandelier. The stage is the brightest place in the frame.
- **Each painted backdrop is lit by its own wash,** and holds no strong light direction of its own that fights the stage.

### Reference images for image-to-3D (Meshy and Hyper3D)

- **One object per image,** centred, whole and uncropped, in a three-quarter front view.
- **A plain light gray background,** soft even studio light, and no cast shadow on the ground.
- **For characters:** a neutral pose with the arms a little away from the body, and a front, side and back turnaround. Separate images for parts that are built separately (arms, heads), as T81 did.
- **Nothing see-through, glowing or reflective** in a reference. Glows and lenses are engine parts.
- **No text, logos or brand marks.**

### What to avoid

- Anything that reads as **human in the audience**, and **realistic human faces** anywhere. The player's eyes in the box slots are the one human detail.
- **Brand marks, logos, writing, and real people's names or likenesses.** The provider bots carry light parody nods through signature traits only (`Docs/BotArt.md`).
- **Any known character's signature look.** A lime bot with antennas drifts toward a famous phone mascot. Watch for it.
- **Ink outlines, a flat 2D look, photoreal surfaces, glossy plastic, chrome.**
- **Scary, creepy or gory looks.** The tone is chaotic, petty slapstick.
- **Hair, fur, fringes, thin wires, antennas on the audience,** and a halo or ring on OpenAI.
- **Tiny detail** that a model turns to mush, and painted lighting in textures.

### The prompt text that every later generation starts from

Start every Leonardo image prompt with this style line, then describe the subject:

> Stop-motion claymation style: hand-sculpted from matte modeling clay with faint thumbprints, soft rounded chunky forms, bold simple shapes and a clean readable silhouette, saturated slightly chalky colors, from the same world as a gold, crimson and cream 19th-century clay opera house.

For a reference image that goes to image-to-3D, end the prompt with:

> Single object, centered, three-quarter front view, whole object in frame, plain light gray background, soft even studio light, no cast shadow, no text, no logos.

Use this negative prompt, and add the group's own items (for the audience: antennas, hair):

> text, letters, words, logo, watermark, brand mark, realistic human face, hair, fur, thin wires, glossy plastic, chrome, photorealistic, ink outlines, flat 2D illustration, scary, gore, extra characters

For an edit (`Tools/art_gen.py edit`), name the one change and everything that must stay ("Keep everything else exactly as it is: ..."). Give every image the same shape.
