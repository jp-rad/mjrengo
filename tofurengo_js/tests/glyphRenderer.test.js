import { GlyphRenderer } from "../src/glyphRenderer.js";

describe("GlyphRenderer", () => {
  test("正常系: コードポイントから Unicode 文字へ変換されること (v 優先)", () => {
    const input = "{GJ000001 b=U+30F1 v=U+100000}";
    const result = GlyphRenderer.render(input);

    // U+100000 の文字
    expect(result).toBe(String.fromCodePoint(0x100000));
  });

  test("正常系: v が存在しない場合は b のコードポイントを使用すること", () => {
    const input = "{GJ000001 b=U+30F1}";
    const result = GlyphRenderer.render(input);

    // U+30F1 は 'ヱ'
    expect(result).toBe("ヱ");
  });

  test("正常系: エスケープ文字がアンエスケープ（復元）されること", () => {
    const input = "パス: \\\\ タグ記号: \\{GJ000001\\}";
    const result = GlyphRenderer.render(input);

    expect(result).toBe("パス: \\ タグ記号: {GJ000001}");
  });

  test("正常系: エスケープ文字と正規化タグが混在する場合に正しく展開されること", () => {
    const input = "エスケープ: \\{GJ000001\\} / 描画: {GJ000001 b=U+30F1}";
    const result = GlyphRenderer.render(input);

    expect(result).toBe("エスケープ: {GJ000001} / 描画: ヱ");
  });

  test("境界値: CodePoint に変換できない不正な属性値の場合はタグをそのまま返すこと", () => {
    const input = "{GJ000001 v=INVALID}";
    const result = GlyphRenderer.render(input);

    expect(result).toBe("{GJ000001 v=INVALID}");
  });
});
