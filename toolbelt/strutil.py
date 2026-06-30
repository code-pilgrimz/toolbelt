def truncate(text: str, length: int, suffix: str = "...") -> str:
    """Truncate text to length, appending suffix if cut."""
    if len(text) <= length:
        return text
    return text[: max(0, length - len(suffix))] + suffix


def camel_to_snake(name: str) -> str:
    import re
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
