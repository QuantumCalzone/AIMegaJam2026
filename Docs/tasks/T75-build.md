# T75 build sheet: each robot can show an emotion

Back to [T75](T75.md). A PC prep session wrote this on 2026-11-15, without the editor. It is written against **`noHumansOnSet` at `c08012d`** (the plan with T75 to T80), with `BP_Robot` **as T57 and T47 leave it** ([T57-build.md](T57-build.md) part 1, [T47-build.md](T47-build.md) part 2). Neither had pushed. T57 adds `SetPassed` and leaves `ResetLook` as it is; T47 adds `SetHeadpiece` and its helpers and changes none of the graphs below. If T38 lands first, it adds one `(CallFunction|HideBubble)` line to `SetCut` and `ResetLook` (T38-build, "Changed graphs"); keep it. Line numbers are at `c08012d`. Find each line by its text before you change it.

**T79 and T80 come first and replace T46's face** (T75 step 7, and its Depends on line). They aren't built, so every face part below is named as T46 left it (`EyeL`, `EyeR`, `Mouth`, `BrowWL`/`BrowWR`, `BrowAL`/`BrowAR`, `Smile`). The sheet keeps all of that in **one function, `FaceParts`** (part 2g): it points the emotion code at the current head's parts. Part 0 says what to read from the editor after T80, and part 2g how to change `FaceParts` for the new heads. Nothing else in the sheet names a face part.

The design doc was read, not changed: Art Inspiration, "The bots" (still T46's pill bots, which T79 rewrites: "big LED eyes and eyebrows and a mouth that stretches wide", and "no ... screaming mouths"). [Docs/BotArt.md](../BotArt.md) was read for the new cast and its rules ("Every emotion face has a mouth"), and [emotions.png](../BotArt/emotions.png) for the range on the round screen face. **T75 needs no doc edit**: T76 puts the emotion feature in the Rules tab.

Sources read: `Docs/tasks/T75.md` to `T80.md` and their plan entries, `T46.md`, `T19.md` (Findings), `T57-build.md`, `T60-build.md`, `T47-build.md`, `T38-build.md` (its `BP_Robot` part), `Docs/BotArt.md`, every file in `Graphs/BP_Robot/`, `Graphs/BPC_LinePlayer/LoadPacing.txt` and `Graphs/BPC_LLMClient/{LoadConfig,FreeAction}.txt` (the JSON and switch forms), `Tools/check_prompts.py`, `Tools/dslpp.py` and `Docs/switches.example.json`.

> **My person answered both questions** (2026-11-15, to the prep session), as recommended: the box's drawn mouth is posed like the others, and Meta's and the box's brows are dark and don't glow. See "Answers" under "Questions for my person". Don't ask again.

## In short

| T75 step | Where in this sheet |
|---|---|
| 1. The emotions are data | Part 1: the full draft of `Content/NHOS/Data/emotes.json`: 12 emotions (id, word, face, gesture, hold) and the 10 gestures, checked by part 4's code |
| 2. `BP_Robot.Emote(Emotion)` | Part 2: `Emote`, `LoadEmotes`, `ReadFace`, `ReadGesture`, `EmoteTick`, `FaceApply`, `EmoteStop`; an empty or unknown id is `neutral`, a cut robot doesn't emote, each call prints `NHOS: EMOTE`, and the talking mouth rides on top |
| 3. Brows for every bot | Part 2b: two run-time brows (`EmBrowL`, `EmBrowR`) on every robot, shown only while it emotes; Anthropic's and SpaceXAI's resting brows hand over to them; Meta's `Smile` makes way for the `Mouth` |
| 4. The gestures | Part 1 (the data) and `GestTick` (part 2e): a pose plus up to two waves, added to the `Rig` in Event Tick, faded out while the robot moves or acts |
| 5. The test switch | Part 3: `emote_test` in `Docs/switches.example.json`, read by `BP_Robot.EmoteTestInit` at BeginPlay |
| 6. The checker | Part 4: `emote_problems` in `Tools/check_prompts.py`, tried on a scratch copy |
| 7. The new cast's faces | Part 0 (what to read) and part 2g (`FaceParts` per head) |
| Done when | Part 5: the PIE run with `emote_test`, the screenshots and close-ups, the log lines, the free autoplay show with it off, `--offline` |

- **New graphs in `BP_Robot`** (each with a new file in `Graphs/BP_Robot/`): `LoadEmotes`, `FaceParts`, `NewPart`, `AttachPart`, `PartLook`, `FaceSetup`, `FaceRest`, `FaceEmoteVis`, `FaceRestVis`, `Emote`, `ReadFace`, `ReadGesture`, `ReadWave`, `EmoteTick`, `GestTick`, `FaceApply`, `PosePart`, `PlaceCorners`, `EmoteStop`, `EmoteTestInit`.
- **Changed graphs** (all have files): `EventGraph` (BeginPlay: two calls; Event Tick: the `Rig` takes the gesture, the mouth takes the emotion), `TickActs` (one call at the end), `SetPersona` (two calls), `ResetLook` (one call), `SetLit` (the new parts' glow), `SetCut` (one call).
- **No new component in the Blueprint's tree, and no `L_Stage` change:** the four new parts are made at run time, as T47 makes its `Hat`, because template components don't reach the robots already placed in `L_Stage` (T17, T46).

## Questions for my person

Both are about the new cast (T80), so they change only `FaceParts` and the brows' material. My recommendation is first in each.

**Answers (my person, 2026-11-15, to the prep session):** 1: **pose the drawn mouth**, as recommended (part 2g's last bullet doesn't apply). 2: **dark brows that don't glow**, as recommended (`BrowMat` is `ClayMat` or a black marker material for Meta and the box, `TintBrows` off). Copy these answers under "Findings" in `T75.md`.

1. **My cardboard box's drawn mouth.** T80 draws a smile on the box. **(Recommended) Pose it like the bots' mouths:** a black marker line that changes shape with each emotion. It's a cartoon, and with a fixed smile my robot would show far less than the four bots (only its eyes, brows and gesture), which reads as a tell. **Or keep the drawn smile fixed:** only the eyes behind the slots, the brows and the gesture change.
2. **Brows on Meta's doll head and my box.** **(Recommended) Dark brows that don't glow:** dark clay just above Meta's glasses, black marker just above the box's eye slots. Glowing brows suit only a screen. **Or glowing LED brows** like the screen faces of OpenAI, Anthropic and SpaceXAI.

## Decisions made for my person

My person asked prep sessions to take their own recommendation on calls that are theirs, and list them here. Each is open to change. The T75 session shows this list to my person when it closes the task.

1. **Gestures are data too.** Each gesture in `emotes.json` is a held pose (x, z, pitch, roll, yaw, scale) plus up to two sine waves on those channels, and the robot has one generic player (`GestTick`), not ten branches. So the Done-when's "rework any two that look alike" is a JSON edit with no graph rewrite, and a new gesture needs no editor work. The checker knows the six channels and the limits.
2. **`emotes` is a list, `gestures` an object.** The list keeps an order (the `emote_test` cycle, T78's chip); T76 reads the ids from it.
3. **Face values are relative to each robot's own resting face** (sizes as multipliers, moves in cm), so `neutral` is today's face on every head, value for value, and one entry fits five different heads. Only `brow_angle` is absolute, because the emotion sets the brows' slant whatever they rest at. The robot reads its resting face from its own parts at run time (`FaceRest`), not from numbers in the sheet.
4. **Three fields beyond the task's list:** `eye_dx` (both eyes slide sideways: a side-eye for suspicious, a look away for worried and embarrassed), `brow_skew` (one brow up: confused, suspicious) and `mouth_tilt` (a smirk: smug). The task allowed "curve (or tilt)" for the mouth; it gets both.
5. **The mouth curves with two corner bars** (`MouthCL`, `MouthCR`), one bent at each end of the `Mouth` bar: up for a smile, down for a frown. A scaled bar can't curve. They show only while the curve is more than 1.5°.
6. **Brows for every bot (step 3):** two new brows (`EmBrowL`, `EmBrowR`) show only while a robot emotes. On the Anthropic and SpaceXAI bots they start exactly where the resting brows sit and take over from them, then hand back at rest, so nothing jumps. On the other three they grow from zero width as the emotion comes in and shrink back as it goes. Their size and depth on the screen come from Anthropic's brows (`BrowWL`, `BrowWR`), which every robot has, hidden (T46's `acc` tags).
7. **Meta's `Smile` hides while it emotes, and the `Mouth` bar shows in its place;** both come back at rest. My robot keeps its eyes, scarf and antenna as T80 leaves them.
8. **Easing:** each face value eases on its own (in at speed 15, about 0.2 s to settle; out at speed 6, about 0.5 s). A new `Emote` eases from wherever the face is, so one emotion blends into the next.
9. **A gesture fades out while the robot moves or acts** (`MvT < 1` or the clock before `BusyUntil`) and back in when it stands, so only the face changes while it walks, grabs, gives or throws. The pose moves the `Rig`, never the actor, so the robot never leaves its mark.
10. **The tint** colors only the parts that glow: the screen face's eyes, mouth, corner bars and brows; Meta's eyes; nothing on my box (flags in `FaceParts`).
11. **Check lines:** `NHOS: EMOTE <seat> <id> persona=<persona> gesture=<gesture>` on every call (`<seat>` is the robot's `Seat`; the persona is there because T77's log reader will want it), `NHOS: EMOTE unknown <id>`, `NHOS: EMOTE loaded <n> emotions`, and `NHOS: EMOTE TEST on seat=<seat> start=<id> ids=<n>`.
12. **`emote_test` lives in the robot:** `BP_Robot` reads `Local/switches.json` at BeginPlay, so no `BP_Show` change. Each robot starts at emotion `Seat × 2 + 1` (happy, angry, scared, confused, suspicious for seats 0 to 4), so all five always show different ones, and moves on every 4 s through all 12. It keeps cycling through the title, Scene Prep and the show; a cut robot stops.
13. **Holds are 2.5 to 3.5 s** (the task: "start near 3"): surprised is the shortest, sad, confused and suspicious the longest.
14. **`TiltSign` is −1,** worked out from Unreal's roll (positive roll turns +Y toward −Z) and the robot facing the camera. It is one class default: if the angry screenshot shows the inner ends of the eyes and brows going up, set it to 1 and recompile; no graph changes.
15. **The talking stretch is added on top of the emotion's mouth** (in units of the resting mouth), so a robot talks and looks worried at once, and with no emotion the mouth stretches exactly as T46's does.
16. **The checker fails a gesture no emotion uses,** so the file stays tidy when the rework drops an emotion.

## 0. Before you start (after T80 is pushed)

1. `git pull`, read `Agents/`, `git lfs locks`. **Claim T75 and lock `Content/NHOS/Stage/BP_Robot.uasset`.** `git log --oneline -12 -- Graphs/BP_Robot Content/NHOS/Stage/BP_Robot.uasset` shows T46, T57, T47 (if done), T79 and T80. T38 may be there too.
2. **Start from the pushed graph files,** not from the copies in this sheet: T79 and T80 rewrite `SetPersona` and `EventGraph` (the hover, the new heads), and T57, T47 and T38 add functions. Every change in part 2f says where it goes by the text it sits next to.
3. **What the new heads left.** One survey script in `BP_Robot` (components and class defaults only, no graph dumps), written under "Findings" in `T75.md`:
   - **Each head's face parts.** For the shared round head, Meta's doll head and my box: the component names of the two eyes, the mouth, any resting brows, Meta's resting mouth (T46's `Smile`, or its replacement), and the box's drawn mouth. For each: its class, its static mesh, its material in slot 0, its parent (`attach_parent`), its relative location, rotation and scale, its tags, and whether it is visible on a robot of each persona after `SetPersona`.
   - **The face parents' world scale.** If a face part's parent is scaled unevenly, a part turned on it shears. Expected (T46): the eyes and mouth sit on a parent with scale 1 (a 0.1 mouth scale is 10 cm). If not, attach the new parts to the nearest parent with even scale and convert their rest transforms; say so under "Findings".
   - **The colors.** What `ResetLook` (or T80's code) sets as each head's eye and mouth `Color`, which parts glow (`Glow` in `SetLit`), and the talking stretch's numbers in Event Tick for each head (T46: `X 0.02`, `Y 0.1 + m × 0.12`, `Z 0.02 + m × 0.07`).
   - **Variables the sheet uses:** `Seat` (Integer; expected 0 to 4, set on each placed robot), `PersonaId`, `Clock`, `IsCut`, `MvT`, `BusyUntil`, `Rig`. The new names in part 2c must not exist yet. The `Rig`'s relative scale (expected 1).
   - **The construction script** (it has no file and needs no change; T19: `write_graph_dsl` can't write it): confirm it runs `SetPersona(PreviewPersona)`. That path reaches `ResetLook`, `EmoteStop` and `FaceRest`, which is why nothing in them makes a component (part 2e, `FaceSetup`).
4. **Node names** (one script, as T45-build part 2b: `find_node_types` with `context_pins: []`, then `get_node_type_pins`). The DSL below spells these as written; use what comes back:

   | In the DSL below | The Blueprint node | If it isn't there |
   |---|---|---|
   | `Transformation|GetRelativeLocation`, `GetRelativeRotation`, `GetRelativeScale3D` | the `RelativeLocation`, `RelativeRotation`, `RelativeScale3D` getters | `Transformation|GetRelativeTransform` and Break Transform |
   | `Transformation|GetAttachParent` | Get Attach Parent | the parent component's variable, from the survey |
   | `Transformation|AttachComponentToComponent` | Attach Component To Component | (T47-build 2b has it too) |
   | `Components|StaticMesh|GetStaticMesh` | the `StaticMesh` getter | the survey's mesh path as a literal |
   | `Rendering|IsVisible` | Is Visible | a Boolean per persona in `FaceParts` |
   | `Rendering|SetCastShadow` | Set Cast Shadow | leave the line out |
   | `Collision|SetCollisionEnabled` | Set Collision Enabled | (T47-build 2b) |
   | `Math|Trig|Sin(Degrees)`, `Math|Trig|Cos(Degrees)` | Sin (Degrees), Cos (Degrees) | `Math|Trig|Sin(Radians)` of the angle × 0.0174533 |

   Already in pushed sources: `Game|AddComponentbyClass` (`BPC_LLMClient/SendReq.txt`), `Components|StaticMesh|SetStaticMesh` and `Rendering|Material|SetMaterial`, `Math|Interpolation|FInterpTo` and `Math|Trig|Sin(Radians)` (`BP_Robot/EventGraph.txt`), `Utilities|Array|FindItem` (`BPC_LLMClient/AskProvider.txt`), the JSON nodes (`BPC_LinePlayer/LoadPacing.txt`), `.roll`, `.pitch`, `.yaw` on a rotator (`BP_Prop/TickFly.txt`).
5. `python Tools/check_prompts.py --offline` passes before you start.
6. Status file with `Editor: driving`. Expand the drafts with `Tools/dslpp.py` and copy them to `Saved/T75/src/` (T28: `AssetTools.read_file` reads only under `Content/` and `Saved/`). Keep each call under about 60 s.

## 1. `Content/NHOS/Data/emotes.json` (new)

The whole file. It passes part 4's check (tried on a scratch copy of `c08012d`: `--offline` exits 0 and says "Files OK: ... props.json, emotes.json and the relay's allow-list").

```json
{
	"_readme": [
		"The emotions each robot can show (T75). BP_Robot.Emote(id) reads this file once per robot. T76 lists the same ids in llm.json's reply_schema, T77 writes each emotion's word in the shared log, and T78 lists them by word on my emotion chip.",
		"emotes is a list, in the order the emote_test switch cycles them and T78's chip lists them. Each entry has id (lowercase, unique), word (the plain word T77 writes in the shared log; empty for neutral), face, gesture (a name in gestures, or none) and hold (the seconds the emotion stays before the face eases back to neutral).",
		"face poses the robot's own face, so one entry fits every head. eye_w and eye_h multiply the eyes' resting width and height. eye_dz moves both eyes up (+) or down, in cm; eye_dx moves both toward the viewer's right (+), in cm, for a side-eye. eye_tilt tips each eye's inner corner down (+, an angry V) or up (-), in degrees.",
		"brow_angle is absolute, in degrees: + raises the brows' inner ends (sad, worried), - lowers them (angry). brow_dz moves the brows up from their resting line, in cm. brow_skew raises the viewer's-left brow and lowers the viewer's-right one by half of it each, in cm (one brow up).",
		"mouth_w and mouth_h multiply the mouth's resting width and height; the talking stretch rides on top. mouth_curve bends the mouth's corners up (+, a smile) or down (-, a frown), in degrees; 0 is a straight bar. mouth_tilt raises the mouth's viewer's-right end (+, a smirk), in degrees.",
		"tint is the color [r, g, b] (linear, 0 to 1) the glowing parts lean toward, and tint_mix how far (0 is none, 1 is all the way). A face that doesn't glow (my cardboard box) ignores the tint.",
		"neutral is the resting face: eye_w, eye_h, mouth_w and mouth_h 1, every other value 0, gesture none and hold 0. The robot shows its own resting face for it: the Anthropic and SpaceXAI bots keep their brows, the others have none.",
		"Every emotion keeps a visible mouth (mouth_w at least 0.4, mouth_h at least 0.8), because the dark shades cover the eyes and a wig's bangs cover the brows (Docs/BotArt.md). No screaming mouths (the design doc's Art Inspiration tab): mouth_h is at most 4.",
		"gestures are the body's moves, shared by the emotions. pose is held while the emotion holds and eases in and out with the face: x (cm, + toward the audience), z (cm, + up), pitch (degrees, + leans back, - leans forward), roll (degrees, tips sideways), yaw (degrees, turns) and scale (0.05 is 5% bigger). waves adds at most two sine waves on top: ch (one of x, z, pitch, roll, yaw, scale), amp, hz, secs (how long it plays and fades out; 0 is the whole hold) and abs (true keeps only the upper half, for hops).",
		"A gesture moves the body, never the robot off its mark, and fades out while the robot moves, grabs, gives or throws, so only the face changes then.",
		"To add an emotion, add an entry that uses a gesture in gestures (or none), then add its id to llm.json's reply_schema (T76). No editor work. python Tools/check_prompts.py --offline checks this file."
	],
	"emotes": [
		{"id": "neutral", "word": "", "face": {"eye_w": 1, "eye_h": 1, "eye_dz": 0, "eye_dx": 0, "eye_tilt": 0, "brow_angle": 0, "brow_dz": 0, "brow_skew": 0, "mouth_w": 1, "mouth_h": 1, "mouth_curve": 0, "mouth_tilt": 0, "tint": [1, 1, 1], "tint_mix": 0}, "gesture": "none", "hold": 0},
		{"id": "happy", "word": "happy", "face": {"eye_w": 1.1, "eye_h": 0.45, "eye_dz": 1, "eye_dx": 0, "eye_tilt": -10, "brow_angle": 8, "brow_dz": 3, "brow_skew": 0, "mouth_w": 1.3, "mouth_h": 1.4, "mouth_curve": 28, "mouth_tilt": 0, "tint": [1, 0.85, 0.45], "tint_mix": 0.2}, "gesture": "bounce", "hold": 3},
		{"id": "sad", "word": "sad", "face": {"eye_w": 0.9, "eye_h": 0.7, "eye_dz": -2, "eye_dx": 0, "eye_tilt": -14, "brow_angle": 24, "brow_dz": 0, "brow_skew": 0, "mouth_w": 0.8, "mouth_h": 1, "mouth_curve": -28, "mouth_tilt": 0, "tint": [0.35, 0.5, 1], "tint_mix": 0.4}, "gesture": "slump", "hold": 3.5},
		{"id": "angry", "word": "angry", "face": {"eye_w": 1.05, "eye_h": 0.5, "eye_dz": -1, "eye_dx": 0, "eye_tilt": 22, "brow_angle": -28, "brow_dz": -3, "brow_skew": 0, "mouth_w": 1.1, "mouth_h": 1.6, "mouth_curve": -18, "mouth_tilt": 0, "tint": [1, 0.15, 0.08], "tint_mix": 0.85}, "gesture": "shake", "hold": 3},
		{"id": "worried", "word": "worried", "face": {"eye_w": 0.9, "eye_h": 1.05, "eye_dz": -2, "eye_dx": -2, "eye_tilt": -6, "brow_angle": 26, "brow_dz": 3, "brow_skew": 0, "mouth_w": 0.7, "mouth_h": 1.3, "mouth_curve": -12, "mouth_tilt": 8, "tint": [1, 1, 1], "tint_mix": 0}, "gesture": "tremble", "hold": 3},
		{"id": "scared", "word": "scared", "face": {"eye_w": 1.3, "eye_h": 1.35, "eye_dz": 1, "eye_dx": 0, "eye_tilt": 0, "brow_angle": 30, "brow_dz": 5, "brow_skew": 0, "mouth_w": 0.6, "mouth_h": 3, "mouth_curve": -8, "mouth_tilt": 0, "tint": [0.85, 0.92, 1], "tint_mix": 0.5}, "gesture": "tremble", "hold": 3},
		{"id": "surprised", "word": "surprised", "face": {"eye_w": 1.35, "eye_h": 1.4, "eye_dz": 2, "eye_dx": 0, "eye_tilt": 0, "brow_angle": 0, "brow_dz": 7, "brow_skew": 0, "mouth_w": 0.5, "mouth_h": 3.5, "mouth_curve": 0, "mouth_tilt": 0, "tint": [1, 1, 1], "tint_mix": 0}, "gesture": "jolt", "hold": 2.5},
		{"id": "confused", "word": "confused", "face": {"eye_w": 1, "eye_h": 1, "eye_dz": 0, "eye_dx": 0, "eye_tilt": 0, "brow_angle": 8, "brow_dz": 2, "brow_skew": 5, "mouth_w": 0.8, "mouth_h": 1.2, "mouth_curve": -6, "mouth_tilt": 14, "tint": [1, 1, 1], "tint_mix": 0}, "gesture": "tilt", "hold": 3.5},
		{"id": "disgusted", "word": "disgusted", "face": {"eye_w": 1, "eye_h": 0.5, "eye_dz": -1, "eye_dx": 0, "eye_tilt": 10, "brow_angle": -14, "brow_dz": -2, "brow_skew": -3, "mouth_w": 1, "mouth_h": 1.5, "mouth_curve": -24, "mouth_tilt": -12, "tint": [0.55, 1, 0.3], "tint_mix": 0.45}, "gesture": "recoil", "hold": 3},
		{"id": "suspicious", "word": "suspicious", "face": {"eye_w": 1, "eye_h": 0.4, "eye_dz": 0, "eye_dx": 3, "eye_tilt": 6, "brow_angle": -10, "brow_dz": -1, "brow_skew": 4, "mouth_w": 0.7, "mouth_h": 1, "mouth_curve": -6, "mouth_tilt": 10, "tint": [1, 1, 1], "tint_mix": 0}, "gesture": "lean_in", "hold": 3.5},
		{"id": "smug", "word": "smug", "face": {"eye_w": 1, "eye_h": 0.55, "eye_dz": 1, "eye_dx": 0, "eye_tilt": -10, "brow_angle": 6, "brow_dz": 2, "brow_skew": 0, "mouth_w": 1.1, "mouth_h": 1.1, "mouth_curve": 18, "mouth_tilt": 16, "tint": [1, 0.8, 0.3], "tint_mix": 0.2}, "gesture": "puff", "hold": 3},
		{"id": "embarrassed", "word": "embarrassed", "face": {"eye_w": 0.85, "eye_h": 0.6, "eye_dz": -2, "eye_dx": -2, "eye_tilt": -10, "brow_angle": 18, "brow_dz": 1, "brow_skew": 0, "mouth_w": 0.6, "mouth_h": 1, "mouth_curve": -4, "mouth_tilt": 6, "tint": [1, 0.45, 0.6], "tint_mix": 0.55}, "gesture": "shrink", "hold": 3}
	],
	"gestures": {
		"bounce": {"pose": {"x": 0, "z": 0, "pitch": 0, "roll": 0, "yaw": 0, "scale": 0}, "waves": [{"ch": "z", "amp": 14, "hz": 1.1, "secs": 1.35, "abs": true}]},
		"slump": {"pose": {"x": 0, "z": -10, "pitch": -10, "roll": 0, "yaw": 0, "scale": -0.03}, "waves": []},
		"shake": {"pose": {"x": 0, "z": 0, "pitch": -4, "roll": 0, "yaw": 0, "scale": 0}, "waves": [{"ch": "yaw", "amp": 18, "hz": 7.2, "secs": 1, "abs": false}]},
		"tremble": {"pose": {"x": 0, "z": -3, "pitch": 0, "roll": 0, "yaw": 0, "scale": -0.02}, "waves": [{"ch": "roll", "amp": 2, "hz": 11, "secs": 0, "abs": false}, {"ch": "yaw", "amp": 1.5, "hz": 9, "secs": 0, "abs": false}]},
		"jolt": {"pose": {"x": -6, "z": 0, "pitch": 6, "roll": 0, "yaw": 0, "scale": 0.02}, "waves": [{"ch": "z", "amp": 16, "hz": 1.4, "secs": 0.36, "abs": true}]},
		"tilt": {"pose": {"x": 0, "z": 0, "pitch": 0, "roll": 0, "yaw": 0, "scale": 0}, "waves": [{"ch": "roll", "amp": 9, "hz": 0.45, "secs": 0, "abs": false}]},
		"recoil": {"pose": {"x": -8, "z": 0, "pitch": 10, "roll": 0, "yaw": 15, "scale": 0}, "waves": []},
		"lean_in": {"pose": {"x": 6, "z": 0, "pitch": -9, "roll": 0, "yaw": 0, "scale": 0}, "waves": [{"ch": "yaw", "amp": 6, "hz": 0.35, "secs": 0, "abs": false}]},
		"puff": {"pose": {"x": 0, "z": 3, "pitch": 7, "roll": 0, "yaw": 0, "scale": 0.07}, "waves": []},
		"shrink": {"pose": {"x": 0, "z": -8, "pitch": -6, "roll": 0, "yaw": 28, "scale": -0.07}, "waves": [{"ch": "roll", "amp": 2, "hz": 1.2, "secs": 0, "abs": false}]}
	}
}
```

**Why these numbers.**

- **Faces** follow the range in [emotions.png](../BotArt/emotions.png) on the round screen face: lidded, slanted eyes for angry and suspicious, round wide eyes for scared and surprised, small open mouths (never screaming) for scared and surprised. A 2D mock of all 12 (the T46 face's proportions: eyes 10 × 13 cm at ±12 cm, brows 4 cm above them, a 10 × 2 cm mouth 14 cm below) read as follows: angry (red, V brows, a frown), happy (squinting eyes, a smile), surprised (raised brows, an "o"), confused (one brow up, a slanted mouth) and disgusted (green, a crooked frown) read at once. Smug and suspicious first looked alike, so smug's brows went level and up and suspicious keeps the one raised brow.
- **The likeliest look-alikes** are sad, worried and embarrassed (brows up, a small frown on all three). Their tints (blue, none, pink), eye moves (down, a glance to the viewer's left, down and away) and gestures (slump, tremble, shrink and turn away) carry them. Check this trio first in the screenshots. Worried and scared share `tremble` (the task's list); if they read alike, give worried its own gesture, for example `"fidget": {"pose": {... "z": -2 ...}, "waves": [{"ch": "roll", "amp": 3, "hz": 2, "secs": 0, "abs": false}]}`.
- **Gestures:** `bounce` is three hops in 1.35 s (`abs` of a 1.1 Hz wave hops every 0.45 s). `shake` is T19's shake (yaw ±14° at 45 rad/s, about 7.2 Hz, for 0.8 s) made harder: ±18° for 1 s. `jolt` is one hop (half a 1.4 Hz wave is 0.36 s) while it leans back. `tilt` rocks ±9° about every 2.2 s. A burst wave (`secs` above 0) fades out over its `secs`, so it never stops with a jerk; a whole-hold wave (`secs` 0) fades with the emotion.
- **Directions to check in the first screenshots:** pitch − leans toward the audience (T19's cut slump uses pitch −14 to tip forward), and `TiltSign` (decision 14). `yaw` + on `recoil` and `shrink` turns the body one way; if the eye moves (`eye_dx` −2 on embarrassed) look the other way, flip the sign of `eye_dx` there.

## 2. `BP_Robot`

### 2a. Which graphs, which have files

| Graph | File in `Graphs/BP_Robot/` | T75 changes | How |
|---|---|---|---|
| `EventGraph` | `EventGraph.txt` | BeginPlay calls `FaceSetup` and `EmoteTestInit`; Event Tick adds the gesture to the `Rig`, sizes the mouth from the emotion, places the corners | DSL write from the pushed file (2f) |
| `TickActs` | `TickActs.txt` | Calls `EmoteTick` at the end | DSL write from the file (2f) |
| `SetPersona` | `SetPersona.txt` | `EmoteStop` first, `FaceRest` before `ResetLook` | DSL write from the pushed file (2f) |
| `ResetLook` | `ResetLook.txt` | `EmoteStop` first | DSL write from the file (2f) |
| `SetLit` | `SetLit.txt` | The new parts' glow | DSL write from the file (2f) |
| `SetCut` | `SetCut.txt` | `EmoteStop` first | DSL write from the file (2f) |
| `Shake`, `Cheer`, `StartAct`, `Receive`, the rest | have files | nothing | — |
| `UserConstructionScript` | none (T19: can't be written) | nothing | Survey only (part 0, step 3) |
| the 20 new functions | new | — | `add_function_graph`, then `write_graph_dsl` (2e) |

Make every new function first (with its inputs and outputs, table in 2e), write them in the order of 2e, then the changed graphs. Compile and save after each few.

### 2b. The four new parts (made at run time)

None of them is in the Blueprint's component tree. `FaceSetup` makes them once per robot at BeginPlay, with `Add Component by Class` (as T47's `MakeHat`), so the five robots in `L_Stage` get them with no re-place and `L_Stage` stays out of T75. `FaceRest` attaches them to the current head and gives them its materials, each time `SetPersona` runs.

| Variable | Type | Parent | Mesh | Material (slot 0) | Rest transform (relative) | Shown |
|---|---|---|---|---|---|---|
| `EmBrowL` | `StaticMeshComponent` | the parent of `PBrowL` (T46: the parent of `BrowWL`) | the mesh of `PBrowL` | `BrowMat` (T46: the eyes' LED material, `LedMat`) | On the Anthropic bot: `BrowWL`'s. On SpaceXAI: `BrowAL`'s. On the others: `BrowWL`'s depth (x) and scale, centered over `EyeL` (its y), at the eye's top plus `BrowGap` 4 cm, roll 0 | Only while the robot emotes |
| `EmBrowR` | `StaticMeshComponent` | the parent of `PBrowR` | the mesh of `PBrowR` | `BrowMat` | the same with `BrowWR`, `BrowAR`, `EyeR` | Only while the robot emotes |
| `MouthCL` | `StaticMeshComponent` | the parent of `PMouth` (T46: the parent of `Mouth`) | the mesh of `PMouth` | `CornerMat` (T46: `LedMat`) | Set each frame by `PlaceCorners`: at the viewer's-left end of the mouth, bent by `mouth_curve`; the mouth's depth and resting height, `0.35 ×` its width long | Only while the robot emotes and the curve is over 1.5° |
| `MouthCR` | `StaticMeshComponent` | the parent of `PMouth` | the mesh of `PMouth` | `CornerMat` | the same at the viewer's-right end | the same |

All four: collision off, no shadow, hidden at first, `Color` set to `LedColor` and `Glow` to 3 (10 while the robot is lit). No tags, so `SetPersona`'s `acc` loop and T47's `InitLift` never touch them.

### 2c. Variables

| Variable | Type | Default | What for |
|---|---|---|---|
| `EmBrowL`, `EmBrowR`, `MouthCL`, `MouthCR`, `TmpPart` | `StaticMeshComponent` ref | none | The new parts (2b) |
| `PEyeL`, `PEyeR`, `PMouth`, `PSmile`, `PBrowL`, `PBrowR` | `StaticMeshComponent` ref (use `PrimitiveComponent` if a part isn't a static mesh) | none | The current head's face parts, set by `FaceParts` |
| `LedMat`, `ClayMat` | `MaterialInterface` ref | `LedMat`: the eyes' material from the survey; `ClayMat`: `/Game/NHOS/Stage/Materials/MI_Clay_Charcoal` | Class defaults the brows and corners can take |
| `BrowMat`, `CornerMat` | `MaterialInterface` ref | none | Set by `FaceParts` |
| `FaceReady`, `HasRest`, `RestBrows`, `HasSmile`, `MouthVis`, `TintEyes`, `TintMouth`, `TintBrows`, `TintDirty`, `LitOn` | Boolean | false (`TintEyes`, `TintMouth`, `TintBrows` true) | State and per-head flags |
| `EmLoaded`, `EmOn`, `EmNeutral`, `EmTest`, `G1On`, `G2On`, `G1Abs`, `G2Abs`, `WAbs` | Boolean | false | The emotion's state |
| `RestFor`, `EmId`, `EmGesture`, `TmpId` | String | "" | |
| `EmIdx`, `EmTestIdx`, `G1Ch`, `G2Ch`, `WCh` | Integer | 0 (`G1Ch`, `G2Ch`, `WCh` −1) | |
| `EmIds` | String array | empty | The ids, in file order |
| `GChans` | String array | `x`, `z`, `pitch`, `roll`, `yaw`, `scale` | A wave's channel name to its number |
| `EmList`, `GWaves` | `JsonObjectWrapper` array | empty | `emotes`, a gesture's `waves` |
| `EmGest`, `EmEntry`, `EmFace`, `GEntry`, `GPoseObj`, `GWave` | `JsonObjectWrapper` | empty | |
| `TintArr` | Float array | empty | A face's `tint` |
| `RestEyeLocL`, `RestEyeLocR`, `RestEyeScaleL`, `RestEyeScaleR`, `RestBrowLocL`, `RestBrowLocR`, `RestBrowScaleL`, `RestBrowScaleR`, `RestMouthLoc` | Vector | 0 | The resting face (`FaceRest`) |
| `MouthRest`, `MouthNow` | Vector | (0.02, 0.1, 0.02) | The mouth's resting scale (T46's Event Tick numbers), and the emotion's mouth before the talking stretch |
| `LedColor` | Vector | (0.55, 0.85, 1.0) | The LED color `ResetLook` sets (T46) |
| `TintCol` | Vector | (1, 1, 1) | |
| `RigScale0` | Vector | (1, 1, 1) | The `Rig`'s own scale |
| `RestEyeRotL`, `RestEyeRotR`, `RestBrowRotL`, `RestBrowRotR`, `RestMouthRot` | Rotator | 0 | |
| `TiltSign` | Float | −1 | Decision 14 |
| `BrowGap`, `CornerFrac`, `CornerX`, `FaceR`, `EmTestStep` | Float | 4, 0.35, 0.4, 35, 4 | Brow height over the eye (cm), corner length (share of the mouth's width), corners' forward bias (cm), the screen's radius (cm), seconds per emotion in the test |
| `SideEyeL`, `SideEyeR`, `SideBrowL`, `SideBrowR` | Float | 1 | +1 for a part on the robot's +Y side (the viewer's left), −1 for −Y |
| `RestBrowRL`, `RestBrowRR`, `EmStart`, `EmUntil`, `EmHold`, `EmTestNext` | Float | 0 | |
| `TEyeW`, `TEyeH`, `TEyeDZ`, `TEyeDX`, `TEyeTilt`, `TBrowA`, `TBrowDZ`, `TBrowSkew`, `TMouthW`, `TMouthH`, `TCurve`, `TMTilt`, `TTint`, `TBrowRL`, `TBrowRR` | Float | 0 (`TEyeW`, `TEyeH`, `TMouthW`, `TMouthH` 1) | The emotion's target face |
| `FEyeW`, `FEyeH`, `FEyeDZ`, `FEyeDX`, `FEyeTilt`, `FBrowRL`, `FBrowRR`, `FBrowDZ`, `FBrowSkew`, `BrowK`, `FMouthW`, `FMouthH`, `FCurve`, `FMTilt`, `FTint` | Float | 0 (`FEyeW`, `FEyeH`, `FMouthW`, `FMouthH` 1) | The face now, eased toward the target |
| `GPoseX`, `GPoseZ`, `GPosePitch`, `GPoseRoll`, `GPoseYaw`, `GPoseScale`, `G1Amp`, `G1Hz`, `G1Secs`, `G2Amp`, `G2Hz`, `G2Secs`, `WAmp`, `WHz`, `WSecs`, `GW`, `GK` | Float | 0 | The gesture's data, its weight (`GW`) and its gate while moving (`GK`) |
| `GX`, `GZ`, `GPitch`, `GRoll`, `GYaw`, `GScale` | Float | 0 | The gesture's offsets that Event Tick adds to the `Rig` |

### 2d. The functions to make

| Function | Inputs | Output |
|---|---|---|
| `Emote` | `Emotion` (String) | |
| `EmoteTick` | `Delta` (Float) | |
| `PlaceCorners` | `W` (Float) | |
| `PosePart` | `P` (`StaticMeshComponent` ref), `Loc` (Vector), `Rot` (Rotator), `Roll` (Float), `Scale` (Vector) | |
| `AttachPart` | `P` (`StaticMeshComponent` ref), `To` (`SceneComponent` ref) | |
| `PartLook` | `P` (`StaticMeshComponent` ref), `Mat` (`MaterialInterface` ref), `Mesh` (`StaticMesh` ref) | |
| `ReadWave` | `I` (Integer) | |
| `NewPart` | | `Part` (`StaticMeshComponent` ref) |
| `LoadEmotes`, `FaceParts`, `FaceSetup`, `FaceRest`, `FaceEmoteVis`, `FaceRestVis`, `ReadFace`, `ReadGesture`, `GestTick`, `FaceApply`, `EmoteStop`, `EmoteTestInit` | | |

T19: functions made with `add_function_graph` are impure, so the DSL binds each call's result before an `if`, `return` or `select` uses it. A pure `select` evaluates both sides, so no `select` below reads an array at an index that may be out of range.

### 2e. The new graphs (one file each)

**`LoadEmotes`**

```lisp
; T75: emotes.json, read once per robot (the first Emote, or EmoteTestInit at BeginPlay).
(fn LoadEmotes ()
  (if (V EmLoaded)
    (return))
  (set EmLoaded true)
  (clear (V EmIds))
  (bind (_o _ok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat (Utilities|Paths|GetProjectContentDirectory) "NHOS/Data/emotes.json"))))
  (if (not _ok)
    (print "NHOS: EMOTE emotes.json missing or not valid JSON")
    (return))
  (bind _l (Json|GetField _o "emotes"))
  (set EmList _l)
  (bind _g (Json|GetField _o "gestures"))
  (set EmGest _g)
  (for _e (V EmList)
    (bind _id (Json|GetField _e "id"))
    (set TmpId _id)
    (add (V EmIds) (V TmpId)))
  (print (cat "NHOS: EMOTE loaded " (cat (str (len (V EmIds))) " emotions"))))
```

**`FaceParts`** (the one place that names face parts; part 2g changes it for T79 and T80)

```lisp
; T75: points the emotion code at this robot's face parts. T46's head: one screen face on every robot,
; brows on the worrier (BrowWL/WR) and the overclocker (BrowAL/AR), a fixed Smile on the copycat.
; The other robots' hidden worrier brows give the new brows their size and depth (FaceRest).
(fn FaceParts ()
  (set PEyeL (Variables|Default|GetEyeL))
  (set PEyeR (Variables|Default|GetEyeR))
  (set PMouth (Variables|Default|GetMouth))
  (set PSmile (Variables|Default|GetSmile))
  (set HasSmile true)
  (bind _w (streq (V PersonaId) "worrier"))
  (bind _o (streq (V PersonaId) "overclocker"))
  (set RestBrows (or _w _o))
  (set PBrowL (select _o (Variables|Default|GetBrowAL) (Variables|Default|GetBrowWL)))
  (set PBrowR (select _o (Variables|Default|GetBrowAR) (Variables|Default|GetBrowWR)))
  (set BrowMat (V LedMat))
  (set CornerMat (V LedMat))
  (set LedColor (Math|Vector|MakeVector :X 0.55 :Y 0.85 :Z 1.0))
  (set MouthRest (Math|Vector|MakeVector :X 0.02 :Y 0.1 :Z 0.02))
  (set TintEyes true)
  (set TintMouth true)
  (set TintBrows true))
```

**`NewPart`, `AttachPart`, `PartLook`**

```lisp
; T75: one hidden part with no collision and no shadow, on the Rig until FaceRest attaches it to the face.
(fn NewPart ()
  (bind _c (Game|AddComponentbyClass self "/Script/Engine.StaticMeshComponent" :bManualAttachment true))
  (set TmpPart _c)
  (Collision|SetCollisionEnabled :self (V TmpPart) :NewType "NoCollision")
  (Rendering|SetCastShadow :self (V TmpPart) :NewCastShadow false)
  (Rendering|SetVisibility :self (V TmpPart) :bNewVisibility false :bPropagateToChildren false)
  (CallFunction|AttachPart :P (V TmpPart) :To (Variables|Default|GetRig))
  (return (V TmpPart)))
```

```lisp
; T75: attaches a new part to a face part's parent, keeping its relative transform (FaceApply sets it).
(fn AttachPart (P To)
  (Transformation|AttachComponentToComponent :self P :Parent To :LocationRule "KeepRelative" :RotationRule "KeepRelative" :ScaleRule "KeepRelative" :bWeldSimulatedBodies false))
```

```lisp
; T75: a new part takes the head's mesh and material, then the LED color and the glow it would have now.
(fn PartLook (P Mat Mesh)
  (Components|StaticMesh|SetStaticMesh :self P :NewMesh Mesh)
  (Rendering|Material|SetMaterial :self P :ElementIndex 0 :Material Mat)
  (Rendering|Material|SetVectorParameterValueonMaterials :self P :ParameterName "Color" :ParameterValue (V LedColor))
  (Rendering|Material|SetScalarParameterValueonMaterials :self P :ParameterName "Glow" :ParameterValue (select (V LitOn) 10.0 3.0)))
```

**`FaceSetup`**

```lisp
; T75: makes the four parts every robot needs for emotions, once, at BeginPlay: two brows (EmBrowL, EmBrowR)
; and the mouth's two corner bars (MouthCL, MouthCR). Made at run time, so the robots already placed in
; L_Stage get them with no re-place (T17, T46, T47). Never called from the construction script.
(fn FaceSetup ()
  (if (V FaceReady)
    (return))
  (set RigScale0 (Transformation|GetRelativeScale3D :self (Variables|Default|GetRig)))
  (bind _a (CallFunction|NewPart))
  (set EmBrowL _a)
  (bind _b (CallFunction|NewPart))
  (set EmBrowR _b)
  (bind _c (CallFunction|NewPart))
  (set MouthCL _c)
  (bind _d (CallFunction|NewPart))
  (set MouthCR _d)
  (set FaceReady true)
  (CallFunction|FaceRest))
```

**`FaceRest`**

```lisp
; T75: reads this robot's resting face from its parts, so neutral is its face value for value.
; SetPersona calls it after it sets the persona's face; Emote calls it if the persona changed since.
; It only reads in the construction script; with FaceReady it also moves the new parts onto this head.
(fn FaceRest ()
  (CallFunction|FaceParts)
  (set RestEyeLocL (Transformation|GetRelativeLocation :self (V PEyeL)))
  (set RestEyeRotL (Transformation|GetRelativeRotation :self (V PEyeL)))
  (set RestEyeScaleL (Transformation|GetRelativeScale3D :self (V PEyeL)))
  (set RestEyeLocR (Transformation|GetRelativeLocation :self (V PEyeR)))
  (set RestEyeRotR (Transformation|GetRelativeRotation :self (V PEyeR)))
  (set RestEyeScaleR (Transformation|GetRelativeScale3D :self (V PEyeR)))
  (set SideEyeL (select (< (.y (V RestEyeLocL)) 0.0) -1.0 1.0))
  (set SideEyeR (select (< (.y (V RestEyeLocR)) 0.0) -1.0 1.0))
  (set RestMouthLoc (Transformation|GetRelativeLocation :self (V PMouth)))
  (set RestMouthRot (Transformation|GetRelativeRotation :self (V PMouth)))
  (bind _mv (Rendering|IsVisible :self (V PMouth)))
  (set MouthVis _mv)
  (bind _bl (Transformation|GetRelativeLocation :self (V PBrowL)))
  (bind _br (Transformation|GetRelativeLocation :self (V PBrowR)))
  (set RestBrowScaleL (Transformation|GetRelativeScale3D :self (V PBrowL)))
  (set RestBrowScaleR (Transformation|GetRelativeScale3D :self (V PBrowR)))
  (if (V RestBrows)
    (set RestBrowLocL _bl)
    (set RestBrowLocR _br)
    (set RestBrowRotL (Transformation|GetRelativeRotation :self (V PBrowL)))
    (set RestBrowRotR (Transformation|GetRelativeRotation :self (V PBrowR)))
    (else
      (set RestBrowLocL (Math|Vector|MakeVector :X (.x _bl) :Y (.y (V RestEyeLocL)) :Z (+ (.z (V RestEyeLocL)) (+ (* (.z (V RestEyeScaleL)) 50.0) (V BrowGap)))))
      (set RestBrowLocR (Math|Vector|MakeVector :X (.x _br) :Y (.y (V RestEyeLocR)) :Z (+ (.z (V RestEyeLocR)) (+ (* (.z (V RestEyeScaleR)) 50.0) (V BrowGap)))))
      (set RestBrowRotL (Math|Rotator|MakeRotator :Roll 0.0 :Pitch (.pitch (V RestEyeRotL)) :Yaw (.yaw (V RestEyeRotL))))
      (set RestBrowRotR (Math|Rotator|MakeRotator :Roll 0.0 :Pitch (.pitch (V RestEyeRotR)) :Yaw (.yaw (V RestEyeRotR))))))
  (set RestBrowRL (.roll (V RestBrowRotL)))
  (set RestBrowRR (.roll (V RestBrowRotR)))
  (set SideBrowL (select (< (.y (V RestBrowLocL)) 0.0) -1.0 1.0))
  (set SideBrowR (select (< (.y (V RestBrowLocR)) 0.0) -1.0 1.0))
  (set FBrowRL (V RestBrowRL))
  (set FBrowRR (V RestBrowRR))
  (set BrowK (select (V RestBrows) 1.0 0.0))
  (set MouthNow (V MouthRest))
  (set RestFor (V PersonaId))
  (set HasRest true)
  (if (V FaceReady)
    (bind _bp (Transformation|GetAttachParent :self (V PBrowL)))
    (bind _bq (Transformation|GetAttachParent :self (V PBrowR)))
    (bind _mp (Transformation|GetAttachParent :self (V PMouth)))
    (CallFunction|AttachPart :P (V EmBrowL) :To _bp)
    (CallFunction|AttachPart :P (V EmBrowR) :To _bq)
    (CallFunction|AttachPart :P (V MouthCL) :To _mp)
    (CallFunction|AttachPart :P (V MouthCR) :To _mp)
    (bind _bm (Components|StaticMesh|GetStaticMesh :self (V PBrowL)))
    (bind _mm (Components|StaticMesh|GetStaticMesh :self (V PMouth)))
    (CallFunction|PartLook :P (V EmBrowL) :Mat (V BrowMat) :Mesh _bm)
    (CallFunction|PartLook :P (V EmBrowR) :Mat (V BrowMat) :Mesh _bm)
    (CallFunction|PartLook :P (V MouthCL) :Mat (V CornerMat) :Mesh _mm)
    (CallFunction|PartLook :P (V MouthCR) :Mat (V CornerMat) :Mesh _mm)))
```

- `* 50.0`: the eyes are 100 cm engine shapes scaled down (T46: a 0.1 scale is 10 cm), so half the eye's height in cm is its z scale × 50. Check the brows' place on a close-up and tune `BrowGap`.
- `Set Material` replaces the dynamic instance, so `PartLook` sets `Color` and `Glow` again after it (each call makes a fresh instance for that part only; the parts never share the eyes' instance).

**`FaceEmoteVis` and `FaceRestVis`**

```lisp
; T75: while an emotion shows: the new brows take over from any resting brows, and the copycat's Smile
; makes way for the Mouth bar. Hide first, then show, in case one part plays two roles on a new head.
(fn FaceEmoteVis ()
  (Rendering|SetVisibility :self (V PBrowL) :bNewVisibility false :bPropagateToChildren false)
  (Rendering|SetVisibility :self (V PBrowR) :bNewVisibility false :bPropagateToChildren false)
  (if (V HasSmile)
    (Rendering|SetVisibility :self (V PSmile) :bNewVisibility false :bPropagateToChildren false))
  (Rendering|SetVisibility :self (V PMouth) :bNewVisibility true :bPropagateToChildren false)
  (Rendering|SetVisibility :self (V EmBrowL) :bNewVisibility true :bPropagateToChildren false)
  (Rendering|SetVisibility :self (V EmBrowR) :bNewVisibility true :bPropagateToChildren false))
```

```lisp
; T75: the resting face's parts, as SetPersona leaves them: resting brows only on the worrier and the
; overclocker, the Smile only on the copycat (its acc tag), the Mouth as FaceRest found it.
(fn FaceRestVis ()
  (Rendering|SetVisibility :self (V EmBrowL) :bNewVisibility false :bPropagateToChildren false)
  (Rendering|SetVisibility :self (V EmBrowR) :bNewVisibility false :bPropagateToChildren false)
  (Rendering|SetVisibility :self (V MouthCL) :bNewVisibility false :bPropagateToChildren false)
  (Rendering|SetVisibility :self (V MouthCR) :bNewVisibility false :bPropagateToChildren false)
  (Rendering|SetVisibility :self (V PBrowL) :bNewVisibility (V RestBrows) :bPropagateToChildren false)
  (Rendering|SetVisibility :self (V PBrowR) :bNewVisibility (V RestBrows) :bPropagateToChildren false)
  (if (V HasSmile)
    (bind _sm (Components|ComponentHasTag :self (V PSmile) :Tag (Utilities|String|StringToName (V PersonaId))))
    (Rendering|SetVisibility :self (V PSmile) :bNewVisibility _sm :bPropagateToChildren false))
  (Rendering|SetVisibility :self (V PMouth) :bNewVisibility (V MouthVis) :bPropagateToChildren false))
```

**`Emote`**

```lisp
; T75: shows emotion Emotion (an id in emotes.json): the face eases to its pose in about 0.2 s, the gesture
; plays, and after its hold (or at the next Emote) the face eases back to neutral. An empty or unknown id
; is neutral; an unknown one also prints. A cut robot doesn't emote (as Shake and Cheer).
(fn Emote (Emotion)
  (if (V IsCut)
    (return))
  (CallFunction|LoadEmotes)
  (CallFunction|FaceSetup)
  (if (or (not (V HasRest)) (not (streq (V RestFor) (V PersonaId))))
    (CallFunction|FaceRest))
  (set EmIdx (Utilities|Array|FindItem (V EmIds) Emotion))
  (if (and (< (V EmIdx) 0) (not (Utilities|String|IsEmpty Emotion)))
    (print (cat "NHOS: EMOTE unknown " Emotion)))
  (if (< (V EmIdx) 0)
    (set EmIdx (Utilities|Array|FindItem (V EmIds) "neutral")))
  (set EmId "neutral")
  (if (>= (V EmIdx) 0)
    (set EmId (get (V EmIds) (V EmIdx))))
  (set EmNeutral (streq (V EmId) "neutral"))
  (set EmStart (V Clock))
  (if (V EmNeutral)
    (set EmUntil (V Clock))
    (print (cat "NHOS: EMOTE " (cat (str (V Seat)) (cat " neutral persona=" (cat (V PersonaId) " gesture=none")))))
    (return))
  (set EmEntry (get (V EmList) (V EmIdx)))
  (CallFunction|ReadFace)
  (CallFunction|ReadGesture)
  (bind _h (Json|GetField (V EmEntry) "hold"))
  (set EmHold _h)
  (set EmUntil (+ (V Clock) (+ 0.2 (V EmHold))))
  (if (not (V EmOn))
    (set EmOn true)
    (CallFunction|FaceEmoteVis))
  (print (cat "NHOS: EMOTE " (cat (str (V Seat)) (cat " " (cat (V EmId) (cat " persona=" (cat (V PersonaId) (cat " gesture=" (V EmGesture))))))))))
```

- `neutral` while another emotion shows sets `EmUntil` to now, so `EmoteTick` eases everything back and `EmoteStop` ends it 1 s later. `neutral` at rest only prints.
- The prints nest `cat` two at a time; `(cat a b c ...)` in `dslpp` does the same, so either form works.

**`ReadFace`**

```lisp
; T75: the emotion's face from emotes.json into the targets (T...). The brows' targets are absolute rolls,
; mirrored per side: + brow_angle raises the inner ends (decision 14 for TiltSign).
(fn ReadFace ()
  (bind _f (Json|GetField (V EmEntry) "face"))
  (set EmFace _f)
  (bind _ew (Json|GetField (V EmFace) "eye_w"))
  (set TEyeW _ew)
  (bind _eh (Json|GetField (V EmFace) "eye_h"))
  (set TEyeH _eh)
  (bind _ez (Json|GetField (V EmFace) "eye_dz"))
  (set TEyeDZ _ez)
  (bind _ex (Json|GetField (V EmFace) "eye_dx"))
  (set TEyeDX _ex)
  (bind _et (Json|GetField (V EmFace) "eye_tilt"))
  (set TEyeTilt _et)
  (bind _ba (Json|GetField (V EmFace) "brow_angle"))
  (set TBrowA _ba)
  (bind _bz (Json|GetField (V EmFace) "brow_dz"))
  (set TBrowDZ _bz)
  (bind _bs (Json|GetField (V EmFace) "brow_skew"))
  (set TBrowSkew _bs)
  (bind _mw (Json|GetField (V EmFace) "mouth_w"))
  (set TMouthW _mw)
  (bind _mh (Json|GetField (V EmFace) "mouth_h"))
  (set TMouthH _mh)
  (bind _mc (Json|GetField (V EmFace) "mouth_curve"))
  (set TCurve _mc)
  (bind _mt (Json|GetField (V EmFace) "mouth_tilt"))
  (set TMTilt _mt)
  (bind _ta (Json|GetField (V EmFace) "tint"))
  (set TintArr _ta)
  (if (>= (len (V TintArr)) 3)
    (set TintCol (Math|Vector|MakeVector :X (get (V TintArr) 0) :Y (get (V TintArr) 1) :Z (get (V TintArr) 2))))
  (bind _tm (Json|GetField (V EmFace) "tint_mix"))
  (set TTint _tm)
  (set TBrowRL (* (- 0.0 (V TiltSign)) (* (V SideBrowL) (V TBrowA))))
  (set TBrowRR (* (- 0.0 (V TiltSign)) (* (V SideBrowR) (V TBrowA)))))
```

If `Get Field` won't fill a Float array (`TintArr`), change `tint` to a hex string in `emotes.json` and read it with T47's `HexColor` (if T47 is in) or three fields `tint_r`, `tint_g`, `tint_b`; change part 4's tint check to match, and say so under "Findings".

**`ReadGesture` and `ReadWave`**

```lisp
; T75: the emotion's gesture from emotes.json: its held pose and up to two waves. "none" or a name
; not in gestures plays no gesture (the checker fails that name).
(fn ReadGesture ()
  (bind _g (Json|GetField (V EmEntry) "gesture"))
  (set EmGesture _g)
  (set GPoseX 0.0)
  (set GPoseZ 0.0)
  (set GPosePitch 0.0)
  (set GPoseRoll 0.0)
  (set GPoseYaw 0.0)
  (set GPoseScale 0.0)
  (set G1On false)
  (set G2On false)
  (bind _gn (Utilities|String|StringToName (V EmGesture)))
  (bind _has (Json|HasField (V EmGest) _gn))
  (if (or (streq (V EmGesture) "none") (not _has))
    (return))
  (bind _ge (Json|GetField (V EmGest) _gn))
  (set GEntry _ge)
  (bind _p (Json|GetField (V GEntry) "pose"))
  (set GPoseObj _p)
  (bind _px (Json|GetField (V GPoseObj) "x"))
  (set GPoseX _px)
  (bind _pz (Json|GetField (V GPoseObj) "z"))
  (set GPoseZ _pz)
  (bind _pp (Json|GetField (V GPoseObj) "pitch"))
  (set GPosePitch _pp)
  (bind _pr (Json|GetField (V GPoseObj) "roll"))
  (set GPoseRoll _pr)
  (bind _py (Json|GetField (V GPoseObj) "yaw"))
  (set GPoseYaw _py)
  (bind _ps (Json|GetField (V GPoseObj) "scale"))
  (set GPoseScale _ps)
  (bind _w (Json|GetField (V GEntry) "waves"))
  (set GWaves _w)
  (if (> (len (V GWaves)) 0)
    (CallFunction|ReadWave :I 0)
    (set G1On (>= (V WCh) 0))
    (set G1Ch (V WCh))
    (set G1Amp (V WAmp))
    (set G1Hz (V WHz))
    (set G1Secs (V WSecs))
    (set G1Abs (V WAbs)))
  (if (> (len (V GWaves)) 1)
    (CallFunction|ReadWave :I 1)
    (set G2On (>= (V WCh) 0))
    (set G2Ch (V WCh))
    (set G2Amp (V WAmp))
    (set G2Hz (V WHz))
    (set G2Secs (V WSecs))
    (set G2Abs (V WAbs))))
```

```lisp
; T75: wave I of the gesture into WCh (0 x, 1 z, 2 pitch, 3 roll, 4 yaw, 5 scale; -1 unknown), WAmp, WHz, WSecs, WAbs.
(fn ReadWave (I)
  (set GWave (get (V GWaves) I))
  (bind _ch (Json|GetField (V GWave) "ch"))
  (set TmpId _ch)
  (set WCh (Utilities|Array|FindItem (V GChans) (V TmpId)))
  (bind _a (Json|GetField (V GWave) "amp"))
  (set WAmp _a)
  (bind _hz (Json|GetField (V GWave) "hz"))
  (set WHz _hz)
  (bind _s (Json|GetField (V GWave) "secs"))
  (set WSecs _s)
  (bind _b (Json|GetField (V GWave) "abs"))
  (set WAbs _b))
```

**`EmoteTick`**

```lisp
; T75: each frame (TickActs calls it): the emote_test cycle, then the face and the gesture ease toward the
; emotion while it holds and back to rest after, and the gesture fades while the robot moves or acts.
(fn EmoteTick (Delta)
  (bind _c (V Clock))
  (if (and (V EmTest) (and (not (V IsCut)) (>= _c (V EmTestNext))))
    (set EmTestNext (+ _c (V EmTestStep)))
    (CallFunction|Emote :Emotion (get (V EmIds) (V EmTestIdx)))
    (set EmTestIdx (+ (V EmTestIdx) 1))
    (if (>= (V EmTestIdx) (len (V EmIds)))
      (set EmTestIdx 0)))
  (if (not (V EmOn))
    (return))
  (bind _hold (< _c (V EmUntil)))
  (bind _sp (select _hold 15.0 6.0))
  (set FEyeW (Math|Interpolation|FInterpTo (V FEyeW) (select _hold (V TEyeW) 1.0) Delta _sp))
  (set FEyeH (Math|Interpolation|FInterpTo (V FEyeH) (select _hold (V TEyeH) 1.0) Delta _sp))
  (set FEyeDZ (Math|Interpolation|FInterpTo (V FEyeDZ) (select _hold (V TEyeDZ) 0.0) Delta _sp))
  (set FEyeDX (Math|Interpolation|FInterpTo (V FEyeDX) (select _hold (V TEyeDX) 0.0) Delta _sp))
  (set FEyeTilt (Math|Interpolation|FInterpTo (V FEyeTilt) (select _hold (V TEyeTilt) 0.0) Delta _sp))
  (set FBrowRL (Math|Interpolation|FInterpTo (V FBrowRL) (select _hold (V TBrowRL) (V RestBrowRL)) Delta _sp))
  (set FBrowRR (Math|Interpolation|FInterpTo (V FBrowRR) (select _hold (V TBrowRR) (V RestBrowRR)) Delta _sp))
  (set FBrowDZ (Math|Interpolation|FInterpTo (V FBrowDZ) (select _hold (V TBrowDZ) 0.0) Delta _sp))
  (set FBrowSkew (Math|Interpolation|FInterpTo (V FBrowSkew) (select _hold (V TBrowSkew) 0.0) Delta _sp))
  (set BrowK (Math|Interpolation|FInterpTo (V BrowK) (select (or _hold (V RestBrows)) 1.0 0.0) Delta _sp))
  (set FMouthW (Math|Interpolation|FInterpTo (V FMouthW) (select _hold (V TMouthW) 1.0) Delta _sp))
  (set FMouthH (Math|Interpolation|FInterpTo (V FMouthH) (select _hold (V TMouthH) 1.0) Delta _sp))
  (set FCurve (Math|Interpolation|FInterpTo (V FCurve) (select _hold (V TCurve) 0.0) Delta _sp))
  (set FMTilt (Math|Interpolation|FInterpTo (V FMTilt) (select _hold (V TMTilt) 0.0) Delta _sp))
  (set FTint (Math|Interpolation|FInterpTo (V FTint) (select _hold (V TTint) 0.0) Delta _sp))
  (set GW (Math|Interpolation|FInterpTo (V GW) (select _hold 1.0 0.0) Delta (select _hold 10.0 5.0)))
  (bind _busy (or (< (V MvT) 1.0) (< _c (V BusyUntil))))
  (set GK (Math|Interpolation|FInterpTo (V GK) (select _busy 0.0 1.0) Delta 10.0))
  (CallFunction|GestTick)
  (CallFunction|FaceApply)
  (if (and (not _hold) (> _c (+ (V EmUntil) 1.0)))
    (CallFunction|EmoteStop)))
```

`_hold` is false for `neutral` (its `EmUntil` is now), so `BrowK`'s `(or _hold RestBrows)` already shrinks a browless robot's brows when it goes back to neutral.

**`GestTick`**

```lisp
; T75: the gesture's offsets for the Rig (GX, GZ, GPitch, GRoll, GYaw, GScale), which Event Tick adds.
; The pose and the waves are scaled by GW (the hold, eased) and GK (zero while the robot moves or acts).
; A burst wave (secs > 0) fades out over its secs, so it never stops with a jerk.
(fn GestTick ()
  (bind _t (- (V Clock) (V EmStart)))
  (bind _e1 (select (> (V G1Secs) 0.0) (Math|Float|Clamp(Float) :Value (- 1.0 (/ _t (Math|Float|Max(Float) (V G1Secs) 0.01))) :Min 0.0 :Max 1.0) 1.0))
  (bind _s1 (Math|Trig|Sin(Radians) (* 6.28318 (* (V G1Hz) _t))))
  (bind _v1 (select (V G1On) (* _e1 (* (V G1Amp) (select (V G1Abs) (Math|Float|Absolute(Float) _s1) _s1))) 0.0))
  (bind _e2 (select (> (V G2Secs) 0.0) (Math|Float|Clamp(Float) :Value (- 1.0 (/ _t (Math|Float|Max(Float) (V G2Secs) 0.01))) :Min 0.0 :Max 1.0) 1.0))
  (bind _s2 (Math|Trig|Sin(Radians) (* 6.28318 (* (V G2Hz) _t))))
  (bind _v2 (select (V G2On) (* _e2 (* (V G2Amp) (select (V G2Abs) (Math|Float|Absolute(Float) _s2) _s2))) 0.0))
  (bind _k (* (V GW) (V GK)))
  (set GX (* _k (+ (V GPoseX) (+ (select (== (V G1Ch) 0) _v1 0.0) (select (== (V G2Ch) 0) _v2 0.0)))))
  (set GZ (* _k (+ (V GPoseZ) (+ (select (== (V G1Ch) 1) _v1 0.0) (select (== (V G2Ch) 1) _v2 0.0)))))
  (set GPitch (* _k (+ (V GPosePitch) (+ (select (== (V G1Ch) 2) _v1 0.0) (select (== (V G2Ch) 2) _v2 0.0)))))
  (set GRoll (* _k (+ (V GPoseRoll) (+ (select (== (V G1Ch) 3) _v1 0.0) (select (== (V G2Ch) 3) _v2 0.0)))))
  (set GYaw (* _k (+ (V GPoseYaw) (+ (select (== (V G1Ch) 4) _v1 0.0) (select (== (V G2Ch) 4) _v2 0.0)))))
  (set GScale (* _k (+ (V GPoseScale) (+ (select (== (V G1Ch) 5) _v1 0.0) (select (== (V G2Ch) 5) _v2 0.0))))))
```

**`PosePart` and `FaceApply`**

```lisp
; T75: puts a face part at Loc, turned as Rot plus Roll (about its own forward axis), at Scale.
(fn PosePart (P Loc Rot Roll Scale)
  (Transformation|SetRelativeLocation :self P :NewLocation Loc)
  (Transformation|SetRelativeRotation :self P :NewRotation (Math|Rotator|MakeRotator :Roll (+ (.roll Rot) Roll) :Pitch (.pitch Rot) :Yaw (.yaw Rot)))
  (Transformation|SetRelativeScale3D :self P :NewScale3D Scale))
```

```lisp
; T75: puts the face where the eased values (F...) say: the eyes, the new brows, the mouth's tilt and its
; size before the talking stretch (MouthNow, which Event Tick reads), and the tint on the parts that glow.
; Each eye's tilt is mirrored by its side, so + eye_tilt tips both inner corners down.
(fn FaceApply ()
  (CallFunction|PosePart :P (V PEyeL) :Loc (+ (V RestEyeLocL) (Math|Vector|MakeVector :X 0.0 :Y (- 0.0 (V FEyeDX)) :Z (V FEyeDZ))) :Rot (V RestEyeRotL) :Roll (* (V TiltSign) (* (V SideEyeL) (V FEyeTilt))) :Scale (Math|Vector|MakeVector :X (.x (V RestEyeScaleL)) :Y (* (.y (V RestEyeScaleL)) (V FEyeW)) :Z (* (.z (V RestEyeScaleL)) (V FEyeH))))
  (CallFunction|PosePart :P (V PEyeR) :Loc (+ (V RestEyeLocR) (Math|Vector|MakeVector :X 0.0 :Y (- 0.0 (V FEyeDX)) :Z (V FEyeDZ))) :Rot (V RestEyeRotR) :Roll (* (V TiltSign) (* (V SideEyeR) (V FEyeTilt))) :Scale (Math|Vector|MakeVector :X (.x (V RestEyeScaleR)) :Y (* (.y (V RestEyeScaleR)) (V FEyeW)) :Z (* (.z (V RestEyeScaleR)) (V FEyeH))))
  (CallFunction|PosePart :P (V EmBrowL) :Loc (+ (V RestBrowLocL) (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z (+ (V FBrowDZ) (* 0.5 (+ (V FEyeDZ) (* (V SideBrowL) (V FBrowSkew))))))) :Rot (Math|Rotator|MakeRotator :Roll 0.0 :Pitch (.pitch (V RestBrowRotL)) :Yaw (.yaw (V RestBrowRotL))) :Roll (V FBrowRL) :Scale (Math|Vector|MakeVector :X (.x (V RestBrowScaleL)) :Y (* (.y (V RestBrowScaleL)) (V BrowK)) :Z (.z (V RestBrowScaleL))))
  (CallFunction|PosePart :P (V EmBrowR) :Loc (+ (V RestBrowLocR) (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z (+ (V FBrowDZ) (* 0.5 (+ (V FEyeDZ) (* (V SideBrowR) (V FBrowSkew))))))) :Rot (Math|Rotator|MakeRotator :Roll 0.0 :Pitch (.pitch (V RestBrowRotR)) :Yaw (.yaw (V RestBrowRotR))) :Roll (V FBrowRR) :Scale (Math|Vector|MakeVector :X (.x (V RestBrowScaleR)) :Y (* (.y (V RestBrowScaleR)) (V BrowK)) :Z (.z (V RestBrowScaleR))))
  (Transformation|SetRelativeRotation :self (V PMouth) :NewRotation (Math|Rotator|MakeRotator :Roll (+ (.roll (V RestMouthRot)) (* (- 0.0 (V TiltSign)) (V FMTilt))) :Pitch (.pitch (V RestMouthRot)) :Yaw (.yaw (V RestMouthRot))))
  (set MouthNow (Math|Vector|MakeVector :X (.x (V MouthRest)) :Y (* (.y (V MouthRest)) (V FMouthW)) :Z (* (.z (V MouthRest)) (V FMouthH))))
  (if (or (> (V FTint) 0.002) (V TintDirty))
    (set TintDirty (> (V FTint) 0.002))
    (bind _col (Math|Vector|Lerp(Vector) :A (V LedColor) :B (V TintCol) :Alpha (V FTint)))
    (if (V TintEyes)
      (Rendering|Material|SetVectorParameterValueonMaterials :self (V PEyeL) :ParameterName "Color" :ParameterValue _col)
      (Rendering|Material|SetVectorParameterValueonMaterials :self (V PEyeR) :ParameterName "Color" :ParameterValue _col))
    (if (V TintMouth)
      (Rendering|Material|SetVectorParameterValueonMaterials :self (V PMouth) :ParameterName "Color" :ParameterValue _col)
      (Rendering|Material|SetVectorParameterValueonMaterials :self (V MouthCL) :ParameterName "Color" :ParameterValue _col)
      (Rendering|Material|SetVectorParameterValueonMaterials :self (V MouthCR) :ParameterName "Color" :ParameterValue _col))
    (if (V TintBrows)
      (Rendering|Material|SetVectorParameterValueonMaterials :self (V EmBrowL) :ParameterName "Color" :ParameterValue _col)
      (Rendering|Material|SetVectorParameterValueonMaterials :self (V EmBrowR) :ParameterName "Color" :ParameterValue _col))))
```

- The eyes slide along the screen's y only; at ±4 cm the curve's depth change is under 0.5 cm. If an eye sinks into the screen on a close-up, add `(- 0.0 (/ (* dy dy) (* 2.0 (V FaceR))))` to its x as `PlaceCorners` does.
- The tint writes only while it is on, plus one last write when it fades out (it writes `LedColor` back). With no tint, `FaceApply` writes no material.
- On the cut, `EmoteStop` runs first and puts `LedColor` back, then `SetCut` darkens the eyes as before.

**`PlaceCorners`**

```lisp
; T75: the mouth's two corner bars, bent up into a smile (mouth_curve > 0) or down into a frown (< 0),
; turned with the mouth's tilt. Event Tick calls it after it sizes the mouth: W is the mouth's width scale
; with the talking stretch. Corners are as thick as the resting mouth, so an open mouth doesn't grow teeth.
; The viewer's right is the robot's -Y (it faces the camera). MouthCR is the viewer's-right corner.
(fn PlaceCorners (W)
  (if (not (V FaceReady))
    (return))
  (bind _show (and (V EmOn) (> (Math|Float|Absolute(Float) (V FCurve)) 1.5)))
  (Rendering|SetVisibility :self (V MouthCL) :bNewVisibility _show :bPropagateToChildren false)
  (Rendering|SetVisibility :self (V MouthCR) :bNewVisibility _show :bPropagateToChildren false)
  (if (not _show)
    (return))
  (bind _h (* W 50.0))
  (bind _len (* (V CornerFrac) (* 2.0 _h)))
  (bind _ca (Math|Trig|Cos(Degrees) (V FCurve)))
  (bind _sa (Math|Trig|Sin(Degrees) (V FCurve)))
  (bind _ct (Math|Trig|Cos(Degrees) (V FMTilt)))
  (bind _st (Math|Trig|Sin(Degrees) (V FMTilt)))
  (bind _du (+ _h (* 0.5 (* _len _ca))))
  (bind _dz (* 0.5 (* _len _sa)))
  (bind _ru (- (* _du _ct) (* _dz _st)))
  (bind _rz (+ (* _du _st) (* _dz _ct)))
  (bind _lu (- (* (- 0.0 _du) _ct) (* _dz _st)))
  (bind _lz (+ (* (- 0.0 _du) _st) (* _dz _ct)))
  (bind _m (V RestMouthLoc))
  (bind _r (V RestMouthRot))
  (bind _sc (Math|Vector|MakeVector :X (.x (V MouthNow)) :Y (/ _len 100.0) :Z (.z (V MouthRest))))
  (Transformation|SetRelativeLocation :self (V MouthCR) :NewLocation (Math|Vector|MakeVector :X (- (+ (.x _m) (V CornerX)) (/ (* _ru _ru) (* 2.0 (V FaceR)))) :Y (- (.y _m) _ru) :Z (+ (.z _m) _rz)))
  (Transformation|SetRelativeRotation :self (V MouthCR) :NewRotation (Math|Rotator|MakeRotator :Roll (+ (.roll _r) (* (- 0.0 (V TiltSign)) (+ (V FMTilt) (V FCurve)))) :Pitch (.pitch _r) :Yaw (.yaw _r)))
  (Transformation|SetRelativeScale3D :self (V MouthCR) :NewScale3D _sc)
  (Transformation|SetRelativeLocation :self (V MouthCL) :NewLocation (Math|Vector|MakeVector :X (- (+ (.x _m) (V CornerX)) (/ (* _lu _lu) (* 2.0 (V FaceR)))) :Y (- (.y _m) _lu) :Z (+ (.z _m) _lz)))
  (Transformation|SetRelativeRotation :self (V MouthCL) :NewRotation (Math|Rotator|MakeRotator :Roll (+ (.roll _r) (* (- 0.0 (V TiltSign)) (- (V FMTilt) (V FCurve)))) :Pitch (.pitch _r) :Yaw (.yaw _r)))
  (Transformation|SetRelativeScale3D :self (V MouthCL) :NewScale3D _sc))
```

- The geometry: in the face's plane, with `u` toward the viewer's right and `z` up, the viewer's-right corner's middle sits at `(h + len/2 · cos a, len/2 · sin a)` from the mouth's center, the left one at `(−(h + len/2 · cos a), len/2 · sin a)`, both turned by the tilt `t`. A bar along angle `θ` in that plane has roll `−TiltSign · θ`: the right corner's angle is `t + a`, the left's `t − a`, the mouth's own `t`. The 2D mock in part 1 used the same formulas.
- `x` steps back by `u² / 2R` so the corners follow the curved screen (`FaceR` 35 cm, half of the 70 cm head), plus `CornerX` 0.4 cm forward so they never sink into it. Tune both on a close-up. The new heads' screens may have another radius (part 2g).
- If `RestMouthRot.roll` isn't 0 on a new head, the corners' positions don't follow it; say so under "Findings" (T46's mouth has none).

**`EmoteStop`**

```lisp
; T75: ends any emotion at once and puts the face back at rest. ResetLook, SetCut and SetPersona call it
; first; EmoteTick calls it once the face has eased back. In the construction script it only clears state.
(fn EmoteStop ()
  (set EmOn false)
  (set EmUntil 0.0)
  (set GW 0.0)
  (set GK 0.0)
  (set GX 0.0)
  (set GZ 0.0)
  (set GPitch 0.0)
  (set GRoll 0.0)
  (set GYaw 0.0)
  (set GScale 0.0)
  (if (V FaceReady)
    (Transformation|SetRelativeScale3D :self (Variables|Default|GetRig) :NewScale3D (V RigScale0)))
  (if (not (and (V HasRest) (V FaceReady)))
    (return))
  (set FEyeW 1.0)
  (set FEyeH 1.0)
  (set FEyeDZ 0.0)
  (set FEyeDX 0.0)
  (set FEyeTilt 0.0)
  (set FBrowRL (V RestBrowRL))
  (set FBrowRR (V RestBrowRR))
  (set FBrowDZ 0.0)
  (set FBrowSkew 0.0)
  (set BrowK (select (V RestBrows) 1.0 0.0))
  (set FMouthW 1.0)
  (set FMouthH 1.0)
  (set FCurve 0.0)
  (set FMTilt 0.0)
  (set FTint 0.0)
  (CallFunction|FaceApply)
  (CallFunction|FaceRestVis))
```

**`EmoteTestInit`**

```lisp
; T75: the emote_test switch (Local/switches.json). On: each robot cycles through every emotion by itself,
; EmTestStep (4) seconds each, starting at emotion Seat * 2 + 1 so the five robots always differ.
; A missing file or field means off. BeginPlay calls it.
(fn EmoteTestInit ()
  (set EmTest false)
  (bind (_so _sok) (Json|LoadJsonfromFile (Utilities|Struct|MakeFilePath (cat (Utilities|Paths|GetProjectDirectory) "Local/switches.json"))))
  (if (not _sok)
    (return))
  (bind _hf (Json|HasField _so "emote_test"))
  (if (not _hf)
    (return))
  (bind _sf (Json|GetField _so "emote_test"))
  (set EmTest _sf)
  (if (not (V EmTest))
    (return))
  (CallFunction|LoadEmotes)
  (if (== (len (V EmIds)) 0)
    (set EmTest false)
    (return))
  (set EmTestIdx (+ (* (V Seat) 2) 1))
  (if (>= (V EmTestIdx) (len (V EmIds)))
    (set EmTestIdx (V Seat)))
  (if (or (< (V EmTestIdx) 0) (>= (V EmTestIdx) (len (V EmIds))))
    (set EmTestIdx 0))
  (set EmTestNext (+ (V Clock) 1.5))
  (print (cat "NHOS: EMOTE TEST on seat=" (cat (str (V Seat)) (cat " start=" (cat (get (V EmIds) (V EmTestIdx)) (cat " ids=" (str (len (V EmIds))))))))))
```

### 2f. The changed graphs

Each is the pushed file with the lines below added. The copies here are `c08012d`'s; if a later task changed a file, add T75's lines to the pushed version by the text named.

**`EventGraph`** (T79 rewrites it for the hover: apply the same changes to its version)

1. **BeginPlay:** after `(CallFunction|InitHome)` in `(event EventBeginPlay`, add two lines:

   ```lisp
     ; T75: the emotion parts, then the emote_test switch.
     (CallFunction|FaceSetup)
     (CallFunction|EmoteTestInit))
   ```

   (the `)` that closed the event moves to the new last line).
2. **Event Tick, the `else` branch** (the robot isn't cut). Replace the two `Rig` lines, at `c08012d` lines 26 and 27:

   ```lisp
         (Transformation|SetRelativeLocation :self (Variables|Default|GetRig) :NewLocation (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z _z))
         (Transformation|SetRelativeRotation :self (Variables|Default|GetRig) :NewRotation (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw _yaw))
   ```

   with three:

   ```lisp
         ; T75: the gesture's offsets (GestTick) ride on the bob, the talking bounce, the cheer and the shake.
         (Transformation|SetRelativeLocation :self (Variables|Default|GetRig) :NewLocation (Math|Vector|MakeVector :X (V GX) :Y 0.0 :Z (+ _z (V GZ))))
         (Transformation|SetRelativeRotation :self (Variables|Default|GetRig) :NewRotation (Math|Rotator|MakeRotator :Roll (V GRoll) :Pitch (V GPitch) :Yaw (+ _yaw (V GYaw))))
         (Transformation|SetRelativeScale3D :self (Variables|Default|GetRig) :NewScale3D (* (V RigScale0) (+ 1.0 (V GScale))))
   ```

3. **Event Tick, the mouth** (`c08012d` line 32). Replace

   ```lisp
         (Transformation|SetRelativeScale3D :self (Variables|Default|GetMouth) :NewScale3D (Math|Vector|MakeVector :X 0.02 :Y (+ 0.1 (* _m 0.12)) :Z (+ 0.02 (* _m 0.07))))
   ```

   with

   ```lisp
         ; T75: the talking stretch rides on the emotion's mouth (MouthNow), in units of the resting mouth.
         ; With no emotion, MouthNow is MouthRest (0.02, 0.1, 0.02), so this is T46's stretch exactly.
         (bind _mw (+ (.y (V MouthNow)) (* _m (* 1.2 (.y (V MouthRest))))))
         (Transformation|SetRelativeScale3D :self (Variables|Default|GetMouth) :NewScale3D (Math|Vector|MakeVector :X (.x (V MouthNow)) :Y _mw :Z (+ (.z (V MouthNow)) (* _m (* 3.5 (.z (V MouthRest)))))))
         (CallFunction|PlaceCorners :W _mw)
   ```

   - At rest: `Y = 0.1 + m · 0.12` and `Z = 0.02 + m · 0.07`, T46's numbers. `1.2` and `3.5` are T46's stretch divided by the resting size (`0.12 / 0.1`, `0.07 / 0.02`).
   - If T79 or T80 changed the stretch (other numbers, or one line per head), set `MouthRest` in `FaceParts` to each head's resting scale and put each head's stretch in this form; say so under "Findings".
   - The cut branch doesn't change: it never writes the `Rig`'s scale, and `SetCut` runs `EmoteStop`, which puts it back.

**`TickActs`**: add the last line of the function, after the queue block that ends `(CallFunction|StartAct :Verb (V CurVerb) :Loc (V CurLoc) :Prop (V CurProp) :Bot (V CurBot))))`:

```lisp
  ; T75: the emotion's face and gesture, and the emote_test cycle.
  (CallFunction|EmoteTick :Delta Delta))
```

(the queue block loses one closing paren to the new line). `TickActs` runs before Event Tick writes the `Rig`, so the gesture is this frame's.

**`SetPersona`**: two lines.

- First line of the body, before `(Variables|Default|SetPersonaId Id)`: `  (CallFunction|EmoteStop)` (with the comment `  ; T75: end any emotion on the old face first.`). It must come before the id changes, so `FaceRestVis` puts back the old persona's parts.
- Right before the last line, `  (CallFunction|ResetLook))`: `  (CallFunction|FaceRest)` (comment: `  ; T75: read the new persona's resting face, after the eyes are set.`).

**`ResetLook`**: first line of the body, before `(Variables|Default|SetIsCut false)`:

```lisp
  ; T75: any emotion ends, and the face is at rest (Restart, a new persona).
  (CallFunction|EmoteStop)
```

**`SetLit`**: right before `  (if On` (its last block), add:

```lisp
  ; T75: the new brows and corner bars glow like the eyes. LitOn lets PartLook match it later.
  (set LitOn On)
  (if (V FaceReady)
    (Rendering|Material|SetScalarParameterValueonMaterials :self (V EmBrowL) :ParameterName "Glow" :ParameterValue (select On 10.0 3.0))
    (Rendering|Material|SetScalarParameterValueonMaterials :self (V EmBrowR) :ParameterName "Glow" :ParameterValue (select On 10.0 3.0))
    (Rendering|Material|SetScalarParameterValueonMaterials :self (V MouthCL) :ParameterName "Glow" :ParameterValue (select On 10.0 3.0))
    (Rendering|Material|SetScalarParameterValueonMaterials :self (V MouthCR) :ParameterName "Glow" :ParameterValue (select On 10.0 3.0)))
```

`SetLit` runs from `ResetLook`, which the construction script reaches; `FaceReady` is false there, so nothing touches a part that doesn't exist. A clay brow (decision on question 2) has no `Glow`; setting it does nothing.

**`SetCut`**: first line of the body, before `(CallFunction|DropAll)`:

```lisp
  ; T75: a cut robot stops emoting, and its face is at rest before it goes dark.
  (CallFunction|EmoteStop)
```

Save the 20 new files and the six changed ones in `Graphs/BP_Robot/`, as written.

### 2g. `FaceParts` after T79 and T80

T79 keeps "T46's LED eyes and mouth" on the shared head and T80 makes two new heads, so `FaceParts` picks each head's parts by persona. From the part 0 survey, per head:

| Head | Personas | Parts to point at | Flags |
|---|---|---|---|
| The shared round screen face (T79) | `visionary`, `worrier`, `overclocker` | T79's eyes and mouth (expected `EyeL`, `EyeR`, `Mouth`). `RestBrows` and `PBrowL`/`PBrowR` as T79 left the worrier's and overclocker's brows; for `visionary`, a hidden brow pair to copy (the worrier's). | `BrowMat` and `CornerMat` `LedMat`, all three tints on, `FaceR` the screen's radius |
| Meta's doll head (T80) | `copycat` | The eyes behind the glasses, the mouth below them. `PSmile` and `HasSmile` if T80 kept a fixed smile beside a posable mouth; otherwise `HasSmile` false and `PMouth` the mouth itself. Brows: a hidden pair above the glasses to copy, or the screen face's pair with its height fixed in `FaceRest` | `BrowMat`: question 2 (recommended `ClayMat`), `CornerMat`: the mouth's own material, `TintEyes` on, `TintMouth` and `TintBrows` off, `LedColor` Meta's eye color |
| My cardboard box (T80) | `human` | The eyes behind the slots (keep each eye inside its slot: clamp `eye_dx` and `eye_dz` in `FaceApply` with `Math|Float|Clamp(Float)` to the slot's size if they peek out), the drawn mouth (question 1) | `BrowMat`: question 2 (recommended a black marker material, or `ClayMat`), `CornerMat`: the drawn mouth's material, every tint off |

- The DSL form: `(bind _m (streq (V PersonaId) "copycat"))`, `(bind _h (streq (V PersonaId) "human"))`, then `(set PEyeL (select _m (Variables|Default|GetMetaEyeL) (select _h (Variables|Default|GetBoxEyeL) (Variables|Default|GetEyeL))))` and the same for each part and flag, with the names the survey found. Every other function stays as written.
- If a head's eyes are not engine shapes scaled from 100 cm, the brows' `* 50.0` in `FaceRest` is wrong for it: use half the eye's bounding height instead (from the survey) and say so.
- **If question 1's answer is "keep the drawn smile fixed":** for the box, point `PMouth` at a hidden spare (or set `MouthRest` and skip the mouth lines with a `MouthFixed` flag around the `PMouth` lines in `FaceApply`, `FaceEmoteVis` and `PlaceCorners`), and say in "Findings" that the box shows emotions with its eyes, brows and gesture only.

## 3. The `emote_test` switch

**`Docs/switches.example.json`**: add a field after `"error_test": ""`, and a sentence at the end of `_readme`.

- The field (the line before gets a comma): `"emote_test": false`
- The `_readme` sentence, appended after "... Set it back to empty before a person plays.": `emote_test (T75): every robot cycles through every emotion in Content/NHOS/Data/emotes.json by itself from BeginPlay, 4 seconds each, each robot starting at a different one, with no LLM and no show needed, so the faces can be screenshot. It is read once at BeginPlay. Set it back to false before a person plays.`

**Where the game reads it:** `BP_Robot.EmoteTestInit` (2e), called from Event BeginPlay in `BP_Robot`'s `EventGraph` (2f), reads `<project>/Local/switches.json` (`Utilities|Paths|GetProjectDirectory`, the same path `BPC_LinePlayer.LoadPacing` reads `fast_lines` from). Each robot reads it for itself, so `BP_Show` doesn't change. A packaged build reads `Packaged/Windows/AIMegaJam2026/Local/switches.json`, like the other switches.

## 4. `Tools/check_prompts.py`

Tried on a scratch copy of `c08012d` with the draft of part 1: `--offline` exits 0. Each broken case below fails with the line shown (exit 1): no `neutral`; a posed `neutral` ("neutral is the resting face, so eye_w must be 1"); a face field missing; a gesture not in `gestures` (and the gesture it replaced reported unused); `mouth_h` 6; a wave with `ch` "y"; three waves; a gesture no emotion uses; an id twice (and its word twice); a tint of two numbers; a hold of 0; a word of two words. With `emotes.json` deleted: `FAIL file: emotes.json: missing`.

**a. The docstring.** Before `Exit code 0 means the files are valid and every reply passed its checks.`, after the "No Director (T55)" paragraph (and any paragraph T57 to T69 added there):

```
Emotions (T75): the file check reads emotes.json, the emotions each robot can
show (BP_Robot.Emote). 'neutral' is there and is the resting face (every face
value at rest, gesture none, hold 0); every emotion has id, word, face, gesture
and hold; ids and words are unique; each face value is in its range in
EMOTE_FACE (a mouth always shows, and never a screaming one); and each gesture
is 'none' or one in 'gestures', whose pose and waves use only the channels in
GESTURE_CHANNELS. A gesture no emotion uses fails too.
```

**b. The code**, a new block right before `def check_files(errors: list[str]):` (line 594 at `c08012d`):

```python
# T75: emotes.json, the emotions BP_Robot.Emote shows. Every field here is one the robot reads.
EMOTE_FIELDS = ["id", "word", "face", "gesture", "hold"]
EMOTE_FACE = {  # field: (lowest, highest, its value in neutral, the resting face)
    "eye_w": (0.3, 1.6, 1), "eye_h": (0.3, 1.6, 1),
    "eye_dz": (-4, 4, 0), "eye_dx": (-4, 4, 0), "eye_tilt": (-30, 30, 0),
    "brow_angle": (-35, 35, 0), "brow_dz": (-5, 8, 0), "brow_skew": (-6, 6, 0),
    "mouth_w": (0.4, 1.6, 1), "mouth_h": (0.8, 4.0, 1),  # a mouth always shows, and never a screaming one
    "mouth_curve": (-35, 35, 0), "mouth_tilt": (-20, 20, 0), "tint_mix": (0, 1, 0),
}
GESTURE_CHANNELS = {"x": 12, "z": 20, "pitch": 15, "roll": 15, "yaw": 30, "scale": 0.1}  # largest pose value or wave amp
EMOTE_HOLD = (0.5, 6.0)
EMOTE_ID = re.compile(r"[a-z][a-z_]*")


def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def gesture_problems(name, g) -> list[str]:
    where = f"emotes.json: gesture {name!r}"
    if name == "none" or not EMOTE_ID.fullmatch(name):
        return [f"{where}: a gesture's name is lowercase letters and _, and never 'none'"]
    if not isinstance(g, dict) or set(g) != {"pose", "waves"}:
        return [f"{where}: needs pose and waves, and nothing else"]
    errs = []
    pose = g["pose"]
    if not isinstance(pose, dict) or set(pose) != set(GESTURE_CHANNELS):
        errs.append(f"{where}: pose needs {', '.join(GESTURE_CHANNELS)}, and nothing else")
    else:
        for ch, v in pose.items():
            if not _num(v) or abs(v) > GESTURE_CHANNELS[ch]:
                errs.append(f"{where}: pose {ch} = {v!r} is outside -{GESTURE_CHANNELS[ch]} to {GESTURE_CHANNELS[ch]}")
    waves = g["waves"]
    if not isinstance(waves, list) or len(waves) > 2:
        return errs + [f"{where}: waves must be a list of at most 2 (the robot reads two)"]
    for i, w in enumerate(waves, 1):
        ww = f"{where}: wave {i}"
        if not isinstance(w, dict) or set(w) != {"ch", "amp", "hz", "secs", "abs"}:
            errs.append(f"{ww} needs ch, amp, hz, secs and abs, and nothing else")
            continue
        if w["ch"] not in GESTURE_CHANNELS:
            errs.append(f"{ww}: ch {w['ch']!r} is not one of {', '.join(GESTURE_CHANNELS)}")
        elif not _num(w["amp"]) or not 0 < w["amp"] <= GESTURE_CHANNELS[w["ch"]]:
            errs.append(f"{ww}: amp {w['amp']!r} must be above 0 and at most {GESTURE_CHANNELS[w['ch']]} for {w['ch']}")
        if not _num(w["hz"]) or not 0.1 <= w["hz"] <= 14:
            errs.append(f"{ww}: hz {w['hz']!r} must be 0.1 to 14")
        if not _num(w["secs"]) or not 0 <= w["secs"] <= 3:
            errs.append(f"{ww}: secs {w['secs']!r} must be 0 (the whole hold) to 3")
        if not isinstance(w["abs"], bool):
            errs.append(f"{ww}: abs must be true or false")
    return errs


def emote_problems(em) -> list[str]:
    """T75: emotes.json holds the emotions each robot can show, and the gestures they use."""
    if not isinstance(em, dict):
        return ["emotes.json: must be an object with _readme, emotes and gestures"]
    errs = []
    if not is_lines(em.get("_readme")):
        errs.append("emotes.json: _readme must be a list of lines")
    gestures = em.get("gestures")
    if not isinstance(gestures, dict) or not gestures:
        errs.append("emotes.json: gestures must be an object of named gestures")
        gestures = {}
    for name, g in gestures.items():
        errs.extend(gesture_problems(name, g))
    emotes = em.get("emotes")
    if not isinstance(emotes, list) or not emotes:
        return errs + ["emotes.json: emotes must be a list of emotions"]
    ids, words, used = [], [], set()
    for e in emotes:
        if not isinstance(e, dict):
            errs.append("emotes.json: every emotion must be an object")
            continue
        eid = e.get("id")
        where = f"emotes.json: emotion {eid!r}"
        if set(e) != set(EMOTE_FIELDS):
            errs.append(f"{where} needs {', '.join(EMOTE_FIELDS)}, and nothing else")
        if not isinstance(eid, str) or not EMOTE_ID.fullmatch(eid):
            errs.append(f"{where}: an id is lowercase letters and _")
        elif eid in ids:
            errs.append(f"{where} is listed twice")
        ids.append(eid)
        word = e.get("word")
        if eid == "neutral":
            if word != "":
                errs.append(f"{where}: neutral's word must be empty (T77 writes nothing for it)")
        elif not isinstance(word, str) or not re.fullmatch(r"[a-z]+", word):
            errs.append(f"{where}: word must be one plain lowercase word, as T77 writes it in the shared log")
        elif word in words:
            errs.append(f"{where}: word {word!r} is used twice")
        else:
            words.append(word)
        face = e.get("face")
        if not isinstance(face, dict) or set(face) != set(EMOTE_FACE) | {"tint"}:
            errs.append(f"{where}: face needs {', '.join(list(EMOTE_FACE) + ['tint'])}, and nothing else")
        else:
            for k, (lo, hi, rest) in EMOTE_FACE.items():
                v = face[k]
                if not _num(v) or not lo <= v <= hi:
                    errs.append(f"{where}: face {k} = {v!r} is outside {lo} to {hi}")
                elif eid == "neutral" and v != rest:
                    errs.append(f"{where}: neutral is the resting face, so {k} must be {rest}")
            t = face["tint"]
            if not (isinstance(t, list) and len(t) == 3 and all(_num(c) and 0 <= c <= 1 for c in t)):
                errs.append(f"{where}: face tint must be [r, g, b], each 0 to 1")
        gesture = e.get("gesture")
        if gesture != "none" and gesture not in gestures:
            errs.append(f"{where}: gesture {gesture!r} is not in gestures (or 'none')")
        used.add(gesture)
        hold = e.get("hold")
        if eid == "neutral":
            if gesture != "none" or hold != 0:
                errs.append(f"{where}: neutral has gesture 'none' and hold 0")
        elif not _num(hold) or not EMOTE_HOLD[0] <= hold <= EMOTE_HOLD[1]:
            errs.append(f"{where}: hold {hold!r} must be {EMOTE_HOLD[0]} to {EMOTE_HOLD[1]} seconds")
    if "neutral" not in ids:
        errs.append("emotes.json: needs 'neutral', the resting face that an empty or unknown id shows")
    for name in gestures:
        if name not in used:
            errs.append(f"emotes.json: gesture {name!r} is used by no emotion; drop it or use it")
    return errs
```

**c. In `check_files`:**

- After `    error_lines = load_json("errors.json", errors)` (line 599): `    emotes = load_json("emotes.json", errors)  # T75`
- After `    errors.extend(prewritten_problems(scenes, errors))` (line 749):

  ```python

      # emotes.json: the emotions each robot can show (T75).
      errors.extend(emote_problems(emotes))
  ```

- The return (line 753) becomes `    return {"llm": llm, "prompts": prompts, "personas": plist, "scenes": scenes, "emotes": emotes}`, so T76 can compare `reply_schema`'s enum with the ids.

**d. The "Files OK" line** (`main`, line 1595 at `c08012d`): `... autoplay.json, props.json and the relay's allow-list` becomes `... autoplay.json, props.json, emotes.json and the relay's allow-list`.

T76 adds the check that `reply_schema`'s `emotion` enum holds exactly these ids; `check_files` now returns `emotes` for it.

## 5. The check

The Done-when: screenshots in PIE (Test for Free, `emote_test` on, the house camera) of each emotion on at least one robot and one frame with all five on different emotions; Claude's judgment under "Findings" with any look-alike pair reworked or dropped; `NHOS: EMOTE` for each emotion and no `LogScript` line; with `emote_test` off, a free autoplay show in a game window reaches `NHOS: SHOW END` with the robots neutral and still acting; `--offline` passes; `emote_test` back to false.

### Run A: every emotion in PIE (`emote_test` on)

`Local/switches.json`: `"emote_test": true`, `"autoplay": false`, `"mode": "free"`, `"fast_lines": false`, every other switch as in `Docs/switches.example.json`.

1. Start PIE in a 1600 × 900 floating window (T33). Click **Test for Free**, then let the show reach Scene Prep and stay there (don't press Start the scene): the five robots stand on their marks with their personas, under the house camera. Each robot changes emotion every 4 s.
2. **The log** (`Saved/Logs/AIMegaJam2026.log`) right after BeginPlay:

   ```
   NHOS: EMOTE loaded 12 emotions                                   (five times)
   NHOS: EMOTE TEST on seat=0 start=happy ids=12
   NHOS: EMOTE TEST on seat=1 start=angry ids=12
   NHOS: EMOTE TEST on seat=2 start=scared ids=12
   NHOS: EMOTE TEST on seat=3 start=confused ids=12
   NHOS: EMOTE TEST on seat=4 start=suspicious ids=12
   NHOS: EMOTE 0 happy persona=<id> gesture=bounce                  (then one line per robot every 4 s)
   ```

   (`start=` follows the file's order, if the rework changed it.) After the cast draw, the `persona=` fields change to the drawn personas.
3. **The screenshots** (`SlateInspectorToolset.Screenshot` of the PIE window, as T33 and T60 did; keep them in `Saved/T75/shots/`, not in git):
   - **`cycle_00.png` to `cycle_11.png`:** 12 frames, one 1.6 s after each round of `NHOS: EMOTE` lines (the face has settled, the hold has 1.4 s left). Each frame shows five different emotions, and the 12 frames show every emotion on every robot. `cycle_00.png` is the "all five on different emotions" frame.
   - **`burst_bounce_*.png`, `burst_shake_*.png`, `burst_jolt_*.png`:** four frames 0.25 s apart, starting right after the `NHOS: EMOTE` line for that gesture, to see the move (the bursts are over in 1.35, 1 and 0.36 s).
   - **The close-ups, one face per emotion:** move the house camera in the PIE world in front of one robot's face. In an editor Python script (as T46 ran one through the console's `py` command): `w = unreal.UnrealEditorSubsystem().get_game_world()`, `cam = unreal.GameplayStatics.get_all_actors_of_class(w, unreal.CameraActor)[0]`, keep `cam.get_actor_transform()`, then `cam.set_actor_location_and_rotation(face + forward * 170, look_back_at_face, False, False)` (the face about 115 cm up the robot; `unreal.MathLibrary.find_look_at_rotation`). Take `close_<seat>_<id>.png` for 12 rounds on one robot of each head (the round screen face, Meta, my box). Put the camera back after; the robots' own facing uses the camera's place from BeginPlay (`CamLoc`), so it doesn't change. If the PIE camera can't be moved, crop the full-size house-camera frames instead (T19's `Saved/T19/resize.ps1`).
4. **The checks in the log** after a full cycle (48 s):

   ```bash
   grep -oE "NHOS: EMOTE [0-9-]+ [a-z_]+" Saved/Logs/AIMegaJam2026.log | awk '{print $4}' | sort | uniq -c
   grep -c "NHOS: EMOTE unknown" Saved/Logs/AIMegaJam2026.log
   grep -c "LogScript" Saved/Logs/AIMegaJam2026.log
   ```

   The first lists all 12 ids (each at least 5 times); the second and third print 0. Count only this PIE run's lines (from its `NHOS: EMOTE loaded`).

### Run A2: the edges, in the same PIE

From an editor Python script on the PIE robots (`w` as above; the robots are `unreal.GameplayStatics.get_all_actors_of_class(w, unreal.load_class(None, "/Game/NHOS/Stage/BP_Robot.BP_Robot_C"))`, each with `call_method`):

1. `bot.call_method("Emote", ("bogus",))` prints `NHOS: EMOTE unknown bogus`, then `NHOS: EMOTE <seat> neutral persona=<id> gesture=none`, and the face eases back to rest.
2. `bot.call_method("Emote", ("",))` prints the `neutral` line only, with no `unknown`.
3. **Talking on top:** `bot.call_method("Emote", ("worried",))`, then `bot.call_method("SetLit", (True,))` (2.6 s of talking). A close-up (`talk_worried.png`) shows the worried mouth stretching as it talks and the worried brows and eyes holding.
4. **Meta's smile:** on the copycat, `Emote("happy")`: the `Smile` (or T80's fixed smile) is gone and the mouth bar curves; 4 s later the `Smile` is back (`close_copycat_happy.png`, `close_copycat_rest.png`).
5. **A cut robot:** `bot.call_method("SetCut", ("TEST",))`, then `bot.call_method("Emote", ("happy",))`: no `NHOS: EMOTE` line for that seat, the test cycle stops for it, it tips over gray as before, its brows and corners hidden.

Stop PIE. Every `LogScript` count is still 0.

### Run B: a free autoplay show with `emote_test` off (a game window, the saved assets)

`Local/switches.json`: `"emote_test": false`, `"autoplay": true`, `"mode": "free"`, `"fast_lines": true`, `"spare_human": false`.

```bash
"E:/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" "C:/Users/Personal/Projects/AIMegaJam2026/AIMegaJam2026.uproject" -game -windowed -ResX=1600 -ResY=900 -log=T75auto.log
```

(the editor must have saved `BP_Robot` first). Then:

```bash
grep -E "NHOS: (SHOW END|ACT )" Saved/Logs/T75auto.log | tail -5
grep -c "NHOS: EMOTE" Saved/Logs/T75auto.log
grep -c "LogScript" Saved/Logs/T75auto.log
```

Expected: `NHOS: SHOW END result=...`, `NHOS: ACT` lines throughout (the robots still move, grab, throw), 0 `EMOTE` lines (nothing calls `Emote` until T77), 0 `LogScript`. Two screenshots of the game window (T30's `Saved/T30/shot.ps1`, `PrintWindow` flag 2): `auto_prep.png` and `auto_scene.png`. Compare them with T80's screenshots: the faces are T80's resting faces, the Anthropic and SpaceXAI bots have their brows, no other bot has brows, and nothing shows a corner bar.

### Run C (optional): gestures while moving

The same as run B with `"emote_test": true`. In frames taken while a robot hops to a mark or grabs, its face shows an emotion but its body doesn't bounce, slump or lean; it picks the gesture up again once it stands. The show still reaches `SHOW END` with no `LogScript`.

### Judge, rework, and close

- Under "## Findings" in `T75.md`, judge each emotion from the house-camera frames as a critical first-time player would: can you name it with no label? Name any two that look alike. Check sad, worried and embarrassed first, then worried and scared (part 1, "Why these numbers"). Rework them in `emotes.json` (a face value, a tint or the gesture's data; no graph change), run A again for the reworked ones, or drop one and say so. Every rework is checked by `--offline`.
- Note what only a close-up shows (the brows' slant, the corners' curve), and which emotions carry mostly on their tint or gesture from the house.
- `python Tools/check_prompts.py --offline` passes.
- Set `emote_test`, `autoplay` and `fast_lines` back to false in `Local/switches.json`, and close the game window.

## 6. The commit

`Content/NHOS/Data/emotes.json` (new), `Content/NHOS/Stage/BP_Robot.uasset`, `Docs/switches.example.json`, `Tools/check_prompts.py`, the 20 new files and the 6 changed files in `Graphs/BP_Robot/` (`LoadEmotes`, `FaceParts`, `NewPart`, `AttachPart`, `PartLook`, `FaceSetup`, `FaceRest`, `FaceEmoteVis`, `FaceRestVis`, `Emote`, `ReadFace`, `ReadGesture`, `ReadWave`, `EmoteTick`, `GestTick`, `FaceApply`, `PosePart`, `PlaceCorners`, `EmoteStop`, `EmoteTestInit`; `EventGraph`, `TickActs`, `SetPersona`, `ResetLook`, `SetLit`, `SetCut`), `Docs/tasks/T75.md`, `Docs/Plan.md` (the box), `Docs/DevLog.md`. All are in T75's Touches. Unlock `BP_Robot` after the push.

Under "Findings" in `T75.md`: my person's answers to the two questions, the survey (part 0 step 3), what `FaceParts` points at for each head, any node name that differed from part 0's table, `TiltSign`'s final value, every rework of `emotes.json` and why, and the judgment from the screenshots.

## 7. Knock-on: tell, don't change

- **T76:** reads the ids from `emotes.json`'s `emotes` list (in order) for `reply_schema`'s `emotion` enum; `check_files` returns `emotes` for its check. The ids are lowercase with `_`.
- **T77:** calls `BP_Robot.Emote(Emotion)` from `BPC_LinePlayer.PlayCur` when a line plays; an empty or unknown id is safe (neutral). The `word` field is what it writes as `feels`; `neutral`'s is empty, so it leaves `feels` out. `NHOS: EMOTE` lines carry `persona=`, so its log check can match a line to its robot. A new `Emote` blends from the current face, so lines that come fast never snap.
- **T78:** lists the `emotes` entries by `word` in file order, with `neutral` as the task's "calm" (or another word; `neutral`'s `word` stays empty for T77).
- **T38 (bubbles):** its bubble hangs on the `Label`'s parent, not the `Rig`, so a gesture never moves a bubble. Its `HideBubble` lines in `SetCut` and `ResetLook` sit after `SetLit`; T75's `EmoteStop` lines sit first. No clash.
- **T47 (headpieces):** the `Hat` is on the `Rig`, so it bows, leans and grows with a gesture, as it should. `InitLift` lists only `acc`-tagged parts and the stalk and label, never T75's parts.
- **T57:** `SetPassed` changes only the label; no clash.
- **T34 (the in-show screen) and T70 (the itch.io page):** the five-faces frame from run A is a good still for the page.
