import re


def decode_ucs(seq: str) -> str:
    """
    Decode a UCS codepoint sequence into a Unicode string.
    Supports BMP + Supplementary Plane + IVS.
    """
    cps = re.findall(r"U\+([0-9A-Fa-f]{4,6})", seq)
    return "".join(chr(int(cp, 16)) for cp in cps)


def encode_ucs(char: str) -> str:
    """
    Encode a Unicode string (including IVS) into a UCSSeq.
    """
    return " ".join(f"U+{ord(c):X}" for c in char)
