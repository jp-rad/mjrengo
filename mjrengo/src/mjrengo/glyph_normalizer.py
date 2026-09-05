"""
Glyph Tag normalizer module for the tofurengo library.

This module provides the `GlyphNormalizer` class, which handles the normalization phase
of Glyph Tags using a delegated callback function (`ReplaceFn`).
"""

from typing import List, Optional

from mjrengo.tag_parser import TagParser
from mjrengo.types import TagError, NormalizeResult, ReplaceFn


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
        replace_fn: Optional[ReplaceFn] = None
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
            GlyphResult: Result object containing the normalized text, success status,
                and any accumulated errors.

        Raises:
            ValueError: If no `replace_fn` is provided in either `__init__` or `normalize()`.
        """
        if not text:
            return NormalizeResult(success=True, text="", errors=[])

        fn = replace_fn or self.replace_fn
        if fn is None:
            raise ValueError("replace_fn is required in __init__ or normalize()")

        errors: List[TagError] = []

        normalized_text = TagParser.process_pipeline(
            text=text,
            replacer=lambda match: fn(match, errors),
            unescape=False,  # Retain '{{' escape sequences during normalization
        )

        return NormalizeResult(
            success=len(errors) == 0,
            text=normalized_text,
            errors=errors,
        )

