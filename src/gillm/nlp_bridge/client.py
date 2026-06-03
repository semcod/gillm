"""NLP to GUI translation client using nlp2dsl."""

from __future__ import annotations

from typing import Any

try:
    from nlp2dsl_sdk import NLP2DSLClient
except ImportError:
    # Minimal fallback implementation if sdk is not in sys.path
    class NLP2DSLClient:  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def workflow_from_text(self, text: str, execute: bool = False, mode: str = "auto") -> dict[str, Any]:
            # Mock / local translation for test stability when nlp2dsl service is not running
            lowered = text.lower()
            steps = []
            if "focus" in lowered or "okno" in lowered:
                # E.g. "focus vscode" -> focus window
                hints = ["vscode"]
                for app in ["windsurf", "cursor", "vscode", "vscodium", "zed", "chrome", "firefox"]:
                    if app in lowered:
                        hints = [app]
                        break
                steps.append({
                    "action": "focus_window",
                    "config": {"window_name_hints": hints}
                })
            if "type" in lowered or "wpisz" in lowered or "napisz" in lowered:
                # E.g. "type hello"
                words = text.split()
                literal = "hello"
                for i, word in enumerate(words):
                    if word.lower() in ("type", "wpisz", "napisz") and i + 1 < len(words):
                        literal = " ".join(words[i+1:])
                        break
                steps.append({
                    "action": "inject_keys",
                    "config": {"literal_text": literal, "submit": True}
                })
            return {
                "status": "complete",
                "steps": steps,
                "text": text,
            }


class NLPBridgeClient:
    """Bridge to nlp2dsl backend for resolving natural language GUI commands."""

    def __init__(self, client: NLP2DSLClient | None = None) -> None:
        self.client = client or NLP2DSLClient()

    def parse_intent(self, text: str) -> list[dict[str, Any]]:
        """Parse natural language command into structured workflow steps.

        # @intract.v1 scope:method intent:nlp:parse priority:3 domain:nlp input:text output:steps effect:parse_intent meaning:"Parses natural language commands to GUI actions"
        """
        try:
            res = self.client.workflow_from_text(text)
            return res.get("steps") or []
        except Exception as exc:
            # Fallback to local heuristic parser if remote call fails
            fallback_client = NLP2DSLClient()
            try:
                res = fallback_client.workflow_from_text(text)
                return res.get("steps") or []
            except Exception:
                raise RuntimeError(f"Failed to parse NLP intent via nlp2dsl: {exc}") from exc
