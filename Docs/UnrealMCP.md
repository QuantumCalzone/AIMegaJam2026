# Unreal MCP: how it is set up

Background on the Unreal MCP server in this project. The rules for using it are in the "Unreal MCP" section of [CLAUDE.md](../CLAUDE.md).

UE 5.8 includes **Unreal MCP**, the experimental `ModelContextProtocol` plugin. It runs an MCP server inside the editor process at `http://127.0.0.1:8000/mcp`. Docs: https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor

- **How it's set up here** (UE 5.8.4 has both the plugin and auto-start off by default, unlike the docs):
  - `ModelContextProtocol` and `AllToolsets` are enabled in the `.uproject`, limited to the Editor target, so packaged builds don't include the server.
  - Auto-start is on through `Config/DefaultEditorPerProjectUserSettings.ini` (`bAutoStartServer=True`), so the server starts whenever the editor opens.
  - `AllToolsets` pulls in Game Features, which needs the `GameFeatureData` entry under `AssetManagerSettings` in `DefaultGame.ini`. Without that entry, the editor reports load errors at startup. The entry has `bIsEditorOnly=True`, because packaged builds don't include Game Features; without it, the packaged game hits an ensure at startup.
  - `.mcp.json` in the project root (written by `ModelContextProtocol.GenerateClientConfig ClaudeCode`) points Claude Code at the server as `unreal-mcp`.
- **Approval:** Each person approves `unreal-mcp` once, or adds `"enabledMcpjsonServers": ["unreal-mcp"]` to their own `.claude/settings.local.json` (git ignores that file).
- The server only exists while the editor runs. Commandlets don't start it unless you pass `-ModelContextProtocolStartServer`.
- Instructions for every connecting agent can be set in Project Settings > Agentic Workflows > Model Context Protocol > Instructions. They are stored in `DefaultGame.ini`.
- Server logs use the `LogModelContextProtocol` category in the editor log.
