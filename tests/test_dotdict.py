from toolbelt.dotdict import DotDict


def test_dotdict_access():
    d = DotDict(a=1)
    assert d.a == 1
    d.b = 2
    assert d["b"] == 2
