"""
Unit tests for the `tofurengo.tag_parser` module.

Verifies token escaping, `ParsedTag` parsing from content, and pipeline processing.
"""

# from tofurengo.tag_parser import MARK_LB, ParsedTag, TagIssue, TagParser
from mjrengo.tag_parser import MARK_LB, ParsedTag, TagIssue, TagParser


class TestGlyphUtilsTokenEscape:
    """Tests for token escaping and restoration methods in `TagParser`."""

    def test_escape_tokens(self) -> None:
        """Verify that double-brace opening tokens ('{{') are replaced by placeholder markers."""
        input_text = "Text with {{escaped}} and {normal} tags."
        expected = "Text with " + MARK_LB + "escaped}} and {normal} tags."
        assert TagParser.escape_tokens(input_text) == expected

    def test_restore_tokens_keep_escape(self) -> None:
        """Verify that placeholder markers are restored back to double braces ('{{')."""
        input_text = f"Text with {MARK_LB}escaped}} and tags."
        expected = "Text with {{escaped}} and tags."
        assert TagParser.restore_tokens_preserve_escape(input_text) == expected

    def test_restore_tokens_unescape(self) -> None:
        """Verify that placeholder markers are converted to single braces ('{')."""
        input_text = f"Text with {MARK_LB}escaped}} and tags."
        expected = "Text with {escaped}} and tags."
        assert TagParser.restore_tokens_unescape(input_text) == expected


class TestParsedTagFromContent:
    """Tests for `ParsedTag.from_content` parsing functionality."""

    def test_parse_simple_glyph(self) -> None:
        """Verify parsing a tag containing only a glyph name."""
        tag = ParsedTag.from_content("GJ000001")
        assert tag.glyph_name == "GJ000001"
        assert tag.b is None
        assert tag.v is None
        assert tag.set is None
        assert tag.properties == {}

    def test_parse_glyph_with_props(self) -> None:
        """Verify parsing a tag with multiple key-value attributes."""
        tag = ParsedTag.from_content("GJ000001 b=U+30F1 v=U+100000 set=MJ2026")
        assert tag.glyph_name == "GJ000001"
        assert tag.b == "U+30F1"
        assert tag.v == "U+100000"
        assert tag.set == "MJ2026"
        assert tag.properties == {
            "b": "U+30F1",
            "v": "U+100000",
            "set": "MJ2026",
        }

    def test_parse_with_extra_spaces(self) -> None:
        """Verify parsing content containing redundant surrounding or interior whitespace."""
        tag = ParsedTag.from_content("   GJ000001    b=U+30F1   v=U+100000  ")
        assert tag.glyph_name == "GJ000001"
        assert tag.b == "U+30F1"
        assert tag.v == "U+100000"
        assert tag.properties == {"b": "U+30F1", "v": "U+100000"}

    def test_parse_value_containing_equals(self) -> None:
        """Verify that attribute values containing equals signs are parsed correctly."""
        tag = ParsedTag.from_content("GJ000001 expr=a=b")
        assert tag.glyph_name == "GJ000001"
        assert tag.properties == {"expr": "a=b"}

    def test_parse_empty_content(self) -> None:
        """Verify parsing empty or whitespace-only tag content."""
        tag = ParsedTag.from_content("   ")
        assert tag.glyph_name == ""
        assert tag.properties == {}


class TestGlyphUtilsProcessPipeline:
    """Tests for `TagParser.process_pipeline` execution flow."""

    def test_pipeline_normalize_mode_keep_escape(self) -> None:
        """Verify normalization mode (unescape=False): preserves '{{' while replacing '{}' tags."""
        text = "Hello {GJ000001} and {{GJ000002}}!"

        def dummy_replacer(tag: ParsedTag, issues: list[TagIssue]) -> str:
            return f"[{tag.glyph_name}_NORMALIZED]"

        result = TagParser.process_pipeline(text, dummy_replacer, unescape=False)
        assert result == "Hello [GJ000001_NORMALIZED] and {{GJ000002}}!"

    def test_pipeline_render_mode_unescape(self) -> None:
        """Verify rendering mode (unescape=True): unescapes '{{' into '{' during output generation."""
        text = "Hello {GJ000001} and {{GJ000002}}!"

        def dummy_replacer(tag: ParsedTag, issues: list[TagIssue]) -> str:
            return f"[{tag.glyph_name}_RENDERED]"

        result = TagParser.process_pipeline(text, dummy_replacer, unescape=True)
        assert result == "Hello [GJ000001_RENDERED] and {GJ000002}!"

    def test_pipeline_no_tags(self) -> None:
        """Verify processing input text containing no tag markup."""
        text = "Plain text without any tags."

        def dummy_replacer(tag: ParsedTag, issues: list[TagIssue]) -> str:
            return f"{{{tag.raw_content}}}"

        result = TagParser.process_pipeline(text, dummy_replacer, unescape=False)
        assert result == "Plain text without any tags."

    def test_pipeline_empty_string(self) -> None:
        """Verify processing an empty input string."""
        def dummy_replacer(tag: ParsedTag, issues: list[TagIssue]) -> str:
            return f"{{{tag.raw_content}}}"

        result = TagParser.process_pipeline("", dummy_replacer, unescape=False)
        assert result == ""

