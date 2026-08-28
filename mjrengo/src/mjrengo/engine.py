import re
from dataclasses import dataclass, field
from typing import Protocol, List, Dict, Any, Match

from mjrengo.glyph_utils import (
    escape_left_brace,
    unescape_left_brace,
    render_escape_left_brace,
    render_unescape_left_brace,
)
from mjrengo.ucs import decode_ucs


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
# Normalization callback factory
# ============================================================

def make_replace_fn(glyph_table: Dict[str, Dict[str, Any]], set_name: str) -> ReplaceFn:
    """
    v0.5.8 Normalization Rules:

    - glyph-name を環境の glyph_table で解決
    - b/v を環境固有の UCSSeq に置き換える
    - set は必ず環境の set_name に強制置換する
    - active=false の場合は正規化しない
    """

    def replace_fn(m: Match[str], errors: List[GlyphError]) -> str:
        glyph = m.group("glyph")

        # Not found
        if glyph not in glyph_table:
            code = "error.glyph.not_found"
            msg = f"Glyph '{glyph}' does not exist."
            errors.append(GlyphError(code, f"{code}: {msg}", {"glyph": glyph}))
            return m.group(0)

        entry = glyph_table[glyph]

        # Archived
        if not entry.get("active", True):
            code = "error.glyph.archived"
            msg = f"Glyph '{glyph}' is archived."
            errors.append(GlyphError(code, f"{code}: {msg}", {"glyph": glyph}))
            return m.group(0)

        # Normalization (v0.5.8)
        b = entry.get("b")
        v = entry.get("v")

        return "{%s b=%s v=%s set=%s}" % (
            glyph,
            b,
            v,
            set_name,
        )

    return replace_fn


# ============================================================
# GlyphTagEngine (Stateless, Fully Extensible)
# ============================================================

class GlyphTagEngine:
    """
    Stateless glyph tag processor.
    Tag semantics are fully delegated to replace_fn.

    Syntax (v0.5.8):

        {<glyph-name> [b=<UCSSeq>] [v=<UCSSeq>] [set=<Identifier>]}
    """

    TAG_PATTERN = re.compile(
        r'\{(?P<glyph>[A-Za-z0-9]+)'
        r'(?:\s+b=(?P<b>(?:U\+[0-9A-Fa-f]{4,6}(?:\s+U\+[0-9A-Fa-f]{4,6})*)))?'
        r'(?:\s+v=(?P<v>(?:U\+[0-9A-Fa-f]{4,6}(?:\s+U\+[0-9A-Fa-f]{4,6})*)))?'
        r'(?:\s+set=(?P<set>[A-Za-z0-9_+\-]+))?'
        r'\}'
    )

    def __init__(self, replace_fn: ReplaceFn):
        self.replace_fn = replace_fn

    # --------------------------------------------------------
    # normalize_tags()
    # --------------------------------------------------------
    def normalize_tags(self, text: str) -> GlyphResult:
        """
        Normalization (v0.5.8):

        - "{{" → {_ESC_LB_}
        - TAG_PATTERN により b/v/set を正規化
        - {_ESC_LB_} → "{{"}
        - {_LB_} はそのまま残す
        """
        if self.replace_fn is None:
            raise ValueError("replace_fn is required")

        text = escape_left_brace(text)
        errors: List[GlyphError] = []

        result_text = self.TAG_PATTERN.sub(
            lambda m: self.replace_fn(m, errors),
            text,
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
    def render_text(self, text: str, use_base: bool = False, tofu: str = "U+25A1") -> str:
        """
        Rendering Rules (v0.5.9):

        mode="v"       → v → b → tofu
        mode="b"       → b → tofu

        - use_base=True  → mode="b"
        - use_base=False → mode="v"
        """

        expanded = render_escape_left_brace(text)

        def _replace(m: Match[str]) -> str:
            b = m.group("b")
            v = m.group("v")

            if use_base:
                # mode="b"
                seq = b or tofu
            else:
                # mode="v"
                seq = v or b or tofu

            return decode_ucs(seq)

        rendered = self.TAG_PATTERN.sub(_replace, expanded)

        return render_unescape_left_brace(rendered)
