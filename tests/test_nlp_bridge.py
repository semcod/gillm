"""Regression tests for gillm.nlp_bridge heuristic parser and client delegation."""

from __future__ import annotations

from typing import Any

import pytest

from gillm.nlp_bridge import NLPBridgeClient, parse_intent_heuristic
from gillm.nlp_bridge.client import _heuristic_parse_intent


class _FakeShimClient:
    """Stub for the optional nlpshim.client NLPBridgeClient."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def parse_intent(self, command: str) -> list[dict[str, Any]]:
        return [{"action": "shim_parsed", "config": {"command": command}}]


class TestHeuristicParseIntent:
    """Focused regression tests for the offline heuristic parser."""

    def test_focus_and_type_pattern(self) -> None:
        steps = _heuristic_parse_intent("focus vscode and type hello world")
        assert len(steps) == 2
        assert steps[0] == {
            "action": "focus_window",
            "config": {"window_name_hints": ["vscode"]},
        }
        assert steps[1] == {
            "action": "inject_keys",
            "config": {"literal_text": "hello world"},
        }

    def test_case_insensitive(self) -> None:
        steps = _heuristic_parse_intent("FOCUS VSCODE AND TYPE HELLO")
        assert len(steps) == 2
        assert steps[0]["config"]["window_name_hints"] == ["vscode"]
        assert steps[1]["config"]["literal_text"] == "HELLO"

    def test_extra_whitespace_trimmed(self) -> None:
        steps = _heuristic_parse_intent("  focus   windsurf   and   type   code  ")
        assert steps[0]["config"]["window_name_hints"] == ["windsurf"]
        # The regex captures everything after "type " as group 2, so extra
        # spaces at the end are stripped by .strip() but internal ones remain.
        assert steps[1]["config"]["literal_text"] == "code"

    def test_no_match_returns_empty_list(self) -> None:
        assert _heuristic_parse_intent("") == []
        assert _heuristic_parse_intent("open file") == []
        assert _heuristic_parse_intent("focus vscode") == []
        assert _heuristic_parse_intent("focus vscode and type") == []

    def test_window_name_with_underscore_or_dot(self) -> None:
        steps = _heuristic_parse_intent("focus code.exe and type hi")
        assert steps[0]["config"]["window_name_hints"] == ["code.exe"]


def test_backward_compat_alias_is_same_object() -> None:
    from gillm.nlp_bridge.heuristic_parser import parse_intent_heuristic
    assert _heuristic_parse_intent is parse_intent_heuristic


class TestNLPBridgeClient:
    """Focused regression tests for NLPBridgeClient delegation."""

    def test_delegates_to_shim_when_available(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "gillm.nlp_bridge.client._ShimClient", _FakeShimClient
        )
        client = NLPBridgeClient()
        steps = client.parse_intent("do something")
        assert steps == [{"action": "shim_parsed", "config": {"command": "do something"}}]

    def test_falls_back_to_heuristic_when_shim_unavailable(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr("gillm.nlp_bridge.client._ShimClient", None)
        client = NLPBridgeClient()
        steps = client.parse_intent("focus code and type print('hi')")
        assert len(steps) == 2
        assert steps[0]["action"] == "focus_window"
        assert steps[1]["action"] == "inject_keys"

    def test_init_passes_args_to_shim(self, monkeypatch: pytest.MonkeyPatch) -> None:
        captured: list[Any] = []
        original_init = _FakeShimClient.__init__

        def recording_init(self: Any, *args: Any, **kwargs: Any) -> None:
            captured.append((args, kwargs))
            original_init(self, *args, **kwargs)

        monkeypatch.setattr(
            "gillm.nlp_bridge.client._ShimClient",
            type("RecordingShim", (_FakeShimClient,), {"__init__": recording_init}),
        )
        NLPBridgeClient("arg1", kw="val")
        assert captured == [(('arg1',), {'kw': 'val'})]
