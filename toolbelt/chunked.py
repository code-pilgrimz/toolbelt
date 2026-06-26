from itertools import islice
from typing import Iterable, Iterator, TypeVar

T = TypeVar("T")


def chunked(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield successive lists of at most `size` items from `iterable`."""
    if size <= 0:
        raise ValueError("size must be positive")
    it = iter(iterable)
    while batch := list(islice(it, size)):
        yield batch
