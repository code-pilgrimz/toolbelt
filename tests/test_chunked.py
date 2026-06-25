import pytest
from toolbelt.chunked import chunked


def test_chunked_splits():
    assert list(chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]


def test_chunked_rejects_zero():
    with pytest.raises(ValueError):
        list(chunked([1], 0))
