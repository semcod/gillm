"""Auto-generated pydantic models — do not edit by hand.

Regenerate: python -m dsl2gillm.codegen
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class ActionsCommand(BaseModel):
    model_config = ConfigDict(extra='forbid')

    verb: Literal['ACTIONS']

class CaptureCommand(BaseModel):
    model_config = ConfigDict(extra='forbid')

    verb: Literal['CAPTURE']
    scale: float = 0.2

class ExecuteCommand(BaseModel):
    model_config = ConfigDict(extra='forbid')

    verb: Literal['EXECUTE']
    file: str | None = None
    steps: list[dict[str, Any]] | None = None
    dry_run: bool = False

class FocusCommand(BaseModel):
    model_config = ConfigDict(extra='forbid')

    verb: Literal['FOCUS']
    hints: str
    dry_run: bool = False

class HealthCommand(BaseModel):
    model_config = ConfigDict(extra='forbid')

    verb: Literal['HEALTH']

class InjectCommand(BaseModel):
    model_config = ConfigDict(extra='forbid')

    verb: Literal['INJECT']
    text: str
    ide: str = 'default'
    submit: bool = True
    dry_run: bool = False

class OrientCommand(BaseModel):
    model_config = ConfigDict(extra='forbid')

    verb: Literal['ORIENT']

class ParseCommand(BaseModel):
    model_config = ConfigDict(extra='forbid')

    verb: Literal['PARSE']
    instruction: str

class ResolveCommand(BaseModel):
    model_config = ConfigDict(extra='forbid')

    verb: Literal['RESOLVE']
    prompt: str

class SimulateCommand(BaseModel):
    model_config = ConfigDict(extra='forbid')

    verb: Literal['SIMULATE']
    file: str | None = None
    steps: list[dict[str, Any]] | None = None

class ValidateCommand(BaseModel):
    model_config = ConfigDict(extra='forbid')

    verb: Literal['VALIDATE']
    file: str | None = None
    steps: list[dict[str, Any]] | None = None

MODEL_BY_VERB: dict[str, type[BaseModel]] = {
    'ACTIONS': ActionsCommand,
    'CAPTURE': CaptureCommand,
    'EXECUTE': ExecuteCommand,
    'FOCUS': FocusCommand,
    'HEALTH': HealthCommand,
    'INJECT': InjectCommand,
    'ORIENT': OrientCommand,
    'PARSE': ParseCommand,
    'RESOLVE': ResolveCommand,
    'SIMULATE': SimulateCommand,
    'VALIDATE': ValidateCommand,
}
