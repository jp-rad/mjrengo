from mjrengo.engine import GlyphError

def make_replace_fn(table):
    def replace_fn(m, errors):
        glyph = m.group("glyph")

        # Not found
        if glyph not in table:
            code = "error.glyph.not_found"
            msg = f"Glyph '{glyph}' does not exist."
            errors.append(GlyphError(code, f"{code}: {msg}", {"glyph": glyph}))
            return m.group(0)

        entry = table[glyph]

        # Archived
        if not entry.get("active", True):
            code = "error.glyph.archived"
            msg = f"Glyph '{glyph}' is archived."
            errors.append(GlyphError(code, f"{code}: {msg}", {"glyph": glyph}))
            return m.group(0)

        # Normalization
        return "{%s ucs=%s rep=%s set=%s}" % (
            glyph,
            entry["ucs"],
            entry["rep"],
            entry.get("set", "")
        )

    return replace_fn
