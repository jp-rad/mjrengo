"""
Replacer and normalization closures for glyph tags.

This module provides factory functions such as `make_replace_fn` to generate
regex substitution callbacks used during text processing and normalization pipelines.
"""

from collections.abc import Callable
import re
from typing import Any

from mjrengo.types import GlyphError, ReplaceFn


def make_replace_fn(
    glyph_table: dict[str, dict[str, Any]],
    set_name: str,
) -> ReplaceFn:
    """
    Factory that creates a normalization replacement callback for regex matching.

    The generated closure inspects incoming match objects, looks up glyph entries in
    the provided `glyph_table`, validates their active status, and formats them into
    canonical tag strings: `{<glyph> b=<b> v=<v> set=<set_name>}`.

    If validation fails (glyph missing or inactive), an appropriate `GlyphError`
    is appended to the mutable `errors` list, and the match is left unmodified.

    Args:
        glyph_table (dict[str, dict[str, Any]]): Dictionary mapping glyph identifiers
            to property maps containing `b`, `v`, and `active` keys.
        set_name (str): The target dataset/set identifier assigned to normalized tags.

    Returns:
        ReplaceFn: A callback closure with signature `(re.Match[str], list[GlyphError]) -> str`.

    Examples:
        >>> table = {"MJ012345": {"b": "U+4E00", "v": "v6_02", "active": True}}
        >>> replace_fn = make_replace_fn(table, set_name="mj")
        >>> errors = []
        >>> # Assuming `match` matched `{MJ012345}`
        >>> # replace_fn(match, errors) -> "{MJ012345 b=U+4E00 v=v6_02 set=mj}"
    """

    def replace_fn(match: re.Match[str], errors: list[GlyphError]) -> str:
        """
        Process a regex tag match, performing lookup, validation, and string normalization.

        Args:
            match (re.Match[str]): Regex match object corresponding to a tag.
            errors (list[GlyphError]): Mutable list to store encountered validation errors.

        Returns:
            str: Normalized tag string if valid; original matched text otherwise.
        """
        # Extract tag interior content (support named group 'content' or fallback to entire match)
        content = match.group("content") if "content" in match.groupdict() else match.group(0)
        tokens = content.strip("{} ").split()

        if not tokens:
            return match.group(0)

        glyph = tokens[0]

        # 1. Glyph existence validation
        if glyph not in glyph_table:
            code = "error.glyph.not_found"
            msg = f"Glyph '{glyph}' does not exist in dataset '{set_name}'."
            errors.append(
                GlyphError(
                    code=code,
                    message=f"{code}: {msg}",
                    details={"glyph": glyph, "set": set_name},
                )
            )
            return match.group(0)

        entry = glyph_table[glyph]

        # 2. Glyph active status validation
        if not entry.get("active", True):
            code = "error.glyph.archived"
            msg = f"Glyph '{glyph}' is archived or inactive."
            errors.append(
                GlyphError(
                    code=code,
                    message=f"{code}: {msg}",
                    details={"glyph": glyph, "set": set_name},
                )
            )
            return match.group(0)

        # 3. Canonical tag formatting
        b_val = entry.get("b", "")
        v_val = entry.get("v", "")

        return f"{{{glyph} b={b_val} v={v_val} set={set_name}}}"

    return replace_fn

