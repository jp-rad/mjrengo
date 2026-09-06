import pytest
from tofurengo.ucs import ucs_to_glyph, glyph_to_ucs


def test_decode_ucs():
    assert ucs_to_glyph("U+4E00") == "一"
    assert ucs_to_glyph("U+4E00 U+E0100") == "一" + "\U000E0100"

def test_encode_ucs():
    assert glyph_to_ucs("一") == "U+4E00"
    assert glyph_to_ucs("一" + "\U000E0100") == "U+4E00 U+E0100"
