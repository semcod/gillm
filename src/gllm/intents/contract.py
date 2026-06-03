"""GUI Interaction Intents Contracts and Validation.

Integrates with semcod/intract to define and validate contracts.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, TypeVar

logger = logging.getLogger("gllm.intents")

F = TypeVar("F", bound=Callable[..., Any])


def gui_contract(
    intent: str,
    scope: str = "function",
    priority: int = 3,
    domain: str = "gui",
    inputs: tuple[str, ...] = (),
    outputs: tuple[str, ...] = (),
    required: tuple[str, ...] = (),
    forbidden: tuple[str, ...] = (),
    meaning: str = "",
) -> Callable[[F], F]:
    """Decorator to document and validate GUI interaction contracts.

    Inlines intract metadata comments so that the static/dynamic contract
    validators in semcod/intract can verify the codebase integrity.
    """

    def decorator(func: F) -> F:
        # Build the contract metadata dictionary
        meta = {
            "intent": intent,
            "scope": scope,
            "priority": priority,
            "domain": domain,
            "inputs": inputs,
            "outputs": outputs,
            "required": required,
            "forbidden": forbidden,
            "meaning": meaning,
        }
        setattr(func, "__intract_contract__", meta)
        return func

    return decorator


def validate_contract_runtime(func: Callable[..., Any], *args: Any, **kwargs: Any) -> bool:
    """Validate that the call conforms to the contract defined on ``func``."""
    contract = getattr(func, "__intract_contract__", None)
    if not contract:
        return True

    # Validate inputs presence
    func_code = func.__code__
    varnames = func_code.co_varnames[:func_code.co_argcount]

    # Map args and kwargs to argument names
    passed_args = {}
    for i, arg in enumerate(args):
        if i < len(varnames):
            passed_args[varnames[i]] = arg
    passed_args.update(kwargs)

    # Check required inputs are not empty/None
    for req in contract.get("inputs", []):
        if req not in passed_args or passed_args[req] is None:
            logger.warning(
                f"Contract warning: function '{func.__name__}' missing "
                f"required input parameter '{req}'"
            )
            return False

    return True
