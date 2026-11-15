# T82 build sheet: the Hyper3D cast as assets (prep for T82 and T83)

Back to [T82](T82.md) and [T83](T83.md). Made on the Mac on 2026-11-15 in a second editor (a worktree, port 8011) while T75 held `BP_Robot`. It does T82's steps 2 and 3 for all 13 parts, T83's included. **Nothing in `BP_Robot`, `L_Stage`, `M_Clay` or any existing asset changed**, and T82 and T83 are not claimed. All numbers are also in [`Docs/CastArt/manifest.json`](../CastArt/manifest.json).

## 1. What was made

All new, all saved, 77 files:

| Folder | Assets |
|---|---|
| `Content/NHOS/Stage/Cast/RoundHead/` | `SM_RoundHead`, `MI_RoundHead`, `M_RoundHead`, `T_RoundHead_BaseColor`, `_Normal`, `_Roughness` |
| `Content/NHOS/Stage/Cast/openai/` | `SM_OpenAIBody`, `SM_OpenAIArm`, and for each: `MI_`, `M_`, `T_*_BaseColor`, `_Normal`, `_Roughness` |
| `Content/NHOS/Stage/Cast/anthropic/` | `SM_AnthropicBody`, `SM_AnthropicArm`, the same set each |
| `Content/NHOS/Stage/Cast/spacexai/` | `SM_SpaceXAIBody`, `SM_SpaceXAIArm`, the same set each |
| `Content/NHOS/Stage/Cast/meta/` | `SM_MetaHead`, `SM_MetaBody`, `SM_MetaArm`, the same set each |
| `Content/NHOS/Stage/Cast/you/` | `SM_YouHead` (3 slots, no textures: `M_YouHead_Teal_cardboard_paint`, `M_YouHead_Unpainted_cardboard_interior`, `M_YouHead_Gray_duct_tape`), `SM_YouBody`, `SM_YouArm` with the same set each |
| `Content/NHOS/Stage/Materials/` | `M_CastModel` (the new Substrate material) |

- **Names:** `SM_<Part>` the mesh; `M_<Part>` the material the importer made (renamed from `model` right after each import); `T_<Part>_BaseColor`, `_Normal`, `_Roughness` the textures (renamed from `texture_diffuse`, `texture_normal`, `texture_roughness`); `MI_<Part>` the new `M_CastModel` instance. The FBX files don't reference the metallic maps (near black), so none was imported.
- **Each mesh's default slot is now its `MI_<Part>`** (the textured `M_CastModel` look, the recommendation in part 3). The importer's `M_<Part>` (a legacy material with the same textures) is still there.
- Import rules as T43: `StaticMeshTools.import_file` with materials and textures, combined, one FBX at a time, renamed before the next. Normal maps came in as `TC_Normalmap`. The roughness maps came in sRGB; `M_CastModel` samples them as Color, so nothing breaks (a slight gamma on roughness, which `RoughFromTex` 0.5 blends anyway).
- Triangles: 14,998 to 15,000 a part; `SM_YouBody` 13,513; `SM_YouHead` 1,858.
- The importer left a `model.fbm/` folder beside each FBX (the embedded textures). They are not in git: moved to `/Users/personal/Projects/AIMegaJam2026/Local/art/T82prep/fbm/`.

## 2. The fits (yaw, scale, offset)

**The frame.** Every Rodin part faces **mesh +Y** after import (the importer maps the FBX's raw (x, y, z) to (100x, −100y, 100z) cm). So **yaw 270 (= −90)** turns each part's front to Rig +X, the robot's face. Checked by eye on four turned copies of every part on the stage (`facing_1.png`, `facing_2.png`). All parts come in at about 190 cm on their longest side, centered (my box head is 40 × 29 × 35 cm, centered too).

**How they were worked out.** A stdlib FBX reader read every part's vertices, so each number below comes from the geometry, not from a guess: the bounds after the yaw, the arms' long axis (its principal axis), the shoulder end's center, the round head's screen recess, Meta's nose tip and my box's eye slots. Then each bot was assembled from its parts in a throwaway preview on the stage, with these exact transforms, and checked by eye (part 3).

Locations are a component's relative location under its parent, in cm; rotations (roll, pitch, yaw).

### Heads and bodies (parent `Rig`, rotation yaw 270)

| Part | Scale | Location | Size in the Rig (deep × wide × tall) | Notes |
|---|---|---|---|---|
| `SM_RoundHead` | 0.3686 | (0, 0, 124.6) | 64 × 70 × 66.8, z 91.2 to **158** | Uniform scale by the 70 cm width. Its height is 66.8, not T79's 62 (it reaches 4.8 cm lower, into the collar). For T79's exact 62, scale Z 0.342 instead. |
| `SM_OpenAIBody` | 0.4907 | (0, 0, 46.6) | 50 × 70 × 93 | feet z 0, turtleneck top z 93 |
| `SM_AnthropicBody` | 0.4914 | (0, −0.1, 46.5) | 72 × 74 × 93 | |
| `SM_SpaceXAIBody` | 0.4894 | (0, 0, 46.6) | 61 × 65 × 93 | boots z 0 |
| `SM_MetaHead` | 0.3696 | (0, 0, 123.0) | 58 × 62 × 70, z 87.9 to **158** | Scaled so the nose tip lands at z 124 (T80's nose) with the top at 158. Its neck runs down into the tee. |
| `SM_MetaBody` | 0.4951 | (0, 0, 47.0) | 31 × 51 × 94 | shoes z 0, tee top z 94 |
| `SM_YouHead` | 1.6 | (0, 0, 130.0) | 47 × 64 × 56, z 102 to **158** | T80's box was 56 × 66 × 54; the model is shallower. |
| `SM_YouBody` | 0.526 | (0, 0, 50.0) | 57 × 61 × 100 | box top z 100 as T80's; jeans and sneakers to z 0 |

The bodies' tops (93, 94, 100) meet each head's bottom, as T79 and T80 built them; on the round head T79's gold collar (z 88 to 98) covers the joint.

### Arms (parent `ArmPivotL` / `ArmPivotR`)

Each arm is scaled to **53 cm from the shoulder's top to the hand's bottom** (T79's: the mitten's center at −44), hangs straight down, and its shoulder's top sits 4 cm above the pivot. One model per bot; the other side is mirrored with **X scale negated** (that flips the Rig's Y, because yaw 270 turns mesh X into Rig −Y) and the rotation given for that side.

| Arm | Modeled as | Left arm (`ArmPivotL`): rotation, scale, location | Right arm (`ArmPivotR`): rotation, scale, location | Hand center in the pivot |
|---|---|---|---|---|
| `SM_OpenAIArm` | either (straight, text only) | (0, 0, −90), (−0.2792, 0.2792, 0.2792), (−0.2, 1.4, −22.5) | (0, 0, −90), (0.2792, 0.2792, 0.2792), (−0.2, −1.4, −22.5) | (0.2, ±0.9, −43.4) |
| `SM_AnthropicArm` | robot's left; bent, raised 52° forward | (51.8, −1.7, −90.8), (0.2371 ×3), (0.3, −1.2, −24.6) | (51.8, 1.7, −89.2), (−0.2371, 0.2371, 0.2371), (0.3, 1.2, −24.6) | (−1.2, ±0.9, −42.4) |
| `SM_SpaceXAIArm` | robot's right; horizontal (thumbs up) | (−73.5, −0.5, −89.7), (−0.2599, 0.2599, 0.2599), (−3.0, −2.3, −20.9) | (−73.5, 0.5, −90.3), (0.2599 ×3), (−3.0, 2.3, −20.9) | (−2.2, ±0.2, −42.1) |
| `SM_MetaArm` | robot's right; straight | (0, 0, −90), (−0.2791, 0.2791, 0.2791), (3.4, −1.2, −22.5) | (0, 0, −90), (0.2791 ×3), (3.4, 1.2, −22.5) | (5.4, ±2.3, −44.0) |
| `SM_YouArm` | robot's left; straight | (0, 0, −90), (0.2798 ×3), (0.7, −1.5, −22.4) | (0, 0, −90), (−0.2798, 0.2798, 0.2798), (0.7, 1.5, −22.4) | (2.9, ±1.3, −42.7) |

- **The roll on the two bent arms hangs them:** Anthropic's arm hangs with its elbow a little bent forward and the mitten down; SpaceXAI's with the thumb pointing forward. Both checked in the preview.
- **`HandSocket` stays at (0, 5, −44)**: every hand center above is within 5 cm of it (Meta's hand sits 5 cm forward).

### The shoulders: move the pivots out

The model bodies are wider than T79's engine shapes at the shoulders, so at today's pivots the arms sink into the body (Anthropic's half-buried at y 29 in a first try). The preview used these pivots (`SetPersona`'s `_sy`), from each body's half-width at and below the shoulder plus a little of the arm's thickness:

| Bot | `_sy` today | Suggested | Why |
|---|---|---|---|
| OpenAI | 19 | **24** (the preview's 30 was too far) | At 30 the knit arms float clear of the narrow sweater. At about 24 they cover the body's own sleeve stubs (T81). |
| Anthropic | 29 | **40** | The egg is 37 cm half-wide below the shoulder. |
| SpaceXAI | 30 | **35** | |
| Meta | 29 | **30** | |
| Me | 33 | **35** | |

`_sz` (the shoulder heights 80, 76, 74, 86, 94) can stay. T75's poses should be checked with the new arm lengths and pivots, as T81 said.

### Faces and sockets (estimates from the geometry; T82 and T83 check them in close-ups)

- **Round head:** its screen is a recess about 6 cm deep, from z about 114 to 139 and about ±28 wide, its floor at x 25.8 and the rim at x 32. T79's face expects a screen with the eyes at (33, ±11, 135). So **`Face` on the round head should move about (−6, 0, −7)** to put the eyes and mouth in the recess, and **T79's `Visor` should be hidden on the round head**: its front (x 36) would stand out of the recess as a dark bump. The brows (z 144) would sit on the shell above the recess.
- **Meta's head:** nose tip at (28.9, 0, 123.9), as T80's (29.5, 0, 124). The face is flatter than T80's sphere: at eye level its surface is at x 22.6, and the model's closed eyes are at about z 130. T80's glasses (on `Rig` at x 31, z 134) would float about 8 cm in front of the face; move them back about 7 cm and down about 3, and `Face` (−4, 0, −1) about (−10, 0, −4). The head's crown is at 158, so `HeadSocket` (0, 0, 158) at 0.9 can stay.
- **My box head:** its front is at x 23.4 (T80's at 28). The eye slots are 12.3 wide × 15.7 tall, centered at (23.3, ±12.6, 134.7). They are taller than T80's 14 × 9 slots and 1.6 cm further apart. **`Face` (−7.5, 0, 3) becomes about (−11.6, 0, −0.4)** so the eyes sit behind the slots, bulging 2 cm. The marker mouth lands at x 24.3, 0.9 cm proud of the box front. Lid at 158, so `HeadSocket` (−2, 0, 162) at 1.1 should hold; check that the wig's corners still clear the narrower box (47 deep, not 56).
- Labels (z 228), toppers, halo and the stalk are untouched: every head's top stays at 158.

## 3. The material, and which reads better

### `M_CastModel` (Substrate Slab, `/Game/NHOS/Stage/Materials/M_CastModel`)

| Parameter | Kind, default | What it does |
|---|---|---|
| `BaseTex`, `NormalTex`, `RoughTex` | textures (the round head's by default) | the model's own maps |
| `Color` | vector, (1, 1, 1) | the seat color, multiplied into the texture by `TintAmount`. **The name `ResetLook` and `SetCut` already set on every `seat` part.** |
| `TintAmount` | scalar, 0 | 1 on the white head shell (`MI_RoundHead`), so the shell takes each seat color and its dark screen stays dark; 0 on every textured part, which carries its own color |
| `Cut` | scalar, 0 | 1 = the cut: the texture desaturated, times `CutTint` |
| `GrayFromColor` | scalar, 0 in the master, **1 in every `MI_` here** | when 1, a `Color` with no saturation (the cut's 0.16 gray) also counts as cut. Every seat color is strongly saturated, so a seat color never trips it. |
| `CutTint` | vector, (0.25, 0.25, 0.25) | how dark the cut goes |
| `Rough` | scalar, 0.85 | the clay roughness |
| `RoughFromTex` | scalar, 0.5 | how much of the texture's roughness mixes in |
| `NormalAmount` | scalar, 1 | 0 flattens the normal map |

It compiles with no warning. **With `GrayFromColor` on, today's `ResetLook` and `SetCut` loops work on these instances unchanged:** tag a part `seat` and the cut grays it (checked: the third robot in each pair shot is the textured version with `Color` set to SetCut's gray). Each `MI_<Part>`'s own `Color` is its bot's seat color (the round head's is OpenAI's), so an untagged part looks right too. If T82 would rather drive the cut by hand, set `GrayFromColor` 0 and add `SetScalarParameterValueOnMaterials "Cut" 1` / `0` to the same two loops.

### The comparison

Pairs on the stage under its own lights (my editor's unsaved copy of `L_Stage`, the five robots moved out of shot, then put back; nothing saved). Left: the textured models on `M_CastModel`. Middle: the same meshes on `M_Clay`: `MI_Clay_Seat` in the seat color for the seat parts, and T79's and T80's own instances for the rest (`MI_Clay_Knit` on OpenAI's arms, `MI_Clay_Doll` on Meta's head and arms, `MI_Clay_Cream` on my sleeves, `MI_Clay_Glove` and `MI_Clay_Tape` on my box head's inside and tape). Right: textured, in the cut state.

Screenshots (not in git), in `/Users/personal/Projects/AIMegaJam2026/Local/art/T82prep/`:

- `all_pairs.png`: all five front pairs, stacked
- `pair_openai.png`, `pair_anthropic.png`, `pair_spacexai.png`, `pair_meta.png`, `pair_you.png`: front, 1.3 m up, from 5.6 m
- `pair_<bot>_34.png`: three-quarter views at the suggested pivots (OpenAI's at 30)
- `facing_1.png`, `facing_2.png`: the yaw test (four turned copies of each part)

**Recommendation for step 3: the textured `M_CastModel`.** It reads better on every bot. The texture carries what makes each bot read as its concept: OpenAI's gray cable-knit turtleneck and cream belly, Anthropic's cream belly and buttons, SpaceXAI's belly and steel springs, Meta's royal-blue tee (closer to meta.png than the seat blue), my tape strips, bottle caps, jeans and sneakers. On `M_Clay`, each part is one flat color: the bellies, the buttons, the sweater, the tape and the jeans vanish, and every bot turns into a single-color blob. `M_Clay`'s thumbprint noise also looks like frost on these meshes, because it scales with local position and these meshes are 190-unit models scaled to 0.25 to 0.5. A clay version would need about 0.4 × `ThumbScale` in its own instance. The textured models still read as matte clay under the stage light. The one cost: on the cut, the whole textured part goes gray (Meta's skin-colored arms and my jeans included, if they're tagged), where T79's cut left the cream parts cream. Tag only the parts that should gray.

## 4. What's wrong with a part

- **Meta's head** (as T81 said): a realistic bald mannequin with closed eyes. At the stage's size it reads as a doll more than as meta.png's android, and its neck is long and thin above the tee. T80's glasses hide the eyes. The faint blemish under the nose doesn't show at this size. Usable; T83 and my person may want a redo.
- **Meta's arm:** its blue sleeve cap at the shoulder matches the tee's sleeve; fine in the shots.
- **OpenAI's body** has sleeve stubs with little hands at its shoulders (T81). With the pivot at about 24 the real arms should cover them; at 30 they show as a second pair of cuffs.
- **OpenAI's arm** is chunky (20 × 15 cm at this length) next to the narrow sweater; scale X and Y to about 0.8 if it looks heavy in a close-up.
- **My box head** is 64 cm wide and slightly wider than the body box (61); fine for a costume. Its eye slots show the dark cardboard inside until the eyes go in.
- **Anthropic's arm** is modeled raised and pointing; the roll hangs it, with the elbow bent a little forward. It looks natural.
- No holes or stray pieces showed on any part (T81 checked closed meshes; the preview agrees).

## 5. What T82 and T83 still have to do in `BP_Robot`

1. Put the meshes on components under the parents above (the head shell where `RHead` is; Meta's and my heads where `MHead` and `BoxHead` are; the bodies on `Rig`; one arm under each pivot), with the manifest's transforms and the `MI_` materials (`SM_YouHead` keeps its three `M_YouHead_*` slots, or takes the clay instances for its paint slot so it is tagged `seat`).
2. Tag the seat parts `seat` (the head shell, the bodies, my box head's paint slot): `ResetLook` tints the shell and `SetCut` grays them, with no graph change (`GrayFromColor`).
3. Move the arm pivots (`_sy`) as in part 2, hide `Visor` on the round head, and move `Face` (and Meta's glasses) as the estimates say, checked in close-ups.
4. Keep the engine parts T82 and T83 list (`Face` and its LEDs, the glasses, the ring, the halo, the warning light, the bolt, the collar, the ear pods, the nose and teeth, Meta's chain, my scarf, the ping-pong ball). Delete the engine shapes the models replace only after the check passes.
5. **The cook:** once `BP_Robot`'s components reference the meshes, they cook through the reference. If T82 loads any of them by soft path or name at run time instead, add this line to `Config/DefaultGame.ini` under `[/Script/UnrealEd.ProjectPackagingSettings]`, beside T45's lines:
   `+DirectoriesToAlwaysCook=(Path="/Game/NHOS/Stage/Cast")`
6. `Docs/Assets.md`, `Docs/Plan.md`, `Docs/DevLog.md`, the task files and `costumes.json` are T82's and T83's to update. This prep changed none of them.

## Unreal MCP notes from this prep

- `call_tool` takes `toolset_name` and `tool_name` as separate arguments. Inside `execute_tool_script`, `execute_tool` takes the full dotted name. The sandbox's dicts reject `.get(key, default)`; use `[]`.
- `AssetTools.find_assets` needs `folder_path` and `name` (pass `""`).
- `ObjectTools.set_properties` with `{"OverrideMaterials": [paths]}` on a placed actor's `StaticMeshComponent` sets its materials.
- A single-input material expression (Desaturation, ComponentMask, Saturate, OneMinus) connects with input name `""`. Desaturation's input is not called "Input".
- `CaptureViewport` returns `returnValue.image.data` (base64 PNG).
