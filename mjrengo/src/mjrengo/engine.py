import re
from dataclasses import dataclass, field
from typing import Protocol, List, Dict, Any, Match
from .glyph_utils import (
    escape_left_brace,
    unescape_left_brace,
    protect_left_brace,
    restore_left_brace,
)
from .ucs import decode_ucs


# ============================================================
# Dataclasses (Structured JSON)
# ============================================================

@dataclass
class GlyphError:
    code: str
    message: str
    params: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "params": self.params,
        }


@dataclass
class GlyphResult:
    success: bool
    text: str
    errors: List[GlyphError] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "text": self.text,
            "errors": [e.to_dict() for e in self.errors],
        }


# ============================================================
# Callback Protocol (Type-safe replace_fn)
# ============================================================

class ReplaceFn(Protocol):
    def __call__(self, m: Match[str], errors: List[GlyphError]) -> str:
        ...

# ============================================================
# GlyphTagEngine (Stateless, Fully Extensible)
# ============================================================

class GlyphTagEngine:
    """
    Stateless glyph tag processor.
    Tag semantics are fully delegated to replace_fn.
    """

    TAG_PATTERN = re.compile(
        r'\{(?P<glyph>[A-Za-z0-9]+)'
        r'(?:\s+ucs=(?P<ucs>(?:U\+[0-9A-Fa-f]{4,6}(?:\s+U\+[0-9A-Fa-f]{4,6})*)))?'
        r'(?:\s+rep=(?P<rep>(?:U\+[0-9A-Fa-f]{4,6}(?:\s+U\+[0-9A-Fa-f]{4,6})*)))?'
        r'(?:\s+set=(?P<set>[A-Za-z0-9_+\-]+))?'
        r'\}'
    )

    def __init__(self, replace_fn: ReplaceFn):
        self.replace_fn = replace_fn
    
    # --------------------------------------------------------
    # normalize_tags()
    # --------------------------------------------------------
    def normalize_tags(self, text: str) -> GlyphResult:
        if self.replace_fn is None:
            raise ValueError("replace_fn is required")
        
        text = escape_left_brace(text)
        errors: List[GlyphError] = []

        result_text = self.TAG_PATTERN.sub(
            lambda m: self.replace_fn(m, errors),
            text
        )

        result_text = unescape_left_brace(result_text)

        return GlyphResult(
            success=len(errors) == 0,
            text=result_text,
            errors=errors,
        )

    # --------------------------------------------------------
    # render_text()
    # --------------------------------------------------------
    def render_text(self, text: str, use_rep=False, tofu="U+25A1") -> str:

        expanded = protect_left_brace(text)

        def _replace(m):
            ucs = m.group("ucs")
            rep = m.group("rep")
            seq = rep if use_rep else ucs
            return decode_ucs(seq or tofu)
        
        rendered = self.TAG_PATTERN.sub(_replace, expanded)

        return restore_left_brace(rendered)
