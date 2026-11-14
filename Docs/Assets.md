# Assets

Every art, audio and font asset in the game that we didn't make by hand in the editor: what it is, where it came from, and its license. The submission form needs this list. Add a row when you add an asset.

## Fonts

| Asset | What it is | Source | License |
|---|---|---|---|
| `Content/NHOS/UI/Fonts/F_UI` | The one UI font for every screen. A copy of the engine's `/Engine/EngineFonts/Roboto` composite font, so it uses the engine's Roboto font faces (Regular, Bold, Italic, Bold Italic, Light). | Roboto by Google, shipped with Unreal Engine 5.8 (`Engine/Content/Slate/Fonts`, `Roboto.tps`). | Apache License 2.0 (`Engine/Source/ThirdParty/Licenses/ROBOTO_License.txt`). |
| Fallback in `F_UI` | Droid Sans Fallback, the composite font's fallback typeface. It draws characters Roboto lacks, such as Chinese, Japanese and Korean. | Shipped with Unreal Engine 5.8 (`/Engine/EngineFonts/Faces/DroidSansFallback`, `DroidSans.tps`). | Apache License 2.0. |

Neither font draws emoji or pictographs. `WBP_Stage.CleanText` removes them, and other symbols from U+2190 up (arrows, dingbats, emoji, private use), before any line reaches the screen.

## Art

No outside or generated art. Everything on stage is built in the editor from the engine's basic shapes (`/Engine/BasicShapes/` Cube, Cylinder, Sphere, Cone) with our own Substrate materials:

- T11: the robots' first look (`M_Robot`, `MI_StageFloor`, `MI_StageWall`).
- T17: the improv theater, the persona robots' parts and the six scene backdrops. `M_Set` (one material for the set and the robots' accessories; its wood planks are drawn by a small HLSL node, not a texture), `M_Backdrop` (a two-color painted sky) and the instances in `Content/NHOS/Stage/Materials/`. No textures.

## Audio

None yet (T20).
