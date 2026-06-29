from typing import Iterator


def expo_backoff(base: float = 0.1, factor: float = 2.0, cap: float = 30.0) -> Iterator[float]:
    """Infinite exponential backoff sequence, capped at `cap` seconds."""
    delay = base
    while True:
        yield min(delay, cap)
        delay *= factor
