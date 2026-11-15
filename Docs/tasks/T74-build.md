# T74 build sheet: re-shoot the design doc's stage and cast captures

Back to [T74](T74.md) and [the plan](../Plan.md). A PC prep session wrote this on 2026-11-15, without the editor. It is a plan, not a record: nothing in `Content/`, `Graphs/`, `Config/` or the design doc changed. The design doc was read, not changed (Art Inspiration tab rev 33, Stories tab rev 10).

- **Written against `noHumansOnSet` at `8444bc7`** (T79 `ab4da13` and T73 `74533c8` in; T58 landed on top while this was written, `122c4df`, and changes nothing T74 uses). **T80 and T47 run on the Mac now and are not pushed.** Every robot and headpiece call below comes from [T80-build.md](T80-build.md) and [T47-build.md](T47-build.md), not from pushed graphs, and is marked **RE-CHECK**.
- **"not run"** marks every script and call this session could not run (no editor, no doc edit allowed). Run each once, fix what fails, and write what you changed under T74's "## Findings". **"run"** marks what this session did run, with what it printed.
- **Two decisions are my person's, asked in this session (2026-11-15):** the Space saga (`space_plans`) on both Art Inspiration pictures, and re-shoot the stage close-ups too. The rest are listed under "Decisions made for my person".

| File | What it is | Run? |
|---|---|---|
| [T74-build/t74.py](T74-build/t74.py) | The driver, on this PC's Python (standard library only): talks to T74's own editor on port 8011, runs the editor scripts through its console box, captures, crops, composes, writes `Saved/T74/shots/`. | `selftest` run (camera math); the rest not run |
| [T74-build/dress.py](T74-build/dress.py) | Editor Python: dresses `L_Stage` for one card (backdrop, props, a seat's headpiece on each robot, labels hidden) and reports the cameras' inputs to `Saved/T74/dress.json`. Saves nothing. | not run |
| [T74-build/setfov.py](T74-build/setfov.py) | Editor Python: the level viewport's FOV and Game View for a capture. | not run |
| [T74-build/hats_fallback.py](T74-build/hats_fallback.py) | Editor Python, fallback A: the headpieces attached by hand if `SetHeadpiece` can't make its `Hat` outside PIE. | not run |
| [T74-build/crop.ps1](T74-build/crop.ps1) | PowerShell + System.Drawing: crop a capture's middle to W:H, scale to W × H, PNG. | run, on a 2026-11-15 capture |
| [T74-build/cast.ps1](T74-build/cast.ps1) | The cast strip: five close-ups in seat order, each labeled with its provider and its role. | run, on the 2026-11-15 close-ups |
| [T74-build/details.ps1](T74-build/details.ps1) | The stage close-ups picture: the proscenium shot beside the chandelier shot. | run, on the 2026-11-15 close-ups |

No download is needed: the image work is Windows PowerShell 5.1's System.Drawing, and the driver is the standard library of this PC's Python 3.13. (The 2026-11-15 captures used Pillow from a venv in another session's scratchpad. Don't rely on it. Installing Pillow is a download and needs my person's OK first.)

## 0. Re-check before you run anything

1. **T80 and T47 are pushed.** `git fetch`, then `git log --oneline 8444bc7..origin/noHumansOnSet -- Content/NHOS/Stage/BP_Robot.uasset Content/NHOS/Maps/L_Stage.umap Content/NHOS/Data/costumes.json Content/NHOS/Data/scenes.json Graphs/BP_Robot Graphs/BP_Prop Graphs/BP_Backdrop Graphs/BP_StageDirector Content/NHOS/Data/props.json` shows a T80 and a T47 commit. Read `Docs/tasks/T80.md` and `T47.md` "## Findings". T74 depends on both (and on T45 and T48, done). If either is missing, stop.
2. **RE-CHECK `SetHeadpiece`** in the pushed `Graphs/BP_Robot/SetHeadpiece.txt`: its name, its two inputs `(Id Color)` (an id in `costumes.json` and an sRGB hex like `#E3C770`), and the `Hat` variable it fills. `dress.py` step 3 calls `bot.call_method("SetHeadpiece", (id, color))` and reads `Hat`; change those two lines if T47 named them differently. Also read whether T47 tuned a fit (`costumes.json`) or added `on` overrides: nothing to change here, `dress.py` uses what the game uses.
3. **RE-CHECK the seats' costume fields.** `scenes.json`'s 35 seats each have `headpiece` and `color` (T47 part 1b). If they don't, `dress.py` falls back to `Docs/tasks/T47-build/scenes_seats.json` and says so in `dress.json`'s `errors`; that means T47 isn't really in, so stop and ask.
4. **RE-CHECK the robots after T80.** T80 re-places all five robots in `L_Stage` (T80-build part 3). `dress.json` reports each robot's label, persona, place and facing: expect `Robot0` OpenAI (`visionary`) at (−50, −330), `Robot1` Anthropic (`worrier`) at (−12, −165), `Robot2` You (`human`) at (0, 0), `Robot3` SpaceXAI (`overclocker`) at (−12, 165), `Robot4` Meta (`copycat`) at (−50, 330), each facing the house camera. The persona ids are `BP_Robot.SetPersona`'s; if T80 renamed one, fix `SEAT_ORDER` in `dress.py` and `SEAT_KEYS` in `t74.py`. T80 must keep `HeadSocket` on every head (T47 attaches the hat to it) and the `glasses` tag on Anthropic's and Meta's glasses (`hats_fallback.py` uses it).
5. **RE-CHECK what only appears at run time.** Tasks between now and T74 may add parts a robot makes only in PIE: T75 (the face for each emotion: its sheet makes face parts at run time, "never in the construction script"), T77 (emotes), T38 (bubbles, which shouldn't show anyway). If T75's Findings say a resting face looks different once its parts exist (brows, a mouth that isn't the editor's), the editor capture won't match the game. Then take one house shot both ways (editor, and fallback B in PIE) and compare the faces before you choose the route. The props, backdrop and hats come out the same either way.
6. **RE-CHECK the other three Blueprints' sources.** Since `8444bc7`, `git log` on `Graphs/BP_Backdrop/ShowBackdrop.txt` (it must still find the id in `ArtIds` and show `T_Backdrop_<id>`), `Graphs/BP_Prop/SetProp.txt` (a name in `props.json` shows its model) and `Graphs/BP_StageDirector/ResetStage.txt` (still `SetProp` per prop, in `GetAllActorsOfClass` order; T47 adds a bare-headed loop there, which `dress.py` doesn't call). If one changed, compare with part 2's table.
7. **RE-CHECK the doc.** Read both tabs' changes since this sheet (`read` with `{"kind":"view","sinceRev":33}` on the Art Inspiration body and `{"kind":"view","sinceRev":10}` on the Stories body; part 4 has the ids). The blocks in part 1's tables must still be there with the same text; take each block's new `h` and the read's `rev` for the guards. If T80 or T73 changed a caption first, write the new caption from what stands, keeping their words where they still hold. T73's pending Art Inspiration edit (the Chat row of the Components table) is not a picture: leave it.
8. **The editor.** Read every status file in the repo folder's `Agents/status/`. Another session will likely be driving the PC's editor, so T74 opens its own (part 3a). Write `Agents/status/task-T74.md` first, with `- Editor: driving (own editor, port 8011, PID <pid>)`, because other sessions restart the editor by killing every `UnrealEditor.exe`.
9. **The worktree has the assets.** In T74's worktree, `git lfs pull` (it shares the repo folder's LFS store, so it usually fetches nothing), then check one asset isn't a pointer: `head -c 60 Content/NHOS/Stage/BP_Robot.uasset` must not start with `version https://git-lfs`.

## 1. The pictures

The doc's 18 pictures today, and what T74 does with each. "Replace" swaps the picture's block for a new PNG; "Add" inserts a new one. All of today's pictures are JPEGs, so the docs `picture` read refuses them (T74.md); the new ones are PNGs.

### 1a. Art Inspiration (tab `0b64f21d-5f0e`, body `61d7c585-d94a`, read at rev 33)

Full block ids start `m90jp575z84.` (the tab's first id).

| # | Under | Picture block (media id, blob now) | Caption block and its text now | T74 | New caption | Shot |
|---|---|---|---|---|---|---|
| A1 | The bots | `.20321` h `8e00c20e` (`.20322`, `blob/60df0472-0296`) | `.20161` h `ad443ac2`: "The five bots as built on 2026-11-15, in seat order, with their name tags hidden. The castle backdrop and props behind them are older pieces, not yet replaced." | **Replace** | "The five bots as built on `<T74's date>`, front on in seat order, in Space saga costumes: OpenAI as the farm kid (wide-brim hat), Anthropic as the smuggler pilot (dark shades over its own glasses), SpaceXAI as the old desert hermit (hood), Meta as the masked villain (saucepan helmet) and You as the rebel princess (tiara)." | `cast_space_plans.png` |
| A2 | The stage | `.20462` h `1f14810e` (`.20463`, `blob/48e9a3c6-2593`) | `.20323` h `6c81e26f`: "The stage from the house camera, as built on 2026-11-15. The castle backdrop and the shared prop table are older pieces, not yet replaced." | **Replace** | "The stage from the house camera, as built on `<T74's date>`, dressed for the Space saga: its painted desert backdrop, its four props on the Prop Table and the five bots in its costumes." | `house_space_plans.png` (the same blob as S1) |
| A3 | The stage | `.20575` h `42f02906` (`.20576`, `blob/e22ed4d5-91a5`) | `.20464`: "Close up: a cherub at the apron's corner, the horseshoe boxes with their top-hat audience, and the chandelier." | **Replace** (my person's call: it showed the castle backdrop and a pill bot) | unchanged: the words still hold. If the new shot shows no robot or backdrop, still unchanged. | `stage_details_space_plans.png` |
| – | The stage | `.20639` (`.20640`): the set-piece renders | `.20577` | stays | – | – |
| – | Costumes | `.20747` (`.20748`): the 13 headpiece renders | `.20641` | stays, unless T47 changed a model (T47-build: none) | – | – |
| – | Props and backdrops | `.20889` (`.20890`): the 27 prop renders | `.20749` ("The bowl of oranges has no model yet.") | stays, unless a prop model changed since T45 | – | – |
| – | Image 1 to 5 | `.1247`, `.1249`, `.1251`, `.1253`, `.1255`: the mood images | their own headings | stay (they predate the direction, as the tab says) | – | – |

The "Layout" embed (`.12155`) is a drawing, not a picture; it stays.

**New alt text** (the `![alt]` in part 4; check each against the picture before you send it):
- A1: "The five clay bots front on in Space saga costumes, each labeled with its provider: OpenAI's pale-blue teardrop in a straw wide-brim hat, Anthropic's orange body in dark shades, SpaceXAI's lime body in a brown hood, Meta's doll android in a black saucepan helmet, and You, the teal cardboard costume, in a silver tiara"
- A2: the S1 alt text below (one blob for both places).
- A3: "Close-ups on the Space saga stage: a gold cherub at the apron's corner beside the red curtain and the left audience boxes, and the gold chandelier over the house, with the painted desert backdrop behind"

### 1b. Stories (tab `b016d5bc-bb34`, body `1775d40f-9ea4`, read at rev 10)

The tab has one picture per story today, the props strip under its "Props:" line (`.10584` to `.10596`, blobs `940b3319-2f58`, `6be50884-6cb7`, `d4c1488e-7124`, `f3cad793-a6ee`, `c75b1cca-8351`, `db9b901a-3f0a`, `75343af3-e35c`). **They stay.** T74 **adds** one house shot per story right under its "Backdrop (…)" line, so it sits between the backdrop's words and the props line. No caption: the Backdrop line above names the picture, as the "Props:" line names the strip.

| # | Story (card id) | Insert after (Backdrop paragraph) | Shot | Alt text |
|---|---|---|---|---|
| S1 | Who Hid the Plans in the Robot? (`space_plans`) | `.713` h `776bc5cd` | `house_space_plans.png` | The Space saga stage from the house camera: the painted desert at dusk under two suns, the tin-can robot, glow-stick sword, toy blaster and piggy bank on the Prop Table, and the five bots in the story's costumes |
| S2 | The Ring Is Mine, I Mean Ours (`mine_bridge`) | `.2187` h `57bba65b` | `house_mine_bridge.png` | The Ring quest stage from the house camera: the painted dwarf mine with its stone bridge and orange glow, the cursed ring, glowing staff, water bucket and frying pan on the Prop Table, and the five bots in the story's costumes |
| S3 | Dino Island Is Mostly Safe (`dino_island`) | `.3602` h `0b8148b9` | `house_dino_island.png` | The Dino park stage from the house camera: the painted jungle with its sagging fence and warning sign, the dino egg, meaty drumstick, safety waiver and dino plush on the Prop Table, and the five bots in the story's costumes |
| S4 | The Favor Father (`favor_father`) | `.4871` h `36bc2c9c` | `house_favor_father.png` | The Crime family stage from the house camera: the painted garden wedding with its striped tent and lemon trees, the plush horse head, cannoli tray, wedding envelope and the spare on the Prop Table, and the five bots in the story's costumes |
| S5 | What's in the Glowing Briefcase? (`glowing_briefcase`) | `.6361` h `413a9590` | `house_glowing_briefcase.png` | The Diner stage from the house camera: the painted retro diner with its chrome counter and red stools, the glowing briefcase, gold pocket watch, giant milkshake and giant cheeseburger on the Prop Table, and the five bots in the story's costumes |
| S6 | League Night, Bathrobe Optional (`league_night`) | `.7919` h `6bc01f38` | `house_league_night.png` | The Bowling stage from the house camera: the painted bowling alley with its lanes and pins, the rolled-up rug, bowling ball, ransom bag and milk carton on the Prop Table, and the five bots in the story's costumes |
| S7 | Pick a Pill, Any Pill (`pick_a_pill`) | `.9337` h `d33ff3f9` | `house_pick_a_pill.png` | The Simulation stage from the house camera: the painted night office with its cubicles and green screens, the red pill, blue pill, ringing phone and bent spoon on the Prop Table, and the five bots in the story's costumes |

The Crime family's bowl of oranges had no model on 2026-11-15 (Art Inspiration says so), so S4's alt text says "the spare" until you see what the table shows: a model, T19's fallback shape, or nothing. Name what you see.

**So T74 replaces 3 pictures (A1 to A3) and adds 7 (S1 to S7), from 9 new PNGs** (S1 and A2 share one).

### 1c. Who wears what

`dress.py`'s rule: each card's seats go to the robots in the card's order (OpenAI, Anthropic, SpaceXAI, Meta, You), except that the dark shades never go to Meta, who already wears black glasses, or to You, the box. They swap with Anthropic, whose gold glasses the shades then hide. Run on `Docs/tasks/T47-build/scenes_seats.json` (run):

| Card | OpenAI | Anthropic | SpaceXAI | Meta | You |
|---|---|---|---|---|---|
| `space_plans` | farm kid (wide-brim hat #E3C770) | smuggler pilot (dark shades #1A1A1E) | old desert hermit (hood #7A5232) | masked villain (saucepan helmet #222226) | rebel princess (tiara #D9DEE6) |
| `mine_bridge` | barefoot homebody (bob wig #8B4A26) | bossy old wizard (wizard hat #8C8A86) | brooding ranger (hood #5E7A3A) | loud, proud dwarf (horned helmet #6B6F75) | vain elf (tiara #C9CED6) |
| `dino_island` | billionaire park owner (top hat #F0E6CC) | nervous lawyer (dark shades #1A1A1E) | runaway dinosaur (dino hood #5DA642) | kid on the tour (ball cap #C8202E) | dinosaur expert (wide-brim hat #7A7A3A) |
| `favor_father` | family boss (fedora #2A2A2E) | family adviser (dark shades #1A1A1E) | reluctant youngest son (hood #6B6B30) | hot-headed eldest son (ball cap, backwards #E0482E) | washed-up crooner (top hat #8A3FB8) |
| `glowing_briefcase` | chatty errand man (dark shades #121216) | nosy errand man (fedora #4A4A4E) | boss's bored wife (bob wig #141416) | runaway boxer (hood #B8262A) | smooth fixer (top hat #1C1C20) |
| `league_night` | laid-back slacker (hood #D9C9A3) | rule-keeper teammate (saucepan helmet #6E7438) | quiet bowler (ball cap #9CCCEB) | flashy rival bowler (top hat #F0459A) | avant-garde artist (bob wig #1F4FC8) |
| `pick_a_pill` | sleepy office worker (beanie #6E7F92) | stern agent (dark shades #1A1A1E) | rebel in black leather (bob wig #18181C) | grand leader (wide-brim hat #6E1E2A) | fortune-teller (wizard hat #B9A3DE) |

The colors are T47's drafts; `dress.py` uses whatever `scenes.json` holds after T47. If T47 tuned any, the A1 caption's words still hold (it names roles and pieces, not colors).

## 2. The stage for each card

`dress.py` (not run) does it in one call per card; `t74.py dress <card>` writes `Saved/T74/spec.json` and runs it through the console box. Step by step, with whether each call can run outside PIE:

| Step | The call | Outside PIE? | Why |
|---|---|---|---|
| Backdrop | `Backdrop.set_editor_property("PreviewBackdrop", id)`, then `Backdrop.call_method("ShowBackdrop", (id,))` | **Yes** | `BP_Backdrop`'s construction script runs `ShowBackdrop(PreviewBackdrop)` in the editor (T17), and T48 shot all seven backdrops in the editor this way. `ShowBackdrop` only sets visibility and material parameters (`Graphs/BP_Backdrop/ShowBackdrop.txt`). |
| Props: the call T45 added | `BP_StageDirector.ResetStage()` | **No, in effect** | It runs, but `CardFromShow` takes the card from `BP_Show`'s `CardArr`, which `BP_Show.LoadData` fills only at BeginPlay. In the editor it finds no card and leaves every prop as it is; its `GoTable` flights also need Tick. |
| Props: what `ResetStage` calls | for each `BP_Prop` in `GameplayStatics.get_all_actors_of_class` order: `set_editor_property("PropName", name)`, then `call_method("SetProp", (name,))` | **Yes** | This is `ResetStage`'s loop body, in its order. `BP_Prop`'s construction script runs `SetProp(PropName)` in the editor (T45-build), and `SetProp` reads `props.json` from the Content folder and loads the mesh by its path. A prop actor past the card's four gets `""` and hides, as in `ResetStage`. |
| Costumes | for each robot in seat order: `call_method("SetHeadpiece", (seat.headpiece, seat.color))` | **Probably: RE-CHECK** | Everything in T47's `SetHeadpiece` is editor-safe (JSON, a soft load, transforms, material parameters, visibility) except `MakeHat`'s `Add Component by Class`, which T47 runs only in PIE. On an editor actor called from Python it should make a transient component. `dress.json` says `hat_ok` per robot: the `Hat` is valid, visible and has a mesh. If any is false, use fallback A. |
| Labels | `set_visibility(False)` on every `TextRenderComponent` of every robot (`Label`, with T57's "(passed)" line), and on every component the game hides anyway (`hidden_in_game`: billboards, sprites) | **Yes** | Component visibility, nothing more. It runs after the costumes, because `SetHeadpiece` moves the label (it doesn't show it). |

- **Order matters for one reason:** a property set on a robot reruns its construction script, which rebuilds its look without the hat. `dress.py` sets no robot property; it only calls functions on the robots, and the robots come after the backdrop and the props.
- **It runs again for the next card** without a reload: `SetHeadpiece` reuses its `Hat`, `ShowGlasses` brings the glasses back when the shades come off, and the backdrop and props switch.
- **It reports** the `StageCamera`'s transform and FOV (expected (−1050, 0, 330), pitch −20, yaw 0, FOV 90; T43-build E5 says to use the real one) and each robot's place, facing, visible top and half-width, for the close-up cameras.
- Every editor call in `dress.py` was checked against the 2026-11-15 capture scripts (another session's `probe.py`, `hide_labels.py`, `setfov.py`) and T46's findings on editor Python (`set_editor_property`, `component_tags` read with `get_editor_property`). `call_method` on a Blueprint function and `SystemLibrary.get_component_bounds` are new here: not run.

### Fallback A: the hats by hand (editor, not run)

If `dress.json` shows `hat_ok: false`, run [hats_fallback.py](T74-build/hats_fallback.py) right after `dress.py` (`py "<path>"` in the console box; it writes `Saved/T74/hats.json`). It spawns a `StaticMeshActor` per robot with the headpiece mesh, attaches it to the robot's `HeadSocket` with `KEEP_RELATIVE` (as T80-build part 5 tried hats), sets T47's relative fit (with any `on` override) and the seat's color on a dynamic instance, hides the robot's own glasses under the shades, and lifts `Nub` and the toppers by T47's formula (the stalk's base 4 cm under the hat's top). Then capture as usual.

### Fallback B: PIE at the title screen (not run)

If the editor world can't match the game (part 0 step 5), or fallback A fails:
1. Set the PIE window to 1920 × 1080: `ObjectTools.set_properties` on `/Script/UnrealEd.Default__LevelEditorPlaySettings` (T46: Python can't reach it) with `NewWindowWidth` 1920, `NewWindowHeight` 1080, then start PIE in a new window. Click nothing: the title screen shows, and no show starts.
2. `python t74.py dress <card> --pie`: `dress.py` runs the same calls on the PIE world's actors (no property sets). Then hide the title screen: a one-line editor Python, `for w in unreal.WidgetBlueprintLibrary.get_all_widgets_of_class(unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world(), unreal.UserWidget, True): w.set_visibility(unreal.SlateVisibility.HIDDEN)`.
3. `SlateInspectorToolset.Windows` (`select` the PIE window), then `SlateInspectorToolset.Screenshot`; decode `returnValue.data` to a PNG (T54). `CaptureViewport` captures the editor world, not PIE (T17). The game's own camera is the house camera, so this is the house shot as the game frames it; crop it to 16:9 with `crop.ps1` if the window has a title bar. The close-ups and the cast still come from the editor (fallback A for their hats).

### Fallback C: the task's own (not run)

A free autoplay show in PIE (`"mode": "free"`, `"autoplay": true` in `Local/switches.json`, which a worktree doesn't have: copy the repo folder's), with screenshots of a scene turn of each card that comes up. A show plays 4 cards of 7 at random and the HUD covers the stage's edges, so it takes several shows and gives worse pictures. Use it only if A and B both fail.

## 3. The capture

### 3a. T74's own editor (not run)

From T74's worktree (part 0 step 9), in PowerShell, so the PID comes back:

```powershell
$p = Start-Process -FilePath "E:/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor.exe" -ArgumentList '"<worktree>/AIMegaJam2026.uproject"', '-ModelContextProtocolPort=8011', '-NoLiveCoding' -PassThru; $p.Id
```

Put the PID in `Agents/status/task-T74.md`. The first open from a new worktree compiles shaders and can take several minutes. Then `python Docs/tasks/T74-build/t74.py check`: it finds the console box (the textbox after `text "Cmd"` in a `SlateInspectorToolset.Snapshot`) and takes one capture to learn the viewport's shape (`Saved/T74/viewport.json`). Leave the editor window maximized with one perspective viewport, and don't resize it between shots: the crop math depends on the viewport's shape, and `t74.py` stops if it changes. At the end, close only this editor: `Stop-Process -Id <pid> -Force`, which also discards the dirty level (nothing saved, as the task requires).

`t74.py` posts JSON-RPC straight to `http://127.0.0.1:8011/mcp` (`initialize`, then `tools/call` of `call_tool` with `toolset_name`, `tool_name` and `arguments`), never through `unreal-mcp`, which reaches the other editor on port 8000. It refuses port 8000. The calls are the 2026-11-15 session's (`mcp.py`, `pyrun.py`, `vcap.py` in its scratchpad), which worked.

### 3b. The calls

```bash
python Docs/tasks/T74-build/t74.py all
```

(not run) dresses and shoots everything, the cast card last so its house shot, close-ups and cast share one dressing, and writes `Saved/T74/shots/manifest.json` (each card's roles, colors, props and cameras). One card at a time: `t74.py house <card>`, `t74.py cast`, `t74.py details`. Every capture is:

```json
{"toolset_name": "EditorToolset.EditorAppToolset", "tool_name": "CaptureViewport", "arguments": {
  "captureTransform": {"location": {"x": -1050, "y": 0, "z": 330}, "rotation": {"pitch": -20, "yaw": 0, "roll": 0}, "scale": {"x": 1, "y": 1, "z": 1}},
  "annotations": {"gridSpacing": 0, "gridExtent": 0, "gridHeight": 0, "maxLabelDistance": 0, "classFilter": {"refPath": "/Script/Engine.StaticMeshActor"}, "maxLabels": 0},
  "bShowUI": false}}
```

`annotations` is required even unused (T43, T46). The PNG comes back as base64, in an `image` content item or in `returnValue.image.data`; `t74.py` takes either, saves it to `Saved/T74/raw/`, and since it reads the HTTP reply itself, the image's size is no problem (T46's tool-result limit was Claude Code's). Before each capture, `setfov.py` sets the viewport's FOV (`LevelEditorSubsystem.set_level_viewport_fov`) and Game View, so editor sprites don't show. Each shot is rendered twice and the second kept, in case the first comes before Lumen settles (`--no-warm` for one).

### 3c. The cameras

| Shot | Camera | Horizontal FOV of the frame | Frame | Out |
|---|---|---|---|---|
| House, one per card | `StageCamera`'s own transform from `dress.json` (expected (−1050, 0, 330), pitch −20, yaw 0) | its own FOV (expected 90) | 16:9, cropped to 1920 × 1080 | `house_<card>.png` |
| Close-up, one per robot, the cast card | front on: the robot's place plus its forward vector × D, at height z, pitch 0, yaw facing the robot. D and z are the same for all five, so they share one scale: z is the middle of floor − 8 cm to the tallest visible top + 12 cm, and D fits that height and the widest robot + 20 cm each side, at least 250 cm. On the 2026-11-15 places with a 262 cm top (OpenAI's halo over a lifted stalk), D = 346 cm and z = 133 (`t74.py selftest`, run). | 34 (the 2026-11-15 close-ups) | 3:4, 900 × 1200 | `bot_<seat>.png` |
| Stage close-ups, the cast card | the 2026-11-15 cameras: proscenium (−820, −150, 230), pitch −5.495, yaw −41.10; chandelier (−820, 60, 300), pitch 17.87, yaw −10.62 | 58 and 42 | 1600 × 1000 and 1200 × 1000 | `proscenium.png`, `chandelier.png` |

**The crop.** The editor viewport is wider than any frame here (2.4:1 to 2.9:1 on this PC), and the game's camera keeps its horizontal FOV. So for a frame of aspect a and horizontal FOV f, the viewport gets the FOV F = 2·atan(tan(f/2) · A/a), A being the viewport's aspect, and `crop.ps1` keeps the middle a-wide box at full height. For the house shot on the 2026-11-15 viewport (3376 × 1166), F = 116.9°, and the crop is exactly the game's 16:9 frame (no pitch fix needed, unlike T48's and T49's uncropped captures). `t74.py selftest` checks this sum (run: "selftest ok").

**The pictures.** `cast.ps1` puts the five close-ups in seat order (OpenAI, Anthropic, SpaceXAI, Meta, You), each cropped to 3:4 and scaled to 380 × 506 with rounded corners, and under each a seat-color swatch, the provider's name in Segoe UI Bold and the role in smaller type, on the cream sheet of the 2026-11-15 picture: 2012 × 658 px. `details.ps1` puts the proscenium shot (its left 17% cut off) beside the chandelier shot, both 700 px tall: about 1833 × 748. Both were run on the 2026-11-15 shots and came out right (the test strip showed the old pill bots, as expected).

### 3d. Look at each PNG before uploading (not run)

Read each file in `Saved/T74/shots/` (the Read tool shows a PNG). Each house shot passes when: the backdrop is that card's painted picture; the card's four props are on the Prop Table, and you know which ones a bot hides; every robot wears its piece from part 1c, sitting right (not floating, not sunk, facing the house), with its topper poking out; Anthropic's glasses are gone under the shades; no "ROBOT" label, editor sprite, gizmo or grid shows; the chandelier is at the top center and the stalls at the bottom, as in the game frame. The cast passes when all five are whole (feet to topper), the same scale, front on, and labeled in seat order. The close-ups pass when they show the new backdrop, not the castle. Fix and re-shoot what fails. Write what each picture showed under T74's "## Findings".

## 4. The upload (not run)

`C` is `{"kind":"project","id":"f5944726-d81b-42c0-8891-1b48b7d14b1d"}` (the doc; its link is <https://claude.ai/artifact/XKrsACU5w4kHFwhztXCoTA>). The connector's own guide for this is `guide(items=["topic.uploads", "topic.editing", "topic.pictures"])`: read it first, as its words win over this sheet's.

1. **Upload the 9 PNGs to the doc's artifact**, in one call (one approval), with the Artifact tool's asset upload:
   ```text
   Artifact(action="publish", url="https://claude.ai/artifact/XKrsACU5w4kHFwhztXCoTA", asset=true,
            file_paths=["<worktree>/Saved/T74/shots/house_space_plans.png", "<...>/house_mine_bridge.png",
                        "<...>/house_dino_island.png", "<...>/house_favor_father.png", "<...>/house_glowing_briefcase.png",
                        "<...>/house_league_night.png", "<...>/house_pick_a_pill.png",
                        "<...>/cast_space_plans.png", "<...>/stage_details_space_plans.png"])
   ```
   Each file comes back with an id (32 hex) and a url. Use the id.
2. **Record each upload as a blob in the doc**, one call each:
   ```text
   create(object="blob", engine="blob", container=C, payload={"asset": "<the upload's 32-hex id>"})   -> {"id": "blob/<id>"}
   ```
   A blob answer of "no blob with that id" or `not_minted` means the upload went to another artifact: upload again to the doc's link.
3. **Art Inspiration: three pictures and two captions, one call**, guards from the part 0 step 7 read (the values below are from rev 33):
   ```json
   update(ref={"object":"node","id":"61d7c585-d94a"}, engine="prose", container=C, payload={"ops":[
     {"op":"replace","target":{"kind":"blocks","ids":["m90jp575z84.20161"]},"ifHash":"ad443ac2","ifRev":33,
      "with":{"as":"text","from":{"kind":"inline","content":"<A1's new caption>"}}},
     {"op":"replace","target":{"kind":"blocks","ids":["m90jp575z84.20321"]},"ifHash":"8e00c20e","ifRev":33,
      "with":{"as":"markdown","from":{"kind":"inline","content":"![<A1's alt>](blob/<cast>)"}}},
     {"op":"replace","target":{"kind":"blocks","ids":["m90jp575z84.20323"]},"ifHash":"6c81e26f","ifRev":33,
      "with":{"as":"text","from":{"kind":"inline","content":"<A2's new caption>"}}},
     {"op":"replace","target":{"kind":"blocks","ids":["m90jp575z84.20462"]},"ifHash":"1f14810e","ifRev":33,
      "with":{"as":"markdown","from":{"kind":"inline","content":"![<S1's alt>](blob/<house_space_plans>)"}}},
     {"op":"replace","target":{"kind":"blocks","ids":["m90jp575z84.20575"]},"ifHash":"42f02906","ifRev":33,
      "with":{"as":"markdown","from":{"kind":"inline","content":"![<A3's alt>](blob/<stage_details>)"}}} ]})
   ```
   `"as":"text"` re-words a caption in place; `"as":"markdown"` re-creates the picture's paragraph with the new image. A `guard_mismatch` means someone changed that block after your read: read it again and work from what stands. An `anchors_affected` refusal means a comment hangs on words you replace: narrow the edit, or ask my person (never resolve their thread to clear the way).
4. **Stories: seven new pictures, one call** (inserts need no guard):
   ```json
   update(ref={"object":"node","id":"1775d40f-9ea4"}, engine="prose", container=C, payload={"ops":[
     {"op":"insert","target":{"kind":"blocks","ids":["m90jp575z84.713"]},"side":"after",
      "source":{"as":"markdown","from":{"kind":"inline","content":"![<S1's alt>](blob/<house_space_plans>)"}}},
     {"op":"insert","target":{"kind":"blocks","ids":["m90jp575z84.2187"]},"side":"after",
      "source":{"as":"markdown","from":{"kind":"inline","content":"![<S2's alt>](blob/<house_mine_bridge>)"}}},
     ... the same for .3602 (S3), .4871 (S4), .6361 (S5), .7919 (S6), .9337 (S7) ]})
   ```
5. **Look at each picture in the doc** (the task's Done-when): first `read` each tab with `{"kind":"view","sinceRev":<your last read's rev>}` to see the new `<media>` blocks where part 1 says, then one `read(ref={"object":"blob","id":"blob/<id>"}, container=C, payload={"kind":"picture"})` per new blob, each its own call. An answer with no image means you haven't seen it: say so, never claim it.
6. **Keep every other word.** The only changes are part 1's: two captions, three picture blocks, seven inserts. If the doc shows them as suggestions (a viewer in Suggesting mode), tell my person rather than accepting them yourself.

## 5. Done when (T74.md), and what checks it

| T74's Done-when | Checked by |
|---|---|
| The doc's stage and cast pictures show the painted backdrop, the card's props and the bots in costume | part 3d on each PNG, then part 4 step 5 in the doc (A1, A2, A3) |
| Every story in the Stories tab has its house shot | part 4 step 5: seven new `<media>` blocks, one under each Backdrop line (S1 to S7) |
| You looked at each picture in the doc | part 4 step 5's `picture` reads, all nine blobs (A2 and S1 share one) |
| No asset was saved | `git status` in the worktree shows no `.uasset` or `.umap`; the editor was closed by its PID with the level dirty |

T74's commit holds `Docs/tasks/T74.md` (Result and Findings), the plan's box and a `Docs/DevLog.md` line. No asset, no `Graphs/` file (nothing was written to a graph). Delete the status file and push.

## Decisions made for my person

1. **The Space saga on both Art Inspiration pictures** (the cast and the house view): my person's pick, asked 2026-11-15. Its five headpieces are five different kinds and none is very tall.
2. **The stage close-ups are re-shot too** (A3): my person's call, asked 2026-11-15. The old picture showed the castle backdrop and a pill bot.
3. **Who wears what:** each card's seats go to the robots in card order, and the dark shades swap to Anthropic when they would fall to Meta or You (part 1c). Meta's own glasses are already black, so shades on Meta change nothing you can see, and the shades hide Anthropic's gold ones, which shows the costume. One rule in `dress.py`'s `seat_map`.
4. **The cast strip names each bot's role** under its provider ("OpenAI / farm kid"), so the picture explains its costumes.
5. **The seven Stories pictures have no caption,** only alt text: the Backdrop line right above each one names it, as each "Props:" line names its strip.
6. **One upload serves two places:** the Space saga's house shot is S1 and A2.
7. **The editor world, not PIE,** for every shot, with Game View on and the labels hidden; PIE only as a fallback (part 2), because `CaptureViewport` can't capture PIE and the editor gives the exact game frame by the crop.
8. **The image work uses PowerShell's System.Drawing,** so nothing is installed.
9. **The render sheets stay** (set pieces, headpieces, props), since T45 and T47 change no model.

## Findings for T74 to pass on

- **The Stories tab's intro is out of date:** it still says "This is the draft for review (2026-11-15): one agent wrote each card, and nothing is in the game yet." T44 put all seven cards in the game. That paragraph isn't a picture or a caption, so it is outside T74's Touches: tell my person in T74's Findings, and don't change it.
- **The doc's in-engine pictures are all JPEGs today,** so no agent can look at them through the docs `picture` read. The 2026-11-15 originals (PNG and JPEG) are in another session's scratchpad, `C:/Users/Personal/AppData/Local/Temp/claude/3541f847906fb233/918b0f1b-68a0-4fa9-937e-13fe89e5c85a/scratchpad/` (`cap/shots/`, `sheets/`), which a cleanup can delete. This prep looked at `sheets/stage_details.jpg`: the castle backdrop and a pill bot are in it, hence decision 2.

## Findings

(For the T74 session.)
