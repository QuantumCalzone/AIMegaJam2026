# T109 build sheet: the arms re-fit, measured from the meshes

Back to [T109](T109.md). Written by a T109 prep session on 2026-11-19 (UTC), without the editor and with no paid call. It did T109's step 1 from the files, measured everything that step 3 needs from the GLBs, worked out a re-fit for all five robots, and rendered it offline. T109's own session still does steps 2 to 6 in the editor: it sees the robots, applies the re-fit, checks the gestures and props, gets my person's OK on a sheet from the editor, and plays a show.

Step 3's measuring is done here, offline. T109 still checks the numbers against the editor. The questions only the editor or T104 can answer are listed under "Open questions".

## What is where

- **The preview sheets** (SceneKit renders of the GLBs with their diffuse textures, not the game's lighting or camera):
  - [`Docs/Art/Cast/arms_refit_sheet.png`](../Art/Cast/arms_refit_sheet.png): one row per robot. It shows today's fit from the front, the side (the robot's right) and three-quarter, then the re-fit in the same three views, then the re-fit while talking (arms rolled 52° out) and cheering (150°). The last row is OpenAI's fold, before and after, with today's talk and cheer. The red dot is `HandSocket`. OpenAI's rows above the last one show its arms unfolded (idle roll 6°, fold 0), because the fold hides the shoulder.
  - [`Docs/Art/Cast/arms_refit_shoulders.png`](../Art/Cast/arms_refit_shoulders.png): close-ups of each robot's shoulders, before and after, from the front and three-quarter.
- **The tools** are in the shared notes folder of the dispatcher's session group, under `T109-prep-tools/` (its `README.md` says how to run them). They are not in git:
  - `lib.py` reads the GLBs and places the parts in the Rig.
  - `measure.py`, `side.py` and `armcol.py` measure.
  - `refit.py` and `try.py` compute a fit and its metrics.
  - `final.py` holds the picked re-fits and makes the renders. `fold.py` finds where OpenAI's folded hand lands.
  - `shot.swift` renders, and `sheet.swift` and `row.swift` tile the renders.
  - `final.json` holds every number in this file.
- **Frames.** A GLB (metres, Y up, facing +Z) becomes the UE mesh as Interchange imports it: X = 100·gx, Y = 100·gz, Z = 100·gy. That is ×100, Z up, facing mesh +Y, with mesh +X as the model's left. This matched T103's vertex dumps from the editor (`Saved/T103/out/v_*.json`) to 0.1 cm on every part. Each part's Rig transform is UE's: scale, then `FRotator` (Roll, Pitch, Yaw), then location. Bodies and heads use T103's placements (`Saved/T103/out/fits.json`, yaw −90). Meta's head is 7 cm lower (T103's decision 6).
- **Today's arm transforms** are taken from T103's `Saved/T103/out/armfit.json` (on the Mac, not in git, and copied to the tools folder). Its hand points equal the `HandSocket` vectors in `SetPersona` to 0.1 cm, so T103 almost certainly applied it. **Read the ten arm components in the editor before changing them**, and see "Open questions".

## Step 1: what the files say

- **T103's decision 7.** Each pivot sits 4 cm under its arm's top, and each top sits where the turnaround has it: OpenAI ±30 at z 72.8, Anthropic ±34 at z 74 (arm pitched ±20° outward), SpaceXAI ±39 at z 81 (arm 1.3× across), Meta ±30 at z 66, and me ±33 at z 94. Meta's and my arm models are the robot's left arm. The right arm of every robot is the left one mirrored, with negative X scale. `HandSocket` on `ArmPivotR` is at OpenAI (0.1, 1.6, −36.3), Anthropic (0.6, 15.7, −42.4), SpaceXAI (−0.3, 0.7, −37.2), Meta (10.7, −1.5, −29.5) and me (9.0, 5.7, −59.9).
- **`SetPersona`** places only the pivots (`_sy` and `_sz`, through two `SetRelativeLocation` nodes on `ArmPivotL`/`ArmPivotR`) and `HandSocket`. It does not set the arm meshes. They are per-robot components under the pivots: `OArmXL`/`OArmXR`, `AArmXL`/`AArmXR`, `SArmXL`/`SArmXR`, `MArmXL`/`MArmXR` and `YArmXL`/`YArmXR`. T82 and T83 named them, and the comment in `SetPersona` names `AArmXL`/`AArmXR`. Their transforms are component defaults in `BP_Robot`, which no graph sets. So each arm's offset, pitch and roll is a component edit, not a graph edit.
- **`EventGraph`'s tick** sets both pivots' rotation on every frame:
  - Right pivot: Roll = `FoldRoll·Fold − _arm`. Left pivot: Roll = `_arm − FoldRoll·Fold`. Both: Pitch = `FoldPitch·Fold`. A negative roll swings the right arm outward.
  - `_arm` is 6 ± 4 at idle, so **every robot's arms always roll 2° to 10° outward at rest.** It is 30 ± 22 while talking, and 150 for 2.8 s during a cheer.
  - The fold is OpenAI's alone (`FoldPitch` 70, `FoldRoll` 33). `Fold` eases to 1 at rest and to 0 while it talks or cheers.
  - A cut robot's pivots go to (0, 0, 0), so its arms hang at their component pose while the Rig falls.
  - The fits below are judged at the idle roll (2°, 6° and 10°), not with the pivot unrotated.
- **`Emote` and `GestTick`** never touch the pivots. `GestTick` writes only the Rig's offsets (`GX`, `GZ`, `GPitch`, `GRoll`, `GYaw`, `GScale`), and `emotes.json`'s gesture channels are only `z`, `roll` and `yaw`. A gesture moves the whole robot, arms and body together, so a re-fit can't open a gap in one. They need no change. Check them only because step 5 asks for it.
- **`Receive` holds the left hand at a fixed point:** its second `FlyToComp` (slot 1) puts a prop on `ArmPivotL` with `Off` (0, −5, −44) for every robot. Today that is already 8 to 15 cm off most left hands. After the re-fit it would be off by up to 23 cm, with SpaceXAI's left prop floating by its belly. It must move with the hands: see "`Receive`: the left hand" below.
- **`HandSocket`** is a Scene component on `ArmPivotR` (T79). Props fly to it in `Receive`, and grab, hold, throw and give use it.
- **Nothing outside `BP_Robot` names the pivots or `HandSocket`.** A search of `Graphs/` finds them only in `BP_Robot`'s `EventGraph`, `SetPersona` and `Receive`, and `BP_Prop` attaches to whatever component it is given.
- **T104** (running now) holds `BP_Robot`.
  - Its no-editor drafts (`Saved/T104/drafts/graphs/`) change `SetHeadpiece` and `DressFromShow`. Their `EventGraph` draft has the same arm lines as today.
  - Its costumes ride `HeadSocket`. None hangs from an arm or a shoulder in the drafts.
  - Its build sheet's open question 4 asks whether T75's arm gestures clip the cube hood's short cape, the dino hood's lower jaw or the beard.
  - Re-read all of this after T104's push.

## The measurements

All numbers are in cm in the Rig: X forward, Y the robot's right, Z up. They are measured on the right side, and the left side matches it within 0.5 cm.

### Each body's half-width at the shoulder (T82's decision 5)

The largest Y of the body's vertices in each 1.5 cm slice, over all X.

| Robot | Body top | Half-width by height | What is there |
|---|---|---|---|
| OpenAI | 79.9 | 24.4 from z 39 to 69, 22.6 at 71, 20.5 at 73, 18.9 at 75, 14.6 at 77 | The sweater's side, with its baked sleeve shapes, is a straight 24.4 up to z 69. Above that the shoulder slopes in to the gold collar (z 77 to 80). |
| Anthropic | 89.2 | 37.8 from z 49 to 69, 36.5 at 71, 34.5 at 73, 32.9 at 75, 30.2 at 77, 29.0 at 79, 26.8 at 81, 24.7 at 83, 21.0 at 85 | The egg, with a shallow hollow on each side where the arm hangs, and the tan collar disc on top. |
| SpaceXAI | 96.7 | 30.4 to 31.0 from z 55 to 67, **32.9 from z 68.5 to 85**, 29.8 at 85, 25.2 at 88, 18.2 at 89.5 | The lime ball. **A white socket disc on each side**, z 68.5 to 85 and X −10 to +4.4 (centre about X −3, z 77), stands 2 cm proud of the ball. A lime cap sits above it (z 85 to 88, Y 25 to 30). The spring neck is 10.8 half-wide. |
| Meta | 77.1 | Shirt and pants 20.5 to 22.3 from z 30 to 42; **a pale fin out to 25.6 from z 45 to 64** (X −9 to +5.5), with the shirt beside it at 21 to 24; the shirt's shoulder 24.3 to 24.5 at z 64.5 to 69, then 19.4 at 70.5 and 15.5 at 73.5 | There are no real sleeves. The black shirt's shoulder is the "sleeve" from the front. The pale fin is where the reference crop's arm hung (T103-build's "pale patch"). |
| Me | 104.8 | 26.7 to 27.1, flat, all the way up | The box's flat sides, X −28 to +23. |

### Each arm's top

| Robot | Length | The top | Width × depth below it |
|---|---|---|---|
| OpenAI | 49 | A **domed sleeve end**: 11 cm wide at its top slice, full width 4 cm down | 15 × 15 knit sleeve, ribbed cuff, mitten |
| Anthropic | 58 | A **ball shoulder**, 10 cm across (a separate piece, 0.2 cm from the first ring) | Ribbed rings 10 to 12 wide, open four-finger hand |
| SpaceXAI | 49 | A **steel spring**, 7 cm long and 6 cm wide | Lime upper arm 12 wide from 7.5 cm down, forearm, open hand |
| Meta | 40 | A **flat-topped stub**, 12 × 12 at the very top | Silver jointed arm. The elbow bends forward, and the hand is 11 cm ahead of the shoulder |
| Me | 75 | A **round sleeve end**: 2.5 cm wide at its crown, 9 at 4.5 down, 12 at 9 down | A striped sleeve that curves 6.5 cm outward over its upper 31 cm, a brown cuff at 40 down, a garden glove |

### The gap today

The front-view gap is the arm's inner edge minus the body's outer edge (each over all X) in the arm's top 12 cm, with the pivots at the idle roll (6°). A positive number is daylight between arm and body from the house camera.

| Robot | Largest gap at the shoulder | Where |
|---|---|---|
| OpenAI | **12.0** | The sleeve touches the sweater from z 49 to 70, but its top (z 71 to 79) stands 2 to 12 cm off the sloping shoulder. |
| Anthropic | 3.5 | Only the ball's top, at z 80, is clear of the egg's slope. The rest of the arm overlaps the egg's silhouette by 1 to 6 cm. |
| SpaceXAI | **8.3** | The arm hangs 0 to 9 cm off the ball. The spring top (z 80 to 87, Y 36 to 42) stands beside the spring neck, above the ball's shoulder. |
| Meta | **10.1** | The stub's top (z 68 to 72) stands 1 to 10 cm off the shirt's shoulder, and the pale fin shows between arm and shirt. |
| Me | 4.7 | The whole sleeve is 2 to 5 cm off the box's side. |

## The re-fit

**How every arm is fitted:**

- The pivot is the shoulder joint, on or inside the body's surface.
- Each arm has a joint point: the centre of its cross-section at a set depth below its top. That point sits on the pivot.
- The arm hangs tilted outward, by a pitch on its component in the mesh frame, which tilts it across after the yaw. Its top end then leans into the body, and the hand clears it.
- The joint point is where the arm enters the body. With the pivot there, nothing hidden swings out when the arm turns. That is why SpaceXAI's pivot is at the spring's inner end: with the pivot at its outer end, the cheer swung the spring out below the raised arm.
- Every right arm stays the left one mirrored (negative X scale), as today, including Meta's and mine.
- Pivot X stays 0. Meta's 3 cm back is in its arm's component location.

| Robot | Pivot (±Y, Z): today → new | Joint point | Tilt (hand outward) | Arm Z range | Largest gap after | `HandSocket` on `ArmPivotR`: today → new |
|---|---|---|---|---|---|---|
| OpenAI | (30, 72.8) → **(21, 69)** | 4 below the top | 14° | 26.9 to 74.3 | 2.5 (the dome's top 1.5 cm only), −2.4 to −9.6 below it | (0.1, 1.6, −36.3) → **(0.1, 11.1, −36.5)** |
| Anthropic | (34, 74) → **(31, 75.5)** | 5 (the ball's centre) | 20° (as today) | 26.5 to 80.5 | 0.9 (the ball's top), then −1.9 to −9 | (0.6, 15.7, −42.4) → **(0.7, 16.1, −42.9)** |
| SpaceXAI | (39, 81) → **(27.5, 80)** | 0.6 (the spring's inner end) | 32° | 39.3 to 82.3 | **−3.3** (none) | (−0.3, 0.7, −37.2) → **(−0.1, 23.2, −35.6)** |
| Meta | (30, 66) → **(22, 63)** | 4 | 12°, and 8° back | 27.1 to 68.4 | **−1.3** (none) | (10.7, −1.5, −29.5) → **(3.9, 5.4, −32.1)** |
| Me | (33, 94) → **(27, 98)** | 6 | **−6°** (hand inward, to straighten the curve along the box) | 28.9 to 104.0 | **−1.4** (none) | (9.0, 5.7, −59.9) → **(7.8, −0.7, −60.3)** |

**The arm components** (relative location, rotation as `FRotator` Roll/Pitch/Yaw, scale), under their pivots:

| Component | Location | Rotation | Scale | Today (location, rotation) |
|---|---|---|---|---|
| `OArmXL` | (−0.23, −6.09, −19.54) | Roll 0, Pitch 14, Yaw −90 | (0.258, 0.258, 0.258) | (−0.16, −0.84, −18.58), (0, 0, −90) |
| `OArmXR` | (−0.23, 6.09, −19.54) | Roll 0, Pitch −14, Yaw −90 | (−0.258, 0.258, 0.258) | (−0.16, 0.84, −18.58), (0, 0, −90) |
| `AArmXL` | (0.02, −8.84, −22.29) | Roll 0, Pitch 20, Yaw −90 | (0.305, 0.305, 0.305) | (−0.10, −8.82, −21.31), (0, 20, −90) |
| `AArmXR` | (0.02, 8.84, −22.29) | Roll 0, Pitch −20, Yaw −90 | (−0.305, 0.305, 0.305) | (−0.10, 8.82, −21.31), (0, −20, −90) |
| `SArmXL` | (−0.12, −13.52, −19.70) | Roll 0, Pitch 32, Yaw −90 | (0.3367, 0.3367, 0.259) | (−0.32, −0.85, −18.56), (0, 0, −90) |
| `SArmXR` | (−0.12, 13.52, −19.70) | Roll 0, Pitch −32, Yaw −90 | (−0.3367, 0.3367, 0.259) | (−0.32, 0.85, −18.56), (0, 0, −90) |
| `MArmXL` | (−0.25, −1.77, −16.57) | Roll 8, Pitch 12, Yaw −90 | (0.211, 0.211, 0.211) | (4.37, 1.81, −14.34), (0, 0, −90) |
| `MArmXR` | (−0.25, 1.77, −16.57) | Roll 8, Pitch −12, Yaw −90 | (−0.211, 0.211, 0.211) | (4.37, −1.81, −14.34), (0, 0, −90) |
| `YArmXL` | (4.55, −1.77, −31.95) | Roll 0, Pitch −6, Yaw −90 | (0.395, 0.395, 0.395) | (5.72, −5.26, −31.38), (0, 0, −90) |
| `YArmXR` | (4.55, 1.77, −31.95) | Roll 0, Pitch 6, Yaw −90 | (−0.395, 0.395, 0.395) | (5.72, 5.26, −31.38), (0, 0, −90) |

- In Python, `unreal.Rotator(roll, pitch, yaw)` takes this order. The editor's Details panel shows X = Roll, Y = Pitch, Z = Yaw.
- The signs were computed, not guessed. For each side, the script picked the pitch sign that sends the hand outward (inward for me), and Meta's roll sign that sends its hand back.
- After setting them, check in the editor that each left arm's hand goes outward and that the pair is mirror-symmetric.

**Why each robot fits this way** (the sheets show each one):

- **OpenAI.** The sleeves now grow out of the sloping shoulders beside the collar, angled out like the concept's raglan sweater, with no gap from z 74 down. The dome's last 1.5 cm touches the slope, and only a sliver shows above it.
  - The fold barely moves. With `FoldRoll` 33 the folded right hand lands at (35, 14, 56), against (31, 15, 62) today, so the hands still stop about 17 cm apart (18 today).
  - Optional: `FoldRoll` **45** brings the folded hands together (each reaches Y 0.9), which T79 meant ("presses its hands together"). It is one pin, `SetFoldRoll`'s `select _v 33.0` in `SetPersona`. Decide it from the editor's screenshot.
- **Anthropic.** The ball shoulder sinks about half its diameter into the egg's shoulder, so it reads as a joint. The 20° tilt stays, and the hand and rings clear the egg's wide middle (z 49 to 69).
- **SpaceXAI.** The arm is tilted 32° out and hung from the body's own side socket, so the spring runs into the socket and only the lime cap shows against it. That matches the concept, where the arms angle out from the ball.
  - At rest no steel shows above the cap. While talking, the spring stays in the socket. In the cheer, the spring points up out of the socket into the raised arm, like a joint.
  - An alternative if my person wants the concept's visible springs: pivot (33, 75) with the joint point 7 below the top (the spring's outer end) and a tilt of 30. That shows 2 to 3 cm of spring between socket and cap (`a_spacexai` in the tools), but the cheer then swings the spring out below the arm.
- **Meta.**
  - The flat stub goes up under the black shirt's shoulder, so the shoulder flap covers it from the front.
  - The arm angles 12° out and 8° back. The 8° back plus 3 cm back covers most of the pale fin from the side. Most of the forward bend that remains is in the forearm.
  - `HandSocket` moves 7 cm back and 7 cm outward with the hand.
  - The glove brushes the pants at the idle roll's low end (8% of the hand's vertices are inside at a 2° roll, 2% at 6°, none at 10°). Check it in the editor.
- **Me.** The sleeve hugs the box's side, about 1.4 cm into it, from the box's top corner down. Its round top sits at z 104, 0.8 under the box's top edge, like the concept's sleeves starting at the corners. The −6° straightens the sleeve's own curve along the flat side. The glove brushes the box's lower edge (9% of the hand's vertices inside at a 2° roll, 4% at 6°, 1% at 10°).

### The change to `SetPersona`

Make these changes in `Graphs/BP_Robot/SetPersona.txt`, after re-reading it as T104 left it, and write the graph with `BlueprintTools.write_graph_dsl` as `Graphs/README.md` says. They change the option pins of the `select` chains that feed the two `ArmPivot` `SetRelativeLocation` nodes and `HandSocket`'s `SetRelativeLocation`:

```diff
-  ; T103: the shoulders of each new body, 4 cm under each arm's top, which sits where the turnaround has it, just outside the body. Anthropic's arms angle 20 degrees out from its egg (AArmXL/AArmXR).
-  (bind _sy (select _v 30.0 (select _w 34.0 (select _o 39.0 (select _p 30.0 33.0)))))
-  (bind _sz (select _v 72.8 (select _w 74.0 (select _o 81.0 (select _p 66.0 94.0)))))
+  ; T109: each shoulder pivot sits where the arm enters its body (T109-build.md): OpenAI's sleeves come out of the sloping shoulders, Anthropic's ball sinks half into the egg,
+  ; SpaceXAI's spring goes into the body's side socket, Meta's stub goes up under the shirt's shoulder, my sleeves hug the box from its top corners. Each arm's tilt is on its component (xArmXL/xArmXR).
+  (bind _sy (select _v 21.0 (select _w 31.0 (select _o 27.5 (select _p 22.0 27.0)))))
+  (bind _sz (select _v 69.0 (select _w 75.5 (select _o 80.0 (select _p 63.0 98.0)))))
```

```diff
-  (Transformation|SetRelativeLocation :self (Variables|Default|GetHandSocket) :NewLocation (select _v (Math|Vector|MakeVector :X 0.1 :Y 1.6 :Z -36.3) (select _w (Math|Vector|MakeVector :X 0.6 :Y 15.7 :Z -42.4) (select _o (Math|Vector|MakeVector :X -0.3 :Y 0.7 :Z -37.2) (select _p (Math|Vector|MakeVector :X 10.7 :Y -1.5 :Z -29.5) (Math|Vector|MakeVector :X 9.0 :Y 5.7 :Z -59.9))))))
+  (Transformation|SetRelativeLocation :self (Variables|Default|GetHandSocket) :NewLocation (select _v (Math|Vector|MakeVector :X 0.1 :Y 11.1 :Z -36.5) (select _w (Math|Vector|MakeVector :X 0.7 :Y 16.1 :Z -42.9) (select _o (Math|Vector|MakeVector :X -0.1 :Y 23.2 :Z -35.6) (select _p (Math|Vector|MakeVector :X 3.9 :Y 5.4 :Z -32.1) (Math|Vector|MakeVector :X 7.8 :Y -0.7 :Z -60.3))))))
```

If the left hand gets its own socket (below), add its line right after `HandSocket`'s, with each Y negated:

```lisp
  (Transformation|SetRelativeLocation :self (Variables|Default|GetHandSocketL) :NewLocation (select _v (Math|Vector|MakeVector :X 0.1 :Y -11.1 :Z -36.5) (select _w (Math|Vector|MakeVector :X 0.7 :Y -16.1 :Z -42.9) (select _o (Math|Vector|MakeVector :X -0.1 :Y -23.2 :Z -35.6) (select _p (Math|Vector|MakeVector :X 3.9 :Y -5.4 :Z -32.1) (Math|Vector|MakeVector :X 7.8 :Y 0.7 :Z -60.3))))))
```

Optional, from OpenAI's fold above: `(Variables|Default|SetFoldRoll (select _v 33.0 0.0))` → `45.0`.

### `Receive`: the left hand

The left hand's slot 1 is a fixed `Off` (0, −5, −44) on `ArmPivotL`. After the re-fit, the left hand centres on `ArmPivotL` are: OpenAI (0.1, −11.1, −36.5), Anthropic (0.7, −16.1, −42.9), SpaceXAI (−0.1, −23.2, −35.6), Meta (3.9, −5.4, −32.1) and me (7.8, 0.7, −60.3).

- **Recommended:** add a Scene component `HandSocketL` on `ArmPivotL`, place it in `SetPersona` (the line above), and change `Receive`'s second `FlyToComp` to `:Comp (V HandSocketL) :Off (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 0.0)`. That edits `Graphs/BP_Robot/Receive.txt` too. A new component is a `BP_Robot` change inside T109's Touches.
- **Without a new component:** feed that `Off` pin a `select` on the persona with the five vectors above. `Receive` has no `_v`…`_h` binds, so it would need its own `EqualExactly(String)` on `PersonaId`.

### What to check because it depends on the pivots

- **`EventGraph`'s tick.**
  - The idle roll (2° to 10° out): the fits above were judged across it.
  - Talking (52°) and the cheer (150°): see the sheet. The cheer puts the hands beside or behind the big heads on every robot, as it does today. Check that no hand comes through a face.
  - OpenAI's fold: `FoldRoll` above.
  - The cut branch: the pivots go to 0, so the arms hang at their component tilt while the Rig slumps and tips. Look at a fallen robot from the house camera.
- **`HandSocket`:** grab, hold, throw and give. On SpaceXAI the socket keeps the pivot's rotation (0 relative to `ArmPivotR`), so a held prop stays upright while the hand and forearm are tilted 32°. Check that a held prop doesn't cut into the forearm. `HandSocket`'s Y grows from 0.7 to 23.2 because the arm now hangs out at an angle from a pivot further in.
- **`Receive`'s left slot** (above).
- **`Emote` and `GestTick`** move the whole Rig, so they can't open a shoulder gap. `emote_test` (step 5) still shows every emotion with the new arms.
- **The cut robot's fall and its getting back up** (`SetCut`, `Rise`, the tick's `Slump` and `TipRoll`) don't name the pivots. They only need a look.
- **T104's costumes:** the cube hood's short cape and the dino hood's jaw sit on the head. Arms raised in the cheer may pass through them. That was T104's open question 4, and it still applies with the new shoulders.

## Step 4: which robot may need more than a re-fit

- **Meta's pale fin** is the only thing the re-fit doesn't close. It is body geometry, 3 to 4 cm proud of the shirt (z 45 to 64, X −9 to +5.5), and it shows under a raised arm while talking or cheering, today and after alike (the talk and cheer frames on the sheet).
  - At rest the new arm covers it from the front and mostly from the side.
  - Fixes that need no paid call: cut it off with a plane cut at |Y| 22.5 between z 44 and 64 in Modeling Tools (it's one closed mesh, so close the cut), or paint it in `T_Meta_Body` to the shirt's black and mustard, which hides its color but not its shape.
  - A new body from Hyper3D is the paid fix, and it isn't needed for the arms.
  - Ask my person from the editor's talk frame, since it is a body change, not a shoulder change.
- **No robot needs a shoulder cap or a new arm** by these numbers.
  - SpaceXAI's spring and Meta's stub are hidden at rest by the re-fit.
  - My round sleeve top sits flush under the box's top edge. If my person reads it as a stub in the editor, lower my pivot 2 cm (z 96) before thinking about a cap.

## Open questions (only the editor or T104 can answer)

1. **Are the arm components what `armfit.json` says?** Read the ten `xArmX*` transforms (and their names) before writing new ones. If they differ, re-run `final.py` from their real values. Every new number here is computed from the meshes and the pivots, not from today's component values, so it holds either way.
2. **Do the pivots and the bodies share the Rig's frame?** The measuring assumes `ArmPivotL`/`ArmPivotR`, the bodies and the heads are all children of `Rig` with no extra offset (T79's build sheet).
3. **How does it read from the house camera, in the game's light?** The renders are orthographic and lit by SceneKit. Take step 2's and step 5's shots.
4. **SpaceXAI's springs:** hidden (this fit) or showing, like the concept (the alternative)? My person chooses from the sheet.
5. **OpenAI's fold:** keep `FoldRoll` 33, which matches today, or 45 so its hands touch?
6. **Meta's pale fin:** cut it, paint it, or leave it?
7. **Held props on the tilted arms** (SpaceXAI 32°, Anthropic 20°): do they clip the forearm?
8. **Re-read after T104's push:** `Graphs/BP_Robot/SetPersona.txt`, `EventGraph.txt` and `Receive.txt` as T104 commits them. Check for any new attach point on the arms or shoulders, and how T104's costumes sit when the arms rise (its open question 4). Then re-check `Docs/tasks/T104.md`'s findings.
