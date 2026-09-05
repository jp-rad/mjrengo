"""
Core data models and protocol definitions for tag normalization operations.

This module contains data classes for tracking normalization errors (`NormalizeError`),
encapsulating execution results (`NormalizeResult`), and defining the protocol
interface (`ReplaceFn`) used across tag transformation pipelines in the `tofurengo` library.
"""

from dataclasses import dataclass, field
import re
from typing import Any, Protocol
from mjrengo.tag_parser import TagError


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


