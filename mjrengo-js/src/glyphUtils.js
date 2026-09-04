const MARK_BS = "\u0001";
const MARK_LB = "\u0002";
const MARK_RB = "\u0003";
const TAG_PATTERN = /\{([^}]+)\}/g;

export class GlyphUtils {
  static escapeTokens(text) {
    return text.replace(/\\\\/g, MARK_BS).replace(/\\\{/g, MARK_LB).replace(/\\\}/g, MARK_RB);
  }

  static restoreTokens(text) {
    return text.replace(new RegExp(MARK_BS, "g"), "\\")
               .replace(new RegExp(MARK_LB, "g"), "{")
               .replace(new RegExp(MARK_RB, "g"), "}");
  }

  static parseTagContent(content) {
    const tokens = content.trim().split(/\s+/);
    if (!tokens.length || !tokens[0]) return { glyphName: "", props: {} };
    
    const glyphName = tokens[0];
    const props = {};
    for (let i = 1; i < tokens.length; i++) {
      const [k, v] = tokens[i].split("=");
      if (k && v !== undefined) props[k] = v;
    }
    return { glyphName, props };
  }

  static processPipeline(text, replacer, unescape = true) {
    let s = this.escapeTokens(text);
    s = s.replace(TAG_PATTERN, replacer);
    if (unescape) {
      s = this.restoreTokens(s);
    }
    return s;
  }
}
