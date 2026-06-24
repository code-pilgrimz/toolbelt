import re
import unicodedata

_slug_re = re.compile(r"[^a-z0-9]+")


def slugify(text: str, sep: str = "-") -> str:
    """Turn arbitrary text into a url-safe slug."""
    norm = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return _slug_re.sub(sep, norm.lower()).strip(sep)
