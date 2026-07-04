"""Command-line interface for the gillm GUI control engine."""

from __future__ import annotations

import argparse
import json
import sys


def _print_result(result: dict, *, label: str = "Execution") -> int:
    if result.get("error"):
        print(f"[-] Error: {result['error']}", file=sys.stderr)
    print(f"[+] {label} finished:")
    output = result.get("output")
    data = result.get("data")
    if data:
        print(json.dumps(data if isinstance(data, dict) else {"data": data}, indent=2))
    elif output:
        print(output)
    return 0 if result.get("ok") else 1


def _run_route(args: argparse.Namespace) -> int:
    from gillm.routing import route_for

    plan = route_for(args.app, plugin_connected=args.plugin_connected)
    if args.json:
        print(json.dumps(plan.to_dict(), indent=2))
        return 0 if plan.selected else 1
    env = plan.environment
    print(f"environment: session={env.session or 'unknown'} desktop={env.desktop or '-'}")
    print(
        f"  keyboard={', '.join(env.keyboard_backends) or '-'}; "
        f"focus_detection={env.focus_detection}; vdisplay={env.vdisplay_available}; "
        f"blind_opt_in={env.blind_opt_in}"
    )
    print(f"app: {plan.app.app_id or '-'} (calibration={plan.app.has_calibration}, plugin={plan.app.plugin_connected})")
    print("solutions:")
    for s in plan.solutions:
        mark = "→" if plan.selected is s else ("✓" if s.viable else "✗")
        ext = " [external]" if s.external else ""
        print(f"  {mark} {s.solution_id:<28} {s.confidence:<9}{ext} {s.reason}")
    if plan.selected is None:
        print("no viable solution — see reasons above")
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="gillm: LLM/NLP-driven GUI Control Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    run_parser = subparsers.add_parser("run", help="Execute GUI actions from file")
    run_parser.add_argument("file", help="Path to JSON file containing GUI steps")
    run_parser.add_argument("--dry-run", action="store_true", help="Log actions without executing them")

    nlp_parser = subparsers.add_parser("nlp", help="Translate and execute natural language GUI commands")
    nlp_parser.add_argument("instruction", help="Natural language instruction (e.g. 'focus vscode and type hello')")
    nlp_parser.add_argument("--dry-run", action="store_true", help="Log actions without executing them")

    capture_parser = subparsers.add_parser("capture", help="Take a primary display screen capture")
    capture_parser.add_argument("--scale", type=float, default=0.2, help="Image scale factor (default: 0.2)")

    route_parser = subparsers.add_parser(
        "route",
        help="Pick a control solution for (this environment, an application)",
    )
    route_parser.add_argument("--app", default="", help="Target app id (jetbrains, vscode, cursor, …)")
    route_parser.add_argument(
        "--plugin-connected",
        action="store_true",
        help="Declare that a live IDE-plugin channel exists for the app",
    )
    route_parser.add_argument("--json", action="store_true", help="Emit the full plan as JSON")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "route":
        return _run_route(args)

    try:
        from dsl2gillm import dispatch
    except ImportError:
        print(
            "[-] Error: dsl2gillm not installed. Run: cd gillm && bash packages/install-dev.sh",
            file=sys.stderr,
        )
        return 1

    if args.command == "run":
        try:
            verb = "SIMULATE" if args.dry_run else "EXECUTE"
            line = f"{verb} FILE {args.file}"
            result = dispatch(line, default_file=args.file).to_dict()
            return _print_result(result)
        except Exception as exc:
            print(f"[-] Error: {exc}", file=sys.stderr)
            return 1

    if args.command == "nlp":
        try:
            print(f"[*] Parsing and executing instruction: {args.instruction!r}")
            parse_result = dispatch(
                {"verb": "PARSE", "instruction": args.instruction},
            ).to_dict()
            if not parse_result.get("ok"):
                return _print_result(parse_result, label="Parse")
            steps = (parse_result.get("data") or {}).get("steps", [])
            verb = "SIMULATE" if args.dry_run else "EXECUTE"
            exec_result = dispatch({"verb": verb, "steps": steps}).to_dict()
            return _print_result(exec_result)
        except Exception as exc:
            print(f"[-] Error: {exc}", file=sys.stderr)
            return 1

    if args.command == "capture":
        try:
            print(f"[*] Capturing screenshot (scale={args.scale})...")
            result = dispatch({"verb": "CAPTURE", "scale": args.scale}).to_dict()
            if result.get("ok"):
                print(f"[+] Success: {result.get('output', '').strip()}")
                return 0
            return _print_result(result, label="Capture")
        except Exception as exc:
            print(f"[-] Error: {exc}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
