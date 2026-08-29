from mjrengo.engine import GlyphError

def make_replace_fn(glyph_table, set_name):
    def replace_fn(m, errors):
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
        return "{%s b=%s v=%s set=%s}" % (
            glyph,
            entry["b"],
            entry["v"],
            set_name,
        )

    return replace_fn
