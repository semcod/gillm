"""Interactive shell for dsl2gillm."""

from __future__ import annotations

import json

from dsl2gillm.bus import execute_dsl_line


def run_shell(*, default_file: str | None = None, json_out: bool = False) -> int:
    print("cli2gillm shell — dsl2gillm control (exit/quit to leave)")
    code = 0
    while True:
        try:
            line = input("gillm> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        if line.lower() in {"exit", "quit", ":q"}:
            break
        result = execute_dsl_line(line, default_file=default_file)
        if json_out:
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        else:
            if result.error:
                print(f"error: {result.error}")
            if result.output:
                print(result.output.rstrip())
        if not result.ok:
            code = 1
    return code
