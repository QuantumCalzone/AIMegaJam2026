# The cast (T95)

The concept art for the five characters in T94's clay opera house direction: the four AI robots and my robot, a person in a cardboard costume. My person approved each character, the lineup and the turnarounds on 2026-11-18. T96 fits the costumes to these heads, and T103 builds the models from the turnarounds. The style guide they follow is [../Direction/README.md](../Direction/README.md).

![The approved cast in seat order: OpenAI, Anthropic, SpaceXAI, Meta and You, on one clay opera stage](lineup.png)

## What is where

Each character's folder holds:

- `approved.png`: the approved concept.
- `turnaround.png`: the approved front and side views on plain gray, for Meshy and Hyper3D. `side.png` is its right half (672 × 768). `front.png` is not its left half: it is a 672 × 768 cut from the middle of the canvas, with the front view half cut off, so crop the front view from `turnaround.png` (x 0 to 671) instead, as T103's prep did.
- `r1/`, `r2/` ...: every round, with its takes and its log (`leonardo.json` for a text generation, `edit.json` for an edit, each with the full prompt). `turn/` (and Meta's `turn2/`) hold the turnaround edits and `canvas.png`, the input each was drawn from.

`lineup.png` is `lineup/collage_v3.png`. The scripts, run from the repo root, are `sheet.swift` (the side-by-side review sheets, which were not kept), `recolor.swift` (SpaceXAI's free hue shift), `lineup.swift` (the lineup collage) and `turn_canvas.swift` (the turnaround input). Leonardo serves JPEG data under a `.png` name, so every take was converted with `sips -s format png`.

| Seat | Concept | Turnaround | The look |
|---|---|---|---|
| OpenAI | `openai/r2/edit_1.png` | `openai/turn/edit_1.png` | A pale sky blue round head with a dark screen face, cream ear pods and a gold collar; a short teardrop body on stubby feet in a gray knit sweater; hands pressed together. No halo, no ring. |
| Anthropic | `anthropic/r1/candidate_3.png` | `anthropic/turn/edit_2.png` | An orange round head with circular gold glasses on the screen and an amber light on a short stalk; a round body with a cream belly and three buttons; one finger raised. |
| SpaceXAI | `spacexai/r3/recolor_a.png` | `spacexai/turn/edit_1.png` | A lime round head with a dark visor, a cocked brow, a long cream nose and a toothy grin; a round body with a cream belly and a lime lightning bolt; steel coil-spring neck, arms and legs; dark boots; a double thumbs-up. |
| Meta | `meta/r5/edit_1.png` | `meta/turn2/edit_1.png` | An android with pale silver skin, a grown-up head with thin, flat, slicked-back black hair (one solid cap), pale yellow eyes with black pupils, thick black smart glasses with a camera lens and a recording light, a black and mustard-gold top, black pants, silver shoes and a gold link chain. |
| You | `you/r2/edit_2.png` | `you/turn/edit_1.png` | A person in a teal cardboard box costume: a cube head with two eye slots (human eyes peek through), a smile drawn in marker and a ping-pong ball on a straw; a box body with a duct-tape band and bottle-cap buttons; red and cream striped sleeves, the red and cream scarf, tan garden gloves with brown cuffs, jeans and sneakers. |

## The rounds

All text generations are Leonardo `lucid-origin`, 864 × 1152, four takes. All edits are `Tools/art_gen.py edit` (`gemini-2.5-flash-image`), which keeps the source's size (864 × 1184 from an 864 × 1152 source). The round 1 prompt for each character is T94's style line, the character, and a shared ending (toy proportions, a bare smooth head top, the wooden stage and a blurred crimson curtain, full body, three-quarter front view), with T94's negative prompt plus "multiple characters, cropped, halo, glowing ring".

| Round | Character | What it did | My person's words | Generation | Takes | Credits | Pick |
|---|---|---|---|---|---|---|---|
| 1 | OpenAI | Four candidates from text | "3" | `1f1e37b9-5bab-65c0-9c52-910f52828405` (seed 79243207) | 4 | 32 | 3 (the clearest smile) |
| 1 | Anthropic | Four candidates from text | "3", then "Approve as it is" | `1f1e37b9-5d43-6130-be61-31b17f646a8c` (seed 600644331) | 4 | 32 | 3, **approved** |
| 1 | SpaceXAI | Four candidates from text | "3" | `1f1e37b9-5d54-62a0-847e-d55dc184f28a` (seed 486234096) | 4 | 32 | 3 (no antenna) |
| 1 | Meta | Four candidates from text | "1", then "Approve as it is" | `1f1e37b9-5b51-6070-8cf6-635e018faee9` (seed 1243111220) | 4 | 32 | 1 (later redesigned, below) |
| 1 | You | Four candidates from text | "3" | `1f1e37b9-5d19-6920-b271-18aa19ce0366` (seed 238532518) | 4 | 32 | 3 |
| 2 | OpenAI | Gray-mint to pale sky blue #A8CCFF | "Approve take 1" | `1f1e37bf-d206-6fc0-b035-df8c69a879c2` | 2 | 52 | take 1, **approved** |
| 2 | SpaceXAI | Olive to lime #D8F04A | "Free hue shift" | `1f1e37bf-d899-61d0-a672-b6498fd372d5` | 2 | 52 | take 1 (barely moved) |
| 2 | You | Teal hands to tan garden gloves | "Approve take 2" | `1f1e37bf-d0e6-6e60-9500-f876f39bd1a0` | 2 | 52 | take 2, **approved** |
| 3 | SpaceXAI | Local hue shift of round 2's take 1 (`recolor.swift`): band 75 ± 21°, saturation over 0.2, to hue 72, saturation 0.75, value × 1.2 (A); B to hue 76, value × 1.3 | "Approve A" | none, made on the Mac | 2 | 0 | A, **approved** |
| Lineup | all | Collage of the five at one height (`lineup.swift`), repainted as one scene | "Approve collage v2" | `1f1e37d5-34ba-66c0-bd74-717d8cd7e565` (on `collage_v1.png`) | 2 | 52 | neither repaint: both kept the collage's seams, and take 2 dropped a thumbs-up. The free `collage_v2.png` was approved |
| Turn | Meta, You | Front and side views on gray from `canvas.png`: no glow, a blank screen, no antenna light, no ping-pong ball | | `1f1e3822-4eb4-6c90-90d3-e91bf3eba8cf`, `1f1e3822-4e3d-6280-9f0d-f09ed86fbf4d` | 1 + 1 | 52 | You's, **approved**. OpenAI's, Anthropic's and SpaceXAI's failed: the balance ran out (no charge) |
| Turn | OpenAI, Anthropic, SpaceXAI | The same, after the top-up | "Approve all" | `1f1e382f-f256-6350-b7b7-589c2c03d77a`, `1f1e382f-f234-6070-b890-08c47480d4b1`, `1f1e382f-f173-6280-ae81-c9d2ccd8a2cd` | 2 + 2 + 2 | 156 | OpenAI 1, Anthropic 2 (kept the glasses), SpaceXAI 1 (take 2 grew a bead necklace), **approved** |
| Turn | Meta | Add the chain the front view lost | | `1f1e382f-f113-6f10-a03c-cafcd3e55879` | 1 | 26 | superseded |
| 2 | Meta | Skin to pale gold (concept, and the turnaround to match) | "Make the meta character have skin like Data from The Next Generation. Also have his color scene the same star fleet outfit Data wore.", then "Skin only" | `1f1e3836-d950-6660-86e5-c22ea69a25c0`, `1f1e3836-c93c-6300-9827-ca31dbd82756` | 2 + 2 | 104 | "Change something" |
| 3 | Meta | Six changes in one edit: pale yellow-gold skin, a less baby-like head, a black and mustard top, black pants, a pure gold chain, smart glasses with a camera lens and a recording light | "His skin should be a pale yellow-gold. The pants should be black; the shirt should be black & gold (or mustard). The chain around the neck should be pure gold. The glasses should be like the Meta glasses and have a light on it the indicates it's recording. I'd like the head shape to be less baby-like." | `1f1e3846-29ef-6990-b195-132b36a25f59` | 2 | 52 | take 2 (take 1 kept the bead chain) |
| 4 | Meta | Skin to pale silver | "Change the skin to pale and silver" | `1f1e384a-bfa6-6ca0-aa04-a85929e70421` | 2 | 52 | take 2 (both also turned the shoes silver) |
| 5 | Meta | Yellow eyes with dead black pupils, thin flat black hair | "Change the eyes to be yellow with dead black pupils. Like Data. And add thin flat black hair." | `1f1e384e-ea67-62b0-b2bb-002c87a7b175` | 2 | 52 | take 1, **approved** ("Approve take 1") |
| Turn | Meta | The new Meta's front and side views | "Approve all" | `1f1e3854-81de-63f0-baea-7b346630bd5a` | 1 | 26 | **approved** |
| Lineup | all | `collage_v3.png`: the v2 collage rebuilt with the new Meta | "Approve all" | none, made on the Mac | 1 | 0 | **approved** |

**Cost: 888 Leonardo API credits.** Round 1 measured 160 (the balance on `GET /v1/me`, 1,202 to 1,042; 32 per four-take generation at 864 × 1152) and round 2 measured 156 (to 886, 26 per edited image). After that the balance can't be measured per task, because T97 and T98 spent from the same balance at the same time, so the rest is counted at 26 per edited image. My person OKed a cap of 800 before the first call, and raised it to 900 for Meta's redesign. The replies' `apiCreditCost` is empty for both models.

## Decisions my person made

- **The cube head stays.** I asked whether wigs need a round head for my robot; my person chose to keep the cube, so T96 draws a cube version of each headpiece.
- **Meta's seat color becomes mustard.** With the black and mustard top there is no blue left on Meta, and my person chose "Black & mustard, seat goes mustard" over keeping the seat blue. The UI's seat color for Meta has to change to match (see "For later tasks").
- **Meta nods to Data.** My person asked for Data's look from *Star Trek: The Next Generation*. I recommended a nod in the seat blue, warned that the style guide rules out a known character's signature look, and kept every badge and insignia out of the prompts. My person chose the pale skin, the yellow eyes, the slicked black hair and the black and mustard top.

## For later tasks

- **Meta's seat color (not done in T95).** The game still colors Meta's name tag, chat bar and ballot ticket #5B8CFF blue: `UIStyle.SeatColor` (`Graphs/UIStyle/SeatColor.txt`, an editor asset), the UI section's palette line in `Docs/Design/ArtInspiration.md`, and the palette in T94's style guide. The bots section now says mustard. Mustard sits close to the UI's gold "act now" color (#C9A04A) and to the audience's mustard body (#C9A43F, T98), and nearer Anthropic's orange than blue did. Whoever changes the UI picks the exact hex with my person.
- **Image-to-3D, T103:** the turnarounds leave out what the style guide makes engine parts: the round heads' face (the screens are blank, because T75's eyes, brows and mouth are engine parts), Anthropic's antenna and amber light, and my ping-pong ball and straw. Meta's eyes don't glow in its turnaround, and its recording light is a plain dot, to become an emissive engine part.
- **Glasses are separate parts.** T47's shades hide Anthropic's and Meta's own glasses (the `glasses` tag), so a model with the glasses baked in can't take the shades. Build them as their own part, or cut them from the model.
- **Meta's hair is one solid clay cap,** not strands, so wigs and hats sit over it and image-to-3D can build it. T96 fits every headpiece over it, as it does over the cube.
- **OpenAI stands on its feet** now. It no longer hovers over a ring, so T103 drops the hover and the ring.

## Lessons

- **The edit model resists a color change.** It moved SpaceXAI's olive only a little toward lime. A local hue shift (`recolor.swift`) did it exactly, for free, and with no softening.
- **A recolor edit spills into nearby parts.** Meta's silver skin edit also turned the cream shoes silver. Name every part that must keep its color.
- **A repaint keeps a collage's seams.** Both lineup repaints kept the panel edges in the curtain. Stretching each panel's top strip of curtain upward (`lineup.swift`) and blending the panels gave a seamless lineup with no generation, and with no drift in any character.
- **Several changes in one edit work** when they are numbered and the prompt names everything to keep (Meta round 3: all six changes landed in take 2). That is one softening pass instead of six.
- **The Leonardo balance is shared.** T95, T97 and T98 ran at once on caps of 800, 600 and 700, against 1,202 credits. The balance ran out mid-run: a failed call costs nothing, but the run stops. Check the balance against every running task's cap before a batch.
- **A turnaround from a 16:9 canvas** (the concept on the left half, gray on the right) gives a matched front and side view in one edit, at one image's price.

## The models (T103)

Each character's parts are in `<character>/<part>/` (`head`, `body`, `arm`, and Meta's `glasses`): the Hyper3D Rodin model (`model.glb`), its textures, the crops sent to Rodin, a thumbnail, a turntable, `mesh_stats.json` and `log.json` (tool, settings, prompt, generation id, the dropped tries and the credits). My person approved all five on `models_sheet.png` on 2026-11-18; `models_parts.png` turns every part. [T103-build.md](../../tasks/T103-build.md) has each part's notes and suggested fit, and [T103.md](../../tasks/T103.md) the fits as built and what T104 needs to know about each head. In the game they are `Content/NHOS/Stage/Cast/<character>/SM_<Character>_<Part>`, each on its `MI_<Character>_<Part>` (a `M_CastModel` instance).
