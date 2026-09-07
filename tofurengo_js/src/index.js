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

import { GlyphRenderer, ucsToGlyph } from "./glyph_renderer.js";

// Re-export all public components and primitives
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
    ucsToGlyph,
};

/**
 * Convenient helper function to directly render text containing normalized glyph tags
 * into Unicode character strings without applying dataset table normalization.
 *
 * @param {string} text - Input text containing normalized or raw glyph tags.
 * @param {boolean} [useBase=false] - If true, prioritizes base character attributes (`b=`).
 * @param {string} [tofu="U+25A1"] - Fallback UCS sequence or literal character.
 * @returns {string} Rendered Unicode output text.
 */
export function renderOnly(text, useBase = false, tofu = "U+25A1") {
    const renderer = new GlyphRenderer(useBase, tofu);
    return renderer.render(text);
}

/**
 * Convenient all-in-one helper function to normalize and immediately render text into Unicode string.
 *
 * @param {string} text - Raw input text with glyph tags.
 * @param {Object.<string, Object>} glyphTable - Dataset table mapping glyph IDs to attributes.
 * @param {string} setName - Dataset identifier (e.g., 'mj').
 * @param {boolean} [useBase=false] - If true, prioritizes base character attributes (`b=`).
 * @param {string} [tofu="U+25A1"] - Fallback UCS sequence or literal character.
 * @returns {{ text: string, issues: Array<TagIssue> }} Object containing rendered text and encountered issues.
 */
export function normalizeAndRender(text, glyphTable, setName, useBase = false, tofu = "U+25A1") {
    const normalizer = new GlyphNormalizer(glyphTable, setName);
    const normalizationResult = normalizer.normalize(text);

    const renderedText = renderOnly(normalizationResult.text, useBase, tofu);

    return {
        text: renderedText,
        issues: normalizationResult.issues,
    };
}

