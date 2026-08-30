# mjrengo/builder.py

from mjrengo.resource import get_resource
from mjrengo.replace import make_replace_fn
from mjrengo.engine import GlyphTagEngine


def build_engine(
    glyph_set: str,
    version: str,
    set_name: str | None = None,
    base: str = "mjrengo.data",
) -> GlyphTagEngine:
    """
    Build a GlyphTagEngine instance using get_resource() and make_replace_fn().

    If set_name is not provided, glyph_set is used as the default.
    """

    # Default set_name = glyph_set
    if set_name is None:
        set_name = glyph_set

    # Load dataset module
    res = get_resource(glyph_set, version, base=base)
    glyph_table = res["GLYPH_TABLE"]

    # Create replace function
    fn = make_replace_fn(glyph_table, set_name)

    # Build engine
    return GlyphTagEngine(fn)
