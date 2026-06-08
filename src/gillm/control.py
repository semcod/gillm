"""Thin shim — delegate legacy callers to dsl2gillm bus."""

from __future__ import annotations

from typing import Any


def dispatch_health() -> dict[str, Any]:
    from dsl2gillm import dispatch

    return dispatch("HEALTH").to_dict()


def dispatch_parse(instruction: str) -> dict[str, Any]:
    from dsl2gillm import dispatch

    return dispatch({"verb": "PARSE", "instruction": instruction}).to_dict()


def dispatch_execute(*, file: str | None = None, steps: list[dict[str, Any]] | None = None, dry_run: bool = False) -> dict[str, Any]:
    from dsl2gillm import dispatch

    payload: dict[str, Any] = {"verb": "EXECUTE", "dry_run": dry_run}
    if file:
        payload["file"] = file
    if steps is not None:
        payload["steps"] = steps
    return dispatch(payload, default_file=file).to_dict()


def dispatch_validate(*, file: str | None = None, steps: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    from dsl2gillm import dispatch

    payload: dict[str, Any] = {"verb": "VALIDATE"}
    if file:
        payload["file"] = file
    if steps is not None:
        payload["steps"] = steps
    return dispatch(payload, default_file=file).to_dict()
