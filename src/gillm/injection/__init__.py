"""GUI injection backends — keyboard, mouse, clipboard."""

from gillm.injection.errors import InjectorError
from gillm.injection.injector import BackendStatus, InjectionResult, Injector
from gillm.injection.os_injector import (
    OsInjectorError,
    OsInjectorProfile,
    inject_with_profile,
    load_profile,
    save_profile,
    try_drive_with_profile,
)

__all__ = [
    "BackendStatus",
    "InjectionResult",
    "Injector",
    "InjectorError",
    "OsInjectorError",
    "OsInjectorProfile",
    "inject_with_profile",
    "load_profile",
    "save_profile",
    "try_drive_with_profile",
]
