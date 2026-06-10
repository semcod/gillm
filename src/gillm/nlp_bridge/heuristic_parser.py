"""Offline heuristic parser for simple natural-language GUI commands."""

from __future__ import annotations

import re
from typing import Any


FOCUS_TYPE_PATTERN = re.compile(
    r"focus\s+([^\s]+)\s+and\s+type\s+(.+)",
    flags=re.IGNORECASE,
)


def parse_intent_heuristic(command: str) -> list[dict[str, Any]]:
    """Parse ``focus <ide> and type <text>`` patterns without external NLP."""
    text = command.strip()
    match = FOCUS_TYPE_PATTERN.match(text)
    if not match:
        return []
    ide = match.group(1).strip().lower()
    literal = match.group(2).strip()
    return [
        {"action": "focus_window", "config": {"window_name_hints": [ide]}},
        {"action": "inject_keys", "config": {"literal_text": literal}},
    ]


__all__ = ["parse_intent_heuristic", "FOCUS_TYPE_PATTERN"]
