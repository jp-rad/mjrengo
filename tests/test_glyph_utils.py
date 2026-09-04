import re
import pytest

from mjrengo.glyph_utils import (
    GlyphUtils,
    MARK_LB,
    # MARK_RB,
)


class TestGlyphUtilsTokenEscape:
    """エスケープ・復元メソッドのテスト"""

    def test_escape_tokens(self):
        input_text = "Text with {{escaped}} and {normal} tags."
        expected = f"Text with {MARK_LB}escaped}} and {normal} tags."
        assert GlyphUtils.escape_tokens(input_text) == expected

    def test_restore_tokens_keep_escape(self):
        input_text = f"Text with {MARK_LB}escaped}} and tags."
        expected = "Text with {{escaped}} and tags."
        assert GlyphUtils.restore_tokens_keep_escape(input_text) == expected

    def test_restore_tokens_unescape(self):
        input_text = f"Text with {MARK_LB}escaped}} and tags."
        expected = "Text with {escaped}} and tags."
        assert GlyphUtils.restore_tokens_unescape(input_text) == expected


class TestGlyphUtilsParseTagContent:
    """parse_tag_content のテスト"""

    def test_parse_simple_glyph(self):
        name, props = GlyphUtils.parse_tag_content("GJ000001")
        assert name == "GJ000001"
        assert props == {}

    def test_parse_glyph_with_props(self):
        name, props = GlyphUtils.parse_tag_content("GJ000001 b=U+30F1 v=U+100000 set=MJ2026")
        assert name == "GJ000001"
        assert props == {"b": "U+30F1", "v": "U+100000", "set": "MJ2026"}

    def test_parse_with_extra_spaces(self):
        name, props = GlyphUtils.parse_tag_content("  GJ000001   b=U+30F1   v=U+100000  ")
        assert name == "GJ000001"
        assert props == {"b": "U+30F1", "v": "U+100000"}

    def test_parse_value_containing_equals(self):
        """値に = が含まれている場合の挙動 (split('=', 1))"""
        name, props = GlyphUtils.parse_tag_content("GJ000001 expr=a=b")
        assert name == "GJ000001"
        assert props == {"expr": "a=b"}

    def test_parse_empty_content(self):
        name, props = GlyphUtils.parse_tag_content("   ")
        assert name == ""
        assert props == {}


class TestGlyphUtilsProcessPipeline:
    """process_pipeline のテスト"""

    def test_pipeline_normalize_mode_keep_escape(self):
        """normalize モード (unescape=False): {{ }} が維持され、{ } のみが置換される"""
        text = "Hello {GJ000001} and {{GJ000002}}!"

        def dummy_replacer(m: re.Match) -> str:
            content = m.group(1)
            glyph, _ = GlyphUtils.parse_tag_content(content)
            return f"[{glyph}_NORMALIZED]"

        result = GlyphUtils.process_pipeline(text, dummy_replacer, unescape=False)
        assert result == "Hello [GJ000001_NORMALIZED] and {{GJ000002}}!"

    def test_pipeline_render_mode_unescape(self):
        """render モード (unescape=True): {{ }} が { } にアンエスケープされる"""
        text = "Hello {GJ000001} and {{GJ000002}}!"

        def dummy_replacer(m: re.Match) -> str:
            content = m.group(1)
            glyph, _ = GlyphUtils.parse_tag_content(content)
            return f"[{glyph}_RENDERED]"

        result = GlyphUtils.process_pipeline(text, dummy_replacer, unescape=True)
        assert result == "Hello [GJ000001_RENDERED] and {GJ000002}!"

    def test_pipeline_no_tags(self):
        text = "Plain text without any tags."
        result = GlyphUtils.process_pipeline(text, lambda m: m.group(0), unescape=False)
        assert result == "Plain text without any tags."

    def test_pipeline_empty_string(self):
        result = GlyphUtils.process_pipeline("", lambda m: m.group(0), unescape=False)
        assert result == ""
