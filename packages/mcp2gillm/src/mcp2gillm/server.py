"""FastMCP server for dsl2gillm."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


_TRUE_VALUES = frozenset({"1", "true", "yes", "on"})


def _enabled(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in _TRUE_VALUES


def _workspace_root() -> Path:
    return Path(os.getenv("GILLM_MCP_WORKSPACE_ROOT", ".")).expanduser().resolve()


def _require_within_workspace(raw_path: str) -> None:
    candidate = Path(raw_path).expanduser().resolve(strict=False)
    try:
        candidate.relative_to(_workspace_root())
    except ValueError as exc:
        raise PermissionError(
            "gillm MCP workflow path is outside GILLM_MCP_WORKSPACE_ROOT"
        ) from exc


def _guard_payload(payload: dict[str, Any], *, default_file: str = "") -> None:
    verb = str(payload.get("verb", "")).upper()
    workflow_file = str(payload.get("file") or default_file or "")
    if workflow_file:
        _require_within_workspace(workflow_file)

    if verb == "CAPTURE" and not _enabled("GILLM_MCP_ALLOW_CAPTURE"):
        raise PermissionError(
            "screen capture through MCP is disabled; set GILLM_MCP_ALLOW_CAPTURE=1 to enable it"
        )

    live_command = verb in {"EXECUTE", "FOCUS", "INJECT"} and not bool(
        payload.get("dry_run", False)
    )
    if live_command and not _enabled("GILLM_MCP_ALLOW_EXECUTE"):
        raise PermissionError(
            "live gillm execution through MCP is disabled; "
            "use DRY_RUN true or set GILLM_MCP_ALLOW_EXECUTE=1"
        )


def _guard_command(command: str | bytes, *, default_file: str = "") -> None:
    from dsl2gillm.codec import envelope_from_bytes, parse_text

    payload = envelope_from_bytes(command) if isinstance(command, bytes) else parse_text(
        command, default_file=default_file or None
    )
    if payload:
        _guard_payload(payload, default_file=default_file)


def _require_fastmcp():
    try:
        from mcp.server.fastmcp import FastMCP
        return FastMCP
    except ImportError as exc:
        raise RuntimeError("Install mcp: pip install mcp") from exc


@dataclass
class GillmMCPServer:
    name: str = "gillm"

    def __post_init__(self) -> None:
        FastMCP = _require_fastmcp()
        self.app = FastMCP(self.name)
        self._register_tools()

    def _register_tools(self) -> None:
        from dsl2gillm.bus import dispatch, execute_dsl
        from dsl2gillm.pb_codec import encode_result_protobuf
        from nlp2gillm.to_dsl import to_dsl

        @self.app.tool()
        def gillm_run_command(command: str, default_file: str = "") -> dict[str, Any]:
            """Execute one dsl2gillm command line."""
            _guard_command(command, default_file=default_file)
            return dispatch(command, default_file=default_file or None).to_dict()

        @self.app.tool()
        def gillm_run_dsl(script: str, default_file: str = "") -> list[dict[str, Any]]:
            """Execute multiline dsl2gillm script."""
            for line in script.splitlines():
                if line.strip() and not line.lstrip().startswith("#"):
                    _guard_command(line, default_file=default_file)
            return [r.to_dict() for r in execute_dsl(script, default_file=default_file or None)]

        @self.app.tool()
        def gillm_run_command_pb(envelope_bytes: bytes, default_file: str = "") -> bytes:
            """Execute protobuf DslEnvelope; returns protobuf DslResult."""
            _guard_command(envelope_bytes, default_file=default_file)
            result = dispatch(envelope_bytes, default_file=default_file or None)
            return encode_result_protobuf(result)

        @self.app.tool()
        def gillm_to_dsl(prompt: str, default_file: str = "") -> str:
            """Map natural language to dsl2gillm command line."""
            return to_dsl(prompt, file=default_file or None)

        @self.app.tool()
        def gillm_health() -> dict[str, Any]:
            """Legacy granular tool — HEALTH query."""
            return dispatch("HEALTH").to_dict()

        @self.app.tool()
        def gillm_parse(instruction: str) -> dict[str, Any]:
            """Legacy granular tool — PARSE query."""
            return dispatch(f'PARSE "{instruction}"').to_dict()

        @self.app.tool()
        def gillm_execute(file: str, dry_run: bool = False) -> dict[str, Any]:
            """Legacy granular tool — EXECUTE workflow file."""
            line = f"EXECUTE FILE {file}"
            if dry_run:
                line += " DRY_RUN true"
            _guard_command(line, default_file=file)
            return dispatch(line, default_file=file).to_dict()

    def run(self) -> None:
        self.app.run()


def create_server(name: str = "gillm") -> GillmMCPServer:
    return GillmMCPServer(name=name)


def run_server() -> None:
    create_server().run()


if __name__ == "__main__":
    run_server()
