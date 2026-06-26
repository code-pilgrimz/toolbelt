import pytest

from toolbelt.filesize import human_size, parse_size


def test_human_size_scales_units():
    assert human_size(0) == "0.0 B"
    assert human_size(1536) == "1.5 KB"
    assert human_size(5 * 1024 ** 2) == "5.0 MB"


def test_human_size_rejects_negative():
    with pytest.raises(ValueError):
        human_size(-1)


def test_parse_size_roundtrips():
    assert parse_size("1.5 KB") == 1536
    assert parse_size("5MB") == 5 * 1024 ** 2


def test_parse_size_rejects_garbage():
    with pytest.raises(ValueError):
        parse_size("not a size")
