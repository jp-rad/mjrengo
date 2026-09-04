"""
UCS sequence conversion module for Glyph Tag processing.

This module provides utility functions to convert between Unicode character strings
and UCS code point sequence strings (e.g., "U+845B U+E0102").
"""

import re

# Regex pattern to capture hex code points formatted as "U+XXXX"
UCS_CODEPOINT_PATTERN: re.Pattern = re.compile(r"U\+([0-9A-Fa-f]{4,6})")


def ucs_to_str(ucs_seq: str) -> str:
    """
    Convert a UCS code point sequence into a native Unicode string.

    Handles standard Unicode characters, supplementary planes, and Ideographic
    Variation Sequences (IVS).

    Args:
        ucs_seq (str): Space-separated UCS code point string (e.g., "U+845B U+E0102").

    Returns:
        str: Decoded Unicode character string.

    Examples:
        >>> ucs_to_str("U+845B U+E0102")
        '葛\udb40\udd02'
    """
    code_points = UCS_CODEPOINT_PATTERN.findall(ucs_seq)
    return "".join(chr(int(cp, 16)) for cp in code_points)


def str_to_ucs(text: str) -> str:
    """
    Encode a native Unicode string into a UCS code point sequence string.

    Args:
        text (str): Input Unicode string (may include IVS sequences).

    Returns:
        str: Space-separated UCS code point sequence formatted as "U+XXXX".

    Examples:
        >>> str_to_ucs("葛")
        'U+845B'
    """
    return " ".join(f"U+{ord(char):X}" for char in text)

