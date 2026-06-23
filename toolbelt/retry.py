import time
from functools import wraps
from typing import Callable, TypeVar

T = TypeVar("T")


def retry(times: int = 3, delay: float = 0.1, backoff: float = 2.0,
          exceptions: tuple[type[Exception], ...] = (Exception,)) -> Callable:
    """Retry a callable on failure with exponential backoff."""

    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        @wraps(fn)
        def wrapper(*args, **kwargs) -> T:
            wait, last = delay, None
            for _ in range(times):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:  # noqa: PERF203
                    last = exc
                    time.sleep(wait)
                    wait *= backoff
            raise last  # type: ignore[misc]

        return wrapper

    return decorator
