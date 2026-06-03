"""Koru-specific intent mapping for gillm ActionPlan execution."""

from __future__ import annotations

from typing import Any

from gillm.contracts.driver import ActionPlan, ActionStep, WindowTarget

DEFAULT_STRATEGY = (
    "plugin_bridge",
    "command_palette",
    "clipboard_paste",
    "keyboard_fallback",
)


def drive_payload_to_action_plan(payload: dict[str, Any]) -> ActionPlan:
    """Convert a structured Koru/gillm drive payload into an ActionPlan."""
    intent = str(payload.get("intent") or "gui.chat.inject_and_submit")
    target_raw = payload.get("target") if isinstance(payload.get("target"), dict) else {}
    input_raw = payload.get("input") if isinstance(payload.get("input"), dict) else {}
    strategy_raw = payload.get("strategy") if isinstance(payload.get("strategy"), dict) else {}
    validation = payload.get("validation") if isinstance(payload.get("validation"), dict) else {}

    tool_id = str(target_raw.get("ide") or target_raw.get("tool_id") or "default")
    hints = target_raw.get("window_hints") or target_raw.get("hints") or (tool_id,)
    if isinstance(hints, str):
        hints = (hints,)
    profile_id = target_raw.get("profile") or target_raw.get("profile_id")

    text = str(input_raw.get("text") or payload.get("text") or "")
    submit = bool(input_raw.get("submit", payload.get("submit", True)))

    steps: list[ActionStep] = []
    if "steps" in payload and isinstance(payload["steps"], list):
        steps = [step for step in payload["steps"] if isinstance(step, dict)]
    else:
        prefer = strategy_raw.get("prefer") or DEFAULT_STRATEGY
        steps = _steps_from_prefer(prefer, text=text, submit=submit, tool_id=tool_id)

    return ActionPlan(
        intent=intent,
        target=WindowTarget(
            hints=tuple(str(h) for h in hints),
            tool_id=tool_id,
            profile_id=str(profile_id) if profile_id else None,
        ),
        steps=steps,
        validation=validation,
    )


def koru_drive_to_payload(
    *,
    text: str,
    ide: str = "auto",
    submit: bool = True,
    prefer: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Build the YAML-shaped drive contract Koru should send to gillm."""
    tool_id = ide if ide and ide != "auto" else "default"
    return {
        "intent": "ide.chat.submit",
        "target": {"ide": tool_id, "lane": "default"},
        "input": {"text": text, "submit": submit},
        "strategy": {"prefer": list(prefer or DEFAULT_STRATEGY)},
        "validation": {
            "expect": [
                "window_focused",
                "text_submitted" if submit else "text_pasted",
            ],
        },
    }


def _steps_from_prefer(
    prefer: list[Any] | tuple[Any, ...],
    *,
    text: str,
    submit: bool,
    tool_id: str,
) -> list[ActionStep]:
    """Map high-level strategy names to concrete gillm execution steps."""
    normalized = [str(item).strip().lower() for item in prefer]
    steps: list[ActionStep] = []
    if any(item in normalized for item in ("plugin_bridge", "command_palette")):
        steps.append({"action": "focus", "target": tool_id})
    if any(item in normalized for item in ("clipboard_paste", "keyboard_fallback", "plugin_bridge")):
        steps.append({"action": "type_text", "text": text})
    if submit:
        steps.append({"action": "submit", "tool_id": tool_id})
    if not steps:
        return ActionPlan.chat_inject_and_submit(text=text, tool_id=tool_id, submit=submit).steps
    return steps
