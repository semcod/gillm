"""FastMCP server for dsl2gillm."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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
            return dispatch(command, default_file=default_file or None).to_dict()

        @self.app.tool()
        def gillm_run_dsl(script: str, default_file: str = "") -> list[dict[str, Any]]:
            """Execute multiline dsl2gillm script."""
            return [r.to_dict() for r in execute_dsl(script, default_file=default_file or None)]

        @self.app.tool()
        def gillm_run_command_pb(envelope_bytes: bytes, default_file: str = "") -> bytes:
            """Execute protobuf DslEnvelope; returns protobuf DslResult."""
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
            return dispatch(line, default_file=file).to_dict()

    def run(self) -> None:
        self.app.run()


def create_server(name: str = "gillm") -> GillmMCPServer:
    return GillmMCPServer(name=name)


def run_server() -> None:
    create_server().run()


if __name__ == "__main__":
    run_server()
