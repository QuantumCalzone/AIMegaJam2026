# T104 build sheet: the costumes' models, ready to import and fit

Back to [T104](T104.md). The T104 prep session wrote this on 2026-11-19 (Claude Opus 5.5, started by the Mac dispatcher). The prep did T104's step 2 (generate) and the part of step 1 that needs no editor. It read T96's costumes, T47's dressing, `costumes.json`, the seats in `scenes.json`, and the graph files `Graphs/BP_Robot/DressFromShow.txt`, `SetHeadpiece.txt`, `LoadCostumes.txt`, `MakeHat.txt`, `FitNum.txt`, `WatchShow.txt` and `EmoteTestInit.txt`. Then it generated one Hyper3D model per costume version, checked each against its view, and fitted each to T103's new heads in an offline preview. My person approved the models and the first-guess fits on 2026-11-19 ("Approve all"), after two rounds of notes on the fits. T104's own session does steps 3 to 8: import, fits in `costumes.json`, `SetHeadpiece`, `costume_test`, fit by eye, clean-up, and the records (`Docs/Assets.md`, `Docs/Art/Costumes/README.md`, the design doc, `T104.md`, the plan).

Everything here is measured from the files: the GLBs, T96's views and T103's head GLBs in `Docs/Art/Cast/`. The prep made no editor read and changed no asset, data file or graph. Questions that only the editor, or T103's heads in the game, can answer are under "Open questions".

## What is where

- **The approved sheets** are in `Docs/Art/Costumes/`:
  - [`models_sheet_round.png`](../Art/Costumes/models_sheet_round.png) and [`models_sheet_cube.png`](../Art/Costumes/models_sheet_cube.png): each model's turntable next to T96's view.
  - [`models_fit_preview_a.png`](../Art/Costumes/models_fit_preview_a.png) (the hats) and [`models_fit_preview_b.png`](../Art/Costumes/models_fit_preview_b.png) (the rest): each costume on T103's five robots, from the front and at three-quarter.
  - The preview is SceneKit, not the game. Anthropic's gold glasses, an engine part, are stand-in rings there.
- **One folder per version:** `Docs/Art/Costumes/<costume>/<version>/`, where `<version>` is `round` (OpenAI, Anthropic, SpaceXAI and Meta) or `cube` (my robot), plus `horned_helmet_beard/beard`. Each folder holds:
  - `model.glb`: the model, with its three textures embedded.
  - `thumbnail.png` (front) and `turntable.png`: front, its left side, back, its right side.
  - `reference_front.png`: the image sent to Rodin. A text-only model has none.
  - `mesh_stats.json`: triangles, pieces, open edges and the bounding box.
  - `cavity.json`: ray-cast depth maps of the openings, from the front and from below.
  - `log.json`: tool, settings, prompt, generation id, upload id, the dropped tries and why, and `preview_fit` (the preview numbers per head, in the preview's world frame).
- **Tools.** The prep's tools are in the shared notes folder of the dispatcher's session group, `T104-prep-tools/`, not in git:
  - `glb.py`: the GLB reader.
  - `render.swift`: the turntable renderer.
  - `cavity.py`: the opening ray-caster.
  - `fitprev.py` and `fitview.swift`: the fit preview, with its rule table.
  - `draft.py`: turns the preview's fits into the `costumes.json` draft below.
  - `rows.swift` and `cut.swift`: the sheets and the crops.
  - `heads.json`: T103's heads measured in the rig frame.

## The models

All 21 kept models are from **Hyper3D Rodin** on my person's Business plan (T81's license finding: ship them and list them as ours, made with Hyper3D Rodin). Settings for every one:

- `rodin_generate`, `Gen-2.5-Medium`, `Raw` mesh, 15,000 triangles, GLB.
- The PBR file, `base_basic_pbr.glb`.
- `texture_delight` off.

**Why Hyper3D, not Meshy.** It's T103's and T105's method in this project. It costs about 0.5 credit a call, several times less than Meshy, and it gives a closed 15,000-triangle model with PBR maps. My person OKed a 20-credit cap.

| Version | Generation | Triangles, pieces | glTF size x × y × z (m) | bbox centre (m) | MB |
|---|---|---|---|---|---|
| `hood/round` | `c8d21c04` | 15,000, 1 | 1.44 × 1.88 × 1.44 | [0.001, 0.004, -0.0] | 6.0 |
| `dark_shades/round` | `e94ccd04` | 15,000, 1 | 1.89 × 0.61 × 1.90 | [0.0, 0.0, 0.001] | 6.3 |
| `top_hat/round` | `c3bd0895` | 15,000, 1 | 1.75 × 1.90 × 1.74 | [-0.0, -0.001, -0.003] | 7.1 |
| `bob_wig/round` | `0c3f6967` | 15,000, 1 | 1.85 × 1.78 × 1.90 | [-0.0, -0.001, 0.001] | 7.4 |
| `ball_cap/round` | `7693a100` | 15,000, 1 | 1.22 × 0.99 × 1.90 | [0.0, -0.002, -0.002] | 6.3 |
| `wide_brim_hat/round` | `fd19d2bf` | 15,000, 1 | 1.82 × 0.65 × 1.90 | [-0.001, -0.001, -0.0] | 6.7 |
| `saucepan_helmet/round` | `2786a4e0` | 15,000, 1 | 1.29 × 0.62 × 1.90 | [0.001, -0.0, -0.001] | 6.9 |
| `wizard_hat/round` | `85dac385` | 15,000, 1 | 1.83 × 1.64 × 1.90 | [-0.002, -0.0, -0.001] | 6.5 |
| `tiara/round` | `50cfb236` | 15,000, 1 | 1.90 × 1.53 × 1.86 | [-0.0, 0.0, -0.001] | 8.8 |
| `fedora/round` | `fce31b05` | 15,000, 1 | 1.65 × 0.82 × 1.89 | [-0.0, 0.0, 0.002] | 6.5 |
| `horned_helmet_beard/round` | `3f2b2a2d` | 15,000, 1 | 1.90 × 1.19 × 1.34 | [0.0, 0.0, -0.001] | 7.6 |
| `horned_helmet_beard/beard` | `9297198f` | 15,000, 1 | 1.90 × 1.83 × 1.41 | [0.001, -0.003, -0.001] | 8.6 |
| `dino_hood/round` | `73caa96b` | 15,000, 1 | 1.42 × 1.90 × 1.65 | [0.001, -0.001, 0.001] | 7.3 |
| `beanie/round` | `aced02d3` | 15,000, 1 | 1.73 × 1.89 × 1.73 | [0.0, 0.002, -0.001] | 9.3 |
| `hood/cube` | `45d6c927` | 15,000, 1 | 1.76 × 1.90 × 1.12 | [0.001, -0.002, -0.0] | 6.8 |
| `bob_wig/cube` | `92ca5706` | 15,000, 1 | 1.90 × 1.39 × 1.89 | [0.0, -0.001, 0.002] | 6.5 |
| `ball_cap/cube` | `bd22e48b` | 15,000, 1 | 1.42 × 1.10 × 1.90 | [0.001, 0.001, 0.001] | 7.6 |
| `saucepan_helmet/cube` | `8aaec10b` | 15,000, 1 | 0.90 × 0.53 × 1.90 | [-0.0, 0.0, -0.001] | 5.6 |
| `horned_helmet_beard/cube` | `b9cba460` | 15,000, 1 | 1.79 × 1.89 × 1.83 | [-0.001, 0.002, -0.001] | 6.3 |
| `dino_hood/cube` | `f9c5df4e` | 15,000, 1 | 1.20 × 1.79 × 1.90 | [0.0, 0.0, -0.002] | 7.2 |
| `beanie/cube` | `2d5c3ce6` | 15,000, 3 | 1.90 × 1.53 × 1.18 | [-0.002, 0.002, -0.001] | 7.4 |

**The frame of every GLB.** glTF as exported: metres, +Y up, and **the costume faces +Z** (the hood's opening, the dino's mouth, the cap's peak). Rodin scales the longest side to about 1.9 m and centres the bounding box on the origin; the table's centres are all within 4 mm of it. So the pivot is the bounding box's centre, and every number in the draft below assumes that pivot.

**What each model is, and what to know:**

- `hood/round`: **a cowl with no cape** (text only, generation `c8d21c04`), with a wide, deep face opening (93 cm wide at 1:1, 83% of its depth deep) and a short rolled collar at the neck.
  - Why not `pick.png`: the take made from it (`a8129277`) has a cape twice the hood's width. At a size whose hood holds these 80 cm heads, that cape is about 1.7 m wide and the head still stuck out of the hood.
  - My person approved the cowl. Their alternative was a short capelet as a second part, and none was made. A seat's color now shows on the cowl, and the body below it shows its own.
- `hood/cube`: a square hood with a square face opening and a short cape (text, from the cube panel of `hood/fit_sheet.png`). The opening is only about 29 cm deep at its fit scale; the box head (46 cm deep) goes through it and hides inside the closed hood. Its cape is about 1.5 m wide at the fit scale, so check it against my arms' gestures (T75).
- `horned_helmet_beard`: **three parts, two versions plus one shared extra.**
  - `round`: the round helmet with its headband ring, made from `pick.png` with the beard cut off.
  - `cube`: a tall square helmet (text, from the cube panel of the fit sheet). Its fit squashes it to 0.62 of its height, so it sits above the eye slots.
  - `beard`: the beard alone (from `pick.png`). Each robot has its own beard fit, so the beard hangs in front of the face below every mouth, as T96's note asks. It can also take its own ginger color.
  - The beard is a shell, open at the back.
- `dino_hood/round`: **a rounded dino head with a wide, short mouth** (text only, generation `73caa96b`), like T96's fit sheets, not `pick.png`. The take from the pick (`6919e1f2`) had a tall, narrow mouth and was 1.9 m long front to back; at a size that holds these heads, it reached down to about z 40, over the arms.
- `dino_hood/cube`: from `view_cube.png`. The round dino would also fit the cube, if T104 wants one model fewer.
- `saucepan_helmet`:
  - `round`: a pot turned bottom up, with its handle along +Z (forward). The fit turns it 90° so the handle points out to the robot's right, and moves the pivot so the pot, not its bounding box, is centred on the head.
  - `cube`: a square pan, **open side up** as in `view_cube.png`. Its fit adds a roll of 180°.
- `tiara/round`: a ring with five ball-tipped points across the front half; the back half is a plain band.
- `beanie/cube`: 3 pieces. The pompom and a small bit are separate from the body.
- `bob_wig`: both versions are hollow underneath. The round wig's inside is 85 to 95% of its height deep.
- `ball_cap/cube`: the box crown is solid underneath, so it sits on the lid.
- **Hats:** the top hat, the fedora, the round ball cap and the wide-brim hat are hollow underneath (the top hat's crown is hollow up to 95% of its height). The beanie and the cube cap are solid lumps that sit on, or around, the head.
- **Colors:** the textures' colors don't matter. The models come in clay colors (the wig is salmon, the hoods mint), and each costume is tinted to its role's color by `M_Clay`, as in T47.

**Texture maps** (embedded in each GLB, 2048² each): `texture_diffuse.png`, `texture_normal.png` and `texture_metallic_roughness.png`. They follow glTF rules:
- Roughness is in G and metallic in B.
- The normal map is OpenGL (+Y), so tick *Flip Green Channel* if it's imported as a loose texture.
- Metallic is near 0 on all of them.

The prep didn't extract them as loose files, to save LFS space: `glb.py` writes them out on demand.

**Triangles per robot:** each costume is 15,000 triangles, and the dwarf with its beard is 30,000.

## Import (T104 step 3)

- **Where:** `Content/NHOS/Stage/Costumes/<costume>/`, named as in the draft: `SM_<Name>_Round`, `SM_<Name>_Cube`, `SM_Beard`. For example `SM_TopHat_Round` and `SM_HornedHelmet_Cube`.
- **Scale:** the glTF importer should bring metres in as cm (×100). Check one mesh's bounds against the table: `top_hat/round` should come in at about 175 × 190 × 174 cm before any scale.
- **Facing:** bake the rotation at import so **every mesh faces +X, with +Z up**. The draft's `yaw` and `roll` are only the extra turns on top of that: 90 for the saucepan, 180 for `ball_cap_back` and the cube pan's 180 roll. T47's old FBX headpieces needed `yaw` 270 on the component instead. If T104 keeps that way, add 270 to every `yaw` and swap `scale3`'s first two numbers.
- **Material:** put T47's clay on every mesh (`MI_Clay_Neutral` on `M_Clay`, so `SetHeadpiece` sets its `Color`). The beard gets the same clay; the `extra` part sets its own color.
  - Whether to keep the imported normal map as clay detail is the T104 session's call. `M_Clay`'s inputs aren't listed anywhere the prep could read.
  - The imported diffuse and metallic-roughness textures can be deleted if `M_Clay` doesn't use them.
- **Collision:** none. `MakeHat` already sets `NoCollision`. Lightmap UVs aren't needed (`r.AllowStaticLighting=False`).
- **Cooking:** `Config/DefaultGame.ini` cooks `/Game/NHOS/Stage/Headpieces` (T47). Add `/Game/NHOS/Stage/Costumes`, because a mesh named only in `costumes.json` is referenced by nothing, and drop the old line when the old folder goes.
- **No new socket or attach point is needed.** Every part, the beard included, hangs on `HeadSocket`.

## The fits (T104 step 4)

**How the numbers were made.** The prep placed T103's five robots as `Docs/tasks/T103-build.md` "Sizes" gives them, each head's top at z 158. It used T103's face table for each head's eyes and mouth, and measured each head's width and front surface from its GLB (`heads.json`). Then it fitted each costume by a rule (width as a multiple of the head's crown width, an anchor height, a forward offset). It tuned the rules by eye on the preview until my person's notes were met:

- The saucepan is centred.
- Meta's and Anthropic's glasses sit in front of the bob wig and the cowl.
- The beard hangs in front of the face.
- The shades stand far enough out not to clip into Anthropic's screen rim or my box.
- Every head is inside its cowl, wig and dino hood.

**Assumptions to check in the editor:**

1. `HeadSocket` sits at each head's top (0, 0, 158 in the rig) with scale 1. That's what T103-build.md recommends; T80's old sockets on Meta and me had scale 1.1.
2. Meta's head top is z 158, as in T103's "Sizes" table. T103's preview lowered Meta's head 7 cm. The fits are relative to the socket, so they hold either way, as long as the socket stays on the head's top.
3. Each mesh pivot is its bounding-box centre, as imported.
4. The rig frame is UE's: X forward, Y the robot's right, Z up.

**The draft below is a first guess for step 6, not a finished fit.** Read `scale` as the uniform scale on a mesh imported at ×100, and `scale3` as the per-axis scale (X forward, Y across, Z up) where a fit needs one.

### `costumes.json`, new form (draft, not in the data file)

Each costume has:
- `meshes`: one mesh per version.
- `test_color`: for `costume_test`, the color of T96's concept role.
- `fit`: one entry per persona id (`visionary` OpenAI, `worrier` Anthropic, `overclocker` SpaceXAI, `copycat` Meta, `human` me).

A fit has these fields:
- `mesh`: which version.
- `scale`, plus `scale3` [X, Y, Z] when it isn't uniform.
- `x`, `y`, `z`: the pivot under `HeadSocket`, in cm.
- `yaw` and `roll` (optional).
- `top`: the costume's top above the socket, for T47's stalk and label lift. 0 leaves them.

`horned_helmet_beard` adds `extra`: a second mesh with its own fixed color and its own fit per persona. `ball_cap_back` is `ball_cap` turned 180° with `x` flipped. The old `on` override is gone: every robot has its own fit now.

```json
{
  "_readme": [
    "The costumes the robots wear (T47, remade by T104 from T96's concepts). Each seat in scenes.json names one by its id ('headpiece') and gives its color ('color', sRGB hex).",
    "meshes: the static mesh object path of each version: 'round' (OpenAI, Anthropic, SpaceXAI and Meta) and 'cube' (my robot), loaded by BP_Robot.SetHeadpiece as a soft reference. Every mesh has MI_Clay_Neutral, and SetHeadpiece sets its Color.",
    "fit: one entry per persona id. mesh names the version; scale (or scale3 [x, y, z], which wins), x, y, z, yaw and roll (degrees, optional) are the Hat component's relative transform under the robot's HeadSocket (cm). Every mesh faces +X as imported.",
    "top: the costume's top above HeadSocket, in cm. The antenna stalk, the toppers and the name label rise so they poke out of it. 0 leaves them where they are (the tiara and the shades).",
    "extra: optional, a second mesh on HeadSocket with its own fixed color and its own fit per persona (the dwarf's beard).",
    "test_color: the color costume_test (Local/switches.json) shows it in.",
    "The game never sends this file or a seat's headpiece and color to the AIs."
  ],
  "costumes": {
    "hood": {
      "meshes": {"cube": "/Game/NHOS/Stage/Costumes/hood/SM_Hood_Cube.SM_Hood_Cube", "round": "/Game/NHOS/Stage/Costumes/hood/SM_Hood_Round.SM_Hood_Round"},
      "test_color": "#5E7A3A",
      "fit": {
        "visionary": {"mesh": "round", "scale": 0.6531, "scale3": [0.6531, 0.6531, 0.5486], "x": -4.0, "y": 0.0, "z": -43.9, "yaw": 0, "top": 8.0},
        "worrier": {"mesh": "round", "scale": 0.6826, "scale3": [0.6689, 0.6826, 0.5051], "x": -9.0, "y": 0.0, "z": -39.8, "yaw": 0, "top": 8.0},
        "overclocker": {"mesh": "round", "scale": 0.648, "scale3": [0.6804, 0.648, 0.4925], "x": -4.0, "y": 0.0, "z": -39.6, "yaw": 0, "top": 7.0},
        "copycat": {"mesh": "round", "scale": 0.6281, "scale3": [0.6281, 0.6281, 0.6407], "x": -9.0, "y": 0.0, "z": -52.7, "yaw": 0, "top": 8.0},
        "human": {"mesh": "cube", "scale": 0.8529, "x": -12.0, "y": 0.1, "z": -72.7, "yaw": 0, "top": 8.0}
      }
    },
    "dark_shades": {
      "meshes": {"round": "/Game/NHOS/Stage/Costumes/dark_shades/SM_DarkShades_Round.SM_DarkShades_Round"},
      "test_color": "#1A1A1E",
      "fit": {
        "visionary": {"mesh": "round", "scale": 0.3581, "x": 11.4, "y": 0.0, "z": -38.0, "yaw": 0, "top": 0},
        "worrier": {"mesh": "round", "scale": 0.3752, "x": 10.9, "y": 0.0, "z": -34.0, "yaw": 0, "top": 0},
        "overclocker": {"mesh": "round", "scale": 0.2934, "x": 9.2, "y": 0.0, "z": -32.0, "yaw": 0, "top": 0},
        "copycat": {"mesh": "round", "scale": 0.2939, "x": 7.2, "y": 0.0, "z": -47.0, "yaw": 0, "top": 0},
        "human": {"mesh": "round", "scale": 0.3561, "x": -3.7, "y": 0.0, "z": -19.0, "yaw": 0, "top": 0}
      }
    },
    "top_hat": {
      "meshes": {"round": "/Game/NHOS/Stage/Costumes/top_hat/SM_TopHat_Round.SM_TopHat_Round"},
      "test_color": "#8A3FB8",
      "fit": {
        "visionary": {"mesh": "round", "scale": 0.4216, "x": 0.1, "y": -0.0, "z": 34.1, "yaw": 0, "top": 74.1},
        "worrier": {"mesh": "round", "scale": 0.4148, "x": 0.1, "y": -0.0, "z": 33.5, "yaw": 0, "top": 72.8},
        "overclocker": {"mesh": "round", "scale": 0.3454, "x": 0.1, "y": -0.0, "z": 26.9, "yaw": 0, "top": 59.7},
        "copycat": {"mesh": "round", "scale": 0.346, "x": 0.1, "y": -0.0, "z": 26.9, "yaw": 0, "top": 59.8},
        "human": {"mesh": "round", "scale": 0.2967, "x": 0.1, "y": -0.0, "z": 27.2, "yaw": 0, "top": 55.4}
      }
    },
    "bob_wig": {
      "meshes": {"cube": "/Game/NHOS/Stage/Costumes/bob_wig/SM_BobWig_Cube.SM_BobWig_Cube", "round": "/Game/NHOS/Stage/Costumes/bob_wig/SM_BobWig_Round.SM_BobWig_Round"},
      "test_color": "#8B4A26",
      "fit": {
        "visionary": {"mesh": "round", "scale": 0.5357, "scale3": [0.5625, 0.5357, 0.6], "x": -5.0, "y": -0.0, "z": -35.4, "yaw": 0, "top": 18.0},
        "worrier": {"mesh": "round", "scale": 0.5543, "scale3": [0.582, 0.5543, 0.6208], "x": -8.0, "y": -0.0, "z": -22.2, "yaw": 0, "top": 33.0},
        "overclocker": {"mesh": "round", "scale": 0.4877, "scale3": [0.5121, 0.4877, 0.5462], "x": -5.0, "y": -0.0, "z": -28.6, "yaw": 0, "top": 20.0},
        "copycat": {"mesh": "round", "scale": 0.4624, "scale3": [0.4855, 0.4624, 0.5179], "x": -9.0, "y": -0.0, "z": -25.1, "yaw": 0, "top": 21.0},
        "human": {"mesh": "cube", "scale": 0.3819, "scale3": [0.4583, 0.3819, 0.4392], "x": -4.1, "y": 0.0, "z": -9.5, "yaw": 0, "top": 21.0}
      }
    },
    "ball_cap": {
      "meshes": {"cube": "/Game/NHOS/Stage/Costumes/ball_cap/SM_BallCap_Cube.SM_BallCap_Cube", "round": "/Game/NHOS/Stage/Costumes/ball_cap/SM_BallCap_Round.SM_BallCap_Round"},
      "test_color": "#C8202E",
      "fit": {
        "visionary": {"mesh": "round", "scale": 0.574, "x": 8.1, "y": 0.0, "z": 11.5, "yaw": 0, "top": 39.7},
        "worrier": {"mesh": "round", "scale": 0.5646, "x": 8.1, "y": 0.0, "z": 11.0, "yaw": 0, "top": 38.8},
        "overclocker": {"mesh": "round", "scale": 0.4702, "x": 8.1, "y": 0.0, "z": 6.3, "yaw": 0, "top": 29.5},
        "copycat": {"mesh": "round", "scale": 0.471, "x": 8.1, "y": 0.0, "z": 6.4, "yaw": 0, "top": 29.5},
        "human": {"mesh": "cube", "scale": 0.3825, "x": 5.0, "y": 0.0, "z": 15.0, "yaw": 0, "top": 36.1}
      }
    },
    "wide_brim_hat": {
      "meshes": {"round": "/Game/NHOS/Stage/Costumes/wide_brim_hat/SM_WideBrimHat_Round.SM_WideBrimHat_Round"},
      "test_color": "#E3C770",
      "fit": {
        "visionary": {"mesh": "round", "scale": 0.5851, "x": 0.0, "y": -0.1, "z": 10.0, "yaw": 0, "top": 28.9},
        "worrier": {"mesh": "round", "scale": 0.5755, "x": 0.0, "y": -0.1, "z": 9.7, "yaw": 0, "top": 28.3},
        "overclocker": {"mesh": "round", "scale": 0.4793, "x": 0.0, "y": -0.0, "z": 6.6, "yaw": 0, "top": 22.1},
        "copycat": {"mesh": "round", "scale": 0.4801, "x": 0.0, "y": -0.0, "z": 6.6, "yaw": 0, "top": 22.1},
        "human": {"mesh": "round", "scale": 0.4118, "x": 0.0, "y": -0.0, "z": 12.4, "yaw": 0, "top": 25.7}
      }
    },
    "saucepan_helmet": {
      "meshes": {"cube": "/Game/NHOS/Stage/Costumes/saucepan_helmet/SM_SaucepanHelmet_Cube.SM_SaucepanHelmet_Cube", "round": "/Game/NHOS/Stage/Costumes/saucepan_helmet/SM_SaucepanHelmet_Round.SM_SaucepanHelmet_Round"},
      "test_color": "#222226",
      "fit": {
        "visionary": {"mesh": "round", "scale": 0.5805, "x": 0.1, "y": 17.8, "z": 6.1, "yaw": 90, "top": 24.2},
        "worrier": {"mesh": "round", "scale": 0.571, "x": 0.1, "y": 17.5, "z": 5.8, "yaw": 90, "top": 23.6},
        "overclocker": {"mesh": "round", "scale": 0.4756, "x": 0.0, "y": 14.6, "z": 2.9, "yaw": 90, "top": 17.7},
        "copycat": {"mesh": "round", "scale": 0.4764, "x": 0.1, "y": 14.6, "z": 2.9, "yaw": 90, "top": 17.7},
        "human": {"mesh": "cube", "scale": 0.5441, "x": 0.1, "y": 27.0, "z": 10.3, "yaw": 90, "roll": 180, "top": 24.6}
      }
    },
    "wizard_hat": {
      "meshes": {"round": "/Game/NHOS/Stage/Costumes/wizard_hat/SM_WizardHat_Round.SM_WizardHat_Round"},
      "test_color": "#8C8A86",
      "fit": {
        "visionary": {"mesh": "round", "scale": 0.5034, "x": 0.1, "y": -0.1, "z": 32.2, "yaw": 0, "top": 73.4},
        "worrier": {"mesh": "round", "scale": 0.4952, "x": 0.1, "y": -0.1, "z": 31.6, "yaw": 0, "top": 72.1},
        "overclocker": {"mesh": "round", "scale": 0.4124, "x": 0.1, "y": -0.1, "z": 24.8, "yaw": 0, "top": 58.5},
        "copycat": {"mesh": "round", "scale": 0.4131, "x": 0.1, "y": -0.1, "z": 24.8, "yaw": 0, "top": 58.6},
        "human": {"mesh": "round", "scale": 0.3543, "x": 0.0, "y": -0.1, "z": 28.0, "yaw": 0, "top": 57.0}
      }
    },
    "tiara": {
      "meshes": {"round": "/Game/NHOS/Stage/Costumes/tiara/SM_Tiara_Round.SM_Tiara_Round"},
      "test_color": "#D9DEE6",
      "fit": {
        "visionary": {"mesh": "round", "scale": 0.3103, "x": -2.0, "y": -0.0, "z": 14.8, "yaw": 0, "top": 0},
        "worrier": {"mesh": "round", "scale": 0.3052, "x": -2.0, "y": -0.0, "z": 14.4, "yaw": 0, "top": 0},
        "overclocker": {"mesh": "round", "scale": 0.2542, "x": -2.0, "y": -0.0, "z": 10.5, "yaw": 0, "top": 0},
        "copycat": {"mesh": "round", "scale": 0.2546, "x": -2.0, "y": -0.0, "z": 10.5, "yaw": 0, "top": 0},
        "human": {"mesh": "round", "scale": 0.232, "x": 0.0, "y": -0.0, "z": 16.8, "yaw": 0, "top": 0}
      }
    },
    "fedora": {
      "meshes": {"round": "/Game/NHOS/Stage/Costumes/fedora/SM_Fedora_Round.SM_Fedora_Round"},
      "test_color": "#4A4A4E",
      "fit": {
        "visionary": {"mesh": "round", "scale": 0.5343, "x": -0.1, "y": -0.0, "z": 12.9, "yaw": 0, "top": 34.8},
        "worrier": {"mesh": "round", "scale": 0.5256, "x": -0.1, "y": -0.0, "z": 12.5, "yaw": 0, "top": 34.1},
        "overclocker": {"mesh": "round", "scale": 0.4378, "x": -0.1, "y": -0.0, "z": 8.9, "yaw": 0, "top": 26.9},
        "copycat": {"mesh": "round", "scale": 0.4385, "x": -0.1, "y": -0.0, "z": 8.9, "yaw": 0, "top": 26.9},
        "human": {"mesh": "round", "scale": 0.3761, "x": -0.1, "y": -0.0, "z": 14.4, "yaw": 0, "top": 29.8}
      }
    },
    "horned_helmet_beard": {
      "meshes": {"cube": "/Game/NHOS/Stage/Costumes/horned_helmet_beard/SM_HornedHelmet_Cube.SM_HornedHelmet_Cube", "round": "/Game/NHOS/Stage/Costumes/horned_helmet_beard/SM_HornedHelmet_Round.SM_HornedHelmet_Round"},
      "test_color": "#6B6F75",
      "fit": {
        "visionary": {"mesh": "round", "scale": 0.5423, "x": 0.0, "y": 0.0, "z": 12.2, "yaw": 0, "top": 44.4},
        "worrier": {"mesh": "round", "scale": 0.5334, "x": 0.0, "y": 0.0, "z": 11.7, "yaw": 0, "top": 43.4},
        "overclocker": {"mesh": "round", "scale": 0.4443, "x": 0.0, "y": 0.0, "z": 6.4, "yaw": 0, "top": 32.8},
        "copycat": {"mesh": "round", "scale": 0.445, "x": 0.0, "y": 0.0, "z": 6.4, "yaw": 0, "top": 32.9},
        "human": {"mesh": "cube", "scale": 0.3471, "scale3": [0.3471, 0.3471, 0.2152], "x": 0.0, "y": -0.0, "z": 9.3, "yaw": 0, "top": 29.7}
      },
      "extra": {
        "mesh": "/Game/NHOS/Stage/Costumes/horned_helmet_beard/SM_Beard.SM_Beard",
        "color": "#B4532A",
        "fit": {
          "visionary": {"scale": 0.4069, "scale3": [0.2034, 0.4069, 0.4069], "x": 46.5, "y": 0.1, "z": -87.2, "yaw": 0},
          "worrier": {"scale": 0.4003, "scale3": [0.2001, 0.4003, 0.4003], "x": 43.2, "y": 0.1, "z": -78.6, "yaw": 0},
          "overclocker": {"scale": 0.3651, "scale3": [0.1825, 0.3651, 0.3651], "x": 28.0, "y": 0.1, "z": -85.3, "yaw": 0},
          "copycat": {"scale": 0.3498, "scale3": [0.1749, 0.3498, 0.3498], "x": 31.8, "y": 0.1, "z": -83.9, "yaw": 0},
          "human": {"scale": 0.2591, "scale3": [0.1295, 0.2591, 0.2591], "x": 26.8, "y": 0.0, "z": -64.7, "yaw": 0}
        }
      }
    },
    "dino_hood": {
      "meshes": {"cube": "/Game/NHOS/Stage/Costumes/dino_hood/SM_DinoHood_Cube.SM_DinoHood_Cube", "round": "/Game/NHOS/Stage/Costumes/dino_hood/SM_DinoHood_Round.SM_DinoHood_Round"},
      "test_color": "#5DA642",
      "fit": {
        "visionary": {"mesh": "round", "scale": 0.7518, "scale3": [0.7894, 0.7518, 0.5413], "x": 1.9, "y": 0.1, "z": -35.4, "yaw": 0, "top": 16.0},
        "worrier": {"mesh": "round", "scale": 0.7395, "scale3": [0.7765, 0.7395, 0.5324], "x": 1.9, "y": 0.1, "z": -34.6, "yaw": 0, "top": 16.0},
        "overclocker": {"mesh": "round", "scale": 0.6796, "scale3": [0.7136, 0.6796, 0.4893], "x": 1.9, "y": 0.1, "z": -30.5, "yaw": 0, "top": 16.0},
        "copycat": {"mesh": "round", "scale": 0.6595, "scale3": [0.6925, 0.6595, 0.4748], "x": 1.9, "y": 0.1, "z": -29.1, "yaw": 0, "top": 16.0},
        "human": {"mesh": "cube", "scale": 0.7543, "scale3": [0.8297, 0.7543, 0.6412], "x": 4.1, "y": 0.0, "z": -43.3, "yaw": 0, "top": 14.0}
      }
    },
    "beanie": {
      "meshes": {"cube": "/Game/NHOS/Stage/Costumes/beanie/SM_Beanie_Cube.SM_Beanie_Cube", "round": "/Game/NHOS/Stage/Costumes/beanie/SM_Beanie_Round.SM_Beanie_Round"},
      "test_color": "#6E7F92",
      "fit": {
        "visionary": {"mesh": "round", "scale": 0.4261, "x": 0.0, "y": 0.0, "z": 26.3, "yaw": 0, "top": 66.7},
        "worrier": {"mesh": "round", "scale": 0.4192, "x": 0.0, "y": 0.0, "z": 25.6, "yaw": 0, "top": 65.4},
        "overclocker": {"mesh": "round", "scale": 0.3491, "x": 0.0, "y": 0.0, "z": 19.0, "yaw": 0, "top": 52.2},
        "copycat": {"mesh": "round", "scale": 0.3497, "x": 0.0, "y": 0.0, "z": 19.1, "yaw": 0, "top": 52.3},
        "human": {"mesh": "cube", "scale": 0.3143, "x": 0.0, "y": -0.1, "z": 14.0, "yaw": 0, "top": 38.2}
      }
    },
    "ball_cap_back": {
      "meshes": {"cube": "/Game/NHOS/Stage/Costumes/ball_cap/SM_BallCap_Cube.SM_BallCap_Cube", "round": "/Game/NHOS/Stage/Costumes/ball_cap/SM_BallCap_Round.SM_BallCap_Round"},
      "test_color": "#E0482E",
      "fit": {
        "visionary": {"mesh": "round", "scale": 0.574, "x": -8.1, "y": 0.0, "z": 11.5, "yaw": 180, "top": 39.7},
        "worrier": {"mesh": "round", "scale": 0.5646, "x": -8.1, "y": 0.0, "z": 11.0, "yaw": 180, "top": 38.8},
        "overclocker": {"mesh": "round", "scale": 0.4702, "x": -8.1, "y": 0.0, "z": 6.3, "yaw": 180, "top": 29.5},
        "copycat": {"mesh": "round", "scale": 0.471, "x": -8.1, "y": 0.0, "z": 6.4, "yaw": 180, "top": 29.5},
        "human": {"mesh": "cube", "scale": 0.3825, "x": -5.0, "y": 0.0, "z": 15.0, "yaw": 180, "top": 36.1}
      }
    }
  }
}
```

### `scenes.json`: no change needed

Every seat's `headpiece` and `color` already match T96's role table. The prep checked all 35 seats with a script. The one difference is `favor_father` seat 2, `ball_cap_back` for "ball cap, worn backwards", which is intended. T104's step 4 can leave `scenes.json` as it is.

### `Tools/check_prompts.py`

`costume_problems` (line 998) reads `cdata["headpieces"]` and checks `mesh`, the fit numbers (`FIT_KEYS`) and the `on` override. For the new form it should check these:

- `costumes` is an object.
- Every costume has `meshes`, each value an object path on disk.
- `fit` has all five persona ids, each with `mesh` naming a key of `meshes`, `scale` above 0 (or `scale3`, three numbers above 0), numbers for `x`, `y`, `z` and `yaw`, an optional `roll`, and `top` of 0 or more.
- `extra`, if present, has a mesh on disk, a hex color and the same five fits without `mesh` and `top`.
- `test_color` is hex.
- Every seat's `headpiece` is a key of `costumes`.
- Every costume is worn by some seat. The old "no seat wears" check runs on meshes; run it on costume ids now.
- Update the docstring at line 133 to match.

## The graph changes (`BP_Robot`)

Start each from its file in `Graphs/BP_Robot/`, and commit the new file with the change. Each item names the graph, the node and the pin, as written in the DSL files today. The DSL lines are drafts: the prep couldn't compile them.

### `LoadCostumes`

- Change `(bind _h (Json|GetField _o "headpieces"))` to read the field `"costumes"`. Nothing else changes; `CostObj` keeps the object keyed by costume id.

### `SetHeadpiece`

The calls at the top (`InitLift`, `LoadCostumes`, `MakeHat`), `_has`, `ShowGlasses` and the off/unknown branch stay. Change these:

1. **The off/unknown branch and the `:CastFailed` branch** also call the new `SetExtra :On false`, which hides the beard.
2. **Replace the reads of `mesh`, `scale`, `x`, `y`, `z`, `yaw` and `top` from `CEntry`, and the whole `on` block,** with a read of this persona's fit. `FitNum` already reads a number from `CFit` with a default, so keep it:

   ```lisp
   (bind _e (Json|GetField (V CostObj) Id))
   (set CEntry _e)
   ; T104: this robot's fit (fit.<persona>) and the mesh of the version it names.
   (bind _fs (Json|GetField (V CEntry) "fit"))
   (set COn _fs)
   (if (not (Json|HasField (V COn) (Variables|Default|GetPersonaId)))
     (print (cat "NHOS: COSTUME " (cat (Variables|Default|GetPersonaId) (cat " no fit for " Id))))
     (Rendering|SetVisibility :self (V Hat) :bNewVisibility false :bPropagateToChildren false)
     (CallFunction|SetExtra :On false)
     (CallFunction|LiftTop :Lift 0.0)
     (return))
   (bind _pf (Json|GetField (V COn) (Variables|Default|GetPersonaId)))
   (set CFit _pf)
   (bind _v (Json|GetField (V CFit) "mesh"))
   (set HVer _v)
   (bind _ms (Json|GetField (V CEntry) "meshes"))
   (set CMeshes _ms)
   (bind _m (Json|GetField (V CMeshes) (V HVer)))
   (set HMesh _m)
   (set HScale (CallFunction|FitNum :Key "scale" :Def 1.0))
   (set HX (CallFunction|FitNum :Key "x" :Def 0.0))
   (set HY (CallFunction|FitNum :Key "y" :Def 0.0))
   (set HZ (CallFunction|FitNum :Key "z" :Def 0.0))
   (set HYaw (CallFunction|FitNum :Key "yaw" :Def 0.0))
   (set HRoll (CallFunction|FitNum :Key "roll" :Def 0.0))
   (set HTop (CallFunction|FitNum :Key "top" :Def 0.0))
   (set HS3 (Math|Vector|MakeVector :X (V HScale) :Y (V HScale) :Z (V HScale)))
   (if (Json|HasField (V CFit) "scale3")
     (bind _s3 (Json|GetField (V CFit) "scale3"))
     (set HS3A _s3)
     (set HS3 (Math|Vector|MakeVector :X (get (V HS3A) 0) :Y (get (V HS3A) 1) :Z (get (V HS3A) 2))))
   ```

   New variables: `HVer` (String), `CMeshes` (Json), `HRoll` (Float), `HS3` (Vector), `HS3A` (Float array). `CFit`, `COn`, `HScale`, `HX`, `HY`, `HZ`, `HYaw`, `HTop` and `HMesh` exist. Whether setting a Float array from a Json array works the way T47's Json-to-Float sets do is unchecked. If it doesn't, read `scale3` as three fields (`sx`, `sy`, `sz`) with `FitNum` instead, and change the draft to match.
3. **In `:then`:**
   - `Transformation|SetRelativeScale3D` pin `NewScale3D` takes `(V HS3)` in place of the uniform `MakeVector`.
   - `Transformation|SetRelativeRotation` pin `NewRotation`: `Math|Rotator|MakeRotator` pin `Roll` takes `(V HRoll)` in place of `0.0`.
   - After `Rendering|SetVisibility`, call `(CallFunction|SetExtra :On true)`.
   - The lift math (`_sl`, `_ss`, `_nb`, `LiftTop`) is unchanged.
   - The `print` is unchanged.

### New: `MakeExtra` and `SetExtra`

- **`MakeExtra`** copies `MakeHat`: it makes a second `StaticMeshComponent`, `Extra`, attaches it to `HeadSocket` (`KeepRelative` ×3), sets `NoCollision` and hides it.
- **`SetExtra(On)`** hides `Extra` when `On` is false, or when `CEntry` has no `extra` or no `extra.fit.<persona>`. Otherwise it loads `extra.mesh` the way `SetHeadpiece` loads `HMesh`, reads the fit with `FitNum` (with `CFit` set to `extra.fit.<persona>`, so set it after the main transform is done), sets the transform the same way, and sets `Color` from `extra.color` through `HexColor`. Log `NHOS: COSTUME <persona> extra <hex>` or `... extra mesh missing <path>`.

### `ShowGlasses`, `LiftTop`, `FitNum`, `MakeHat`

No change. `FitNum` reads `CFit`, which is now the persona's fit. The shades still hide the `glasses` tags, so Anthropic's and Meta's own glasses don't clip into them.

### `DressFromShow`

**No change.** It passes the dealt seat's `headpiece` and `color` to `SetHeadpiece`, and every seat already names a costume id.

### `WatchShow`

- First line: `(if (V CostTest) (return))`, so a show doesn't undress the robots while `costume_test` runs.

## A test switch: `costume_test` (T104 step 5)

Copy T75's `emote_test`.

- **`CostumeTestInit`**, called from `EventGraph` after `EmoteTestInit`:
  - It reads `costume_test` from `Local/switches.json` into the new Boolean `CostTest`, as `EmoteTestInit` reads `emote_test`, and returns if it's off.
  - Then it runs `LoadCostumes` and fills the new String array `CostIds` with `CostObj`'s keys. The JSON plugin's field-names node lists them; if there isn't one, use a fixed list of the 14 ids.
  - It sets `CostTestIdx` to 0 and `CostTestNext` to `Clock` + 1.5, and prints `NHOS: COSTUME TEST on ids=<n>`.
- **`CostumeTick`**, called from `TickActs` after `EmoteTick`. When `CostTest` is on and `Clock` ≥ `CostTestNext`:
  - It reads the current id's `test_color` and calls `SetHeadpiece :Id <id> :Color <test_color>`.
  - It prints `NHOS: COSTUME TEST <id>`, moves `CostTestIdx` on (wrapping), and adds `CostTestStep` (4.0 s, a new Float) to `CostTestNext`.
  - Every robot starts at index 0, so all five wear the same costume at the same time, which is what step 6's grid needs.
- **`Docs/switches.example.json`:** add `"costume_test": false`, and this sentence to its `_readme` after `emote_test`:

  > costume_test (T104): every robot wears each costume in Content/NHOS/Data/costumes.json in turn from BeginPlay, 4 seconds each, all five in the same costume at once in its test_color, with no LLM and no show needed, so each costume can be screenshot on every robot. A show doesn't dress or undress the robots while it is on. It is read once at BeginPlay. Set it back to false before a person plays.

## Costs

- **30 Hyper3D calls**, about **15 credits** at T81's measure of about 0.5 a call, under my person's 20-credit cap:
  - 21 first calls.
  - 2 dropped redos of the cube hood (`9be319d0`, `94649cf1`) and 2 of the cube helmet (`d7dfa051`, `bbedb44e`).
  - The round dino (`73caa96b`, kept) and a dropped cube dino (`270c06ca`).
  - Two round hood tries (`eca4d652` dropped, `c8d21c04` kept), and a dropped cube cowl (`14c0b8b9`).
  - The first round hood (`a8129277`) and the first round dino (`6919e1f2`) were first calls and are dropped too; the kept second takes replaced them.
- The MCP tools report no cost per call, and T106's prep spent from the same wallet at the same time, so this is counted by calls, not read from the balance.
- **Meshy: 0.** The uploads (19 reference images) and the downloads cost nothing.
- Each dropped try is in its version's `log.json` under `tries`, with why.

## Findings

- **Naming the box head makes Rodin build it.** "Made for a person with a cardboard box head" gave a hood with the box inside, and a helmet sitting on a box. "Shown on its own, nothing under it" fixed both.
- **Rodin's hoods come with a cape twice the hood's width.** Asking for "a very short capelet, barely wider than the hood" didn't change it. A cowl with "no cape, no cloak, no shoulders" did. "No cape" also turned the boxy version into a frame open on all four sides.
- **For proportions, text beats the picture.** Image-led takes copy the view's proportions, even when the fit sheets drew them differently (the dino's tall mouth, the hood's big cape). Text-only takes followed "wider than it is tall" and "ends below the lower jaw".
- **These heads are bigger than the costumes' openings.** OpenAI's and Anthropic's heads are 96 to 98 cm wide with their ear pods. A hood, wig or dino hood scaled to its look alone left the head sticking out. Each fit is sized to hold the head (the pods may poke out, as T47's decision 18 allows), and the fits need per-axis scale (`scale3`) to hold a head without hanging to the floor.
- **The beard as its own part** is what lets it hang below every mouth: its fit is per robot, apart from the helmet's.
- **The box head's mesh is too sparse to slice** (n-gons, 9 meshes). Its front is flat at 23.1 cm from the centre; the preview uses that.
- **Rodin centres each model's bounding box on the origin,** so a turn about the pivot moves a lopsided model, such as the saucepan with its handle. Its fit moves the pivot 14.5 to 27 cm toward the handle, close to T47's old `y` of 17.7.

## Open questions (the editor or T103's heads can answer them, the prep couldn't)

1. Does the glTF importer (Interchange in 5.8.4) bring these in at ×100, with +Z front turned to UE +X, or does each need a yaw (T82's FBX needed 270)? Check one and bake the same turn into all, as "Import" says.
2. Does T103's `HeadSocket` sit at each head's top with scale 1, and is Meta's head top at z 158 or 151? The fits are relative to the socket either way, but a socket scale other than 1 scales every costume.
3. With T103's real heads, eyes and mouths in the game: does any costume cover the eyes, the face or the name tag (T104's step 6 check)? The preview had no LED eyes or mouths, only T103's numbers for where they are.
4. Do T75's arm gestures clip through the cube hood's cape, the dino hood's lower jaw or the beard? The preview had arms only at rest.
5. Does `M_Clay` keep the imported normal maps (clay detail), or tint flat? Does the cut's gray (`SetCut`) reach the `Extra` component, or does `SetCut` need to tag it?
6. Does setting a Float array from a Json array work in the DSL (`HS3A`)? If not, use `sx`, `sy` and `sz` fields.
7. Is there a JSON field-names node for `CostIds`, or does `costume_test` need a fixed list?
8. Do the antenna stalk and the toppers still clear the new costumes with T47's lift (`top`)? The cowl's and the dino's `top` values are first guesses.
