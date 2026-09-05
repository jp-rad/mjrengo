"""
Tag parsing and placeholder escaping utilities for glyph resolution.

This module provides the `TagParser` class to process syntax tokens like `{glyph ...}`
while safely handling escaped double-brace sequences like `{{`.
"""

from collections.abc import Callable
import re

# Control character used as a placeholder for escaped opening braces '{{'
MARK_LB: str = "\u0002"

# Matches a single tag enclosed in single braces: {glyph_name key=value ...}
TAG_PATTERN: re.Pattern[str] = re.compile(
    r"\{"
    r"(?P<content>[^\}]+)"
    r"\}",
    re.DOTALL,
)


class TagParser:
    """
    Utility class for handling brace escaping, restoration, and tag parsing.

    Provides mechanisms to temporarily protect escaped braces (`{{`), parse
    and substitute tag matches, and restore the preserved sequences into either
    unescaped (`{`) or original escaped (`{{`) representations.
    """

    @staticmethod
    def escape_tokens(text: str) -> str:
        """
        Replace escaped double-brace sequences with a temporary control character.

        Args:
            text (str): Input text containing potential `{{` escape sequences.

        Returns:
            str: Text with `{{` replaced by the internal placeholder character.
        """
        return text.replace("{{", MARK_LB)

    @staticmethod
    def restore_tokens_preserve_escape(text: str) -> str:
        """
        Restore internal placeholders back to double-brace escape sequences (`{{`).

        Args:
            text (str): Processed text containing placeholder characters.

        Returns:
            str: Text with placeholders restored to `{{`.
        """
        return text.replace(MARK_LB, "{{")

    @staticmethod
    def restore_tokens_unescape(text: str) -> str:
        """
        Restore internal placeholders to single unescaped braces (`{`).

        Args:
            text (str): Processed text containing placeholder characters.

        Returns:
            str: Text with placeholders converted to `{`.
        """
        return text.replace(MARK_LB, "{")

    @staticmethod
    def parse_tag_content(content: str) -> tuple[str, dict[str, str]]:
        """
        Extract the primary glyph name and key-value properties from tag content.

        Args:
            content (str): Raw string inside a tag (e.g., `"MJ012345 b=1 v=v6_02_201"`).

        Returns:
            tuple[str, dict[str, str]]: A tuple containing:
                - `glyph_name` (str): The primary identifier token (empty string if missing).
                - `properties` (dict[str, str]): Key-value pairs parsed from `key=value` tokens.

        Examples:
            >>> TagParser.parse_tag_content("MJ012345 b=1 v=6.02")
            ('MJ012345', {'b': '1', 'v': '6.02'})
        """
        tokens = content.strip().split()
        if not tokens:
            return "", {}

        glyph_name = tokens[0]
        properties: dict[str, str] = {}
        for token in tokens[1:]:
            if "=" in token:
                key, value = token.split("=", 1)
                properties[key] = value

        return glyph_name, properties

    @classmethod
    def process_pipeline(
        cls,
        text: str,
        replacer: Callable[[re.Match[str]], str],
        unescape: bool = True,
    ) -> str:
        """
        Execute the full transformation pipeline: escape -> substitute -> restore.

        Args:
            text (str): Target string to transform.
            replacer (Callable[[re.Match[str]], str]): Callback function passed to `re.Pattern.sub`.
            unescape (bool): If `True`, converts `{{` to `{` (for rendering).
                If `False`, preserves `{{` as `{{` (for normalization). Defaults to `True`.

        Returns:
            str: Fully transformed string after tag substitution and brace restoration.
        """
        escaped = cls.escape_tokens(text)
        substituted = TAG_PATTERN.sub(replacer, escaped)

        if unescape:
            return cls.restore_tokens_unescape(substituted)
        return cls.restore_tokens_preserve_escape(substituted)

