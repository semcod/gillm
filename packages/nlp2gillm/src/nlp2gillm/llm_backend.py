"""LLM backend for nlp2gillm NL → DSL translation."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from dsl2gillm.grammar import parse_line

from nlp2gillm.contracts import response_format, validate_payload


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
        if model.startswith("openrouter/"):
            app_name = (
                os.getenv("OPENROUTER_APP_NAME", "").strip()
                or Path.cwd().name
                or "gillm"
            )
            headers = {"X-Title": app_name}
            app_url = os.getenv("OPENROUTER_APP_URL", "").strip()
            if app_url:
                headers["HTTP-Referer"] = app_url
            kwargs["extra_headers"] = headers
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
    resolved_model = model or os.getenv("LLM_MODEL", "openrouter/z-ai/glm-5.2")
    llm = get_backend(backend)
    system = (
        "Convert user request to ONE dsl2gillm command line. "
        "Allowed verbs: HEALTH, ORIENT, PARSE, ACTIONS, VALIDATE, RESOLVE, CAPTURE, "
        "EXECUTE, SIMULATE, FOCUS, INJECT. "
        'Return one DslLineResponse 1.0.0 JSON object: '
        '{"contractVersion":"1.0.0","dsl":"..."}'
    )
    try:
        content = llm.complete(
            model=resolved_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps({"prompt": prompt, "file": file or ""})},
            ],
            response_format=response_format(),
        )
        data = json.loads(content)
        validate_payload(data)
        dsl = data["dsl"].strip()
        return dsl if parse_line(dsl, default_file=file) else None
    except Exception:  # noqa: BLE001 - provider failures deliberately trigger rules fallback
        return None
