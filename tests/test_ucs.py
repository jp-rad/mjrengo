import pytest
from mjrengo.ucs import ucs_to_str, str_to_ucs


def test_decode_ucs():
    assert ucs_to_str("U+4E00") == "一"
    assert ucs_to_str("U+4E00 U+E0100") == "一" + "\U000E0100"

def test_encode_ucs():
    assert str_to_ucs("一") == "U+4E00"
    assert str_to_ucs("一" + "\U000E0100") == "U+4E00 U+E0100"
