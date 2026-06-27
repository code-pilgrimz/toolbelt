import os
from typing import Callable, TypeVar

T = TypeVar("T")


def env(key: str, default: T | None = None, cast: Callable[[str], T] = str) -> T | None:
    """Read an env var with an optional cast and default."""
    raw = os.getenv(key)
    if raw is None:
        return default
    return cast(raw)


def env_bool(key: str, default: bool = False) -> bool:
    raw = os.getenv(key)
    if raw is None:
        return default
    return raw.lower() in {"1", "true", "yes", "on"}
