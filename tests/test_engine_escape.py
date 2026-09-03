import pytest
from mjrengo.engine import GlyphTagEngine, make_replace_fn

# テスト用の簡易 glyph_table
glyph_table = {
    "MJ006295": {"v": "U+4E01", "b": "U+4E01"}, # 丁
}

engine = GlyphTagEngine(make_replace_fn(glyph_table, "test"))


# ============================================================
# normalize_tags() のテスト
# ============================================================

def test_normalize_keeps_escape_backslash_brace():
    text = "\{MJ006295}"
    result = engine.normalize_tags(text)
    assert result.text == "\{MJ006295}"


def test_normalize_keeps_double_backslash():
    text = r"\\"
    result = engine.normalize_tags(text)
    assert result.text == r"\\"


def test_normalize_keeps_double_left_brace():
    text = "{{MJ006295}"
    result = engine.normalize_tags(text)
    assert result.text == "{{MJ006295}"


def test_normalize_tag_is_normalized():
    text = "{MJ006295}"
    result = engine.normalize_tags(text)
    assert result.text == "{MJ006295 b=U+4E01 v=U+4E01 set=test}"


def test_normalize_mixed_text():
    text = "a\{MJ006295} b{MJ006295} c{{MJ006295}"
    result = engine.normalize_tags(text)
    assert result.text == "a\{MJ006295} b{MJ006295 b=U+4E01 v=U+4E01 set=test} c{{MJ006295}"


# ============================================================
# render_text() のテスト
# ============================================================

def test_render_unescape_backslash_brace():
    text = "\{MJ006295}"
    rendered = engine.render_text(text)
    # \{ → { → タグとして描画される
    assert rendered == "{MJ006295}"


def test_render_unescape_double_backslash():
    text = "\\"
    rendered = engine.render_text(text)
    assert rendered == "\\"


def test_render_keeps_double_left_brace():
    text = "{{MJ006295}"
    rendered = engine.render_text(text)
    # {{ は変換しない → タグとして扱われない
    assert rendered == "{{MJ006295}"


def test_render_tag_is_rendered():
    text = "{MJ006295}"
    norm = engine.normalize_tags(text)
    rendered = engine.render_text(norm.text)
    assert rendered == "丁"


def test_render_mixed_text():
    text = "a\{MJ006295} b{MJ006295} c{{MJ006295}"
    norm = engine.normalize_tags(text)
    rendered = engine.render_text(norm.text)
    assert rendered == "a{MJ006295} b丁 c{{MJ006295}"
