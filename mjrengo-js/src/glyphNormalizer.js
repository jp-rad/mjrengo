import { GlyphUtils } from "./glyphUtils.js";

export class GlyphNormalizer {
  constructor(glyphTable = {}) {
    this.glyphTable = glyphTable;
  }

  normalize(text, glyphTable = null) {
    const table = glyphTable !== null ? glyphTable : this.glyphTable;
    const errors = [];

    const _normalize_tag = (match, content) => {
      const { glyphName, props: existingProps } = GlyphUtils.parseTagContent(content);

      // エラー1: 未定義
      if (!table[glyphName]) {
        errors.push({
          glyph_name: glyphName,
          reason: "NOT_FOUND",
          message: `Glyph '${glyphName}' is not defined in GLYPH_TABLE.`
        });
        return match;
      }

      const glyphInfo = table[glyphName];

      // エラー2: 非アクティブ
      if (!glyphInfo.active) {
        errors.push({
          glyph_name: glyphName,
          reason: "INACTIVE",
          message: `Glyph '${glyphName}' is marked as inactive.`
        });
        return match;
      }

      // 正常処理: active 除外 & null/undefined 除外
      const props = {};
      for (const [k, v] of Object.entries(glyphInfo)) {
        if (k !== "active" && v !== null && v !== undefined) {
          props[k] = v;
        }
      }
      Object.assign(props, existingProps);

      const propsEntries = Object.entries(props);
      const propsStr = propsEntries.map(([k, v]) => `${k}=${v}`).join(" ");
      return `{${glyphName}${propsStr ? " " + propsStr : ""}}`;
    };

    const normalizedText = GlyphUtils.processPipeline(text, _normalize_tag, false);

    if (errors.length > 0) {
      return { success: false, result: null, errors: errors };
    }

    return { success: true, result: normalizedText, errors: [] };
  }
}
