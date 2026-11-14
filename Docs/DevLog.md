# Dev log

One line for each commit that changes the game or the plan, oldest first. The jam's Glass Box category needs a dev log, and it must be submitted with the entry; it can't be added later.

Format: `- <date and time, UTC> · <task ID, or Plan> · <model and effort> · <what was done and what was learned>`

- 2026-11-13 23:20 UTC · Plan · Claude Fable 5.2 · Read the design doc and saved a copy in the repo. Checked the engine install: it ships HTTP and JSON Blueprint plugins, both off by default, so a Blueprint-only LLM call looks possible. Wrote the MVP plan: 14 tasks, the LLM-call spike first, a playtest gate at T11, and task claims through Git LFS locks.
- 2026-11-13 23:49 UTC · T01 · Claude Opus 5.5 (high) · One Claude call from Blueprint works in PIE: BPC_LLMClient builds the request with JSON nodes, sends it with the HttpBlueprint node and parses a JSON reply ("NHOS: SPIKE OK"); a wrong key gives the API error ("NHOS: SPIKE FAIL"). About 2 s per call. Built through Unreal MCP graph scripts; the Http Request node needed hand wiring, and the level had to be made in the editor.
- 2026-11-14 00:12 UTC · T02 · Claude Opus 5.5 (high) · The Claude call works in a packaged Windows Development build too ("NHOS: SPIKE OK", 1.5-1.8 s per call), so LLM calls stay Blueprint-only. But the HTTP and JSON plugins make the packager compile a game program, so packaging needs Visual Studio C++ and the Windows 11 SDK, plus -nocompileeditor -unrealexe to skip a project editor build. Data files ship loose next to the pak; the key goes in the build's Local/ folder and must never be zipped. Build: 968 MB, 387 MB zipped without the .pdb.
- 2026-11-14 00:15 UTC · Plan · Claude Opus 5.5 · Every Claude role (actor, input LLM, Director) now runs claude-haiku-5-5 at low effort, the cheapest model at its lowest level, to cut cost per call about 40x from Opus 5.5. Haiku 5.5 has no server-side fallback, so fallbacks are off in llm.json. Not yet checked in PIE.
