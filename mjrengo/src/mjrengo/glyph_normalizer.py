"""
Glyph Tag normalization models and processing engine for the tofurengo library.

This module provides data models for tracking normalization results (`NormalizeResult`)
and the `GlyphNormalizer` class, which handles the normalization phase of Glyph Tags
using a delegated callback function (`ReplaceFn`).
"""

from dataclasses import dataclass, field
from typing import Any, Optional

# TODO: mjrengo を tofurengo に統合する際に、以下の import 文を元に戻す
# from tofurengo.tag_parser import ReplaceFn, TagError, TagParser
from mjrengo.tag_parser import ReplaceFn, TagIssue, TagParser


@dataclass
class NormalizeResult:
    """
    Encapsulates the final outcome of a tag normalization pipeline operation.

    Attributes:
        success (bool): Indicates whether the process completed without validation errors.
        text (str): The transformed or normalized output string.
        errors (list[TagError]): List of non-fatal validation errors collected
            during the normalization process.
    """

    success: bool
    text: str
    errors: list[TagIssue] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the result object and its collected errors into a dictionary.

        Returns:
            dict[str, Any]: Serialized dictionary containing status, output text,
                and error dictionaries.
        """
        return {
            "success": self.success,
            "text": self.text,
            "errors": [e.to_dict() for e in self.errors],
        }


class GlyphNormalizer:
    """
    Stateless normalization engine for processing text containing Glyph Tags.

    Delegates tag lookup and attribute reconstruction details to a `ReplaceFn` callback.
    The `replace_fn` can be provided either during initialization or dynamically
    during the `normalize()` method call.
    """

    def __init__(self, replace_fn: Optional[ReplaceFn] = None) -> None:
        """
        Initialize the GlyphNormalizer.

        Args:
            replace_fn (Optional[ReplaceFn]): Default replacement callback function.
        """
        self.replace_fn = replace_fn

    def normalize(
        self,
        text: str,
        replace_fn: Optional[ReplaceFn] = None,
    ) -> NormalizeResult:
        """
        Execute normalization on the input text.

        Replaces Glyph Tags with their canonical attributes while preserving
        the opening escape tokens (`{{`).

        Args:
            text (str): Input text containing Glyph Tags.
            replace_fn (Optional[ReplaceFn]): Replacement callback to use for this call.
                Overrides instance `self.replace_fn` if provided.

        Returns:
            NormalizeResult: Result object containing the normalized text, success status,
                and any accumulated errors.

        Raises:
            ValueError: If no `replace_fn` is provided in either `__init__` or `normalize()`.
        """
        if not text:
            return NormalizeResult(success=True, text="", errors=[])

        fn = replace_fn or self.replace_fn
        if fn is None:
            raise ValueError("replace_fn is required in __init__ or normalize()")

        errors: list[TagIssue] = []

        normalized_text = TagParser.process_pipeline(
            text=text,
            replacer=fn,
            unescape=False,  # Retain '{{' escape sequences during normalization
            errors=errors,
        )

        return NormalizeResult(
            success=len(errors) == 0,
            text=normalized_text,
            errors=errors,
        )

