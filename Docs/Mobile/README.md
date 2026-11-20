# The stage on the mobile renderer (T112)

Back to [T112](../tasks/T112.md). A spike, made on the PC on 2026-11-20 in a throwaway copy of the project. Nothing in the game changed.

**In short:** the stage survives the mobile renderer better than expected. The robots, the backdrops, the props, the gold and crimson house and every UI panel read the same on the Android Vulkan and Android OpenGL ES 3.1 previews as on the desktop. Two things in the picture change a lot: the near stalls turn much darker without Lumen's bounce light, and the robots cast no shadow on the stage floor, so they seem to float. On top of that, the engine's two touch joysticks show on screen. The work for a phone is mostly elsewhere: touch controls and text size for the typed chat, fewer triangles, smaller textures, and Android files that this PC doesn't have yet.

## How the shots were made

- **The copy:** `C:/Users/Personal/Projects/NHOS_mobile`, a detached git worktree of the repo at `4caba44`, made like the deploy worktree. Its `Local/switches.json` was free mode with analytics off and no key. Nothing in it was saved or committed.
- **The renderers:** each shot is a game window of the copy at 1600 × 900 (`UnrealEditor.exe <copy> -game -windowed -ResX=1600 -ResY=900`), captured with `PrintWindow` as in T86. The two mobile previews use the command line that the editor's own "Mobile Preview (Standalone)" builds once a preview platform is picked (`PlayLevelNewProcess.cpp` in the engine), so they are the editor's preview platforms in a window of their own:
  - **Desktop:** no extra flags (D3D12, SM6, Lumen, Virtual Shadow Maps, Substrate).
  - **Android Vulkan:** `-featureleveles31 -faketouches OVERRIDESP=VULKAN_ES3_1_ANDROID_Preview -DeviceProfile=Android_Preview_Vulkan`.
  - **Android OpenGL ES 3.1:** `-featureleveles31 -faketouches OVERRIDESP=OPENGL_ES3_1_ANDROID_Preview -DeviceProfile=Android_Preview_OpenGL`.
  - The shader platform name needs the `_Preview` ending. Without it the engine logs "it is not a preview platform" and falls back to the generic `PCD3D_ES3_1`.
- **The shows:** a free autoplay show per renderer, captured every 3 s from start to end screen. Desktop and Vulkan played four scenes and won; ES 3.1 was caught in scene 1. The draw is random, so each column shows the same phase from the same house camera, with a different scene and cast order. Scene Prep and the title come from runs with autoplay off: the title's keyboard focus was moved to Test for Free by key messages posted to the game window (Down, Enter), which needs no mouse and no focus change.
- **First start of each mobile preview:** about 2 minutes of shader compiling (114 s for Vulkan, 155 s for ES 3.1), then as fast as the desktop.

## Side by side

Each sheet: desktop, Android Vulkan, Android ES 3.1, from left to right.

![The title on the three renderers](1_title.png)

![Scene Prep on the three renderers](2_scene_prep.png)

![A scene turn on the three renderers](3_scene_turn.png)

![Free Talk on the three renderers](4_free_talk.png)

![The Cut: the votes, on the three renderers](5_the_cut_votes.png)

![The Cut: the reveal stamp, on the three renderers](6_the_cut_stamp.png)

![The end screen on the three renderers](7_end_screen.png)

Two details at 1:1:

![The title's stalls and right-hand boxes, the same frame on desktop, Vulkan and ES 3.1](detail_stalls.png)

![Robots on the stage floor in a scene turn: soft shadows on desktop, none on mobile](detail_robots.png)

## What breaks or changes

Vulkan and ES 3.1 look the same as each other in every shot. So everything below holds for both.

| Area | On the mobile previews | Why |
|---|---|---|
| **The house's light** | The near stalls (rows B to D) are much darker: the red seat backs still show, but the bots' domes and hats fade out, and the nearest row is nearly black. A first try without the Android device profile (so with local exposure on) was darker still. The boxes and the side walls are a little darker. The stage itself keeps its warm look: the footlights, the spot pools, the gold and the crimson read as on desktop. | The house has no sky light and no fill. Its soft light is Lumen's bounce from the stage, and the mobile renderer has no Lumen. T86's faint `SM_HouseGlow` (250 cd, lighting channel 1) is all that lights the near rows there. |
| **Shadows** | The robots, props and Riser cast no shadow on the stage floor, so the robots seem to float a little. Desktop has a soft shadow under each robot. | The 11 stage lights are Stationary, and with static lighting off (`r.AllowStaticLighting=False`) a Stationary light has no shadow on mobile. Virtual Shadow Maps are desktop only. The 5 robot spots are Movable but hidden in these phases. |
| **Reflections** | The plank floor loses its faint sheen from the lights; it reads matte. | No Lumen reflections. The art direction asks for matte clay anyway, so this is close to the brief. |
| **Substrate materials** | All 34 compile and look right, with one exception: `M_GlowStickSword` fails ("Sampler type is Grayscale, should be Linear Grayscale") and falls back to the default material. | The same bug the Mac cook hit; T119 fixes it in all three glow props. Nothing else needs a fallback material. |
| **Hyper3D models and textures** | They look the same: no missing textures, no seams. | 117 textures, 100 of them 2048 × 2048 (434 megapixels in all), no virtual textures, no Nanite on any of the 79 meshes. |
| **Draw calls and triangles** | Per frame in a scene turn (`stat rhi`): desktop about 880 draws and 5.1 M triangles (shadow passes included); Vulkan preview about 317 draws and 2.9 M triangles. | 1,412 static mesh parts in `L_Stage`, 3.5 M triangles at full detail, and no mesh has a lower LOD. The audience alone is 1.5 M: 49 bots at 15,000 triangles, 54 seats at 8,000, 49 hats at 8,000. On this RTX 3060 the preview takes 5.8 ms of GPU time, which says nothing about a phone. |
| **The UI** | Every panel, button, tag, bubble, stamp and the end screen draws exactly as on desktop. New: two touch joystick rings at the bottom left and right, over the chat panel and the house. | The engine's default touch interface (`DefaultVirtualJoysticks`) shows whenever touch is on. One line in `DefaultInput.ini` turns it off. |

What screenshots can't show: sound, frame rate on a phone, memory on a phone, and how it feels to type the chat on a phone. Those need step 4.

## What a mobile look would take

Estimates for a device profile that keeps the art direction (the clay opera house, warm footlights, pink and cyan rims, a dim house, the bright stage). The game keeps Lumen on desktop; the mobile changes apply only on mobile, through the Android device profiles and a check of the feature level in the Blueprints.

1. **Lights (about one task).** Keep static lighting off: baking would need `r.AllowStaticLighting=True` for the whole project, lightmap UVs on every Hyper3D model and a new bake whenever the set changes, which is not worth it for a set where everything moves.
   - Give the house a mobile-only fill: a dim warm sky light, or `SM_HouseGlow` raised on mobile, so the near rows show again.
   - Robot shadows: either make the key spot (`KeyLight`) Movable with `r.Mobile.EnableMovableSpotlightsShadow=1` (mobile draws shadows for a few Movable spot lights), or put a soft clay-dark blob decal under each robot. The blob is cheaper and suits the stop-motion look; the spot looks closer to desktop. Try both on a phone.
   - Everything else carries over: the footlights, the rims and the spot pools already read.
2. **Materials (nothing beyond T119).** All Substrate materials compile for mobile. Once T119's grayscale fix is in, no fallback is needed. Glow still works (bloom is on in the mobile preview).
3. **Textures (small, no asset change).** At the house camera a robot is about 125 px tall, so a 2048 texture is 8 to 16 times more than the screen shows. A cap of 1024 in the Android device profiles (`TextureLODGroups`, or a LOD bias of 1 on the World group) quarters the texture memory and the download, and the cook stores them as ASTC. Today's textures come to about 370 to 580 MB with their mips at desktop compression; capped at 1024 in ASTC they are about 50 to 70 MB.
4. **Triangles (one task).** Generate lower LODs for the 79 meshes (the engine's mesh reduction, for example 25% at LOD 1), or one 2,000 to 3,000 triangle audience bot, seat and hat for the house, which the camera sees at about 40 px. That takes the frame from 2.9 M triangles to under 1 M, where mid-range phones are comfortable. 317 draws are already fine.
5. **The UI on a phone (one or two tasks).**
   - Turn off the touch joysticks (`DefaultTouchInterface`).
   - Text and buttons scale with the screen's short side. On a 6.5 inch phone in landscape, the 900 units of height are about 6.8 cm, so 18 pt text is about 1.4 mm tall and a 48 px button about 3.6 mm: too small to read and too small to tap. A phone needs about 1.5 times larger UI (the DPI curve, or a phone layout).
   - The typed chat: Android's on-screen keyboard covers the lower half of the screen, where the chat panel and its input box are. Either Unreal's native text dialog (the default: a system box pops up for each line) or the integrated keyboard with the input moved above it.
   - The hover cards (T85) need a tap: tap a robot to show its card, tap again to hide it. Scene Prep already offers Left and Right for the keyboard.
   - The end screen's four cards scroll; drag-to-scroll works on touch, but the text needs the same scale-up.
6. **Build size.** The Windows release is 855 MB: 414 MiB of cooked content in one `.ucas`, a 316 MiB Development `.exe`, and engine DLLs (Vulkan layers, DirectML, ONNX runtime). An Android Shipping `.apk` drops the `.exe` and DLLs for one `.so` (about 100 MB, compressed in the `.apk`), and with textures capped at 1024 the content shrinks most. The music (131 MiB of source WAV in `Content/NHOS/Audio/Music`) becomes the next biggest part. My estimate is an `.apk` of 150 to 300 MB, which itch.io takes. Google Play's 200 MB base limit doesn't apply to itch.io.

## Android: what step 4 would need (not done: no OK yet)

Nothing for Android is installed on the PC today, and two separate things are missing:

1. **The engine's own Android files.** This 5.8.4 install was made without its platform parts. Its install manifest (`E:/Epic Games/UE_5.8/zen-manifest.json`) lists 20,288 Android files, and 1,362 of them are on disk: there is no `Engine/Binaries/Android` (the prebuilt `UnrealGame-Android-*.so` that a Blueprint-only project packages with) and no `Engine/Build/Android` (the Gradle and Java parts). The Epic launcher doesn't list this install (`LauncherInstalled.dat` is empty), so its Options > Target Platforms > Android checkbox can't add them. They come from the same installer that made the install, with Android ticked. The manifest gives no sizes and Epic gives no figure; my estimate is 2 to 5 GB.
2. **Google's tools,** at the versions the engine asks for in `Engine/Config/Android/Android_SDK.json`: NDK r27c (27.2.12479018), SDK platform `android-36`, build-tools 36.0.0, CMake 3.22.1, plus platform-tools and the command-line tools. Epic's table for 5.8 names Android Studio Koala (2024.1.2 Patch 1). Android Studio brings its own JDK, and the engine's `Engine/Extras/Android/SetupAndroid.bat` installs the rest through its SDK manager.
   - Android Studio: about 1.2 GB to download, about 3 GB installed.
   - NDK r27c: 781.5 MB to download (the Windows zip), about 2.5 to 3 GB unpacked.
   - SDK platform, build-tools, platform-tools, command-line tools and CMake: about 0.5 GB to download, about 1.5 GB installed.
   - Only without a phone: the emulator and an x86_64 system image, about 2 GB more. The game would then need an x86_64 build too (5.8 builds arm64 by default).
   - **In all: about 2.5 GB to download and 7 GB on disk for Google's tools (4.5 GB and 9 GB with the emulator), plus the engine's Android files.** C: has 106 GB free.

With those in place, step 4 is: the project copy gets Android settings (package name, SDK versions, arm64, ASTC), `RunUAT BuildCookRun -platform=Android -cookflavor=ASTC`, then the `.apk` on a phone over USB with `adb install`, and `stat unit`, `stat memory` and the `.apk`'s size read on the phone. itch.io takes the `.apk` as its own file on the page, and butler pushes it to an `android` channel.

## The web (UE 5.9): what this game would need

Checked on 2026-11-20 against Epic's 5.9 Preview 2 release notes and announcement, and two write-ups of Preview 1. Nothing was installed.

| Need | What Epic's notes say now | What it means for this game |
|---|---|---|
| Engine | The announcement still says "a source build and C++ project". Preview 2's release notes say Blueprint-only projects now package for the web with the standard game executable, and the known issues name launcher-built games, so the Windows launcher build includes the web target. The emsdk toolkit is still needed. | A second engine install (5.9) beside 5.8.4, and emsdk. Our project is Blueprint-only, which Preview 2 allows. |
| Engine version | The web target exists only in 5.9. | Assets saved in 5.9 don't open in 5.8.4. A web build needs a 5.9 copy of the project that never goes back to `dev`, or the whole team moves to 5.9 at its full release. |
| Renderer | The mobile renderer: Mobile Forward (phones), Mobile Deferred, and an experimental desktop tier. Parts of the web renderer are prototypes Epic plans to refactor before 5.9 ships. Nothing says Lumen, Virtual Shadow Maps, ray tracing or Substrate run on the web. | The same look work as Android ("What a mobile look would take"). A mobile look is the first step for both. |
| Memory | Preview 1 crashed above 2 GB of Wasm memory (UE-411671). Preview 2 builds only 64-bit WebAssembly and "supports heaps larger than 2 GB". | Not a blocker once the textures are capped (see above). |
| Download size | itch.io takes browser games up to 500 MB in all and 200 MB per file (Epic's own known issues cite this). | Today's Windows content is one 414 MiB `.ucas`. A web build needs Shipping, the texture cap, smaller music, and content split into files under 200 MB. |
| Files (`Local/`) | Preview 2: "Saved games survive a page reload with an installed engine"; Preview 1 lost saves and settings on reload. Nothing on reading or writing loose files. | The game writes `Local/progress.json` (the first-show flag) and `Local/llm_key.json` (keys), and reads `Local/switches.json` and the loose `Content/NHOS/Data/*.json`. On the web the data JSON goes inside the package, the first-show flag and the Play stats choice move to a SaveGame, the switches drop out, and "Use my own API keys" is left out (see the next row). |
| HTTP and CORS | Nothing in Epic's notes on HTTP or CORS. | Every relay call becomes a cross-origin request from itch.io's HTML5 player. The relay sends no CORS headers today and has no `OPTIONS` route (`Relay/src/index.js`: `POST /`, `GET /health`, `POST /event`, `GET /stats`). It would need `Access-Control-Allow-Origin` for itch.io's player origin and an answer to the preflight for JSON `POST`s. Calling the providers straight from a browser with a player's own keys needs each provider to allow browser calls and puts the keys in browser storage, so a web build offers Test for Free and Play only. |
| Hosting | Opening `index.html` from disk shows "a cross-origin isolation error"; Epic serves it with its own `serve.py`. Web builds can be installed as a progressive web app. | The build wants cross-origin isolation, so on itch.io tick "SharedArrayBuffer support". Under that, the relay's answers need CORS headers too. |
| Browsers | Chrome is the only browser named ("the best experience"). Phones get a lighter texture set; iOS 26 has a memory problem (UE-412148). | Desktop Chrome first. Typing the chat on a phone's on-screen keyboard isn't covered by Epic's notes. |
| Readiness | Preview builds are "unstable until the final release"; Preview 2 had about a week of work and a short QA pass; the full 5.9 release is "next year". Agents wrote the web platform code, starting from UE4's retired HTML5 platform. | No web build before the full 5.9 release. |

Sources: [5.9 release notes](https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-9-release-notes), [5.9 Preview 2 announcement and known issues](https://forums.unrealengine.com/t/preview-2-unreal-engine-5-9-preview/2852840), [indietooling on Preview 1](https://indietooling.com/posts/unreal-5-9-preview-web-export), [Digital Production on the preview](https://digitalproduction.com/2026/11/16/unreal-engine-5-9-preview-agents-canvas-and-a-browser-sized-ambition/), [Epic's Android requirements](https://dev.epicgames.com/documentation/unreal-engine/android-development-requirements-for-unreal-engine), [the NDK r27c release](https://github.com/android/ndk/releases).

## The recommendation

**Android: a go for one more step, not yet for a release.** The pictures say the look is not the risk: the stage reads on the mobile renderer today, and about a task of lighting brings back the house and the shadows. The open risks are the ones a preview can't show: frame rate and memory on a real phone with 2.9 M triangles, and whether a typed-chat game is pleasant on a phone's keyboard. So the next step is to OK the downloads above and package the copy as it is, run it on a phone, and decide then. If that goes well, the tasks are:

1. Android setup on the PC: the engine's Android files, Android Studio, `SetupAndroid.bat`, Android settings in the project, a packaging command in `Docs/Builds.md` and an `android` channel in `Tools/deploy_itch.py`.
2. The mobile look: the house fill, robot shadows (blob or Movable spot), the 1024 texture cap, all through the Android device profiles.
3. Fewer triangles: LODs for the 79 meshes, or a light audience.
4. Touch: no joysticks, a phone-size UI scale, the typed chat with the on-screen keyboard, tap for the hover cards.
5. A check on a phone, then a release with the `.apk` on the itch.io page.

**The web: no-go now; look again at the full 5.9 release (2027).** The target is a preview with prototype parts, it needs a 5.9 copy of the project apart from the team's 5.8.4, and it needs the same mobile look as Android first. If Android goes ahead, most of the web's work is done by then. At the full release, the tasks are:

1. A spike on 5.9 in a separate copy: package the Blueprint-only project for the web, check HTTP to the relay from Chrome, and measure the download.
2. CORS and a preflight answer on the relay for itch.io's player origin.
3. The `Local/` files: data JSON in the package, the first-show flag and Play stats in a SaveGame, no own-keys mode on the web.
4. The size under itch.io's limits (Shipping, files under 200 MB).
5. A decision on moving the whole project to 5.9, or keeping a separate web copy.
