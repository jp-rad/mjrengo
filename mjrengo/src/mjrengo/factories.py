from typing import Dict, Any, List, Match
from mjrengo.types import GlyphError, ReplaceFn


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

        # Archived / Inactive
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
