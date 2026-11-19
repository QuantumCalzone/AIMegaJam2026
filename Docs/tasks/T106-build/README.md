# T106's build scripts: the house in `L_Stage`

The editor Python that built T106's theater, in the order it ran (2026-11-19). Run each from the
editor's `Cmd` box: `py "<repo>/Docs/tasks/T106-build/<step>.py"`. Each writes its result to
`Saved/T106/out/<step>.json` (or `<step>.err.txt`). [T106.md](../T106.md) has what each found.

1. `s01_inventory.py` (read only). Dumps every actor and freezes `Saved/T106/out/snapshot.json` the first
   time: every audience bot's place, turn, lean, scale, color, hat and glasses, and the old parts' bounds.
   `s05` reads the snapshot, so it keeps working after the old parts are gone.
2. `s02_import.py`. The 12 GLBs from `Docs/Art/Set/<piece>/model.glb` into `Content/NHOS/Stage/Set/`.
3. `s03_materials.py`. The `MI_Theater_*` swatches, `M_SetModel` (the palette shift) and its instances.
4. `s04_audbot.py`. `BP_AudienceBot` on the generated model. Run once; it deletes the old shapes.
5. `s05_house.py`. The house, re-runnable: it destroys only its own folder
   (`Stage/Theater/Opera/T106`), the old parts named in `DELETE`, and every audience bot, then places it all
   again. It does not save. `s06_shots.py` takes layout shots from the editor viewport.
6. Save the level, then `s07_cleanup.py` (`DRY_RUN` first) deletes the old assets that nothing references.
