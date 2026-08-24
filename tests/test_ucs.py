import pytest
from mjrengo.ucs import decode_ucs, encode_ucs


def test_decode_ucs():
    assert decode_ucs("U+4E00") == "一"
    assert decode_ucs("U+4E00 U+E0100") == "一" + "\U000E0100"

def test_encode_ucs():
    assert encode_ucs("一") == "U+4E00"
    assert encode_ucs("一" + "\U000E0100") == "U+4E00 U+E0100"
