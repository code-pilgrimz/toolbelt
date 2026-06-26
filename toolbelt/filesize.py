"""Human-readable file sizes: convert between byte counts and strings like '1.5 KB'."""
from __future__ import annotations

import re

_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]
_FACTORS = {unit: 1024 ** i for i, unit in enumerate(_UNITS)}
_PATTERN = re.compile(r"^([\d.]+)\s*([A-Za-z]+)$")


def human_size(num_bytes: int, precision: int = 1) -> str:
    """Format a byte count as a human-readable string.

    >>> human_size(1536)
    '1.5 KB'
    """
    if num_bytes < 0:
        raise ValueError("num_bytes must be non-negative")
    size = float(num_bytes)
    for unit in _UNITS:
        if size < 1024 or unit == _UNITS[-1]:
            return f"{size:.{precision}f} {unit}"
        size /= 1024
    raise AssertionError("unreachable")  # pragma: no cover


def parse_size(text: str) -> int:
    """Parse a human-readable size back into bytes.

    >>> parse_size("1.5 KB")
    1536
    """
    match = _PATTERN.match(text.strip())
    if not match:
        raise ValueError(f"cannot parse size: {text!r}")
    value, unit = float(match.group(1)), match.group(2).upper()
    if unit not in _FACTORS:
        raise ValueError(f"unknown unit: {unit!r}")
    return int(value * _FACTORS[unit])
