"""
Unicode and UCS code point conversion utilities for glyph processing.

This module provides bidirectional conversion functions between native Python
glyph character representations and formatted UCS code point sequences.
"""

import re

# Matches hexadecimal code point formats like 'U+845B', 'U+E0102', '845B', or 'e0102'
UCS_CODEPOINT_PATTERN: re.Pattern[str] = re.compile(
    r"(?:U\+)?([0-9A-Fa-f]{4,6})",
    re.IGNORECASE,
)


def glyph_to_ucs(glyph: str) -> str:
    """
    Convert a native Unicode glyph representation into a space-separated UCS string.

    Encodes characters (including surrogate pairs and Ideographic Variation Sequences)
    into formatted "U+XXXX" hexadecimal code point strings.

    Args:
        glyph (str): Native Unicode string representing a single glyph or IVS sequence.

    Returns:
        str: Space-separated UCS code point sequence formatted as "U+XXXX".
    """
    return " ".join(f"U+{ord(char):X}" for char in glyph)


def ucs_to_glyph(ucs_seq: str) -> str:
    """
    Convert a space-separated UCS code point sequence into a native Unicode glyph string.

    Decodes formatted "U+XXXX" hexadecimal strings back into standard Unicode characters,
    handling supplementary planes and Ideographic Variation Sequences (IVS).

    Args:
        ucs_seq (str): Space-separated UCS code point string (e.g., "U+845B U+E0102").

    Returns:
        str: Decoded native Unicode glyph string.
    """
    code_points = UCS_CODEPOINT_PATTERN.findall(ucs_seq)
    return "".join(chr(int(cp, 16)) for cp in code_points)

