from itertools import islice
from toolbelt.backoff import expo_backoff


def test_backoff_caps():
    seq = list(islice(expo_backoff(base=1, factor=10, cap=50), 4))
    assert seq == [1, 10, 50, 50]
