"""Command-line interface for the gillm GUI control engine."""

from __future__ import annotations

import argparse
import json
import sys

from gillm.orchestrator.drive import DriveOrchestrator


def main() -> int:
    parser = argparse.ArgumentParser(
        description="gillm: LLM/NLP-driven GUI Control Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Command: run (execute direct actions or DSL file)
    run_parser = subparsers.add_parser("run", help="Execute GUI actions from file")
    run_parser.add_argument("file", help="Path to JSON file containing GUI steps")
    run_parser.add_argument("--dry-run", action="store_true", help="Log actions without executing them")

    # Command: nlp (execute natural language command)
    nlp_parser = subparsers.add_parser("nlp", help="Translate and execute natural language GUI commands")
    nlp_parser.add_argument("instruction", help="Natural language instruction (e.g. 'focus vscode and type hello')")
    nlp_parser.add_argument("--dry-run", action="store_true", help="Log actions without executing them")

    # Command: capture (take screen capture)
    capture_parser = subparsers.add_parser("capture", help="Take a primary display screen capture")
    capture_parser.add_argument("--scale", type=float, default=0.2, help="Image scale factor (default: 0.2)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    orchestrator = DriveOrchestrator(log_fn=lambda msg: print(f"[*] {msg}"))

    if args.command == "run":
        try:
            with open(args.file, encoding="utf-8") as f:
                steps = json.load(f)
            if not isinstance(steps, list):
                print("[-] Error: Workflow file must contain a JSON list of steps", file=sys.stderr)
                return 1
            results = orchestrator.execute_workflow(steps, dry_run=args.dry_run)
            print("[+] Execution finished:")
            print(json.dumps(results, indent=2))
            return 0
        except Exception as exc:
            print(f"[-] Error: {exc}", file=sys.stderr)
            return 1

    elif args.command == "nlp":
        try:
            print(f"[*] Parsing and executing instruction: {args.instruction!r}")
            results = orchestrator.drive_natural_language(args.instruction, dry_run=args.dry_run)
            print("[+] Execution finished:")
            print(json.dumps(results, indent=2))
            return 0
        except Exception as exc:
            print(f"[-] Error: {exc}", file=sys.stderr)
            return 1

    elif args.command == "capture":
        try:
            print(f"[*] Capturing screenshot (scale={args.scale})...")
            img = orchestrator.capture_screenshot(scale=args.scale)
            print(f"[+] Success: Captured {img.width}x{img.height} screen at scale {img.scale}")
            return 0
        except Exception as exc:
            print(f"[-] Error: {exc}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
