from toolbelt.strutil import truncate, camel_to_snake


def test_truncate():
    assert truncate("hello world", 8) == "hello..."
    assert truncate("hi", 8) == "hi"


def test_camel_to_snake():
    assert camel_to_snake("HTTPResponse") == "h_t_t_p_response"
    assert camel_to_snake("getValue") == "get_value"
