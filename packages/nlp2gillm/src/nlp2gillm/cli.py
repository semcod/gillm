"""CLI for nlp2gillm."""

from __future__ import annotations

import argparse
import json
import sys

from nlp2gillm.to_dsl import apply_nl, to_dsl


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Natural language → dsl2gillm")
    sub = parser.add_subparsers(dest="cmd", required=True)

    to_dsl_parser = sub.add_parser("to-dsl", help="NL → DSL line only")
    to_dsl_parser.add_argument("prompt")
    to_dsl_parser.add_argument("--file", default="")

    apply_parser = sub.add_parser("apply", help="NL → DSL → dispatch")
    apply_parser.add_argument("prompt")
    apply_parser.add_argument("--file", default="")
    apply_parser.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)
    default_file = args.file or None

    if args.cmd == "to-dsl":
        try:
            print(to_dsl(args.prompt, file=default_file))
            return 0
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1

    if args.cmd == "apply":
        try:
            result = apply_nl(args.prompt, file=default_file)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if result.get("error"):
                print(f"error: {result['error']}", file=sys.stderr)
            if result.get("output"):
                print(str(result["output"]).rstrip())
        return 0 if result.get("ok") else 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
