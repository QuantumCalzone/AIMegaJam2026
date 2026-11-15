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

## Audio

None yet (T20).
