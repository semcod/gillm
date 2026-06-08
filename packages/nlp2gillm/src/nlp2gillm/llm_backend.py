"""LLM backend for nlp2gillm NL → DSL translation."""

from __future__ import annotations

import json
import os
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class LLMBackend(Protocol):
    def complete(
        self,
        *,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        ...


class LitellmBackend:
    def complete(
        self,
        *,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        import litellm  # type: ignore

        kwargs: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        if response_format is not None:
            kwargs["response_format"] = response_format
        response = litellm.completion(**kwargs)
        return (response.choices[0].message.content or "").strip()


def get_backend(backend: LLMBackend | None = None) -> LLMBackend:
    if backend is not None:
        return backend
    return LitellmBackend()


def nl_to_dsl_line(
    prompt: str,
    *,
    file: str | None = None,
    model: str | None = None,
    backend: LLMBackend | None = None,
) -> str | None:
    """Convert NL prompt to a single dsl2gillm command line via LLM."""
    resolved_model = model or os.getenv("LLM_MODEL", "openrouter/qwen/qwen3-coder-next")
    llm = get_backend(backend)
    system = (
        "Convert user request to ONE dsl2gillm command line. "
        "Allowed verbs: HEALTH, ORIENT, PARSE, ACTIONS, VALIDATE, RESOLVE, CAPTURE, "
        "EXECUTE, SIMULATE, FOCUS, INJECT. "
        'Return JSON: {"dsl": "..."}'
    )
    try:
        content = llm.complete(
            model=resolved_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps({"prompt": prompt, "file": file or ""})},
            ],
            response_format={"type": "json_object"},
        )
        data = json.loads(content or "{}")
        dsl = str(data.get("dsl", "")).strip()
        return dsl or None
    except Exception:
        return None
