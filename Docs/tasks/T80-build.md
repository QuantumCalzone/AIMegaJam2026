# T80 build sheet: Meta's android and my cardboard costume

Back to [T80](T80.md) and [the plan](../Plan.md). A Mac prep session wrote this on 2026-11-15, without the editor. It is a plan, not a record: nothing in `Content/`, `Tools/`, `Config/` or `Graphs/` changed, and the design doc was read, not changed.

**Written for `BP_Robot` as [T79-build.md](T79-build.md) leaves it,** on `noHumansOnSet` at `969fbd6` (T79's sheet pushed; T79 itself not built). At that commit the newest change to `BP_Robot` is **T57's `SetPassed(On)`** (`069d4f6`), which puts "(passed)" on its own line above the name on the label and changes no graph this sheet touches. Every DSL block below starts from T79's version of the graph (T79-build part 3), not from today's pushed file, because T79 rewrites those graphs first. T47, T75 and T38 change `BP_Robot` after T80; part 7 says what each must change.

Sources read: `Docs/tasks/T80.md` and its plan entry, everything [T79-build.md](T79-build.md) lists, T79's own sheet, `Docs/BotArt.md` with meta.png, you.png, cast.png and the three costume check images, `Docs/tasks/T47-build/costumes.json` (the three headpieces' fits), and T57's `Graphs/BP_Robot/SetPassed.txt` and Findings.

## In short

- **Meta (`copycat`):** a doll-like android built from engine shapes. A pale gold-white round head (60 cm across, top at z 158), small ears, a short nose, glowing yellow-gold eyes (T46's `EyeL`/`EyeR`, recolored) behind thick black wayfarer glasses with a tiny camera dot at each outer corner, and a small stiff charcoal smile (`Smile`). Jointed arms in the doll color, a royal blue tee and pants (the seat color), cream shoes, T79's gold collar and a chunky gold chain of nine links. The headset goes.
- **My robot (`human`):** a person in a cardboard costume. A teal box over the head (66 × 56 × 54 cm) with two dark eye slots, real eyes behind them (white eyeballs with dark pupils, which move and blink with T75), a black marker mouth drawn on with two upturned corner marks, T79's cream ear pods as cardboard-tube ears, a ping-pong ball on a wire for the antenna, and the red and cream scarf around the neck. A bigger teal box as the body with two strips of duct tape and two bottle-cap buttons; striped sleeves, garden gloves, jeans with rolled cuffs, and canvas sneakers.
- **T46's pill is gone:** its body parts, noodle arms, feet, headset and teal panel are deleted. The seat-colored mittens and the antenna stalk become the three shared-head bots' only (`acc` tags), because Meta and I have our own hands and no stalk.
- **Sockets:** `SetPersona` places each one per body and now scales `HeadSocket`: Meta's at (0, 0, 158), scale 0.9; my box's at (−6, 0, 163), scale 1. Both are starting values for the hand fit in part 5, and the final ones go under T80's "## Findings" for T47.
- **Graphs:** `SetPersona` (bodies, faces, sockets, eye colors), `ResetLook` and `SetLit` (only the shared head's eyes, mouth and brows are LEDs; Meta's eyes glow too; my eyes and mouth don't). `Receive`, `SetCut` and the `EventGraph` don't change. Every motion is kept (part 4).
- **No model is needed,** so no Meshy credits. **The robots in `L_Stage` must be re-placed** again.

## Decisions made for my person

My person asked prep sessions to take the task's default or my recommendation on calls that are theirs, and list them here. The T80 session should show this list to my person when it closes the task.

1. **Meta's eyes are T46's `EyeL`/`EyeR`, glowing gold,** poking 2 cm through black lenses, so they read as glowing rings behind dark glasses (meta.png). One new variable, `EyeColor`, gives each bot its eye color: T46's light blue on the shared head, gold for Meta, eye-white for me.
2. **Meta's resting mouth is `Smile`, now charcoal clay** (T46's was a glowing bar): a small stiff line under the nose. The LED `Mouth` stays hidden on Meta, as T75's sheet expects (it shows the `Mouth` in the smile's place while Meta emotes), and on Meta it is ink-colored, not lit.
3. **My eyes are real eyes:** `EyeL`/`EyeR` become white eyeballs (no glow) with a new dark pupil on each (`PupilL`, `PupilR`, children of the eyes, so they move, squash and blink with them). They bulge about 2 cm out of their slots, because an engine-shape box has no real holes; from the house it reads as eyes peeking out.
4. **My drawn smile:** the `Mouth` bar in black marker (no glow), plus two small marker strokes turned up at its ends (`InkL`, `InkR`), so it reads as a smile at rest. The bar still stretches when I talk (a cartoon, as my person chose for T75: "pose the drawn mouth").
5. **My ears are T79's cream ear pods** (the `human` tag added), as you.png shows cream cups on the box's sides. Meta gets its own small doll ears.
6. **The chain is nine gold links** (flattened spheres, turned alternately) hanging in a U over the tee, on top of T79's gold collar, which Meta now shares.
7. **The tee and pants are royal blue,** in the seat color (`seat` tag), so they gray on the cut; the doll skin, shoes, glasses and chain keep their colors. **My two boxes are teal,** in the seat color; the scarf, gloves, jeans, sleeves and sneakers keep theirs.
8. **The ping-pong ball's wire is a thin straight steel rod,** not the old bent stalk. The task's "no wires" rule is about cables; this one is the task's own antenna.
9. **The headpiece fit:** one `HeadSocket` per head, placed and scaled so T47's numbers for the round head fit (Meta smaller and narrower, so scale 0.9; my box is square and flat on top, so its socket sits 5 cm higher and 6 cm back, so hats rest on the lid and the shades sit just in front of the slots). A wig's corners poking out of the box is fine (T80's task says it passes as costume).
10. **T46's parts are deleted,** not hidden, once Meta and my robot no longer use them (13 components). Part 0 checks first that no graph in `BP_Show` names them.
11. **Meta's glasses carry the tag `glasses`,** as Anthropic's do (T79), so T47 hides both pairs under the dark shades.
12. **New `M_Clay` instances:** `MI_Clay_Doll`, `MI_Clay_Black`, `MI_Clay_White`, `MI_Clay_Tape`, `MI_Clay_Denim` and `MI_Clay_Glove`. Colors are first guesses for the stage light; tune on the close-ups.

## 0. Before you start

1. **T79 is pushed and checked**, and `BP_Robot` and `L_Stage` are free. `git pull`, read `Agents/`, `git lfs locks`. Claim T80 and lock `Content/NHOS/Stage/BP_Robot.uasset` and `Content/NHOS/Maps/L_Stage.umap`. `git log --oneline -6 -- Graphs/BP_Robot Content/NHOS/Stage/BP_Robot.uasset` shows T79 after T57.
2. **Start from the pushed graph files.** T79's `Graphs/BP_Robot/{SetPersona,ResetLook,SetLit}.txt` should match T79-build part 3 (with T79's tuned numbers). Put this sheet's lines into them by their text, keeping any number T79 tuned. If T47, T75 or T38 ran first (they shouldn't; they depend on T80 or come later), keep their lines.
3. **Read T79's Findings** for what moved in the build: the `Face` group (or the fallback with face parts on `Rig`), the visor's and the fold's tuned numbers, the springs (engine or Meshy), the collision profile it used. This sheet's numbers for Meta and my robot are their own and don't depend on those, except the face offsets, which assume the face parts' Face-relative places in T79-build part 2b.
4. **Survey** with T79's `Saved/T79/survey.py` (copy to `Saved/T80/`): every component with its parent, transform, tags and material. Check the T46 parts part 2a deletes are there and the T79 parts part 2a retags.
5. **No `BP_Show` graph names a part to be deleted.** In `BP_Show`, `find_nodes` for each of `Body`, `Head`, `BodyLow`, `CapLow`, `Seam`, `Strap`, `Headset`, `HeadsetLens`, `TealPanel` (as variable getters). Expected: none (no pushed source names them, and T79 removed the last robot graphs that did). If one does, hide that part instead of deleting it (tag `acc` with no persona) and say so.

## 1. Materials

| Instance (new, `M_Clay`) | `Color` (linear) | `Rough` | `ThumbScale` | `ThumbDepth` | Used on |
|---|---|---|---|---|---|
| `MI_Clay_Doll` | (0.74, 0.62, 0.45) | (default 0.85) | 0.12 | 0.15 | Meta's head, ears, nose, arms, hands |
| `MI_Clay_Black` | (0.015, 0.015, 0.017) | 0.3 | 0.12 | 0.1 | Meta's glasses (glossy) |
| `MI_Clay_White` | (0.80, 0.78, 0.72) | (default) | 0.12 | 0.15 | the ping-pong ball, the sneakers' toes |
| `MI_Clay_Tape` | (0.40, 0.40, 0.38) | 0.45 | 0.12 | 0.1 | duct tape |
| `MI_Clay_Denim` | (0.06, 0.11, 0.24) | (default) | 0.5 | 0.3 | jeans and cuffs |
| `MI_Clay_Glove` | (0.62, 0.56, 0.44) | (default) | 0.5 | 0.5 | garden gloves (knit, like T79's sweater) |

From T79: `MI_Clay_Seat` (seat color at run time), `MI_Clay_Cream`, `MI_Clay_Charcoal`, `MI_Clay_Gold`, `MI_Clay_Steel`. Make the new ones as T79 did (T46's `mi()` helper; `Rough` is `M_Clay`'s third scalar, T43). T46 found bright cream washes to white under the spotlight; the doll skin is a little darker than T46's cream for that reason.

## 2. `BP_Robot`'s components

Numbers as in T79-build part 2: relative to `Rig` unless the parent column says otherwise, in cm, `Rig` +X is the face, Z up, floor z 0; engine shapes are 100 cm; rotations are (roll, pitch, yaw). "L, R" rows list the left (−Y) value first: (0, ∓10, 30) means left at y −10 and right at y +10. "R3" is the tags `visionary`, `worrier`, `overclocker`. New static mesh components take T79's collision profile and cast shadows.

### 2a. What changes on T79's robot

| Part | After T79 | T80 |
|---|---|---|
| `Body`, `Head`, `Seam`, `BodyLow`, `CapLow`, `ArmL`, `ArmR`, `FootL`, `FootR` | T46's pill, tags `acc`, `copycat`, `human` | **deleted** |
| `Strap`, `Headset`, `HeadsetLens` (Meta's headset), `TealPanel` (mine) | T46's | **deleted** (the task: "The headset topper goes") |
| `HandL`, `HandR` | shared mittens, tag `seat` | tags `acc`, R3, `seat` |
| `Nub` (the stalk) | shared, bent for me by `SetPersona` | tags `acc`, R3 (the halo, light and bolt sit on it; Meta has no topper, and my antenna is the new wire) |
| `Visor` | shared; `SetPersona` sets it per head | tags `acc`, R3; `SetPersona`'s two `Visor` lines go (the template holds the round head's values) |
| `Collar` (gold) | tags `acc`, R3 | add `copycat` |
| `EarL`, `EarR` (cream) | tags `acc`, R3 | add `human` |
| `Smile` | `Face` (34.5, 0, 122), `MI_SmileGlow` | `Face` (33.2, 0, 122), scale (0.02, 0.12, 0.012), **`MI_Clay_Charcoal`** |
| `ScarfA`, `ScarfB`, `ScarfTail`, `ScarfStripe` | T46's, on the pill | kept, moved to my box (2c) |
| `EyeL`, `EyeR`, `Mouth` | on `Face` | unchanged; `SetPersona` sets the `Mouth`'s place per head and the eyes' scale |

### 2b. Meta (`copycat`), tags `acc`, `copycat`

| Component | Parent | Mesh | Location | Rotation | Scale | Material | Extra tags |
|---|---|---|---|---|---|---|---|
| `MHead` | `Rig` | Sphere | (0, 0, 128) | 0 | (0.60, 0.62, 0.60) | Doll | |
| `MEarL`, `MEarR` | `Rig` | Cylinder | (0, ∓31, 126) | roll 90 | (0.13, 0.13, 0.06) | Doll | |
| `MNose` | `Rig` | Sphere | (29.5, 0, 124) | 0 | (0.07, 0.06, 0.09) | Doll | |
| `MGlassL`, `MGlassR` | `Rig` | Cube | (31, ∓12, 134) | 0 | (0.025, 0.21, 0.14) | Black | `glasses` |
| `MBrowBar` | `Rig` | Cube | (31.2, 0, 141.5) | 0 | (0.035, 0.48, 0.035) | Black | `glasses` |
| `MBridge` | `Rig` | Cube | (31, 0, 136) | 0 | (0.025, 0.05, 0.03) | Black | `glasses` |
| `MTempleL`, `MTempleR` | `Rig` | Cube | (15.5, ∓26.8, 138) | yaw ±15 | (0.32, 0.012, 0.02) | Black | `glasses` |
| `MCamL`, `MCamR` | `Rig` | Sphere | (32.4, ∓21, 139.5) | 0 | (0.022, 0.022, 0.022) | Steel | `glasses` |
| `MTee` | `Rig` | Cube | (0, 0, 72) | 0 | (0.30, 0.46, 0.40) | Seat | `seat` |
| `MSleeveL`, `MSleeveR` | arm pivots | Cube | (0, ∓1, −5) | 0 | (0.15, 0.13, 0.14) | Seat | `seat` |
| `MUpperL`, `MUpperR` | arm pivots | Cylinder | (0, ∓2, −14) | 0 | (0.085, 0.085, 0.18) | Doll | |
| `MElbowL`, `MElbowR` | arm pivots | Cylinder | (0, ∓2, −23.5) | 0 | (0.09, 0.09, 0.012) | Charcoal | |
| `MForeL`, `MForeR` | arm pivots | Cylinder | (0, ∓3, −31.5) | 0 | (0.085, 0.085, 0.15) | Doll | |
| `MWristL`, `MWristR` | arm pivots | Cylinder | (0, ∓3, −39) | 0 | (0.09, 0.09, 0.012) | Charcoal | |
| `MHandL`, `MHandR` | arm pivots | Sphere | (0, ∓5, −44) | 0 | (0.15, 0.12, 0.17) | Doll | |
| `MHips` | `Rig` | Cube | (0, 0, 50) | 0 | (0.28, 0.42, 0.08) | Seat | `seat` |
| `MLegL`, `MLegR` | `Rig` | Cylinder | (0, ∓10, 30) | 0 | (0.17, 0.17, 0.40) | Seat | `seat` |
| `MShoeL`, `MShoeR` | `Rig` | Sphere | (5, ∓10, 7) | 0 | (0.30, 0.19, 0.14) | Cream | |
| `Chain0` to `Chain8` | `Rig` | Sphere | link i: t = −1 + i/4, (16.5, 17t, 77 + 17t²) | roll 90 on odd links | (0.05, 0.08, 0.055) | Gold | |

- **The head:** 60 deep, 62 wide, 60 tall (z 98 to 158), so its top is where the round head's is. The tee runs from z 52 to 92 and the gold collar (z 88 to 98) joins it to the chin. The hips and blue legs run down to z 10, the cream shoes from the floor to 14. About 1.58 m to the top of the head, as the task asks.
- **The face** (with `Face` at (−4, 0, −1), part 3a): the eyes at (29, ±11, 134), each 10 cm across, the front 1.75 cm through its lens (the lens's front is at x 32.25), so a glowing disc about 7.6 cm across shows in each black lens; the nose at z 124 under the lenses' bottom edge (127); the stiff smile at (29.2, 0, 121), 12 cm wide. The glasses are flat in front of a round face, as wayfarers are; the temples run back to the ears.
- **The chain:** link 0 at (16.5, −17, 94), link 4 at (16.5, 0, 77), link 8 at (16.5, 17, 94), each 5 deep, 8 wide and 5.5 tall on the tee's front (x 15), the odd ones turned 90° on their roll so the chain reads as links.
- **The arms:** the pivots go to (0, ∓29, 86), the tee's shoulders. A blue sleeve, then the upper arm, a charcoal joint line, the forearm, another joint line and the doll hand at −44, where the right `HandSocket` already is.

### 2c. My robot (`human`), tags `acc`, `human`

| Component | Parent | Mesh | Location | Rotation | Scale | Material | Extra tags |
|---|---|---|---|---|---|---|---|
| `BoxHead` | `Rig` | Cube | (0, 0, 131) | 0 | (0.56, 0.66, 0.54) | Seat | `seat` |
| `LidTape` | `Rig` | Cube | (27.6, 0, 156.5) | 0 | (0.012, 0.66, 0.03) | Tape | |
| `SlotL`, `SlotR` | `Rig` | Cube | (28.2, ∓11, 138) | 0 | (0.01, 0.14, 0.09) | Charcoal | |
| `PupilL`, `PupilR` | `EyeL`, `EyeR` | Sphere | (40, 0, 0) (in the eye's own units) | 0 | (0.45, 0.5, 0.5) (of the eye) | Charcoal | |
| `InkL`, `InkR` | `Face` | Cube | (35.9, ∓6.5, 119.7) | roll ∓25 | (0.02, 0.035, 0.008) | Charcoal | |
| `Wire` | `Rig` | Cylinder | (0, 0, 168) | 0 | (0.012, 0.012, 0.20) | Steel | |
| `PingPong` | `Rig` | Sphere | (0, 0, 181) | 0 | (0.08, 0.08, 0.08) | White | |
| `BoxBody` | `Rig` | Cube | (0, 0, 70) | 0 | (0.50, 0.62, 0.60) | Seat | `seat` |
| `TapeA` | `Rig` | Cube | (25.3, −4, 88) | roll 4 | (0.008, 0.42, 0.045) | Tape | |
| `TapeB` | `Rig` | Cube | (25.3, 6, 50) | roll −3 | (0.008, 0.38, 0.045) | Tape | |
| `CapA`, `CapB` | `Rig` | Cylinder | (25.6, −16, 80 / 55) | pitch 90 | (0.07, 0.07, 0.015) | Steel | |
| `ScarfA` (T46's) | `Rig` | (T46's) | (0, 0, 102) | 0 | (0.60, 0.60, 0.08) | (T46's red) | |
| `ScarfB` (T46's) | `Rig` | (T46's) | (0, 0, 101) | 0 | (0.61, 0.61, 0.03) | (T46's cream) | |
| `ScarfTail` (T46's) | `Rig` | (T46's) | (27.6, 8, 86) | roll 10 | (0.05, 0.13, 0.30) | (T46's red) | |
| `ScarfStripe` (T46's) | `Rig` | (T46's) | (28.2, 8, 92) | roll 10 | (0.052, 0.132, 0.06) | (T46's cream) | |
| `HSleeveL`, `HSleeveR` | arm pivots | Cylinder | (0, ∓2, −18) | 0 | (0.11, 0.11, 0.36) | Cream | |
| `HStripe0L` to `HStripe3L`, and `…R` | arm pivots | Cylinder | (0, ∓2, −6 / −13 / −20 / −27) | 0 | (0.115, 0.115, 0.02) | Charcoal | |
| `GloveL`, `GloveR` | arm pivots | Sphere | (0, ∓5, −44) | 0 | (0.17, 0.14, 0.19) | Glove | |
| `HJeanL`, `HJeanR` | `Rig` | Cylinder | (0, ∓11, 23) | 0 | (0.15, 0.15, 0.34) | Denim | |
| `HCuffL`, `HCuffR` | `Rig` | Cylinder | (0, ∓11, 9) | 0 | (0.17, 0.17, 0.05) | Denim | |
| `HShoeL`, `HShoeR` | `Rig` | Sphere | (5, ∓11, 6) | 0 | (0.30, 0.17, 0.12) | Charcoal | |
| `HToeL`, `HToeR` | `Rig` | Sphere | (14, ∓11, 4) | 0 | (0.13, 0.15, 0.08) | White | |

- **The head box:** 56 deep, 66 wide, 54 tall (z 104 to 158), its front at x 28, with a strip of tape along the lid's front edge. The two eye slots are dark panels 14 by 9 cm on its front at z 138. T79's cream ear pods (y ±30 to ±38 at z 128) stick 5 cm out of its sides.
- **The eyes** (with `Face` at (−7.5, 0, 3), part 3a): eyeballs 10 cm across at (25.5, ±11, 138), so each pokes 1.8 cm out of its slot and shows a disc about 7.7 cm across inside the 14 × 9 slot. Each pupil is a child of its eye: 4 cm forward in the eye's frame (40 units × the eye's 0.1 scale) and half the eye's size, so it bulges a little at the eye's front. Because the pupils are children, an eye that T75 squashes (`eye_h`) or shifts (`eye_dx`, `eye_dz`) takes its pupil with it, which is how it blinks.
- **The mouth:** the `Mouth` bar moved to (35.9, 0, 119) on `Face` for me (part 3a), which puts it at (28.4, 0, 122), on the box's front, in black marker; the two `InkL`/`InkR` strokes turn up at its ends.
- **The antenna:** a 1.2 cm steel rod from the lid (z 158) to 178, and a white 8 cm ball on it at 181. Both are `acc` parts at z 165 or more, so T47's `InitLift` lifts them with a hat.
- **The body box:** 50 deep, 62 wide, 60 tall (z 40 to 100), its front at x 25, with two strips of tape across it at slight angles and two steel bottle caps. The scarf wraps the gap between the two boxes (z 98 to 106), a little wider than the boxes are deep so it shows all round, with its tail hanging in front of the body.
- **The arms:** the pivots go to (0, ∓33, 94), the body box's top corners: a cream sleeve with four charcoal stripes, then the glove at −44 (`HandSocket`'s place). **The legs:** jeans from z 6 to 40 with rolled cuffs, black canvas sneakers with white toes.

## 3. The graphs

New variables in `BP_Robot`: `EyeColor` (`LinearColor`, default (0.55, 0.85, 1.0, 1)), `LedEyes` and `LedMouth` (Boolean, default true).

### 3a. `SetPersona` (from T79's)

Changes, by their text in T79's version:

1. **Remove** the `Nub` rotation line (`(Transformation|SetRelativeRotation :self (Variables|Default|GetNub) ...)`) and the two `Visor` lines (`SetRelativeLocation` and `SetRelativeScale3D` on `GetVisor`).
2. **The eyes' scale:** in `_es`, the human's (0.14, 0.14, 0.18) becomes (0.10, 0.10, 0.10), and the last value (now Meta's only) becomes (0.10, 0.10, 0.10).
3. **The face:** replace T79's `Face` line, and add the eye colors and the mouth's place, after the eyes' scale:
   ```lisp
   ; T80: each head's face. The shared round head at the origin, Meta's doll face and my box's eyes behind their slots.
   (Transformation|SetRelativeLocation :self (Variables|Default|GetFace) :NewLocation (select _r (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 0.0) (select _p (Math|Vector|MakeVector :X -4.0 :Y 0.0 :Z -1.0) (Math|Vector|MakeVector :X -7.5 :Y 0.0 :Z 3.0))))
   (Transformation|SetRelativeLocation :self (Variables|Default|GetMouth) :NewLocation (select _h (Math|Vector|MakeVector :X 35.9 :Y 0.0 :Z 119.0) (select _p (Math|Vector|MakeVector :X 33.2 :Y 0.0 :Z 122.0) (Math|Vector|MakeVector :X 34.5 :Y 0.0 :Z 123.0))))
   ; T80: LED eyes on the shared head (light blue) and on Meta (gold); my eyes are eyes. Only the shared head's mouth is an LED.
   (Variables|Default|SetEyeColor (select _p (Utilities|Struct|MakeLinearColor :R 1.0 :G 0.62 :B 0.08 :A 1.0) (select _h (Utilities|Struct|MakeLinearColor :R 0.78 :G 0.76 :B 0.7 :A 1.0) (Utilities|Struct|MakeLinearColor :R 0.55 :G 0.85 :B 1.0 :A 1.0))))
   (Variables|Default|SetLedEyes (not _h))
   (Variables|Default|SetLedMouth _r)
   ```
4. **The shoulders:** `_sy` and `_sz` gain Meta's and mine (the pill's 36 and 92 go):
   ```lisp
   (bind _sy (select _v 19.0 (select _w 29.0 (select _o 30.0 (select _p 29.0 33.0)))))   ; T80
   (bind _sz (select _v 80.0 (select _w 76.0 (select _o 74.0 (select _p 86.0 94.0)))))   ; T80
   ```
5. **The sockets:** replace T79's two socket lines with:
   ```lisp
   ; T80: each body's head socket, placed and scaled so T47's headpieces fit every head (Findings has the final numbers), and its back socket.
   (Transformation|SetRelativeLocation :self (Variables|Default|GetHeadSocket) :NewLocation (select _h (Math|Vector|MakeVector :X -6.0 :Y 0.0 :Z 163.0) (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 158.0)))
   (bind _hs (select _p 0.9 1.0))
   (Transformation|SetRelativeScale3D :self (Variables|Default|GetHeadSocket) :NewScale3D (Math|Vector|MakeVector :X _hs :Y _hs :Z _hs))
   (Transformation|SetRelativeLocation :self (Variables|Default|GetBackSocket) :NewLocation (select _v (Math|Vector|MakeVector :X -30.0 :Y 0.0 :Z 60.0) (select _w (Math|Vector|MakeVector :X -34.0 :Y 0.0 :Z 52.0) (select _o (Math|Vector|MakeVector :X -33.0 :Y 0.0 :Z 62.0) (select _p (Math|Vector|MakeVector :X -16.0 :Y 0.0 :Z 72.0) (Math|Vector|MakeVector :X -26.0 :Y 0.0 :Z 70.0))))))
   ```
6. `BobSpeed` and `BobAmp` stay: Meta's 0.7 and 0.6 (a stiff doll) and my 2.0 and 2.5 already fit.

- **`HeadSocket`'s scale 0.9 on Meta** also scales a head prop's grip offset by 0.9 (`BP_Prop.TickFly` applies the socket's world transform; T79-build part 2b). Props are all worn in the hand today (T45), so nothing shows it; if a head prop looks off on Meta, it is that.
- With the pill gone, `_r` is false only for Meta and me, so every `select _r` picks between the round head and those two.

### 3b. `ResetLook` (from T79's)

```lisp
  ; T80: each bot's eye color; the mouth is an LED only on the shared head, black marker or ink on the others.
  (bind _eye (Math|Conversions|ToVector(LinearColor) (Variables|Default|GetEyeColor)))
  (bind _ink (Math|Vector|MakeVector :X 0.015 :Y 0.015 :Z 0.015))
  (Rendering|Material|SetVectorParameterValueonMaterials :self (Variables|Default|GetEyeL) :ParameterName "Color" :ParameterValue _eye)
  (Rendering|Material|SetVectorParameterValueonMaterials :self (Variables|Default|GetEyeR) :ParameterName "Color" :ParameterValue _eye)
  (Rendering|Material|SetVectorParameterValueonMaterials :self (Variables|Default|GetMouth) :ParameterName "Color" :ParameterValue (select (Variables|Default|GetLedMouth) _eye _ink))
```

These replace T46's `(bind _eye (Math|Vector|MakeVector :X 0.55 :Y 0.85 :Z 1.0))` and its three lines on `EyeL`, `EyeR` and `Mouth`. The four brow lines keep `_eye`: only the worrier and the overclocker show resting brows, and their `EyeColor` is T46's light blue. The rest of T79's `ResetLook` stays.

### 3c. `SetLit` (from T79's)

The `Glow` on the eyes and the mouth follows the new flags (the brows' lines stay):

```lisp
  ; T80: only LEDs glow: the shared head's eyes and mouth, and Meta's eyes.
  (bind _g (select On 10.0 3.0))
  (Rendering|Material|SetScalarParameterValueonMaterials :self (Variables|Default|GetEyeL) :ParameterName "Glow" :ParameterValue (select (Variables|Default|GetLedEyes) _g 0.0))
  (Rendering|Material|SetScalarParameterValueonMaterials :self (Variables|Default|GetEyeR) :ParameterName "Glow" :ParameterValue (select (Variables|Default|GetLedEyes) _g 0.0))
  (Rendering|Material|SetScalarParameterValueonMaterials :self (Variables|Default|GetMouth) :ParameterName "Glow" :ParameterValue (select (Variables|Default|GetLedMouth) _g 0.0))
```

These replace the three lines on `EyeL`, `EyeR` and `Mouth`. With `Glow` 0, `M_Robot` shows its `Color` as a plain surface (check on the close-up that my eyeballs read as white, not gray; if `M_Robot` needs some glow to show color at all, give my eyes a fixed 0.6 and say so).

### 3d. Graphs that don't change

- **`Receive`:** T79's sockets already serve every body; T80 only places them (3a).
- **`SetCut`:** T79's `seat` loop grays Meta's tee, sleeves, hips and legs and my two boxes; the eyes and mouth go dark as before (my eyeballs turn dark gray, which reads as "out"). The glasses, chain, skin, scarf and clothes keep their colors.
- **`EventGraph`:** unchanged. `HoverZ`, `FoldPitch` and `FoldRoll` are 0 for both, the mouth's talking stretch works on my marker mouth and on Meta's hidden `Mouth` alike, and the warning-light pulse is the worrier's only.
- **The construction script** still calls `SetPersona(PreviewPersona)`, so `Robot4` shows Meta and `Robot2` my costume in the editor.

## 4. Every motion, kept (step 4)

T79-build part 4 lists every motion the robot has, from the graphs. Each still works for Meta and me because every new part is under `Rig` or an arm pivot (the bob, the talking bounce, the cheer's hop, the shake's yaw and the cut's slump and tip move `Rig`; the arm flap and cheer move the pivots; moves, hops and turns move the actor), the right hand is `HandSocket` (grab, throw, give), and the cut grays every `seat` part. Two checks particular to T80:

- **My pupils ride on my eyes** (children), so `SetPersona`'s eye scale, and T75 later, scale and move them too.
- **The arm pivots' new places** (Meta's 86, my 94) make the cheer's 150° arms rise from the tee's and the box's shoulders; check in a cheer frame that the arms clear the head (Meta's head starts at z 98; my box at 104 and 33 wide, so my arms swing up beside it).

The height is about 1.58 m to the head's top for both (my ball to 185), as the task asks; the labels (z 228) and T38's bubbles keep their places.

## 5. Sockets and the headpiece fit (step 3)

1. **Start** from the numbers in 3a: Meta's `HeadSocket` at (0, 0, 158), scale 0.9; mine at (−6, 0, 163), scale 1.
2. **Try three headpieces by hand on both, without saving.** In the editor (not PIE), with editor Python: for each of the top hat, the bob wig and the dark shades, spawn a `StaticMeshActor` with the mesh, attach it to the robot's `HeadSocket` (`actor.attach_to_component(socket, socket_name="", location_rule=unreal.AttachmentRule.KEEP_RELATIVE, rotation_rule=unreal.AttachmentRule.KEEP_RELATIVE, scale_rule=unreal.AttachmentRule.KEEP_RELATIVE, weld_simulated_bodies=False)`; the socket is the robot's scene component named `HeadSocket`), and set its relative transform to the fit below. Capture a close-up (T79-build part 6 step 3's camera), then destroy the actor. Never save `L_Stage` while one of these actors is in it.

   | Headpiece | Mesh | Scale | x | z (from the socket) | yaw |
   |---|---|---|---|---|---|
   | top hat | `/Game/NHOS/Stage/Headpieces/SM_TopHat` | 0.3787 | 0 | 19.7 | 270 |
   | bob wig | `/Game/NHOS/Stage/Headpieces/SM_BobWig` | 0.4502 | −4 | −23.1 | 270 |
   | dark shades | `/Game/NHOS/Stage/Headpieces/SM_DarkShades` | 0.4338 | −1.3 | −22.7 | 270 |

   These are T47's draft fits (`Docs/tasks/T47-build/costumes.json`) for the round head, measured from the head's top (z − 158), with T79's change to the shades (19 cm higher, 4 cm forward: T79-build part 8). The socket's scale applies on top. If T47's numbers changed by then, use T47's.
3. **Tune each socket, not the fits:** move and scale `HeadSocket` until all three sit right on that head, then change 3a's numbers to match. One socket per head must suit all three (and so all 14 headpieces):
   - **Meta:** the hat rests on the crown, the wig's bangs stop above the glasses, and the shades sit in front of Meta's own glasses and hide them (T47 hides the `glasses` parts while the shades are on; for this try, hide them by hand).
   - **My box:** the hat rests on the lid (a hat sized for a dome would sink 8 cm into a flat lid, which is why the socket sits 5 cm higher), the wig covers the lid with its corners poking out at the box's edges (the task: that passes as costume), and the shades sit just in front of the eye slots. The socket sits 6 cm back so the shades don't float in front of the box; if the hat then looks pushed back, split the difference.
4. **Write each socket's final transform** (location, scale) under T80's "## Findings" for T47, with what each of the six close-ups showed.

## 6. Re-place the robots, and the check (steps 4 and 5)

**Re-place the five robots** in `L_Stage` as in T79-build part 5 (T79's `Saved/T79/robots.py` and `replace.py`, copied to `Saved/T80/`): T80 adds and deletes components, and template changes don't reach placed robots (T17, T46). Dump first, re-place with the same label, folder, `Seat`, `FallDir` and `PreviewPersona`, save `L_Stage`.

**The check** (switches as in T79-build part 6: free autoplay, `spare_human`, `fast_lines`, `ai_seats` 0; shots to `Saved/T80/shots/`):

1. **Compile** with no error; the survey after the build matches part 2.
2. **All five side by side from the house camera** (PIE, T46's way), next to [cast.png](../BotArt/cast.png): read both images together. The five must read as the cast sheet: three polished bots on the shared head in pale blue, orange and lime, Meta's doll with its black glasses, blue tee and gold chain, and my teal cardboard costume with its scarf and ping-pong ball. **My robot must read as a person in a costume** next to four polished bots: the boxes' hard edges, the tape, the eyes in the slots, the striped sleeves and the jeans.
3. **Close-ups** of Meta and my robot (T79-build part 6 step 3's camera), each beside its concept image: Meta's glowing eyes inside the lenses, the camera dots, the nose and stiff smile, the chain's links, the joints; my eyes in their slots with pupils, the marker smile with its upturned ends, the tape and caps, the scarf's wrap and tail, the sleeves' stripes.
4. **The three headpieces on both new heads** (part 5): six close-ups.
5. **A held prop** on Meta and on me (in the right hand, through `HandSocket`), and **a cut** of either one (the tee or the boxes gray, the eyes dark, tipped over).
6. **A free autoplay show in a game window** reaches `NHOS: SHOW END` with no `LogScript` line (T79-build part 6 step 6's commands, with `-log=T80.log`).
7. **Judge, as a critical first-time player** (the Done-when): do the five read as the cast sheet from the house camera, and does my robot read as a person in a costume? Write what each shot showed under T80's "## Findings", with what wasn't seen.

**What to tune first:** the doll skin and the white parts under the spotlight (T46: bright colors wash out), the size of my eyes in their slots, Meta's eyes in the lenses, the chain's link size, and the sockets (part 5).

## 7. What T80 commits, and later tasks

**Commit:** `Content/NHOS/Stage/BP_Robot.uasset`, `Content/NHOS/Maps/L_Stage.umap`, the six new instances in `Content/NHOS/Stage/Materials/`, `Graphs/BP_Robot/{SetPersona,ResetLook,SetLit}.txt`, `Docs/tasks/T80.md` (Result and Findings, with the socket transforms and "Decisions made for my person"), the plan's box and `Docs/DevLog.md`. No model, so no `Docs/Assets.md` row. Unlock both assets after the push.

### T47 (headpieces)

On top of T79-build part 8's list:

1. **The socket transforms** are in T80's Findings (starting values: Meta (0, 0, 158) at scale 0.9, my box (−6, 0, 163) at scale 1). `MakeHat` attaches the hat to `HeadSocket` with `KeepRelative`, so the socket's scale applies to every headpiece; `costumes.json` keeps one fit per headpiece.
2. **Meta's glasses carry the tag `glasses`** too: T79-build part 8 item 5's loop hides them under the dark shades with no extra line.
3. **My antenna:** `Wire` and `PingPong` are `acc` parts at z 165 or more, so `InitLift` lifts them with a hat. Meta has no topper, so nothing of Meta's lifts. `Nub` is now the shared head's only; `InitLift` adds it by name, and lifting it on Meta or me moves a hidden part, which is harmless.
4. **A hat on my box sits 5 cm higher** than on the round head (the socket), so a tall hat's `lift` leaves my ball 5 cm lower over its brim than the round bots' toppers. If the ball disappears into a hat, raise that headpiece's `lift`.

### T75 (emotions): `FaceParts` after T80 ([T75-build.md](T75-build.md) part 2g)

| Head | Parts | Notes |
|---|---|---|
| Meta's doll head | `PEyeL`/`PEyeR` = `EyeL`/`EyeR` (glowing gold, behind the lenses); `PMouth` = `Mouth` (hidden at rest, ink, not lit); `PSmile` = `Smile` with `HasSmile` true | clamp `eye_dx` and `eye_dz` so each eye stays inside its 21 × 14 cm lens; `LedColor` = `EyeColor`; `TintMouth` off (as T75 planned); brows: T75's run-time brows, above the glasses' top bar (z 141.5) in dark clay (my person's answer 2) |
| My box | `PEyeL`/`PEyeR` = `EyeL`/`EyeR` (eyeballs; their pupils are children and follow); `PMouth` = `Mouth` (black marker) | clamp the eyes to their 14 × 9 cm slots; treat `InkL` and `InkR` like a smile (`PSmile`-style: hide them while emoting, so T75's corner bars curve the mouth instead); every tint off; brows: black marker just above the slots (z about 145) |

- **`EyeColor`** (new in T80) is each bot's resting eye color: T75's `LedColor` can read it instead of naming colors.
- **`LedEyes` and `LedMouth`** say which parts glow; T75's glow or tint on a part whose flag is off should stay off.
- **`FaceR`:** Meta's head curves at about 30 cm; my box is flat (use a large `FaceR`, such as 1,000, so the corner bars don't step back).
- The `Face` offsets per head are in 3a: Meta (−4, 0, −1), my box (−7.5, 0, 3).

### T38 (bubbles)

Nothing moves: the label is on the root at z 228, and no robot is taller (my ping-pong ball tops out at 185).

## Findings

(For the T80 session: the socket transforms, the six headpiece close-ups, and what the check showed.)
