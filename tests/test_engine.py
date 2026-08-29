import pytest
from mjrengo.engine import GlyphTagEngine, GlyphError, GlyphResult
from mjrengo.replace import make_replace_fn
# from mjrengo.data.mj import glyph_table
from mjrengo.data.mj_plus import glyph_table

set_name = "mj_plus"

# ------------------------------------------------------------
# normalize_tags() のテスト
# ------------------------------------------------------------

def test_normalize_success():
    fn = make_replace_fn(glyph_table, set_name)
    engine = GlyphTagEngine(fn)

    result = engine.normalize_tags("{MJ000001}")
    assert isinstance(result, GlyphResult)
    assert result.success is True
    assert result.errors == []
    assert result.text == "{MJ000001 b=U+3005 v=U+3005 set=mj_plus}"


def test_normalize_not_found():
    fn = make_replace_fn(glyph_table, set_name)
    engine = GlyphTagEngine(fn)
    
    result = engine.normalize_tags("{MJ999999}")

    assert result.success is False
    assert len(result.errors) == 1

    err = result.errors[0]
    assert err.code == "error.glyph.not_found"
    assert "MJ999999" in err.message
    assert err.params["glyph"] == "MJ999999"


def test_normalize_archived():
    fn = make_replace_fn(glyph_table, set_name)
    engine = GlyphTagEngine(fn)

    result = engine.normalize_tags("{MJ000012}")

    assert result.success is False
    assert len(result.errors) == 1

    err = result.errors[0]
    assert err.code == "error.glyph.archived"
    assert err.params["glyph"] == "MJ000012"


# ------------------------------------------------------------
# render_text() のテスト
# ------------------------------------------------------------

def test_render_success():
    fn = make_replace_fn(glyph_table, set_name)
    engine = GlyphTagEngine(fn)
    
    norm = engine.normalize_tags("{MJ000001}")
    assert norm.success is True
    assert norm.errors == []

    result = engine.render_text(norm.text)
    assert result == "々"  # U+3005


# ------------------------------------------------------------
# to_dict() のテスト
# ------------------------------------------------------------

def test_to_dict():
    fn = make_replace_fn(glyph_table, set_name)
    engine = GlyphTagEngine(fn)

    result = engine.normalize_tags("{MJ999999}")
    d = result.to_dict()

    assert d["success"] is False
    assert "text" in d
    assert "errors" in d
    assert isinstance(d["errors"], list)
    assert d["errors"][0]["code"] == "error.glyph.not_found"


def test_complex_text():
    fn = make_replace_fn(glyph_table, set_name)
    engine = GlyphTagEngine(fn)

    text = (
        "東京都{MJ022336}飾区は、{{MJ022336}を使います。<845B,E0103>\n"
        "奈良県{MJ022335}城市は、{{MJ022335}を使います。<845B,E0102>"
    )

    # ------------------------------
    # normalize_tags()
    # ------------------------------
    norm = engine.normalize_tags(text)
    assert norm.success is True
    assert len(norm.errors) == 0

    # 正規化後のテキストにタグ展開が含まれていること
    assert "東京都{MJ022336 b=U+845B v=U+845B U+E0103 set=mj_plus}飾区" in norm.text
    assert "奈良県{MJ022335 b=U+845B v=U+845B U+E0102 set=mj_plus}城市" in norm.text

    # ------------------------------
    # render_text()
    # ------------------------------
    rend = engine.render_text(norm.text)

    # U+845B U+E0103 https://moji.or.jp/mojikibansearch/info?MJ%E6%96%87%E5%AD%97%E5%9B%B3%E5%BD%A2%E5%90%8D=MJ022336
    # U+845B U+E0102 https://moji.or.jp/mojikibansearch/info?MJ%E6%96%87%E5%AD%97%E5%9B%B3%E5%BD%A2%E5%90%8D=MJ022335
    assert "東京都" + chr(0x845B) + chr(0xE0103) + "飾区" in rend
    assert "奈良県" + chr(0x845B) + chr(0xE0102) + "城市" in rend

    # タグ外の MJ 番号はそのまま
    assert "{MJ022336}を使います。<845B,E0103>" in rend
    assert "{MJ022335}を使います。<845B,E0102>" in rend

    # ------------------------------
    # render_text() 代替字形「葛」で判定する
    # ------------------------------
    rend = engine.render_text(norm.text, True)

    # U+845B → 葛
    assert "東京都葛飾区" in rend
    assert "奈良県葛城市" in rend

    # タグ外の MJ 番号はそのまま
    assert "{MJ022336}を使います。<845B,E0103>" in rend
    assert "{MJ022335}を使います。<845B,E0102>" in rend
