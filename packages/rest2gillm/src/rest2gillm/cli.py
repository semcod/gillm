"""CLI for rest2gillm."""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="REST API for dsl2gillm")
    sub = parser.add_subparsers(dest="cmd", required=True)
    serve = sub.add_parser("serve", help="Start FastAPI server")
    serve.add_argument("--port", type=int, default=8220)
    serve.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args(argv)

    if args.cmd == "serve":
        import uvicorn

        from rest2gillm.app import create_app

        uvicorn.run(create_app(), host=args.host, port=args.port)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
