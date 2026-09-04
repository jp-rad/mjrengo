from mjrengo.resource import get_resource
from mjrengo.factories import make_replace_fn
from mjrengo.glyph_normalizer import GlyphNormalizer
from mjrengo.glyph_renderer import GlyphRenderer

def build_normalizer(
    glyph_set: str,
    version: str,
    set_name: str | None = None,
    base: str = "mjrengo.data",
) -> GlyphNormalizer:
    """
    Build a GlyphNormalizer instance using get_resource() and make_replace_fn().

    If set_name is not provided, glyph_set is used as the default.
    """
    if set_name is None:
        set_name = glyph_set

    res = get_resource(glyph_set, version, base=base)
    glyph_table = res["GLYPH_TABLE"]

    fn = make_replace_fn(glyph_table, set_name)
    return GlyphNormalizer(replace_fn=fn)


def build_renderer(
    use_base: bool = False,
    tofu: str = "U+25A1",
) -> GlyphRenderer:
    """
    Build a GlyphRenderer instance with specified rendering options.

    Note: GlyphRenderer operates statelessly on normalized tags and
    does not require a dataset resource or glyph_table.
    """
    return GlyphRenderer(use_base=use_base, tofu=tofu)
