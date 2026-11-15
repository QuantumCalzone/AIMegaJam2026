# Background

Back to [the plan](../Plan.md). Findings that belong to no one task: the research before T01 and the spike questions.

## Findings

Spike and playtest results went here, newest at the bottom, until 2026-11-14. Since then each task's results are under "## Findings" in its own file in `Docs/tasks/`.

### Before T01: plan research (2026-11-13)

Checked by reading the engine install and the Claude API reference. Nothing here is proven in PIE yet.

- **The engine has what the spike needs.** UE 5.8.4 ships three plugins that are off by default:
  - `HttpBlueprint` (experimental): an `Http Request` node that takes a URL, a verb, a map of headers and a body string. It returns the response body as a string, a success flag and the response headers. It has no status-code output and no timeout input.
  - `JsonBlueprintUtilities` (beta): `From String`, `From File`, `To String`, `To File`, `Get Field`, `Set Field`, `Has Field`, `Get Field Names` and `Struct To Json String`.
  - `BlueprintFileUtils`: find, copy, move and delete files. It can't read a file's text.
- **Runtime text files will probably be JSON.** The only stock Blueprint node found that reads a file from disk is `From File`, which reads JSON. That is why the plan stores prompts as `.json` with long text as arrays of lines.
- **A C++ fallback is possible on this machine.** Visual Studio 2022 with the C++ tools is installed. Mac teammates would need Xcode. The engine is a launcher build, so a Blueprint-only package needs no compiler.
- **Claude API, raw HTTP.** `POST https://api.anthropic.com/v1/messages` with the headers `x-api-key`, `anthropic-version: 2026-10-21` and `content-type: application/json`. JSON replies are requested with `output_config.format`. The reply's `content` is an array that can start with a `thinking` block, so the game must take the first block whose `type` is `text`. A reply can also stop with `stop_reason: "refusal"`; treat that like a reply that can't be parsed. The `claude-api` skill has the exact shapes.
- **Calls per show:** about 55, counted from the rules for a cast of 4 with 2 Free Talk rounds.
- **Claims work.** `git lfs lock` on a plain text file works on GitHub from a branch that is not pushed yet (tested, then unlocked).

### Spike questions for T01 and T02

T01 and T02 write the answers here.

1. Can Unreal MCP place the `Http Request` node and the `Get Field` node? If not, can editor Python?
2. What is the cleanest way to build the request body in Blueprint, with correct escaping of quotes and line breaks in the prompt text?
3. Can `Get Field` read an array of objects (the reply's `content`) and an array of strings (prompt lines)?
4. Does `From File` read a file under `Content/NHOS/Data/` in PIE and in a packaged build? Which Blueprint node gives the right folder in both?
5. How does an HTTP error look to Blueprint (a wrong key, a rate limit, no network), given that there is no status code?
6. Which HTTP timeout applies, and does `[HTTP]` in `Config/DefaultEngine.ini` need a longer one?
7. How many seconds does one call take, and what does one show cost, with the model and effort in `llm.json`?
8. Blueprint-only or C++? (T02 writes the decision note.)
