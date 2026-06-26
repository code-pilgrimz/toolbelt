import time
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def timer(label: str = "elapsed") -> Iterator[dict]:
    """Context manager that records wall-clock time into a dict."""
    result = {"label": label, "seconds": 0.0}
    start = time.perf_counter()
    try:
        yield result
    finally:
        result["seconds"] = time.perf_counter() - start
