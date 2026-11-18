# T103 build sheet: the new cast's models, ready to import

Back to [T103](T103.md). Written by the T103 prep session on 2026-11-18. That session did T103's steps 1 to 3 without the editor: it read the old cast's records, generated every part with Hyper3D Rodin, checked each one against its concept and got my person's OK on the sheet. T103's own session does steps 4 to 6 (import, swap, check in the game, record). It also writes `Docs/Assets.md`, `Docs/Art/Cast/README.md`, `T103.md` and the plan.

Everything here is measured from the files: the GLBs, the approved turnarounds, and the old cast's `Docs/CastArt/manifest.json` and `Graphs/BP_Robot/`. The prep made no editor read. The questions only the editor can answer are under "Open questions".

## What is where

- **The approved sheets:** [`Docs/Art/Cast/models_sheet.png`](../Art/Cast/models_sheet.png) shows each robot as concept, turnaround, then the assembled model from the front, three-quarter and side. My person approved all five on it on 2026-11-18 ("Approve all five"). [`models_parts.png`](../Art/Cast/models_parts.png) turns every part through four views.
- **One folder per part:** `Docs/Art/Cast/<character>/<part>/`, with `<character>` one of `openai`, `anthropic`, `spacexai`, `meta`, `you`, and `<part>` one of `head`, `body`, `arm`, plus `meta/glasses`. Each folder holds:
  - `model.glb`: the model, with its textures embedded.
  - `texture_diffuse.png`, `texture_normal.png` and `texture_metallic_roughness.png`: the same three 2048² maps as loose files. The agentic box head has none.
  - `reference_front.png` (and `reference_side.png`): the crop sent to Rodin. A text-only part has none.
  - `thumbnail.png` (front view) and `turntable.png` (front, right, back, left).
  - `mesh_stats.json`: triangles, separate pieces, open edges and the bounding box.
  - `log.json`: the tool, settings, prompt, generation id, upload ids and crop spec, the dropped tries and why, and a `suggested_fit` (the numbers in "Sizes" below).
- **The frame of every GLB:** glTF as exported. Metres, +Y up, and **the part faces +Z**. Rodin scales each model's longest side to about 1.9 m and centres it on the origin. The agentic box head comes at its own scale (0.42 m wide). Check each part's yaw after import, as T82 did, because the importer's axis change is not checked here. An arm hangs along −Y with its shoulder end at the top.
- **The texture maps follow glTF rules:**
  - `texture_metallic_roughness.png` packs roughness in **G** and metallic in **B**. Its R is 255.
  - `texture_normal.png` is **OpenGL** (+Y), so tick *Flip Green Channel* on the loose PNG. A material made by the glTF importer may handle that already.
  - Metallic is near 0 everywhere except Meta's chain (see Findings).
- **Tools:** the prep's GLB reader (`glb.py`: stats and OBJ preview), SceneKit turntable (`render.swift`), assembler (`assemble.swift`, with its placements in `asm_*.json`) and crop tool (`crop.swift`) are in the shared notes folder of the dispatcher's session group, `T103-prep-tools/`, not in git. The scratchpad copies are gone once the Mac restarts.

## The parts

All parts come from **Hyper3D Rodin** on my person's Business plan (T81's license finding: ship it and list it as ours, made with Hyper3D Rodin). Settings, unless a row says otherwise:

- `rodin_generate`, `Gen-2.5-Medium`, `Raw` mesh, 15,000 triangles, GLB.
- The PBR file `base_basic_pbr.glb`. The "shaded" one has baked light.
- `texture_delight` per row ("de-lit").

Meshy wasn't used: Hyper3D did every part and costs far less per call.

**Why Hyper3D:** T81's method, proven on the last cast. It's the cheapest (about 0.5 credit a call), and it gives a closed 15,000-triangle part with PBR maps. It also takes a front and a side view of the same part as one input (two `reference_upload_ids`), which the heads used.

| Part | Generation id | Input | De-lit | Triangles, pieces | What to know |
|---|---|---|---|---|---|
| openai/head | `33c56d9a-42f4-4d5a-b045-e0c21a3d6736` | front + side crops | yes | 15,000, 1 | Pale sky blue helmet head, cream ear pods baked in, a blank black oval screen **recessed** into the front, a small neck stub. |
| openai/body | `1278e041-8aeb-46c0-86f9-fabd30dda773` | front crop | no | 15,000, 1 | Gray knit sweater with ribbed hem and gold collar ring, pale blue legs and feet. Faint sleeve shapes on the shoulders and sides: the arms cover them. |
| openai/arm | `a50b1fd2-d40e-4dde-a104-6810cff903d5` | text | no | 15,000, 1 | Straight gray knit sleeve, ribbed cuff, pale blue mitten. Symmetric. |
| anthropic/head | `fa339270-cb20-4523-8c4b-8fbcc8f1a669` | front + side crops, glasses painted out | yes | 15,000, 1 | Orange rounded head, cream ring ear pods, a blank black rounded-rectangle screen **recessed** under an orange rim. **No glasses, no antenna:** both stay engine parts. |
| anthropic/body | `0681d112-2780-4a4a-99e8-cc82fca56867` | front crop | yes | 15,000, 1 | Orange egg, cream belly, three buttons, tan collar disc on top, legs and round feet. |
| anthropic/arm | `2de3d640-1381-4c64-af50-6186834864dc` | text | no | 15,000, **3** | Stacked ribbed rings, a ball shoulder, an open four-finger hand. The ball and the top ring are separate pieces with a gap of about 0.2 cm after scaling. A redder orange than the body. |
| spacexai/head | `efade402-4142-422d-88da-3a838e0c78dd` | front + side crops | yes | 15,000, 1 | Lime ball head, cream ear pods, a dark visor band, **the long cream nose baked in**. No mouth: the grin stays an engine part, under the nose. |
| spacexai/body | `5245fe65-f728-448d-a220-6b2ef513db0b` | front crop | yes | 15,000, 1 | Lime ball body, tan belly with a raised lime bolt (baked in), spring neck on top, spring legs, charcoal boots. **The tan belly repeats on the back**, and there are white sockets on the sides (under the arms). My person accepted it. |
| spacexai/arm | `e90348a0-8862-4ab3-ad67-41ec48ed8cc4` | text | no | 15,000, 1 | Spring upper arm with a lime shoulder cap, lime forearm, open hand. **Thinner than the concept:** scale it about 1.3 across (X and Y in the arm's own frame), not along its length. |
| meta/head | `390fc8ca-4f8b-4a3b-9bef-a329c65bdcc1` | text | no | 15,000, 1 | Silver-gray squarish head, the black hair as one solid cap, ears, a small nose, a neck stub. **A blank face:** no eyes, mouth or glasses. A small dark dot on the forehead (texture), about where the glasses' top rim sits. |
| meta/glasses | `95bafedc-c9f1-4211-903c-28aa11bba243` | text, 8,000 triangles | yes | 8,000, 1 | Thick black square frames with temples, and two tiny white dots at the top corners (the camera lens and the recording light). Clear lenses (the frames only). Its own part, so T47's shades can hide it (`glasses` tag). |
| meta/body | `f16da075-9e98-49d6-8f4c-aede373d57ab` | front crop | no | 15,000, 1 | Black tee with the mustard band, **the gold chain baked in** (metallic), black pants, silver-gray shoes, a neck stub. A pale patch on each side under the sleeve, where the arm hangs. |
| meta/arm | `1d1f3061-0b41-44fd-a6d8-4a03caf7aba0` | front crop | yes | 15,000, 1 | Jointed silver arm with a hand, a little bent forward at the elbow. Modelled as the robot's **left** arm. |
| you/head | `c8987209-09d7-4ad8-b632-0af7d27a1df6` | front + side crops, smile painted out; `rodin_generate_agentic`, standard, n-gons | n/a | 27,074, 5 | A hollow teal box of 9 meshes and 4 flat materials, with no textures. **The eye slots are real holes** with the brown liner behind them. Round teal knobs on the sides, and the **bottom is open**. See Findings. |
| you/body | `d6cc9e66-8046-4264-ab52-26bfa3b4acc5` | front crop | yes | 15,000, **2** | Teal box with tape band and four bottle caps, rolled jeans, sneakers. Plain teal on the back and sides. The second piece is a 230-triangle stray bit (a glove tip from the crop) on the robot's right side, by the box's lower edge. Delete it in Modeling Tools, or leave it, since the glove hangs over it. |
| you/arm | `195a3e6a-495e-4af1-9a92-62722a11b8fc` | front crop | yes | 15,000, 1 | Red and cream striped sleeve, brown ribbed cuff, tan garden glove. A gentle curve, modelled as the robot's **left** arm. |

Per robot: head, body and two arms come to 60,000 triangles for OpenAI, Anthropic and SpaceXAI, 68,000 for Meta with its glasses, and about 72,000 for me (the agentic box head is 27,074).

### What each robot is made of now, and what the engine still makes

| Robot | Model parts (tag `seat` on all but the glasses) | Engine parts that stay | Old engine parts the models replace (delete after the check) |
|---|---|---|---|
| OpenAI (`visionary`) | head, body, arm ×2 (one mirrored) | `Face` and its LED eyes, mouth and brows | T79's ear pods and gold collar, now baked into the head and body. **The floor ring (`ring`) and the hover go**: OpenAI stands on its feet now (T95). Set `HoverZ` to 0 and hide or delete the ring. |
| Anthropic (`worrier`) | head, body, arm ×2 | `Face` and its parts; **the round gold glasses** (`glasses`, so the shades hide them); **the antenna and amber light** | the ear pods and collar |
| SpaceXAI (`overclocker`) | head, body, arm ×2 | `Face` and its parts; **the toothy grin** (mouth, teeth) under the nose | the ear pods, **the nose**, the bolt, the collar |
| Meta (`copycat`) | head, body, arm ×2, glasses (`glasses`, not `seat`) | `Face`; **the eyes**, which become pale yellow with black pupils (they were gold LEDs, `EyeColor` (1, 0.62, 0.08)); the mouth (ink); **the recording light**, an emissive dot on the glasses' top right corner | T80's head (`MHead`, `MNose`, `MEarL`/`MEarR`), its glasses and chain |
| You (`human`) | head (the box), body, arm ×2 | `Face` with my real eyes, the marker smile, **the ping-pong ball on its straw**, **the scarf** (it fills the 8 cm gap between the box and the body) | T80's ear pods (now the box's knobs). `SlotL`/`SlotR` may not be needed: the new box has its own back wall, with the brown liner behind the slots. Check the slots from the house camera. |

**The seat color.** The colors are in the textures now: each head carries its own color, unlike T82's shared white `RoundHead` that `ResetLook` tinted. So every model part goes on `M_CastModel` with `TintAmount` 0 and is tagged `seat`, only so that `SetCut` grays it. Meta's mustard is in its texture too, so T108's new seat color changes the UI and not the model. My box head's paint slot can keep T83's `MI_YouHeadPaint` (flat teal, grays on the cut). The glTF factor of its "Muted teal" material, (0.072, 0.213, 0.170) linear, is the same teal.

## Sizes, and where each part goes

The targets come from the approved turnarounds: each robot keeps its head top at **z 158**, as now, so the labels (z 228), the bubbles and the house camera's frame stay. Each part is scaled to its share of the turnaround's height. The heads come out bigger than the old cast's 70 cm shell, because the concepts have bigger heads.

`Scale` is the uniform UE scale on the imported mesh, if it imports in metres converted to cm (×100). Check it against the imported mesh's bounds. W is across (rig Y), D is front to back (rig X), H is height (rig Z). Arms hang from their top; the z range is where each part sits at that scale.

| Part | Scale | W × D × H (cm) | z range | Old part (W × D × H, z) |
|---|---|---|---|---|
| openai/head | 0.516 | 97.9 × 82.8 × 80.4 (with the ear pods; 81 without) | 77.6 to 158 | `RoundHead` 70 × 64 × 66.8, 91.2 to 158 |
| openai/body | 0.420 | 48.8 × 47.2 × 79.9 | 0 to 79.9 | 69.6 × 50.4 × 93 |
| openai/arm | 0.258 | 16.8 × 15.8 × 49.0 | 27.8 to 76.8 | 53 long |
| anthropic/head | 0.506 | 96.2 × 75.7 × 68.7 (77 without pods) | 89.3 to 158 | `RoundHead` |
| anthropic/body | 0.471 | 75.6 × 73.7 × 89.3 | 0 to 89.3 | 73.8 × 72.4 × 93 |
| anthropic/arm | 0.305 | 22.0 × 11.0 × 58.0 | 20.0 to 78.0 | 53 long |
| spacexai/head | 0.456 | 86.4 × 76.5 × 62.8 (62 without pods; the nose adds depth) | 95.2 to 158 | `RoundHead` |
| spacexai/body | 0.510 | 65.8 × 61.2 × 96.7 (to the spring neck's top) | 0 to 96.7 | 65.2 × 61.2 × 93 |
| spacexai/arm | 0.259 | 18.6 × 9.5 × 49.0 | 36.0 to 85.0 | 53 long |
| meta/head | 0.426 | 76.3 × 62.3 × 81.0 (with the neck stub) | 77.0 to 158 | T80's engine sphere (the Hyper3D head was 61.8 × 57.8 × 70.1) |
| meta/glasses | 0.352 | 66.9 × 64.3 (the temples) × 25.8 | 98.8 to 124.6 | T80's engine glasses |
| meta/body | 0.405 | 51.8 × 34.7 × 77.0 | 0 to 77.0 | 50.8 × 31.4 × 94 |
| meta/arm | 0.211 | 15.8 × 21.9 × 40.0 | 30.0 to 70.0 | 53 long |
| you/head | 1.521 | 64.5 (51.8 without the knobs) × 46.2 × 44.9 | 113.1 to 158 | 64.4 × 46.8 × 55.9, 102.1 to 158 |
| you/body | 0.552 | 56.5 × 56.9 × 104.8 | 0 to 104.8 | 61.4 × 56.8 × 100 |
| you/arm | 0.395 | 23.6 × 21.2 × 75.0 | 23.0 to 98.0 | 53 long |

- **Meta's neck:** at these numbers the head's and the body's neck stubs stack into a long neck. In the preview the head sat about 7 cm lower (bottom at z 70) to match the concept's short neck. Lower it until the chin meets the chain.
- **The arms' lengths change:** Meta's arms get shorter, from 53 to 40, and mine longer, 75. Check T75's gestures and T79's fold and cheer on each, as T82 said.

### Shoulders (`ArmPivotL`/`ArmPivotR`) and `HandSocket`

The shoulders are measured on the turnarounds at the arm's top, centred in the sleeve. `HandSocket` rides on the right pivot, at the hand's centre, measured on each arm model at the scale above (down from the arm's top; forward is rig +X).

| Robot | Pivot now (y, z) | From the turnaround (±y, z) | Hand centre below the arm's top | Hand forward / sideways |
|---|---|---|---|---|
| OpenAI | ±24, 80 | ±28.5, 76.8 | 44.9 | 0 / 2.4 |
| Anthropic | ±30, 76 | ±41, 78 | 52.1 | 0.7 / 0 |
| SpaceXAI | ±35, 74 | ±38, 85 | 44.1 | 0 / 0 |
| Meta | ±27, 82 | ±29, 70 | 36.4 | **10.8 forward** (the bent elbow) / 0.9 |
| You | ±34, 94 | ±33, 98 | 67.9 | **8.3 forward** (the curve) / 5.5 |

- Measure each body's half-width at the shoulder from its vertices before you take these numbers (T82's decision 5). Anthropic's egg is 75.6 cm wide, so its arms sit far out.
- Every arm is modelled straight down except Meta's and mine. Mirror the other side with a negative scale, as T82 and T83 did. Meta's and my arm are modelled as the robot's **left**; the three text-only arms are symmetric.

### The face on each new head

Measured on the front of each turnaround, with the head top at z 158 and the head centred at y 0. A recessed screen sits a few cm behind the head's front: read the recess floor from the vertices (`ProceduralMeshLibrary.get_section_from_static_mesh`, T82's finding 4) and put `Face` (or `Visor`) in it. Then update `FaceRest`'s ellipsoids (`ScrC`/`ScrR`/`ShC`/`ShR`) and `FaceParts`' per-head numbers (`BrowMaxZ`, eye limits, `MouthDX`/`MouthDZ`), as T75's "For later tasks" says.

| Head | Screen or face area | Notes |
|---|---|---|
| OpenAI | Black oval screen, z 93 to 138, half-width 33 (centre z 115.6) | The old screen was z 102.5 to 146.7, half-width 27.9: the new one is bigger and 8 cm lower. Ear pods at z 104 to 125, out to ±46. The screen is recessed under a pale blue rim. |
| Anthropic | Black rounded rectangle, z 101.5 to 143.3, half-width 32 (centre z 122) | The glasses (engine) sit on it. In the turnaround the lens centres were at about ±19 cm, z 124. Ear pods centred about z 122. |
| SpaceXAI | Visor band z 116.5 to 136, half-width 26 | The LED eyes go on the visor. The nose is model geometry from about z 109 to 129, sticking out about 11 cm in front of the face, so **the grin goes below the nose, about z 100 to 108**, on the lime skin, not on a screen. `ScreenX` has no screen to follow there, so treat the visor as the screen and the mouth as a flat face part. |
| Meta | No screen: a silver face. Glasses z 99 to 121, half-width 34. Eyes centred at ±16, z 111, about 11.5 cm across | Pale yellow eyes with black pupils sit behind the lenses. The nose is model geometry (about z 103). The smile (ink) goes at about z 96, 17 cm wide. Ears at z 97.5 to 112, out to ±43. The hairline is about z 133 at the front. |
| You | Eye slots centred at ±12.3, z 138, about 12.5 × 9.7 cm (wide, not tall) | The old slots were 12.3 × 15.7 cm at z 134.7. My eyes go behind them, and the marker smile goes below them on the box front, about z 118 to 127. The knobs are at z 131 to 142.5, out to ±30.6. |

### `HeadSocket` and `BackSocket`

- **`HeadSocket`:** at the top of each head, (0, 0, 158), my box at (0, 0, 158) on its flat lid. The heads are bigger and differently shaped than T47's fits assumed (the round heads are 77 to 81 cm wide without their pods, against 70; my box is 52, against 64). T104 refits every costume to these heads (T96, T104). For T103, keep the socket at each head's top and check that today's 14 headpieces don't fall through or float far off. Don't refit them.
- **`BackSocket`:** on the back of the body, at about two thirds of the body's height.

| Robot | `BackSocket` now | Suggested: about −D/2 of the body, at z |
|---|---|---|
| OpenAI | (−30, 0, 60) | (−24, 0, 55) |
| Anthropic | (−34, 0, 52) | (−37, 0, 52) |
| SpaceXAI | (−33, 0, 62) | (−31, 0, 62) |
| Meta | (−16, 0, 72) | (−17, 0, 55) |
| You | (−26, 0, 70) | (−28, 0, 75) |

## What to delete from the old cast

Delete these only once nothing references them and the new parts pass T103's check:

- **`Content/NHOS/Stage/Cast/`:** the old meshes, their `MI_`, `M_` and `T_` assets (the list is in `Docs/CastArt/manifest.json`):
  - `RoundHead/` (the shared shell)
  - `openai/`, `anthropic/` and `spacexai/` (bodies and arms)
  - `meta/` (body, arm, and the unused `SM_MetaHead`)
  - `you/` (head, body, arm)
- **Keep `MI_YouHeadPaint` and `T_YouHead_Paint`** if the new box head uses them for its paint slot.
- **Keep `M_CastModel`** in `Content/NHOS/Stage/Materials/`, unless T94's style guide calls for a new material.
- **The engine shapes** in the table above.
- **`Docs/CastArt/`** (T81's models, about 177 MB in LFS) and its rows in `Docs/Assets.md`: whether they go with the old assets, or stay as a record, is the T103 session's call with my person. The prep didn't touch them.

## Costs

- **25 Hyper3D calls**, of which 16 parts are kept and 9 tries dropped: about **12.5 credits** at T81's measure of about 0.5 a call, under the 20-credit cap my person OKed.
- The MCP tools report no cost per call, and T105 spent from the same wallet at the same time, so this is counted by calls, not read from the balance.
- **Meshy: 0.**
- The uploads (21 reference crops) and the downloads cost nothing.

The dropped tries are in each part's `log.json` under `tries`, with why each was dropped:

- `c0b24547` (OpenAI body)
- `e5319d9f` (OpenAI arm)
- `0b0b658f` (Anthropic arm)
- `9aa0ed72` (SpaceXAI body)
- `dbf60b7a` (SpaceXAI arm)
- `a6a2455f` and `e6c555e1` (Meta head)
- `fb090bab` (Meta body)
- `ffd444dd` (my body)

## Findings

- **`front.png` in each character's folder is not the turnaround's front half.** It is a 672 × 768 cut from the middle of the canvas, with the front view half cut off on its left. `side.png` is the right half, as `Docs/Art/Cast/README.md` says. The prep cropped from `turnaround.png` (1344 × 768, front view in x 0 to 671). Fix the README or the files in T103's commit; the prep may not edit them.
- **`texture_delight` drains gray and metal.** It made OpenAI's gray sweater near white, Meta's silver skin white and Meta's gold chain pale. Saturated clay (orange, lime, sky blue, teal) kept its color. Every gray, silver or gold part was redone without it.
- **A painted-over patch still comes back as geometry,** as T81 found. Meta's head from the turnaround, with the glasses, eyes and smile painted out, grew a gray visor plate. Text alone gave the right blank face. Anthropic's glasses painted out as a dark screen (a rounded rectangle in the screen's own black) worked, because the patch matched what was under it.
- **An arm cropped beside a body, or cut by the crop's edge, fails:** a fused body disc, a flat side or a bent malformed hand. Three of the five arms are text only, as T81 did for OpenAI.
- **A side view adds whatever is in it.** SpaceXAI's body from front and side views got its arms back. Use a side view only where nothing overlaps the part (the heads).
- **Meta's silver isn't metal in the maps.** The skin, arms and shoes are a light gray diffuse with metallic 0; only the chain has metallic in B. On `M_CastModel`, which has no metallic input (`Docs/CastArt/manifest.json` lists its parameters), Meta reads as pale gray clay. If it should shine like the concept, add a metallic or specular parameter to an `M_CastModel` instance, or a metallic texture input, and check the cut's gray on it.
- **The agentic box head:**
  - 9 meshes (front with the slots, back, crown, two side walls, two knobs, two knob discs) and 4 materials, with flat glTF base-color factors and no textures: `Muted teal · matte craft paint`, `Kraft · unpainted liner`, `Abraded kraft fibres`, `Dark pressed board`.
  - 685 non-manifold edges, where the wall panels meet. Fine for rendering, but don't build complex collision from it.
  - It is hollow with an open bottom, so the house camera can't see in, and the scarf covers the neck. Its pivot is at its centre, not its bottom.
- **The arms' rest pose:** Anthropic's hands are open and face forward, not curled as in the concept. SpaceXAI's are open, not thumbs up. T75's gestures turn the arms, not the hands, so this stays as is.
- **OpenAI's sweater** reads closest to its concept. **SpaceXAI's arms** read thin in the preview; the across-scale above fixes it.

## Open questions (the editor can answer them, the prep couldn't)

1. Does the glTF importer (Interchange in 5.8.4) bring these in at ×100 (m to cm) with +Z front turned to UE +X, or does each part need yaw 270 as T82's FBX did? Check one part, then apply the same to all.
2. Which channel does `M_CastModel`'s `RoughTex` read? T81's roughness maps were grayscale; these pack roughness in G.
3. Does `NormalTex` on the loose `texture_normal.png` need *Flip Green Channel*? Yes if the importer doesn't set it: glTF normals are OpenGL.
4. Does `Visor` stay for the round heads? Both new screens are real recesses with a black floor. T82 kept `Visor` because the old recess was shallow and uneven. Read the recess floor first.
5. With the bigger heads, does the house camera's frame still hold all five, and do the labels at z 228 still clear the heads? The heads' tops don't move (z 158), but they are wider.
6. `FaceRest`'s new ellipsoids for each head, and whether SpaceXAI's grin needs `ScreenX` at all.
