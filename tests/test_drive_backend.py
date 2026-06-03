"""Tests for :mod:`gillm.injection.drive_backend` (OS profile + keyboard paths)."""

from __future__ import annotations

from unittest import mock

import pytest

from gillm.injection.drive_backend import (
    apply_keyboard_injection,
    format_os_injector_ack,
    try_os_injector_drive,
)
from gillm.injection.errors import InjectorError


def test_try_os_injector_drive_returns_none_when_no_profile(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "gillm.injection.os_injector.try_drive_with_profile",
        lambda **kwargs: None,
    )
    assert try_os_injector_drive("vscode", "hello", True, project=None) is None


def test_try_os_injector_drive_raises_on_error(monkeypatch: pytest.MonkeyPatch) -> None:
    from gillm.injection import os_injector as oi_module

    def raise_error(**kwargs):
        raise oi_module.OsInjectorError("test error")

    monkeypatch.setattr(
        "gillm.injection.os_injector.try_drive_with_profile",
        raise_error,
    )
    with pytest.raises(InjectorError, match="test error"):
        try_os_injector_drive("vscode", "hello", True, project=None)


def test_format_os_injector_ack_includes_target() -> None:
    info = format_os_injector_ack(
        {
            "backend": "os_injector",
            "submitted": True,
            "tool_id": "cursor",
            "dry_run": True,
        },
        submit=False,
        target={"id": "cursor", "label": "Cursor"},
    )
    assert info["backend"] == "os_injector"
    assert info["submitted"] is True
    assert info["tool_id"] == "cursor"
    assert info["dry_run"] is True
    assert info["ide"] == {"id": "cursor", "label": "Cursor"}


def test_apply_keyboard_injection_delegates_to_injector() -> None:
    inj = mock.Mock()
    inj.type_text.return_value = mock.Mock(backend="wtype", submitted=True)
    result = apply_keyboard_injection(inj, "hello", target_id="vscode", submit=True)
    inj.type_text.assert_called_once_with("hello", ide="vscode", submit=True)
    assert result.backend == "wtype"


def test_apply_keyboard_injection_propagates_injector_error() -> None:
    inj = mock.Mock()
    inj.type_text.side_effect = InjectorError("keyboard failed")
    with pytest.raises(InjectorError, match="keyboard failed"):
        apply_keyboard_injection(inj, "hi", target_id="vscode", submit=False)
