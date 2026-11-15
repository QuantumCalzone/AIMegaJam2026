# Assets

Every art, audio and font asset in the game that we didn't make by hand in the editor: what it is, where it came from, and its license. The submission form needs this list. Add a row when you add an asset.

## Fonts

| Asset | What it is | Source | License |
|---|---|---|---|
| `Content/NHOS/UI/Fonts/F_UI` | The one UI font for every screen. A copy of the engine's `/Engine/EngineFonts/Roboto` composite font, so it uses the engine's Roboto font faces (Regular, Bold, Italic, Bold Italic, Light). | Roboto by Google, shipped with Unreal Engine 5.8 (`Engine/Content/Slate/Fonts`, `Roboto.tps`). | Apache License 2.0 (`Engine/Source/ThirdParty/Licenses/ROBOTO_License.txt`). |
| Fallback in `F_UI` | Droid Sans Fallback, the composite font's fallback typeface. It draws characters Roboto lacks, such as Chinese, Japanese and Korean. | Shipped with Unreal Engine 5.8 (`/Engine/EngineFonts/Faces/DroidSansFallback`, `DroidSans.tps`). | Apache License 2.0. |

Neither font draws emoji or pictographs. `WBP_Stage.CleanText` removes them, and other symbols from U+2190 up (arrows, dingbats, emoji, private use), before any line reaches the screen.

## Art

Everything on stage is built in the editor from the engine's basic shapes (`/Engine/BasicShapes/` Cube, Cylinder, Sphere, Cone) with our own Substrate materials:

- T11: the robots' first look (`M_Robot`, `MI_StageFloor`, `MI_StageWall`).
- T17: the improv theater, the persona robots' parts and the six scene backdrops. `M_Set` (one material for the set and the robots' accessories; its wood planks are drawn by a small HLSL node, not a texture), `M_Backdrop` (a two-color painted sky) and the instances in `Content/NHOS/Stage/Materials/`. No textures.

The money burn (T35) is the only 2D art: four textures in `Content/NHOS/UI/MoneyBurn/`, imported from `Docs/MoneyBurnArt/`. `Docs/MoneyBurnArt.md` has how each was made, the script that made them and their colors.

| Asset | What it is | Source | License |
|---|---|---|---|
| `Content/NHOS/UI/MoneyBurn/T_Bill` (`bill.png`) | The banknote: a muted sage bill with a robot head in a round medallion and "100" in each corner. No real currency's design, portrait or symbol. | Drawn by our script `makeart.swift` during the jam (2026-11-14). No outside art, no AI image tool. | Ours, made during the jam. |
| `Content/NHOS/UI/MoneyBurn/T_BillChar` (`bill_char.png`) | The same bill, charred to ash, for the wipe as it burns. | Drawn by `makeart.swift` from `bill.png`. | Ours, made during the jam. |
| `Content/NHOS/UI/MoneyBurn/T_FlameSheet` (`flame_sheet.png`) | The flame flipbook: one row of 8 frames, played at 14 fps. | Kenney, Particle Pack 1.1, `muzzle_02/03/05.png`, scaled, mirrored and recolored by `makeart.swift`. https://kenney.nl/assets/particle-pack | CC0 1.0 (the pack's `License.txt`). |
| `Content/NHOS/UI/MoneyBurn/T_Ember` (`ember.png`) | One soft ember for the sparks that rise from the burn. | Kenney, Particle Pack 1.1, `circle_05.png`, scaled and recolored by `makeart.swift`. https://kenney.nl/assets/particle-pack | CC0 1.0. |

### Generated 3D models

Made with Leonardo.ai (a reference image, through its paid API, private) and Meshy (image to 3D, on the Pro plan, which gives ownership). `Docs/PropArt.md` has how; each model's folder in `Docs/PropArt/` has its reference image and the JSON logs of its prompts, settings and credits. Not in the game yet.

| Asset | What it is | Source | License |
|---|---|---|---|
| `Content/NHOS/Stage/Props/Meshes/SM_PlushHorseHead` (with `M_PlushHorseHead`, `T_PlushHorseHead_BaseColor`) | The crime-family story's plush horse head prop, in clay style. | Leonardo.ai `lucid-origin` image (prompt in `Docs/PropArt/plush_horse_head/leonardo.json`), then Meshy 7.1 image to 3D with a 2K texture, 15,584 triangles, 2026-11-15. | Ours: made on paid Leonardo API and Meshy Pro plans. |
| `Docs/PropArt/hood/hood.fbx` | Clay headpiece: a cloth hood with a pointed tip and an open front. Mesh only; a clay material colors it per role (T47). | Leonardo.ai `lucid-origin` image (prompt in `Docs/PropArt/hood/leonardo.json`), then Meshy 7.1 image to 3D without a texture, target 15,000 triangles, 20 credits, 2026-11-15 (T40). | Ours: made on paid Leonardo API and Meshy Pro plans. |
| `Docs/PropArt/dark_shades/dark_shades.fbx` | Clay headpiece: chunky round sunglasses. Mesh only; a clay material colors it per role (T47). | Leonardo.ai `lucid-origin` image (prompt in `Docs/PropArt/dark_shades/leonardo.json`), then Meshy 7.1 image to 3D without a texture, target 15,000 triangles, 20 credits, 2026-11-15 (T40). | Ours: made on paid Leonardo API and Meshy Pro plans. |
| `Docs/PropArt/top_hat/top_hat.fbx` | Clay headpiece: a top hat with a band. Mesh only; a clay material colors it per role (T47). | Leonardo.ai `lucid-origin` image (prompt in `Docs/PropArt/top_hat/leonardo.json`), then Meshy 7.1 image to 3D without a texture, target 15,000 triangles, 20 credits, 2026-11-15 (T40). | Ours: made on paid Leonardo API and Meshy Pro plans. |
| `Docs/PropArt/bob_wig/bob_wig.fbx` | Clay headpiece: a bob-cut wig with a fringe, open at the face. Mesh only; a clay material colors it per role (T47). | Leonardo.ai `lucid-origin` image (prompt in `Docs/PropArt/bob_wig/leonardo.json`), then Meshy 7.1 image to 3D without a texture, target 15,000 triangles, 20 credits, 2026-11-15 (T40). | Ours: made on paid Leonardo API and Meshy Pro plans. |
| `Docs/PropArt/ball_cap/ball_cap.fbx` | Clay headpiece: a baseball cap. Mesh only; a clay material colors it per role (T47). | Leonardo.ai `lucid-origin` image (prompt in `Docs/PropArt/ball_cap/leonardo.json`), then Meshy 7.1 image to 3D without a texture, target 15,000 triangles, 20 credits, 2026-11-15 (T40). | Ours: made on paid Leonardo API and Meshy Pro plans. |
| `Docs/PropArt/wide_brim_hat/wide_brim_hat.fbx` | Clay headpiece: a wide-brimmed explorer's hat. Mesh only; a clay material colors it per role (T47). | Leonardo.ai `lucid-origin` image (prompt in `Docs/PropArt/wide_brim_hat/leonardo.json`), then Meshy 7.1 image to 3D without a texture, target 15,000 triangles, 20 credits, 2026-11-15 (T40). | Ours: made on paid Leonardo API and Meshy Pro plans. |
| `Docs/PropArt/saucepan_helmet/saucepan_helmet.fbx` | Clay headpiece: an upside-down saucepan worn as a helmet. Mesh only; a clay material colors it per role (T47). | Leonardo.ai `lucid-origin` image (prompt in `Docs/PropArt/saucepan_helmet/leonardo.json`), then Meshy 7.1 image to 3D without a texture, target 15,000 triangles, 20 credits, 2026-11-15 (T40). | Ours: made on paid Leonardo API and Meshy Pro plans. |
| `Docs/PropArt/wizard_hat/wizard_hat.fbx` | Clay headpiece: a floppy pointed wizard hat. Mesh only; a clay material colors it per role (T47). | Leonardo.ai `lucid-origin` image (prompt in `Docs/PropArt/wizard_hat/leonardo.json`), then Meshy 7.1 image to 3D without a texture, target 15,000 triangles, 20 credits, 2026-11-15 (T40). | Ours: made on paid Leonardo API and Meshy Pro plans. |
| `Docs/PropArt/tiara/tiara.fbx` | Clay headpiece: a small crown-shaped tiara with gems. Mesh only; a clay material colors it per role (T47). | Leonardo.ai `lucid-origin` image (prompt in `Docs/PropArt/tiara/leonardo.json`), then Meshy 7.1 image to 3D without a texture, target 15,000 triangles, 20 credits, 2026-11-15 (T40). | Ours: made on paid Leonardo API and Meshy Pro plans. |
| `Docs/PropArt/fedora/fedora.fbx` | Clay headpiece: a fedora with a pinched crown and a band. Mesh only; a clay material colors it per role (T47). | Leonardo.ai `lucid-origin` image (prompt in `Docs/PropArt/fedora/leonardo.json`), then Meshy 7.1 image to 3D without a texture, target 15,000 triangles, 20 credits, 2026-11-15 (T40). | Ours: made on paid Leonardo API and Meshy Pro plans. |
| `Docs/PropArt/horned_helmet_beard/horned_helmet_beard.fbx` | Clay headpiece: a horned helmet joined to a braided beard. Mesh only; a clay material colors it per role (T47). | Leonardo.ai `lucid-origin` image (prompt in `Docs/PropArt/horned_helmet_beard/leonardo.json`), then Meshy 7.1 image to 3D without a texture, target 15,000 triangles, 20 credits, 2026-11-15 (T40). | Ours: made on paid Leonardo API and Meshy Pro plans. |
| `Docs/PropArt/dino_hood/dino_hood.fbx` | Clay headpiece: a dinosaur costume hood, the face showing through its mouth. Mesh only; a clay material colors it per role (T47). | Leonardo.ai `lucid-origin` image (prompt in `Docs/PropArt/dino_hood/leonardo.json`), then Meshy 7.1 image to 3D without a texture, target 15,000 triangles, 20 credits, 2026-11-15 (T40). | Ours: made on paid Leonardo API and Meshy Pro plans. |
| `Docs/PropArt/beanie/beanie.fbx` | Clay headpiece: a knitted beanie with a pom-pom. Mesh only; a clay material colors it per role (T47). | Leonardo.ai `lucid-origin` image (prompt in `Docs/PropArt/beanie/leonardo.json`), then Meshy 7.1 image to 3D without a texture, target 15,000 triangles, 20 credits, 2026-11-15 (T40). | Ours: made on paid Leonardo API and Meshy Pro plans. |

## Audio

None yet (T20).
