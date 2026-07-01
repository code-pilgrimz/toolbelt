from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    items: Sequence[T]
    total: int
    limit: int
    offset: int

    @property
    def has_next(self) -> bool:
        return self.offset + self.limit < self.total


def paginate(items: Sequence[T], limit: int = 50, offset: int = 0) -> Page[T]:
    window = items[offset: offset + limit]
    return Page(items=window, total=len(items), limit=limit, offset=offset)
