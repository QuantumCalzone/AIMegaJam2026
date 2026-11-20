# The costumes: concepts (T96)

T96 drew a costume for every role in T94's direction ([../Direction/README.md](../Direction/README.md)), and fitted each one to all five approved characters from T95 ([../Cast/README.md](../Cast/README.md)). My person approved the picks on 2026-11-18 and every fit sheet the same day. T104 makes the models from the views here and writes `costumes.json` and `scenes.json` from the role table below.

![The 13 approved costumes, one row of five head shots each, in seat order: OpenAI, Anthropic, SpaceXAI, Meta and You](approved.png)

`approved.png` is the overview: each costume's fit sheet cut to the heads. Each costume's full sheet is `<costume>/fit_sheet.png`.

## The costumes

There are 13 costumes, one per headpiece, shared by the roles that share it today. My person chose "Keep the 13" over adding extras or splitting roles. A costume is its headpiece only. Each role keeps its own color, and the model is one color, tinted per role by `M_Clay` (T47). The concepts are drawn in one of their roles' colors (`color_role` in [prompts.json](prompts.json)).

## What T104 takes from here

**Versions.** Every costume has a round version, which the three round heads and Meta's head share: on Meta it sits over the hair cap, as the fit sheets show. Seven costumes also have a cube version for my robot. The other six sit on the cube's flat lid as they are, so the cube shares the round model. **T104 makes 20 models: 13 round, 7 cube.** Each model still needs its own fit numbers per head (`scale`, `x`, `y`, `z`, `top` in `costumes.json`, with the `on` override per persona), set from the fit sheets.

| Costume (folder) | Round version: OpenAI, Anthropic, SpaceXAI, Meta | Cube version: You | Notes for T104 |
|---|---|---|---|
| hood (`hood`) | `pick.png` | `view_cube.png` | The cube view lost its short cape, so it reads as a square frame. Build the cape as on the round hood (see the cube panel of `fit_sheet.png`). The cape ends at the shoulders, so the seat color shows. |
| dark shades (`dark_shades`) | `pick.png` | shares the round model | Hides Anthropic's and Meta's own glasses (T47's `glasses` tag). On the cube it sits flat across both eye slots, scaled wider. |
| top hat (`top_hat`) | `pick.png` | shares the round model | It sits flat on the lid. Anthropic's light and the ping-pong ball rise out of its top (T47's stalk lift). |
| bob wig (`bob_wig`) | `pick.png` | `view_cube.png` | The cube bob has a flat top and straight square sides that hang from the box's top edges. |
| ball cap (`ball_cap`, also `ball_cap_back`) | `pick.png` | `view_cube.png` | A boxy cap. In the cube panel of the fit sheet the peak points to the side; the view has it forward, which is right. `ball_cap_back` stays the same model turned round. |
| wide-brim hat (`wide_brim_hat`) | `pick.png` | shares the round model | Sits flat on the lid. |
| saucepan helmet (`saucepan_helmet`) | `pick.png` | `view_cube.png` | The cube version is a square pan that fits over the lid. Handle out to the robot's right. |
| wizard hat (`wizard_hat`) | `pick.png` | shares the round model | Sits flat on the lid. The tall hat hid Anthropic's light in the sheet; the stalk lift brings it out. |
| tiara (`tiara`) | `pick.png` | shares the round model | All five fits drew it as a full ring with points round it, more crown than tiara. My person approved it that way. |
| fedora (`fedora`) | `pick.png` | shares the round model | Sits flat on the lid. |
| horned helmet with beard (`horned_helmet_beard`) | `pick.png` | `view_cube.png` (poor, see notes) | **Make the face gap taller** than the fit sheets show, so the beard hangs below every mouth: on SpaceXAI, Meta and the cube the beard covers the mouth, which the design forbids. Two redos failed, and my person approved the sheet with this note. The cube view kept the straw and ball and turned the straps into legs: build the boxy helmet and the beard from the cube panel of `fit_sheet.png`. Two colors (iron gray, ginger) if T104 gives it two material slots; one color otherwise, as T47 did. |
| dino hood (`dino_hood`) | `pick.png` | `view_cube.png` | The face looks out between the jaws. Keep the lower jaw under each mouth (T47 found it hid SpaceXAI's). |
| beanie (`beanie`) | `pick.png` | `view_cube.png` | Short, not a tall sock (T47's weak spot). |

Every view is one object on plain light gray, from a Leonardo generation or edit; nothing in them glows or is see-through.

## The role table

One row per role, in each card's seat order in `Content/NHOS/Data/scenes.json`. The colors are T47's, unchanged. T104 writes `costumes.json` and the seats' `headpiece` and `color` from it.

**Changed on 2026-11-19, after T104:** a costume goes only on roles where it fits the story (my person's call). The hood stays on the ring quest and the space saga, and the shades on the bowling night and the simulation; the slacker trades the hood for the shades, in their near-black. The 8 roles marked "none yet" had nothing that fits: their seats' `headpiece` is empty, so they play bare-headed until T129 draws the costume my person picked for each in T121 (2026-11-20) and T122 makes it. Their colors are kept for those costumes and may change with them.

| Card | Seat | Role | Costume (folder) | Color |
|---|---|---|---|---|
| `space_plans` | 1 | A farm kid | wide-brim hat (`wide_brim_hat`) | #E3C770 |
| `space_plans` | 2 | A masked villain | saucepan helmet (`saucepan_helmet`) | #222226 |
| `space_plans` | 3 | An old desert hermit | hood (`hood`) | #7A5232 |
| `space_plans` | 4 | A smuggler pilot | none yet: aviator cap, picked in T121 (T129, T122) | #1A1A1E |
| `space_plans` | 5 | A rebel princess | tiara (`tiara`) | #D9DEE6 |
| `mine_bridge` | 1 | A barefoot homebody | bob wig (`bob_wig`) | #8B4A26 |
| `mine_bridge` | 2 | A bossy old wizard | wizard hat (`wizard_hat`) | #8C8A86 |
| `mine_bridge` | 3 | A brooding ranger | hood (`hood`) | #5E7A3A |
| `mine_bridge` | 4 | A loud, proud dwarf | horned helmet with beard (`horned_helmet_beard`) | #6B6F75 |
| `mine_bridge` | 5 | A vain elf | tiara (`tiara`) | #C9CED6 |
| `dino_island` | 1 | The billionaire park owner | top hat (`top_hat`) | #F0E6CC |
| `dino_island` | 2 | A dinosaur expert | wide-brim hat (`wide_brim_hat`) | #7A7A3A |
| `dino_island` | 3 | A runaway dinosaur with tiny arms | dino hood (`dino_hood`) | #5DA642 |
| `dino_island` | 4 | A kid on the tour | ball cap (`ball_cap`) | #C8202E |
| `dino_island` | 5 | The park's nervous lawyer | none yet: hard hat, picked in T121 (T129, T122) | #1A1A1E |
| `favor_father` | 1 | The family boss, father of the bride | fedora (`fedora`) | #2A2A2E |
| `favor_father` | 2 | The hot-headed eldest son | ball cap, worn backwards (`ball_cap`) | #E0482E |
| `favor_father` | 3 | The reluctant youngest son | none yet: newsboy cap, picked in T121 (T129, T122) | #6B6B30 |
| `favor_father` | 4 | The family adviser | none yet: bowler hat, picked in T121 (T129, T122) | #1A1A1E |
| `favor_father` | 5 | A washed-up crooner | top hat (`top_hat`) | #8A3FB8 |
| `glowing_briefcase` | 1 | A chatty errand man in a black suit | none yet: pompadour wig, picked in T121 (T129, T122) | #121216 |
| `glowing_briefcase` | 2 | A nosy errand man in a black suit | fedora (`fedora`) | #4A4A4E |
| `glowing_briefcase` | 3 | The boss's bored wife | bob wig (`bob_wig`) | #141416 |
| `glowing_briefcase` | 4 | A runaway boxer who refused to lose | none yet: boxing headgear, picked in T121 (T129, T122) | #B8262A |
| `glowing_briefcase` | 5 | A smooth fixer in a tuxedo | top hat (`top_hat`) | #1C1C20 |
| `league_night` | 1 | A laid-back slacker in a bathrobe | dark shades (`dark_shades`) | #1A1A1E |
| `league_night` | 2 | A hot-headed teammate who knows every rule | saucepan helmet (`saucepan_helmet`) | #6E7438 |
| `league_night` | 3 | A quiet bowler nobody listens to | ball cap (`ball_cap`) | #9CCCEB |
| `league_night` | 4 | A flashy rival bowler | top hat (`top_hat`) | #F0459A |
| `league_night` | 5 | An avant-garde artist | bob wig (`bob_wig`) | #1F4FC8 |
| `pick_a_pill` | 1 | A sleepy office worker | beanie (`beanie`) | #6E7F92 |
| `pick_a_pill` | 2 | A grand leader in a long coat | none yet: round glasses and high collar, picked in T121 (T129, T122) | #6E1E2A |
| `pick_a_pill` | 3 | A rebel in black leather | bob wig (`bob_wig`) | #18181C |
| `pick_a_pill` | 4 | A stern agent in a dark suit | dark shades (`dark_shades`) | #1A1A1E |
| `pick_a_pill` | 5 | A fortune-teller baking cookies | none yet: headscarf, picked in T121 (T129, T122) | #B9A3DE |

## How it was made

- **Candidates:** [gen.py](gen.py) `cand`, one Leonardo `lucid-origin` generation of two images at 1024 × 1024 per costume. The prompt is the style guide's style line, the costume's subject and the style guide's reference ending with "Shown on its own, worn by no one." added ([prompts.json](prompts.json)). The negative prompt is the style guide's, plus head and character words, less "hair" for the wig and beard. Leonardo serves JPEG data under a `.png` name, so every take is converted with `sips`.
- **Picks:** [picks.json](picks.json). `pick.png` in each folder is the picked image, after its fix edit where it had one (`fix/`).
- **Fit sheets:** [fit.py](fit.py) `run`, one `Tools/art_gen.py edit` (`gemini-2.5-flash-image`) per costume and character. The source is the character's panel of the approved lineup, with headroom added for tall hats, on the left of a 614 × 864 canvas, plain gray on the right. The reference is `pick.png` on a canvas of the same shape. The prompts come from [fits.json](fits.json): each head shape's fit, the character's own note where it has one, and what must stay. `fit.py sheet` puts the five left halves side by side in `fit_sheet.png`. Each character's take is `<costume>/fit/<character>/edit_1.png`, and an earlier take is `r<N>_edit_1.png`.
- **Cube views:** an edit on a crop of the cube fit that removes the box character and leaves the piece (`<costume>/view_cube/`). The cap's and the pan's are crops of the gray right half of a fit take, where the edit drew the cube version on its own.
- **Images:** [canvas.swift](canvas.swift) makes the canvases (`pad`, `tile`, `crop`), the fit sheets (`sheet`) and `approved.png` (`grid`). The candidate sheets `sheet_a.png` and `sheet_b.png` were made with T97's `Docs/Art/Props/sheet.swift`.
- [log.json](log.json) holds every call: its generation id, prompt, source and references, files, nominal cost and the balance before and after.

## Rounds

| Step | What was made | My person's words | Result |
|---|---|---|---|
| Costume list | | "Keep the 13 (Recommended)" | 13 costumes, headpiece only |
| Cost | | "Cap 1,200 (Recommended)" | |
| Candidates, round 1 | 2 per costume, 13 generations | | Saucepan: a frying pan and a pot with an upright handle. Dwarf: both had a face. Hood: both full-length cloaks |
| Candidates, round 2 | Saucepan and dwarf redrawn with clearer subjects | | Saucepan take 1 close (handle up). Dwarf round 1 take 1 kept, with the face to be taken out |
| Picks | Sheets `sheet_a.png`, `sheet_b.png` | First "I am worried about how uniform these will fit on each of the characters' heads and faces. In particular, the human character has a cube head, while the other characters have round-shaped heads." Then, after the test fit, "My picks + 3 edits (Recommended)" | hood 2, shades 2, top hat 1, bob wig 1, ball cap 2, wide-brim 1, saucepan 1 (round 2), wizard 1, tiara 2, fedora 1, dwarf round 1 take 1, dino 2, beanie 1 |
| Test fit | The bob wig on all five: `bob_wig/fit_test*` and `fit_test_sheet.png` | "Test the bob wig (Recommended)" | The cube version came out boxy, as asked. Group edits dressed only one or two characters per call (see the lessons) |
| Method and cost | | "All five, cap 2,500 (Recommended)" | One edit per character |
| Fix edits | Hood shortened to the shoulders; saucepan handle turned to the side; dwarf face taken out | (in the picks answer) | All three landed |
| Fit sheets | 13 costumes × 5 characters; the bob wig's cube panel is the test's | | 12 clean. The dwarf's beard covered three mouths, the cube's dino hood was twisted and hid an eye slot, and the cube cap's peak pointed sideways |
| Fit redos | Dwarf on SpaceXAI, Meta and the cube; dino and cap on the cube (`r2_edit_1.png` where not kept) | | Dino fixed. The others got worse (the costume went to the right panel instead), so round 1 was kept; the cap redo's right panel became the cube cap view |
| Cube views | Hood, bob wig, beanie, dwarf, dino | | Wig, beanie, dino good. Hood lost its cape, dwarf poor (see T104 notes) |
| Approval | All 13 fit sheets and the views | "Approve all, beard note (Recommended)" | **approved** |

## Cost

**2,387 Leonardo API credits** (nominal), under the cap my person raised from 1,200 to 2,500 after the test fit.

- 15 `lucid-origin` generations of two images at 1024 × 1024, 17 each: 255.
- 82 edited images at 26 each: 2,132. Of these: 5 for the bob wig test, 3 fix edits, 64 fit takes (13 × 5, less the bob wig's cube panel, which is the test's), 5 fit redos and 5 cube views.
- The replies' `apiCreditCost` is empty, so the cost is counted at the rates the quiet measurements showed (17 per generation, 26 per edit). T99 spent from the same balance at the same time, so the balance before and after in `log.json` often shows more.

## Lessons

- **The edit model dresses one character per call.** Given the five-character lineup it dressed three; four characters, two; a pair, one, every time. One edit per character, on a canvas that holds only that character, dressed every one.
- **A `[character | plain gray]` canvas keeps the framing.** A single tall panel, or a group crop, came back zoomed or reframed. The empty right half also gave a place to ask for the piece on its own, which worked for two of 13 (the square pan and the boxy cap). Usually it drew the round version there.
- **The cube versions follow the prompt for soft pieces, not rigid hats.** Wigs, hoods, beanies, caps, the dino hood and the pan came out boxy. Hats with a crown and brim came out round and simply sat on the flat lid, which reads well, so they share the round model.
- **Things on the head get copied.** In group tries the edit gave SpaceXAI a copy of Anthropic's antenna light. Saying "it has no antenna; do not add one" stopped it.
- **A beard goes over the mouth.** The model kept hanging the beard from just under the eyes. Stronger words ("starts below the grin", "no moustache") made it leave the costume off instead.
- **`sips -c` ignores `--cropOffset`** and crops from the centre. One test edit went to the wrong characters because of it. Crop with `canvas.swift crop`.
- **A wait loop that greps for its own command line never ends** (`pgrep -f` matches the shell running the loop).

## In the game (T104)

T104 made the models from these views and fitted each one to each character. Each version's folder (`<costume>/round/`, `<costume>/cube/`, and `horned_helmet_beard/beard/`) holds its `model.glb`, `thumbnail.png`, `turntable.png` and `log.json` (the Hyper3D generation id, the prompt and the settings). They were imported into `Content/NHOS/Stage/Costumes/<costume>/`; `Content/NHOS/Data/costumes.json` has each one's fit per character.

- [game_fit_grid.png](game_fit_grid.png): every costume on every character, close up, in the game (`costume_test`).
- [game_house_sheet.png](game_house_sheet.png): each costume on all five at the house camera.
- What changed from the fit sheets, and why, is under "Findings" in [Docs/tasks/T104.md](../../tasks/T104.md).
