"""NLP to GUI translation client using nlp2dsl (optional) or local heuristics."""

from __future__ import annotations

import re
from typing import Any

try:
    from nlpshim.client import NLPBridgeClient as _ShimClient
except ImportError:  # pragma: no cover - optional NLP stack
    _ShimClient = None


def _heuristic_parse_intent(command: str) -> list[dict[str, Any]]:
    """Minimal offline parser for ``focus <ide> and type <text>`` patterns."""
    text = command.strip()
    match = re.match(
        r"focus\s+([^\s]+)\s+and\s+type\s+(.+)",
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return []
    ide = match.group(1).strip().lower()
    literal = match.group(2).strip()
    return [
        {"action": "focus_window", "config": {"window_name_hints": [ide]}},
        {"action": "inject_keys", "config": {"literal_text": literal}},
    ]


class NLPBridgeClient:
    """Bridge to nlp2dsl when installed; otherwise a small heuristic parser."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._delegate = _ShimClient(*args, **kwargs) if _ShimClient is not None else None

    def parse_intent(self, command: str) -> list[dict[str, Any]]:
        if self._delegate is not None:
            return self._delegate.parse_intent(command)
        return _heuristic_parse_intent(command)


__all__ = ["NLPBridgeClient"]
