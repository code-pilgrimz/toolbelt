def normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())


def chunk(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]
# check perf here
# TODO clean this
# TODO clean this
# tidy up
# minor wording
