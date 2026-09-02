from mjrengo.builder import build_engine

# Engine definitions (set and version)
engine_info = {
    "mj":      {"set": "mj",       "version": "6.02.201"},
    "mj-onka": {"set": "mj",       "version": "6.02.201-onka"},
    "mj-plus": {"set": "mj_plus",  "version": "4.10"},
    "mj-plusx":{"set": "mj_plusx", "version": "1.20"},
}

# Build engines from engine_info
engines = {
    name: build_engine(info["set"], info["version"])
    for name, info in engine_info.items()
}

# Return both engine_info and engine instance
def get_engine(glyph_set: str):
    if glyph_set not in engine_info:
        raise ValueError(f"Unknown engine: {glyph_set}")

    return {
        "info": engine_info[glyph_set],
        "engine": engines[glyph_set],
    }

# normalize_service
def normalize_service(glyph_set: str, text: str):
    e = get_engine(glyph_set)
    eng = e["engine"]
    info = e["info"]

    n = eng.normalize_tags(text)
    errors = [err.to_dict() for err in n.errors]

    return {
        "service": "normalize",
        "meta": {
            "engine": glyph_set,
            "glyph": info,
        },
        "text": {
            "input": text,
            "normalized": n.text,
        },
        "errors": errors
    }

# render_service (does not call normalize_tags)
def render_service(glyph_set: str, normalized_text: str):
    e = get_engine(glyph_set)
    eng = e["engine"]
    info = e["info"]

    rendered_variant = eng.render_text(normalized_text, use_base=False)
    rendered_base = eng.render_text(normalized_text, use_base=True)

    return {
        "service": "render",
        "meta": {
            "engine": glyph_set,
            "glyph": info,
        },
        "text": {
            "rendered": {
                "variant": rendered_variant,
                "base": rendered_base,
            }
        },
        "errors": []
    }

# convert_service (normalize + render)
def convert_service(glyph_set: str, text: str):
    e = get_engine(glyph_set)
    eng = e["engine"]
    info = e["info"]

    n = eng.normalize_tags(text)
    errors = [err.to_dict() for err in n.errors]

    rendered_variant = eng.render_text(n.text, use_base=False)
    rendered_base = eng.render_text(n.text, use_base=True)

    return {
        "service": "convert",
        "meta": {
            "engine": glyph_set,
            "glyph": info,
        },
        "text": {
            "input": text,
            "normalized": n.text,
            "rendered": {
                "variant": rendered_variant,
                "base": rendered_base,
            }
        },
        "errors": errors
    }
