# 📘 Glyph Tag Specification  
**Version:** 0.3.0  
**Status:** Complete  
**Author:** [jp-rad](https://github.com/jp-rad)  
**Last Updated:** 2026-08-21  


# 1. Purpose（目的）

Glyph Tag は、MJ/GJ などの字形名（glyph name）を  
**UCS（ISO/IEC 10646）コードポイント列・IVS（異体字セレクタ）・代表文字（縮退後文字）**  
とともに安全に扱うための **文字抽象化タグ形式**である。

本仕様は、Unicode の抽象的な文字体系と、  
実際のフォント実装に依存する字形体系のギャップを埋めるために設計されている。

Glyph Tag の `ucs=` は **縮退前の UCS コードポイント列（IVS を含む）**であり、  
`rep=` は **縮退後の代表文字（Representative Character）**である。

`set=` は **字形体系を表すユーザー定義識別子**であり、  
**Glyph Table 全体で 1つだけ指定される。  
entries 内の各項目は set= を持たず、テーブルの set= を継承する。**


# 2. Syntax（構文）

Glyph Tag は **2つの表記形式**を許容する。

## 2.1 完全形式

```
{glyph:<図形名> [ucs=<UCSSeq>] [rep=<UCSSeq>] [set=<Identifier>]}
```

## 2.2 省略形式

```
{<図形名> [ucs=<UCSSeq>] [rep=<UCSSeq>] [set=<Identifier>]}
```


# 2.3 Tag Recognition（タグ認識）

```
glyph 名は英数字（A–Z, a–z, 0–9）のみで構成される。

正規表現：
    glyph-name = [A-Za-z0-9]+

非英数字を含む {や}, {漢字}, {★} などは Glyph Tag として認識されない。
これらは Tag Completion の対象外であり、そのまま出力される。
```


# 2.4 Tag Escape（タグのエスケープ）

Glyph Tag をリテラルとして出力したい場合、  
波括弧を二重化して `{{` を使用する。

```
"{{MJ0001}" → "{MJ0001}"
```

### ✔ エスケープ処理の仕様（v0.4.2）

```
1. "{{" を予約タグ "{_LB_}" に一時置換する。
2. Tag Completion を実行する。
3. "{_LB_}" を単一波括弧 "{" に戻す。
```

### ✔ 予約タグ（短縮版）

```
{_LB_}
```

- LB = Left Brace  
- 衝突しない  
- 軽量  
- エスケープ専用  
- 通常の Glyph Tag として扱われない  


# 3. Attributes（属性）

| 属性 | 説明 |
|------|------|
| **glyph** | 図形名（MJ0001 / GJ0431 / EMOJI001 など）。 |
| **ucs** | 縮退前の UCS コードポイント列（U+XXXX）。IVS を含む。 |
| **rep** | 縮退後の代表文字（Representative Character）。 |
| **set** | 字形体系識別子（Glyph System Identifier）。ユーザー定義。 |


# 4. UCSSeq（UCS コードポイント列）

### ✔ UCSSeq は **U+XXXX を空白で区切った列**である。

例：

```
U+4E00
U+4E00 U+E0100
U+9AD8 U+E0101
U+1F600
```


# 5. Glyph System Identifier（字形体系識別子）

### ✔ set= はユーザー定義の識別子  
例：

```
set=dwpex
set=ipaexm
set=shsjp
set=mj+
```

### ✔ 同一システム内では set= を統一することを推奨  
Glyph Table が set= を 1つ持つことで自動的に統一される。

---

# 6. Rendering rules（レンダリング仕様）

```
mode="ucs"     → ucs → rep → unknown
mode="rep"     → rep → ucs → unknown
mode="auto"    → ucs → rep → unknown（既定）
mode="reduce"  → rep → unknown
```


# 7. Tag completion（タグ補完）

補完対象：

- `{MJ0001}`
- `{glyph:MJ0001}`
- `{GJ0431 rep=U+9AD8}`
- `{MJ0001 ucs=U+4E00 U+E0100}`

補完時に **Glyph Table の set= が自動付与される**。


# 8. Glyph Table（仕様）

```
glyph-table = {
    version: "<日付>",
    description: "<任意の説明>",
    set: "<字形体系識別子>",
    entries: {
        <glyph-name>: { ucs: "<UCSSeq>", rep: "<UCSSeq>" },
        ...
    }
}
```

### ✔ entries は set= を持たない  
### ✔ set= はテーブル全体の字形体系識別子  
### ✔ Glyph Tag の set= は補完時に付与される


# 9. Example Glyph Table（例）

```
glyph-table = {
    version: "2026-08-21",
    description: "行政事務標準フォント(DWPIexMincho.ttf)",
    set: "mj+",
    entries: {
        MJ0001: { ucs: "U+4E00 U+E0100", rep: "U+4E00" },
        GJ0431: { ucs: "U+9AD8 U+E0101", rep: "U+9AD8" },
        EMOJI001: { ucs: "U+1F600", rep: "U+1F600" }
    }
}
```


# 10. Reference Implementation（Python, v0.4.2）

予約タグ `{_LB_}` を採用した最新版。

```python
# -*- coding: utf-8 -*-
"""
Glyph Tag – Reference Implementation (Version 0.4.2)
"""

import re
import codecs

ESCAPED = "{_LB_}"

# ----------------------------------------------------------------------
# 1. Glyph Table (example)
# ----------------------------------------------------------------------

GLYPH_TABLE = {
    "version": "2026-08-21",
    "description": "行政事務標準フォント(DWPIexMincho.ttf)",
    "set": "mj+",
    "entries": {
        "MJ0001": { "ucs": "U+4E00 U+E0100", "rep": "U+4E00" },
        "GJ0431": { "ucs": "U+9AD8 U+E0101", "rep": "U+9AD8" },
        "EMOJI001": { "ucs": "U+1F600", "rep": "U+1F600" }
    }
}

# ----------------------------------------------------------------------
# 2. Tag pattern
# ----------------------------------------------------------------------

GLYPH_TAG_PATTERN = re.compile(
    r'\{(?:glyph:)?(?P<glyph>[A-Za-z0-9]+)'
    r'(?:\s+ucs=(?P<ucs>(?:U\+[0-9A-Fa-f]{4,6}(?:\s+U\+[0-9A-Fa-f]{4,6})*)))?'
    r'(?:\s+rep=(?P<rep>(?:U\+[0-9A-Fa-f]{4,6}(?:\s+U\+[0-9A-Fa-f]{4,6})*)))?'
    r'(?:\s+set=(?P<set>[A-Za-z0-9_+\-]+))?'
    r'\}'
)

# ----------------------------------------------------------------------
# 3. UCS → JSON Unicode escape
# ----------------------------------------------------------------------

def ucs_to_json_escape(ucs_seq: str) -> str:
    cps = re.findall(r"U\+([0-9A-Fa-f]{4,6})", ucs_seq)
    esc = ""
    for cp_hex in cps:
        cp = int(cp_hex, 16)
        if cp <= 0xFFFF:
            esc += f"\\u{cp:04X}"
        else:
            cp -= 0x10000
            high = 0xD800 + (cp >> 10)
            low  = 0xDC00 + (cp & 0x3FF)
            esc += f"\\u{high:04X}\\u{low:04X}"
    return esc

def json_escape_to_text(s: str) -> str:
    return codecs.decode(s, "unicode_escape")

# ----------------------------------------------------------------------
# 4. Escape processing
# ----------------------------------------------------------------------

def escape_braces(text: str) -> str:
    return text.replace("{{", ESCAPED)

def unescape_braces(text: str) -> str:
    return text.replace(ESCAPED, "{")

# ----------------------------------------------------------------------
# 5. Tag completion
# ----------------------------------------------------------------------

def build_tag(glyph_name: str, info: dict, table_set: str) -> str:
    parts = [f"glyph:{glyph_name}"]
    if info.get("ucs"):
        parts.append(f"ucs={info['ucs']}")
    if info.get("rep"):
        parts.append(f"rep={info['rep']}")
    parts.append(f"set={table_set}")
    return "{" + " ".join(parts) + "}"

def expand_tag(match: re.Match) -> str:
    glyph = match.group("glyph")
    table_set = GLYPH_TABLE["set"]
    info = GLYPH_TABLE["entries"].get(glyph)
    if not info:
        return match.group(0)
    return build_tag(glyph, info, table_set)

def expand_all(text: str) -> str:
    text = escape_braces(text)
    text = GLYPH_TAG_PATTERN.sub(expand_tag, text)
    text = unescape_braces(text)
    return text

# ----------------------------------------------------------------------
# 6. Rendering
# ----------------------------------------------------------------------

def render(parsed: dict, mode: str = "auto", unknown: str = "□") -> str:
    ucs = parsed.get("ucs")
    rep = parsed.get("rep")

    if mode == "ucs":
        if ucs:
            return json_escape_to_text(ucs_to_json_escape(ucs))
        if rep:
            return json_escape_to_text(ucs_to_json_escape(rep))
        return unknown

    if mode == "rep" or mode == "reduce":
        if rep:
            return json_escape_to_text(ucs_to_json_escape(rep))
        if ucs:
            return json_escape_to_text(ucs_to_json_escape(ucs))
        return unknown

    if ucs:
        return json_escape_to_text(ucs_to_json_escape(ucs))
    if rep:
        return json_escape_to_text(ucs_to_json_escape(rep))
    return unknown

def render_text(text: str, mode: str = "auto", unknown: str = "□") -> str:
    def _replace(m: re.Match) -> str:
        parsed = {
            "glyph": m.group("glyph"),
            "ucs": m.group("ucs"),
            "rep": m.group("rep"),
            "set": m.group("set"),
        }
        return render(parsed, mode=mode, unknown=unknown)

    return GLYPH_TAG_PATTERN.sub(_replace, text)
```


# 11. Examples（例）

```
入力:
これは{{MJ0001}です。これは{MJ0001}です。

出力:
これは{MJ0001}です。これは一です。
```
