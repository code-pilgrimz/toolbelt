from toolbelt.slugify import slugify


def test_slugify_basic():
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_unicode_and_sep():
    assert slugify("Caf\u00e9 au lait", sep="_") == "cafe_au_lait"
