/**
 * Unit tests for glyph_renderer.js
 * ASCII-only comments only.
 */

import { GlyphRenderer } from "../src/glyph_renderer.js";
import { TagParser, ParsedTag } from "../src/tag_parser.js";

describe("GlyphRenderer.decodeCodePoints", () => {
  test("single code point", () => {
    const out = GlyphRenderer.decodeCodePoints("U+3005");
    expect(out).toBe("\u{3005}");
  });

  test("multiple code points", () => {
    const out = GlyphRenderer.decodeCodePoints("U+845B U+E0102");
    expect(out).toBe("\u{845B}\u{E0102}");
  });

  test("invalid input returns empty string", () => {
    const out = GlyphRenderer.decodeCodePoints("INVALID");
    expect(out).toBe("");
  });

  test("empty input returns empty string", () => {
    const out = GlyphRenderer.decodeCodePoints("");
    expect(out).toBe("");
  });
});

describe("GlyphRenderer.createRenderReplacer", () => {
  const renderer = new GlyphRenderer({
    useRuby: true,
    showGlyphNameTooltip: true,
    fallbackClass: "glyph-test",
  });

  const replacer = renderer.createRenderReplacer();

  test("missing glyphName returns raw tag", () => {
    const tag = new ParsedTag("", {}, "");
    const out = replacer(tag);
    expect(out).toBe("{}");
  });

  test("span rendering when no variation", () => {
    const tag = new ParsedTag(
      "MJ000001",
      { b: "U+3005", v: "U+3005", set: "mj" },
      "MJ000001"
    );
    const out = replacer(tag);
    expect(out).toContain("<span");
    expect(out).toContain("glyph-test");
    expect(out).toContain('data-glyph="MJ000001"');
    expect(out).toContain('title="MJ000001 (mj)"');
    expect(out).toContain("\u{3005}");
  });

  test("ruby rendering when base and variation differ", () => {
    const tag = new ParsedTag(
      "MJ022335",
      { b: "U+845B", v: "U+845B U+E0102", set: "mj" },
      "MJ022335"
    );
    const out = replacer(tag);
    expect(out.startsWith("<ruby")).toBe(true);
    expect(out).toContain("glyph-test");
    expect(out).toContain("\u{845B}\u{E0102}"); // variation
    expect(out).toContain("<rt>\u{845B}</rt>"); // base
  });

  test("no ruby when useRuby=false", () => {
    const renderer2 = new GlyphRenderer({
      useRuby: false,
      fallbackClass: "glyph-test",
    });
    const replacer2 = renderer2.createRenderReplacer();
    const tag = new ParsedTag(
      "MJ022335",
      { b: "U+845B", v: "U+845B U+E0102" },
      "MJ022335"
    );
    const out = replacer2(tag);
    expect(out.startsWith("<span")).toBe(true);
    expect(out).toContain("\u{845B}\u{E0102}");
  });

  test("tooltip disabled", () => {
    const renderer3 = new GlyphRenderer({
      showGlyphNameTooltip: false,
      fallbackClass: "glyph-test",
    });
    const replacer3 = renderer3.createRenderReplacer();
    const tag = new ParsedTag("MJ000001", { b: "U+3005" }, "MJ000001");
    const out = replacer3(tag);
    expect(out).not.toContain("title=");
  });
});

describe("GlyphRenderer.renderToHtml", () => {
  const renderer = new GlyphRenderer({
    fallbackClass: "glyph-test",
  });

  test("empty text returns empty string", () => {
    const out = renderer.renderToHtml("");
    expect(out).toBe("");
  });

  test("basic rendering", () => {
    const out = renderer.renderToHtml("A {MJ000001 b=U+3005 v=U+3005}");
    expect(out).toContain("<span");
    expect(out).toContain("\u{3005}");
  });

  test("escape '{{' then unescape to '{'", () => {
    const out = renderer.renderToHtml("Start {{X}} {MJ000001 b=U+3005}");
    expect(out.startsWith("Start {X}")).toBe(true);
  });

  test("unescape=false preserves '{{'", () => {
    const out = renderer.renderToHtml("Start {{X}} {MJ000001 b=U+3005}", false);
    expect(out.startsWith("Start {{X}}")).toBe(true);
  });

  test("multiple tags mixed", () => {
    const text =
      "A {MJ000001 b=U+3005 v=U+3005} B {MJ022335 b=U+845B v=U+845B U+E0102}";
    const out = renderer.renderToHtml(text);
    expect(out).toContain("\u{3005}");
    expect(out).toContain("\u{845B}\u{E0102}");
    expect(out).toContain("<ruby");
  });

  test("extra braces preserved", () => {
    const out = renderer.renderToHtml("{MJ000001 b=U+3005}}}");
    expect(out.endsWith("}}")).toBe(true);
  });
});

