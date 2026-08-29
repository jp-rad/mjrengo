# tools/loaders/loader_mji_00602_xlsx.py

from __future__ import annotations
from pathlib import Path
import zipfile

from tools.loaders.xlsx_strict_ooxml_loader import (
    find_first_sheet_filename,
    load_sheet_rows,
    parse_header,
)

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
COL_BASE     = "対応するUCS"
COL_VARIANT  = "実装したMoji_JohoコレクションIVS"
COL_FONT     = "font"
COL_NOTE     = "備考"

REQUIRED_COLUMNS = {
    COL_MJ_NAME,
    COL_BASE,
    COL_VARIANT,
    COL_FONT,
    COL_NOTE,
}

def load_mji_00602_xlsx(path: Path) -> list[GlyphRecord]:
    """
    mji.00602.xlsx 専用 Strict OOXML ローダー。

    - Strict OOXML の workbook.xml / sheet XML を基盤モジュールで処理
    - 列名はヘッダー行から復元
    - Moji_Joho コレクション IVS を variant として扱う
    - base が空の場合は active=False とする
    """

    with zipfile.ZipFile(path, "r") as z:
        # --- Strict OOXML: 1枚目のシートを特定 ---
        sheet_filename = find_first_sheet_filename(z)

        # --- 行データ抽出（セル参照 A1/B1/C1... を保持） ---
        rows = load_sheet_rows(z, sheet_filename)

        # --- ヘッダー解析（列記号 → 列名） ---
        headers = parse_header(rows)

    # --- 必須列チェック ---
    if not REQUIRED_COLUMNS.issubset(headers.values()):
        missing = REQUIRED_COLUMNS - set(headers.values())
        raise ValueError(f"Missing required columns in XLSX: {missing}")

    # 列名 → 列記号（A, B, C...）
    col_map = {v: k for k, v in headers.items()}

    def get(row_dict, col_name):
        """
        行 dict から列名で値を取得する。
        A列なら A1/A2/A3... のように cell_ref.startswith(col) で判定。
        """
        col = col_map[col_name]
        for cell_ref, value in row_dict.items():
            if cell_ref.startswith(col):
                return value.strip()
        return ""

    # --- レコード生成 ---
    records: list[GlyphRecord] = []

    for row_dict in rows[1:]:
        comments = []

        glyph_name = get(row_dict, COL_MJ_NAME)
        if glyph_name == "":
            continue

        # font="実装なし" → active=False
        font_value = get(row_dict, COL_FONT)
        active = font_value != "実装なし"
        if not active:
            comments.append(font_value)

        # --- base（REP） ---
        base_raw = get(row_dict, COL_BASE)
        base = to_uplus_string(base_raw)

        if base:
            ok, reason = validate_uplus_input(base)
            if not ok:
                raise ValueError(f"Invalid base for {glyph_name}: {reason}")

            comments.append(decode_ucs(base))

            # --- variant（Moji_Joho コレクション IVS） ---
            variant_raw = get(row_dict, COL_VARIANT)
            if variant_raw == "":
                variant = base
            else:
                if ";" in variant_raw:
                    comments.append(variant_raw)

                variant = pick_ucs_by_rep(variant_raw, base)

                ok, reason = validate_uplus_input(variant)
                if not ok:
                    raise ValueError(f"Invalid variant for {glyph_name}: {reason}")

        else:
            base = None
            variant = None

        rec = GlyphRecord(
            name=glyph_name,
            b=base,
            v=variant,
            active=active,
            comment=sanitize_comment(" ".join(comments)),
        )

        records.append(rec)

    return records
