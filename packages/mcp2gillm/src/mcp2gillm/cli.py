"""CLI for mcp2gillm."""

from __future__ import annotations

import argparse

from mcp2gillm.server import run_server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MCP server for dsl2gillm")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("serve", help="Start MCP stdio server")
    args = parser.parse_args(argv)
    if args.cmd == "serve":
        run_server()
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
