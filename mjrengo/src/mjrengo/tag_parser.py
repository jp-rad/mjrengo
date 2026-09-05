"""
Tag parsing, replacement protocols, and placeholder escaping utilities.

This module provides data models and utilities for tag-based string processing,
including `TagIssue` for capturing validation warnings and errors, the `ReplaceFn`
protocol for substitution callbacks, and `TagParser` for managing double-brace escaping.
"""

from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Any, Protocol

# Control character used as a placeholder for escaped opening braces '{{'
MARK_LB: str = "\u0002"

# Matches a single tag enclosed in single braces: {glyph_name key=value ...}
# Captures the raw tag body inside the "content" named group.
TAG_PATTERN: re.Pattern[str] = re.compile(
    r"\{"
    r"(?P<content>[^\}]+)"
    r"\}",
    re.DOTALL,
)


class IssueLevel(str, Enum):
    """
    Severity levels for tag processing diagnostics.
    """

    WARNING = "warning"
    ERROR = "error"


@dataclass
class TagIssue:
    """
    Represents a warning or error encountered during tag processing.

    Attributes:
        code (str): Machine-readable issue category identifier.
        message (str): Human-readable message explaining failure details.
        level (IssueLevel): Severity level (`IssueLevel.WARNING` or `IssueLevel.ERROR`).
        details (dict[str, Any]): Additional contextual metadata regarding the issue.
    """

    code: str
    message: str
    level: IssueLevel = IssueLevel.ERROR
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the issue instance into a JSON-serializable dictionary.

        Returns:
            dict[str, Any]: Dictionary representation of the tag issue.
        """
        return {
            "code": self.code,
            "message": self.message,
            "level": self.level.value,
            "details": self.details,
        }


class ReplaceFn(Protocol):
    """
    Protocol definition for tag match-replacement closures.

    Implementations are callable objects that accept a regex match object and a mutable
    issue list, returning a replacement string while appending any encountered issues.
    """

    def __call__(self, match: re.Match[str], issues: list[TagIssue]) -> str:
        """
        Process a regex tag match and record any non-fatal processing issues.

        Args:
            match (re.Match[str]): The regex match object representing a tag.
                Use `match.group("content")` to retrieve the raw inner tag string.
            issues (list[TagIssue]): Mutable list to collect encountered issues.

        Returns:
            str: The replacement string to substitute into target text.
        """
        ...


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
            content (str): Raw string inside a tag (e.g., extracted via `match.group("content")`).

        Returns:
            tuple[str, dict[str, str]]: A tuple containing:
                - `glyph_name` (str): Primary identifier token (empty string if missing).
                - `properties` (dict[str, str]): Key-value pairs parsed from `key=value` tokens.
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
        replacer: ReplaceFn,
        unescape: bool = True,
        issues: list[TagIssue] | None = None,
    ) -> str:
        """
        Execute the full transformation pipeline: escape -> substitute -> restore.

        Args:
            text (str): Target text to process.
            replacer (ReplaceFn): Replacement callback implementing `ReplaceFn`.
            unescape (bool): If `True`, converts preserved placeholders to `{`.
                If `False`, preserves them as `{{`. Defaults to `True`.
            issues (list[TagIssue] | None): Optional mutable list to collect issues
                encountered during substitution. If `None`, an internal list is used.

        Returns:
            str: Transformed output text after tag substitution and brace restoration.
        """
        issue_list = issues if issues is not None else []
        escaped = cls.escape_tokens(text)

        def sub_callback(match: re.Match[str]) -> str:
            return replacer(match, issue_list)

        substituted = TAG_PATTERN.sub(sub_callback, escaped)

        if unescape:
            return cls.restore_tokens_unescape(substituted)
        return cls.restore_tokens_preserve_escape(substituted)

