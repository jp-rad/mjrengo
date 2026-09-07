/**
 * Unit tests for index.js (tofurengo_js)
 * ASCII-only comments only.
 */

import { describe, test, expect } from "vitest";

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
  ucsToGlyph,
  renderOnly,
  normalizeAndRender,
} from "../src/index.js";

//
// Basic sanity checks for re-exported primitives
//
describe("index.js re-exports", () => {
  test("MARK_LB is defined", () => {
    expect(MARK_LB).toBe("\u0002");
  });

  test("TAG_PATTERN matches basic tag", () => {
    const m = "{MJ000001 b=U+3005}".match(TAG_PATTERN);
    expect(m).not.toBeNull();
  });

  test("IssueLevel contains expected keys", () => {
    expect(IssueLevel.ERROR).toBe("error");
    expect(IssueLevel.WARNING).toBe("warning");
  });

  test("ucsToGlyph works", () => {
    expect(ucsToGlyph("U+3005")).toBe("\u{3005}");
    expect(ucsToGlyph("ABC")).toBe("ABC");
  });
});

//
// Tests for renderOnly
//
describe("renderOnly", () => {
  test("empty text returns empty string", () => {
    const out = renderOnly("");
    expect(out).toBe("");
  });

  test("basic rendering", () => {
    const out = renderOnly("A {MJ000001 b=U+3005 v=U+3005}");
    expect(out).toBe("A \u{3005}");
  });

  test("useBase=true overrides variant", () => {
    const out = renderOnly("{MJ022335 b=U+845B v=U+845B U+E0102}", true);
    expect(out).toBe("\u{845B}");
  });

  test("tofu override works", () => {
    const out = renderOnly("{MJ999999}", false, "U+3005");
    expect(out).toBe("\u{3005}");
  });

  test("double braces '{{' unescaped to '{'", () => {
    const out = renderOnly("Start {{X}}");
    expect(out).toBe("Start {X}}");
  });
});

//
// Tests for normalizeAndRender
//
describe("normalizeAndRender", () => {
  const glyphTable = {
    MJ000001: { b: "U+3005", v: "U+3005", active: true },
    MJ022335: { b: "U+845B", v: "U+845B U+E0102", active: true },
    MJ999999: { active: false },
  };

  test("basic normalize + render", () => {
    const out = normalizeAndRender(
      "A {MJ000001} B {MJ022335}",
      glyphTable,
      "mj"
    );
    expect(out.text).toBe("A \u{3005} B \u{845B}\u{E0102}");
  });

  test("inactive glyph produces tofu", () => {
    const out = normalizeAndRender("{MJ999999}", glyphTable, "mj");
    expect(out.text).toBe("\u{25A1}");
    expect(out.issues.length).toBeGreaterThan(0);
  });

  test("useBase=true overrides variant", () => {
    const out = normalizeAndRender(
      "{MJ022335}",
      glyphTable,
      "mj",
      true
    );
    expect(out.text).toBe("\u{845B}");
  });

  test("tofu override works", () => {
    const out = normalizeAndRender(
      "{MJ999999}",
      glyphTable,
      "mj",
      false,
      "U+3005"
    );
    expect(out.text).toBe("\u{3005}");
  });

  test("unescape=false preserves '{{'", () => {
    const out = normalizeAndRender(
      "Start {{X}} {MJ000001}",
      glyphTable,
      "mj",
      false,
      "U+25A1"
    );
    expect(out.text.startsWith("Start {X}}")).toBe(true);
  });

  test("issues propagate from normalizer", () => {
    const out = normalizeAndRender(
      "{MJ999999}",
      glyphTable,
      "mj"
    );
    expect(out.issues.length).toBeGreaterThan(0);
    const issue = out.issues[0];
    expect(issue).toBeInstanceOf(TagIssue);
  });
});

