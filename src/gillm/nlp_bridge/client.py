"""NLP to GUI translation client using nlp2dsl (optional) or local heuristics."""

from __future__ import annotations

from typing import Any

from gillm.nlp_bridge.heuristic_parser import parse_intent_heuristic

try:
    from nlpshim.client import NLPBridgeClient as _ShimClient
except ImportError:  # pragma: no cover - optional NLP stack
    _ShimClient = None

# Backward-compat alias for consumers importing from this module
_heuristic_parse_intent = parse_intent_heuristic


class NLPBridgeClient:
    """Bridge to nlp2dsl when installed; otherwise a small heuristic parser."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._delegate = _ShimClient(*args, **kwargs) if _ShimClient is not None else None

    def parse_intent(self, command: str) -> list[dict[str, Any]]:
        if self._delegate is not None:
            return self._delegate.parse_intent(command)
        return _heuristic_parse_intent(command)


__all__ = ["NLPBridgeClient"]
