# tools/loaders/loader_mji_00602_xlsx.py

from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET

from mjrengo.ucs import decode_ucs
from tools.core.model import GlyphRecord
from tools.core.normalize import (
    to_uplus_string,
    validate_uplus_input,
    pick_ucs_by_rep,
    sanitize_comment,
)

# === mji.00602.xlsx 固有の列名定数 ===

COL_MJ_NAME = "MJ文字図形名"
COL_REP     = "対応するUCS"
COL_UCS_IVS = "実装したMoji_JohoコレクションIVS"
COL_FONT    = "font"

REQUIRED_COLUMNS = {
    COL_MJ_NAME,
    COL_REP,
    COL_UCS_IVS,
    COL_FONT,
}


# ------------------------------------------------------------
# workbook.xml → 1枚目のシートの XML ファイル名を取得
# ------------------------------------------------------------

def _find_first_sheet_filename(z: zipfile.ZipFile) -> str:
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

    # Strict OOXML: r:id が存在しない
    rid = first_sheet.attrib.get(
        "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    )

    if rid is None:
        # Strict OOXML の場合は sheetId を使う
        sheet_id = first_sheet.attrib.get("sheetId")
        if sheet_id is None:
            raise ValueError("Strict OOXML: sheetId がありません")

        # sheetId=1 → sheet1.xml
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
# Strict OOXML 専用ローダー本体
# ------------------------------------------------------------

def load_mji_00602_xlsx(path: Path) -> dict[str, GlyphRecord]:
    """
    Strict OOXML 専用ローダー。
    pandas / openpyxl が壊れる行政系 XLSX を確実に読み取る。

    - workbook.xml で 1枚目のシートを特定
    - sharedStrings.xml を使って文字列を復元（先頭ゼロ保持）
    - sheet XML を Strict OOXML の namespace で解析
    - 列名は A1, B1, C1... のセル内容から取得
    - font="実装なし" → active=False
    """

    with zipfile.ZipFile(path, "r") as z:

        # --- 1枚目のシートの XML ファイル名 ---
        sheet_filename = _find_first_sheet_filename(z)

        # --- sheet XML ---
        sheet_xml = z.read(sheet_filename)
        root = ET.fromstring(sheet_xml)

        # namespace 自動判定
        ns_uri = root.tag.split("}")[0].strip("{")
        ns = f"{{{ns_uri}}}"

        # --- sharedStrings.xml ---
        shared_strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            ss_xml = z.read("xl/sharedStrings.xml")
            ss_root = ET.fromstring(ss_xml)

            ss_ns_uri = ss_root.tag.split("}")[0].strip("{")
            ss_ns = f"{{{ss_ns_uri}}}"

            for si in ss_root.findall(f".//{ss_ns}si"):
                t = si.find(f".//{ss_ns}t")
                shared_strings.append(t.text if t is not None else "")

        # --- 行データ抽出 ---
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
                        value = shared_strings[int(raw)]
                    else:
                        value = raw

                record[cell_ref] = value

            rows.append(record)

    if not rows:
        raise ValueError("sheet XML に <row> がありません（Strict OOXML の空シート）")

    # --- ヘッダー行 ---
    header_row = rows[0]
    headers = {}

    for cell_ref, value in header_row.items():
        col = "".join([c for c in cell_ref if c.isalpha()])
        headers[col] = value.strip()

    # 必須列チェック
    if not REQUIRED_COLUMNS.issubset(headers.values()):
        missing = REQUIRED_COLUMNS - set(headers.values())
        raise ValueError(f"Missing required columns in XLSX: {missing}")

    # 列名 → 列記号（A, B, C...）
    col_map = {v: k for k, v in headers.items()}

    def get(row_dict, col_name):
        col = col_map[col_name]
        for cell_ref, value in row_dict.items():
            if cell_ref.startswith(col):
                return value.strip()
        return ""

    # --- レコード生成 ---
    records: dict[str, GlyphRecord] = {}

    for row_dict in rows[1:]:
        comments = []

        glyph_name = get(row_dict, COL_MJ_NAME)
        if glyph_name == "":
            continue

        font_value = get(row_dict, COL_FONT)
        active = font_value != "実装なし"
        
        rep_raw = get(row_dict, COL_REP)
        
        rep = to_uplus_string(rep_raw)
        if rep:
            ok, reason = validate_uplus_input(rep)
            if not ok:
                raise ValueError(f"Invalid REP for {glyph_name}: {reason}")
            # コメント：代表文字
            comments.append(decode_ucs(rep))

            ucs_raw = get(row_dict, COL_UCS_IVS)
            if ucs_raw == "":
                ucs = rep
            else:
                has_multiple = ";" in ucs_raw
                if has_multiple:
                    # コメント：複数の UCS 候補
                    comments.append(ucs_raw)
                ucs = pick_ucs_by_rep(ucs_raw, rep)
                ok, reason = validate_uplus_input(ucs)
                if not ok:
                    raise ValueError(f"Invalid UCS for {glyph_name}: {reason}")
        else:
            rep = None
            ucs = None

        rec = GlyphRecord(
            glyph_name=glyph_name,
            ucs=ucs,
            rep=rep,
            active=active,
            comment=sanitize_comment(" ".join(comments)),
        )

        records[glyph_name] = rec

    return records
