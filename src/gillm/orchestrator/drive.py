"""Orchestrator for parsing, validating, and executing GUI control sequences."""

from __future__ import annotations

import logging
import time
from typing import Any, Callable

from gillm.capture import capture_primary_rgb_wayland_fallback
from gillm.focus import resolve_active_os_strategy
from gillm.focus.strategy import FocusOutcome, KeySequence
from gillm.injection import Injector
from gillm.intents import gui_contract, validate_contract_runtime
from gillm.nlp_bridge import NLPBridgeClient

logger = logging.getLogger("gillm.orchestrator")


class DriveOrchestrator:
    """Consolidated orchestrator for GUI drive tasks."""

    def __init__(
        self,
        nlp_client: NLPBridgeClient | None = None,
        log_fn: Callable[[str], None] | None = None,
    ) -> None:
        self.nlp_bridge = nlp_client or NLPBridgeClient()
        self.log_fn = log_fn or logger.info
        self.injector = Injector(log=self.log_fn)

    def log(self, message: str) -> None:
        if self.log_fn:
            self.log_fn(message)

    @gui_contract(
        intent="gui:focus",
        inputs=("window_name_hints",),
        outputs=("outcome",),
        meaning="Focuses the window matching the given hints.",
    )
    def focus_target_window(self, window_name_hints: tuple[str, ...]) -> FocusOutcome:
        """Focus the target window using the active OS strategy.

        # @intract.v1 scope:method intent:gui:focus priority:3 domain:gui input:window_name_hints output:FocusOutcome effect:focus_window meaning:"Focus the target window using active OS strategy."
        """
        validate_contract_runtime(self.focus_target_window, window_name_hints=window_name_hints)
        strategy = resolve_active_os_strategy()
        self.log(f"orchestrator: focusing window via active strategy {strategy.id} hints={window_name_hints}")
        return strategy.focus_window(window_name_hints)

    @gui_contract(
        intent="gui:inject",
        inputs=("text", "submit"),
        outputs=("result",),
        meaning="Injects key strokes / text into the active window.",
    )
    def inject_text(
        self,
        text: str,
        ide: str = "default",
        submit: bool = True,
        dry_run: bool = False,
    ) -> Any:
        """Inject text using the core Injector.

        # @intract.v1 scope:method intent:gui:inject priority:3 domain:gui input:text,ide,submit,dry_run output:result effect:inject_keys meaning:"Injects keystrokes or types text into the IDE."
        """
        validate_contract_runtime(self.inject_text, text=text, ide=ide, submit=submit, dry_run=dry_run)
        self.log(f"orchestrator: injecting text '{text[:40]}' submit={submit} dry_run={dry_run}")
        return self.injector.type_text(text, ide=ide, submit=submit, dry_run=dry_run)

    @gui_contract(
        intent="gui:capture",
        inputs=(),
        outputs=("screenshot",),
        meaning="Captures the primary monitor screen.",
    )
    def capture_screenshot(self, scale: float | None = None) -> Any:
        """Capture primary screen.

        # @intract.v1 scope:method intent:gui:capture priority:3 domain:gui input:scale output:CapturedImage effect:capture_primary_rgb_wayland_fallback meaning:"Captures screenshot of primary display."
        """
        validate_contract_runtime(self.capture_screenshot, scale=scale)
        self.log(f"orchestrator: capturing screen, scale={scale}")
        return capture_primary_rgb_wayland_fallback(scale=scale)

    def execute_step(self, step: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
        """Execute a single workflow step.

        # @intract.v1 scope:method intent:execute:step priority:3 domain:gui input:step,dry_run output:result effect:execute_step meaning:"Executes one GUI control DSL step."
        """
        action = step.get("action")
        config = step.get("config") or {}
        self.log(f"orchestrator: executing step action={action} config={config}")

        if action == "focus_window":
            hints = config.get("window_name_hints")
            if isinstance(hints, str):
                hints = [hints]
            hints_tuple = tuple(hints or [])
            outcome = self.focus_target_window(hints_tuple)
            return {"action": action, "ok": outcome.ok, "detail": outcome.detail, "method": outcome.method}

        elif action in ("inject_keys", "type_text"):
            literal_text = config.get("literal_text") or config.get("text") or ""
            submit = config.get("submit", True)
            ide = config.get("ide", "default")
            res = self.inject_text(literal_text, ide=ide, submit=submit, dry_run=dry_run)
            return {"action": action, "ok": True, "detail": res.to_dict()}

        elif action == "capture_screen":
            scale = config.get("scale")
            img = self.capture_screenshot(scale=scale)
            return {
                "action": action,
                "ok": True,
                "detail": f"Captured {img.width}x{img.height} screen at scale {img.scale}",
            }

        elif action == "wait":
            seconds = float(config.get("seconds") or 1.0)
            if not dry_run:
                time.sleep(seconds)
            return {"action": action, "ok": True, "detail": f"Waited {seconds}s"}

        else:
            raise ValueError(f"Unknown workflow action {action!r}")

    def execute_workflow(self, steps: list[dict[str, Any]], dry_run: bool = False) -> list[dict[str, Any]]:
        """Execute a list of workflow steps.

        # @intract.v1 scope:method intent:execute:workflow priority:3 domain:gui input:steps,dry_run output:results effect:execute_workflow meaning:"Executes a list of GUI actions sequentially."
        """
        results = []
        for step in steps:
            res = self.execute_step(step, dry_run=dry_run)
            results.append(res)
            if not res.get("ok", True):
                self.log(f"orchestrator: step failed: {res}")
                break
        return results

    def drive_natural_language(self, command: str, dry_run: bool = False) -> list[dict[str, Any]]:
        """Translate natural language command into actions and execute them.

        # @intract.v1 scope:method intent:gui:drive_nlp priority:3 domain:gui input:command,dry_run output:results effect:drive_natural_language meaning:"Parses and runs natural language GUI command."
        """
        self.log(f"orchestrator: received NL command: '{command}'")
        steps = self.nlp_bridge.parse_intent(command)
        if not steps:
            self.log("orchestrator: no actions parsed from command")
            return []
        self.log(f"orchestrator: parsed steps: {steps}")
        return self.execute_workflow(steps, dry_run=dry_run)
