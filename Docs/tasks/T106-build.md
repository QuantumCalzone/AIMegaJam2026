# T106 build sheet: the set's models, ready to import, and a plan for the house

Back to [T106](T106.md). Written by the T106 prep session on 2026-11-19. That session did T106's step 2 and the part of step 1 that needs no editor. It read T98's README, house view, pieces and swatches, T49's and T86's records, T17's, `Docs/PropArt.md`, T99's backdrops and T105's import findings. It then generated every model piece with Hyper3D Rodin and got my person's OK on the sheet. T106's own session does the rest: it reads `L_Stage`, locks it, and does steps 3 to 6 (materials, the house, the check, the records). It also writes `Docs/Assets.md`, `Docs/Art/Set/README.md`, `T106.md`, the design doc and the plan.

Everything here is measured from the files: the GLBs, T98's views and the task records. The prep made no editor read, so every place and size from `L_Stage` comes from the records, as T17, T49 and T86 wrote them. "Open questions" at the end lists what only the editor can answer.

## What is where

- **The approved sheet:** [`Docs/Art/Set/models_sheet.png`](../Art/Set/models_sheet.png) shows each piece as T98's approved view, then the model from the front and from three-quarter above. My person approved all 12 on it on 2026-11-19 ("Approve all 12").
- **One folder per piece:** `Docs/Art/Set/<piece>/`. Each folder holds:
  - `model.glb`: the model, with its three maps embedded.
  - `texture_diffuse.png`, `texture_normal.png` and `texture_metallic_roughness.png`: the same maps as loose 2048² files.
  - `reference_front.png` (and `reference_back.png` for the audience robot): the image sent to Rodin, made from T98's view in `pieces/views/`.
  - `thumbnail.png` (front), `three_quarter.png` and `turntable.png` (front, right, back, left).
  - `mesh_stats.json`: triangles, separate pieces, open edges, the bounding box and the maps.
  - `log.json`: the tool, settings, prompt, generation id, upload ids and what the reference changed from T98's view. It also has a `suggested_fit` with the numbers in "The pieces" below.
- **Two folders are renamed:** T98 already has concept folders `pieces/chandelier/` and `pieces/cherub_robot/`. The model folders are `chandelier_model/` and `cherub_robot_model/`, so that no name is used twice. The other ten use the piece's view name: `wall_pilaster`, `theater_box`, `side_curtain`, `valance`, `prop_table`, `stalls_seat`, `footlight`, `audience_bot`, `top_hat` and `bowler_hat`.
- **The frame of every GLB:** glTF as exported. Metres, +Y up, **the piece faces +Z**, centred on the origin. Rodin scales each model's longest side to about 1.9 m. The importer's axis change is not checked here (open question 1).
- **The maps follow glTF rules:**
  - `texture_metallic_roughness.png` packs roughness in **G** and metallic in **B**. Its R is 255.
  - `texture_normal.png` is **OpenGL** (+Y).
  - Metallic is near 0 except on the chandelier (B averages 66 of 255: Rodin read its orange as metal) and on the valance's gold bands. T98 says no metal, so the materials below take no metallic from the maps.
  - Rodin also offered a `texture_emissive.png` for the curtain and the valance (it took the painted gold for a glow). It wasn't downloaded, and the GLBs have no emissive map.
- **Tools:** the prep used T103's GLB reader (`glb.py`), its SceneKit turntable (`render.swift`, plus a three-quarter variant) and its sheet tool. It also used `prep.swift`, T103's crop tool with a solid color fill and a stroke added, which made the references. All of them are in the dispatcher's shared notes folder, `T103-prep-tools/` and `T106-prep-tools/`, not in git.

## The pieces

All of them were made with **Hyper3D Rodin**, on my person's Business plan. T81's license finding applies: ship them, and list them as ours, made with Hyper3D Rodin. The settings were `rodin_generate`, `Gen-2.5-Medium`, `Raw` mesh, GLB, `texture_delight` off, with one reference image (two for the audience robot) and a prompt. The file kept is `base_basic_pbr.glb`; the "shaded" one has baked light. Every piece came out right on its first take.

**Why Hyper3D:** it costs about 0.5 credit a call, against Meshy's 20 to 30. T103 and T105 proved it on the cast and the props, and it gives a closed mesh with PBR maps at a set triangle count.

| Piece (folder) | Generation id | Triangles, pieces | What the reference changed | What to know |
|---|---|---|---|---|
| Chandelier (`chandelier_model`) | `9fe3de1b-79c8-44f9-ac96-f8307c635bb1` | 15,000, 2 | The chain is painted out. | A turned column, a scalloped canopy on top, 11 scrolled arms with cream candles and a drop finial. The finial is the second piece. **No chain and no flames:** both are engine parts (T98). The candle tips are where the flames go. |
| Robot cherub (`cherub_robot_model`) | `1a043b91-576e-4670-b815-7950245c65f0` | 15,000, 1 | The plinth is painted out. The LED eyes and smile are painted over in the screen's black. | Sitting, wings, a horn at its face, round ear pods, a **blank black screen recessed** in the helmet. A thin flat base under it (what was left of the plinth's top), so it sits flat on the engine plinth. The eyes are engine parts, as on the cast. |
| Pilaster capital (`wall_pilaster`) | `b8cae34d-31bc-4bec-b798-9d702642134e` | 15,000, 1 | Cropped to the capital and its slab. | A scroll block with a red-brown cornice slab. **Rodin made it a near cube with the S-scrolls on all four sides.** Only the front shows: squeeze its depth (below). The shaft is an engine box. |
| Theater box (`theater_box`) | `a4dfa3c8-dcc1-4913-901d-7b2828670569` | 15,000, 1 | None. | A round-topped arch, fluted side pilasters, beaded moulding, crimson drapes inside, a curved balcony with a carved front. A **solid block** with the drapes as the back wall of a shallow alcove. All tan except the drapes: see "Surfaces" for the dark wood. |
| Side curtain (`side_curtain`) | `7a417439-a28a-4f57-ba89-530dee6d67d6` | 15,000, 1 | The rope and tassel are replaced by a thick gold band. | Thick pleats, the gold band at the waist, a flared foot. Flat enough to stand against the proscenium line. One a side: mirror the second with a negative scale. |
| Valance (`valance`) | `4539ad13-9683-44bf-8e47-ea22eb61a0ac` | 15,000, 2 | The rope and knot are painted as a thick gold swag, and a gold band runs under the header roll. | Header roll, gold band, two deep swags, a gold swag and a gold knot in the middle. One piece across (no halves needed). **Deep flat top**: squeeze its depth (below). The second piece is the gold band. |
| Prop table (`prop_table`) | `77c3343e-4742-4707-b938-2e34aacc2dcc` | 8,000, 1 | None. | A round table under a cream cloth to the floor. The top is flat. |
| Stalls seat (`stalls_seat`) | `6d9c4332-0b2d-4077-95a8-6d1d2e96421c` | 8,000, 1 | None. | Tall crimson back, cushion, gold arm caps, a dark wood box base. |
| Footlight (`footlight`) | `e13f025a-3078-425a-bff0-c1d22f847651` | 8,000, 1 | None. | A scalloped dome hood over a cream bulb on a round dark base. The hood is big against the base, as in the view. The glow is an emissive engine part. |
| Audience robot (`audience_bot`) | `0bfbaea5-9427-4698-82ce-765e54c40755` | 15,000, 1 | Front: the LED eyes painted out, the screen filled with #16141A. Back: none. Both went in as one generation's two references. | Helmet head with cream ear pods and a **blank black screen recessed** in the front, rose body, cream belly, claw hands, round feet. **No antennas.** The back matches the back view. |
| Top hat (`top_hat`) | `74275bb2-6491-4ce8-b6b5-c09a4e026890` | 8,000, 2 | None. | Straight crown, flat top, flat brim, a bright red band. The band is the second piece. |
| Bowler (`bowler_hat`) | `0094a468-3c01-464d-804e-d72d89ad10e5` | 8,000, 1 | None. | Dome crown, short curled brim, a brick-red band. |

**Not models,** as T98 says: the Riser (engine boxes), the cherub's plinth (an engine cube, 55 × 55 × 60), the pilaster shaft (an engine box), the chandelier's chain (an engine part, or none), the candle flames and footlight glows (small emissive engine parts), and the screens' LED eyes on the cherubs and the audience (engine parts, as on the cast).

## Sizes

`Scale` is the scale on the model's own **width (glTF X), height (glTF Y) and depth (glTF Z)**, for an import that turns metres into cm (×100). After the import, map these onto the UE axes the import gives (open question 1), and check them against the imported mesh's bounds. The targets are T98's sizes. "Pivot to bottom" is how far the pivot (the model's centre) sits above its lowest point at that scale.

| Piece | Model size (m, W × H × D) | Scale (W, H, D) | Size (cm, W × H × D) | Pivot to bottom (cm) | Why |
|---|---|---|---|---|---|
| Chandelier | 1.275 × 1.892 × 1.304 | 1.057 uniform | 135 × 200 × 138 | 100.5 | T98's 180 × 180 × 200 box, fitted by its height. Widening it to 180 (×1.41) would make it 267 tall. |
| Robot cherub | 1.728 × 1.899 × 1.711 | 0.342 uniform | 59 × 65 × 59 | 32.5 | 65 tall (T98) |
| Pilaster capital | 1.895 × 1.237 × 1.850 | 0.633, 0.633, 0.324 | 120 × 78 × 60 | 38.8 | A little wider than the 100 cm shaft, as in the view. Only the front shows. |
| Theater box | 1.505 × 1.901 × 1.770 | 1.0, 1.0, 0.904 | 150 × 190 × 160 | 95.2 | 190 tall keeps the tiers' pitch (z 152 and 342). **Half as wide as the old 300 cm box.** Stretching the width to 300 (×2.0) would flatten the arch; ×1.3 (196 wide) still reads. T106 judges it in the frame. |
| Side curtain | 0.648 × 1.900 × 0.233 | 3.263 uniform | 212 × 620 × 76 | 310.6 | 620 tall. T98 says 250 wide: a width scale of 3.856 gives that. |
| Valance | 1.893 × 0.438 × 1.080 | 7.396, 4.111, 0.556 | 1400 × 180 × 60 | 90.2 | T98's size. At a uniform 7.4 it would be 324 tall. |
| Prop table | 1.902 × 0.829 × 1.783 | 0.631, 0.965, 0.673 | 120 × 80 × 120 | 39.6 | 120 across, 80 tall. **Keep the old table's top height** so `BP_Prop`'s `Prop1` to `Prop4` still sit on it (T45). Read the old top's z in the editor and set the height scale from it. |
| Stalls seat | 1.135 × 1.886 × 1.014 | 0.705, 0.408, 0.691 | 80 × 77 × 70 | 38.4 | The back's top stays near T86's 75 above the row floor. A squatter chair than the model, but it is seen only from behind. |
| Footlight | 1.776 × 1.895 × 1.780 | 0.14 uniform | 25 × 27 × 25 | 13.2 | T98's 35 × 25 × 25 stretches the round hood; a width scale of 0.197 gives 35 if it reads better. |
| Audience robot | 1.480 × 1.900 × 0.887 | 0.842 uniform | 125 × 160 × 75 (the ear pods make the width) | 80.1 | 160 tall as modeled. The actor scale stays 0.37 to 0.43 (T86), so a bot stands about 64 cm. The old engine bot's hat socket was at z 163 at scale 1, so the new bot is about as tall. |
| Top hat | 1.894 × 0.982 × 1.899 | 0.517 uniform, in the bot's 160 cm frame | 98 × 51 × 98 | 25.3 | Brim 1.1 × the head's width. The head is 89 cm across without the ear pods in model units (from its depth), 75 cm at the bot's 0.842. |
| Bowler | 1.865 × 1.167 × 1.901 | 0.526 uniform, in the bot's frame | 98 × 61 × 100 | 30.7 | The same brim |

### On the audience robot (in its 160 cm frame, before the actor scale)

Measured from the vertices and the reference, with the feet at z 0:

- **The head** runs from the neck at about z 80 to the top at z 160. The dome's centre is at about z 120, with a radius of about 37 cm (44 cm in model units at 0.842). The ear pods stick out to ±52 cm, at about z 104 to 136.
- **The screen** (from the front reference): about z 106 to 140, 63 cm wide, centred. Read the recess floor from the vertices before you place the engine visor and eyes (T82's finding 4: `ProceduralMeshLibrary.get_section_from_static_mesh`).
- **The hats' crowns** sit on the dome where it is as wide as the crown. The top hat's crown is 66 cm across at 0.517, so its bottom sits at about **z 149**. The bowler's is 69 cm, at about **z 147**. Each hat's pivot is 25.3 (top hat) or 30.7 (bowler) above its bottom, so the `Hat` component goes at about z 174 and z 178. Check them in the editor.
- **The arms** hang at the sides from about z 60 to 110 and stick out to ±62 cm.

## Import settings (for every piece)

- **Import the GLB** with an editor Python script run from the Cmd box (`py "<file>"`, T46's and T105's way): `AssetImportTask` with `automated=True`, using the Interchange glTF importer (Interchange is on, T105). `StaticMeshTools.import_file` refuses `.glb` (`Docs/PropArt.md`).
- **Names and folders,** in `Content/NHOS/Stage/Set/` (T106's Touches). They are new names, so nothing collides with T42's `SM_Chandelier`, `SM_Cherub` and `SM_TheaterBox`, which the level still uses until the rebuild:
  - `SM_Set_Chandelier`, `SM_Set_Cherub`, `SM_Set_PilasterCapital`, `SM_Set_TheaterBox`
  - `SM_Set_SideCurtain`, `SM_Set_Valance`, `SM_Set_PropTable`, `SM_Set_StallsSeat`, `SM_Set_Footlight`
  - `SM_AudienceBot`, `SM_Aud_TopHat`, `SM_Aud_Bowler`
  - Each mesh gets `T_<Name>_BaseColor` and `T_<Name>_Normal`. The metallic-roughness map isn't needed.
- **The materials the importer makes:** delete them and its other textures (T105). The meshes go on the materials in "Surfaces".
- **Nanite off** (T105: a new mesh came in with Nanite on, and `get_num_triangles` then reports the fallback mesh).
- **No collision** on any piece (T49, T86: nothing in the house has collision). Generate no collision, or set `NoCollision` on each placed part.
- **The textures:**
  - BaseColor: sRGB on, default compression.
  - Normal: compression `Normalmap`, sRGB off, and **Flip Green Channel on**, because glTF normals are OpenGL. The importer may set this already: check one.
  - Every map is 2048². For the hats, the footlight and the seat (small on screen), a max size of 1024 is enough.
- **The two-piece meshes** (chandelier, valance, top hat): import as one static mesh (combine). Their second pieces are the finial, the gold band and the hat band.
- **Shadows:** the chandelier casts none (T49: it sits in `FrontWash`'s beam and would shade the middle of the stage). Rows B to D of the stalls cast none and sit on lighting channel 1 only (T86).

## Surfaces: Substrate materials and instances

T98: every surface is **one Substrate slab**, matte clay with faint thumbprints, **no metal**, no baked light. The house already has two Substrate masters that do this:

- **`M_Set`** (`Content/NHOS/Stage/M_Set.uasset`): `Color`, `Metal`, `Rough`, `Glow`, `Fuzz` (velvet), `Planks`, and T49's `ThumbScale` and `ThumbDepth` (a world-position thumbprint normal).
- **`M_Clay`**: `Color`, `Rough`, `ThumbScale`, `ThumbDepth`.

### 1. The swatches as instances of `M_Set`, for the engine parts

**Update T49's `MI_Theater_*` instances in place**, rather than making new ones. Every engine part of the theater already uses them (T49 moved 53 slots onto them), so the walls, the floor, the masking and the Riser take the new look with no slot changed. Colors are given as linear values (the parameters are linear) and as sRGB hex.

| Instance | Swatch | `Color` (linear) | `Rough` | Other parameters | Goes on |
|---|---|---|---|---|---|
| `MI_Theater_Velvet` | `velvet_crimson` #9E1B22 | (0.342, 0.011, 0.016) | 0.8 | `Fuzz` 0.3, `Metal` 0 | Any engine velvet that stays (masking legs). The models carry their own. |
| `MI_Theater_Gold` | `gold_bright` #D9B24E | (0.694, 0.445, 0.076) | 0.55 | **`Metal` 0** (it is 0.3 now), `ThumbDepth` 0.2, `ThumbScale` 0.08 (T49's) | The Riser's top trim, the apron trim, the box wall's trim strip, the stalls' gold rail |
| `MI_Theater_WoodDark` | `wood_dark` #5A3A22 | (0.102, 0.042, 0.016) | 0.8 | `ThumbDepth` 0.15 | The house walls, the proscenium columns, the pilaster shafts, the cherubs' plinths (they are gold cubes now), the Riser, the apron's face if it isn't planks |
| `MI_Theater_Wood` | `stage_planks` #A87E4F | (0.392, 0.209, 0.078) | 0.75 | `Planks` on, as now | The stage floor and the apron's face |
| `MI_Theater_Cloth` | `cream` #F0E3C4 | (0.871, 0.768, 0.552) | 0.85 | | Anything cream from engine shapes (the candle and bulb stems, if any) |
| `MI_Theater_Black` | `house_black` #17110F | (0.009, 0.006, 0.005) | 0.9 | | The masking, the house floor, T86's row decks |

`MI_Theater_Gunmetal` (the truss and spotlight cans) has no swatch. If those parts are out of the house camera's frame, leave them; if not, delete them (open question 4).

**Glows** stay as they are: `MI_FootGlow` for the footlight bulbs, and the candle flames as small emissive engine parts in a warm glow instance. `M_Chandelier` makes its candles glow now; a `MI_CandleGlow` on `M_Set` with `Glow` would replace it.

### 2. A new master for the generated models: `M_SetModel`

The models' textures have the right detail, but not quite the swatch colors. The gold came out tan-orange, the box is tan where T98 wants dark wood, and the hats' bands are a bright red. Painted detail is in the texture, so a flat `M_Clay` color would lose it. A **palette shift** keeps the detail and moves each color region onto its swatch:

- **`M_SetModel`** (new, in `Content/NHOS/Stage/Materials/`): one Substrate slab, built like `M_CastModel` (`BaseTex`, `NormalTex`, `NormalAmount`, `Rough`) with no metallic input.
  - Albedo = `BaseTex` + Σᵢ wᵢ · (`Toᵢ` − `Keyᵢ`), for i = A, B, C.
  - wᵢ = exp(−‖`BaseTex` − `Keyᵢ`‖² / `Width`²): each texel moves by the shift of the key colors near it. `Width` ≈ 0.25 in sRGB units.
  - Clamp the albedo to 0 to 1.
  - An unused key has `To` = `Key`.
  - `Rough`: one value per instance (0.8; 0.6 on the all-gold pieces).
  - `ThumbDepth`: 0, since the generated normals already carry the clay.
  - Do the shift in sRGB (`BaseTex` sampled as sRGB, so convert or compare in linear consistently). The keys below are sRGB, measured with k-means on each diffuse map.
- **If the shift is too fiddly** to build through MCP, use one `M_CastModel`-style master with `TintAmount` per instance and accept the textures' colors. The gold reads ochre and the box tan. That is a decision for my person.

| Instance (on `M_SetModel`) | Mesh | Key A → To A | Key B → To B | Key C → To C |
|---|---|---|---|---|
| `MI_Set_Chandelier` | `SM_Set_Chandelier` | #C38444 → gold #D9B24E | #E9D5B0 → cream #F0E3C4 | |
| `MI_Set_Cherub` | `SM_Set_Cherub` | #CF9B5F → gold #D9B24E | | |
| `MI_Set_PilasterCapital` | `SM_Set_PilasterCapital` | #D08A5C → gold #D9B24E | #B7633E (the cornice slab) → wood_dark #5A3A22 | |
| `MI_Set_TheaterBox` | `SM_Set_TheaterBox` | #B47E44 (the flat front and arch) → wood_dark #5A3A22 | #851C18 / #AC4635 (the drapes) → velvet #9E1B22 | #D5AC73 (the light mouldings) → gold #D9B24E |
| `MI_Set_SideCurtain` | `SM_Set_SideCurtain` | #720F14 → velvet #9E1B22 | #D79A46 → gold #D9B24E | |
| `MI_Set_Valance` | `SM_Set_Valance` | #871E20 → velvet #9E1B22 | #F2B85E → gold #D9B24E | |
| `MI_Set_PropTable` | `SM_Set_PropTable` | #D6C7A8 → cream #F0E3C4 | | |
| `MI_Set_StallsSeat` | `SM_Set_StallsSeat` | #CC414B → velvet #9E1B22 | #84523E → wood_dark #5A3A22 | #D69764 → gold #D9B24E |
| `MI_Set_Footlight` | `SM_Set_Footlight` | #C9945B → gold #D9B24E | #F4E7C9 → cream | #4C372E → wood_dark #5A3A22 |
| `MI_Aud_Rose` | `SM_AudienceBot` | #B86752 → rose #C98B8B | #E5C8A4 → cream #F0E3C4 | |
| `MI_Aud_Plum`, `_Mustard`, `_Brick`, `_Lilac` | `SM_AudienceBot` | #B86752 → plum #7E5A7A, mustard #C9A43F, brick #A65A3E, lilac #A89BC9 | #E5C8A4 → cream | |
| `MI_Aud_Hat` | both hats | #444547 → house_black #17110F | #DF0704 (top hat) and #9F4B3C (bowler) → band #7A1E22 | |

**The box's dark wood is the weakest key.** Its tan flat parts (#B47E44) and its mouldings (#D5AC73) are close in color, so the split will be soft. If it reads muddy, put the whole tan on gold and let the dark-wood house wall behind it carry the brown, as the approved house view's boxes do.

**The audience's second shade** (#9B4C35, the shadowed side of the rose) needs its own key, or a `Width` big enough to catch it. Check a bot of each color from the house camera.

**The cut gray.** The audience is never cut, so `M_SetModel` needs no `Cut` input.

## The house in `L_Stage`: what stays, what is built, what goes

Every number here is from the records (T17, T45, T49, T86). Read the level before you trust any of them. T103 runs now and may move the robots' places in `L_Stage` (open question 2).

### What must stay

| What | Where it is now (records) | Why it stays |
|---|---|---|
| **The house camera** `StageCamera` | (−1050, 0, 230), pitch −12, 90° horizontal FOV (T17) | Its frame at 1600 × 900 and 1440 × 900 is "What must keep working". Don't move it; build the house to its frame. A taller window shows more at the top and bottom (T86). |
| **The places** (`Stage/Places`, `BP_PlaceMark`) | Center, Left, Right, Front, Back, Riser, Prop Table (T15). The Riser at (300, −300), the prop table at (300, 300) (T17). | The game logic walks the robots to them. |
| **The prop table's top height** | T17's cloth table at (300, 300). `BP_Prop`'s `Prop1` to `Prop4` sit on it (T45). | The props rest on it. Read its top z before you swap it for `SM_Set_PropTable`. |
| **The backdrop flat** `BP_Backdrop` | (520, 0, 0), 13 × 6.2 m (T17), showing T99's backdrops through `M_Backdrop`'s emission (T48, T99) | T99's paintings. Don't touch `BP_Backdrop.uasset` unless the flat changes. |
| **The near rows' lighting channel** | Rows B to D (x −570, −670, −770) on lighting channel 1 only, lit by `SM_HouseGlow` (250 cd, radius 1300, cones 50/80°, no shadow) at (−380, 0, 180), also on channel 1 only (T86) | Keeps the stage lights off the near rows, and the house glow off the stage. Every new part in rows B to D goes on channel 1 only, with no shadow. |
| **The lights** | `FrontWash`, `RimPink`, `RimCyan`, three `FootGlow` points, two `BackdropWash` spots, `KeyLight` (T17), `SM_HouseGlow` (T86). Exposure: `StagePost`, manual, bias 6 (T17). | T98: they stay; T106 retunes them for the darker walls, and the stage stays the brightest place in the frame. |
| **The stage floor** | 9 × 20 m planks, front edge at x −260 (T17). House floor top at z −110 (T86). | It holds the places. It takes the planks swatch through `MI_Theater_Wood`. |
| **The rows' layout** | Row A at x −470 (13 seats, y −600 to 600, 100 apart). B at −570 (13), C at −670 (11), D at −770 (9), raised 14, 28 and 42 on `MI_Theater_Black` decks 100 deep. 46 seats, 41 bots (T49, T86). | T98: "T106 keeps T86's rows, seat pitch and bot scale". Swap the parts, keep the layout. |

### What is built, piece by piece

All of it goes under the outliner folder `Stage/Theater/Opera/` as now (T49), placed by **one re-runnable script** that destroys and places only its own folders. Start from T86's `Docs/tasks/T86-build/stalls_more.py`, which already does this for the stalls with a fixed seed. Don't run T49's `Saved/T49/layout.py` (on the Mac only, not in git) as it is: it destroys everything under `Stage/Theater/Opera/`.

| Piece | Where (records) | How |
|---|---|---|
| **Chandelier** | (−500, 0, 411), yaw 90, no shadow (T49). Its bottom sits about 60 px above the highest robot label. | `SM_Set_Chandelier` at its scale. Put its bottom where the old one's bottom is (read the old bounds), so the labels and bubbles clear it. Add a short engine chain (a thin dark cylinder) up out of frame, or none. Small emissive flames on the 11 candle tips. |
| **Robot cherubs** | (−243, ±495), turned 20° toward the middle, on plinths at the apron's front corners (T49) | An engine plinth 55 × 55 × 60 in `MI_Theater_WoodDark`, then `SM_Set_Cherub` on top: its bottom at the plinth's top, so the pivot is 32.5 above it. Add an engine visor in the screen recess, with two LED eyes in `MI_Aud_Eye`. Turn each to face the house. |
| **Theater boxes** | (−450, ±600), tiers centred at z 152 and 342, turned 25° from the side wall toward the house (T49) | `SM_Set_TheaterBox`, one per tier per side (4). At 150 wide it is half the old box: judge in the frame whether to widen it (×1.3) or set two side by side. Keep the dark-wood wall behind, with its gold trim strip. The 8 box bots stay, facing out of each box, a third with opera glasses (T49). |
| **Wall pilasters** | The side walls between the boxes and the curtains (T98) | An engine shaft 100 × 50 × 600 in `MI_Theater_WoodDark`. `SM_Set_PilasterCapital` at its top, and the same capital **repeated up the shaft as reliefs**: the house view's tall gold S-scrolls (T98). The frame's top at the proscenium is about z 460 (T49), so the top capital is out of frame and the reliefs are what shows. |
| **Side curtains** | Either side of the stage opening, in front of the proscenium columns' line (y ±640) (T98). T17's seven velvet pleats a side are there now. | `SM_Set_SideCurtain`, one a side, the second mirrored. Face the house. |
| **Valance** | Across the top of the stage opening (T98). T17's valance with a gold fringe is there now. | `SM_Set_Valance` at 1400 × 180 × 60. The proscenium header starts at z 580 and the frame's top there is about z 460 (T49). **The valance must hang below z 460 to show**, and above the labels (z 228) and bubbles. Tune it in the frame. |
| **Riser** | (300, −300), 300 × 150 × 45, with a step 60 × 30 × 22 (T17, T98) | Keep T17's engine boxes. Put `MI_Theater_WoodDark` on them and `MI_Theater_Gold` on a thin top trim. Don't move it: the Riser place is on it. |
| **Prop table** | (300, 300) (T17) | `SM_Set_PropTable`, its top at the old top's z (T45). Delete T17's engine table. |
| **Footlights** | Nine along the apron's front edge (x about −260), as now (T17) | `SM_Set_Footlight` in place of each engine hood, facing the stage. A small emissive bulb sphere in `MI_FootGlow` inside each hood. Keep the three `FootGlow` point lights. |
| **Stalls seats** | Every seat of rows A to D (46). Today a seat is the 100 cm engine cube at (0.14, 0.82, 0.75) in `MI_Theater_Velvet` (T49, T86). | `SM_Set_StallsSeat`, facing the stage (+X), with its back's rear face where the cube's rear face is. The back's top is near 75 above the row's floor. The cushion now sticks out about 50 cm toward the stage, so move each bot onto it: T86's `BOT_DX` 18 becomes about 30 to 35. Read the cushion's top before you set `BOT_DZ`. Rows B to D on channel 1 only, no shadow. Row A's gold rail stays. |
| **Audience bots** | 49 `BP_AudienceBot`: 41 in the stalls, 8 in the boxes. Scale 0.37 to 0.43, turn ±15°, six lean 5 to 8° (T86, seed 86). | Rebuild `BP_AudienceBot` (below), then re-run the layout so every bot keeps its place, color, turn and lean. |

### `BP_AudienceBot`, rebuilt

T49 built it from engine shapes copied from T46's `BP_Robot`, with no graph: each placed copy sets its own color, hat and glasses on its components (T49, T86). Keep that.

- **Keep:** the root; `Visor` (`MI_Aud_Screen`), moved into the new screen recess (about z 106 to 140, 63 wide, in the 160 cm frame); `EyeL` and `EyeR` (`MI_Aud_Eye`) on the visor; `Hat`; and the two gold opera-glass cylinders (hidden by default).
- **New:** `Body`: `SM_AudienceBot` at scale 0.842, its feet at the old bot's feet, on `MI_Aud_<Color>`.
- **Delete:** the old shapes the model replaces: `CapLow`, `BodyLow`, `Seam`, `Head`, `FootL` and `FootR`, and the old `Body` if it's a shape.
- **The hats:** `Hat` takes `SM_Aud_TopHat` (scale 0.517, about z 174) or `SM_Aud_Bowler` (0.526, about z 178), both on `MI_Aud_Hat`. Mix them about half and half (T94's board: three bowlers to three top hats), and leave a few heads bare.
- **No more `Stage/Headpieces/`:** T86's script put T40's top hat, fedora, wide brim, beanie and backward cap on the audience, all from `Stage/Headpieces/`. **T104 deletes that folder**, so after T106 no audience bot may reference it (T98's dependency).
- **Rows B to D** hide what can't be seen from behind (T86). Now that is only `Visor`, `EyeL` and `EyeR`, since the body is one mesh.
- **Triangles:** 49 bots × (15,000 + 8,000 for a hat) is about 1.1 million triangles. T86 measured about +1 ms of GPU for its house. Check the frame time (T86's `startfpschart` way). If it rises noticeably, the bots in rows B to D can use a simplified LOD: generate LODs on `SM_AudienceBot` in the static mesh editor (LOD1 at 30%).

### What goes (delete once nothing references it)

- **T42's set models in `Content/NHOS/Stage/Set/`:** `SM_Chandelier`, `SM_Cherub`, `SM_TheaterBox`, with `M_Chandelier`, `M_Cherub`, `M_TheaterBox` and their `T_*_BaseColor`. Their rows in `Docs/Assets.md` and their entries (`kind: set`) in `Docs/PropArt/manifest.json` go too, or are marked replaced.
- **T17's engine parts** that the models replace:
  - the seven velvet pleats a side
  - the valance with its gold fringe
  - the nine footlight hoods (keep the `FootGlow` lights)
  - the cloth-covered prop table
- **T49's engine parts:**
  - the cherubs' gold cube plinths (replaced by dark wood plinths)
  - row A's 13 seat-back cubes
- **T86's engine parts:** the 33 seat-back cubes in `StallsMore`. Keep the three decks and `SM_HouseGlow`.
- **`BP_AudienceBot`'s old shapes** (above). Every audience reference to `Stage/Headpieces/`.
- **The truss and its five spotlight cans** (T17, `MI_Theater_Gunmetal`), if they are in the frame and the house view has no place for them (open question 4).
- **Materials:**
  - `MI_Clay_AudRose`, `AudPlum`, `AudMustard`, `AudBrick` and `AudLilac`, once the bots are on `MI_Aud_*`.
  - `MI_Theater_Gunmetal`, if the truss goes.
  - `MI_Clay_Charcoal`, `MI_Clay_Black`, `MI_Clay_Knit` and `MI_Clay_Denim` were the audience's hat colors (T86), but the robots' costumes may use them too: check their references, and leave them for T104 if anything else uses them.
  - Don't delete T17's old `MI_Gold`, `MI_Velvet` and the rest: the robots and props use them (T49).
- **Keep** `MI_Aud_Screen`, `MI_Aud_Eye`, `MI_FootGlow`, `M_Set`, `M_Clay` and `M_CastModel`.

## Costs

- **12 Hyper3D calls**, all kept, no retries: about **6 credits** at T81's measure of about 0.5 a call. My person OKed up to 15.
- The MCP tools report no cost per call, and `t104-prep-costumes` spent from the same wallet at the same time, so this is counted by calls, not read from the balance.
- **Meshy: 0.** The uploads (13 images) and the downloads (12 GLBs, about 83 MB) cost nothing.

## Findings

- **Rodin follows a painted fix well when it is a simple shape in a flat color.** The rope tie-back became a solid gold band. The valance's painted gold strokes became a raised band and a swag with a knot. The cast's lesson (T103: a patch comes back as geometry) holds the other way round: paint what you want, plainly.
- **A blank screen painted in the screen's own black comes back as a recess.** Both the cherub and the audience robot have a real recessed screen with a black floor, as T103's heads do. The eyes go on as engine parts.
- **Front and back views of the same robot in one call give a matching back,** with no stray parts. That's unlike T103's side view, which added arms: here nothing overlaps.
- **Rodin makes wide objects deep.** The pilaster capital came out as a cube with scrolls on all four sides, and the valance with a deep flat top. Both are fixed by a depth scale, and their backs sit against walls. The box is a solid block: its alcove is shallow, with the drapes as its back wall.
- **The chandelier came out partly metallic** (B about 0.26) and the valance's gold fully metallic. Ignore the metallic map (T98: no metal).
- **The texture colors are near the views', not the swatches'.** That's why the palette-shift material above exists. The k-means keys are measured on the 2048² maps, every sixth pixel.

## Open questions (the editor can answer them, the prep couldn't)

1. **The glTF import's axes.** Does the Interchange glTF importer in 5.8.4 bring these in at ×100, with glTF +Y to UE +Z, and to which UE axis does the model's front (+Z) turn? Check one piece, then apply the same to all. T105's FBX path needed yaw 90 to face the house; T103 asks the same for its GLBs.
2. **Check the places after T103.** T103 runs now and may move the robots' places in `L_Stage`, and add a material in `Stage/Materials/`. Read `Stage/Places` after T103's push, and build around what is there.
3. **The old pieces' real transforms and bounds:** the chandelier's bottom, the prop table's top z, the cherubs' plinths, the boxes, the pleats, the valance and the footlights. The records give centres, not every bound. Read them before you replace each one.
4. **Is the truss (and its five spotlight cans) in the house camera's frame?** If not, leave it. If it is, it goes, since the house view has no truss.
5. **The theater box's width:** 150 cm (uniform scale, as made), ×1.3, or two boxes side by side per tier? Judge it in the frame at both window sizes.
6. **The valance's height,** so that it shows below the frame's top (about z 460 at the proscenium) and clears the labels and bubbles.
7. **`M_SetModel`'s palette shift:** does it read well on the box (the weakest split) and on all five audience colors from the house camera? If not, use the fallback (texture colors with a tint).
8. **The normal map's green channel** on import (glTF is OpenGL).
9. **The bots on the new seats:** the cushion's top z and the bot's offset onto it (T86's `BOT_DX` and `BOT_DZ`), from the imported seat's bounds.
10. **The frame time** with 49 model bots and hats against T86's engine bots. Measure before and after.
