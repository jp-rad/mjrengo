Module mjrengo.builder
======================

Functions
---------

`build_engine(glyph_set: str, version: str, set_name: str | None = None, base: str = 'mjrengo.data') ‑> mjrengo.engine.GlyphTagEngine`
:   Build a GlyphTagEngine instance using get_resource() and make_replace_fn().
    
    If set_name is not provided, glyph_set is used as the default.