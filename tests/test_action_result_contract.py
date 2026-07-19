"""Deterministic contract tests for GUI action outcomes."""

from __future__ import annotations

import ast
from pathlib import Path

from gillm.contracts import (
    GUI_ACTION_RESULT_V1,
    ActionResult,
    ExecutionOutcome,
    gui_action_result_v1_schema,
)

ROOT = Path(__file__).resolve().parents[1]


def test_action_result_is_versioned_and_stably_hashed() -> None:
    first = ExecutionOutcome(
        ok=False,
        intent="gui.chat.inject_and_submit",
        backend="ydotool",
        evidence=["window-focused"],
        recovery=["retry after focus"],
        retryable=True,
        reason="submit unverified",
        steps=[ActionResult(ok=True, backend="ydotool")],
    )
    second = ExecutionOutcome(
        ok=False,
        intent="gui.chat.inject_and_submit",
        backend="ydotool",
        evidence=["window-focused"],
        recovery=["retry after focus"],
        retryable=True,
        reason="submit unverified",
        steps=[ActionResult(ok=True, backend="ydotool")],
    )

    assert first.schema == GUI_ACTION_RESULT_V1
    assert first.canonical_json() == second.canonical_json()
    assert first.result_hash == second.result_hash
    assert len(first.result_hash) == 64
    assert first.to_dict()["result_hash"] == first.result_hash


def test_action_result_schema_is_packaged() -> None:
    schema = gui_action_result_v1_schema()
    assert schema["properties"]["schema"]["const"] == GUI_ACTION_RESULT_V1
    assert "result_hash" in schema["required"]


def test_gillm_runtime_has_no_reverse_koru_import() -> None:
    found: list[str] = []
    for path in (ROOT / "src/gillm").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] == "koru":
                found.append(path.relative_to(ROOT).as_posix())
            if isinstance(node, ast.Import):
                if any(alias.name.split(".")[0] == "koru" for alias in node.names):
                    found.append(path.relative_to(ROOT).as_posix())
    assert found == []
