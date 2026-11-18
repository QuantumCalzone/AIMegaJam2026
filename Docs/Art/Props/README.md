# The story props: concepts (T97)

T97 drew the 28 story props in T94's direction ([../Direction/README.md](../Direction/README.md)), four per card, and my person approved every prop and each card's four as a set on 2026-11-18. T105 makes the models from the views here.

![The 28 approved props in seven rows, one per card, each labeled with its size and the spare marked](approved.png)

## What T105 takes from here

Each prop has a folder, `<card id>/<prop id>/`. Its **`model_view.png`** is the clean view for image-to-3D: one object on a plain light gray background, nothing glowing in it. Its size is the **real size in centimeters of its longest side**, which T105 scales the model to. The sizes are those in `Content/NHOS/Data/props.json`, unchanged, and are listed below and on `approved.png`. Where a prop also has a **`concept.png`**, that is the approved look with its glow, and `model_view.png` is the same object with the glow taken out.

| Card | Prop | Size (cm) | Model view | Notes for T105 |
|---|---|---|---|---|
| `space_plans` | tin-can robot | 45 | candidate 1 | Its can is drawn as shiny metal. Make it matte silver-gray clay, as the style guide asks. |
| | glow-stick sword | 70 | candidate 1 | The mint blade glows in the game: an emissive part, not in the model's texture. |
| | toy blaster | 32 | candidate 1 | |
| | piggy bank (spare) | 32 | candidate 1 | |
| `mine_bridge` | cursed ring | 12 | candidate 1 | Old gold, satin, no shine. |
| | glowing staff | 90 | candidate 1 | The white crystal on top glows in the game (emissive part). |
| | water bucket | 35 | candidate 1 | The rope handle is thick enough for image-to-3D; check it survives. |
| | frying pan (spare) | 42 | candidate 1 | |
| `dino_island` | dino egg | 32 | candidate 2 | |
| | meaty drumstick | 32 | candidate 2 | The meat is drawn red; my person kept it. |
| | safety waiver | 30 | candidate 2 | Front-on view. The wavy lines are not writing; keep them big. |
| | dino plush (spare) | 36 | candidate 2 | |
| `favor_father` | plush horse head | 40 | candidate 2 | |
| | cannoli tray | 42 | candidate 1 | |
| | wedding envelope | 26 | candidate 2 | Its wax seal has a small mark that could pass for letters. Leave the seal plain in the texture. |
| | bowl of oranges (spare) | 30 | candidate 2 | The first model of this prop: the old one was an engine sphere. |
| `glowing_briefcase` | glowing briefcase | 45 | `r9_edit/edit_1.png` (round 8 take 1 with the beam taken out) | Lies flat, open wide, lid upright and hinged at the back, handle and latches to the front (`concept.png`). The gold lining glows and a beam of god rays rises out of it in the game: emissive lining plus an engine light shaft, never part of the model. The lid may be its own part, so it can open. |
| | gold pocket watch | 14 | `r2_edit/edit_1.png` (candidate 1, numbers cleared) | No numbers on the face, two thick hands. |
| | giant milkshake | 45 | candidate 2 | The glass is opaque cream clay, not see-through. |
| | giant cheeseburger (spare) | 40 | candidate 2 | |
| `league_night` | rolled-up rug | 80 | candidate 1 | Its diamonds are mustard, which is now Meta's seat color (T95, 2026-11-18; the hex comes in T108). Darken them toward old gold or brown once T108 sets it. |
| | bowling ball | 26 | candidate 1 | |
| | ransom bag | 36 | candidate 1 | The bills' small detail turns to mush; plain green is fine. |
| | milk carton (spare) | 26 | candidate 1 | |
| `pick_a_pill` | red pill | 12 | candidate 2 | Half deep red, half cream. |
| | blue pill | 12 | candidate 2 | Half deep navy blue, half cream (darker than Meta's old blue). |
| | ringing phone | 26 | candidate 1 | Leave the curly cord off the model: it is a thin wire. The ringing is a shake in the game. |
| | bent spoon (spare) | 20 | `r4_bend/bend_30.png` | Round 3 take 1, bent 30° at the neck by `bend_spoon.swift`, as my person's reference showed (a spoon bent just below the bowl). It rests on its bowl with the handle tilted. |

## How it was made

- **Prompts** are in [prompts.json](prompts.json): the style guide's style line, the prop's subject and the style guide's reference ending, with the style guide's negative prompt plus "glow, light rays, see-through glass, transparent, reflections, multiple objects, cropped, hands, table". A prop's earlier subjects are kept there as `subject_round1`, and so on.
- **[gen.py](gen.py)** makes a card's candidates (Leonardo `lucid-origin`, 1024 × 1024, two per prop), converts them to real PNGs (Leonardo serves JPEG data under a `.png` name) and logs each generation in [log.json](log.json). It also builds each card's contact sheet (`<card>/sheet.png`, with [sheet.swift](sheet.swift)) and the approved strips (`<card>/approved.png` and `approved.png`, with [stack.swift](stack.swift)).
- **Edits** used `Tools/art_gen.py edit` (`gemini-2.5-flash-image`). Each edit folder holds its `edit.json`, with the full prompt and generation id.
- **The spoon's bend** was made with [bend_spoon.swift](bend_spoon.swift), no generation: it cuts the handle at the neck, rotates it about the neck's centre, paints the background back in, and rounds the joint.
- In a prop folder, `candidate_N.png` is the last round's take. An earlier round's takes are `r<round>_candidate_N.png`. `picks.json` has every pick and my person's words.

## Rounds

My person picked one card at a time from its contact sheet, each card as a set.

| Card | Round | What was made | My person's words | Pick |
|---|---|---|---|---|
| `space_plans` | 1 | 2 candidates each | "1 for all" | 1, 1, 1, 1 |
| `mine_bridge` | 1 | 2 candidates each | "All 1" | 1, 1, 1, 1 |
| `dino_island` | 1 | 2 candidates each | "All 2" | 2, 2, 2, 2 |
| `favor_father` | 1 | 2 candidates each | "All 2 except cannoli should be 1" | 2, 1, 2, 2 |
| `glowing_briefcase` | 1 | 2 candidates each | Briefcase: "The brief case should be on it's side, be open, and be glowing god rays out." | the other three held |
| | 2 | Briefcase redrawn: lying on its side, open, god rays | "2 needs to be more like a briefcase. So flatter but wide. Think of a lawyers case in NY" | none |
| | 3 | Edit on round 2 take 2 (2 takes): slim lawyer's case | "Reduce the height of the case." | none: still deep |
| | 4 | Edit on round 3 take 1: half as deep | none (it came out deeper) | none |
| | 5 | Briefcase redrawn from text: slim attaché case | "Do 2 but have the case's lid slightly open" | take 2 |
| | 6 | Edit on round 5 take 2: lid slightly open | "The brief case is hinging on the wrong side." | none |
| | 6 | Edit on watch candidate 1: numbers cleared | "Raise the cap to 700 (Recommended)" (the cap question named this edit) | the edit |
| | 7 | Edit on round 5 take 2: hinged at the back | none (the lid floated and the handle was doubled) | none |
| | 8 | Briefcase redrawn from text after my person's reference (a stock photo of an open attaché case, described in words, never uploaded) | "Take 1, approve card 5" | take 1; watch edit, milkshake 2, burger 2 |
| | 9 | Edit on round 8 take 1: beam and glow taken out, for the model view | approved with take 1 | the edit |
| `league_night` | 1 | 2 candidates each | "All 1 (Recommended)" | 1, 1, 1, 1 |
| `pick_a_pill` | 1 | 2 candidates each | "Pills 2, phone 1, redo the spoon (Recommended)" | 2, 2, 1, spoon held |
| | 2 | Spoon redrawn with a stronger bend | "The spoon should be bent like this", with a reference sticker of a spoon bent at the neck | none: neither bent |
| | 3 | Spoon redrawn to the reference | none (both straight) | none |
| | 4 | Round 3 take 1 bent by hand, at 30° and 40° | "30°, approve card 7 (Recommended)" | 30° |

The edit logs of rounds 3, 6 and 7 name `candidate_2.png` as their source: at the time that was round 2's take 2 (now `r2_candidate_2.png`) and round 5's take 2 (now `r5_candidate_2.png`).

## Cost

**743 Leonardo API credits**, against the cap my person OKed: 600 before the first call, raised to 700 for the briefcase and watch edits, and the last spoon redraw and the briefcase's model-view edit, which my person chose with their cost named.

- 33 generations of two `lucid-origin` images at 1024 × 1024, 17 credits each (8.5 an image): 561 credits. The replies' `apiCreditCost` is empty, so the cost is the change in the balance on `GET /v1/me` around each call. Four entries in `log.json` show more (43, 69, 69, and a gap between calls) because T95 and T98 spent from the same balance in the same minutes. Every quiet measurement was 17.
- 7 edited images at 26 credits each: 182 credits (round 3 made two).
- The balance ran out once, at 54, after card 4. My person topped it up, and the cards went on.
