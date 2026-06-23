import pytest
from toolbelt.retry import retry


def test_retry_eventually_succeeds():
    calls = {"n": 0}

    @retry(times=3, delay=0)
    def flaky():
        calls["n"] += 1
        if calls["n"] < 2:
            raise ValueError("boom")
        return "ok"

    assert flaky() == "ok"
    assert calls["n"] == 2


def test_retry_exhausts():
    @retry(times=2, delay=0)
    def always_fail():
        raise ValueError("nope")

    with pytest.raises(ValueError):
        always_fail()
