# tools/loaders/loader_mjih_00201_xlsx.py

from __future__ import annotations
from pathlib import Path
import zipfile

from tools.loaders.xlsx_strict_ooxml_loader import (
    find_first_sheet_filename,
    load_sheet_rows,
    parse_header,
)

from tools.core.model import GlyphRecord
from tools.core.normalize import (
    to_uplus_string,
    validate_uplus_input,
    sanitize_comment,
)


# ------------------------------------------------------------
# 参照する列名
# ------------------------------------------------------------

COL_MJ_NAME     = "MJ文字図形名"
COL_FONT        = "font文字"
COL_UCS         = "UCS符号位置"
COL_JIMO        = "字母"
COL_JIMO_UCS    = "字母のUCS符号位置"
COL_ONKA1       = "音価１"
COL_ONKA2       = "音価２"
COL_ONKA3       = "音価３"
COL_NOTE        = "備考"

REQUIRED_COLUMNS = {
    COL_MJ_NAME,
    COL_FONT,
    COL_UCS,
    COL_JIMO,
    COL_JIMO_UCS,
    COL_ONKA1,
    COL_ONKA2,
    COL_ONKA3,
    COL_NOTE,
}


# ------------------------------------------------------------
# ローダー本体
# ------------------------------------------------------------

def load_mjih_00201_xlsx(path: Path) -> list[GlyphRecord]:
    """
    MJ文字情報一覧表 変体仮名編 Ver.002.01 専用 Strict OOXML ローダー。

    - 1行目セル値をヘッダーとして使用
    - b = 字母のUCS符号位置
    - v = UCS符号位置（変体仮名自身）※空欄なら None
    - active = UCS がある場合 True、空欄なら False（統合・廃止）
    - comment = 字母 + 音価1/2/3 + 統合先（備考）
    """

    with zipfile.ZipFile(path, "r") as z:
        sheet_filename = find_first_sheet_filename(z)
        rows = load_sheet_rows(z, sheet_filename)
        headers = parse_header(rows)

    # --- 必須列チェック ---
    if not REQUIRED_COLUMNS.issubset(headers.values()):
        missing = REQUIRED_COLUMNS - set(headers.values())
        raise ValueError(f"Missing required columns in XLSX: {missing}")

    # 列名 → 列記号（A, B, C...）
    col_map = {v: k for k, v in headers.items()}

    def get(row_dict, col_name):
        """行 dict から列名で値を取得する。"""
        col = col_map[col_name]
        for cell_ref, value in row_dict.items():
            if cell_ref.startswith(col):
                return value.strip()
        return ""

    # --- レコード生成 ---
    records: list[GlyphRecord] = []

    for row_dict in rows[1:]:
        glyph_name = get(row_dict, COL_MJ_NAME)
        if glyph_name == "":
            continue

        # --- b: 字母のUCS符号位置 ---
        jimo_ucs_raw = get(row_dict, COL_JIMO_UCS)
        b = to_uplus_string(jimo_ucs_raw)

        ok, reason = validate_uplus_input(b)
        if not ok:
            raise ValueError(f"Invalid 字母UCS for {glyph_name}: {reason}")

        # --- v: UCS符号位置（変体仮名自身） ---
        ucs_raw = get(row_dict, COL_UCS)

        if ucs_raw == "":
            # UCS未割り当て → 廃止・統合された変体仮名
            v = None
            active = False
        else:
            v = to_uplus_string(ucs_raw)
            ok, reason = validate_uplus_input(v)
            if not ok:
                raise ValueError(f"Invalid UCS for {glyph_name}: {reason}")
            active = True

        # --- コメント構築 ---
        jimo  = get(row_dict, COL_JIMO)
        onka1 = get(row_dict, COL_ONKA1)
        onka2 = get(row_dict, COL_ONKA2)
        onka3 = get(row_dict, COL_ONKA3)
        note  = get(row_dict, COL_NOTE)

        comment_parts = [
            jimo,
            onka1 if onka1 else "",
            onka2 if onka2 else "",
            onka3 if onka3 else "",
            note if note else "",
        ]

        comment = sanitize_comment(" ".join([p for p in comment_parts if p]))

        rec = GlyphRecord(
            name=glyph_name,
            b=b,
            v=v,
            active=active,
            comment=comment,
        )

        records.append(rec)

    return records
