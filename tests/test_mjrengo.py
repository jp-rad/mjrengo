import pytest
from mjrengo.glyph_utils import GlyphUtils
from mjrengo.glyph_normalizer import GlyphNormalizer
from mjrengo.glyph_renderer import GlyphRenderer
from mjrengo.factories import make_replace_fn


# --- テスト用フィクスチャ（共通データ） ---
@pytest.fixture
def mock_glyph_table():
    return {
        "GJ000001": {
            "b": "U+30F1",
            "v": "U+100000",
            "active": True,
        },
        "GJ000002": {
            "b": None,
            "v": "U+100001",
            "active": True,
        },
        "GJ000003": {
            "b": "U+5B89",
            "v": "U+1B002",
            "active": False,  # 非アクティブ
        },
    }


@pytest.fixture
def mock_replace_fn(mock_glyph_table):
    """set_name を指定して ReplaceFn を生成するフィクスチャ"""
    return make_replace_fn(mock_glyph_table, set_name="MJ2026")


# ==============================================================================
# GlyphUtils の単体テスト ({{ }} エスケープ仕様)
# ==============================================================================
class TestGlyphUtils:
    def test_escape_and_restore_tokens(self):
        original = "文字: {{GJ000001}} タグ記号: {{ test }}"
        escaped = GlyphUtils.escape_tokens(original)

        # {{ と }} が制御文字に退避されていることを確認
        assert "{{" not in escaped
        # assert "}}" not in escaped

        # 復元後に { と } に変換されることを確認
        restored = GlyphUtils.restore_tokens_unescape(escaped)
        assert restored == "文字: {GJ000001}} タグ記号: { test }}"

    def test_parse_tag_content(self):
        content = "GJ000001 b=U+30F1 v=U+100000 custom=test"
        glyph_name, props = GlyphUtils.parse_tag_content(content)

        assert glyph_name == "GJ000001"
        assert props == {"b": "U+30F1", "v": "U+100000", "custom": "test"}


# ==============================================================================
# GlyphNormalizer の単体テスト
# ==============================================================================
class TestGlyphNormalizer:
    def test_normalize_success_basic(self, mock_replace_fn):
        normalizer = GlyphNormalizer(replace_fn=mock_replace_fn)
        input_text = "テスト {GJ000001} と {GJ000002}"

        res = normalizer.normalize(input_text)

        assert res.success is True
        assert res.text == "テスト {GJ000001 b=U+30F1 v=U+100000 set=MJ2026} と {GJ000002 b=None v=U+100001 set=MJ2026}"
        assert res.errors == []

    def test_normalize_preserves_escapes(self, mock_replace_fn):
        normalizer = GlyphNormalizer(replace_fn=mock_replace_fn)
        # 二重波括弧 {{ }} を使用したエスケープ入力
        input_text = "エスケープ: {{GJ000001}} タグ: {GJ000001}"

        res = normalizer.normalize(input_text)

        assert res.success is True
        # 正規化時には {{ }} のエスケープ表記が保持されることを確認
        assert res.text == "エスケープ: {{GJ000001}} タグ: {GJ000001 b=U+30F1 v=U+100000 set=MJ2026}"

    def test_normalize_collects_all_errors(self, mock_replace_fn):
        normalizer = GlyphNormalizer(replace_fn=mock_replace_fn)
        input_text = "非アクティブ {GJ000003 v=U+1234} と 未定義 {GJ999999 b=U+5678}"

        res = normalizer.normalize(input_text)

        assert res.success is False
        assert res.text == "非アクティブ {GJ000003 v=U+1234} と 未定義 {GJ999999 b=U+5678}"
        assert len(res.errors) == 2
        assert res.errors[0].code == "error.glyph.archived"
        assert res.errors[1].code == "error.glyph.not_found"


# ==============================================================================
# GlyphRenderer の単体テスト
# ==============================================================================
class TestGlyphRenderer:
    def test_render_unicode_conversion(self):
        renderer = GlyphRenderer()
        input_text = "{GJ000001 b=U+30F1 v=U+100000 set=MJ2026}"
        rendered = renderer.render(input_text)

        assert rendered == chr(0x100000)

    def test_render_unescapes_double_brackets(self):
        renderer = GlyphRenderer()
        # 描画時に {{ が単一の { にアンエスケープ（復元）されることを確認
        input_text = "パス: {{ path } タグ記号: {{GJ000001}}"
        rendered = renderer.render(input_text)

        assert rendered == "パス: { path } タグ記号: {GJ000001}}"

    def test_render_pipeline_mixed(self):
        renderer = GlyphRenderer()
        # エスケープ復元とタグ描画が同時に正しく処理されること
        input_text = "エスケープ: {{GJ000001} / 描画: {GJ000001 b=U+30F1 set=MJ2026}"
        rendered = renderer.render(input_text)

        assert rendered == "エスケープ: {GJ000001} / 描画: ヱ"

    def test_render_override_options(self):
        """コンストラクタと render() でのパラメータ（use_base, tofu）指定の動作検証"""
        renderer = GlyphRenderer(use_base=True)
        input_text = "{GJ000001 b=U+30F1 v=U+100000 set=MJ2026}"

        # 引数なし（インスタンス設定: use_base=True 優先 -> ヱ）
        assert renderer.render(input_text) == "ヱ"

        # render() で上書き（use_base=False 優先 -> U+100000）
        assert renderer.render(input_text, use_base=False) == chr(0x100000)