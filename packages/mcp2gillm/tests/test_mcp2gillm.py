from pathlib import Path

import pytest


def test_create_server() -> None:
    from mcp2gillm.server import create_server

    server = create_server()
    assert server.name == "gillm"


def test_live_execution_is_disabled_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    from mcp2gillm.server import _guard_command

    monkeypatch.delenv("GILLM_MCP_ALLOW_EXECUTE", raising=False)
    with pytest.raises(PermissionError, match="GILLM_MCP_ALLOW_EXECUTE"):
        _guard_command('INJECT TEXT "hello"')


def test_dry_run_and_explicit_execution_are_allowed(monkeypatch: pytest.MonkeyPatch) -> None:
    from mcp2gillm.server import _guard_command

    monkeypatch.delenv("GILLM_MCP_ALLOW_EXECUTE", raising=False)
    _guard_command('INJECT TEXT "hello" DRY_RUN true')
    monkeypatch.setenv("GILLM_MCP_ALLOW_EXECUTE", "1")
    _guard_command('INJECT TEXT "hello"')


def test_screen_capture_requires_separate_opt_in(monkeypatch: pytest.MonkeyPatch) -> None:
    from mcp2gillm.server import _guard_command

    monkeypatch.delenv("GILLM_MCP_ALLOW_CAPTURE", raising=False)
    with pytest.raises(PermissionError, match="GILLM_MCP_ALLOW_CAPTURE"):
        _guard_command("CAPTURE")
    monkeypatch.setenv("GILLM_MCP_ALLOW_CAPTURE", "yes")
    _guard_command("CAPTURE")


def test_workflow_path_is_confined(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from mcp2gillm.server import _guard_command

    monkeypatch.setenv("GILLM_MCP_WORKSPACE_ROOT", str(tmp_path))
    _guard_command(f"VALIDATE FILE {tmp_path / 'workflow.json'}")
    with pytest.raises(PermissionError, match="GILLM_MCP_WORKSPACE_ROOT"):
        _guard_command("VALIDATE FILE ../workflow.json")
