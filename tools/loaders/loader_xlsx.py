# tools/loaders/loader_mji00602_xlsx.py

import pandas as pd
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


def load_mji_00602_xlsx(path: Path) -> dict[str, GlyphRecord]:
    """
    mji.00602.xlsx 専用の XLSX ローダー。

    対応する列仕様（mji.00602.xlsx 固有）:
        - MJ文字図形名
        - 対応するUCS
        - 実装したMoji_JohoコレクションIVS
        - font

    この関数は mji.00602.xlsx の列構成に依存しており、
    他のバージョンの MJ コレクション XLSX では動作しない。

    Returns:
        dict[str, GlyphRecord]
        key = glyph_name (MJ文字図形名)
    """

    records: dict[str, GlyphRecord] = {}

    df = pd.read_excel(path, dtype=str)
    # df = pd.read_excel(path, dtype=str, engine="openpyxl")
    if not REQUIRED_COLUMNS.issubset(df.columns):
        missing = REQUIRED_COLUMNS - set(df.columns)
        raise ValueError(f"Missing required columns in XLSX: {missing}")

    for _, row in df.iterrows():

        # --- glyph_name ---
        glyph_name_raw = row[COL_MJ_NAME]
        if glyph_name_raw is None or pd.isna(glyph_name_raw):
            continue
        glyph_name = str(glyph_name_raw).strip()

        # --- font 判定 ---
        font_raw = row[COL_FONT]
        font_value = str(font_raw).strip() if font_raw is not None else ""

        # --- rep 判定 ---
        rep_raw = row[COL_REP]

        # rep が空、または font が "実装なし" の場合は active=False
        if rep_raw is None or pd.isna(rep_raw) or font_value == "実装なし":
            active = False
            rep = None
            ucs = None
            comment = "実装なし"

        else:
            active = True

            # REP 正規化
            rep = to_uplus_string(str(rep_raw).strip())
            ok, reason = validate_uplus_input(rep)
            if not ok:
                raise ValueError(f"Invalid REP for {glyph_name}: {reason}")

            # UCS（IVS）選択
            ucs_raw = row[COL_UCS_IVS]
            if ucs_raw is None or pd.isna(ucs_raw):
                ucs = rep
            else:
                ucs = pick_ucs_by_rep(ucs_raw, rep)
                ok, reason = validate_uplus_input(ucs)
                if not ok:
                    raise ValueError(f"Invalid UCS for {glyph_name}: {reason}")

            # コメント（REP の UCS 名）
            comment = sanitize_comment(decode_ucs(rep))

        # --- レコード生成 ---
        rec = GlyphRecord(
            glyph_name=glyph_name,
            ucs=ucs,
            rep=rep,
            active=active,
            comment=comment,
        )

        records[glyph_name] = rec

    return records


def load_mji_00602_xlsx_as_zip(path: Path) -> dict[str, GlyphRecord]:
    with zipfile.ZipFile(path, "r") as z:

        # --- sheet1.xml を読む ---
        sheet_xml = z.read("xl/worksheets/sheet1.xml")
        root = ET.fromstring(sheet_xml)

        # Namespace 自動判定（Strict / Transitional 両対応）
        tag = root.tag
        if tag.startswith("{"):
            ns_uri = tag.split("}")[0].strip("{")
        else:
            raise ValueError("Invalid worksheet XML")

        ns = f"{{{ns_uri}}}"

        # --- sharedStrings.xml ---
        shared_strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            ss_xml = z.read("xl/sharedStrings.xml")
            ss_root = ET.fromstring(ss_xml)

            ss_tag = ss_root.tag
            ss_ns_uri = ss_tag.split("}")[0].strip("{")
            ss_ns = f"{{{ss_ns_uri}}}"

            for si in ss_root.findall(f".//{ss_ns}si"):
                t = si.find(f".//{ss_ns}t")
                shared_strings.append(t.text if t is not None else "")

        # --- 行データ抽出（Strict OOXML 対応） ---
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
        raise ValueError("sheet1.xml に <row> がありません（Strict OOXML の空シート）")

    # --- ヘッダー行 ---
    header_row = rows[0]
    headers = {}

    for cell_ref, value in header_row.items():
        col = "".join([c for c in cell_ref if c.isalpha()])
        headers[col] = value.strip()

    if not REQUIRED_COLUMNS.issubset(headers.values()):
        missing = REQUIRED_COLUMNS - set(headers.values())
        raise ValueError(f"Missing required columns in XLSX: {missing}")

    col_map = {v: k for k, v in headers.items()}

    def get(row_dict, col_name):
        col = col_map[col_name]
        for cell_ref, value in row_dict.items():
            if cell_ref.startswith(col):
                return value.strip()
        return ""

    records: dict[str, GlyphRecord] = {}

    for row_dict in rows[1:]:

        glyph_name = get(row_dict, COL_MJ_NAME)
        if glyph_name == "":
            continue

        font_value = get(row_dict, COL_FONT)
        rep_raw = get(row_dict, COL_REP)

        if rep_raw == "" or font_value == "実装なし":
            active = False
            rep = None
            ucs = None
            comment = "実装なし"

        else:
            active = True

            rep = to_uplus_string(rep_raw)
            ok, reason = validate_uplus_input(rep)
            if not ok:
                raise ValueError(f"Invalid REP for {glyph_name}: {reason}")

            ucs_raw = get(row_dict, COL_UCS_IVS)
            if ucs_raw == "":
                ucs = rep
            else:
                ucs = pick_ucs_by_rep(ucs_raw, rep)
                ok, reason = validate_uplus_input(ucs)
                if not ok:
                    raise ValueError(f"Invalid UCS for {glyph_name}: {reason}")

            comment = sanitize_comment(decode_ucs(rep))

        rec = GlyphRecord(
            glyph_name=glyph_name,
            ucs=ucs,
            rep=rep,
            active=active,
            comment=comment,
        )

        records[glyph_name] = rec

    return records
