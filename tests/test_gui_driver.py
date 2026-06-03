"""Tests for GuiDriver protocol and dry-run driver."""

from __future__ import annotations

from gillm.contracts.driver import ActionPlan, WindowTarget
from gillm.drivers.dry_run import DryRunGuiDriver
from gillm.runtime.backend_selector import BackendSelector, session_backend_order


def test_session_backend_order_wayland_prefers_wtype() -> None:
    order = session_backend_order("wayland")
    assert order[0] == "wtype"
    assert "ydotool" in order


def test_backend_selector_forced_backend() -> None:
    selector = BackendSelector(session="wayland", which=lambda n: "/bin/wtype" if n == "wtype" else None)
    assert selector.select_backend() == "wtype"


def test_dry_run_driver_executes_chat_plan() -> None:
    driver = DryRunGuiDriver(session="wayland")
    plan = ActionPlan.chat_inject_and_submit(text="hello", tool_id="cursor", submit=True)
    outcome = driver.execute(plan)
    assert outcome.ok is True
    assert outcome.backend == "dry_run"
    assert len(outcome.steps) == 3
    assert "type_text:cursor" in driver.log[1]


def test_dry_run_driver_probe() -> None:
    driver = DryRunGuiDriver(session="x11")
    status = driver.probe()
    assert status.dry_run is True
    assert status.backends.get("dry_run") is True


def test_action_plan_chat_factory() -> None:
    plan = ActionPlan.chat_inject_and_submit(text="x", tool_id="cursor")
    assert plan.intent == "gui.chat.inject_and_submit"
    assert plan.target.tool_id == "cursor"
    assert plan.steps[0]["action"] == "focus"
