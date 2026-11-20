# The game icon (T115)

The icon on the packaged game's `.exe`, its window and taskbar button, and the Mac app. My person picked it on 2026-11-20: **a grinning person pushes the costume's teal box head up and off with one gloved hand and winks**, on a UIStyle Red (`#C8202F`) tile, the game's "YOU: HUMAN" color.

![The icon at every size, on light and dark](icon_sheet.png)

| File | What it is |
|---|---|
| `icon_1024.png` | The source at 1024 × 1024, as Windows shows it (the tile fills the square). |
| `icon_mac_1024.png` | The Mac source: the same tile on Apple's icon grid (an 824 px body, 100 px in from each edge) with a soft shadow. |
| `icon_sheet.png` | The pick at 256 px, every Windows size at real pixels, 16 and 32 px zoomed, and a Windows 11 taskbar and title bar, on light and dark. |
| `check_windows.png` | The check in a packaged Windows build: Explorer's icon for the `.exe`, the game's title bar and its taskbar button. |
| `render/` | The in-engine render it was drawn from: `head_front.png` and `head_34.png`, close-ups of my costume robot in `L_Stage` (`SM_You_Head` and `BP_Robot`'s face parts). |
| `round1/` | The first three candidates, the box head alone: A on an ink tile with a gold rim, B on a gold tile, C the face alone. Not picked: my person asked for "a human pulling off the robot headpiece" instead. |
| `round2/` | The three candidates of that idea: 1 Lift (both gloves hold the box overhead), 2 Tilt (picked), 3 Peek (the box lifted a crack, the eyes peeking out). |
| `IconArt.cs`, `RevealArt.cs` | The drawing code (C# 5 and System.Drawing, no packages). `RevealArt.cs` draws round 2 and the pick; `IconArt.cs` draws round 1, the sheets, the `.ico` and the Mac set. |
| `pixel_tilt.py` | Laid out the hand-placed grids for 16, 20, 24 and 32 px (see below). |
| `make_icon.ps1` | Rebuilds everything above, `Build/Windows/Application.ico` and `Build/Mac/Resources/Assets.xcassets`. |

Rebuild from the repo root, on Windows:

```powershell
powershell -ExecutionPolicy Bypass -File Docs/Art/Icon/make_icon.ps1
```

## How it was made

1. **The render.** A second editor opened from the task's worktree (MCP port 8011, nothing saved) framed the costume robot in `L_Stage` (`BP_Robot_C_15`, persona `human`) with `CaptureViewport`, front and three-quarter. The box head's colors were sampled from it: face `#2B7C70`, slot liner `#63482A`, eyeball `#CBC4BB`, near-black pupils and marker smile. The icon lifts them a little toward flat, bright light (teal `#2F8A7C`).
2. **Round 1** (`round1/`). The front view, redrawn as flat shapes in the render's proportions: a 1.24 : 1 box, slots at ±24% of its width and 43% of its height, the marker smile at 80%, side knobs and the ping-pong antenna.
3. **Round 2 and the pick** (`round2/`). The costume parts are the game's own: the box head (its slots empty now, so you see into the hollow box), the red and cream knit scarf (`#E8563F`, from the render), and the striped sleeve and tan garden glove of the approved cast art (`Docs/Art/Cast/you/`). The person under the box is new: warm skin (`#E3A87C`), dark brown hair standing up with static, a wink and an open grin.
4. **Small sizes.** Below 32 px the vector shapes blur, so 16, 20, 24 and 32 px are hand-placed pixels (the `Pix` table in `RevealArt.cs`). `pixel_tilt.py` laid out the big shapes, the box stepped at a clean 1:2 slope (about 27°, near the vector's 24°), and the details were placed by hand. 40 and 48 px use the vector with fewer details (no nose or blush, wider stripes, a smaller mouth). 64 px and up are the full vector.
5. **The files.** `Build/Windows/Application.ico` holds 16, 20, 24, 32, 40, 48, 64 and 128 px as 32-bit images and 256 px as a PNG. `Build/Mac/Resources/Assets.xcassets/AppIcon.appiconset` holds the ten Mac sizes (16 to 512 at 1× and 2×), scaled from `icon_mac_1024.png`.

## Where UE 5.8 reads each icon

- **Windows:** `Build/Windows/Application.ico` in the project. UnrealBuildTool compiles it into the game `.exe` (`GetWindowsApplicationIcon` in `UEBuildWindows.cs`; `IDICON_UEGame` in `Engine/Build/Windows/Resources/Default.rc2`), and the running game loads that resource for its window and taskbar button. The packager also writes it into the bootstrap `.exe` at the build's root (`WinPlatform.Automation.cs`). Without the file, both use `Engine/Build/Windows/Resources/Default.ico`.
- **Mac:** `Build/Mac/Resources/Assets.xcassets` in the project replaces the engine's catalog (`ProjectOrEnginePath` in `XcodeProject.cs`), and Xcode compiles its `AppIcon` set as the app icon (`ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon`). The packager would also copy a `Build/Mac/Application.icns` into the app, but the plist doesn't point at it, so there is no `.icns`.
