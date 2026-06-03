"""Registry + resolver for :class:`OsStrategy` implementations."""

from __future__ import annotations

from gllm.focus.strategy import OsStrategy

_REGISTRY: list[OsStrategy] = []


def register_os_strategy(strategy: OsStrategy) -> None:
    """Register ``strategy``."""
    existing = [s for s in _REGISTRY if s.id == strategy.id]
    if existing:
        for old in existing:
            _REGISTRY.remove(old)
    _REGISTRY.append(strategy)


def get_os_strategy(strategy_id: str) -> OsStrategy | None:
    """Return the strategy with ``id == strategy_id`` if registered."""
    for strategy in _REGISTRY:
        if strategy.id == strategy_id:
            return strategy
    return None


def list_os_strategy_ids() -> tuple[str, ...]:
    """Return the ids of every registered strategy."""
    return tuple(s.id for s in _REGISTRY)


def resolve_active_os_strategy() -> OsStrategy:
    """Return the strategy whose ``matches_current_environment`` is true."""
    for strategy in _REGISTRY:
        if strategy.matches_current_environment():
            return strategy
    if not _REGISTRY:
        raise RuntimeError(
            "gllm.focus.registry: no OsStrategy registered; "
            "did import of gllm.focus fail?"
        )
    return _REGISTRY[-1]


__all__ = [
    "get_os_strategy",
    "list_os_strategy_ids",
    "register_os_strategy",
    "resolve_active_os_strategy",
]
