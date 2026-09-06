import { GlyphUtils } from "./glyphUtils.js";

export class GlyphRenderer {
  /**
   * 正規化済みテキストを描画（Unicode変換 & アンエスケープ）
   */
  static render(text) {
    const _render_tag = (match, content) => {
      const { props } = GlyphUtils.parseTagContent(content);
      const targetCode = props.v || props.b;

      if (targetCode) {
        try {
          const codePoint = parseInt(targetCode.replace("U+", ""), 16);
          return String.fromCodePoint(codePoint);
        } catch {}
      }
      return match;
    };

    return GlyphUtils.processPipeline(text, _render_tag, true);
  }
}
