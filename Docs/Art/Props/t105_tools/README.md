# T105's tools

The scripts that made, fixed, imported and checked the 28 story props' models. `Docs/tasks/T105.md` ("Findings") says how they were used; paths inside them point at the session's scratchpad and at `Saved/T105/`, so read them as a record, not as ready-to-run tools.

| File | What it does |
|---|---|
| `plan.py` | Builds each prop's Rodin prompt and settings from T97's `prompts.json`. |
| `mk.py`, `put.py` | Upload the approved views to Hyper3D's presigned URLs. |
| `fetch.sh`, `fetch2.sh` | Download a finished generation's FBX and diffuse map, then convert and render it. |
| `fbx2obj.py` | Reads a binary FBX (stdlib only) and writes an OBJ plus mesh stats: triangles, pieces, open edges, bounds. |
| `render.swift` | Renders an OBJ with its texture from four sides with SceneKit, offscreen (turntable and thumbnail). |
| `sheet.swift`, `grid.swift` | Tile the approval sheets and the check screenshots. |
| `fbxedit.py` | Edits a binary FBX 7.4 and writes it back with every unchanged array byte for byte: `seal` (smooth a stamped relief), `tray` (add a round tray), `tex` (swap an embedded texture). |
| `fixtex.swift`, `fillrect.swift` | Texture fixes: recolor (plum ball, old-gold rug), paint a disc plain (the seal), glow masks by hue, a gray block for the tray's UVs. |
| `assemble.py`, `save.py` | Build each final FBX (fixed diffuse, flat 1-pixel normal, roughness and metallic maps) and write each prop's files and `model_log.json`. |
| `imp.py`, `glow.py` | Editor Python, run from the Cmd box: reimport over the old assets, and add the emissive glow. |
| `dress.py` | Editor Python for the PIE check: dress the table with a card's props, put one in a hand, move the house camera. |
