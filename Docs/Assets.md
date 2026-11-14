# Assets

Every art, audio and font asset in the game that we didn't make by hand in the editor: what it is, where it came from, and its license. The submission form needs this list. Add a row when you add an asset.

## Fonts

| Asset | What it is | Source | License |
|---|---|---|---|
| `Content/NHOS/UI/Fonts/F_UI` | The one UI font for every screen. A copy of the engine's `/Engine/EngineFonts/Roboto` composite font, so it uses the engine's Roboto font faces (Regular, Bold, Italic, Bold Italic, Light). | Roboto by Google, shipped with Unreal Engine 5.8 (`Engine/Content/Slate/Fonts`, `Roboto.tps`). | Apache License 2.0 (`Engine/Source/ThirdParty/Licenses/ROBOTO_License.txt`). |
| Fallback in `F_UI` | Droid Sans Fallback, the composite font's fallback typeface. It draws characters Roboto lacks, such as Chinese, Japanese and Korean. | Shipped with Unreal Engine 5.8 (`/Engine/EngineFonts/Faces/DroidSansFallback`, `DroidSans.tps`). | Apache License 2.0. |

Neither font draws emoji or pictographs. `WBP_Stage.CleanText` removes them, and other symbols from U+2190 up (arrows, dingbats, emoji, private use), before any line reaches the screen.

## Art

None yet. The robots and the stage use engine basic shapes and our own Substrate materials (T11).

## Audio

None yet (T20).
