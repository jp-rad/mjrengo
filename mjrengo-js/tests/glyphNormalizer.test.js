import { GlyphNormalizer } from "../src/glyphNormalizer.js";

describe("GlyphNormalizer", () => {
  const mockTable = {
    GJ000001: { b: "U+30F1", v: "U+100000", active: true },
    GJ000002: { b: null, v: "U+100001", active: true },
    GJ000003: { b: "U+5B89", v: "U+1B002", active: false } // 非アクティブ
  };

  let normalizer;

  beforeEach(() => {
    normalizer = new GlyphNormalizer(mockTable);
  });

  test("正常系: 属性が正しく補完されること（b=null は除外）", () => {
    const input = "テスト {GJ000001} と {GJ000002}";
    const response = normalizer.normalize(input);

    expect(response.success).toBe(true);
    expect(response.result).toBe(
      "テスト {GJ000001 b=U+30F1 v=U+100000} と {GJ000002 v=U+100001}"
    );
    expect(response.errors).toHaveLength(0);
  });

  test("正常系: エスケープ文字が置換されず保持されること", () => {
    const input = "エスケープ: \\{GJ000001\\} タグ: {GJ000001}";
    const response = normalizer.normalize(input);

    expect(response.success).toBe(true);
    expect(response.result).toBe(
      "エスケープ: \\{GJ000001\\} タグ: {GJ000001 b=U+30F1 v=U+100000}"
    );
  });

  test("正常系: 既存の属性指定がある場合は上書き・追加されること", () => {
    const input = "{GJ000001 custom=123}";
    const response = normalizer.normalize(input);

    expect(response.success).toBe(true);
    expect(response.result).toBe(
      "{GJ000001 b=U+30F1 v=U+100000 custom=123}"
    );
  });

  test("異常系: 未定義タグおよび非アクティブタグのエラーが全件収集されること", () => {
    const input = "非アクティブ {GJ000003} と 未定義 {GJ999999}";
    const response = normalizer.normalize(input);

    expect(response.success).toBe(false);
    expect(response.result).toBeNull();
    expect(response.errors).toEqual([
      {
        glyph_name: "GJ000003",
        reason: "INACTIVE",
        message: "Glyph 'GJ000003' is marked as inactive."
      },
      {
        glyph_name: "GJ999999",
        reason: "NOT_FOUND",
        message: "Glyph 'GJ999999' is not defined in GLYPH_TABLE."
      }
    ]);
  });
});
