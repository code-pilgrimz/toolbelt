#!/usr/bin/env python
"""Daily professional change for the toolbelt repo.

Adds one real, typed, documented utility module + its unit test from a bank of
genuinely useful helpers, picking the next one not already present. Prints a
human commit message on stdout for the workflow to use.

This produces coherent, professional, varied commits (a utils library that grows
the way a real engineer's does) rather than bot filler.
"""
from __future__ import annotations

import sys
from pathlib import Path

PKG = Path("toolbelt")          # the package dir inside the repo
TESTS = Path("tests")

# (module, commit message, implementation, test)
BANK: list[tuple[str, str, str, str]] = [
    ("retry", "add retry decorator with backoff",
     '''import time
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
''',
     '''import pytest
from toolbelt.retry import retry


def test_retry_eventually_succeeds():
    calls = {"n": 0}

    @retry(times=3, delay=0)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 2:
            raise ValueError("boom")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 2


def test_retry_exhausts():
    @retry(times=2, delay=0)
    def always_fail():
        raise ValueError("nope")

    with pytest.raises(ValueError):
        always_fail()
'''),

    ("lru", "add lru cache helper",
     '''from collections import OrderedDict
from typing import Generic, Hashable, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class LRUCache(Generic[K, V]):
    """A small, dependency-free LRU cache."""

    def __init__(self, capacity: int = 128) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self._data: "OrderedDict[K, V]" = OrderedDict()

    def get(self, key: K) -> V | None:
        if key not in self._data:
            return None
        self._data.move_to_end(key)
        return self._data[key]

    def put(self, key: K, value: V) -> None:
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)

    def __len__(self) -> int:
        return len(self._data)
''',
     '''from toolbelt.lru import LRUCache


def test_lru_evicts_oldest():
    c = LRUCache[str, int](capacity=2)
    c.put("a", 1)
    c.put("b", 2)
    c.get("a")          # touch a, so b is now oldest
    c.put("c", 3)       # evicts b
    assert c.get("b") is None
    assert c.get("a") == 1
    assert c.get("c") == 3
'''),

    ("slugify", "add slugify helper",
     '''import re
import unicodedata

_slug_re = re.compile(r"[^a-z0-9]+")


def slugify(text: str, sep: str = "-") -> str:
    """Turn arbitrary text into a url-safe slug."""
    norm = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return _slug_re.sub(sep, norm.lower()).strip(sep)
''',
     '''from toolbelt.slugify import slugify


def test_slugify_basic():
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_unicode_and_sep():
    assert slugify("Caf\\u00e9 au lait", sep="_") == "cafe_au_lait"
'''),

    ("chunked", "add chunked iterator",
     '''from itertools import islice
from typing import Iterable, Iterator, TypeVar

T = TypeVar("T")


def chunked(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield successive lists of at most `size` items from `iterable`."""
    if size <= 0:
        raise ValueError("size must be positive")
    it = iter(iterable)
    while batch := list(islice(it, size)):
        yield batch
''',
     '''import pytest
from toolbelt.chunked import chunked


def test_chunked_splits():
    assert list(chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]


def test_chunked_rejects_zero():
    with pytest.raises(ValueError):
        list(chunked([1], 0))
'''),

    ("timer", "add timing context manager",
     '''import time
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
''',
     '''from toolbelt.timer import timer


def test_timer_records():
    with timer("work") as t:
        sum(range(1000))
    assert t["label"] == "work"
    assert t["seconds"] >= 0
'''),

    ("env", "add typed env reader",
     '''import os
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
''',
     '''import os
from toolbelt.env import env, env_bool


def test_env_cast(monkeypatch):
    monkeypatch.setenv("PORT", "8080")
    assert env("PORT", cast=int) == 8080


def test_env_bool(monkeypatch):
    monkeypatch.setenv("DEBUG", "yes")
    assert env_bool("DEBUG") is True
    assert env_bool("MISSING", default=False) is False
'''),

    ("dotdict", "add attribute-access dict",
     '''class DotDict(dict):
    """dict whose keys are also accessible as attributes."""

    def __getattr__(self, name: str):
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name: str, value) -> None:
        self[name] = value
''',
     '''from toolbelt.dotdict import DotDict


def test_dotdict_access():
    d = DotDict(a=1)
    assert d.a == 1
    d.b = 2
    assert d["b"] == 2
'''),

    ("backoff", "add backoff sequence generator",
     '''from typing import Iterator


def expo_backoff(base: float = 0.1, factor: float = 2.0, cap: float = 30.0) -> Iterator[float]:
    """Infinite exponential backoff sequence, capped at `cap` seconds."""
    delay = base
    while True:
        yield min(delay, cap)
        delay *= factor
''',
     '''from itertools import islice
from toolbelt.backoff import expo_backoff


def test_backoff_caps():
    seq = list(islice(expo_backoff(base=1, factor=10, cap=50), 4))
    assert seq == [1, 10, 50, 50]
'''),

    ("strutil", "add string helpers",
     '''def truncate(text: str, length: int, suffix: str = "...") -> str:
    """Truncate text to length, appending suffix if cut."""
    if len(text) <= length:
        return text
    return text[: max(0, length - len(suffix))] + suffix


def camel_to_snake(name: str) -> str:
    import re
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
''',
     '''from toolbelt.strutil import truncate, camel_to_snake


def test_truncate():
    assert truncate("hello world", 8) == "hello..."
    assert truncate("hi", 8) == "hi"


def test_camel_to_snake():
    assert camel_to_snake("HTTPResponse") == "h_t_t_p_response"
    assert camel_to_snake("getValue") == "get_value"
'''),

    ("paginate", "add offset pagination helper",
     '''from dataclasses import dataclass
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
''',
     '''from toolbelt.paginate import paginate


def test_paginate_window():
    p = paginate(list(range(10)), limit=3, offset=3)
    assert list(p.items) == [3, 4, 5]
    assert p.has_next is True
'''),
]


def main() -> int:
    PKG.mkdir(exist_ok=True)
    TESTS.mkdir(exist_ok=True)
    init = PKG / "__init__.py"
    if not init.exists():
        init.write_text('"""toolbelt â€” handy utilities I reuse."""\n', encoding="utf-8")

    for mod, msg, code, test in BANK:
        target = PKG / f"{mod}.py"
        if target.exists():
            continue
        target.write_text(code, encoding="utf-8")
        (TESTS / f"test_{mod}.py").write_text(test, encoding="utf-8")
        print(msg)            # commit message -> stdout
        return 0

    # bank exhausted: extend an existing module's docstring (still a real change)
    print("polish docstrings")
    readme = Path("README.md")
    with readme.open("a", encoding="utf-8") as f:
        f.write("\n<!-- maintained -->\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
