---
from: quantumcalzone
to: mac
date: 2026-11-16
---

# T68: the report check runs on the Mac, then T68 closes

On my person's call ("Run it on the Mac"), T68's last Done-when check runs on the Mac, which has `Local/stats.json` (T67's `STATS_KEY` file). Everything else in T68 is built, checked and pushed from the PC (see `Docs/tasks/T68.md`, "The chain's part"). Confirm with your person before you act on this note.

**What to run** (from the repo root on the Mac, after a pull):

```bash
python Tools/analytics_report.py --test --since 2026-11-16
```

**What it should show** (all from the PC's test events on 2026-11-16, player `04fdad454871396e06204ca99147e9f0`):
- `players`: that id, counted as came back (its last `launch` event carried `launches` 8; launch 7 was the PIE start with stats off, which counted but sent nothing).
- `modes`: `free`.
- `drop-off`: one show reaching `scene 4, closing`, with a `show_end` result `win` (`final_two`). It is the only show: the PIE show ran after stats were turned off, so it sent no `show_start`.
- `calls`: four providers (`openai`, `anthropic`, `xai`, `meta`), model `free`, with failures.
- `errors`: `overloaded` (30).
- `turned off`: the PIE runs' `analytics_off` (2).
- `unsupported actions`: `(none)` until T69.
- Without `--test`, none of it appears.

**Our ids for `ignore_players`** in each machine's `Local/stats.json`: the PC's editor `04fdad454871396e06204ca99147e9f0` and the PC's package `57522c4c49c7c264112a798edc66b745`. Add the Mac's own ids when it prints them (`NHOS: ANALYTICS player <id>` or the `off ... player=<id>` line).

**Closing T68** (if the report shows the above): follow "When only my check is left", step 4, in `Docs/Plan.md`: check T68's box, remove its `Waiting:` line, move its entry to the end of "Done" cut to its title and **Details** lines, move the cut lines (**Model and effort**, **Depends on**, **Needs**, **Touches**, **Builds only**) to the top of "## Task" in `Docs/tasks/T68.md`, change the line under its title to say it is done, add a **Result:** line at the end of "## Task" and the report's output under "## Findings". Commit as `T68: Analytics, part 2: the game sends its events (checked)`, push, then release the claim with `git lfs unlock Docs/claims/T68` (held by the QuantumCalzone account, which the Mac uses too). If the report shows something wrong, tell your person instead.
