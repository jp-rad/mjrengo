/**
 * tofurengo_js - Client-side glyph tag parsing, normalization, and rendering toolkit.
 *
 * @module tofurengo_js
 */

import {
    MARK_LB,
    TAG_PATTERN,
    IssueLevel,
    TagIssue,
    ParsedTag,
    TagParser,
} from "./tag_parser.js";

import {
    makeReplaceFn,
    NormalizationResult,
    GlyphNormalizer,
} from "./glyph_normalizer.js";

import { GlyphRenderer } from "./glyph_renderer.js";

// Re-export all public components
export {
    // Tag Parser module
    MARK_LB,
    TAG_PATTERN,
    IssueLevel,
    TagIssue,
    ParsedTag,
    TagParser,
    // Normalizer module (includes makeReplaceFn)
    makeReplaceFn,
    NormalizationResult,
    GlyphNormalizer,
    // Renderer module
    GlyphRenderer,
};

/**
 * Convenient helper function to directly render text containing glyph tags to HTML
 * without applying dataset table normalization.
 *
 * @param {string} text - Input text containing normalized or raw glyph tags.
 * @param {Object} [renderOptions={}] - Options passed to GlyphRenderer.
 * @returns {string} Rendered HTML string.
 */
export function renderOnly(text, renderOptions = {}) {
    const renderer = new GlyphRenderer(renderOptions);
    return renderer.renderToHtml(text);
}

/**
 * Convenient all-in-one helper function to normalize and immediately render text to HTML.
 *
 * @param {string} text - Raw input text with glyph tags.
 * @param {Object.<string, Object>} glyphTable - Dataset table mapping glyph IDs to attributes.
 * @param {string} setName - Dataset identifier (e.g., 'mj').
 * @param {Object} [renderOptions={}] - Options passed to GlyphRenderer.
 * @returns {{ html: string, issues: Array<TagIssue> }} Object containing rendered HTML and encountered issues.
 */
export function normalizeAndRender(text, glyphTable, setName, renderOptions = {}) {
    const normalizer = new GlyphNormalizer(glyphTable, setName);
    const normalizationResult = normalizer.normalize(text);

    const html = renderOnly(normalizationResult.text, renderOptions);

    return {
        html,
        issues: normalizationResult.issues,
    };
}

