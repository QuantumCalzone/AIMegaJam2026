# T47 build sheet: a headpiece for each role

Back to [T47](T47.md) and [the plan](../Plan.md). A Mac prep session wrote this on 2026-11-15 for T46's capsule head, and a second Mac prep session refreshed it the same day for the new cast (T79 and T80). Both worked without the editor. It is a plan, not a record: nothing in `Content/`, `Tools/`, `Config/` or `Graphs/` changed, and the design doc was read, not changed (Stories tab rev 9, Art Inspiration rev 29).

**Refreshed against `noHumansOnSet` at `7e973bd`.** There, T44 (the seven cards), T45 (each card's props, `props.json`) and T57 (`SetPassed`) are done; [T79-build.md](T79-build.md) and [T80-build.md](T80-build.md) are pushed; **T79 is being built on the Mac and has not pushed**, and T80 is not built. So every `BP_Robot` number below that comes from T79 or T80 comes from their sheets, not from their pushed graphs.

## What this refresh changed, and why

- **The headpiece hangs on `HeadSocket`, not `Rig`** (T79 adds the socket on every head; T80 places and scales it on Meta's and my heads). `MakeHat` attaches the `Hat` to it, so one fit per headpiece serves all five heads.
- **Every fit is measured from `HeadSocket`** (on the round head, at z 158 in `Rig`), not from `Rig`: each old `z` minus 158, before the re-fit below.
- **Each of the 13 headpieces was fitted again to T79's round head** (an oval 70 wide, 66 deep, 62 tall, top at z 158, with its screen, eyes and mouth about 20 cm higher than on T46's pill: eyes at z 135, not 114 to 116). The hats that sit on the crown keep their numbers (the crown didn't move). The pieces that come down the front were raised off the eyes (`ball_cap`, `beanie`, `tiara`, `saucepan_helmet`) or raised with the face (`dark_shades`, `horned_helmet_beard`). The table in 1a has each one; 10 of the 14 ids are on the list to look at first in the editor (part 5c).
- **`lift` became `top`**, the headpiece's top above `HeadSocket`. `SetHeadpiece` works out the lift from the socket's own place and scale, so the toppers clear a hat on every head (on T80's box, `lift` would have left my ping-pong ball 5 cm low: T80-build part 7, item 4).
- **A `y` field,** for the saucepan: its bounding box includes the handle, so its pivot is off the pot's center by about 18 cm sideways.
- **An optional `on` field per headpiece** (`{persona: {scale, x, y, z, top}}`), so a head the socket alone doesn't fit (T80's Meta or my box) can be fixed with a number. Empty by default.
- **The shades hide the robot's own glasses:** T79 tags Anthropic's glasses `glasses`, T80 tags Meta's the same; a new `ShowGlasses` hides them while the `dark_shades` are on.
- **The data part was checked against `scenes.json` and `props.json` as T44 and T45 pushed them** (the first sheet used drafts): every card id and role matches, `make_costumes.py` writes exactly 36 lines into today's `scenes.json`, and `check_prompts.py --offline` with the new check passes on the result. T45 made every prop a hand prop (`wear: hand`), so no prop lands on `HeadSocket` under a hat.
- **The DSL follows T45's pushed forms:** the cast is the multi-exec `Utilities|Casting|CastToStaticMesh` with `:then` and `:CastFailed`, and `Json|HasField` takes a string (`BP_Prop.SetProp`).
- **Part 0 now checks T79's and T80's pushed graphs** instead of T46's head, and Decisions 4, 5, 9, 13 to 18 are new or changed.

## What T47 must re-check against the pushed `Graphs/BP_Robot/` files

T79 is being built as this is written and may differ from its sheet. Before part 2, read T79's and T80's pushed files (`SetPersona`, `Receive`, `ResetLook`, `SetCut`, `SetLit`, `EventGraph`) and their tasks' "Findings", and check:

1. **`HeadSocket` exists and is a variable** on `Rig` (T79 part 2b), as `(V HeadSocket)` or `(Variables|Default|GetHeadSocket)` in their sources. If T79 named it differently, use that name in `MakeHat` and `SetHeadpiece`.
2. **Its place and scale per persona** in `SetPersona`: (0, 0, 158), scale 1 on the round head; Meta and my box per T80's "Findings" (T80's starting values: Meta (0, 0, 158) at 0.9, my box (−6, 0, 163) at 1). Every fit assumes the round head's socket sits on its top at (0, 0, 158), scale 1. If T79 put it elsewhere, set `HEAD_TOP` in `make_costumes.py` to the socket's z (and fold any x into the fits) and run the script again. If T79 moved or reshaped the **head** itself, re-fit the pieces in 1a against the new numbers and say so in the Findings.
3. **The face:** the eyes at z 135, the screen's top about 147, the mouth at 123 (T79 part 2b, 2c). T79 may tune the `Face` or `Visor`. If the eyes moved, move `dark_shades`' and `horned_helmet_beard`'s `bottom` in `make_costumes.py` by the same amount, and check the pieces raised off the eyes still clear them.
4. **The stalk:** `Nub` still at (0, 0, 168), 24 cm tall, and every topper an `acc` part at z 165 or more (T79 adds none there; T80 adds `Wire` and `PingPong` there). `SetHeadpiece`'s lift reads `Nub`'s place (its base at z 156) as every robot's stalk base. T80's `Wire` starts at the lid (z 158), so on my box the ping-pong ball ends 2 cm higher over a hat than the round bots' toppers, which is fine; if T80 moved the wire or `Nub`, check my ball over a tall hat by eye.
5. **The `glasses` tag** on Anthropic's rims, lenses, bridge and temples (T79 part 2e) and on Meta's glasses (T80 part 2b), each also tagged `acc` and its persona. `ShowGlasses` needs both tags.
6. **Nothing else loops every static mesh's visibility** in a way that would hide or show the `Hat` (it has no tag): T79's `acc`, `seat` and `ring` loops skip untagged parts.
7. **T80's own costume check** (T80-build part 5): which of the top hat, bob wig and shades fit by the socket alone, and any fit it says needs its own number. Those go into `ON` in `make_costumes.py` (1a).

## Run T47 after T80

**Recommended order: T79, T80, then T47.** T47 needs every head's `HeadSocket` in its final place: T80 sets Meta's and my box's from its own costume check and writes them under its "Findings", and it tags Meta's glasses. Run before T80, T47 would fit and screenshot five bots of which two still wear T46's pill (T79 keeps it for Meta and me until T80), and T80 would then move both sockets, so T47's check on two of the five robots would have to be done again. Both tasks lock `BP_Robot`, so they run one at a time anyway. T80's sheet is written to work without T47 (it tries the headpieces with spawned actors).

If T80 is delayed and T47 must go first: build parts 1 to 4 on T79's robot, check the costumes on the three round heads only, and leave a note in T47's "Findings" that Meta's and my costumes are unchecked; T80's part 5 then checks them through `SetHeadpiece`.

| File | What it is |
|---|---|
| [T47-build/costumes.json](T47-build/costumes.json) | The draft of the new `Content/NHOS/Data/costumes.json`: 14 headpiece ids (the 13 models, plus the ball cap worn backwards), each with its mesh and its fit on `HeadSocket`. |
| [T47-build/scenes_seats.json](T47-build/scenes_seats.json) | All 35 seats, card by card in `scenes.json` order: role, `headpiece`, `color` (hex), and the doc's color words (for reading only; not copied into the game). Unchanged in this refresh. |
| [T47-build/make_costumes.py](T47-build/make_costumes.py) | Builds both files from `Docs/PropArt/manifest.json` and its own tables, and writes the seats' `headpiece` and `color` into a `scenes.json` by editing its text (the file keeps its one-line-per-seat form). |

Sources read for the refresh: `Docs/tasks/T47.md` and its plan entry, [T79-build.md](T79-build.md) (all of it; part 8 lists what T47 must change), [T80-build.md](T80-build.md) (parts 2, 3a, 5 and 7), `T80.md`, `T45.md` (its Findings), `Docs/BotArt.md`, `Graphs/BP_Robot/{SetPassed,SetPersona,InitHome}.txt`, `Graphs/BP_Prop/{SetProp,LoadProps}.txt`, `Graphs/BP_StageDirector/ResetStage.txt`, `Graphs/BP_Show/StagePrep.txt`, `Content/NHOS/Data/{scenes,props}.json`, `Tools/check_prompts.py`, `Config/DefaultGame.ini` and `Docs/PropArt/manifest.json`. The first sheet's sources are in its git history (`26a7ae7`).

## In short

- **Data:** each seat in `scenes.json` gets `headpiece` (an id) and `color` (sRGB hex). A new `costumes.json` holds the headpieces: mesh, scale, `x`, `y`, `z`, `yaw` and `top` on `HeadSocket`, and an optional `on`. `make_costumes.py` writes the seats' fields and one `_readme` sentence; the checker gets `costume_problems`.
- **`BP_Robot`:** `SetHeadpiece(Id, Color)` makes a `Hat` static mesh component on `HeadSocket` the first time (at run time, so the robots in `L_Stage` need no re-place), loads the mesh from `costumes.json`, sets its transform, colors its `M_Clay` instance from the hex, hides the robot's own glasses under the shades, and lifts the antenna stalk, the toppers and the name label so the topper pokes out of the top. An empty id takes it off and puts them back.
- **Bare-headed at Scene Prep:** `BP_StageDirector.ResetStage` (which runs at Scene Prep) takes every standing robot's headpiece off. A cut robot keeps its own.
- **`BP_Show`** (the PC's chain): one call per robot where each robot gets its seat (`StageSetup`): `SetHeadpiece(seat.headpiece, seat.color)`. Kept separate in part 4.
- **`Config/DefaultGame.ini`:** `+DirectoriesToAlwaysCook=(Path="/Game/NHOS/Stage/Headpieces")`, next to T45's prop line.

## Decisions made for my person

My person asked prep sessions to take the task's default or my recommendation on calls that are theirs, and list them here. The T47 session should show this list to my person when it closes the task.

1. **The hex values are mine.** The doc names each color in words ("sandy straw yellow", "moss green"); `make_costumes.py`'s `SEATS` table turns each into an sRGB hex, and `scenes_seats.json` keeps the doc's words beside it. Blacks are very dark grays (#121216 to #2A2A2E), because pure black clay reads as a hole under the stage lights; the white-ish ones are a little warm or cool (#F0E6CC cream, #D9DEE6 silver) because T46 found the spotlight washes bright colors to white.
2. **One color per headpiece.** Every headpiece model is one clay mesh with `MI_Clay_Neutral` (T43), and `SetHeadpiece` colors the whole mesh. Five roles lose a second detail the doc names: the boxer's gold trim, the boss's red hat band, the nosy errand man's black band, the fixer's white band and the dwarf's ginger beard (the dwarf's whole helmet and beard are iron gray). A second color would need a model with two material slots, or a second mesh.
3. **The eldest son's backwards cap is its own id, `ball_cap_back`:** the same model and color input, turned 180°. So `costumes.json` has 14 ids for 13 models. The task's "one of the 13 ids" counts models; the checker counts models too ("every model is worn by some seat").
4. **The headpieces are sized by the round head, from bounding boxes** (changed in the refresh). Each piece's width across the face is set by hand (hats 72 to 90 cm, wigs and hoods 84 to 98, the saucepan 89 with its handle), and `make_costumes.py` turns it into scale and height from the manifest's bounds. The rule: nothing but the shades covers the eyes (front edge above z 141), nothing covers the mouth, and a wig's bangs may cover the brows (`Docs/BotArt.md`: "the mouth always shows"). These are starting points from bounding boxes only; the shapes inside them were not seen. Tune by screenshot (part 5c); a change is a number in `make_costumes.py`, not a graph change.
5. **The topper rises with the hat** (changed: `top` replaces `lift`). The doc: the antenna topper "pokes up through" the hat; T47.md says "beside it". A top hat or a wizard hat would swallow the halo and the warning light, so `SetHeadpiece` raises the stalk (`Nub`), the toppers (and my `Wire` and `PingPong` after T80) and the name label until the stalk's base is 4 cm under the hat's top, on any head and socket scale. The tallest is the beanie (top at z 221 on the round head, so the stalk rises 61 cm and the label to z 289); if that leaves the house camera's frame, narrow the beanie first, then the wizard hat.
6. **The name label rises too,** by the same lift, so a raised topper doesn't run through it. T57's "(passed)" line is part of the label and rises with it. If T38's bubbles anchor on the label, they follow.
7. **Bare-headed in Scene Prep, dressed at the scene's start,** as T47 step 3 says.
8. **The bare-headed call goes in `BP_StageDirector.ResetStage`,** not `BP_Show`: it already loops every robot at Scene Prep. This adds `BP_StageDirector.uasset` and `Graphs/BP_StageDirector/ResetStage.txt` to T47's commit, outside its Touches; name them in the commit message. The fallback is a loop over the robots in `BP_Show.StagePrep`.
9. **The `Hat` component is made at run time** (`Add Component by Class`) **and attached to `HeadSocket`** (changed). A template component would mean re-placing all five robots (T17, T46), and T79 and T80 have each just done that.
10. **Cook the headpiece folder** (`Config/DefaultGame.ini`, outside the Touches; name it in the commit). A mesh named only in `costumes.json` is referenced by nothing, so a packaged build would leave it out (T45 found the same for its props).
11. **New check lines:** `NHOS: COSTUME <persona> <id> <hex>` when a robot puts a headpiece on, `NHOS: COSTUME <persona> off` when it takes it off, and `NHOS: COSTUME <persona> unknown <id>` or `... mesh missing <path>` on a failure.
12. **No design doc edit.** The doc names each role's piece and color word, and the game follows it.
13. **The dark shades hide Anthropic's and Meta's own glasses** (new; T47.md step 2 and `Docs/BotArt.md`), by the `glasses` tag T79 and T80 give them. On SpaceXAI they sit on the visor and the nose comes out under them (`Docs/BotArt.md`).
14. **Hats that sit on the crown keep the first sheet's numbers** (new): the round head's top is where T46's dome topped out, and at the brim's height (z 150) the two heads' widths differ by about 2 cm (47 cm across on the round head, 45 on the dome). The top hat, wide-brim hat, fedora and wizard hat rest at z 150, 5 cm over the brows.
15. **The saucepan rests on the forehead** (new): a pot can't come down over a head whose face reaches 11 cm from its top, so it is 54 cm across and rests where the round head is that wide, its front rim at z 145, over the brows, pot bottom up. The first sheet's 76 cm pot came down to z 128, over the new eyes.
16. **A `y` offset for the saucepan's handle** (new), 17.7 cm, sign unknown until a close-up (5c).
17. **A per-persona override (`on`) is built but empty** (new). T80 makes one socket per head fit, which is the plan's way; `on` is the fallback for a piece that still doesn't fit one head (most likely the shades on my box, or a wig on its corners), so the fix stays a number. The checker allows only the five persona ids in it.
18. **The ear pods stay shown** under every headpiece (new). T79 suggests an `ears` tag to hide them under hoods and wigs; nothing is hidden by default, because the hood (98 cm) and the dino hood (84) are wider than the pods' 76 cm, and a pod showing under the bob wig may read as an ear. If a close-up shows a pod through a wig's side, widen that wig first (5c).

## 0. Before you start

1. **T80 is done** (see "Run T47 after T80"), or my person chose to run T47 first. `git pull`, read `Agents/`, then `git lfs locks`: no lock on `BP_Robot.uasset`, `BP_StageDirector.uasset` or (for part 4) `BP_Show.uasset`.
2. **Re-check the list above** ("What T47 must re-check") against T79's and T80's pushed `Graphs/BP_Robot/` files and Findings, and fix this sheet's numbers where they moved.
3. **The roles haven't moved.** `python Docs/tasks/T47-build/make_costumes.py` checks every card id and role in `Content/NHOS/Data/scenes.json` against its table and stops on an `assert` that names what moved. At `7e973bd` it says "every role matches".
4. **Which way the robot faces.** This sheet takes the robot's face as `Rig` +X (T79: "`Rig` +X is the robot's face"), and `HeadSocket` has no rotation, so `yaw` 270 turns a Meshy model's face (raw +Y, T43) to it. If the first screenshot shows hats facing backwards, set `FRONT_YAW = 90` in the script and run it again.
5. **The lift list.** With editor Python (T46's way: `SubobjectDataSubsystem.k2_gather_subobject_data_for_blueprint`), print every component tagged `acc` whose relative Z is 165 or more, plus `Nub`, `Label` and `HeadSocket`: its name, its parent, its relative location and scale, and its tags. Expected: `Nub` (0, 0, 168), the toppers (`Halo0` to `Halo11`, `WarnDome`, `Bolt0` to `Bolt2`), T80's `Wire` (centre about 168) and `PingPong` (181), `Label` on the root at z 228, and nothing of the bodies (T79 adds no part that high; OpenAI's floor ring is at z 0.6). Part 2d's `InitLift` lifts `Nub`, `Label` and each of those. If a topper is a child of `Nub` (T46 hung them off `Rig`), leave it out: lifting `Nub` already lifts it.
6. **Locks:** `BP_Robot.uasset`, `BP_StageDirector.uasset`, `BP_Show.uasset` (part 4). `BP_Show` is the PC's chain: take it only when the chain has released it, and pull first.

## 1. Data (step 1)

### 1a. `costumes.json` (new)

Copy [T47-build/costumes.json](T47-build/costumes.json) to `Content/NHOS/Data/costumes.json` (or run the script again after a change and copy its output). Its 14 ids, fitted to the round head:

| Id | scale | x | y | z | yaw | top | Width × depth × height (cm) | On the round head (`Rig` z) | Stalk rises | First sheet (`Rig` z / lift) |
|---|---|---|---|---|---|---|---|---|---|---|
| `top_hat` | 0.3787 | 0 | 0 | 19.7 | 270 | 47.4 | 72 × 72 × 55 | 150 to 205 | 45.4 | 177.7 / 45.4 |
| `wide_brim_hat` | 0.4732 | 0 | 0 | 7.8 | 270 | 23.6 | 90 × 89 × 32 | 150 to 182 | 21.6 | 165.8 / 21.6 |
| `fedora` | 0.4505 | 0 | 0 | 9.8 | 270 | 27.7 | 80 × 86 × 36 | 150 to 186 | 25.7 | 167.8 / 25.7 |
| `wizard_hat` | 0.4204 | 0 | 0 | 23.3 | 270 | 54.5 | 80 × 78 × 63 | 150 to 213 | 52.5 | 181.3 / 52.5 |
| `ball_cap` | 0.6021 | 20 | 0 | 12.9 | 270 | 40.8 | 74 × 115 × 56 | 143 to 199 | 38.8 | 162.9 / 30.8 |
| `ball_cap_back` | 0.6021 | −20 | 0 | 12.9 | 90 | 40.8 | 74 × 115 × 56 | 143 to 199 | 38.8 | 162.9 / 30.8 |
| `beanie` | 0.4182 | 0 | 0 | 23.8 | 270 | 63.4 | 68 × 69 × 79 | 142 to 221 | 61.4 | 174.5 / 58.8 |
| `tiara` | 0.3415 | 0 | 0 | 4.1 | 270 | 0 | 56 × 65 × 32 | 146 to 178 | 0 | 158.4 / 0 |
| `saucepan_helmet` | 0.4679 | 0 | 17.7 | 2.2 | 270 | 17.2 | 89 × 54 × 30 | 145 to 175 | 15.2 | 149.5 / 10.8 |
| `bob_wig` | 0.4502 | −4 | 0 | −23.1 | 270 | 19.7 | 84 × 78 × 86 | 92 to 178 | 17.7 | 134.9 / 17.7 |
| `hood` | 0.5496 | −6 | 0 | −7.7 | 270 | 44.5 | 98 × 66 × 105 | 98 to 203 | 42.5 | 150.3 / 42.5 |
| `dino_hood` | 0.5911 | 10 | 0 | −14.7 | 270 | 28.5 | 84 × 112 × 86 | 100 to 186 | 26.5 | 143.3 / 26.5 |
| `horned_helmet_beard` | 0.6003 | 4 | 0 | −12.9 | 270 | 44.2 | 85 × 67 × 114 | 88 to 202 | 42.2 | 125.1 / 22.2 |
| `dark_shades` | 0.422 | −0.2 | 0 | −20.1 | 270 | 0 | 72 × 80 × 28 | 124 to 152 | 0 | 116.3 / 0 |

`scale`, `x`, `y`, `z`, `yaw` are the `Hat`'s relative transform under `HeadSocket`; `z` is the model's center (Meshy pivots are centered, T43). "On the round head" is where the piece runs in `Rig` z on OpenAI, Anthropic and SpaceXAI (socket at z 158, scale 1); "Stalk rises" is the lift `SetHeadpiece` works out there. On Meta and my box, `HeadSocket`'s place and scale (T80) carry every number. **Missing a model: none.** All 13 headpiece meshes are in `Content/NHOS/Stage/Headpieces/` (the script checks each `.uasset`), and every one is worn by at least one seat. Who wears which is in `scenes_seats.json` (unchanged).

How the numbers come out (the script's comments say the same): scale = width ÷ the model's raw X bound; `z` = where its lowest point sits + half its height − 158; `top` = its top − 158 (0 for the tiara and the shades, which leave the stalk where it is); the shades' front sits at x 40, in front of Anthropic's glasses (x 35.8) and the eyes (x 38), and their `z` puts them over the eyes (z 124 to 152, centered near the eye line at 135) with their bottom just over the mouth (z 122 to 124 at rest).

**Look at these first** (from their bounds, not their shapes; the script prints the list, and part 5c says how to tune):
- `dark_shades`: on the eyes (z 129 to 141) and clear of the mouth; the temples (80 cm deep with the arms) rest on the ear pods and may stick out 7 cm behind the round head and 18 cm behind my box (T80 puts its front at x 28, 56 deep). If they do, narrow the shades or give my box an `on` entry. On SpaceXAI, the nose should come out under them.
- `horned_helmet_beard`: raised 20 cm with the face. The helmet's rim must clear the eyes (z 141) and the beard start under the mouth (z 118). If the 85 cm width is the horns' span, the helmet's bowl may be narrower than the 70 cm head and the head may show through it: widen it.
- `ball_cap` and `ball_cap_back`: raised 8 cm (T46's bill at z 135 is now the eye line); the bill rests over the brows. It perches on the crown: if it floats, lower it to z 141 at most.
- `beanie`: raised 12 cm off the eyes and narrowed from 76 to 68 cm, so it stands 63 cm over the head, not 74. If it reads as a sock, narrow it more.
- `tiara`: raised 6 cm off the eyes and narrowed to 56 cm, about the head's width at z 146 (55 cm across, 52 deep). If the model is a front-only arc, not a circlet, move it forward (`x` about 22).
- `saucepan_helmet`: the pot (54 of the 89 cm) should sit centered on the head, the handle out to one side. If the pot sits off to the side and the handle over the head, negate `y`. If the pot is modeled upright (open on top), add 180 to its pitch (a new `pitch` field and one more pin in `SetHeadpiece`), or flip the mesh in the asset.
- `bob_wig` (open underside): the fringe should end over the brows (about z 145), not the eyes, and the sides may show the ear pods (Decision 18).
- `hood` and `dino_hood`: the face opening must frame the screen (z 118 to 147); the dino hood's snout and jaw must leave the eyes and the mouth showing. Both hang to the collar (z 88 to 98).

### 1b. `scenes.json`

In the repo folder:

```bash
python Docs/tasks/T47-build/make_costumes.py Content/NHOS/Data/scenes.json Content/NHOS/Data/scenes.json
```

It adds `, "headpiece": "<id>", "color": "#RRGGBB"` to each of the 35 one-line seats, and appends one sentence to the end of the `_readme`'s `cards` line: `Each seat's 'headpiece' (an id in costumes.json) and 'color' (sRGB hex) dress the robot that plays it (T47); the game never sends them to the AIs.` `git diff` should show exactly 36 changed lines. The script can run again on its own output (a second run changes nothing), so it is also how a color or headpiece changes later. Every seat's values are in [T47-build/scenes_seats.json](T47-build/scenes_seats.json). **Tested on a copy of `scenes.json` at `7e973bd`** (T44's cards, after T45 took the shared props out of `set`): 36 lines, and the checker with 1c's function passes on the result.

**"The game never sends these fields to the AIs":** the AIs' state copies `role` and `want` from a seat by name (T06's `cast [{name, role, want, status}]` and `you {name, role, want, note}`), and the checker's simulated shows do the same. Check in part 4 that `BP_Show` copies fields by name too and never sends the whole seat object.

### 1c. `Tools/check_prompts.py`

1. **`costume_problems`**, after T45's `props_file_problems`, called from `check_files` right after T45's line (`errors.extend(props_file_problems(cards, load_json("props.json", errors) or {}))`):
   ```python
       errors.extend(costume_problems(cards, load_json("costumes.json", errors) or {}))
   ```
   **Tested at `7e973bd`** (in a copy of the checker): with the drafts in place, `--offline` passes; with today's `scenes.json` it fails with 83 lines (35 seats × 2, plus 13 unworn models); a made-up headpiece, a color word, a missing `top` and a bad `on` key give one line each.
   ```python
   PERSONA_IDS = {"visionary", "worrier", "overclocker", "copycat", "human"}  # BP_Robot.SetPersona's ids
   FIT_KEYS = ("scale", "x", "y", "z", "yaw", "top")


   def costume_problems(cards, cdata) -> list[str]:
       """costumes.json and each seat's costume (T47): every seat names a known headpiece and a hex
       color; every headpiece has a mesh on disk and a fit; every headpiece model is worn by some seat."""
       def num(v):
           return isinstance(v, (int, float)) and not isinstance(v, bool)
       out, heads = [], cdata.get("headpieces", {})
       if not isinstance(heads, dict) or not heads:
           return ["costumes.json: needs a 'headpieces' object keyed by id"]
       for hid, h in heads.items():
           h = h if isinstance(h, dict) else {}
           mesh = h.get("mesh", "")
           if not isinstance(mesh, str) or not re.fullmatch(r"/Game/[\w/]+\.\w+", mesh):
               out.append(f"costumes.json: headpiece {hid!r} needs a mesh object path (/Game/.../SM_X.SM_X)")
           elif not (ROOT / "Content" / (mesh[6:].rsplit(".", 1)[0] + ".uasset")).exists():
               out.append(f"costumes.json: headpiece {hid!r}'s mesh {mesh} is not in Content/")
           if not all(num(h.get(k)) for k in FIT_KEYS) or not h.get("scale", 0) > 0 or h.get("top", 0) < 0:
               out.append(f"costumes.json: headpiece {hid!r} needs a scale above 0, a top of 0 or more and numbers for {', '.join(FIT_KEYS[1:])}")
           for pid, o in (h.get("on") or {}).items():
               if pid not in PERSONA_IDS or not isinstance(o, dict) or not o or set(o) - set(FIT_KEYS) or not all(num(v) for v in o.values()):
                   out.append(f"costumes.json: headpiece {hid!r}'s 'on' needs persona ids ({', '.join(sorted(PERSONA_IDS))}) with numbers for scale, x, y, z or top")
       worn = set()
       for c in cards:
           for x in c.get("seats", []):
               hp, col = x.get("headpiece"), x.get("color", "")
               if hp not in heads:
                   out.append(f"scenes.json: {c.get('id')}'s seat {x.get('role')!r} needs a headpiece from costumes.json, not {hp!r}")
               else:
                   worn.add(heads[hp].get("mesh"))
               if not re.fullmatch(r"#[0-9A-Fa-f]{6}", col or ""):
                   out.append(f"scenes.json: {c.get('id')}'s seat {x.get('role')!r} needs a color like #A8CCFF")
       for m in sorted({h.get("mesh") for h in heads.values() if isinstance(h, dict)} - worn):
           out.append(f"costumes.json: no seat wears {m}")
       return out
   ```
2. **The seat check** ("needs 5 seats ..., each with a role and a want") stays as it is.
3. **The docstring:** a paragraph after T44's and T45's props paragraphs: "Costumes (T47): each seat names a headpiece from `costumes.json` and a hex color. The checker fails an unknown headpiece, a color that isn't `#RRGGBB`, a headpiece mesh that isn't on disk, a headpiece without its fit numbers and a model no seat wears. The game never sends these fields to the AIs." Add `costumes.json` to the `Files OK:` line's list.
4. Run `python Tools/check_prompts.py --offline`. It must pass.

## 2. `BP_Robot` (step 2)

Start from `BP_Robot` as T79 and T80 pushed it (see "What T47 must re-check"). Every graph below is new; T47 changes none of T79's or T80's graphs.

### 2a. Variables

| Variable | Type | Default |
|---|---|---|
| `Hat` | `StaticMeshComponent` object reference | none |
| `CostObj`, `CEntry`, `COn`, `CFit` | `JsonObjectWrapper` (`add_struct_variable` with `/Script/JsonUtilities.JsonObjectWrapper`, T45) | empty |
| `CostLoaded`, `LiftReady` | Boolean | false |
| `HMesh` | String | "" |
| `HScale`, `HX`, `HY`, `HZ`, `HYaw`, `HTop`, `FTmp` | Float | 1, 0, 0, 0, 0, 0, 0 |
| `LiftComps` | `SceneComponent` object reference, array | empty |
| `LiftBase` | Vector, array | empty |

No component is added to the Blueprint (Decision 9), so the robots in `L_Stage` stay as they are.

### 2b. Nodes to look up first

As in [T45-build.md](T45-build.md) part 2b (`find_node_types` with `context_pins: []`, then `get_node_type_pins`; spell the DSL from what comes back). The soft load and the cast are spelled as T45 pushed them in `Graphs/BP_Prop/SetProp.txt`. New ones:

| In the DSL below | The Blueprint node |
|---|---|
| `Game|AddComponentbyClass` | Add Component by Class (already used in `BPC_LLMClient.SendReq`; its return value takes the class pin's type, so no cast) |
| `Transformation|AttachComponentToComponent` | Attach Component To Component |
| `Collision|SetCollisionEnabled` | Set Collision Enabled |
| `Utilities|String|Mid`, `Utilities|String|FindSubstring`, `Utilities|String|ToUpper`, `Utilities|String|Replace` | the string nodes |
| `Utilities|Struct|MakeColor`, `Math|Conversions|ToLinearColor(Color)`, `Math|Conversions|ToByte(Integer)` | Make Color (bytes), Color to Linear Color (the sRGB conversion), Integer to Byte |
| `Transformation|GetRelativeLocation`, `Transformation|GetRelativeScale3D` | the component's `RelativeLocation` and `RelativeScale3D` getters |

`Math|Float|Max(Float)` is in `Graphs/WBP_Stage/FadeBanner.txt`; `(.z v)` in `Graphs/BP_Robot/StartMove.txt`.

### 2c. `LoadCostumes` and `HexColor` (new)

```lisp
; T47: costumes.json, read once per robot. A missing or broken file leaves CostObj empty, so every
; headpiece is "unknown" and the robot stays bare-headed.
(fn LoadCostumes ()
  (if (V CostLoaded)
    (return))
  (set CostLoaded true)
  (bind (_o _ok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat (Utilities|Paths|GetProjectContentDirectory) "NHOS/Data/costumes.json"))))
  (if (not _ok)
    (print "NHOS: COSTUME costumes.json missing or not valid JSON")
    (return))
  (bind _h (Json|GetField _o "headpieces"))
  (set CostObj _h))
```

```lisp
(fn HexByte (S At)
  ; T47: two hex digits of S, from At, as a byte. A bad digit counts as 0.
  (bind _d "0123456789ABCDEF")
  (bind _hi (Utilities|String|FindSubstring :SearchIn _d :Substring (Utilities|String|Mid :SourceString S :Start At :Count 1)))
  (bind _lo (Utilities|String|FindSubstring :SearchIn _d :Substring (Utilities|String|Mid :SourceString S :Start (+ At 1) :Count 1)))
  (return (Math|Conversions|ToByte(Integer) (+ (* (max _hi 0) 16) (max _lo 0)))))

(fn HexColor (Hex)
  ; T47: "#E3C770" -> linear color. Color to Linear Color does the sRGB conversion, so
  ; HexColor("#A8CCFF") is about (0.39, 0.60, 1.0), OpenAI's seat color in SetPersona.
  (bind _h (Utilities|String|ToUpper (Utilities|String|Replace :SourceString Hex :From "#" :To "")))
  (return (Math|Conversions|ToLinearColor(Color) (Utilities|Struct|MakeColor :R (CallFunction|HexByte :S _h :At 0) :G (CallFunction|HexByte :S _h :At 2) :B (CallFunction|HexByte :S _h :At 4) :A 255))))
```

Mark `HexByte` and `HexColor` pure if the DSL lets you; they are fine as plain functions too. If a string literal can't be bound (`(bind _d "...")`), put the digits in a String variable `HexDigits` with that default. `max` on integers: use the integer Max node if the DSL has no `max`.

### 2d. `InitLift`, `LiftTop`, `MakeHat`, `ShowGlasses` and `FitNum` (new)

```lisp
(fn InitLift ()
  ; T47: what rises with a hat, and where each part sits bare-headed. Nub first: SetHeadpiece reads
  ; its place as the stalk's base. Check the list in part 0 step 5.
  (if (V LiftReady)
    (return))
  (set LiftReady true)
  (add (V LiftComps) (Variables|Default|GetNub))
  (add (V LiftComps) (Variables|Default|GetLabel))
  (for _c (Actor|GetComponentsByClass :ComponentClass "/Script/Engine.StaticMeshComponent")
    (if (and (Components|ComponentHasTag :self _c :Tag "acc") (>= (.z (Transformation|GetRelativeLocation :self _c)) 165.0))
      (add (V LiftComps) _c)))
  (for _c (V LiftComps)
    (add (V LiftBase) (Transformation|GetRelativeLocation :self _c))))

(fn LiftTop (Lift)
  (for _i (range (len (V LiftComps)))
    (Transformation|SetRelativeLocation :self (get (V LiftComps) _i) :NewLocation (+ (get (V LiftBase) _i) (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z Lift)))))

(fn MakeHat ()
  ; T47: the Hat component, made once, on HeadSocket (T79), so it sits on each head's own socket
  ; and bobs, hops and slumps with the body.
  (Utilities|IsValid (V Hat)
    (:"Is Valid")
    (:"Is Not Valid"
      (bind _c (Game|AddComponentbyClass self "/Script/Engine.StaticMeshComponent" :bManualAttachment true))
      (set Hat _c)
      (Transformation|AttachComponentToComponent :self (V Hat) :Parent (V HeadSocket) :LocationRule "KeepRelative" :RotationRule "KeepRelative" :ScaleRule "KeepRelative" :bWeldSimulatedBodies false)
      (Collision|SetCollisionEnabled :self (V Hat) :NewType "NoCollision"))))

(fn ShowGlasses (On)
  ; T47: the dark shades hide this robot's own glasses (Anthropic's from T79, Meta's from T80, tagged
  ; "glasses"). On again, only the persona's own pair comes back, as SetPersona's acc rule shows it.
  (bind _tag (Utilities|String|StringToName (Variables|Default|GetPersonaId)))
  (for _c (Actor|GetComponentsByClass :ComponentClass "/Script/Engine.StaticMeshComponent")
    (if (Components|ComponentHasTag :self _c :Tag "glasses")
      (Rendering|SetVisibility :self _c :bNewVisibility (and On (Components|ComponentHasTag :self _c :Tag _tag)) :bPropagateToChildren false))))

(fn FitNum (Key Def)
  ; T47: a number from this robot's override (CFit), or Def if the override doesn't set it.
  (if (not (Json|HasField (V CFit) Key))
    (return Def))
  (bind _v (Json|GetField (V CFit) Key))
  (set FTmp _v)
  (return (V FTmp)))
```

- `Nub`'s rotation isn't touched; only locations move. T80 removes `SetPersona`'s `Nub` rotation line anyway.
- `InitLift` runs once, at the first `SetHeadpiece`, after `SetPersona` and `InitHome` (the show seats every robot before its first Scene Prep). It doesn't touch rotation, so `InitHome`'s absolute rotation on `Label` stays.
- If `Rig`, `Nub`, `Label` or `HeadSocket` read differently in the pushed sources (`(Variables|Default|GetHeadSocket)` in T79's `SetPersona`, `(V HeadSocket)` in its `Receive`), use the form that compiles.

### 2e. `SetHeadpiece(Id, Color)` (new)

```lisp
(fn SetHeadpiece (Id Color)
  ; T47: put on headpiece Id (an id in costumes.json) in Color (sRGB hex), or take it off ("").
  ; It hangs on HeadSocket; the stalk, the toppers and the label rise so the topper pokes out of it.
  (CallFunction|InitLift)
  (CallFunction|LoadCostumes)
  (bind _has (and (not (Utilities|String|IsEmpty Id)) (Json|HasField (V CostObj) Id)))
  (CallFunction|ShowGlasses :On (not (and _has (streq Id "dark_shades"))))
  (if (not _has)
    (Utilities|IsValid (V Hat)
      (:"Is Valid" (Rendering|SetVisibility :self (V Hat) :bNewVisibility false :bPropagateToChildren false))
      (:"Is Not Valid"))
    (CallFunction|LiftTop :Lift 0.0)
    (print (cat "NHOS: COSTUME " (Variables|Default|GetPersonaId) (select (Utilities|String|IsEmpty Id) " off" (cat " unknown " Id))))
    (return))
  (bind _e (Json|GetField (V CostObj) Id))
  (set CEntry _e)
  (bind _m (Json|GetField (V CEntry) "mesh"))
  (set HMesh _m)
  (bind _s (Json|GetField (V CEntry) "scale"))
  (set HScale _s)
  (bind _x (Json|GetField (V CEntry) "x"))
  (set HX _x)
  (bind _y (Json|GetField (V CEntry) "y"))
  (set HY _y)
  (bind _z (Json|GetField (V CEntry) "z"))
  (set HZ _z)
  (bind _w (Json|GetField (V CEntry) "yaw"))
  (set HYaw _w)
  (bind _t (Json|GetField (V CEntry) "top"))
  (set HTop _t)
  ; T47: this persona's override, if costumes.json has one ("on": {persona: {scale, x, y, z, top}}).
  (if (Json|HasField (V CEntry) "on")
    (bind _on (Json|GetField (V CEntry) "on"))
    (set COn _on)
    (if (Json|HasField (V COn) (Variables|Default|GetPersonaId))
      (bind _pf (Json|GetField (V COn) (Variables|Default|GetPersonaId)))
      (set CFit _pf)
      (set HScale (CallFunction|FitNum :Key "scale" :Def (V HScale)))
      (set HX (CallFunction|FitNum :Key "x" :Def (V HX)))
      (set HY (CallFunction|FitNum :Key "y" :Def (V HY)))
      (set HZ (CallFunction|FitNum :Key "z" :Def (V HZ)))
      (set HTop (CallFunction|FitNum :Key "top" :Def (V HTop)))))
  (CallFunction|MakeHat)
  (bind _obj (Utilities|LoadAssetBlocking :Asset (Utilities|ToSoftObjectReference (Utilities|MakeSoftObjectPath :PathString (V HMesh)))))
  (bind _mesh (Utilities|Casting|CastToStaticMesh :Object _obj)
    (:then
      (Components|StaticMesh|SetStaticMesh :self (V Hat) :NewMesh _mesh)
      (Transformation|SetRelativeScale3D :self (V Hat) :NewScale3D (Math|Vector|MakeVector :X (V HScale) :Y (V HScale) :Z (V HScale)))
      (Transformation|SetRelativeLocation :self (V Hat) :NewLocation (Math|Vector|MakeVector :X (V HX) :Y (V HY) :Z (V HZ)))
      (Transformation|SetRelativeRotation :self (V Hat) :NewRotation (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw (V HYaw)))
      (Rendering|Material|SetVectorParameterValueonMaterials :self (V Hat) :ParameterName "Color" :ParameterValue (Math|Conversions|ToVector(LinearColor) (CallFunction|HexColor :Hex Color)))
      (Rendering|SetVisibility :self (V Hat) :bNewVisibility true :bPropagateToChildren false)
      ; T47: the stalk's base ends 4 cm under the hat's top, on any head: the hat's top in Rig is
      ; socket z + socket scale x top, and the stalk's base is Nub's bare z - 12 (it is 24 cm tall).
      ; On the round head this is top - 2, the first sheet's lift.
      (bind _sl (Transformation|GetRelativeLocation :self (V HeadSocket)))
      (bind _ss (Transformation|GetRelativeScale3D :self (V HeadSocket)))
      (bind _nb (get (V LiftBase) 0))
      (CallFunction|LiftTop :Lift (select (> (V HTop) 0.0) (Math|Float|Max(Float) 0.0 (+ (+ (.z _sl) (* (.z _ss) (V HTop))) (- 8.0 (.z _nb)))) 0.0))
      (print (cat "NHOS: COSTUME " (Variables|Default|GetPersonaId) " " Id " " Color)))
    (:CastFailed
      (print (cat "NHOS: COSTUME " (Variables|Default|GetPersonaId) " mesh missing " (V HMesh)))
      (Rendering|SetVisibility :self (V Hat) :bNewVisibility false :bPropagateToChildren false)
      (CallFunction|LiftTop :Lift 0.0)
      (CallFunction|ShowGlasses :On true))))
```

- `SetVectorParameterValueOnMaterials` makes a dynamic instance of each slot's `MI_Clay_Neutral` (T11), so each robot's hat has its own color, and `Color` is `M_Clay`'s parameter (T43).
- **The cast is multi-exec** (T45's finding): everything after it is inside `:then`, because the call ends the flow.
- **The hat inherits `HeadSocket`'s scale and place** (`KeepRelative`): on Meta (T80: 0.9) every fit shrinks with it; on my box (T80: 5 cm higher, 6 cm back) every fit moves with it. The lift formula reads the socket, so the toppers follow too.
- **The cut keeps the hat:** T79's `SetCut` and `ResetLook` color only the parts tagged `seat` (and T79's `ring` loop hides only `ring` parts), so the untagged `Hat` keeps its color and stays on as the robot slumps. Nothing to change.
- **The talking bounce, hops, cheer, shake, slump and OpenAI's hover** move `Rig`, and `HeadSocket` is on `Rig`, so the hat moves with the head.
- **A head prop** would land on `HeadSocket` inside the hat (T79's `Receive`). T45 made every prop a hand prop, so none does today; a later task that adds a head prop should take the hat off for it.
- Optional, if time allows: a quick pop when the hat goes on (scale from 0.6 to 1 over 0.2 s in `EventTick`). Not in the task.

Save `Graphs/BP_Robot/{SetHeadpiece,LoadCostumes,HexByte,HexColor,InitLift,LiftTop,MakeHat,ShowGlasses,FitNum}.txt` as written.

## 3. Bare-headed at Scene Prep: `BP_StageDirector.ResetStage` (step 3, first half)

Start from the pushed `Graphs/BP_StageDirector/ResetStage.txt` (T45's: the props loop, `CardFromShow` and the `NHOS: ACT reset card=` line). Change only the robots' loop:

```lisp
  (for _b (V AllBots)
    (Class|BPRobot|GoHome :self _b)
    ; T47: every robot still standing takes its headpiece off for Scene Prep; a cut robot keeps its own.
    (if (not (Class|BPRobot|IsDown :self _b))
      (Class|BPRobot|SetHeadpiece :self _b :Id "" :Color "")))
```

`ResetStage` runs from `BP_Show.StagePrep` at every Scene Prep, before the prep card shows, so the robots stand bare-headed while I read my card. Taking the hat off also brings back Anthropic's and Meta's glasses.

## 4. Dressed at the scene's start: `BP_Show` (step 3, second half) — the PC's chain

**Re-check against the `Graphs/BP_Show/` sources of that day.** At `7e973bd` the graphs this part needs still have no source file: the deal of the card's seats to the actors (in `ScenePrep`, which prints `NHOS: SETUP`) and `StageSetup`, which gives each robot its seat name at `PREP start` (`StartFromPrep.txt` calls `StartScene`). T58 and T62 to T66 run on the PC before T47 and may change both. So, on the day:

1. `find_nodes` with title `Setup` in `BP_Show` (T28: titles match without spaces): the call that sets each robot's name and color (`BP_Robot.Setup(Name, Color, IsMe)`). Read only the graph it is in (expected: `StageSetup`). There the graph has, for each actor on stage, its robot and its seat index.
2. Find where that actor's dealt seat is kept: `find_nodes` for `GetField` with `role` in `ScenePrep` (or the graph that prints `NHOS: SETUP`). Confirm there that `role` and `want` are copied by name and the whole seat object never goes into a state (1b).
3. Add the call **right after `Setup`** for each robot, in one of two shapes:
   - **If the actor's seat object is at hand** (a `JsonObjectWrapper`):
     ```lisp
     (bind _hp (Json|GetField <seat> "headpiece"))
     (Variables|Default|SetHatId _hp)
     (bind _hc (Json|GetField <seat> "color"))
     (Variables|Default|SetHatColor _hc)
     (Class|BPRobot|SetHeadpiece :self <robot> :Id (Variables|Default|GetHatId) :Color (Variables|Default|GetHatColor))   ; T47
     ```
     with two new String variables, `HatId` and `HatColor` (T01: a JSON value goes through a typed variable).
   - **If only role and want were kept** (per-actor String arrays): add two String arrays, `ActorHat` and `ActorHatColor`, filled at the same spot and from the same seat as the role (`GetField "headpiece"`, `GetField "color"`), then in `StageSetup`: `(Class|BPRobot|SetHeadpiece :self <robot> :Id (get (V ActorHat) <i>) :Color (get (V ActorHatColor) <i>))`.
4. Save the graph files of the graphs you wrote (both have none today: write each one's source from a read of the graph, per `Graphs/README.md`, and commit it).

If writing a whole graph is too risky on the day, put the nodes in by hand (as T18 did in `SetupShow`) and record that in the graph's file. Nothing else in `BP_Show` changes for T47.

## 5. The check (step 4)

### 5a. A free autoplay show in a game window (the saved assets)

`Local/switches.json` as for T45's run (`"autoplay": true`, `"mode": "free"`, `"spare_human": true`, `"fast_lines": true`, `"ai_seats": 0`), so a show plays all its scenes. With the editor's assets saved (T27's Mac command):

```bash
"/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor" "<PROJECT>" -game -windowed -ResX=1600 -ResY=900 -log=T47.log
```

```bash
grep -E "NHOS: (SETUP|PREP (shown|start)|COSTUME|SHOW END)" ~/Library/Logs/AIMegaJam2026/T47.log
grep -c "LogScript" ~/Library/Logs/AIMegaJam2026/T47.log
```

Expected, per scene (`<…>` varies):

```
NHOS: SETUP human=human scene=<card id> ...
NHOS: COSTUME <persona> off                      (one per standing robot, from ResetStage)
NHOS: PREP shown scene=<n>
NHOS: PREP start scene=<n>
NHOS: COSTUME <persona> <headpiece id> <#hex>    (one per actor on stage)
...
NHOS: SHOW END result=<win|lose> ...
```

It passes when: the show reaches `SHOW END`; each scene has an `off` line for every standing robot before `PREP shown` and a `COSTUME <id>` line for every actor on stage after `PREP start`; each scene's ids and colors are that card's (compare with `scenes_seats.json`); a cut robot gets no `off` line in later scenes; no `unknown` or `mesh missing` line; and no `LogScript` line.

### 5b. Screenshots

The Done-when: all five bots in costume in two different scenes. Scene 1 has five actors on stage; scene 2 has four plus the cut one slumped in its costume, which shows the "keeps its headpiece" part.

- From the house camera: Scene Prep (bare-headed, Anthropic's and Meta's glasses on), the first turn of scene 1 (five in costume), and the first turn of scene 2 (a different card's costumes, and the cut robot still in its hat).
- Close-ups of each robot's head (T79-build part 6 step 3's camera: 260 cm in front, 100 cm up), in PIE (`SlateInspectorToolset.Screenshot`, T46's way) if the game-window capture is black (T46: a locked Mac screen gives black images). Seats are dealt at random, so to see each of the 10 pieces on the look-first list (1a), in PIE call `SetHeadpiece` on a robot with a one-off editor Python file (`bot.call_method("SetHeadpiece", ("<id>", "<#hex>"))`, the way T79-build part 6 step 4 calls `Receive`), on one round head, Meta and my box.
- The dark shades on Anthropic and on Meta: their own glasses must be gone. On SpaceXAI: the nose under the shades.
- Save them to `Saved/T47/shots/` (not in git).

### 5c. Judge, and tune

As a first-time player: can I tell the roles apart, and does each costume read as its role (the wizard's hat, the dwarf's helmet, the villain's saucepan)? Then per headpiece:

- **It floats, sinks or tilts on the round head:** change its `bottom` (and `x`, `y`) in `make_costumes.py`'s `FIT`, run the script, and copy `costumes.json` again. No graph change, and no editor restart: `LoadCostumes` reads the file at each show's start (a new game window; in PIE, a new PIE session).
- **It fits the round head but not Meta or my box:** first ask whether the socket is off for every piece on that head (then it is T80's number in `SetPersona`, a graph change in T47's commit; say so in the Findings). If only one piece is off, add an `ON` entry in `make_costumes.py` (for example `"dark_shades": {"human": {"x": -2.0}}`), run the script and copy `costumes.json` again.
- **It covers the eyes or the mouth:** the dwarf, the bob wig, the hoods and the shades are the likely ones (1a).
- **The topper doesn't poke out, or floats above the hat:** change that piece's `top` (raise it to lift more).
- **The color washes out under the spotlight** (the cream top hat, the silver tiaras, the sky-blue cap): darken that seat's hex a step in `SEATS` and run the script in place again (1b). A re-run rewrites every seat's `headpiece` and `color` and adds the `_readme` sentence only once, so it changes only what moved in `SEATS`.
- **The bolt or the label leaves the frame** under the beanie or the wizard hat: narrow those hats (Decision 5).
- **An ear pod shows through a wig's side:** widen that wig (Decision 18).

Write what the screenshots showed under T47's "## Findings", including what wasn't checked.

## 6. What T47 commits

`Content/NHOS/Data/costumes.json`, `Content/NHOS/Data/scenes.json`, `Tools/check_prompts.py`, `Config/DefaultGame.ini` (Decision 10), `BP_Robot.uasset`, `BP_StageDirector.uasset` (Decision 8), `BP_Show.uasset`, the `Graphs/` files of parts 2, 3 and 4, the plan, `T47.md` and `DevLog.md`, as "How to run a task" lists. `Docs/Assets.md` needs no line: every headpiece model is T43's and already listed.
