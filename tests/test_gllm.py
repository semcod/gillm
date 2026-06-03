"""Unit tests for the gllm package."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock

import pytest

from gllm import DriveOrchestrator
from gllm.focus import get_os_strategy, list_os_strategy_ids, resolve_active_os_strategy
from gllm.focus.strategy import FocusOutcome
from gllm.injection import Injector, InjectorError
from gllm.intents import gui_contract, validate_contract_runtime
from gllm.nlp_bridge import NLPBridgeClient


def test_focus_strategies_registry() -> None:
    strategy_ids = list_os_strategy_ids()
    assert "linux-x11" in strategy_ids
    assert "linux-wayland" in strategy_ids
    assert "darwin" in strategy_ids
    assert "windows" in strategy_ids

    x11 = get_os_strategy("linux-x11")
    assert x11 is not None
    assert x11.id == "linux-x11"

    active = resolve_active_os_strategy()
    assert active is not None


def test_injector_dry_run() -> None:
    # Setup mock Injector that skips actual OS commands
    injector = Injector(which=lambda cmd: "/usr/bin/xdotool" if cmd == "xdotool" else None)
    backends = injector._candidate_backends()
    selected = injector.select_backend()

    # Dry-run type_text
    res = injector.type_text("print('test')", ide="vscode", submit=True, dry_run=True)
    assert res.dry_run is True
    assert res.submitted is True
    assert "13 chars" in res.output


def test_injector_empty_text_error() -> None:
    injector = Injector()
    with pytest.raises(InjectorError, match="refusing to inject empty text"):
        injector.type_text("", dry_run=True)


def test_nlp_bridge_heuristic_parsing() -> None:
    client = NLPBridgeClient()
    steps = client.parse_intent("focus vscode and type hello world")
    assert len(steps) == 2
    assert steps[0]["action"] == "focus_window"
    assert steps[0]["config"]["window_name_hints"] == ["vscode"]
    assert steps[1]["action"] == "inject_keys"
    assert steps[1]["config"]["literal_text"] == "hello world"


def test_orchestrator_execution() -> None:
    orchestrator = DriveOrchestrator()
    steps = [
        {"action": "wait", "config": {"seconds": 0.01}},
    ]
    results = orchestrator.execute_workflow(steps, dry_run=True)
    assert len(results) == 1
    assert results[0]["action"] == "wait"
    assert results[0]["ok"] is True


def test_orchestrator_nlp_drive(monkeypatch: pytest.MonkeyPatch) -> None:
    orchestrator = DriveOrchestrator()
    # Mock focus_target_window to always succeed so we execute both steps
    monkeypatch.setattr(
        orchestrator,
        "focus_target_window",
        lambda window_name_hints: FocusOutcome(ok=True, method="mock"),
    )
    results = orchestrator.drive_natural_language("focus windsurf and type status", dry_run=True)
    assert len(results) == 2
    assert results[0]["action"] == "focus_window"
    assert results[0]["ok"] is True
    assert results[1]["action"] == "inject_keys"


def test_contract_validation() -> None:
    @gui_contract(
        intent="test_intent",
        inputs=("param1",),
        outputs=("result",),
    )
    def dummy_func(param1: str) -> str:
        return "success"

    # Conforms to contract (param1 is present)
    assert validate_contract_runtime(dummy_func, "value") is True

    # Violates contract (missing param1)
    assert validate_contract_runtime(dummy_func, None) is False
