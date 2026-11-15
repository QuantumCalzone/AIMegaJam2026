# T45 build sheet: each card's props on the prop table

Back to [T45](T45.md) and [the plan](../Plan.md). A Mac prep session wrote this on 2026-11-15, without the editor. It is written against **`noHumansOnSet` at `407a9e6`** (T36, T53 and T49 are in; T44 is not). It is a plan, not a record: nothing in `Content/`, `Tools/`, `Config/` or `Graphs/` changed.

The cards' props first came from **T44's draft**, [T44-build/scenes.json](T44-build/scenes.json). **Re-checked at `6c702b3`, after T44 landed (`6dbd335`):** `make_props.py` on the real `Content/NHOS/Data/scenes.json` gives the same `props.json` byte for byte, the seven cards are the draft's, and the two `_readme` sentences and the `card_prop_problems(cards, s.get("props", []))` line (line 634 of the checker) that part 5 changes are there as quoted. Part 0 says how to check again on the day.

| File | What it is |
|---|---|
| [T45-build/props.json](T45-build/props.json) | The draft of the new `Content/NHOS/Data/props.json`: the 28 card props, each with its mesh, scale, yaw, height and grip, and the one prop with no model. |
| [T45-build/make_props.py](T45-build/make_props.py) | Builds that file from a `scenes.json` and `Docs/PropArt/manifest.json`. The size of each prop on stage (`SIZE_CM`) is its only hand-set value. |

Sources read: `Docs/tasks/T45.md` and its plan entry, `Docs/tasks/T43.md` (the fit), `T44-build.md` and its drafts, `T19.md` (the props), `T17.md` (re-place), `T46.md`, `T01.md` (DSL rules), `Graphs/BP_Prop/*`, `Graphs/BP_StageDirector/{ResetStage,FindProp,Init}.txt`, `Graphs/BP_Robot/{Receive,ToTable,DropAll,GoHome}.txt`, `Graphs/BP_Show/StagePrep.txt`, `Graphs/BPC_LLMClient/FreeReply.txt`, `Tools/check_prompts.py`, `Config/DefaultGame.ini`.

## In short

- **`props.json`** (new, in `Content/NHOS/Data/`): an object keyed by the prop's name. 27 props have a model; the **bowl of oranges** has none (T43 skipped it: `core: false`, no Meshy task), so it falls back to one big orange clay sphere. It is its card's spare, named by no want, so nothing in play needs it to look like a bowl.
- **`BP_Prop`:** a new `Model` static mesh component; `SetProp(Name)` sets `PropName`, looks the name up in `props.json`, loads the mesh by its path (a soft reference, loaded when `ResetStage` dresses the prop at Scene Prep), sets scale, yaw, height and grip, and hides T19's shape parts. A name that `props.json` doesn't know still shows T19's parts, as today.
- **`BP_StageDirector`:** a new `SetCard(Names)` stores the card's props; `ResetStage` dresses the actors with `SetProp` in order and sends every prop to the table, held or not.
- **`L_Stage`:** the eight T19 props are deleted, and four new `BP_Prop` actors are spawned on the table top (re-placed, because template edits don't reach placed actors: T17).
- **`BP_Show`** (the PC's chain): three short additions inside `StagePrep`, which already finds the card in play: read the card's `props`, write them into the state's `set.props` (`SetObj`), and call `SetCard` before `ResetStage`. Kept separate in part 4.
- **`scenes.json`:** `set.props` and its readme sentences go. **`check_prompts.py`:** the shared-props argument goes, a check fails if `set.props` comes back, and a new `props.json` check.
- **`Config/DefaultGame.ini`** (outside T45's Touches): two `DirectoriesToAlwaysCook` lines, or a packaged build has no prop models (Decision 1).

## Decisions made for my person

My person asked prep sessions to take the task's default or my recommendation on calls that are theirs, and list them here. The T45 session should show this list to my person when it closes the task.

1. **Cook the prop folder.** `DefaultGame.ini` cooks only `L_Stage` "and what it references". A mesh named only by a string in `props.json` is referenced by nothing, so a packaged build would leave every prop model out, and `SetProp` would load nothing. Add `+DirectoriesToAlwaysCook=(Path="/Game/NHOS/Stage/Props")` (T47 adds `Headpieces`). This adds `Config/DefaultGame.ini` to T45's commit, outside its Touches; name it in the commit message. The other way, a hard reference (a map variable of meshes on `BP_Prop`), would load all 27 meshes with the level and defeat the soft reference the task asks for.
2. **A size for each prop**, as T43's findings asked (every prop was 30 cm long, so the ring was as big as the bowling ball). The sizes are in `make_props.py`'s `SIZE_CM`: rings, pills and the pocket watch 12 to 14 cm, the glow-stick sword 70, the staff 90, the rug 80, the rest 26 to 45. Scale = size ÷ the model's longest side in the manifest. Change a size by eye in the check, re-run the script, and copy the file again.
3. **The bowl of oranges' fallback is a 30 cm sphere in `MI_PropOrange`** (T19's orange prop material), not T19's shape parts, which hold no bowl. Making its model would spend Meshy credits (its picked image exists: `Docs/PropArt/bowl_of_oranges/`), so it is left for my person to ask for.
4. **Every prop is held in a hand** (`wear: hand`). None of the 28 is worn: the old paper crown (head) and cape (back) are gone. `wear` stays in the file, so a later prop can be worn.
5. **A prop rests upright, as Meshy made it, facing the house** (Model yaw 90, actor rotation 0). It lands that way on the floor too (`RestRot` zero, `RestZ` 0, because the Model's own height already puts its bottom on the actor's origin). The glowing staff stands 90 cm tall on the table; if it hides the robot behind it, lay it down (a `pitch` field and a rotation in `SetProp`) or shorten it.
6. **Held props go back to the table at Scene Prep, at once.** Today `ResetStage` sends only loose props home, and a held one goes back when its robot reaches home. With a new card, a held prop would turn into the next card's prop in a robot's hand on the walk home. `ResetStage` now calls `GoTable` on every prop.
7. **`SetCard` is a new function, and `ResetStage` keeps its signature.** A new input on `ResetStage` would leave a stale call node in `BP_Show` (T18's finding), and `BP_Show` belongs to the PC's chain.
8. **New check lines:** `NHOS: STAGE props <a>, <b>, <c>, <d>` (from `StagePrep`), `NHOS: ACT reset props=<a>, <b>, <c>, <d>` (it replaces `NHOS: ACT reset`, which no checker reads; grep before you change it), and `NHOS: ACT prop <name> mesh missing <path>` when a mesh fails to load.

## 0. Before you start

1. **The cards haven't moved since T44.** Rebuild the draft from the real file and compare:
   ```bash
   python Docs/tasks/T45-build/make_props.py Content/NHOS/Data/scenes.json /tmp/props.json
   diff Docs/tasks/T45-build/props.json /tmp/props.json
   ```
   No diff means the props didn't move. If a later change renamed a prop (T44's sheet allowed "ransom bag" → "mystery bag"; T44 kept "ransom bag"), the script stops on an `assert` that names it: add the new name to `SIZE_CM`, map it to its manifest id in the script, and run it again. The output of the run on the real file is the file you copy.
2. **The graph sources still match** what this sheet starts from: `git log --oneline -3 -- Graphs/BP_Prop Graphs/BP_StageDirector` shows nothing newer than `c2e1c81` (T19) for these files, and `git log --oneline -3 -- Graphs/BP_Show/StagePrep.txt` shows what changed since `407a9e6` (part 4).
3. **Who else calls these.** In the editor, `find_nodes` with title `SetProp` and `ResetStage` in every Blueprint (`BP_Prop`, `BP_StageDirector`, `BP_Show`, `BP_Robot`). Today: `SetProp` in `BP_Prop`'s BeginPlay and its construction script (no source file); `ResetStage` in `BP_Show.StagePrep` only. Neither signature changes, so nothing goes stale.
4. **Locks:** `BP_Prop.uasset`, `BP_StageDirector.uasset`, `L_Stage.umap` and `BP_Show.uasset` (part 4) with `git lfs lock`. `BP_Show` is the PC's chain: take it only when the PC's chain has released it, and pull first.

## 1. `Content/NHOS/Data/props.json` (step 1)

Copy [T45-build/props.json](T45-build/props.json) (or the rebuild from part 0) to `Content/NHOS/Data/props.json`. Its shape:

```json
"props": {
  "tin-can robot": { "card": "space_plans", "mesh": "/Game/NHOS/Stage/Props/space_plans/SM_TinCanRobot.SM_TinCanRobot",
                     "scale": 0.2368, "yaw": 90, "z": 22.5, "grip_z": -22.5, "wear": "hand", "size_cm": 45 },
  "bowl of oranges": { "card": "favor_father", "mesh": "/Engine/BasicShapes/Sphere.Sphere",
                       "material": "/Game/NHOS/Stage/Materials/MI_PropOrange.MI_PropOrange",
                       "scale": 0.3, "yaw": 0, "z": 15.0, "grip_z": -15.0, "wear": "hand", "size_cm": 30 }
},
"missing_models": [ { "name": "bowl of oranges", "card": "favor_father", "manifest_id": "bowl_of_oranges", "why": "..." } ]
```

- `z` = −`min_z` × scale: the model's bottom sits on the actor's origin (T43: "An actor sits on a floor at `Z0` at `z = Z0 - min_z * scale`"). Every Meshy model has its pivot at its center, so `z` is half its height.
- `grip_z` = −half the height: the hand (`Receive`'s slot, 44 cm under the arm pivot) holds the prop's middle.
- Every mesh path is an object path (`.../SM_X.SM_X`), the form `Make Soft Object Path` wants. The script checks that each `/Game/` mesh's `.uasset` is on disk.

**All 28 props, by card** (as T44 left `scenes.json`; the spare, named by no want, in italics):

| Card | Props (size in cm) |
|---|---|
| `space_plans` | tin-can robot 45, glow-stick sword 70, toy blaster 32, *piggy bank 32* |
| `mine_bridge` | cursed ring 12, glowing staff 90, water bucket 35, *frying pan 42* |
| `dino_island` | dino egg 32, meaty drumstick 32, safety waiver 30, *dino plush 36* |
| `favor_father` | plush horse head 40, cannoli tray 42, wedding envelope 26, *bowl of oranges 30 (no model: orange sphere)* |
| `glowing_briefcase` | glowing briefcase 45, gold pocket watch 14, giant milkshake 45, *giant cheeseburger 40* |
| `league_night` | rolled-up rug 80, bowling ball 26, ransom bag 36, *milk carton 26* |
| `pick_a_pill` | red pill 12, blue pill 12, ringing phone 26, *bent spoon 20* |

**Missing a model:** the bowl of oranges only. Every other prop's mesh is in `Content/NHOS/Stage/Props/<card id>/`.

## 2. `BP_Prop` (step 2)

### 2a. The component and the variables

Add with editor Python (T46's findings: `SubobjectDataSubsystem.add_new_subobject`, `rename_subobject`, then `compile_blueprint` and `save_asset`):

- **`Model`**, a `StaticMeshComponent` under the root. No mesh, scale 1, location 0. Collision preset `NoCollision` (the T19 parts don't block robots either; check one part's preset and copy it). **No component tag:** `SetProp` hides every component tagged `prop`, and `Model` must not be one of them.

New variables (T01: a literal can't go into a wildcard pin, so every JSON value lands in a typed variable first):

| Variable | Type | Default |
|---|---|---|
| `PropsObj`, `PEntry` | `JsonObjectWrapper` | empty |
| `PropsLoaded` | Boolean | false |
| `PMesh`, `PMat`, `PWear` | String | "" |
| `PScale`, `PYaw`, `PZ`, `PGrip` | Float | 1, 0, 0, 0 |
| `NullMat` | `MaterialInterface` object reference | none (left empty, like `BP_Robot`'s `NullProp`) |

Kept as they are: `PropName`, `Wear`, `GripLoc`, `GripRot`, `RestRot`, `RestZ`, `HomeLoc`, `HomeRot`, the fly variables, and every function but `SetProp`.

### 2b. The node names to look up first

These nodes appear in no graph source yet. Look each up with `find_node_types` (with `context_pins: []`), then `get_node_type_pins`, and spell the DSL from what they return (T11: a lookup of an id that `find_node_types` didn't return ends the whole script).

| In the DSL below | The Blueprint node | C++ |
|---|---|---|
| `Utilities|MakeSoftObjectPath` | Make Soft Object Path | `UKismetSystemLibrary::MakeSoftObjectPath(PathString)` |
| `Utilities|ToSoftObjectReference` | To Soft Object Reference (from a soft object path) | `UKismetSystemLibrary::Conv_SoftObjPathToSoftObjRef` |
| `Utilities|LoadAssetBlocking` | Load Asset Blocking | `UKismetSystemLibrary::LoadAsset_Blocking` |
| `(cast StaticMesh …)` | Cast To StaticMesh (pure cast) | — |
| `Components|StaticMesh|SetStaticMesh` | Set Static Mesh | `UStaticMeshComponent::SetStaticMesh` |
| `Rendering|Material|SetMaterial` | Set Material | `UPrimitiveComponent::SetMaterial(ElementIndex, Material)` |

No graph here has a cast yet. If the DSL can't write one, write `SetProp` without the two mesh lines, add a pure **Cast To StaticMesh** node by hand (`add_node` with the type id from `find_node_types`), wire it between Load Asset Blocking and Set Static Mesh, and note in the task's findings that the source file has a hand-wired node (as T18 did for `DrawCast`). Then the file says so in a comment, so the next writer re-adds it.

### 2c. `LoadProps` (new)

```lisp
(fn LoadProps ()
  ; T45: props.json, read once per actor. A missing or broken file leaves PropsObj empty,
  ; so every name falls back to T19's shape parts.
  (if (V PropsLoaded)
    (return))
  (set PropsLoaded true)
  (bind (_o _ok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat (Utilities|Paths|GetProjectContentDirectory) "NHOS/Data/props.json"))))
  (if (not _ok)
    (print "NHOS: ACT prop props.json missing or not valid JSON")
    (return))
  (bind _p (Json|GetField _o "props"))
  (set PropsObj _p))
```

### 2d. `SetProp` (rewrite, from `Graphs/BP_Prop/SetProp.txt`)

The old body stays as the branch for a name that `props.json` doesn't know, so the T19 props still work wherever they are named.

```lisp
(fn SetProp (Name)
  ; T45: a card prop gets its model from props.json; any other name shows T19's shape parts.
  ; An empty name hides everything (ResetStage uses it for an actor the card has no prop for).
  (set PropName Name)
  (bind _tag (Utilities|String|StringToName Name))
  (CallFunction|LoadProps)
  (bind _has (and (not (Utilities|String|IsEmpty Name)) (Json|HasField (V PropsObj) _tag)))
  (for _c (Actor|GetComponentsByClass :ComponentClass "/Script/Engine.StaticMeshComponent")
    (if (Components|ComponentHasTag :self _c :Tag "prop")
      (Rendering|SetVisibility :self _c :bNewVisibility (and (not _has) (Components|ComponentHasTag :self _c :Tag _tag)) :bPropagateToChildren false)))
  (Rendering|SetVisibility :self (V Model) :bNewVisibility _has :bPropagateToChildren false)
  (if (not _has)
    (bind _sw (streq Name "cardboard sword"))
    (bind _cr (streq Name "paper crown"))
    (bind _ro (streq Name "plastic rose"))
    (bind _rg (streq Name "toy ray gun"))
    (bind _tc (streq Name "teacup"))
    (bind _cp (streq Name "cape"))
    (bind _ck (streq Name "rubber chicken"))
    (bind _sc (streq Name "scroll"))
    (set Wear (select _cr "head" (select _cp "back" "hand")))
    (set GripRot (select _sw (Math|Rotator|MakeRotator :Roll 0.0 :Pitch -55.0 :Yaw 0.0) (select _ro (Math|Rotator|MakeRotator :Roll 0.0 :Pitch -40.0 :Yaw 0.0) (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw 0.0))))
    (set GripLoc (select _tc (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 9.0) (select _ck (Math|Vector|MakeVector :X 6.0 :Y 0.0 :Z 18.0) (select _sc (Math|Vector|MakeVector :X 6.0 :Y 0.0 :Z 0.0) (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 0.0)))))
    (set RestRot (select _sw (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 90.0 :Yaw 25.0) (select _ro (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 90.0 :Yaw 40.0) (select _cp (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 90.0 :Yaw 0.0) (select _rg (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw 30.0) (select _ck (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw 40.0) (select _sc (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw 20.0) (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw 0.0))))))))
    (set RestZ (select _sw 4.0 (select _ro 7.0 (select _rg 8.0 (select _cp 2.0 (select _ck 21.0 (select _sc 9.0 0.0)))))))
    (return))
  (bind _e (Json|GetField (V PropsObj) _tag))
  (set PEntry _e)
  (bind _m (Json|GetField (V PEntry) "mesh"))
  (set PMesh _m)
  (bind _s (Json|GetField (V PEntry) "scale"))
  (set PScale _s)
  (bind _y (Json|GetField (V PEntry) "yaw"))
  (set PYaw _y)
  (bind _z (Json|GetField (V PEntry) "z"))
  (set PZ _z)
  (bind _g (Json|GetField (V PEntry) "grip_z"))
  (set PGrip _g)
  (bind _w (Json|GetField (V PEntry) "wear"))
  (set PWear _w)
  (set PMat "")
  (bind _hm (Json|HasField (V PEntry) "material"))
  (if _hm
    (bind _mt (Json|GetField (V PEntry) "material"))
    (set PMat _mt))
  ; the soft reference: path -> soft object reference -> load -> StaticMesh
  (bind _obj (Utilities|LoadAssetBlocking :Asset (Utilities|ToSoftObjectReference (Utilities|MakeSoftObjectPath :PathString (V PMesh)))))
  (bind _mesh (cast StaticMesh _obj))
  (if (not (Utilities|IsValidObject _mesh))
    (print (cat "NHOS: ACT prop " Name " mesh missing " (V PMesh)))
    (Rendering|SetVisibility :self (V Model) :bNewVisibility false :bPropagateToChildren false))
  (Components|StaticMesh|SetStaticMesh :self (V Model) :NewMesh _mesh)
  ; slot 0: the fallback's material, or none (the mesh's own M_<Name>)
  (if (Utilities|String|IsEmpty (V PMat))
    (Rendering|Material|SetMaterial :self (V Model) :ElementIndex 0 :Material (V NullMat))
    (else
      (bind _mo (Utilities|LoadAssetBlocking :Asset (Utilities|ToSoftObjectReference (Utilities|MakeSoftObjectPath :PathString (V PMat)))))
      (Rendering|Material|SetMaterial :self (V Model) :ElementIndex 0 :Material (cast MaterialInterface _mo))))
  (Transformation|SetRelativeScale3D :self (V Model) :NewScale3D (Math|Vector|MakeVector :X (V PScale) :Y (V PScale) :Z (V PScale)))
  (Transformation|SetRelativeLocation :self (V Model) :NewLocation (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z (V PZ)))
  (Transformation|SetRelativeRotation :self (V Model) :NewRotation (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw (V PYaw)))
  (set Wear (V PWear))
  (set GripLoc (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z (V PGrip)))
  (set GripRot (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw 0.0))
  (set RestRot (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw 0.0))
  (set RestZ 0.0))
```

Notes:
- `Utilities|IsValidObject` stands for the pure **Is Valid** (object) node; the graphs use only the macro form, `(Utilities|IsValid x (:"Is Valid" …) (:"Is Not Valid" …))`, which also works here. Look it up with the others.
- The `if (not (… IsValid))` branch has no `return` (T01: so the code after it joins), and Set Static Mesh with a null mesh just clears it, which is what a missing mesh should do.
- `SetMaterial` with `NullMat` (none) clears slot 0's override, so a prop that was the orange sphere and becomes a model shows the model's own material.
- **BeginPlay and the construction script call `SetProp(PropName)` as today.** The construction script now also loads `props.json` and the mesh in the editor, so the four actors show their preview prop in the viewport. That is fine; if it stalls the editor, have the construction script skip the load (it has no source file: read it before you touch it).
- `EventGraph`, `NameIs`, `GoTable`, `ThrowTo`, `TickFly`, `FlyToComp`, `SlotFor`, `IsHeld`, `GetWear` don't change. `NameIs` matches the whole name or its last word ("robot" finds "tin-can robot", "pill" finds the first pill actor), which is how `FindProp` keeps working by name.

Save `Graphs/BP_Prop/SetProp.txt` and the new `Graphs/BP_Prop/LoadProps.txt` as written (shorthand).

## 3. `BP_StageDirector` and `L_Stage` (steps 3 and 4)

### 3a. `SetCard` (new) and `ResetStage` (from `Graphs/BP_StageDirector/ResetStage.txt`)

New variable: `CardProps`, String array, empty.

```lisp
(fn SetCard (Names)
  ; T45: the card in play's props, from BP_Show.StagePrep, just before ResetStage.
  (set CardProps Names))
```

```lisp
(fn ResetStage ()
  (if (not (V Ready))
    (CallFunction|Init))
  (for _b (V AllBots)
    (Class|BPRobot|GoHome :self _b))
  ; T45: dress the table with the card's props, in order; an actor past the card's list goes empty.
  ; Every prop goes home now, held or not, so no robot carries the old card's prop as a new one.
  (bind _n (len (V CardProps)))
  (for _i (range (len (V Props)))
    (bind _p (get (V Props) _i))
    (if (> _n 0)
      (if (< _i _n)
        (Class|BPProp|SetProp :self _p :Name (get (V CardProps) _i))
        (else
          (Class|BPProp|SetProp :self _p :Name ""))))
    (Class|BPProp|GoTable :self _p :Dur 0.9))
  (print (cat "NHOS: ACT reset props=" (Utilities|String|JoinStringArray :SourceArray (V CardProps) :Separator ", "))))
```

- With `CardProps` empty (before `BP_Show` calls `SetCard`, or if part 4 isn't in yet) the props keep their names, and the show plays on with whatever the actors were placed as. So parts 2 and 3 can land and be tested before part 4.
- `get` sits inside the `if (< _i _n)` branch, not in a `select`, because a pure Select evaluates both inputs and an out-of-range Get prints a `LogScript` warning.
- `GoTable` returns early for a prop already home, and it detaches a held prop and clears its `Slot`, so the robot's later `ToTable` finds nothing to send.
- Look up `JoinStringArray` too (part 2b's way).
- `Init`, `FindProp`, `PlayPart` and the rest don't change. `Init` still finds the props with `GetAllActorsOfClass`, so four actors in the level means four in `Props`.

Save `Graphs/BP_StageDirector/ResetStage.txt` and the new `SetCard.txt`.

### 3b. Four props on the table (`L_Stage`)

Template edits don't reach placed actors (T17, and T46 again), and the old eight carry actor scales of 1.0 to 1.6 that would scale the new models too. So delete all eight and spawn four. In editor Python, after `BP_Prop` is compiled and saved:

1. Find the table: the static mesh actor of the cloth-covered prop table at about (300, 300) (T17), in the outliner under `Stage/`. Print its label and `get_actor_bounds(False)`: the top is `origin.z + extent.z`.
2. Note the eight `BP_Prop` actors' labels and folder (`Stage/Props`), then `EditorActorSubsystem.destroy_actor` each.
3. Spawn four `BP_Prop` with `spawn_actor_from_class` at `x` = the table's center x, `z` = the table top, rotation 0, scale 1, and `y` spread across the table's width at the centers of four equal slots (for a table of width `W` centered at `y0`: `y0 − 3W/8`, `y0 − W/8`, `y0 + W/8`, `y0 + 3W/8`). Labels `Prop1` to `Prop4`, folder `Stage/Props`, and `PropName` set to the four props of the first card (`tin-can robot`, `glow-stick sword`, `toy blaster`, `piggy bank`), only so the editor shows something.
4. Save `L_Stage`, then `git status` and lock what changed (it isn't World Partition, so it is the one `.umap`).

The widest card on the table is `league_night` (rug 80 cm across, bag 36, ball 26, carton 26). If the slots are narrower than 80 cm, the rug overlaps its neighbor: check it in the screenshots and lower its `SIZE_CM` if it does.

The Prop Table place's spots (`BP_PlaceMark`) stand in front of and beside the table, so they don't move.

## 4. `BP_Show` at Scene Prep (step 4) — the PC's chain

**Re-check against the `Graphs/BP_Show/` sources of that day.** This is written against `Graphs/BP_Show/StagePrep.txt` at `407a9e6`. T52, T54, T55, T57 and T58 run on the PC first and may change `StagePrep` or `LoadData`. Before you write, read the current `StagePrep.txt` and check:

- `StagePrep` still loops `CardArr` and matches `CardId` (the backdrop lookup), and still calls `ResetStage` on the director after it. If so, the three additions below go in exactly where marked.
- `SetObj` is still the `{name, places, props}` object from `LoadData` that every actor state copies as `set` (T06). Check with `find_nodes` for `GetSetObj` in `BP_Show`, and read only the graphs that use it (likely `ActorState`, no source file). If a graph builds `set` some other way, write the card's props there instead.
- **The input LLM's `props`** (prompts.json: "The input LLM gets actor, phase, places [names], props, ..."): find where its state gets `props` (`find_nodes` for `GetField` near `props`, or the input ask's graph). If it reads `SetObj`'s `props`, it follows with no change; if it reads a list from `LoadData`, point it at `CardProps`.
- **The prep card's set text** (`SetLine`, built in `LoadData`): if it lists the props, rebuild it at the same place in `StagePrep` from `CardProps`. Look at a Scene Prep screenshot first: if the card shows no props line, skip this.

New variable on `BP_Show`: `CardProps`, String array.

The three additions to `StagePrep` (marked `; T45`; everything else is the file as it was):

```lisp
(fn StagePrep ()
  (for _s (range (Variables|Default|GetSeatCount))
    (bind _col (CallFunction|PersonaColor :Id (Utilities|Array|Get(acopy) (Variables|Default|GetSeatId) _s)))
    (Utilities|Array|SetArrayElem (Variables|Default|GetSeatColors) _s _col))
  (Variables|Default|SetBdId "")
  (clear (Variables|Default|GetCardProps))                                     ; T45
  (for _c (Variables|Default|GetCardArr)
    (bind _cid (Json|GetField _c "id"))
    (Variables|Default|SetBdStr _cid)
    (if (Utilities|String|EqualExactly(String) (Variables|Default|GetBdStr) (Variables|Default|GetCardId))
      (bind _bd (Json|GetField _c "backdrop"))
      (Variables|Default|SetBdObj _bd)
      (bind _bid (Json|GetField (Variables|Default|GetBdObj) "id"))
      (Variables|Default|SetBdId _bid)
      (bind _pr (Json|GetField _c "props"))                                    ; T45
      (Variables|Default|SetCardProps _pr)))                                   ; T45
  (Json|SetField (Variables|Default|GetSetObj) "props" (Variables|Default|GetCardProps))   ; T45: the state's set.props
  (Development|PrintString (Utilities|String|Append "NHOS: STAGE props " (Utilities|String|JoinStringArray :SourceArray (Variables|Default|GetCardProps) :Separator ", ")) false)   ; T45
  (Development|PrintString (Utilities|String|Append "NHOS: STAGE backdrop " (Variables|Default|GetBdId)) false)
  (bind _dir (Actor|GetActorOfClass :ActorClass "/Game/NHOS/Stage/BP_StageDirector.BP_StageDirector_C"))
  (if (!= _dir (Variables|Default|GetNullDir))
    (Class|BPStageDirector|SetCard :self _dir :Names (Variables|Default|GetCardProps))   ; T45
    (Class|BPStageDirector|ResetStage :self _dir))
  (bind _bp (Actor|GetActorOfClass :ActorClass "/Game/NHOS/Stage/BP_Backdrop.BP_Backdrop_C"))
  (Utilities|IsValid _bp (:"Is Valid" (Class|BPBackdrop|ShowBackdrop :self _bp :Id (Variables|Default|GetBdId))) (:"Is Not Valid")))
```

- `Set Field` on the `SetObj` copy changes the shared object: a `JsonObjectWrapper` holds a pointer to its object, the way `BPC_LLMClient.Ask` fills `_env`. The check proves it: free mode picks its grabs from the state's `set.props` (`FreeReply` reads `set.props` into `FProps`), so `NHOS: ACT … grab - <card prop>` lines can only come from the new list.
- If writing the whole graph is too risky on the day, the same change is two node groups put in by hand: the `GetField props` → `SetCardProps` pair inside the card match, and the `SetField` + `SetCard` pair before `ResetStage`. Then update `StagePrep.txt` to match.
- Save `Graphs/BP_Show/StagePrep.txt`. Don't touch any other `BP_Show` graph unless the checks above send you there.

## 5. `scenes.json` and `Tools/check_prompts.py` (end of step 4)

### 5a. `scenes.json`

After the check passes (so the game no longer reads it), from T44's version of the file:

- Delete `set.props` (the eight shared props).
- In `_readme`'s `set` line, delete the sentence `'props' is the shared list the game still sends as the state's set.props until T45 puts each card's own props on the Prop Table; T45 removes it.`
- In `_readme`'s `cards` line, change `(and, from T45, the card's props as set.props)` to `and the card's props as set.props`.

Both sentences are in `scenes.json` as quoted at `6c702b3`; if they moved, find them by `set.props`.

### 5b. `check_prompts.py`

Against the checker as T44 left it (line numbers at `6c702b3`):

1. **`set.props` is gone.** In `check_files` (line 634), change `errors.extend(card_prop_problems(cards, s.get("props", [])))` to:
   ```python
   if "props" in s:
       errors.append("scenes.json: set.props is gone since T45; the state's set.props is each card's own props")
   errors.extend(card_prop_problems(cards))
   ```
   `card_prop_problems(cards, shared=())` (line 489) keeps its default. In its docstring, drop "or from the shared set.props".
2. **The new `props.json` check**, a function next to `card_prop_problems`, called from `check_files` with `props = load_json("props.json", errors) or {}`:
   ```python
   def props_file_problems(cards, pdata) -> list[str]:
       """props.json (T45): every card prop has a look on the Prop Table, and every look is on a card.
       A model's mesh must be on disk; a prop with no model must be listed in missing_models."""
       out, looks = [], pdata.get("props", {})
       missing = {m.get("name") for m in pdata.get("missing_models", [])}
       on_cards = {p: c.get("id") for c in cards for p in c.get("props", [])}
       for name, cid in on_cards.items():
           e = looks.get(name)
           if not isinstance(e, dict):
               out.append(f"props.json: no entry for {cid}'s prop {name!r}")
               continue
           mesh = e.get("mesh", "")
           if not re.fullmatch(r"/(Game|Engine)/[\w/]+\.\w+", mesh):
               out.append(f"props.json: {name!r} needs a mesh object path (/Game/.../SM_X.SM_X)")
           elif mesh.startswith("/Game/") and not (ROOT / "Content" / (mesh[6:].rsplit(".", 1)[0] + ".uasset")).exists():
               out.append(f"props.json: {name!r}'s mesh {mesh} is not in Content/")
           if mesh.startswith("/Engine/") and name not in missing:
               out.append(f"props.json: {name!r} uses an engine shape, so list it in missing_models")
           if not all(isinstance(e.get(k), (int, float)) for k in ("scale", "yaw", "z", "grip_z")) or not e.get("scale", 0) > 0:
               out.append(f"props.json: {name!r} needs a scale above 0 and numbers for yaw, z and grip_z")
           if e.get("wear") not in ("hand", "head", "back"):
               out.append(f"props.json: {name!r}'s wear must be hand, head or back")
           if e.get("card") != cid:
               out.append(f"props.json: {name!r} says card {e.get('card')!r}, but it is on {cid}")
       for name in set(looks) - set(on_cards):
           out.append(f"props.json: {name!r} is on no card")
       return out
   ```
   `ROOT` and `re` are already in the checker (`DATA = ROOT / "Content" / ...`).
3. **The docstring:** add a line under T44's "Props (T44)" paragraph (line 44), whose last sentence already says "as the game does from T45": "`props.json` (T45) gives each card prop its model on the Prop Table; the checker matches it to the cards and finds each mesh on disk."
4. `prewritten_problems` needs no change: it walks every `props` list in `scenes.json`, which are now the cards' only.
5. Run `python Tools/check_prompts.py --offline` (it must pass), then break one thing by hand (rename a prop in a copy of `props.json`) to see the new error, and put it back.

## 6. The check (step 5)

### 6a. Free autoplay shows in a game window (the saved assets)

`Local/switches.json`: `"autoplay": true`, `"mode": "free"`, `"spare_human": true`, `"fast_lines": true`, `"force_tie": false`, `"ai_seats": 0` (plus whatever switches the tasks before T45 added; see `Docs/switches.example.json`). `spare_human` keeps the human on stage, so a show plays every scene and the table changes three or four times.

Run it twice, with the editor's assets saved (T27's Mac command):

```bash
"/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor" "<PROJECT>" -game -windowed -ResX=1600 -ResY=900 -log=T45a.log
```

The log is `~/Library/Logs/AIMegaJam2026/T45a.log` on a Mac (`Saved/Logs/T45a.log` on Windows). Then:

```bash
grep -E "NHOS: (SETUP|STAGE props|ACT reset|ACT ready|ACT prop|ACT \S+ (grab|throw|give)|SHOW END)" ~/Library/Logs/AIMegaJam2026/T45a.log
grep -c "LogScript" ~/Library/Logs/AIMegaJam2026/T45a.log
```

Expected, for each scene (`<…>` varies):

```
NHOS: ACT ready marks=7 props=4 robots=5
NHOS: SETUP human=human scene=<card id> ...
NHOS: STAGE props <the card's four props, in scenes.json order>
NHOS: ACT reset props=<the same four>
NHOS: ACT <persona> grab - <one of those four>          (free mode grabs from set.props)
NHOS: ACT <persona> throw <target> <one of those four>
...
NHOS: SHOW END result=<win|lose> scenes=<n>
```

It passes when: both shows reach `SHOW END`; `ACT ready` says `props=4`; each scene's `STAGE props` and `ACT reset props` name the card in its `SETUP` line; at least one `grab` and one `throw` per show name a card prop; no `ACT` line names an old prop (`grep -E "cardboard sword|paper crown|plastic rose|toy ray gun|teacup|cape|rubber chicken|scroll"` finds nothing after `SETUP`); no `ACT prop … mesh missing`; and no `LogScript` line. A grab of a name that isn't on the table prints the director's "look around" reason; one or two from the free mode's own guesses are fine, but not a pattern.

Two different cards in the two shows' scene 1 are likely but not certain (seven cards). If both shows draw the same cards, run a third.

### 6b. Screenshots

- **The prop table in each scene of one show**, from the house camera: four models on the table, each scene a different card's four. T27's findings have the Mac way to capture a game window (`screencapture -x -o -l<window id>`); T46 found that it gives a black image while the Mac's screen is locked, and then used PIE screenshots of the same saved assets (`SlateInspectorToolset.Screenshot`), which is fine here too.
- **A held prop:** a robot holding one of them (the hand at the prop's middle), and a thrown one lying on the floor upright, facing the house.
- **Judge, as a first-time player:** can each prop be told apart from the house (the ring and pills are the small ones: if they vanish, raise their `SIZE_CM`), does anything overlap on the table, does the staff hide a robot, and does the orange sphere read as fruit.

Save the shots to `Saved/T45/shots/` (not in git) and write what they showed under T45's "## Findings".

### 6c. A packaged build (if one is made)

Not checkable on the Mac (Mac packaging is untried). On the next Windows package, check that the props show: if the table is empty and the log has `mesh missing`, Decision 1's cook lines are missing.

## 7. What T45 commits

`Content/NHOS/Data/props.json`, `Content/NHOS/Data/scenes.json`, `Tools/check_prompts.py`, `Config/DefaultGame.ini` (Decision 1), `BP_Prop.uasset`, `BP_StageDirector.uasset`, `BP_Show.uasset`, `L_Stage.umap`, `Graphs/BP_Prop/{SetProp,LoadProps}.txt`, `Graphs/BP_StageDirector/{ResetStage,SetCard}.txt`, `Graphs/BP_Show/StagePrep.txt`, the plan, `T45.md` and `DevLog.md`, as "How to run a task" lists. `Docs/Assets.md` needs no line: every model is T43's and already listed.

## 8. For T47

T47 adds 13 headpieces to `props.json` or to a new `costumes.json`. Its build sheet ([T47-build.md](T47-build.md)) uses a separate `costumes.json`, so the `props.json` check above stays a props-only check. It reuses `LoadProps`' pattern and the node lookups in part 2b.
