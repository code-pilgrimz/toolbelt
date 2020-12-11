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
# off-by-one, fixed
# revisit later
# TODO clean this


def safe_normalize(text):
    return normalize(text) if text else ""
# check perf here
# left a note for myself
# TODO clean this
# check perf here
# tidy up
# tidy up
# check perf here
# revisit later
