from toolbelt.core import normalize, chunk


def test_normalize():
    assert normalize("  Hello   World ") == "hello world"


def test_chunk():
    assert list(chunk([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
# TODO clean this
