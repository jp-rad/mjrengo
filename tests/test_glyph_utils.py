import pytest
from mjrengo.glyph_utils import (
    escape_left_brace,
    unescape_left_brace,
    render_escape_left_brace,
    render_unescape_left_brace,
    ESC_LB,
    TAG_LB,
)


def test_escape_left_brace():
    assert escape_left_brace("{{abc") == f"{ESC_LB}abc"
    assert escape_left_brace("no brace") == "no brace"
    assert escape_left_brace("") == ""
    assert escape_left_brace(None) == ""


def test_unescape_left_brace():
    assert unescape_left_brace(f"{ESC_LB}abc") == "{{abc"
    assert unescape_left_brace("no token") == "no token"


def test_render_escape_left_brace():
    assert render_escape_left_brace("{{abc") == f"{TAG_LB}abc"
    assert render_escape_left_brace("no brace") == "no brace"


def test_render_unescape_left_brace():
    assert render_unescape_left_brace(f"{TAG_LB}abc") == "{abc"
    assert render_unescape_left_brace("no token") == "no token"


def test_roundtrip_escape_unescape():
    text = "{{MJ123456}}"
    escaped = escape_left_brace(text)
    restored = unescape_left_brace(escaped)
    assert restored == text


def test_roundtrip_render_escape_unescape():
    text = "{{MJ123456}}"
    protected = render_escape_left_brace(text)
    restored = render_unescape_left_brace(protected)
    assert restored == "{MJ123456}}"
