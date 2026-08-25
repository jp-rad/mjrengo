import re

def decode_ucs(seq: str) -> str:
    """
    Convert a UCS codepoint sequence (e.g., 'U+4E00' or 'U+4E00 U+E0100')
    into a single Unicode character (base + IVS).
    """
    cps = re.findall(r"U\+([0-9A-Fa-f]{4,6})", seq)
    return "".join(chr(int(cp, 16)) for cp in cps)


def encode_ucs(char: str) -> str:
    """
    Convert a single Unicode character (including IVS) into
    a UCS codepoint sequence (e.g., 'U+4E00 U+E0100').
    """
    return " ".join(f"U+{ord(c):X}" for c in char)
