"""NL → dsl2gillm command line (no side effects)."""

from __future__ import annotations

import os
import re

from uri2gillm.nlp2uri import best_uri

from nlp2gillm.llm_backend import LLMBackend, nl_to_dsl_line


def to_dsl(
    prompt: str,
    *,
    file: str | None = None,
    use_llm: bool = False,
    llm_backend: LLMBackend | None = None,
) -> str:
    if use_llm or os.getenv("OPENROUTER_API_KEY"):
        llm_line = nl_to_dsl_line(prompt, file=file, backend=llm_backend)
        if llm_line:
            return llm_line

    hit = best_uri(prompt, file=file)
    if hit and hit.dsl:
        return hit.dsl

    normalized = prompt.strip()
    lower = normalized.lower()

    if lower.startswith(("health", "orient", "actions", "capture", "parse", "validate", "resolve", "execute", "simulate", "focus", "inject")):
        return normalized.upper() if normalized.isupper() else normalized

    match = re.match(r"focus\s+([^\s]+)\s+and\s+type\s+(.+)", normalized, flags=re.IGNORECASE)
    if match:
        return f'PARSE "{normalized}"'

    if "screenshot" in lower or "capture" in lower:
        return "CAPTURE"

    if "health" in lower or "status" in lower:
        return "HEALTH"

    raise ValueError(f"could not map NL to DSL: {prompt!r}")


def apply_nl(prompt: str, *, file: str | None = None) -> dict:
    """Map NL to DSL and dispatch."""
    from dsl2gillm import dispatch

    line = to_dsl(prompt, file=file)
    return dispatch(line, default_file=file).to_dict()
