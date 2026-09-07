/**
 * Unit tests for index.js public API
 * ASCII-only comments only.
 */

import {
    MARK_LB,
    TAG_PATTERN,
    IssueLevel,
    TagIssue,
    ParsedTag,
    TagParser,
    makeReplaceFn,
    NormalizationResult,
    GlyphNormalizer,
    GlyphRenderer,
    renderOnly,
    normalizeAndRender,
} from "../src/index.js";

describe("index.js re-exports", () => {
    test("TagParser is exported", () => {
        expect(typeof TagParser.processPipeline).toBe("function");
    });

    test("GlyphNormalizer is exported", () => {
        const norm = new GlyphNormalizer({}, "mj");
        expect(norm instanceof GlyphNormalizer).toBe(true);
    });

    test("GlyphRenderer is exported", () => {
        const renderer = new GlyphRenderer();
        expect(renderer instanceof GlyphRenderer).toBe(true);
    });

    test("makeReplaceFn is exported", () => {
        expect(typeof makeReplaceFn).toBe("function");
    });

    test("NormalizationResult is exported", () => {
        const r = new NormalizationResult("x", []);
        expect(r instanceof NormalizationResult).toBe(true);
    });

    test("MARK_LB is exported", () => {
        expect(typeof MARK_LB).toBe("string");
    });

    test("TAG_PATTERN is exported", () => {
        expect(TAG_PATTERN instanceof RegExp).toBe(true);
    });
});

describe("renderOnly", () => {
    test("empty text returns empty string", () => {
        const out = renderOnly("");
        expect(out).toBe("");
    });

    test("basic rendering", () => {
        const out = renderOnly("A {MJ000001 b=U+3005 v=U+3005}");
        expect(out).toContain("<span");
        expect(out).toContain("\u3005");
    });

    test("escape '{{' then unescape to '{'", () => {
        const out = renderOnly("Start {{X}} {MJ000001 b=U+3005}");
        expect(out.startsWith("Start {X}")).toBe(true);
    });

    test("unescape=false preserves '{{'", () => {
        const out = renderOnly("Start {{X}} {MJ000001 b=U+3005}", { unescape: false });
        expect(out.startsWith("Start {X}}")).toBe(true);
    });
});

describe("normalizeAndRender", () => {
    const GLYPH_TABLE = {
        MJ000001: { b: "U+3005", v: "U+3005", active: true },
        MJ000012: { b: "U+FFFF", v: "U+FFFF", active: false },
        MJ022335: { b: "U+845B", v: "U+845B U+E0102", active: true },
    };

    test("full pipeline: normalize then render", () => {
        const { html, issues } = normalizeAndRender(
            "A {MJ000001} B",
            GLYPH_TABLE,
            "mj"
        );

        expect(html).toContain("\u3005");
        expect(html).toContain("<span");
        expect(issues.length).toBe(0);
    });

    test("inactive glyph produces error", () => {
        const { html, issues } = normalizeAndRender(
            "A {MJ000012} B",
            GLYPH_TABLE,
            "mj"
        );

        expect(html).toContain("{MJ000012}");
        expect(issues.length).toBe(1);
        expect(issues[0].code).toBe("error.glyph.archived");
    });

    test("unknown glyph produces error", () => {
        const { html, issues } = normalizeAndRender(
            "A {UNKNOWN} B",
            GLYPH_TABLE,
            "mj"
        );

        expect(html).toContain("{UNKNOWN}");
        expect(issues.length).toBe(1);
        expect(issues[0].code).toBe("error.glyph.not_found");
    });

    test("multiple tags mixed", () => {
        const { html, issues } = normalizeAndRender(
            "A {MJ000001} B {UNKNOWN} C {MJ000012} D {MJ022335}",
            GLYPH_TABLE,
            "mj"
        );

        expect(html).toContain("\u3005");
        expect(html).toContain("{UNKNOWN}");
        expect(html).toContain("{MJ000012}");
        expect(html).toContain("\u845B\uE0102");

        expect(issues.length).toBe(2);
    });

    test("escape '{{' then unescape to '{'", () => {
        const { html } = normalizeAndRender(
            "Start {{X}} {MJ000001}",
            GLYPH_TABLE,
            "mj"
        );

        expect(html.startsWith("Start {X}")).toBe(true);
    });

    test("unescape=false preserves '{{'", () => {
        const { html } = normalizeAndRender(
            "Start {{X}} {MJ000001}",
            GLYPH_TABLE,
            "mj",
            { unescape: false }
        );

        expect(html.startsWith("Start {{X}}")).toBe(true);
    });
});

