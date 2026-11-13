# Dev log

One line for each commit that changes the game or the plan, oldest first. The jam's Glass Box category needs a dev log, and it must be submitted with the entry; it can't be added later.

Format: `- <date and time, UTC> · <task ID, or Plan> · <model and effort> · <what was done and what was learned>`

- 2026-11-13 23:20 UTC · Plan · Claude Fable 5.2 · Read the design doc and saved a copy in the repo. Checked the engine install: it ships HTTP and JSON Blueprint plugins, both off by default, so a Blueprint-only LLM call looks possible. Wrote the MVP plan: 14 tasks, the LLM-call spike first, a playtest gate at T11, and task claims through Git LFS locks.
- 2026-11-13 23:49 UTC · T01 · Claude Opus 5.5 (high) · One Claude call from Blueprint works in PIE: BPC_LLMClient builds the request with JSON nodes, sends it with the HttpBlueprint node and parses a JSON reply ("NHOS: SPIKE OK"); a wrong key gives the API error ("NHOS: SPIKE FAIL"). About 2 s per call. Built through Unreal MCP graph scripts; the Http Request node needed hand wiring, and the level had to be made in the editor.
