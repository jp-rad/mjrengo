"""
xlsx_strict_ooxml_loader.py
===========================

Strict OOXML (ISO/IEC 29500 Strict) 形式の XLSX を確実に読み取るための
行政系 Excel 専用ローダーモジュール。

本モジュールは、以下の特徴を持つ行政系 XLSX を対象とする：

- workbook.xml に r:id が存在しない（Strict OOXML 固有の構造）
- sheetId によりシートを識別する必要がある
- sharedStrings.xml が巨大または rich text を含む
- pandas / openpyxl が正常に読み込めないケースがある
- 法務省・IPA・NINJAL・MJ 文字情報基盤などの行政系 Excel で使用される

提供機能：
- Strict OOXML の workbook.xml から 1枚目のシートを特定
- sharedStrings.xml の読み込み（rich text 完全対応）
- sheet XML の行データ抽出（セル参照 A1/B1/C1... を保持）
- A1, B1, C1... のセル参照から列名を復元するヘッダー解析

非対象：
- Transitional OOXML（一般的な Excel）
- xls（BIFF）形式
- マクロ付き Excel（xlsm）

本モジュールは Strict OOXML の構造に依存しており、
一般的な Excel ローダーの「共通化」ではなく、
行政系 XLSX のための「専用ローダー基盤」として設計されている。
"""

from __future__ import annotations
import zipfile
import xml.etree.ElementTree as ET


# ------------------------------------------------------------
# workbook.xml → 1枚目のシートの XML ファイル名を取得
# ------------------------------------------------------------

def find_first_sheet_filename(z: zipfile.ZipFile) -> str:
    """
    Strict OOXML の workbook.xml は r:id を持たないことがある。
    その場合は sheetId=1 を 1枚目とみなし、
    xl/worksheets/sheet1.xml を返す。
    """

    wb_xml = z.read("xl/workbook.xml")
    wb_root = ET.fromstring(wb_xml)

    # namespace 自動判定
    ns_uri = wb_root.tag.split("}")[0].strip("{")
    ns = f"{{{ns_uri}}}"

    sheet_elems = wb_root.findall(f".//{ns}sheet")
    if not sheet_elems:
        raise ValueError("workbook.xml に <sheet> がありません")

    first_sheet = sheet_elems[0]

    # Transitional OOXML の場合は r:id がある
    rid = first_sheet.attrib.get(
        "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    )

    if rid is None:
        # Strict OOXML の場合は sheetId を使う
        sheet_id = first_sheet.attrib.get("sheetId")
        if sheet_id is None:
            raise ValueError("Strict OOXML: sheetId がありません")
        return f"xl/worksheets/sheet{sheet_id}.xml"

    # Transitional OOXML の場合（r:id がある）
    rels_xml = z.read("xl/_rels/workbook.xml.rels")
    rels_root = ET.fromstring(rels_xml)

    rels_ns_uri = rels_root.tag.split("}")[0].strip("{")
    rels_ns = f"{{{rels_ns_uri}}}"

    for rel in rels_root.findall(f".//{rels_ns}Relationship"):
        if rel.attrib.get("Id") == rid:
            target = rel.attrib.get("Target")
            return "xl/" + target

    raise ValueError(f"workbook.xml.rels に r:id={rid} がありません")


# ------------------------------------------------------------
# sharedStrings.xml の読み込み（rich text 対応）
# ------------------------------------------------------------

def load_shared_strings(z: zipfile.ZipFile, rich: bool = False) -> list[str]:
    """
    sharedStrings.xml を読み込み、rich text (<r><t>) を含む場合も
    すべて連結して 1つの文字列として返す。
    """

    if "xl/sharedStrings.xml" not in z.namelist():
        return []

    ss_xml = z.read("xl/sharedStrings.xml")
    ss_root = ET.fromstring(ss_xml)

    ss_ns_uri = ss_root.tag.split("}")[0].strip("{")
    ss_ns = f"{{{ss_ns_uri}}}"

    shared = []
    if rich:
        for si in ss_root.findall(f".//{ss_ns}si"):
            # rich text 対応：複数の <t> を連結
            text = "".join(t.text or "" for t in si.findall(f".//{ss_ns}t"))
            shared.append(text)
    else:
        for si in ss_root.findall(f".//{ss_ns}si"):
            t = si.find(f".//{ss_ns}t")
            shared.append(t.text if t is not None else "")

    return shared


# ------------------------------------------------------------
# sheet XML → 行データ抽出
# ------------------------------------------------------------

def load_sheet_rows(z: zipfile.ZipFile, sheet_filename: str) -> list[dict[str, str]]:
    """
    sheet XML を読み込み、行ごとに {セル参照: 値} の dict を返す。
    Strict OOXML の namespace を自動判定する。
    """

    sheet_xml = z.read(sheet_filename)
    root = ET.fromstring(sheet_xml)

    ns_uri = root.tag.split("}")[0].strip("{")
    ns = f"{{{ns_uri}}}"

    shared = load_shared_strings(z)

    rows = []
    for row in root.findall(f".//{ns}row"):
        record = {}
        for c in row.findall(f"{ns}c"):
            cell_ref = c.attrib.get("r")
            cell_type = c.attrib.get("t")
            v = c.find(f"{ns}v")

            if v is None:
                value = ""
            else:
                raw = v.text
                if cell_type == "s":
                    # sharedStrings の index
                    value = shared[int(raw)]
                else:
                    value = raw

            record[cell_ref] = value

        rows.append(record)

    return rows


# ------------------------------------------------------------
# ヘッダー解析（A1, B1, C1 → 列名）
# ------------------------------------------------------------

def parse_header(rows: list[dict[str, str]]) -> dict[str, str]:
    """
    1行目（ヘッダー行）から列名を抽出する。
    A1 → "MJ文字図形名" のように、
    {列記号: 列名} の dict を返す。
    """

    if not rows:
        raise ValueError("sheet XML に <row> がありません")

    header_row = rows[0]
    headers = {}

    for cell_ref, value in header_row.items():
        # A1 → A, B1 → B
        col = "".join([c for c in cell_ref if c.isalpha()])
        headers[col] = value.strip()

    return headers
