# T79 build sheet: one round head and three bodies

Back to [T79](T79.md) and [the plan](../Plan.md). A Mac prep session wrote this on 2026-11-15, without the editor. It is a plan, not a record: nothing in `Content/`, `Tools/`, `Config/` or `Graphs/` changed, and the design doc was read, not changed (Art Inspiration rev 30).

**Written against `noHumansOnSet` at `9fa160a`,** where the newest change to `BP_Robot` is T46's (`478a76e`) and every `Graphs/BP_Robot/` file is as T46 left it. **T57 adds one function to `BP_Robot`: `SetPassed(On)`**, which puts "(passed)" on its own line above the name on the label, in `UIStyle`'s `Quiet` color. **Re-checked after T57 landed (`069d4f6`):** T57 added only `Graphs/BP_Robot/SetPassed.txt` and changed none of the six graphs this sheet changes (`git diff 9fa160a 069d4f6 -- Graphs/BP_Robot` shows only the new file), and it left the label where it was (on the root at z 228, bottom-aligned, T57 Findings). So nothing below moved. T47, T75 and T38 change `BP_Robot` after T79; part 8 says what each must change.

Sources read: `Docs/tasks/T79.md`, `T80.md` and their plan entries, `T46.md`, `T43.md`, `T45.md`, `T47.md`, `T47-build.md`, `T57-build.md` (part 1), `T75-build.md` (parts 0, 2 and 2g), `T38-build.md` (its `BP_Robot` part), `T49.md` (editor rules), `T40.md` to `T42.md` (Meshy prices), `Docs/BotArt.md` and the five concept images, every file in `Graphs/BP_Robot/`, `Graphs/BP_Prop/{FlyToComp,TickFly}.txt`, `Tools/art_gen.py` (prices), and T46's own scripts and dumps in the Mac's `Saved/T46/` (`build.py`, `parts.json`, `robots.json`, `replace.py`; not in git), which hold the component numbers T46 used.

## In short

- **The shared round head** (`RHead`): an oval 70 cm wide, 66 deep and 62 tall, in the seat color, whose top is at z 158 in `Rig`, exactly where T46's dome tops out. So the antenna stalk, the toppers, the label and T47's hat heights stay where they are. A larger, flatter dark screen (`Visor`), T46's LED eyes and stretching mouth on it, two cream ear pods, a short gold collar.
- **A `Face` scene component** now holds the eyes, mouth, brows and `Smile`. On the round head it sits at the origin; on T46's pill (Meta and my robot until T80) `SetPersona` moves it to (2.5, 0, −21), which puts every face part within 2 cm of where T46 had it.
- **Sockets:** `HeadSocket` and `BackSocket` on `Rig`, `HandSocket` on the right arm pivot. `Receive` attaches head, back and right-hand props to them, with no offset. `SetPersona` places `HeadSocket` and `BackSocket` per body; Meta and my robot keep T46's heights (160 and back 106) until T80.
- **Three bodies,** each about 1.6 m tall, built from engine shapes and `M_Clay` instances and shown by T46's `acc` tag rule: OpenAI's pale-blue teardrop in a gray knit sweater that hovers 8 cm over a glowing floor ring with its hands pressed together; Anthropic's round orange body with cream belly, buttons, round feet and circular gold glasses; SpaceXAI's round lime body on coiled spring arms and legs, chunky boots, a long nose and a toothy grin. No model is needed; the springs have a 5-credit Meshy fallback (part 2e).
- **Tags instead of names:** every seat-colored part carries the tag `seat`, so `ResetLook` colors and `SetCut` grays them in one loop, and a new body needs no graph line. OpenAI's ring parts carry `ring` (off on the cut), Anthropic's glasses `glasses` (T47 hides them under the dark shades).
- **Graphs changed:** `SetPersona`, `Receive`, `ResetLook`, `SetCut`, `SetLit` and the `EventGraph` (the hover and OpenAI's folded hands). Every motion is kept (part 4).
- **`L_Stage`:** the five robots must be re-placed (the T17 and T46 rule), with their seat, fall direction and preview persona.
- **New materials:** `MI_Clay_Gold`, `MI_Clay_Knit` and `MI_Clay_Steel` (`M_Clay`), and `MI_Robot_Screen` (`M_Robot`, the visor's dark color, for the glasses' lenses).

## Decisions made for my person

My person asked prep sessions to take the task's default or my recommendation on calls that are theirs, and list them here. The T79 session should show this list to my person when it closes the task.

1. **The head's top stays at z 158,** T46's dome top, and the head is an oval (70 wide, 66 deep, 62 tall, centered at z 127) rather than a 70 cm ball, like the concept heads, which are a little wider than tall. Everything above the head (stalk, halo, warning light, bolt, label, T47's hat heights) keeps its place.
2. **The LED mouth stays on the screen,** as T46 built it and T75 poses it, not on the shell below the screen as openai.png draws it. T75 needs a glowing mouth it can tint and curve.
3. **SpaceXAI's toothy grin is a cream teeth bar over the LED mouth.** At rest the teeth show; when the bot talks, the mouth stretches past the teeth and glows behind them. The nose hangs over the middle of the grin, as in spacexai.png.
4. **Anthropic's glasses are two gold discs with a dark disc in front,** each centered on an eye, so they read as thin gold rings on the dark screen, and the eyes poke through. No model.
5. **The springs are engine shapes:** a thin steel core with three or four flat steel discs along it. If the close-up reads them as a ribbed pipe, not a spring, one Meshy spring model replaces them: Meshy 6 Lite, mesh only, **5 credits** (`Tools/art_gen.py` prices; the last recorded balance is 60, after T42). Not spent by default.
6. **OpenAI keeps short legs and feet** under its teardrop, as openai.png shows (knit cuffs, round feet), and the whole robot hovers 8 cm over a ring of 12 glowing segments on the floor. The ring is on the actor's root, so it stays on the floor while the body bobs, and it goes dark on the cut.
7. **OpenAI's hands are pressed together at rest** (both arms swing forward and in), and open out as today when it talks or cheers. Anthropic's raised finger and SpaceXAI's double thumbs-up are not built: T75's gestures can pose them.
8. **All three bodies get a cream belly** (openai.png has one too, though the task names it only for the other two).
9. **The eyes keep T46's light blue LED color on all three;** only their shape changes per bot: wide and round for OpenAI, half-closed for Anthropic, small round dots for SpaceXAI.
10. **Brows as today:** Anthropic keeps the worried brows, SpaceXAI the angled ones, OpenAI none. T75 adds brows for every bot while it emotes.
11. **The halo stays T46's ring of 12 glowing beads,** the warning light T46's dome, the bolt T46's three bars; only their stalk is shared, as today.
12. **The ear pods are cream and the collar is gold,** as the task says (the concepts draw some ear pods gold).
13. **The seat colors are unchanged** (`SetPersona`'s five linear colors), so the UI still matches.
14. **T46's hazard bands (`Stripe1`, `Stripe2`) and bolt decals (`Decal0` to `Decal2`) are deleted.** The new orange and lime bodies have neither, and no graph names them.
15. **`SetLit` loses its two `Glow` lines on `Body` and `Head`.** `M_Clay` has no `Glow` parameter (its scalars are `Rough`, `ThumbScale`, `ThumbDepth`), so those lines have done nothing since T46.
16. **The left hand keeps T46's slot** (the left arm pivot, minus 44 cm). The task asks for one hand socket, the right mitten.
17. **`HeadSocket` sits at the head's top, z 158 on the round head.** On the pill it stays at T46's 160, as the task says ("until then they use the old heights").
18. **Smoother clay:** `ThumbDepth` 0.2 on `MI_Clay_Seat` and `MI_Clay_Cream` (T46's finding was 0.35), because the concepts are smooth. This also smooths Meta's and my pill until T80. Tune on the close-up.
19. **`MI_Robot_Screen` is an `M_Robot` instance,** not `M_Clay`, because the lenses must match the visor, which is `M_Robot`. It lives in `Content/NHOS/Stage/Materials/` with the others. Name it in the commit.
20. **The design doc edit** is drafted in part 1 and waits for my person's OK in T79, as the task says.

## 0. Before you start

1. **T57 is pushed and `BP_Robot` is free.** `git pull`, read `Agents/`, then `git lfs locks`: no lock on `Content/NHOS/Stage/BP_Robot.uasset` or `Content/NHOS/Maps/L_Stage.umap`. Claim T79 and lock both (`L_Stage` for part 5). `git log --oneline -6 -- Graphs/BP_Robot Content/NHOS/Stage/BP_Robot.uasset` shows T57 (`069d4f6`) after T46.
2. **The six graphs this sheet changes are as quoted.** `git diff 069d4f6 -- Graphs/BP_Robot/{SetPersona,Receive,ResetLook,SetCut,SetLit,EventGraph}.txt` prints nothing. If a later task changed one of the six, put this sheet's lines into the pushed version by their text.
3. **My person's OK on part 1.** Ask with `AskUserQuestion` (the OK, or changes), make the doc edit after the OK, and go on with the build either way: nothing below depends on the doc's words.
4. **Survey `BP_Robot` and the materials** with one editor Python file, `Saved/T79/survey.py` (T46's `dump.py`, plus the lines below), run through the console box (T46: `SlateInspectorToolset.Type` of `py "<absolute path>"` into the `Cmd` textbox). Write the result to `Saved/T79/survey.json` and keep it for T80 and T75.
   - Every component: name, class, parent, relative location, rotation and scale, visibility, tags, mesh, materials, `get_collision_profile_name()`. **Expected (T46's `build.py` over its `parts.json`):** the parts and numbers in part 2a's "today" column. If a T46 part sits elsewhere, keep the new parts' numbers (they are placed for the new bodies, not against T46's).
   - The scalar and vector parameter values of `MI_Clay_Seat`, `MI_Clay_Cream`, `MI_Clay_Charcoal`, `MI_HaloGlow` (`MaterialEditingLibrary.get_material_instance_scalar_parameter_value`) and the parameter names of `M_Robot` (expected `Color` and `Glow`: `SetLit` and `ResetLook` set them).
   - The bounds of `/Engine/BasicShapes/Cone` (`get_bounds()`): this sheet takes it as 100 cm tall with a 50 cm base radius and its pivot in the middle (base at z −50). If its pivot is at the base, subtract 50 × its Z scale from both cones' z in part 2c.
   - The class defaults `Seat`, `FallDir`, `PreviewPersona`, and the construction script's one call (T75 part 0: it runs `SetPersona(PreviewPersona)`; confirm with `get_graph` on the construction script only).
5. **Node names** this sheet uses that no pushed `BP_Robot` source has: none. Every node below is in a pushed `Graphs/BP_Robot/` file (`Components|ComponentHasTag` and the component loop in `SetPersona.txt`, `Rendering|SetVisibility` there too, `Math|Interpolation|FInterpTo` in `EventGraph.txt`, `or` in T75's sheet and `BP_Show` sources).

## 1. The design doc edit (step 1): waiting for my person's OK

T79 shows this to my person, and after the OK makes it with the Claude Docs connector in the "Art Inspiration" tab (`0b64f21d-5f0e`, node `61d7c585-d94a`, rev 30 when this was written: read the tab again and match by text). It names no real person and copies nothing from the doc into the repo. The two pictures stay; T74 replaces them.

**Art direction, first paragraph (`.12357`):** change "Stop-motion clay pill bots perform film parodies" to "Stop-motion clay robots perform film parodies". The rest of the paragraph stays.

**"The bots" section, its bullets (`.13413`, `.13594`, `.13980`, `.14199`) become:**

- Four polished clay bots and one human in a homemade cardboard costume. That contrast is the premise in one picture: the player is the one pretending. Every bot is about 1.6 m tall, and its seat color is on its body, because a wig or a hood hides most of a head.
- OpenAI, Anthropic and SpaceXAI share one round head: a dark screen face with big LED eyes and a mouth that stretches wide, two small cream ear pods and a short gold collar. Meta has its own doll head, and the player a cardboard box.
- **OpenAI:** a smooth pale-blue teardrop that hovers over a glowing ring on the floor, in a gray knit sweater, hands pressed together, a halo above.
- **Anthropic:** a round orange body with a cream belly and a few buttons, small round feet, perfectly circular thin gold glasses over the screen, an amber light on a thin antenna.
- **SpaceXAI:** a round lime body with a cream belly on coiled spring arms and legs, chunky boots, a long straight nose under the visor, a toothy grin, a small lightning bolt.
- **Meta:** a doll-like android with a pale gold-white head, small ears and a short nose, glowing yellow-gold eyes behind thick black smart glasses with a tiny camera in each corner, a small stiff smile, jointed arms, a royal blue tee and pants, cream shoes and a chunky gold chain.
- **You:** a person in a homemade robot costume: a teal-painted cardboard box over the head with two eye slots and a smile drawn on, a ping-pong-ball antenna and the red and cream knitted scarf; a bigger teal box for the body with duct tape and bottle-cap buttons, striped sleeves, garden gloves, jeans and sneakers.
- (kept as it is, `.13761`) The energy is borrowed from chaotic sidekick crowds: ...
- Each provider bot carries a light parody nod to its company's leader through signature traits only (glasses, clothes, expression, pose), never a name or a likeness, and nothing carries a brand mark. No hair and no wires. Costumes go over the built-in parts: the shades hide Meta's and Anthropic's glasses, and OpenAI's halo, Anthropic's antenna light, SpaceXAI's bolt and the player's ping-pong ball poke up beside any hat.
- The audience in the boxes are small clay capsule bots in top hats.

**The color table:** its header "Top-half color" (`.14286`) becomes "Body color". The rows stay.

**The picture caption (`.20162`):** "The pill bots as built on 2026-11-15, before the new cast, in seat order, with their name tags hidden. The castle backdrop and props behind them are older pieces, not yet replaced." (Only if my person wants it: the task says to leave the pictures, and this changes only the words under one.)

The Costumes section stays: "The antenna topper pokes up through it" still holds (T47.md now says "beside it"; that is T47's to word).

## 2. `BP_Robot`'s components (steps 2 to 5)

All numbers are relative locations, rotations and scales in `Rig` space unless the parent column says otherwise, in cm. `Rig` +X is the robot's face (`InitHome` aims the actor's forward vector at the camera), Z is up, the floor is z 0. Engine shapes are 100 cm across (`Sphere`, `Cube`), 100 cm tall with a 50 cm radius (`Cylinder`, `Cone`), so scale 0.7 is 70 cm. Rotations are (roll, pitch, yaw) as T46's `build.py` writes them. "Seat", "Cream", "Charcoal" are T46's `MI_Clay_Seat`, `MI_Clay_Cream`, `MI_Clay_Charcoal`; "Gold", "Knit", "Steel" and "Screen" are part 2f's new instances; `M_Robot` is the robot material the face already uses.

**Tags.** `acc` plus persona ids: shown only on those personas (T46's rule in `SetPersona`). `seat`: colored with the seat color by `ResetLook` and grayed by `SetCut` (part 3). `ring`: hidden on the cut. `glasses`: hidden by T47 while the dark shades are on. "R3" below means the three tags `visionary`, `worrier`, `overclocker`; "P2" means `copycat`, `human`.

Every new static mesh component gets T46's parts' collision profile (from the survey; T49: set it with `set_collision_profile_name`, not `set_editor_property`) and casts shadows. New scene components (`Face`, the sockets) have scale 1.

### 2a. T46's parts: what stays, what changes

| Part | Today (T46) | T79 |
|---|---|---|
| `Body`, `Head`, `Seam` | the pill's seat-colored top half, cap and seam ring | tags `acc`, P2, `seat` (shown only on Meta and my robot until T80) |
| `BodyLow`, `CapLow` | the pill's cream bottom half and cap | tags `acc`, P2 |
| `ArmL`, `ArmR` (under the arm pivots) | charcoal noodle arms | tags `acc`, P2 |
| `FootL`, `FootR` | charcoal round feet at (6, ∓15, 7) | tags `acc`, P2 |
| `HandL`, `HandR` (under the arm pivots, at (0, ∓5, −44)) | seat-colored mittens, scale (0.17, 0.14, 0.19) | shared by all five: tag `seat`, no `acc` |
| `ArmPivotL`, `ArmPivotR` | at (0, ∓36, 92) | placed per body by `SetPersona` (part 3a) |
| `Visor` | sunk flattened sphere, `M_Robot`, at (17, 0, 110), scale (0.40, 0.56, 0.80) | shared; `SetPersona` sets its place and scale per head (part 3a). The template keeps the round head's: (14, 0, 130), scale (0.44, 0.54, 0.40) |
| `EyeL`, `EyeR`, `Mouth`, `Smile`, `BrowWL`, `BrowWR`, `BrowAL`, `BrowAR` | on `Rig` | **re-parented to `Face`** (2b), with the round head's numbers |
| `Nub` | the antenna stalk, (0, 0, 168), scale (0.04, 0.04, 0.24), charcoal; bent for the human | unchanged |
| `Halo0` to `Halo11`, `WarnDome`, `Bolt0` to `Bolt2` | the toppers on the stalk | unchanged |
| `Strap`, `Headset`, `HeadsetLens` (copycat), `ScarfA`, `ScarfB`, `ScarfTail`, `ScarfStripe`, `TealPanel` (human) | on the pill | unchanged (T80 replaces them) |
| `Stripe1`, `Stripe2`, `Decal0`, `Decal1`, `Decal2` | the worrier's hazard bands and the overclocker's bolt decals | **deleted** (Decision 14) |
| `Label` (root, z 228), `Spot` (root) | | unchanged |

### 2b. The face and the sockets (steps 2 and 3)

| Component | Class | Parent | Location | Rotation | Scale | Notes |
|---|---|---|---|---|---|---|
| `Face` | Scene | `Rig` | (0, 0, 0) | 0 | 1 | moved per head by `SetPersona` |
| `EyeL`, `EyeR` | (T46's) | `Face` | (33, ∓11, 135) | 0 | set per bot by `SetPersona` | T46's LED material |
| `Mouth` | (T46's) | `Face` | (34.5, 0, 123) | 0 | (0.02, 0.10, 0.02) at rest; Event Tick stretches it to 22 × 9 cm | T46's tags (`acc`, `visionary`, `worrier`, `overclocker`, `human`) |
| `Smile` | (T46's) | `Face` | (34.5, 0, 122) | 0 | (0.02, 0.2, 0.025) | copycat; lands on T46's (37, 0, 101) on the pill |
| `BrowWL`, `BrowWR` | (T46's) | `Face` | (27, ∓11, 145) | roll ∓20 (T46's) | (T46's) | worrier |
| `BrowAL`, `BrowAR` | (T46's) | `Face` | (27, ∓11, 144) | roll ±25 (T46's) | (T46's) | overclocker |
| `HeadSocket` | Scene | `Rig` | (0, 0, 158) | 0 | 1 | z 160 on the pill (`SetPersona`) |
| `BackSocket` | Scene | `Rig` | (−34, 0, 52) | 0 | 1 | per body (`SetPersona`) |
| `HandSocket` | Scene | `ArmPivotR` | (0, 5, −44) | 0 | 1 | the right mitten's center; the same on every body |

- **Where the screen shows.** The round head is an ellipsoid (radii 33, 35, 31 around z 127) and the `Visor` one with radii (22, 27, 20) around (14, 0, 130). Worked out from those two shapes, the screen shows on the face from about z 118 to 147 at the middle and y ±24 at eye height, the eyes' centers at (33, ±11, 135) sit 0.3 cm inside its surface (their 5 cm-deep half pokes out, as on T46), the mouth's front is 0.9 cm proud of it, and the brows at z 144 to 145 are just under its top edge. If the close-up shows the brows on the shell, lower them 1 to 2 cm.
- **The pill's face** (`Face` at (2.5, 0, −21)): eyes at (35.5, ±11, 114) against T46's (34, ±11, 114), mouth at (37, 0, 102) against (37, 0, 101), `Smile` at (37, 0, 101). The brows land inside the pill's screen, but neither pill bot shows brows.
- **Re-parenting** in editor Python: `sub.attach_subobject(face_handle, part_handle)` for each face part (`SubobjectDataSubsystem`; if that name isn't there, `sub.reparent_subobject(unreal.ReparentSubobjectParams(new_parent_handle=face_handle, blueprint_context=bp), part_handle)`). Set each part's relative transform after the move. **If neither works,** leave the face parts on `Rig` with the round head's numbers and add their pill places to `SetPersona` instead of the one `Face` line: eight `SetRelativeLocation` lines, each `(select _r <round> <round + (2.5, 0, −21)>)`. Say so under "Findings": T75's `FaceParts` survey then finds the parts on `Rig`.
- **The sockets' world scale must be 1:** `BP_Prop.TickFly` places a prop at the socket's world transform applied to its grip offset, so a scaled socket would scale the grip.

### 2c. The shared round head (step 2), tags `acc`, R3

| Component | Mesh | Location | Rotation | Scale | Material | Extra tags |
|---|---|---|---|---|---|---|
| `RHead` | Sphere | (0, 0, 127) | 0 | (0.66, 0.70, 0.62) | Seat | `seat` |
| `Collar` | Cylinder | (0, 0, 93) | 0 | (0.26, 0.26, 0.10) | Gold | |
| `EarL`, `EarR` | Cylinder | (0, ∓34, 128) | roll 90 | (0.20, 0.20, 0.08) | Cream | |

The head runs from z 96 to 158 and is 70 cm across the ears' line; the ear pods (20 cm across, 8 deep) stand out to y ±38. The collar runs from z 88 to 98, under the head's bottom and into each body's top.

### 2d. OpenAI (`visionary`), tags `acc`, `visionary`

| Component | Parent | Mesh | Location | Rotation | Scale | Material | Extra tags |
|---|---|---|---|---|---|---|---|
| `OBody` | `Rig` | Sphere | (0, 0, 52) | 0 | (0.60, 0.60, 0.60) | Seat | `seat` |
| `OTop` | `Rig` | Cone | (0, 0, 83) | 0 | (0.56, 0.56, 0.40) | Seat | `seat` |
| `OBelly` | `Rig` | Sphere | (27.5, 0, 50) | 0 | (0.08, 0.36, 0.40) | Cream | |
| `Sweater` | `Rig` | Cone | (0, 0, 84) | 0 | (0.62, 0.62, 0.42) | Knit | |
| `Turtle` | `Rig` | Cylinder | (0, 0, 93) | 0 | (0.32, 0.32, 0.12) | Knit | |
| `SleeveL`, `SleeveR` | `ArmPivotL`, `ArmPivotR` | Cylinder | (0, ∓3, −18) | 0 | (0.12, 0.12, 0.36) | Knit | |
| `OLegL`, `OLegR` | `Rig` | Cylinder | (0, ∓12, 17) | 0 | (0.12, 0.12, 0.14) | Seat | `seat` |
| `OCuffL`, `OCuffR` | `Rig` | Cylinder | (0, ∓12, 15) | 0 | (0.15, 0.15, 0.06) | Knit | |
| `OFootL`, `OFootR` | `Rig` | Sphere | (5, ∓12, 6) | 0 | (0.22, 0.16, 0.12) | Seat | `seat` |
| `Ring0` to `Ring11` | **root** (`DefaultSceneRoot`) | Cube | (42 cos a, 42 sin a, 0.6), a = 30° × i | yaw a + 90 | (0.22, 0.025, 0.01) | `MI_HaloGlow` | `ring` |

- The teardrop: a 60 cm ball (z 22 to 82) with a cone on top whose 28 cm base meets the ball where the ball is 28 cm round (z 63) and whose tip hides in the collar. The sweater is a slightly bigger cone over the same place, so its hem stands 3 cm off the body at z 63 and the cream belly shows below it. The turtleneck (z 87 to 99, 32 cm across) covers the gold collar.
- The legs and feet stand from z 0 to 24 in the template; the hover (`HoverZ` 8, part 3) lifts the whole `Rig`, so in play the feet float 8 cm over the ring, plus the slow bob.
- The ring is 12 tangent glowing bars, 84 cm across, on the floor around the robot (each bar 22 cm long, about one twelfth of the circle). On the root, it doesn't bob; it hops with the actor.
- The arm pivots go to (0, ∓19, 80), the sweater's shoulders. The sleeves end at −36 and the seat-colored mittens (−44) poke out of them.

### 2e. Anthropic (`worrier`) and SpaceXAI (`overclocker`)

**Anthropic,** tags `acc`, `worrier`:

| Component | Parent | Mesh | Location | Rotation | Scale | Material | Extra tags |
|---|---|---|---|---|---|---|---|
| `ABody` | `Rig` | Sphere | (0, 0, 52) | 0 | (0.66, 0.68, 0.76) | Seat | `seat` |
| `ABelly` | `Rig` | Sphere | (29.5, 0, 45) | 0 | (0.10, 0.44, 0.48) | Cream | |
| `ABtn0` | `Rig` | Sphere | (25.5, 0, 77) | 0 | (0.045, 0.045, 0.045) | Charcoal | |
| `ABtn1`, `ABtn2` | `Rig` | Sphere | (25, ∓13, 73) | 0 | (0.045, 0.045, 0.045) | Charcoal | |
| `AShoulderL`, `AShoulderR` | arm pivots | Sphere | (0, 0, 0) | 0 | (0.14, 0.14, 0.14) | Charcoal | |
| `AArmL`, `AArmR` | arm pivots | Cylinder | (0, ∓3, −20) | 0 | (0.10, 0.10, 0.40) | Seat | `seat` |
| `AElbowL`, `AElbowR` | arm pivots | Cylinder | (0, ∓3, −20) | 0 | (0.11, 0.11, 0.035) | Charcoal | |
| `AWristL`, `AWristR` | arm pivots | Cylinder | (0, ∓4, −37) | 0 | (0.12, 0.12, 0.03) | Gold | |
| `AFootL`, `AFootR` | `Rig` | Sphere | (6, ∓15, 7) | 0 | (0.26, 0.20, 0.14) | Seat | `seat` |
| `RimL`, `RimR` | `Face` | Cylinder | (34.6, ∓11, 135) | pitch 90 | (0.19, 0.19, 0.012) | Gold | `glasses` |
| `LensL`, `LensR` | `Face` | Cylinder | (35.5, ∓11, 135) | pitch 90 | (0.17, 0.17, 0.006) | Screen | `glasses` |
| `Bridge` | `Face` | Cube | (35, 0, 137) | 0 | (0.01, 0.03, 0.012) | Gold | `glasses` |
| `TempleL`, `TempleR` | `Face` | Cube | (21, ∓28, 136) | yaw ±23 | (0.30, 0.008, 0.012) | Gold | `glasses` |

- The body: an egg 66 deep, 68 wide, 76 tall (z 14 to 90); the belly bulges 2 cm out of its front from z 21 to 69; the buttons sit on its surface above the belly. The arm pivots go to (0, ∓29, 76), the shoulders, with a charcoal ball joint, a seat-colored arm with a charcoal elbow band and a gold wrist band.
- **The glasses (Decision 4):** each rim is a gold disc 19 cm across, 1.2 cm thick, facing forward, centered on its eye; in front of it, a dark lens disc 17 cm across in the visor's color. Seen from the front, only a 1 cm gold ring shows around each lens, and the eye (front at x 38) pokes 2 cm through the lens. A thin bridge joins them and two temples run back to the ear pods. They are on `Face`, so they move with the eyes' head. Check the rim isn't seen edge-on as a gold coin from the house camera's angle (about 10° down); if it is, make the rims thinner (Z scale 0.008).

**SpaceXAI,** tags `acc`, `overclocker`:

| Component | Parent | Mesh | Location | Rotation | Scale | Material | Extra tags |
|---|---|---|---|---|---|---|---|
| `SBody` | `Rig` | Sphere | (0, 0, 62) | 0 | (0.64, 0.66, 0.64) | Seat | `seat` |
| `SBelly` | `Rig` | Sphere | (28.5, 0, 56) | 0 | (0.10, 0.40, 0.44) | Cream | |
| `SLegL`, `SLegR` | `Rig` | Cylinder | (0, ∓14, 25) | 0 | (0.03, 0.03, 0.14) | Steel | |
| `SLegCoil0L` to `SLegCoil2L`, and `…R` | `Rig` | Cylinder | (0, ∓14, 21 / 25 / 29) | 0 | (0.11, 0.11, 0.015) | Steel | |
| `SBootL`, `SBootR` | `Rig` | Cylinder | (2, ∓14, 9) | 0 | (0.20, 0.20, 0.18) | Seat | `seat` |
| `SToeL`, `SToeR` | `Rig` | Sphere | (10, ∓14, 6) | 0 | (0.28, 0.20, 0.12) | Seat | `seat` |
| `SArmL`, `SArmR` | arm pivots | Cylinder | (0, ∓2, −13) | 0 | (0.03, 0.03, 0.26) | Steel | |
| `SArmCoil0L` to `SArmCoil3L`, and `…R` | arm pivots | Cylinder | (0, ∓2, −4 / −10 / −16 / −22) | 0 | (0.10, 0.10, 0.015) | Steel | |
| `SForeL`, `SForeR` | arm pivots | Cylinder | (0, ∓4, −32) | 0 | (0.11, 0.11, 0.14) | Seat | `seat` |
| `SNose` | `Face` | Cylinder | (39, 0, 128) | pitch 20 | (0.06, 0.06, 0.24) | Seat | `seat` |
| `SNoseTip` | `Face` | Sphere | (43, 0, 117) | 0 | (0.075, 0.075, 0.075) | Seat | `seat` |
| `Teeth` | `Face` | Cube | (35.5, 0, 121) | 0 | (0.02, 0.20, 0.045) | Cream | |
| `TGap0` to `TGap2` | `Face` | Cube | (36.6, −5 / 0 / 5, 121) | 0 | (0.003, 0.006, 0.045) | Charcoal | |

- The body: a ball 64 by 66 by 64 (z 30 to 94) with its belly; boots from the floor to z 18, their toes forward; a spring of three steel coils on a thin core from z 18 to 32 into the body's bottom. The arm pivots go to (0, ∓30, 74): four coils on a core from the shoulder down 26 cm, then a lime forearm and the mitten.
- **The nose:** a 24 cm lime rod, 6 cm thick, from the screen between the eyes (about (35, 0, 139)) down and forward to a round tip at (43, 0, 117), over the middle of the grin. Positive pitch swings a part's bottom end forward (the same rule as the arms in part 3); if the nose points back into the head, use pitch −20.
- **The grin (Decision 3):** a cream bar 20 by 4.5 cm with three thin charcoal gaps, 1 cm in front of the LED mouth. The mouth (z 123) peeks over it when it stretches.
- **The springs (Decision 5):** if the close-up reads them as a ribbed pipe, make one spring with `Tools/art_gen.py`: a Leonardo reference image of "a single steel coil spring, clay style, plain background" (`image`, free), then `mesh-image ... --model meshy-6-lite --no-texture` (5 credits), import it to `Content/NHOS/Stage/Cast/SM_Spring` with `MI_Clay_Steel`, record it in `Docs/Assets.md`, and swap each limb's core and coils for one component with that mesh. Not done by default; if done, it's in T79's Touches.

### 2f. Materials (step 5)

| Instance | Parent | `Color` (linear) | `ThumbScale` | `ThumbDepth` | Used on |
|---|---|---|---|---|---|
| `MI_Clay_Gold` (new) | `M_Clay` | (0.60, 0.36, 0.06) | 0.12 | 0.2 | collar, glasses, wrist bands; T80's chain |
| `MI_Clay_Knit` (new) | `M_Clay` | (0.28, 0.25, 0.22) | 0.5 | 0.5 | OpenAI's sweater, turtleneck, sleeves, cuffs. T46 found these two values "looked like terry cloth" on a body; on a sweater that is the point |
| `MI_Clay_Steel` (new) | `M_Clay` | (0.30, 0.30, 0.32) | 0.12 | 0.15 | SpaceXAI's springs |
| `MI_Robot_Screen` (new) | `M_Robot` | (0.012, 0.012, 0.018), `Glow` 0 | | | Anthropic's lenses: the color `ResetLook` gives the visor |
| `MI_Clay_Seat`, `MI_Clay_Cream` | (T46's) | unchanged | unchanged | **0.2** (Decision 18) | |

`MI_Clay_Seat` is colored per robot at run time (`ResetLook`'s loop makes a dynamic instance per part, T11). Make the new ones with T46's `mi()` helper from `Saved/T46/build.py` (a `MaterialInstanceConstantFactoryNew` asset, `set_material_instance_parent`, the parameters, `update_material_instance`, save). For `MI_Robot_Screen`, the same with `M_Robot` as parent and its own parameter names from the survey.

### 2g. The build script

One editor Python file, `Saved/T79/build.py`, in T46's form (its `gather()`, `setc()`, `add_new_subobject` + `rename_subobject`, `delete_subobject`, then `BlueprintEditorLibrary.compile_blueprint` and `EditorAssetLibrary.save_asset`). Keep the parts as data, one row per component, so a tune is a number:

```python
# name, class ('sm' or 'scene'), parent, mesh ('Sphere', 'Cube', 'Cylinder', 'Cone' or None), loc, rot (roll, pitch, yaw), scale, material, tags
PARTS = [
    ("Face", "scene", "Rig", None, (0, 0, 0), (0, 0, 0), (1, 1, 1), None, []),
    ("HeadSocket", "scene", "Rig", None, (0, 0, 158), (0, 0, 0), (1, 1, 1), None, []),
    ("BackSocket", "scene", "Rig", None, (-34, 0, 52), (0, 0, 0), (1, 1, 1), None, []),
    ("HandSocket", "scene", "ArmPivotR", None, (0, 5, -44), (0, 0, 0), (1, 1, 1), None, []),
    ("RHead", "sm", "Rig", "Sphere", (0, 0, 127), (0, 0, 0), (0.66, 0.70, 0.62), SEAT, ["acc", *R3, "seat"]),
    # ... every row of parts 2c to 2e, in that order
]
RETAG = {  # T46 parts: their new tags (2a)
    "Body": ["acc", *P2, "seat"], "Head": ["acc", *P2, "seat"], "Seam": ["acc", *P2, "seat"],
    "BodyLow": ["acc", *P2], "CapLow": ["acc", *P2], "ArmL": ["acc", *P2], "ArmR": ["acc", *P2],
    "FootL": ["acc", *P2], "FootR": ["acc", *P2], "HandL": ["seat"], "HandR": ["seat"],
}
DELETE = ["Stripe1", "Stripe2", "Decal0", "Decal1", "Decal2"]
FACE = ["EyeL", "EyeR", "Mouth", "Smile", "BrowWL", "BrowWR", "BrowAL", "BrowAR"]  # re-parent to Face (2b)
```

Order: materials (2f), delete, add the scene components, add the meshes (each under its parent's handle; `Face` must exist before the glasses, nose and teeth), re-parent `FACE`, then set every transform, mesh, material, tags, collision and `visible` (true for untagged parts; the `acc` rule sets the rest at run time and in the construction script). Log each step to `Saved/T79/build_log.json` as T46 did. Then a second dump (`Saved/T79/parts_after.json`) to compare with the tables. **About 95 components are added;** if one script call nears the 120 s MCP limit, split it: materials, then the head and OpenAI, then Anthropic and SpaceXAI.

## 3. The graphs (steps 3, 4 and 6)

New variables in `BP_Robot` (Float, default 0): `HoverZ`, `FoldPitch`, `FoldRoll`, `Fold`. The new components are variables already (T46: component variables work in the DSL once they exist).

Write each graph with `write_graph_dsl` and save its file in `Graphs/BP_Robot/` as written. Each file below is the pushed source with T79's lines; the lines marked `; T79` are new or changed.

### 3a. `SetPersona` (the bodies, the face, the arms, the sockets)

```lisp
(fn SetPersona (Id)
  (Variables|Default|SetPersonaId Id)
  (Variables|Default|SetPhase (* (Math|Random|RandomFloat) 6.28))
  (bind _tag (Utilities|String|StringToName Id))
  (for _c (Actor|GetComponentsByClass :ComponentClass "/Script/Engine.StaticMeshComponent")
    (if (Components|ComponentHasTag :self _c :Tag "acc")
      (Rendering|SetVisibility :self _c :bNewVisibility (Components|ComponentHasTag :self _c :Tag _tag) :bPropagateToChildren false)))
  (bind _v (Utilities|String|EqualExactly(String) Id "visionary"))
  (bind _w (Utilities|String|EqualExactly(String) Id "worrier"))
  (bind _o (Utilities|String|EqualExactly(String) Id "overclocker"))
  (bind _p (Utilities|String|EqualExactly(String) Id "copycat"))
  (bind _h (Utilities|String|EqualExactly(String) Id "human"))
  ; T79: OpenAI, Anthropic and SpaceXAI wear the shared round head; Meta and my robot keep T46's pill until T80.
  (bind _r (or _v (or _w _o)))
  (Variables|Default|SetBaseColor (select _v (Utilities|Struct|MakeLinearColor :R 0.392 :G 0.604 :B 1.0 :A 1.0) (select _w (Utilities|Struct|MakeLinearColor :R 0.807 :G 0.25 :B 0.068 :A 1.0) (select _o (Utilities|Struct|MakeLinearColor :R 0.687 :G 0.871 :B 0.068 :A 1.0) (select _p (Utilities|Struct|MakeLinearColor :R 0.105 :G 0.262 :B 1.0 :A 1.0) (select _h (Utilities|Struct|MakeLinearColor :R 0.05 :G 0.631 :B 0.584 :A 1.0) (Variables|Default|GetBaseColor)))))))
  ; T79: OpenAI's idle bob becomes a slow hover, 8 cm up, with its hands pressed together at rest.
  (Variables|Default|SetBobSpeed (select _v 1.1 (select _w 6.0 (select _o 4.5 (select _p 0.7 2.0)))))
  (Variables|Default|SetBobAmp (select _v 3.5 (select _w 1.0 (select _o 4.0 (select _p 0.6 2.5)))))
  (Variables|Default|SetHoverZ (select _v 8.0 0.0))
  (Variables|Default|SetFoldPitch (select _v 60.0 0.0))
  (Variables|Default|SetFoldRoll (select _v 33.0 0.0))
  ; T79: eyes: wide and round (OpenAI), half-closed (Anthropic), small dots (SpaceXAI); T46's for the pill.
  (bind _es (select _v (Math|Vector|MakeVector :X 0.1 :Y 0.12 :Z 0.12) (select _w (Math|Vector|MakeVector :X 0.1 :Y 0.11 :Z 0.07) (select _o (Math|Vector|MakeVector :X 0.1 :Y 0.09 :Z 0.09) (select _h (Math|Vector|MakeVector :X 0.14 :Y 0.14 :Z 0.18) (Math|Vector|MakeVector :X 0.1 :Y 0.1 :Z 0.13))))))
  (Transformation|SetRelativeScale3D :self (Variables|Default|GetEyeL) :NewScale3D _es)
  (Transformation|SetRelativeScale3D :self (Variables|Default|GetEyeR) :NewScale3D _es)
  (Transformation|SetRelativeRotation :self (Variables|Default|GetNub) :NewRotation (Math|Rotator|MakeRotator :Roll (select _h 32.0 0.0) :Pitch 0.0 :Yaw 0.0))
  ; T79: the face and the screen on the round head, or where T46 had them on the pill.
  (Transformation|SetRelativeLocation :self (Variables|Default|GetFace) :NewLocation (select _r (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 0.0) (Math|Vector|MakeVector :X 2.5 :Y 0.0 :Z -21.0)))
  (Transformation|SetRelativeLocation :self (Variables|Default|GetVisor) :NewLocation (select _r (Math|Vector|MakeVector :X 14.0 :Y 0.0 :Z 130.0) (Math|Vector|MakeVector :X 17.0 :Y 0.0 :Z 110.0)))
  (Transformation|SetRelativeScale3D :self (Variables|Default|GetVisor) :NewScale3D (select _r (Math|Vector|MakeVector :X 0.44 :Y 0.54 :Z 0.4) (Math|Vector|MakeVector :X 0.4 :Y 0.56 :Z 0.8)))
  ; T79: the shoulders of each body.
  (bind _sy (select _v 19.0 (select _w 29.0 (select _o 30.0 36.0))))
  (bind _sz (select _v 80.0 (select _w 76.0 (select _o 74.0 92.0))))
  (Transformation|SetRelativeLocation :self (Variables|Default|GetArmPivotL) :NewLocation (Math|Vector|MakeVector :X 0.0 :Y (- _sy) :Z _sz))
  (Transformation|SetRelativeLocation :self (Variables|Default|GetArmPivotR) :NewLocation (Math|Vector|MakeVector :X 0.0 :Y _sy :Z _sz))
  ; T79: the head and back sockets of each body (HandSocket rides on the right arm pivot). T80 sets Meta's and mine.
  (Transformation|SetRelativeLocation :self (Variables|Default|GetHeadSocket) :NewLocation (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z (select _r 158.0 160.0)))
  (Transformation|SetRelativeLocation :self (Variables|Default|GetBackSocket) :NewLocation (select _v (Math|Vector|MakeVector :X -30.0 :Y 0.0 :Z 60.0) (select _w (Math|Vector|MakeVector :X -34.0 :Y 0.0 :Z 52.0) (select _o (Math|Vector|MakeVector :X -33.0 :Y 0.0 :Z 62.0) (Math|Vector|MakeVector :X -38.0 :Y 0.0 :Z 106.0)))))
  (CallFunction|ResetLook))
```

- The `acc` loop now also shows each body and hides the others, because every body part is tagged by persona (part 2).
- `select` on vectors and `(- _sy)` are already used in pushed sources (`SetPersona`, `EventGraph`).
- The construction script calls `SetPersona(PreviewPersona)`, so each placed robot shows its body in the editor.

### 3b. `Receive` (props on the sockets)

```lisp
(fn Receive (Prop Dur H)
  (bind _mine (Class|BPProp|SlotFor :self Prop :A self))
  (if (>= _mine 0)
    (return))
  (bind _w (Class|BPProp|GetWear :self Prop))
  ; T79: head and back props go to the robot's sockets, not to fixed heights on the Rig.
  (if (streq _w "head")
    (Class|BPProp|FlyToComp :self Prop :Comp (V HeadSocket) :Off (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 0.0) :NewHolder self :NewSlot 2 :Dur Dur :Height H)
    (return))
  (if (streq _w "back")
    (Class|BPProp|FlyToComp :self Prop :Comp (V BackSocket) :Off (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 0.0) :NewHolder self :NewSlot 3 :Dur Dur :Height H)
    (return))
  (set HeldR false)
  (set HeldL false)
  (bind _all (Actor|GetAllActorsOfClass :ActorClass "/Game/NHOS/Stage/BP_Prop.BP_Prop_C"))
  (for _p _all
    (bind _s (Class|BPProp|SlotFor :self _p :A self))
    (if (== _s 0)
      (set HeldR true)
      (set OldR _p))
    (if (== _s 1)
      (set HeldL true)))
  ; T79: the right hand is HandSocket; the left keeps T46's slot on its arm pivot.
  (if (not (V HeldR))
    (Class|BPProp|FlyToComp :self Prop :Comp (V HandSocket) :Off (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 0.0) :NewHolder self :NewSlot 0 :Dur Dur :Height H)
    (return))
  (if (not (V HeldL))
    (Class|BPProp|FlyToComp :self Prop :Comp (V ArmPivotL) :Off (Math|Vector|MakeVector :X 0.0 :Y -5.0 :Z -44.0) :NewHolder self :NewSlot 1 :Dur Dur :Height H)
    (return))
  (bind _feet (CallFunction|FeetSpot))
  (Class|BPProp|ThrowTo :self (V OldR) :Loc _feet :Dur 0.45 :Height 35.0 :Spin 0.0)
  (Class|BPProp|FlyToComp :self Prop :Comp (V HandSocket) :Off (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 0.0) :NewHolder self :NewSlot 0 :Dur Dur :Height H))
```

`FlyToComp` adds the prop's own `GripLoc` (T45) to the offset and attaches the prop to the component when it lands (`TickFly`), so a held prop follows the socket through every bob, hop, flap and slump. A right-hand prop lands where it did on T46 (the socket is the old offset); only the head and back props move, to each body's head top and back.

### 3c. `ResetLook`, `SetCut`, `SetLit` (one loop for the seat color)

**`ResetLook`:** replace the five lines that set `Color` on `Body`, `Head`, `HandL`, `HandR` and `Seam` with:

```lisp
  ; T79: every part tagged "seat" wears the seat color; OpenAI's floor ring is lit again.
  (for _c (Actor|GetComponentsByClass :ComponentClass "/Script/Engine.StaticMeshComponent")
    (if (Components|ComponentHasTag :self _c :Tag "seat")
      (Rendering|Material|SetVectorParameterValueonMaterials :self _c :ParameterName "Color" :ParameterValue _cv))
    (if (Components|ComponentHasTag :self _c :Tag "ring")
      (Rendering|SetVisibility :self _c :bNewVisibility (Utilities|String|EqualExactly(String) (Variables|Default|GetPersonaId) "visionary") :bPropagateToChildren false)))
```

Keep everything else in `ResetLook` as it is (the `_cv` bind before it, the visor, eyes, mouth and brows, the label, `SetLit`, `FaceCamera`). Add `(Variables|Default|SetFold 0.0)` after `(Variables|Default|SetCheerUntil 0.0)`, so a restarted OpenAI starts with its arms down and eases them together.

**`SetCut`:** replace the five lines that set `_gray` on `Body`, `Head`, `HandL`, `HandR` and `Seam` with:

```lisp
  ; T79: every seat-colored part goes gray; OpenAI's floor ring goes out.
  (for _c (Actor|GetComponentsByClass :ComponentClass "/Script/Engine.StaticMeshComponent")
    (if (Components|ComponentHasTag :self _c :Tag "seat")
      (Rendering|Material|SetVectorParameterValueonMaterials :self _c :ParameterName "Color" :ParameterValue _gray))
    (if (Components|ComponentHasTag :self _c :Tag "ring")
      (Rendering|SetVisibility :self _c :bNewVisibility false :bPropagateToChildren false)))
```

The `_gray` and `_dark` binds stay before it; the eyes, mouth and brows still go dark as before. The cream belly, the knit, the gold and the steel keep their colors on the cut, as T46's cream half did.

**`SetLit`:** delete its two lines on `Body` and `Head` (`"Glow"` 0.15 or 0; Decision 15). The rest stays.

If T38 has landed first, keep its `(CallFunction|HideBubble)` line in `SetCut` and `ResetLook`. T57 changed neither.

### 3d. `EventGraph` (the hover and the folded hands)

Only Event Tick changes; Event BeginPlay stays. Three places, by their text:

1. **The cut branch's `Rig` location:** the hover sinks to the floor with the slump.
   ```lisp
       (Transformation|SetRelativeLocation :self (Variables|Default|GetRig) :NewLocation (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z (+ (* (- 1.0 _k) (Variables|Default|GetHoverZ)) (* _k -10.0))))   ; T79
   ```
2. **The standing branch's `_z`:** add the hover.
   ```lisp
         (bind _z (+ (Variables|Default|GetHoverZ) (+ (* _st (Variables|Default|GetBobAmp)) (+ (select _talk (* (Math|Float|Absolute(Float) _w13) 9.0) 0.0) (select _cheer (* (Math|Float|Absolute(Float) (Math|Trig|Sin(Radians) (* _c 9.0))) 26.0) 0.0)))))   ; T79
   ```
3. **The arms:** after `(bind _arm ...)`, replace the two `ArmPivot` rotation lines with:
   ```lisp
         ; T79: OpenAI presses its hands together at rest; talking or cheering opens them as before.
         (Variables|Default|SetFold (Math|Interpolation|FInterpTo (Variables|Default|GetFold) (select (or _talk _cheer) 0.0 1.0) DeltaSeconds 6.0))
         (bind _fp (* (Variables|Default|GetFoldPitch) (Variables|Default|GetFold)))
         (bind _fr (* (Variables|Default|GetFoldRoll) (Variables|Default|GetFold)))
         (Transformation|SetRelativeRotation :self (Variables|Default|GetArmPivotL) :NewRotation (Math|Rotator|MakeRotator :Roll (+ (- _arm) _fr) :Pitch _fp :Yaw 0.0))
         (Transformation|SetRelativeRotation :self (Variables|Default|GetArmPivotR) :NewRotation (Math|Rotator|MakeRotator :Roll (- _arm _fr) :Pitch _fp :Yaw 0.0))
   ```

- **The fold's numbers** (pitch 60, roll 33) bring two 44 cm arms from shoulders 38 cm apart to mittens touching about 38 cm in front of the body at z 58. They are worked out, not seen: tune on the close-up. Positive pitch swings a hanging arm forward (UE's pitch turns +X toward +Z, so −Z turns toward +X); positive roll on the right arm swings it out, as the cheer's 150 shows, so the right arm's inward roll is negative and the left's positive. If the arms swing back, negate `FoldPitch`.
- `FoldPitch` and `FoldRoll` are 0 for the other four, so their arms move exactly as today.
- The mouth line and the worrier's warning-light pulse stay as they are. The mouth is on `Face` now; its scale numbers don't change.

## 4. Every motion, kept (step 6)

From the pushed graphs, every motion the robot has today, and why it still works:

| Motion | Where (graph) | How the new bodies keep it |
|---|---|---|
| Idle bob | `EventGraph`: `Rig` z = sin(clock × `BobSpeed` + `Phase`) × `BobAmp` | every new part is under `Rig` or an arm pivot; OpenAI adds `HoverZ` 8 and a slower, larger bob (3a) |
| Talking bounce | `EventGraph`: `|sin 13t|` × 9 cm on `Rig` while `TalkUntil` (set by `SetLit`) | the same |
| Talking arm flap | `EventGraph`: arm roll 30 + 22 sin 13t | the same; OpenAI's fold eases out while it talks (3d) |
| Mouth stretch | `EventGraph`: `Mouth` scale up to 22 × 9 cm while talking | `Mouth` is on `Face`, scale 1 at the origin, so the numbers mean the same; on SpaceXAI it stretches past the teeth |
| Cheer | `Cheer` sets `CheerUntil`; `EventGraph`: hop 26 cm and arms up to 150° | the same; the fold opens |
| Shake | `Shake` sets `ShakeUntil` (from a throw that hits, `TickActs` `HitAt`); `EventGraph`: `Rig` yaw ± 14° | the same |
| Cut slump | `SetCut`; `EventGraph`: `Rig` down 10 cm and pitched −14°, then tipped to 82° × `FallDir`, arms to 0 | the same; OpenAI's hover sinks with the slump (3d), its ring goes out, every `seat` part goes gray (3c), the eyes, mouth and brows go dark, the label shows the stamp |
| Moves and hops | `StartMove` (hop 20, 32 or 75 cm), `TickActs` (eased arc on the actor) | on the actor, so the whole robot and the ring move |
| Turning, look, look around | `TickActs` (yaw toward `FaceYaw`, the camera or a 65° sweep), `StartAct` | on the actor |
| Grab | `DoGrab` → `Receive` (the prop flies to `HandSocket`) | 3b |
| Throw | `DoHanded`: `ThrowTo` from the hand, `LandSnd`, `HitBot` shakes | the prop leaves the socket as before |
| Give | `DoHanded` → the other robot's `Receive` | it lands on that robot's `HandSocket` |
| Put down, drop all, back to the table | `DoHanded` (`ThrowTo`), `DropAll` on the cut, `ToTable` at home | unchanged |
| Lit while speaking | `SetLit`: spotlight on, eyes, mouth and brows glow 10 | unchanged (only the no-op `Glow` on the clay is gone) |
| Warning light pulse | `EventGraph`: `WarnDome` `Glow` 7 ± 6 | unchanged |
| Footsteps and robot sounds | `StartMove`, `StepSnd`, `Snd`, `LandSnd` | unchanged |

## 5. Re-place the robots in `L_Stage` (step 7)

**They must be re-placed.** T17 and T46 found that template edits don't reach robots placed before them, and T79 adds about 95 components and moves others. `L_Stage` is not World Partition, so the lock on `L_Stage.umap` (part 0) covers it.

1. Dump the five robots first, with T46's `Saved/T46/robots.py` copied to `Saved/T79/robots.py` (paths changed): label, folder, location, rotation, `Seat`, `FallDir`, `PreviewPersona`. Expected (T46's `robots.json`): `Robot0` (−50, −330) yaw 161.7, seat 0, fall −1, `visionary`; `Robot1` (−12, −165) yaw 171.0, seat 1, fall −1, `worrier`; `Robot2` (0, 0) yaw 180, seat 2, fall 1, `human`; `Robot3` (−12, 165) yaw −171.0, seat 3, fall 1, `overclocker`; `Robot4` (−50, 330) yaw −161.7, seat 4, fall 1, `copycat`; all z 0, folder `Stage`.
2. Re-place them with T46's `replace.py` (destroy, `spawn_actor_from_class`, then label, folder, `Seat`, `FallDir`, `PreviewPersona`) reading `Saved/T79/robots.json`. Touch nothing else in the level (T45's four props, T49's set).
3. Save `L_Stage`, and check in the editor's viewport that each robot shows its preview body (the construction script).

If a later task left a new instance property on the robots (T57 added none), add it to both scripts' lists before the replace.

## 6. The check (step 8)

Switches as for T46's runs (`Local/switches.json`: `"autoplay": true`, `"mode": "free"`, `"spare_human": true`, `"fast_lines": true`, `"ai_seats": 0`), so a show plays all its scenes in free mode. Save the shots to `Saved/T79/shots/` (not in git).

1. **Compile:** `BP_Robot` compiles with no error, and `parts_after.json` matches part 2's tables.
2. **PIE screenshots from the house camera** (T46's way: PIE in a 1600 × 900 floating window, autoplay, `SlateInspectorToolset.Screenshot` every 4 s): one in Scene Prep and one in a scene turn. They must show all five robots, the three new bodies in their seat colors next to Meta's and my pill, the labels above the toppers, OpenAI floating over its ring, and no part sticking out of another.
3. **A close-up of each new bot beside its concept image.** In the editor (not PIE), aim the viewport at each robot from 260 cm in front of it and 100 cm up, facing it, pitched −5° (`UnrealEditorSubsystem.set_level_viewport_camera_info`), and capture it (`CaptureViewport`, with the `annotations` object T46 needed; save the base64 with `AssetTools.write_file` in the same script). Read each capture and its `Docs/BotArt/<seat>.png` together. Each must show: the oval head with the dark screen, eyes and mouth on the screen, the ear pods and gold collar; OpenAI's teardrop, sweater, folded hands (in PIE, or by setting `Fold` to 1 on the instance), feet and ring; Anthropic's round body, belly, buttons, feet and the glasses as two gold rings with the eyes inside; SpaceXAI's round body, belly, springs that read as springs (Decision 5), boots, the nose over the grin and the teeth.
4. **Each of the three holding a prop.** The free autoplay show's grabs give most of them. If one is missing, in PIE run a one-off editor Python file that finds the PIE world's robots and props (`unreal.EditorLevelLibrary.get_game_world()`, `unreal.GameplayStatics.get_all_actors_of_class`) and calls `bot.call_method("Receive", (prop, 0.5, 60.0))` on it, then screenshot it. The prop must sit in the right mitten, through the socket, and move with the arm.
5. **A cut robot:** one PIE frame after a cut shows the cut bot gray (every `seat` part), tipped over at the side of the stage, OpenAI's ring out if it is the cut one.
6. **A free autoplay show in a game window** reaches `NHOS: SHOW END` with no `LogScript` line (T27's Mac command, T46 part 6):
   ```bash
   "/Users/Shared/Epic Games/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor" "<PROJECT>" -game -windowed -ResX=1600 -ResY=900 -log=T79.log
   ```
   ```bash
   grep -E "NHOS: (SHOW END|CUT)" ~/Library/Logs/AIMegaJam2026/T79.log
   grep -c "LogScript" ~/Library/Logs/AIMegaJam2026/T79.log
   ```
   If the Mac's screen is locked (T46: game-window captures came out black), judge the look from the PIE shots of the same saved assets and say so under "Findings".
7. **Judge, as a critical first-time player** (the Done-when): do the three read as their concept images at the house camera's size, and are they told apart by body and color, not only by the topper? Write what each shot showed under T79's "## Findings", including what wasn't seen (the full mouth stretch, the cheer, sound).

**What to tune first, if a shot is off:** the visor's place and scale (the eyes or brows off the screen), the fold (hands not meeting), the springs (Decision 5), the rims seen edge-on, the knit's thumbprint values, and OpenAI's pale blue under its spotlight (T46: it reads almost white when lit; a step darker on `OBody` would mean a new seat color, so leave it unless my person asks).

## 7. What T79 commits

`Content/NHOS/Stage/BP_Robot.uasset`, `Content/NHOS/Maps/L_Stage.umap`, the new `MI_Clay_Gold`, `MI_Clay_Knit`, `MI_Clay_Steel` and `MI_Robot_Screen` and the changed `MI_Clay_Seat` and `MI_Clay_Cream` in `Content/NHOS/Stage/Materials/`, `Graphs/BP_Robot/{SetPersona,Receive,ResetLook,SetCut,SetLit,EventGraph}.txt`, `Docs/tasks/T79.md` (Result and Findings, with "Decisions made for my person"), the plan's box and `Docs/DevLog.md`, as "How to run a task" lists. Name `MI_Robot_Screen` (an `M_Robot` instance) in the commit message. `Docs/Assets.md` only if the Meshy spring is made. Unlock `BP_Robot.uasset` and `L_Stage.umap` after the push.

## 8. For later tasks

### T80 (Meta's android and my costume)

[T80-build.md](T80-build.md) starts from `BP_Robot` as this sheet leaves it: the `Face` group and its offset per head, the three sockets, the `seat`, `ring` and `glasses` tags, `_p` and `_h` in `SetPersona`'s selects, and T46's pill parts tagged `acc`, P2, which T80 replaces.

### T47 (headpieces): what [T47-build.md](T47-build.md) must change once the sockets exist

1. **Attach `Hat` to `HeadSocket`, not `Rig`** (part 2d's `MakeHat`: `:Parent (V HeadSocket)`). The hat then follows each head's socket, including Meta's and my box's (T80).
2. **`costumes.json`'s `z` is measured from the head's top:** subtract 158 from every `z` (the round head's top is at z 158 in `Rig`, where T46's dome topped out, so the fit itself doesn't change). In `make_costumes.py`, set the head-top constant to 0 instead of 158 (its "dome tops out at z 158" rule). `x` and `yaw` stay. `lift` stays: it is still measured from the stalk's base, which hasn't moved.
3. **Scale:** the hat inherits `HeadSocket`'s scale. On the round head it is 1; T80 sets Meta's and my box's (its "Findings" have the transforms), so one scale per headpiece fits all five.
4. **The dark shades:** the eyes are now at z 135 (T46: 114 to 116), so raise `dark_shades`' `bottom` in `FIT` by 19 cm; and Anthropic's glasses stand out to x 35.8 with the eyes to x 38, so move the shades' front from x 36 to about x 40.
5. **The shades hide Anthropic's glasses** (T47.md step 2): in `SetHeadpiece`, after the hat is set, loop the static mesh components and, for each with the tag `glasses` and the robot's persona tag, set its visibility to `(not (streq Id "dark_shades"))`. T80 tags Meta's glasses the same way.
6. **The lift list (part 2d's `InitLift`)** still works: the toppers are the only `acc` parts at z 165 or more, and T79 adds none there (the floor ring is on the root at z 0.6). Re-check with part 0 step 5's print.
7. **Part 0 steps 3 and 6** are out of date: the head is T79's (top at 158), and the eye line is z 135.
8. **The ear pods** stand out to y ±38 at z 128: a hood or wig narrower than 76 cm there may show them through its sides. If a close-up shows that, widen that headpiece or hide the ear pods under it (tag them `ears` and hide them in `SetHeadpiece` for the hoods and wigs).

### T75 (emotions)

- The face parts are on `Face` (scale 1), so `FaceParts`' survey finds `Face` as their parent (part 0 step 3: "a parent with scale 1").
- **`FaceR`** for the round screen: the visor's curve across the face has radius 27² ÷ 22 ≈ 33 cm (its radii 22 deep and 27 wide), not 35. The pill's is 28² ÷ 20 ≈ 39.
- **SpaceXAI's `Teeth`** (and its three `TGap`s) sits over the mouth like Meta's `Smile`: treat it as `PSmile` with `HasSmile` for the overclocker, so it hides while the bot emotes and the posed mouth shows.
- **Anthropic's eyes are inside its glasses' rims** (about 9 cm inner radius): clamp `eye_dx` and `eye_dz` so an eye stays inside its lens.
- **The brows sit near the screen's top edge** (z 144 to 145, the top about 147): a `brow_dz` over +2 cm puts them on the shell. Clamp it on the round head, or let them sit on the shell and say so.
- The resting eye scales per bot are in `SetPersona` (3a).

### T38 (bubbles)

Nothing moves: the label is still on the root at z 228, and no robot is taller.

## Findings

(For the T79 session.)
