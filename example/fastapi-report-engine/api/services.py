from mjrengo.builder import build_engine

# ------------------------------------------------------------
# エンジン（最新版）
# ------------------------------------------------------------
engines = {
    "mj":        build_engine("mj", "6.02.201"),
    "mj-onka":   build_engine("mj", "6.02.201-onka"),
    "mj-plus":   build_engine("mj_plus", "4.10"),
    "mj-plusx":  build_engine("mj_plusx", "1.20"),
}

def get_engine(name: str):
    if name not in engines:
        raise ValueError(f"Unknown engine: {name}")
    return engines[name]


# ------------------------------------------------------------
# normalize
# ------------------------------------------------------------
def normalize_service(engine: str, payload):
    e = get_engine(engine)
    n = e.normalize_tags(payload.text)

    errors = [
        {"stage": "normalize", **err.to_dict()}
        for err in n.errors
    ]

    return {
        "engine": engine,
        "input_text": payload.text,
        "normalized_text": n.text,
        "errors": errors
    }


# ------------------------------------------------------------
# render
# ------------------------------------------------------------
def render_service(engine: str, payload):
    e = get_engine(engine)

    n = e.normalize_tags(payload.text)
    r = e.render_text(n.text, payload.use_base)
    r_fallback = e.render_text(n.text, False)

    errors = [
        {"stage": "normalize", **err.to_dict()}
        for err in n.errors
    ]

    return {
        "engine": engine,
        "input_text": payload.text,
        "normalized_text": n.text,
        "rendered_text": r.text,
        "rendered_text_fallback": r_fallback.text,
        "errors": errors
    }


# ------------------------------------------------------------
# convert (GET)
# ------------------------------------------------------------
def convert_service(engine: str, text: str, use_base: bool):
    e = get_engine(engine)

    n = e.normalize_tags(text)
    r = e.render_text(n.text, use_base)
    r_fallback = e.render_text(n.text, False)

    errors = [
        {"stage": "normalize", **err.to_dict()}
        for err in n.errors
    ]

    return {
        "engine": engine,
        "input_text": text,
        "normalized_text": n.text,
        "rendered_text": r,
        "rendered_text_fallback": r_fallback,
        "errors": errors
    }
