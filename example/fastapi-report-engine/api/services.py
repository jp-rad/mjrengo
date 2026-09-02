from mjrengo.builder import build_engine

# ------------------------------------------------------------
# エンジン情報（set と version）
# ------------------------------------------------------------
engine_info = {
    "mj":      {"set": "mj",       "version": "6.02.201"},
    "mj-onka": {"set": "mj",       "version": "6.02.201-onka"},
    "mj-plus": {"set": "mj_plus",  "version": "4.10"},
    "mj-plusx":{"set": "mj_plusx", "version": "1.20"},
}

# ------------------------------------------------------------
# エンジン（engine_info から自動生成）
# ------------------------------------------------------------
engines = {
    name: build_engine(info["set"], info["version"])
    for name, info in engine_info.items()
}

# ------------------------------------------------------------
# engine_info と engine を同時に返す
# ------------------------------------------------------------
def get_engine(name: str):
    if name not in engine_info:
        raise ValueError(f"Unknown engine: {name}")

    return {
        "info": engine_info[name],   # set / version
        "engine": engines[name],     # build_engine の実体
    }


# ------------------------------------------------------------
# normalize_service
# ------------------------------------------------------------
def normalize_service(engine: str, text: str):
    e = get_engine(engine)
    eng = e["engine"]
    info = e["info"]

    n = eng.normalize_tags(text)

    errors = [
        {**err.to_dict()}
        for err in n.errors
    ]

    return {
        "service": "normalize",
        "meta": {
            "engine": engine,
            "glyph": info,   # set / version をそのまま返す
        },
        "text": {
            "input": text,
            "normalized": n.text,
        },
        "errors": errors
    }


# ------------------------------------------------------------
# render_service（normalize_tags を呼ばない）
# ------------------------------------------------------------
def render_service(engine: str, normalized_text: str):
    e = get_engine(engine)
    eng = e["engine"]
    info = e["info"]

    rendered_variant = eng.render_text(normalized_text, use_base=False)
    rendered_base = eng.render_text(normalized_text, use_base=True)

    return {
        "service": "render",
        "meta": {
            "engine": engine,
            "glyph": info,
        },
        "text": {
            "rendered": {
                "variant": rendered_variant,
                "base": rendered_base,
            }
        },
        "errors": []  # render は normalize のエラーを扱わない
    }


# ------------------------------------------------------------
# convert_service（normalize → render をまとめて行う）
# ------------------------------------------------------------
def convert_service(engine: str, text: str):
    e = get_engine(engine)
    eng = e["engine"]
    info = e["info"]

    # normalize
    n = eng.normalize_tags(text)
    errors = [
        {**err.to_dict()}
        for err in n.errors
    ]

    # render
    rendered_variant = eng.render_text(n.text, use_base=False)
    rendered_base = eng.render_text(n.text, use_base=True)

    return {
        "service": "convert",
        "meta": {
            "engine": engine,
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
