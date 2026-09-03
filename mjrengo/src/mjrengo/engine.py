from dataclasses import dataclass, field
from typing import Protocol, List, Dict, Any, Match

from mjrengo.ucs import decode_ucs
from mjrengo.regex_defs import (
    TAG_PATTERN,
    RE_ESC_BACKSLASH,
    RE_ESC_LBRACE,
)


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
    Normalization Rules:

    - glyph-name を glyph_table で解決
    - b/v を UCSSeq に置き換える
    - set は環境の set_name に強制置換
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

        # Normalization
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

    Syntax:

        {<glyph-name> [b=<UCSSeq>] [v=<UCSSeq>] [set=<Identifier>]}
    """

    def __init__(self, replace_fn: ReplaceFn):
        self.replace_fn = replace_fn

    # --------------------------------------------------------
    # Private: render escape
    # --------------------------------------------------------
    def _apply_render_escape(self, text: str) -> str:
        """
        Rendering phase:
        - \\  → \
        - \{ → {
        - {{ は変換しない（仕様）
        """
        if not text:
            return ""

        # Important: process \\ first
        text = RE_ESC_BACKSLASH.sub(r'\\', text)

        # Then \{
        text = RE_ESC_LBRACE.sub(r'{', text)

        return text

    # --------------------------------------------------------
    # normalize_tags()
    # --------------------------------------------------------
    def normalize_tags(self, text: str) -> GlyphResult:
        """
        Normalization:

        - エスケープ文字は維持する
        - TAG_PATTERN により b/v/set を正規化
        - {{ は変換しない
        """
        if self.replace_fn is None:
            raise ValueError("replace_fn is required")

        errors: List[GlyphError] = []

        result_text = TAG_PATTERN.sub(
            lambda m: self.replace_fn(m, errors),
            text,
        )

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
        Rendering Rules:

        mode="v"       → v → b → tofu
        mode="b"       → b → tofu

        - use_base=True  → mode="b"
        - use_base=False → mode="v"
        """

        def _replace(m: Match[str]) -> str:
            b = m.group("b")
            v = m.group("v")

            if use_base:
                seq = b or tofu
            else:
                seq = v or b or tofu

            return decode_ucs(seq)

        rendered = TAG_PATTERN.sub(_replace, text)
        rendered = self._apply_render_escape(rendered)

        return rendered
