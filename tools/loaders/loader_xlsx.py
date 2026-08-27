# tools/loaders/loader_mji00602_xlsx.py

import pandas as pd
from pathlib import Path
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


def load_mji00602_xlsx(path: Path) -> dict[str, GlyphRecord]:
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
