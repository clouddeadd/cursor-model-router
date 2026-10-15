#!/usr/bin/env python3
"""MCP: pick a named model for a task and display it."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from router import format_display, pick  # noqa: E402


def ok_text(text: str) -> dict:
    return {"content": [{"type": "text", "text": text}]}


def handle_pick(args: dict) -> dict:
    picked = pick(
        str(args.get("task") or ""),
        conversation_id=args.get("conversation_id"),
    )
    return ok_text(format_display(picked) + "\n\n" + json.dumps(picked, indent=2))


TOOLS = {"pick_model": handle_pick}
TOOL_DEFS = [
    {
        "name": "pick_model",
        "description": (
            "Pick the best named model for this task. Returns MODEL display name and "
            "a Task-tool slug in field 'model'. Call at the start of every user task, "
            "then run the work via Task with that model."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "task": {"type": "string", "description": "The user task to route."},
                "conversation_id": {"type": "string"},
            },
            "required": ["task"],
        },
    },
]


def respond(msg_id, result=None, error=None):
    out = {"jsonrpc": "2.0", "id": msg_id}
    if error is not None:
        out["error"] = error
    else:
        out["result"] = result
    sys.stdout.write(json.dumps(out) + "\n")
    sys.stdout.flush()


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        mid = msg.get("id")
        method = msg.get("method")
        params = msg.get("params") or {}
        if method == "initialize":
            respond(
                mid,
                {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "cursor-model-router", "version": "1.0.0"},
                },
            )
        elif method == "notifications/initialized":
            continue
        elif method == "tools/list":
            respond(mid, {"tools": TOOL_DEFS})
        elif method == "tools/call":
            name = params.get("name")
            fn = TOOLS.get(name)
            if not fn:
                respond(mid, error={"code": -32601, "message": f"unknown tool {name}"})
                continue
            try:
                respond(mid, fn(params.get("arguments") or {}))
            except Exception as e:
                respond(mid, ok_text(f"error: {e}"))
        elif method == "ping":
            respond(mid, {})
        elif mid is not None:
            respond(mid, error={"code": -32601, "message": f"unknown method {method}"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
