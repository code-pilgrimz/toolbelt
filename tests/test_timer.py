from toolbelt.timer import timer


def test_timer_records():
    with timer("work") as t:
        sum(range(1000))
    assert t["label"] == "work"
    assert t["seconds"] >= 0
