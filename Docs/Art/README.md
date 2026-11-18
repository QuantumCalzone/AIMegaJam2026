# New art: every art asset in the game

On 2026-11-15 my person asked to replace all the art in the game. On 2026-11-16 they set the scope to everything. This file lists every art asset the game shows today, grouped by the task that redraws it, and names the task that replaces each asset in the game. T94 wrote the list on 2026-11-17. The direction and the style guide that every new piece follows are in [Direction/README.md](Direction/README.md).

| Group | Concepts (approved by my person) | Replaced in the game by |
|---|---|---|
| The cast, me included | T95 → `Docs/Art/Cast/` | T103 (models) |
| The costumes | T96 → `Docs/Art/Costumes/` | T104 (models) |
| The story props | T97 → `Docs/Art/Props/` | T105 (models) |
| The theater, its set pieces and the audience | T98 → `Docs/Art/Set/` | T106 (models and the level) |
| The 2D art: backdrops, the stagehand, the burning bills | T99 → `Docs/Art/2D/` | T99 (generated and imported) |

Each group's old assets stay in the game until its import task replaces them, so the game stays playable throughout.

**How the list was checked:** against every file in `Content/NHOS/Stage/` and `Content/NHOS/UI/`, against [Assets.md](../Assets.md), and against the task files that built the engine-shape parts (T11, T17, T19, T45 to T49, T53, T61, T75, T79 to T83, T86, T88) and the graph sources in `Graphs/BP_Robot/` and `Graphs/BP_Backdrop/`. The `.uasset` files were not opened. Where a doc doesn't name a part's material, or it isn't clear whether a part still shows, the row says so.

Content paths below are under `Content/NHOS/`. "Engine shapes" means parts built in the editor from `/Engine/BasicShapes/`, with our own materials. These parts have no asset file of their own.

## 1. The cast (T95, then T103)

All of it lives in `Stage/BP_Robot`, one Blueprint for the five seats.

### Generated models

They were made in Hyper3D Rodin (T81) from the concept art in `Docs/BotArt/`, and imported by T82 and T83. Each folder holds the `SM_`, `M_` and `MI_` assets with their `T_*_BaseColor`, `_Normal` and `_Roughness` textures.

| Asset | Made from | Notes |
|---|---|---|
| `Stage/Cast/RoundHead/SM_RoundHead` | `Docs/CastArt/round_head/` (from `Docs/BotArt/openai.png`) | The shared head shell of OpenAI, Anthropic and SpaceXAI, tinted per seat. |
| `Stage/Cast/openai/SM_OpenAIBody`, `SM_OpenAIArm` | `Docs/CastArt/openai/body/`, `arm/` | |
| `Stage/Cast/anthropic/SM_AnthropicBody`, `SM_AnthropicArm` | `Docs/CastArt/anthropic/body/`, `arm/` | |
| `Stage/Cast/spacexai/SM_SpaceXAIBody`, `SM_SpaceXAIArm` | `Docs/CastArt/spacexai/body/`, `arm/` | |
| `Stage/Cast/meta/SM_MetaBody`, `SM_MetaArm` | `Docs/CastArt/meta/body/`, `arm/` | |
| `Stage/Cast/meta/SM_MetaHead` | `Docs/CastArt/meta/head/` | Imported but not used. T83 kept T80's engine head. |
| `Stage/Cast/you/SM_YouHead`, `SM_YouBody`, `SM_YouArm` | `Docs/CastArt/you/head/`, `body/`, `arm/` | Also `M_YouHead_*` (three materials), `MI_YouHeadPaint` and `T_YouHead_Paint` (a flat teal, T83). |

### Engine-shape parts on the robots

| Part | Seat | Built by |
|---|---|---|
| `Face`: `EyeL`, `EyeR` (spheres) and `Mouth` (cube), on `M_Robot` with its `Glow` parameter | all | T46, T79 |
| Emotion parts made at BeginPlay: `EmBrowL`/`R`, `MouthCL`/`CR` (`Graphs/BP_Robot/FaceSetup.txt`) | all | T75 |
| Resting brows: `BrowWL`/`WR` (Anthropic), `BrowAL`/`AR` (SpaceXAI) | Anthropic, SpaceXAI | T79 |
| `Visor` (dark `M_Robot`, in the head model's screen recess), `Collar` (`MI_Clay_Gold`), `EarL`/`R` (`MI_Clay_Cream`), antenna stalk `Nub` | round-head seats (collar also on Meta, ears also on mine) | T46, T79, T82 |
| Halo `Halo0`–`Halo11` (no doc names its material) and floor ring `Ring0`–`Ring11` (`MI_HaloGlow`, tag `ring`) | OpenAI | T17, T79 |
| Glasses `RimL`/`R` (gold), `LensL`/`R` (`MI_Robot_Screen`), `Bridge`, `TempleL`/`R` (tag `glasses`); the warning light `WarnDome` | Anthropic | T17, T79 |
| `SNose`, `SNoseTip`, `Teeth` with `TGap0`–`2`; the bolt `Bolt0`–`2` | SpaceXAI | T17, T79 |
| The whole head: `MHead`, `MNose`, `MEarL`/`R` (`MI_Clay_Doll`); glasses `MGlassL`/`R`, `MBrowBar`, `MBridge`, `MTempleL`/`R` (`MI_Clay_Black`) with camera dots `MCamL`/`R`; `Smile` (charcoal); chain `Chain0`–`8` (gold) | Meta | T80, kept by T83 |
| `Wire`, `PingPong`; scarf `ScarfA`, `ScarfB`, `ScarfTail`, `ScarfStripe`; pupils `PupilL`/`R`; marker strokes `InkL`/`R`; eye-slot backing plates `SlotL`/`R` | me | T46, T80, T83 |
| `Label`: the 3D TextRender name tag at z 228, with the red AI or HUMAN stamp on the cut and T57's "(passed)" line | all | T11, T57 |
| `Spot`: the SpotLight that lights while a robot talks | all | T11 |

### Cast materials

These live in `Stage/` and `Stage/Materials/`: `M_Robot`, `M_CastModel`, `MI_Robot_Screen`, `MI_HaloGlow`, `MI_AmberGlow`, `MI_SmileGlow`, `MI_Clay_Gold`, `MI_Clay_Cream`, `MI_Clay_Doll`, `MI_Clay_Black`, `MI_Clay_Charcoal`, `MI_Clay_Knit`, `MI_Clay_Glove`, `MI_Clay_Denim`, `MI_Clay_Tape`, `MI_Clay_Seat`, `MI_Clay_White`, `MI_Cardboard`, `MI_Teal`, `MI_ScarfRed` and `MI_ScarfCream`. They are grouped by name: only the editor's Reference Viewer can confirm which parts use them. Check it before T103 deletes any.

**Since T94:** OpenAI has no halo and no floor ring. My person decided this in T94's round 4 (see [Direction/README.md](Direction/README.md)). T95 draws OpenAI without them, and T103 removes `Halo*` and `Ring*`.

## 2. The costumes (T96, then T104)

There are 13 headpiece models, made with Leonardo images, then Meshy image to 3D (T40), and imported by T43. T47's `Data/costumes.json` dresses all 35 roles from them (14 ids). Each robot puts one on a `Hat` part, made at run time on its `HeadSocket`. The color comes from `Stage/Materials/M_Clay` and its `MI_Clay_*` instances.

| Asset | Made from |
|---|---|
| `Stage/Headpieces/SM_Hood` | `Docs/PropArt/hood/` |
| `Stage/Headpieces/SM_DarkShades` | `Docs/PropArt/dark_shades/` |
| `Stage/Headpieces/SM_TopHat` | `Docs/PropArt/top_hat/` |
| `Stage/Headpieces/SM_BobWig` | `Docs/PropArt/bob_wig/` |
| `Stage/Headpieces/SM_BallCap` | `Docs/PropArt/ball_cap/` |
| `Stage/Headpieces/SM_WideBrimHat` | `Docs/PropArt/wide_brim_hat/` |
| `Stage/Headpieces/SM_SaucepanHelmet` | `Docs/PropArt/saucepan_helmet/` |
| `Stage/Headpieces/SM_WizardHat` | `Docs/PropArt/wizard_hat/` |
| `Stage/Headpieces/SM_Tiara` | `Docs/PropArt/tiara/` |
| `Stage/Headpieces/SM_Fedora` | `Docs/PropArt/fedora/` |
| `Stage/Headpieces/SM_HornedHelmetBeard` | `Docs/PropArt/horned_helmet_beard/` |
| `Stage/Headpieces/SM_DinoHood` | `Docs/PropArt/dino_hood/` |
| `Stage/Headpieces/SM_Beanie` | `Docs/PropArt/beanie/` |

**A dependency to watch:** the audience also wears `SM_TopHat`, `SM_Beanie` and `SM_Fedora` (section 4). T104 deletes `Stage/Headpieces/`, so T106 must give the audience its own hats, or T104 must keep those three, or the audience goes bare-headed.

## 3. The story props (T97, then T105)

`Data/props.json` lists 28 props, four per story card. At each Scene Prep, `BP_Prop`'s `Prop1` to `Prop4` on the Prop Table are dressed with the card's models (T45). Leonardo made the images and Meshy made the models (T39, T41), and T43 imported them. Each prop has an `SM_`, an `M_` and a `T_*_BaseColor` in `Stage/Props/<card id>/`, and its source in `Docs/PropArt/<prop id>/`.

| Card (folder) | Props (spare last) |
|---|---|
| `space_plans` | `SM_TinCanRobot`, `SM_GlowStickSword`, `SM_ToyBlaster`, `SM_PiggyBank` |
| `mine_bridge` | `SM_CursedRing`, `SM_GlowingStaff`, `SM_WaterBucket`, `SM_FryingPan` |
| `dino_island` | `SM_DinoEgg`, `SM_MeatyDrumstick`, `SM_SafetyWaiver`, `SM_DinoPlush` |
| `favor_father` | `SM_PlushHorseHead`, `SM_CannoliTray`, `SM_WeddingEnvelope`, and the bowl of oranges: an engine sphere at scale 0.3 in `MI_PropOrange`, with no model (`Docs/PropArt/bowl_of_oranges/` has no FBX) |
| `glowing_briefcase` | `SM_GlowingBriefcase`, `SM_GoldPocketWatch`, `SM_GiantMilkshake`, `SM_GiantCheeseburger` |
| `league_night` | `SM_RolledUpRug`, `SM_BowlingBall`, `SM_RansomBag`, `SM_MilkCarton` |
| `pick_a_pill` | `SM_RedPill`, `SM_BluePill`, `SM_RingingPhone`, `SM_BentSpoon` |

**Hidden leftovers, never seen in a show:** T19's eight shape props (sword, cape, crown, rose, ray gun, teacup, rubber chicken and scroll) are still in `BP_Prop`. They show only for a prop name that isn't in `props.json`. T105 may delete them, with their materials (`MI_PropYellow`, `MI_ToyRed`, `MI_Paper`, `MI_Cloth` and others; check the Reference Viewer first).

## 4. The theater, its set pieces and the audience (T98, then T106)

### The house in `Maps/L_Stage`, from engine shapes

| Part | Built by |
|---|---|
| `StageFloor`, the plank floor (`M_Set` draws the planks in HLSL) | T17 |
| The gold apron trim and 9 footlights | T17 |
| The gold proscenium columns, 7 velvet pleats each side, and the valance with its gold fringe | T17 |
| The black masking and `StageWall` | T17 |
| The gunmetal truss with 5 spot cans | T17 |
| The Riser with its step, and the cloth-covered Prop Table | T17 |
| The cherub plinths (gold cubes), and the dark-wood wall with a gold strip behind the boxes | T49 |
| Stalls row A: 13 crimson cube seat backs and a gold rail | T49 |
| Stalls rows B to D, on black decks | T86 |
| 7 `Stage/BP_PlaceMark` actors. The docs list them only as spots; it isn't clear whether they show a shape. | T15, T17 |

### Generated set pieces

They were made with Leonardo, then Meshy (T42), and imported by T43. Each has an `M_` and a `T_*_BaseColor`.

| Asset | Made from | Notes |
|---|---|---|
| `Stage/Set/SM_Chandelier` | `Docs/PropArt/chandelier/` | Hangs at (−500, 0, 411), tinted gold, with glowing candles (T49). |
| `Stage/Set/SM_Cherub` | `Docs/PropArt/cherub/` | On the proscenium plinths (T49). |
| `Stage/Set/SM_TheaterBox` | `Docs/PropArt/theater_box/` | The horseshoe boxes, repeated down both sides (T49). |

### The backdrop flat

`Stage/BP_Backdrop` is a 13 × 6.2 m cube with `Stage/M_Backdrop`, showing the card's painted texture (section 5). T17's cardboard cutouts are still inside it, but they are hidden for every backdrop id in use (`Graphs/BP_Backdrop/ShowBackdrop.txt`). T106 may delete them.

### The audience

`Stage/Set/BP_AudienceBot` was built from engine shapes in T49. It is a smaller copy of T46's pill robot:

- `Body` and `Head`, in `MI_Clay_AudRose`, `AudPlum`, `AudMustard`, `AudBrick` or `AudLilac`
- `BodyLow` and `CapLow` in cream, and a `Seam`
- `Visor` (`MI_Aud_Screen`), `EyeL` and `EyeR` (`MI_Aud_Eye`), `FootL` and `FootR`
- two hidden gold opera-glass cylinders
- a `Hat` part holding `SM_TopHat`, `SM_Beanie` or `SM_Fedora` in charcoal

There are 49 bots in all: 41 in the four stalls rows (46 seats) and 8 in the boxes. They wear 21 top hats, 5 beanies and 2 fedoras, and 6 wear no hat. From row B back, they hide the parts that can't be seen from behind (T86).

### Lights and the house glow

The lights are part of the look, so T106 tunes them to the new direction:

- From T11: `KeyLight` and `FillLight`
- From T17: `FrontWash`, `RimPink`, `RimCyan`, the three `FootGlow` and two `BackdropWash` lights, and the `StagePost` exposure volume
- From T86: `SM_HouseGlow`

### Set materials

These are `Stage/M_Set` and `M_Backdrop`, the `MI_Theater_*` instances (`Black`, `Cloth`, `Gold`, `Gunmetal`, `Velvet`, `Wood`, `WoodDark`), and `MI_Velvet`, `MI_Wood`, `MI_WoodDark`, `MI_Gold`, `MI_Gunmetal`, `MI_Black`, `MI_White`, `MI_FootGlow`, `MI_Clay_Aud*`, `MI_Aud_Screen` and `MI_Aud_Eye`. `Stage/MI_StageFloor` and `MI_StageWall` are T11's, and T17 and T49 probably replaced them. Many other instances in `Stage/Materials/` belong to T17's hidden backdrop cutouts or T19's hidden props: `MI_Sand`, `MI_SandDark`, `MI_Moon`, `MI_Ocean`, `MI_Leaf`, `MI_LeafDark`, `MI_Ivy`, `MI_Stone`, `MI_Ice`, `MI_Mud`, `MI_Rust`, `MI_SunGlow`, `MI_Sun2Glow`, `MI_StarGlow`, `MI_NeonGlow`, `MI_FogGlow`, `MI_FireGlow`, `MI_MeterGlow`, `MI_Book*`, `MI_BannerRed`, `MI_Hazard`, `MI_Headset`, `MI_Copper` and `MI_Rubber`. All of this is grouped by name. Check users in the Reference Viewer before deleting any.

## 5. The 2D art (T99)

| Asset | Made from | Made by |
|---|---|---|
| `Stage/Backdrops/T_Backdrop_desert_planet` | `Docs/BackdropArt/desert_planet.png` | Leonardo, T48 |
| `Stage/Backdrops/T_Backdrop_dwarf_mine` | `Docs/BackdropArt/dwarf_mine.png` | Leonardo, T48 |
| `Stage/Backdrops/T_Backdrop_jungle_park` | `Docs/BackdropArt/jungle_park.png` | Leonardo, T48 |
| `Stage/Backdrops/T_Backdrop_garden_wedding` | `Docs/BackdropArt/garden_wedding.png` | Leonardo, T48 |
| `Stage/Backdrops/T_Backdrop_retro_diner` | `Docs/BackdropArt/retro_diner.png` | Leonardo, T48 |
| `Stage/Backdrops/T_Backdrop_bowling_lanes` | `Docs/BackdropArt/bowling_lanes.png` | Leonardo, T48 |
| `Stage/Backdrops/T_Backdrop_midnight_cubicles` | `Docs/BackdropArt/midnight_cubicles.png` | Leonardo, T48 |
| `UI/Stagehand/T_Stagehand_Portrait`, in `UI/WBP_Earpiece` (which draws its own rose ring) | `Docs/StagehandArt/portrait_256.png`, cropped from `stagehand.png` | Leonardo, T61 |
| `UI/MoneyBurn/T_Bill`, `T_BillChar` | `Docs/MoneyBurnArt/bill.png`, `bill_char.png` | Our script `makeart.swift`, T35 |
| `UI/MoneyBurn/T_FlameSheet`, `T_Ember` | `Docs/MoneyBurnArt/flame_sheet.png`, `ember.png` | Kenney Particle Pack (CC0), recolored, T35 |
| `UI/MoneyBurn/T_Logo_anthropic`, `_openai`, `_xai`, `_meta` | `Docs/MoneyBurnArt/logo_*.png` | Our script `make_badges.ps1`, T36 |

The bill textures are used in `UI/WBP_BurningBill`, inside `UI/WBP_MoneyBurn`. The embers are UMG images, not particles. The game has no Niagara assets.

## Not replaced by T95 to T106

These pieces show on screen but aren't art assets. They stay as they are, or another task owns them.

- **The UI's drawn parts:** panels, buttons, speech bubbles (`UI/WBP_SpeechBubble`), the chat, the action builder, the clapperboard (UMG stripes in `WBP_Stage`'s `ClapperBox`, T53) and the note clue (text only, T88). `UI/Style/UIStyle` draws them as rounded boxes, with no images. Their look is the design doc's UI section, and T84 and T34 change it. The UI section's palette shares the seat colors with the cast (see the style guide).
- **The fonts:** `UI/Fonts/F_UI` (Roboto) and `F_Emoji` (Noto Color Emoji).
- **Outside the game:** the itch.io cover (`Docs/ItchMedia/cover.png`) shows the old cast. No task redraws it yet. The design doc's pictures (`Docs/Design/images/ArtInspiration/`) are replaced section by section: T94 replaces the mood images, and T95 to T99 replace the pictures in their sections.
