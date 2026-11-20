"""A small client for Unreal MCP (the editor's ModelContextProtocol plugin), for T113's media scripts.

It posts JSON-RPC straight to an editor's MCP server, so a session can drive its own second editor
(started with -ModelContextProtocolPort=<port>) without touching the one on port 8000.

    python Docs/ItchMedia/tools/mcp.py --port 8031 toolsets
    python Docs/ItchMedia/tools/mcp.py --port 8031 describe <toolset>
    python Docs/ItchMedia/tools/mcp.py --port 8031 call <toolset> <tool> '<json arguments>'

As a module: Mcp(port).call(toolset, tool, {...}) returns the tool's result (parsed JSON when it is JSON).
"""
import argparse
import json
import sys
import urllib.request


class Mcp:
    def __init__(self, port=8031, timeout=600):
        self.url = f"http://127.0.0.1:{port}/mcp"
        self.timeout = timeout
        self.session = None
        self.next_id = 1
        self._rpc("initialize", {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "nhos-itch-media", "version": "1"},
        })
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def _post(self, body):
        req = urllib.request.Request(self.url, data=json.dumps(body).encode("utf-8"), method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json, text/event-stream")
        if self.session:
            req.add_header("Mcp-Session-Id", self.session)
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            sid = resp.headers.get("Mcp-Session-Id")
            if sid:
                self.session = sid
            raw = resp.read().decode("utf-8", "replace")
            ctype = resp.headers.get("Content-Type", "")
        if not raw.strip():
            return None
        if "text/event-stream" in ctype:
            # The last "data:" event that carries a JSON-RPC result or error.
            msg = None
            for line in raw.splitlines():
                if line.startswith("data:"):
                    try:
                        msg = json.loads(line[5:].strip())
                    except ValueError:
                        pass
            return msg
        return json.loads(raw)

    def _rpc(self, method, params):
        body = {"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params}
        self.next_id += 1
        msg = self._post(body)
        if msg is None:
            raise RuntimeError(f"{method}: empty reply")
        if "error" in msg:
            raise RuntimeError(f"{method}: {msg['error']}")
        return msg["result"]

    def tool(self, name, arguments):
        """Calls one of the server's own tools (list_toolsets, describe_toolset, call_tool)."""
        res = self._rpc("tools/call", {"name": name, "arguments": arguments})
        out = []
        for item in res.get("content", []):
            if item.get("type") == "text":
                text = item["text"]
                try:
                    out.append(json.loads(text))
                except ValueError:
                    out.append(text)
            else:
                out.append(item)
        if res.get("isError"):
            raise RuntimeError(f"{name} failed: {out}")
        return out[0] if len(out) == 1 else out

    def call(self, toolset, tool, arguments=None):
        return self.tool("call_tool", {"toolset_name": toolset, "tool_name": tool, "arguments": arguments or {}})

    SLATE = "SlateInspectorToolset.SlateInspectorToolset"

    def console(self, command):
        """Types one console command into the editor's status-bar console box (the textbox after "Cmd").

        No MCP tool runs editor Python, but the console does: console('py "C:/abs/path/script.py"').
        The box needs a Click before Type (T62), and its ref changes per session, so it is found each time.
        """
        import re
        snap = self.call(self.SLATE, "Snapshot", {"ref": ""})["returnValue"]
        menu = None
        for line in snap.splitlines():
            if line.strip().startswith("menu ") and "[ref=" in line:
                menu = re.search(r"\[ref=(\w+)\]", line).group(1)
                sub = self.call(self.SLATE, "Snapshot", {"ref": menu, "maxDepth": 6})["returnValue"]
                if 'text "Cmd"' in sub:
                    tb = re.search(r"textbox .*\[ref=(\w+)\]", sub)
                    if tb:
                        ref = tb.group(1)
                        self.call(self.SLATE, "Click", {"ref": ref})
                        return self.call(self.SLATE, "Type", {"ref": ref, "text": command, "submit": True})
        raise RuntimeError("the console box (Cmd) was not found")

    def py(self, path):
        """Runs an editor Python file through the console box. Write results to a file to read them back."""
        return self.console(f'py "{path}"')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8031)
    ap.add_argument("what", choices=["toolsets", "describe", "call"])
    ap.add_argument("rest", nargs="*")
    a = ap.parse_args()
    m = Mcp(a.port)
    if a.what == "toolsets":
        r = m.tool("list_toolsets", {})
    elif a.what == "describe":
        r = m.tool("describe_toolset", {"toolset_name": a.rest[0]})
    else:
        args = json.loads(a.rest[2]) if len(a.rest) > 2 else {}
        r = m.call(a.rest[0], a.rest[1], args)
    print(json.dumps(r, indent=1)[:20000] if not isinstance(r, str) else r[:20000])


if __name__ == "__main__":
    sys.exit(main())
