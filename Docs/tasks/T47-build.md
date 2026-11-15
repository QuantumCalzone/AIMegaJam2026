# T47 build sheet: a headpiece for each role

Back to [T47](T47.md) and [the plan](../Plan.md). A Mac prep session wrote this on 2026-11-15, without the editor. It is written against **`noHumansOnSet` at `b88c6a2`** (T44's seven cards are in, `6dbd335`; T45's build sheet is in, T45 itself is not). It is a plan, not a record: nothing in `Content/`, `Tools/`, `Config/` or `Graphs/` changed, and the design doc was read, not changed (Stories tab rev 9, Art Inspiration rev 29).

| File | What it is |
|---|---|
| [T47-build/costumes.json](T47-build/costumes.json) | The draft of the new `Content/NHOS/Data/costumes.json`: 14 headpiece ids (the 13 models, plus the ball cap worn backwards), each with its mesh and its fit on the head. |
| [T47-build/scenes_seats.json](T47-build/scenes_seats.json) | All 35 seats, card by card in `scenes.json` order: role, `headpiece`, `color` (hex), and the doc's color words (for reading only; not copied into the game). |
| [T47-build/make_costumes.py](T47-build/make_costumes.py) | Builds both files from `Docs/PropArt/manifest.json` and its own tables, and writes the seats' `headpiece` and `color` into a `scenes.json` by editing its text (the file keeps its one-line-per-seat form). |

Sources read: `Docs/tasks/T47.md` and its plan entry, `T46.md` (the head), `T43.md` (the fit, the undersides), `T45-build.md`, `T17.md`, `T11.md`, `T01.md`, `Graphs/BP_Robot/{Setup,SetPersona,SetCut,ResetLook,InitHome,EventGraph,Receive,IsDown}.txt`, `Graphs/BP_StageDirector/ResetStage.txt`, `Graphs/BP_Show/{StagePrep,StartFromPrep}.txt`, `Content/NHOS/Data/scenes.json`, `Tools/check_prompts.py`, `Config/DefaultGame.ini`, and the design doc's Stories and Art Inspiration (Costumes, The bots) tabs.

## In short

- **Data:** each seat in `scenes.json` gets `headpiece` (an id) and `color` (sRGB hex). A new `costumes.json` holds the headpieces: mesh, scale, `x`, `z`, `yaw` and `lift` on the robot's head. `make_costumes.py` writes the seats' fields and one `_readme` sentence; the checker gets `costume_problems`.
- **`BP_Robot`:** `SetHeadpiece(Id, Color)` makes a `Hat` static mesh component on the `Rig` the first time (at run time, so the five robots in `L_Stage` need no re-place), loads the mesh from `costumes.json`, sets its transform, colors its `M_Clay` instance from the hex, and lifts the antenna stalk, the topper and the name label by the headpiece's `lift`, so the topper pokes out of the top. An empty id takes it off and lowers them again.
- **Bare-headed at Scene Prep:** `BP_StageDirector.ResetStage` (which T45 already changes, and which runs at Scene Prep) takes every standing robot's headpiece off. A cut robot keeps its own.
- **`BP_Show`** (the PC's chain): one call per robot where the scene starts and each robot gets its seat (`StageSetup`): `SetHeadpiece(seat.headpiece, seat.color)`. Kept separate in part 4, with what to re-check.
- **`Config/DefaultGame.ini`:** `+DirectoriesToAlwaysCook=(Path="/Game/NHOS/Stage/Headpieces")`, for the same reason as T45's prop line.

## Decisions made for my person

My person asked prep sessions to take the task's default or my recommendation on calls that are theirs, and list them here. The T47 session should show this list to my person when it closes the task.

1. **The hex values are mine.** The doc names each color in words ("sandy straw yellow", "moss green"); `make_costumes.py`'s `SEATS` table turns each into an sRGB hex, and `scenes_seats.json` keeps the doc's words beside it. Blacks are very dark grays (#121216 to #2A2A2E), because pure black clay reads as a hole under the stage lights; the white-ish ones are a little warm or cool (#F0E6CC cream, #D9DEE6 silver) because T46 found the spotlight washes bright colors to white.
2. **One color per headpiece.** Every headpiece model is one clay mesh with `MI_Clay_Neutral` (T43), and `SetHeadpiece` colors the whole mesh. Five roles lose a second detail the doc names: the boxer's gold trim, the boss's red hat band, the nosy errand man's black band, the fixer's white band and the dwarf's ginger beard (the dwarf's whole helmet and beard are iron gray). A second color would need a model with two material slots, or a second mesh.
3. **The eldest son's backwards cap is its own id, `ball_cap_back`:** the same model and color input, turned 180°. So `costumes.json` has 14 ids for 13 models. The task's "one of the 13 ids" counts models; the checker counts models too ("every model is worn by some seat"). The other way, a `backwards` flag on the seat, would add a third argument to `SetHeadpiece`.
4. **The headpieces are sized by the head, not by T43's 25 cm.** T46: "scale them by the dome". Each piece's width across the face is set by hand (hats 72 to 90 cm, wigs and hoods 84 to 98 cm, the saucepan 126 cm with its handle), and `make_costumes.py` turns it into scale and height from the manifest's bounds. These are starting points from bounding boxes only: T43 looked at no headpiece from below, and the shapes inside the boxes are unknown. Tune by screenshot (part 5c); a change is a number in `make_costumes.py`, not a graph change.
5. **The topper rises with the hat (`lift`).** The doc: the antenna topper "pokes up through" the hat. A top hat (55 cm tall) or a wizard hat (63 cm) would swallow the halo and the warning light, so `SetHeadpiece` raises the stalk (`Nub`), the topper and the name label by the hat's height above the dome. The bolt can reach about 280 cm under the wizard hat; if that leaves the house camera's frame, lower the wizard hat's and the beanie's height first.
6. **The name label rises too,** by the same `lift`, so a raised topper doesn't run through it. If T38's bubbles anchor on the label, they follow.
7. **Bare-headed in Scene Prep, dressed at the scene's start,** as T47 step 3 says (the Costumes section says both "At Scene Prep each bot puts on its role's headpiece" and "In Scene Prep, before the costumes go on, the bots stand bare-headed"; the task settles it).
8. **The bare-headed call goes in `BP_StageDirector.ResetStage`,** not `BP_Show`: it already loops every robot at Scene Prep, and T45 changes it. This adds `BP_StageDirector.uasset` and `Graphs/BP_StageDirector/ResetStage.txt` to T47's commit, outside its Touches; name them in the commit message. The fallback is a loop over the robots in `BP_Show.StagePrep`.
9. **The `Hat` component is made at run time** (`Add Component by Class`), not added to the Blueprint's components. A template edit doesn't reach the robots in `L_Stage` (T17, T46), so a template component would mean re-placing all five robots and changing `L_Stage`, which is outside T47's Touches.
10. **Cook the headpiece folder** (`Config/DefaultGame.ini`, outside the Touches; name it in the commit). A mesh named only in `costumes.json` is referenced by nothing, so a packaged build would leave it out.
11. **New check lines:** `NHOS: COSTUME <persona> <id> <hex>` when a robot puts a headpiece on, `NHOS: COSTUME <persona> off` when it takes it off, and `NHOS: COSTUME <persona> unknown <id>` or `... mesh missing <path>` on a failure.
12. **No design doc edit.** The doc names each role's piece and color word, and the game follows it. The hex values are the build's, like the seat colors' exact values were T46's.

## 0. Before you start

1. **T45 is done** (plan: T47 follows it, and both change `scenes.json`, `check_prompts.py`, `DefaultGame.ini` and `ResetStage`). Start from what T45 left: its `ResetStage.txt`, its checker, its `DefaultGame.ini`.
2. **The roles haven't moved.** `python Docs/tasks/T47-build/make_costumes.py` checks every card id and role in `Content/NHOS/Data/scenes.json` against its table and stops on an `assert` that names what moved. At `b88c6a2` it says "every role matches".
3. **The head is still T46's.** `git log --oneline -3 -- Graphs/BP_Robot Content/NHOS/Stage/BP_Robot.uasset` shows nothing after `478a76e` (T46). If the robots were rescaled (T46 left that open to T49; T49 didn't), every `z` and `lift` scales with them.
4. **Which way the robot faces.** This sheet takes the robot's face as `Rig` +X (`Receive` puts the back slot at X −38, and `InitHome` aims the actor's forward vector at the camera), so `yaw` 270 turns a Meshy model's face (raw +Y, T43) to it. T43's world yaw of 90 doesn't carry over: inside the robot the frame is the robot's. If the first screenshot shows hats facing backwards, set `FRONT_YAW = 90` in the script and run it again.
5. **The toppers' parents.** With editor Python (T46's way: `SubobjectDataSubsystem.k2_gather_subobject_data_for_blueprint`), print every component tagged `acc`, plus `Nub` and `Label`: its name, its parent, its relative location and its tags. Part 2d's `InitLift` lifts `Nub`, `Label` and each `acc` component whose relative Z is 165 or more. That rule is right only if the toppers hang off `Rig` (or `Head`) directly. If a topper is a child of `Nub`, lifting `Nub` already lifts it: leave it out of the list (lift only a chain's top). Check that the copycat's headset hoop and ear cups and the human's scarf stay out of the list (they sit lower than 165).
6. **The eye line.** Print `EyeL`'s relative location. The dark shades are placed for eyes at about z 116 (their `z`). If the eyes sit elsewhere, change `dark_shades`' `bottom` in `FIT` by the difference.
7. **Locks:** `BP_Robot.uasset`, `BP_StageDirector.uasset`, `BP_Show.uasset` (part 4). `BP_Show` is the PC's chain: take it only when the chain has released it, and pull first.

## 1. Data (step 1)

### 1a. `costumes.json` (new)

Copy [T47-build/costumes.json](T47-build/costumes.json) to `Content/NHOS/Data/costumes.json` (or run the script again after a change and copy its output). Its 14 ids:

| Id | Model | Width × depth × height on the head (cm) | x | z | lift | Worn by (card: seat) |
|---|---|---|---|---|---|---|
| `hood` | `SM_Hood` | 98 × 66 × 105 | −6 | 150.3 | 42.5 | hermit (space), ranger (ring), youngest son (wedding), boxer (diner), slacker (bowling) |
| `dark_shades` | `SM_DarkShades` | 74 × 83 × 28 | −5.3 | 116.3 | 0 | smuggler (space), lawyer (dino), adviser (wedding), chatty errand man (diner), agent (office) |
| `top_hat` | `SM_TopHat` | 72 × 72 × 55 | 0 | 177.7 | 45.4 | park owner (dino), crooner (wedding), fixer (diner), rival bowler (bowling) |
| `bob_wig` | `SM_BobWig` | 84 × 78 × 86 | −4 | 134.9 | 17.7 | homebody (ring), boss's wife (diner), artist (bowling), rebel (office) |
| `ball_cap` | `SM_BallCap` | 74 × 115 × 56 | 20 | 162.9 | 30.8 | tour kid (dino), quiet bowler (bowling) |
| `ball_cap_back` | `SM_BallCap`, yaw 90 | 74 × 115 × 56 | −20 | 162.9 | 30.8 | eldest son (wedding) |
| `wide_brim_hat` | `SM_WideBrimHat` | 90 × 89 × 32 | 0 | 165.8 | 21.6 | farm kid (space), dino expert (dino), leader (office) |
| `saucepan_helmet` | `SM_SaucepanHelmet` | 126 × 76 × 43 | 0 | 149.5 | 10.8 | masked villain (space), teammate (bowling) |
| `wizard_hat` | `SM_WizardHat` | 80 × 78 × 63 | 0 | 181.3 | 52.5 | wizard (ring), fortune-teller (office) |
| `tiara` | `SM_Tiara` | 64 × 74 × 37 | 0 | 158.4 | 0 | princess (space), elf (ring) |
| `fedora` | `SM_Fedora` | 80 × 86 × 36 | 0 | 167.8 | 25.7 | family boss (wedding), nosy errand man (diner) |
| `horned_helmet_beard` | `SM_HornedHelmetBeard` | 85 × 67 × 114 | 4 | 125.1 | 22.2 | dwarf (ring) |
| `dino_hood` | `SM_DinoHood` | 84 × 112 × 86 | 10 | 143.3 | 26.5 | runaway dinosaur (dino) |
| `beanie` | `SM_Beanie` | 76 × 77 × 89 | 0 | 174.5 | 58.8 | office worker (office) |

Every id has `yaw` 270 except `ball_cap_back` (90). **Missing a model: none.** All 13 headpiece meshes are in `Content/NHOS/Stage/Headpieces/` (the script checks each `.uasset`), and every one is worn by at least one seat.

How the numbers come out (the script's comments say the same): the head's top cap is a sphere of radius 35 centered at z 123 in `Rig`, so the dome tops out at z 158 (T46); scale = width ÷ the model's raw X bound; every Meshy model's pivot is its center (`min_z` is minus half its height), so `z` = where its lowest point sits + half its height; `lift` = its top − 160, so the stalk's base (z 156) ends up just under the hat's top; the shades' front sits at x 36, the screen's front.

**Pieces to look at first** (from their bounds, not their shapes):
- `horned_helmet_beard`: the beard hangs under the helmet (T43), down to about z 68, over the screen's lower half. The eyes (about z 116) must stay visible; if they don't, raise `bottom` and shrink `width`.
- `hood`, `bob_wig`, `dino_hood`: their fronts must leave the screen clear. The fringe of the bob and the snout of the dino hood are guesses.
- `saucepan_helmet`: whether the pot is modeled upside down (a helmet) or upright (open on top) is unknown (T43's `underside: unchecked`). If it is upright, add 180 to its pitch (a new `pitch` field and one more pin in `SetHeadpiece`), or flip the mesh in the asset.
- `tiara`: a circlet around the dome; if the model is a front-only arc, move it forward (`x` about 25) and lower it to the screen's top.

### 1b. `scenes.json`

In the repo folder, after T45's change to the same file is in:

```bash
python Docs/tasks/T47-build/make_costumes.py Content/NHOS/Data/scenes.json Content/NHOS/Data/scenes.json
```

It adds `, "headpiece": "<id>", "color": "#RRGGBB"` to each of the 35 one-line seats, and appends one sentence to the end of the `_readme`'s `cards` line: `Each seat's 'headpiece' (an id in costumes.json) and 'color' (sRGB hex) dress the robot that plays it (T47); the game never sends them to the AIs.` `git diff` should show exactly 36 changed lines. The script can run again on its own output (tested: a second run changes nothing), so it is also how a color or headpiece changes later. Every seat's values are in [T47-build/scenes_seats.json](T47-build/scenes_seats.json). Tested on a copy at `b88c6a2`: the checker of that day passes on the result.

**"The game never sends these fields to the AIs":** the AIs' state copies `role` and `want` from a seat by name (T06's `cast [{name, role, want, status}]` and `you {name, role, want, note}`), and the checker's simulated shows do the same (`check_prompts.py` lines 842 to 958 at `b88c6a2`). Check in part 4 that `BP_Show` copies fields by name too and never sends the whole seat object.

### 1c. `Tools/check_prompts.py`

1. **`costume_problems`**, next to T45's `props_file_problems`, called from `check_files` with `costumes = load_json("costumes.json", errors) or {}` and `errors.extend(costume_problems(cards, costumes))`. Tested against the drafts at `b88c6a2`: no error with the costumes, two errors for a made-up headpiece and a color word, and 83 errors on today's `scenes.json` (35 seats × 2, plus 13 unworn models).
   ```python
   def costume_problems(cards, cdata) -> list[str]:
       """costumes.json and each seat's costume (T47): every seat names a known headpiece and a hex
       color; every headpiece has a mesh on disk and a fit; every headpiece model is worn by some seat."""
       out, heads = [], cdata.get("headpieces", {})
       for hid, h in heads.items():
           mesh = h.get("mesh", "") if isinstance(h, dict) else ""
           if not re.fullmatch(r"/Game/[\w/]+\.\w+", mesh):
               out.append(f"costumes.json: headpiece {hid!r} needs a mesh object path (/Game/.../SM_X.SM_X)")
           elif not (ROOT / "Content" / (mesh[6:].rsplit(".", 1)[0] + ".uasset")).exists():
               out.append(f"costumes.json: headpiece {hid!r}'s mesh {mesh} is not in Content/")
           if not all(isinstance(h.get(k), (int, float)) for k in ("scale", "x", "z", "yaw", "lift")) or not h.get("scale", 0) > 0:
               out.append(f"costumes.json: headpiece {hid!r} needs a scale above 0 and numbers for x, z, yaw and lift")
       worn = set()
       for c in cards:
           for x in c.get("seats", []):
               hp, col = x.get("headpiece"), x.get("color", "")
               if hp not in heads:
                   out.append(f"scenes.json: {c.get('id')}'s seat {x.get('role')!r} needs a headpiece from costumes.json, not {hp!r}")
               else:
                   worn.add(heads[hp].get("mesh"))
               if not re.fullmatch(r"#[0-9A-Fa-f]{6}", col or ""):
                   out.append(f"scenes.json: {c.get('id')}'s seat {x.get('role')!r} needs a color like #A8CCFF")
       for m in sorted({h.get("mesh") for h in heads.values() if isinstance(h, dict)} - worn):
           out.append(f"costumes.json: no seat wears {m}")
       return out
   ```
2. **The seat check** (line 625 at `b88c6a2`: "needs 5 seats ..., each with a role and a want") stays as it is.
3. **The docstring:** a paragraph after T44's and T45's: "Costumes (T47): each seat names a headpiece from `costumes.json` and a hex color. The checker fails an unknown headpiece, a color that isn't `#RRGGBB`, a headpiece mesh that isn't on disk and a model no seat wears. The game never sends these fields to the AIs."
4. Run `python Tools/check_prompts.py --offline`. It must pass.

## 2. `BP_Robot` (step 2)

### 2a. Variables

| Variable | Type | Default |
|---|---|---|
| `Hat` | `StaticMeshComponent` object reference | none |
| `CostObj`, `CEntry` | `JsonObjectWrapper` | empty |
| `CostLoaded`, `LiftReady` | Boolean | false |
| `HMesh` | String | "" |
| `HScale`, `HX`, `HZ`, `HYaw`, `HLift` | Float | 1, 0, 0, 0, 0 |
| `LiftComps` | `SceneComponent` object reference, array | empty |
| `LiftBase` | Vector, array | empty |

No component is added to the Blueprint (Decision 9), so the robots in `L_Stage` stay as they are.

### 2b. Nodes to look up first

As in [T45-build.md](T45-build.md) part 2b (`find_node_types` with `context_pins: []`, then `get_node_type_pins`; spell the DSL from what comes back). T47 uses the same soft-load chain (Make Soft Object Path → To Soft Object Reference → Load Asset Blocking → Cast To StaticMesh → Set Static Mesh), and whatever T45 found for the cast holds here. New ones:

| In the DSL below | The Blueprint node |
|---|---|
| `Game|AddComponentbyClass` | Add Component by Class (already used in `BPC_LLMClient.SendReq`; its return value takes the class pin's type, so no cast) |
| `Transformation|AttachComponentToComponent` | Attach Component To Component |
| `Collision|SetCollisionEnabled` | Set Collision Enabled |
| `Utilities|String|Mid`, `Utilities|String|FindSubstring`, `Utilities|String|ToUpper`, `Utilities|String|Replace` | the string nodes |
| `Utilities|Struct|MakeColor`, `Math|Conversions|ToLinearColor(Color)`, `Math|Conversions|ToByte(Integer)` | Make Color (bytes), Color to Linear Color (the sRGB conversion), Integer to Byte |
| `Transformation|GetRelativeLocation` | the component's relative location (the `RelativeLocation` getter) |

### 2c. `LoadCostumes` and `HexColor` (new)

```lisp
(fn LoadCostumes ()
  ; T47: costumes.json, read once per robot.
  (if (V CostLoaded)
    (return))
  (set CostLoaded true)
  (bind (_o _ok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat (Utilities|Paths|GetProjectContentDirectory) "NHOS/Data/costumes.json"))))
  (if (not _ok)
    (print "NHOS: COSTUME costumes.json missing or not valid JSON")
    (return))
  (bind _h (Json|GetField _o "headpieces"))
  (set CostObj _h))
```

```lisp
(fn HexByte (S At)
  ; T47: two hex digits of S, from At, as a byte. A bad digit counts as 0.
  (bind _d "0123456789ABCDEF")
  (bind _hi (Utilities|String|FindSubstring :SearchIn _d :Substring (Utilities|String|Mid :SourceString S :Start At :Count 1)))
  (bind _lo (Utilities|String|FindSubstring :SearchIn _d :Substring (Utilities|String|Mid :SourceString S :Start (+ At 1) :Count 1)))
  (return (Math|Conversions|ToByte(Integer) (+ (* (max _hi 0) 16) (max _lo 0)))))

(fn HexColor (Hex)
  ; T47: "#E3C770" -> linear color. Color to Linear Color does the sRGB conversion, so
  ; HexColor("#A8CCFF") is about (0.39, 0.60, 1.0), OpenAI's seat color in SetPersona.
  (bind _h (Utilities|String|ToUpper (Utilities|String|Replace :SourceString Hex :From "#" :To "")))
  (return (Math|Conversions|ToLinearColor(Color) (Utilities|Struct|MakeColor :R (CallFunction|HexByte :S _h :At 0) :G (CallFunction|HexByte :S _h :At 2) :B (CallFunction|HexByte :S _h :At 4) :A 255))))
```

Mark `HexByte` and `HexColor` pure if the DSL lets you; they are fine as plain functions too. If a string literal can't be bound (`(bind _d "...")`), put the digits in a String variable `HexDigits` with that default.

### 2d. `InitLift`, `LiftTop` and `MakeHat` (new)

```lisp
(fn InitLift ()
  ; T47: what rises with a hat, and where each part sits bare-headed. Check the list in part 0 step 5.
  (if (V LiftReady)
    (return))
  (set LiftReady true)
  (add (V LiftComps) (Variables|Default|GetNub))
  (add (V LiftComps) (Variables|Default|GetLabel))
  (for _c (Actor|GetComponentsByClass :ComponentClass "/Script/Engine.StaticMeshComponent")
    (if (and (Components|ComponentHasTag :self _c :Tag "acc") (>= (.z (Transformation|GetRelativeLocation :self _c)) 165.0))
      (add (V LiftComps) _c)))
  (for _c (V LiftComps)
    (add (V LiftBase) (Transformation|GetRelativeLocation :self _c))))

(fn LiftTop (Lift)
  (for _i (range (len (V LiftComps)))
    (Transformation|SetRelativeLocation :self (get (V LiftComps) _i) :NewLocation (+ (get (V LiftBase) _i) (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z Lift)))))

(fn MakeHat ()
  ; T47: the Hat component, made once, on the Rig, so it bobs, hops and slumps with the body.
  (Utilities|IsValid (V Hat)
    (:"Is Valid")
    (:"Is Not Valid"
      (bind _c (Game|AddComponentbyClass self "/Script/Engine.StaticMeshComponent" :bManualAttachment true))
      (set Hat _c)
      (Transformation|AttachComponentToComponent :self (V Hat) :Parent (V Rig) :LocationRule "KeepRelative" :RotationRule "KeepRelative" :ScaleRule "KeepRelative" :bWeldSimulatedBodies false)
      (Collision|SetCollisionEnabled :self (V Hat) :NewType "NoCollision"))))
```

- `Nub` keeps its rotation (the human's bent antenna, set in `SetPersona`); only its location moves.
- `InitLift` must run after `InitHome` has set `Label` to absolute rotation (it doesn't touch rotation, so the order only matters for reading), and before any lift. `SetHeadpiece` calls it first.
- If the robot's `Rig` variable is named differently in the DSL (`(Variables|Default|GetRig)` in `ResetLook`), use that form.

### 2e. `SetHeadpiece(Id, Color)` (new)

```lisp
(fn SetHeadpiece (Id Color)
  ; T47: put on headpiece Id (an id in costumes.json) in Color (sRGB hex), or take it off ("").
  ; The stalk, the topper and the label rise by the headpiece's lift, so the topper pokes out of it.
  (CallFunction|InitLift)
  (CallFunction|LoadCostumes)
  (bind _tag (Utilities|String|StringToName Id))
  (bind _has (and (not (Utilities|String|IsEmpty Id)) (Json|HasField (V CostObj) _tag)))
  (if (not _has)
    (Utilities|IsValid (V Hat)
      (:"Is Valid" (Rendering|SetVisibility :self (V Hat) :bNewVisibility false :bPropagateToChildren false))
      (:"Is Not Valid"))
    (CallFunction|LiftTop :Lift 0.0)
    (print (cat "NHOS: COSTUME " (Variables|Default|GetPersonaId) (select (Utilities|String|IsEmpty Id) " off" (cat " unknown " Id))))
    (return))
  (bind _e (Json|GetField (V CostObj) _tag))
  (set CEntry _e)
  (bind _m (Json|GetField (V CEntry) "mesh"))
  (set HMesh _m)
  (bind _s (Json|GetField (V CEntry) "scale"))
  (set HScale _s)
  (bind _x (Json|GetField (V CEntry) "x"))
  (set HX _x)
  (bind _z (Json|GetField (V CEntry) "z"))
  (set HZ _z)
  (bind _y (Json|GetField (V CEntry) "yaw"))
  (set HYaw _y)
  (bind _l (Json|GetField (V CEntry) "lift"))
  (set HLift _l)
  (CallFunction|MakeHat)
  (bind _obj (Utilities|LoadAssetBlocking :Asset (Utilities|ToSoftObjectReference (Utilities|MakeSoftObjectPath :PathString (V HMesh)))))
  (bind _mesh (cast StaticMesh _obj))
  (Components|StaticMesh|SetStaticMesh :self (V Hat) :NewMesh _mesh)
  (Transformation|SetRelativeScale3D :self (V Hat) :NewScale3D (Math|Vector|MakeVector :X (V HScale) :Y (V HScale) :Z (V HScale)))
  (Transformation|SetRelativeLocation :self (V Hat) :NewLocation (Math|Vector|MakeVector :X (V HX) :Y 0.0 :Z (V HZ)))
  (Transformation|SetRelativeRotation :self (V Hat) :NewRotation (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw (V HYaw)))
  (Rendering|Material|SetVectorParameterValueonMaterials :self (V Hat) :ParameterName "Color" :ParameterValue (Math|Conversions|ToVector(LinearColor) (CallFunction|HexColor :Hex Color)))
  (Rendering|SetVisibility :self (V Hat) :bNewVisibility true :bPropagateToChildren false)
  (CallFunction|LiftTop :Lift (V HLift))
  (print (cat "NHOS: COSTUME " (Variables|Default|GetPersonaId) " " Id " " Color)))
```

- `SetVectorParameterValueOnMaterials` makes a dynamic instance of each slot's `MI_Clay_Neutral` (T11), so each robot's hat has its own color and `Color` is `M_Clay`'s parameter (T43).
- **A missing mesh:** `Set Static Mesh` with no mesh shows nothing. Add a print like T45's (`NHOS: COSTUME <persona> mesh missing <path>`) on an `IsValid` of `_mesh`, the same way T45 does it.
- **The cut keeps the hat:** `SetCut` and `ResetLook` color only named parts and never touch `Hat`, so a cut robot slumps in its costume, colored as it was. Nothing to change.
- **The talking bounce, hops, cheer, shake and slump** move `Rig`, so the hat moves with the head.
- Optional, if time allows: a quick pop when the hat goes on (scale from 0.6 to 1 over 0.2 s in `EventTick`). Not in the task.

Save `Graphs/BP_Robot/{SetHeadpiece,LoadCostumes,HexByte,HexColor,InitLift,LiftTop,MakeHat}.txt` as written.

## 3. Bare-headed at Scene Prep: `BP_StageDirector.ResetStage` (step 3, first half)

Start from **T45's** `Graphs/BP_StageDirector/ResetStage.txt` (T45 adds the props loop; see [T45-build.md](T45-build.md) part 3a). Change only the robots' loop:

```lisp
  (for _b (V AllBots)
    (Class|BPRobot|GoHome :self _b)
    ; T47: every robot still standing takes its headpiece off for Scene Prep; a cut robot keeps its own.
    (if (not (Class|BPRobot|IsDown :self _b))
      (Class|BPRobot|SetHeadpiece :self _b :Id "" :Color "")))
```

`ResetStage` runs from `BP_Show.StagePrep` at every Scene Prep, before the prep card shows, so the robots stand bare-headed while I read my card. If T45 isn't in yet, make the same change on the pushed `ResetStage.txt` (the loop is the same).

## 4. Dressed at the scene's start: `BP_Show` (step 3, second half) — the PC's chain

**Re-check against the `Graphs/BP_Show/` sources of that day.** At `b88c6a2` the graphs this part needs have no source file: the deal of the card's seats to the actors (in `ScenePrep`, which prints `NHOS: SETUP`) and `StageSetup`, which gives each robot its seat name at `PREP start` (T46: "`StageSetup` runs at `PREP start`"; `StartFromPrep.txt` calls `StartScene`). T52, T54, T55, T57 and T58 run on the PC before T47 and may change both. So, on the day:

1. `find_nodes` with title `Setup` in `BP_Show` (T28: titles match without spaces): the call that sets each robot's name and color (`BP_Robot.Setup(Name, Color, IsMe)`). Read only the graph it is in (expected: `StageSetup`). There the graph has, for each actor on stage, its robot and its seat index.
2. Find where that actor's dealt seat is kept: `find_nodes` for `GetField` with `role` in `ScenePrep` (or the graph that prints `NHOS: SETUP`). T06 lists the state's `you {name, role, want, note}`, so `BP_Show` keeps each actor's role and want somewhere (per-actor arrays, or the seat object). Confirm there that `role` and `want` are copied by name and the whole seat object never goes into a state (1b).
3. Add the call **right after `Setup`** for each robot, in one of two shapes:
   - **If the actor's seat object is at hand** (a `JsonObjectWrapper`):
     ```lisp
     (bind _hp (Json|GetField <seat> "headpiece"))
     (Variables|Default|SetHatId _hp)
     (bind _hc (Json|GetField <seat> "color"))
     (Variables|Default|SetHatColor _hc)
     (Class|BPRobot|SetHeadpiece :self <robot> :Id (Variables|Default|GetHatId) :Color (Variables|Default|GetHatColor))   ; T47
     ```
     with two new String variables, `HatId` and `HatColor` (T01: a JSON value goes through a typed variable).
   - **If only role and want were kept** (per-actor String arrays): add two String arrays, `ActorHat` and `ActorHatColor`, filled at the same spot and from the same seat as the role (`GetField "headpiece"`, `GetField "color"`), then in `StageSetup`: `(Class|BPRobot|SetHeadpiece :self <robot> :Id (get (V ActorHat) <i>) :Color (get (V ActorHatColor) <i>))`.
4. Save the graph files of the graphs you wrote (both have none today: write each one's source from a read of the graph, per `Graphs/README.md`, and commit it).

If writing a whole graph is too risky on the day, put the nodes in by hand (as T18 did in `SetupShow`) and record that in the graph's file. Nothing else in `BP_Show` changes for T47.

## 5. The check (step 4)

### 5a. A free autoplay show in a game window (the saved assets)

`Local/switches.json` as for T45's run (`"autoplay": true`, `"mode": "free"`, `"spare_human": true`, `"fast_lines": true`, `"ai_seats": 0`), so a show plays all its scenes. With the editor's assets saved (T27's Mac command):

```bash
"/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor" "<PROJECT>" -game -windowed -ResX=1600 -ResY=900 -log=T47.log
```

```bash
grep -E "NHOS: (SETUP|PREP (shown|start)|COSTUME|SHOW END)" ~/Library/Logs/AIMegaJam2026/T47.log
grep -c "LogScript" ~/Library/Logs/AIMegaJam2026/T47.log
```

Expected, per scene (`<…>` varies):

```
NHOS: SETUP human=human scene=<card id> ...
NHOS: COSTUME <persona> off                      (one per standing robot, from ResetStage)
NHOS: PREP shown scene=<n>
NHOS: PREP start scene=<n>
NHOS: COSTUME <persona> <headpiece id> <#hex>    (one per actor on stage)
...
NHOS: SHOW END result=<win|lose> scenes=<n>
```

It passes when: the show reaches `SHOW END`; each scene has an `off` line for every standing robot before `PREP shown` and a `COSTUME <id>` line for every actor on stage after `PREP start`; each scene's ids and colors are that card's (compare with `scenes_seats.json`); a cut robot gets no `off` line in later scenes; no `unknown` or `mesh missing` line; and no `LogScript` line.

### 5b. Screenshots

The Done-when: all five bots in costume in two different scenes. Scene 1 has five actors on stage; scene 2 has four plus the cut one slumped in its costume, which shows the "keeps its headpiece" part.

- From the house camera: Scene Prep (bare-headed), the first turn of scene 1 (five in costume), and the first turn of scene 2 (a different card's costumes, and the cut robot still in its hat).
- Close-ups of each robot's head, from the editor (PIE, `SlateInspectorToolset.Screenshot`, T46's way) if the game-window capture is black (T46: a locked Mac screen gives black images).
- Save them to `Saved/T47/shots/` (not in git).

### 5c. Judge, and tune

As a first-time player: can I tell the roles apart, and does each costume read as its role (the wizard's hat, the dwarf's helmet, the villain's saucepan)? Then per headpiece:

- **It floats, sinks or tilts:** change its `bottom` (and `x`) in `make_costumes.py`'s `FIT`, run the script, and copy `costumes.json` again. No graph change, and no editor restart: `LoadCostumes` reads the file at each show's start (a new game window).
- **It covers the eyes:** the dwarf, the bob wig and the hoods are the likely ones (1a).
- **The topper doesn't poke out, or floats above the hat:** change `lift` (the script's rule is the hat's top − 160).
- **The color washes out under the spotlight** (the cream top hat, the silver tiaras, the sky-blue cap): darken that seat's hex a step in `SEATS` and run the script in place again (1b). A re-run rewrites every seat's `headpiece` and `color` and adds the `_readme` sentence only once, so it changes only what moved in `SEATS`.
- **The bolt or the label leaves the frame** under the wizard hat or the beanie: lower those hats (Decision 5).

Write what the screenshots showed under T47's "## Findings", including what wasn't checked.

## 6. What T47 commits

`Content/NHOS/Data/costumes.json`, `Content/NHOS/Data/scenes.json`, `Tools/check_prompts.py`, `Config/DefaultGame.ini` (Decision 10), `BP_Robot.uasset`, `BP_StageDirector.uasset` (Decision 8), `BP_Show.uasset`, the `Graphs/` files of part 2, 3 and 4, the plan, `T47.md` and `DevLog.md`, as "How to run a task" lists. `Docs/Assets.md` needs no line: every headpiece model is T43's and already listed.
