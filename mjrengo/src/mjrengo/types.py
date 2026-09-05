"""
Core data models and protocol definitions for tag normalization operations.

This module contains data classes for tracking normalization errors (`NormalizeError`),
encapsulating execution results (`NormalizeResult`), and defining the protocol
interface (`ReplaceFn`) used across tag transformation pipelines in the `tofurengo` library.
"""

from dataclasses import dataclass, field
import re
from typing import Any, Protocol


@dataclass
class TagError:
    """
    Represents an error encountered during tag lookup, validation, or normalization.

    Attributes:
        code (str): A machine-readable error category identifier
            (e.g., 'error.glyph.not_found', 'error.glyph.archived').
        message (str): Human-readable error message explaining the failure details.
        details (dict[str, Any]): Additional contextual metadata regarding the error.
    """

    code: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the error instance into a JSON-serializable dictionary.

        Returns:
            dict[str, Any]: Dictionary representation of the normalization error.

        Examples:
            >>> err = NormalizeError("error.glyph.not_found", "Glyph 'X' missing")
            >>> err.to_dict()
            {'code': 'error.glyph.not_found', 'message': "Glyph 'X' missing", 'details': {}}
        """
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


@dataclass
class NormalizeResult:
    """
    Encapsulates the final outcome of a tag normalization pipeline operation.

    Attributes:
        success (bool): Indicates whether the process completed without validation errors.
        text (str): The transformed or normalized output string.
        errors (list[NormalizeError]): List of non-fatal validation errors collected
            during the normalization process.
    """

    success: bool
    text: str
    errors: list[TagError] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the result object and its collected errors into a dictionary.

        Returns:
            dict[str, Any]: Serialized dictionary containing status, output text,
                and error dictionaries.

        Examples:
            >>> res = NormalizeResult(success=True, text="{MJ000001 b=U+4E00 v=v1 set=mj}")
            >>> res.to_dict()["success"]
            True
        """
        return {
            "success": self.success,
            "text": self.text,
            "errors": [e.to_dict() for e in self.errors],
        }


class ReplaceFn(Protocol):
    """
    Protocol definition for normalization match-replacement closures.

    Implementations are callable objects that accept a regex match object and a mutable
    error list, returning a normalized replacement string while appending encountered errors.
    """

    def __call__(self, match: re.Match[str], errors: list[TagError]) -> str:
        """
        Process a regex tag match and record any non-fatal validation errors.

        Args:
            match (re.Match[str]): The regex match object representing a tag.
            errors (list[NormalizeError]): Mutable list to collect encountered errors.

        Returns:
            str: The normalized tag replacement string to substitute into the target text.
        """
        ...

