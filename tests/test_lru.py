from toolbelt.lru import LRUCache


def test_lru_evicts_oldest():
    c = LRUCache[str, int](capacity=2)
    c.put("a", 1)
    c.put("b", 2)
    c.get("a")          # touch a, so b is now oldest
    c.put("c", 3)       # evicts b
    assert c.get("b") is None
    assert c.get("a") == 1
    assert c.get("c") == 3
