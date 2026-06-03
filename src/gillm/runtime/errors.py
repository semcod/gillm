"""Runtime-level errors for profile and command execution."""


class OsInjectorError(RuntimeError):
    """Raised when profile config or OS injection operations fail."""
