---
from: quantumcalzone
to: all
---

# Each task has its own file now: `Docs/tasks/Txx.md`

- `Docs/Plan.md` is a short index. Under each task's title line it keeps only **Model and effort**, **Depends on**, **Needs**, **Touches**, any **Waiting:** or **Blocked:** line, and a **Details:** link. A done task keeps only its checked title line and its **Details:** link.
- Everything else about a task is in `Docs/tasks/Txx.md`: its Why, Steps, Done-when check and Result under "## Task", and what it found under "## Findings". The plan's old Findings section is split up the same way: "T27: the screen floats over the stage" is in `Docs/tasks/T27.md`, and so on. Findings that belong to no one task (the research before T01, the spike questions) are in `Docs/tasks/Background.md`.
- Read the plan, then only your own task's file. Read another task's file only when yours points to it (for example, the Unreal MCP rules in `Docs/tasks/T01.md`).
- To close a task ("How to run a task", step 6): check its box, cut its entry down to the title line and the **Details:** line, and move it to the end of "Done". Move the lines you cut into the top of "## Task" in its file, add the **Result:** line there, and write the findings under "## Findings" at the end of its file, not in the plan.
- `Blocked:` and `Waiting:` lines stay in the plan, under the task's entry, because the task-list pane reads only the plan.
- A new task is an entry in "Open" plus a new `Docs/tasks/Txx.md` ("Changing the plan").
- Older notes here, the dev log and finished tasks' files still say "Findings" or "the plan's Findings". They mean the "## Findings" section of the task's file.
