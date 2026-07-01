from toolbelt.paginate import paginate


def test_paginate_window():
    p = paginate(list(range(10)), limit=3, offset=3)
    assert list(p.items) == [3, 4, 5]
    assert p.has_next is True
