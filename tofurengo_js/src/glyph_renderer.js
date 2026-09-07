/**
 * Glyph tag rendering pipeline for browser client-side display.
 *
 * Parses normalized or raw glyph tags and replaces them with HTML elements
 * (e.g. <ruby> tags for IVS variations, tooltips, or fallback glyph text).
 */

// Module imports (for CommonJS / Node.js test environments)
let TagParser, ParsedTag;
if (typeof require !== "undefined") {
    const tagParserModule = require("./tag_parser.js");
    TagParser = tagParserModule.TagParser;
    ParsedTag = tagParserModule.ParsedTag;
} else if (typeof window !== "undefined") {
    // Browser global fallback
    TagParser = window.TagParser;
    ParsedTag = window.ParsedTag;
}

/**
 * Options for customizing HTML glyph output rendering.
 * @typedef {Object} RenderOptions
 * @property {boolean} [useRuby=true] - Render base character with ruby annotation for variation sequences.
 * @property {boolean} [showGlyphNameTooltip=true] - Add 'title' attribute with glyph ID for mouse hover tooltips.
 * @property {string} [fallbackClass="glyph-fallback"] - CSS class assigned to glyph elements.
 */

class GlyphRenderer {
    /**
     * @param {RenderOptions} [options={}] - Configuration options for HTML generation.
     */
    constructor(options = {}) {
        this.options = Object.assign(
            {
                useRuby: true,
                showGlyphNameTooltip: true,
                fallbackClass: "glyph-tag",
            },
            options
        );
    }

    /**
     * Convert Unicode code point hex string (e.g., 'U+845B' or 'U+845B U+E0102') into actual JS string.
     *
     * @param {string} codePointStr - Space-separated hex string (e.g. "U+845B U+E0102").
     * @returns {string} Decoded Unicode string representation.
     */
    static decodeCodePoints(codePointStr) {
        if (!codePointStr) return "";
        try {
            return codePointStr
                .trim()
                .split(/\s+/)
                .map((hex) => {
                    const cleanHex = hex.replace(/^U\+?/i, "");
                    return String.fromCodePoint(parseInt(cleanHex, 16));
                })
                .join("");
        } catch (e) {
            return "";
        }
    }

    /**
     * Creates an HTML rendering replacement closure for TagParser.
     *
     * @returns {function(ParsedTag, Array): string} Replacement callback for TagParser.
     */
    createRenderReplacer() {
        const opts = this.options;

        return function renderReplacer(tag) {
            const glyphName = tag.glyphName;

            // If tag has no glyph name, return original tag text
            if (!glyphName) {
                return `{${tag.rawContent}}`;
            }

            const bVal = tag.b;
            const vVal = tag.v;

            const baseChar = GlyphRenderer.decodeCodePoints(bVal);
            const varChar = GlyphRenderer.decodeCodePoints(vVal);

            // Display text preference: Variation sequence > Base character > Glyph ID
            const charToDisplay = varChar || baseChar || glyphName;

            const tooltipAttr = opts.showGlyphNameTooltip
                ? ` title="${glyphName}${tag.set ? ` (${tag.set})` : ""}"`
                : "";

            // Ruby representation when both base and variation exist (and are different)
            if (opts.useRuby && baseChar && varChar && baseChar !== varChar) {
                return `<ruby class="${opts.fallbackClass}"${tooltipAttr}>${varChar}<rt>${baseChar}</rt></ruby>`;
            }

            // Standard span tag representation
            return `<span class="${opts.fallbackClass}" data-glyph="${glyphName}"${tooltipAttr}>${charToDisplay}</span>`;
        };
    }

    /**
     * Render glyph tags inside raw text string into browser-ready HTML.
     *
     * @param {string} text - Input text containing normalized or raw glyph tags.
     * @param {boolean} [unescape=true] - If true, converts escaped placeholders ('{{') to '{'.
     * @returns {string} Rendered HTML string.
     */
    renderToHtml(text, unescape = true) {
        if (!text) return "";
        const replacer = this.createRenderReplacer();
        return TagParser.processPipeline(text, replacer, unescape);
    }
}

// Module export compatibility (Node.js / ES Module / Browser global)
if (typeof module !== "undefined" && module.exports) {
    module.exports = { GlyphRenderer };
} else if (typeof window !== "undefined") {
    window.GlyphRenderer = GlyphRenderer;
}

