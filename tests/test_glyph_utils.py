import pytest
from mjrengo.glyph_utils import (
    escape_left_brace,
    unescape_left_brace,
    protect_left_brace,
    restore_left_brace,
    ESCAPED_LB,
    TAG_LB,
)


def test_escape_left_brace():
    assert escape_left_brace("{{abc") == f"{ESCAPED_LB}abc"
    assert escape_left_brace("no brace") == "no brace"
    assert escape_left_brace("") == ""
    assert escape_left_brace(None) == ""

def test_unescape_left_brace():
    assert unescape_left_brace(f"{ESCAPED_LB}abc") == "{{abc"
    assert unescape_left_brace("no token") == "no token"

def test_protect_left_brace():
    assert protect_left_brace("{{abc") == f"{TAG_LB}abc"
    assert protect_left_brace("no brace") == "no brace"

def test_restore_left_brace():
    assert restore_left_brace(f"{TAG_LB}abc") == "{abc"
    assert restore_left_brace("no token") == "no token"

def test_roundtrip_escape_unescape():
    text = "{{MJ0001}}"
    escaped = escape_left_brace(text)
    restored = unescape_left_brace(escaped)
    assert restored == text

def test_roundtrip_protect_restore():
    text = "{{MJ0001}}"
    protected = protect_left_brace(text)
    restored = restore_left_brace(protected)
    assert restored == "{MJ0001}}"
