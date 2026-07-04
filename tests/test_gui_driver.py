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


def test_backend_selector_excludes_wtype_when_compositor_unsupported(monkeypatch):
    from gillm.runtime import backend_selector as bs

    bs._WTYPE_PROBE_CACHE.clear()
    monkeypatch.setattr(
        bs,
        "_wtype_compositor_supported",
        lambda path: (False, "Compositor does not support the virtual keyboard protocol"),
    )
    sel = bs.BackendSelector(
        session="wayland",
        which=lambda name: f"/usr/bin/{name}" if name in {"wtype", "ydotool"} else None,
    )
    assert sel.candidate_backends() == ["ydotool"]
    rows = {name: (ok, detail) for name, ok, detail in sel.probe()}
    assert rows["wtype"][0] is False
    assert "virtual keyboard" in rows["wtype"][1]


def test_wtype_probe_subprocess_failure_is_cached(monkeypatch):
    # fresh module instance: the autouse fixture stubs the probe on the
    # canonical module, and this test needs the real implementation
    import importlib.util
    import subprocess as sp

    from gillm.runtime import backend_selector as canonical

    spec = importlib.util.spec_from_file_location("bs_fresh", canonical.__file__)
    bs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bs)

    calls: list[list[str]] = []

    def fake_run(cmd, **_kwargs):
        calls.append(cmd)
        return sp.CompletedProcess(cmd, 1, stdout="", stderr="Compositor does not support X")

    monkeypatch.setattr(bs.subprocess, "run", fake_run)
    ok1, detail1 = bs._wtype_compositor_supported("/usr/bin/wtype")
    ok2, _ = bs._wtype_compositor_supported("/usr/bin/wtype")
    assert ok1 is False and ok2 is False
    assert "Compositor" in detail1
    assert len(calls) == 1  # cached after first probe
