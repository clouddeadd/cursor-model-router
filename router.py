#!/usr/bin/env python3
"""Pick a named model slug the Cursor Task tool can actually run."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

LOG = Path.home() / ".cursor" / "router-log" / "picks.jsonl"

# Slugs accepted by Cursor's Task tool when this picker was built.
MODELS = {
    "claude-opus-5-thinking-high": {
        "display": "Claude Opus 5 Thinking High",
    },
    "claude-opus-5-5-medium": {
        "display": "Claude Opus 5.5 Medium",
    },
    "claude-fable-5-1-thinking-high": {
        "display": "Claude Fable 5.1 Thinking High",
    },
    "grok-4.7-high-fast": {
        "display": "Grok 4.7 High Fast",
    },
    "cursor-grok-4.6-high-fast": {
        "display": "Grok 4.6 High Fast",
    },
    "composer-2.5-fast": {
        "display": "Composer 2.5 Fast",
    },
    "gpt-5.3-codex": {
        "display": "GPT-5.3 Codex",
    },
    "gpt-5.6-sol-medium": {
        "display": "GPT-5.6 Sol Medium",
    },
    "gemini-3.8-flash-high": {
        "display": "Gemini 3.8 Flash High",
    },
    "muse-spark-1.3-high": {
        "display": "Muse Spark 1.3 High",
    },
}

RULES = [
    {
        "id": "claude-opus-5-thinking-high",
        "why": "Careful, high-stakes work.",
        "any": [
            r"\b(security|privacy|credentials|production|incident|outage)\b",
            r"\b(high[- ]stakes|careful)\b",
        ],
    },
    {
        "id": "claude-fable-5-1-thinking-high",
        "why": "Long review.",
        "any": [
            r"\b(review|audit)\b",
            r"\b(entire|whole|across the (repo|codebase))\b",
        ],
    },
    {
        "id": "gpt-5.3-codex",
        "why": "Code-heavy implementation / refactor.",
        "any": [
            r"\b(refactor|codex|migrate|typescript|python module)\b",
        ],
    },
    {
        "id": "composer-2.5-fast",
        "why": "Narrow mechanical edit.",
        "any": [
            r"\b(rename|typo|format|lint|one.?liner)\b",
            r"\bjust (fix|change|update)\b",
        ],
    },
    {
        "id": "grok-4.7-high-fast",
        "why": "Implementation / debug / product work.",
        "any": [
            r"\b(implement|build|fix|debug|code|api|ui|deploy|test|mcp|tool|model)\b",
        ],
    },
]


def _match(task: str) -> tuple[str, str]:
    text = task.lower()
    for rule in RULES:
        if any(re.search(p, text, re.I) for p in rule["any"]):
            return rule["id"], rule["why"]
    return "grok-4.7-high-fast", "Named fallback."


def pick(task: str, conversation_id: str | None = None) -> dict:
    task = (task or "").strip()
    if not task:
        return {"error": "task is required"}
    model_id, why = _match(task)
    spec = MODELS[model_id]
    out = {
        "MODEL": spec["display"],
        "model": model_id,
        "why": why,
        "task": task[:240],
        "ts": datetime.now(timezone.utc).isoformat(),
        "conversation_id": conversation_id,
    }
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(out, ensure_ascii=False) + "\n")
    return out


def format_display(picked: dict) -> str:
    if picked.get("error"):
        return picked["error"]
    return (
        f"MODEL: {picked['MODEL']}\n"
        f"SLUG: {picked['model']}\n"
        f"WHY: {picked['why']}"
    )


if __name__ == "__main__":
    import sys

    print(format_display(pick(" ".join(sys.argv[1:]) or "build an mcp tool")))
