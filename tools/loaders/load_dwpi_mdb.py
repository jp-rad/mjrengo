# tools/loaders/load_dwpi_mdb.py

from pathlib import Path
import subprocess
import csv

from mjrengo.ucs import decode_ucs, encode_ucs

from tools.core.model import GlyphRecord
from tools.core.normalize import (
    to_uplus_string,
    validate_uplus_input,
    pick_ucs_by_rep,
    sanitize_comment,
)


def load_dwpi_mdb(mdb_path: Path) -> list[GlyphRecord]:
    """
    DWPI 明朝 4.10版 V2.0.mdb の「文字属性辞書」テーブルを読み込み、
    list[GlyphRecord] に変換して返す。
    """

    records: list[GlyphRecord] = []

    # --- mdb-export を使って CSV を取得
    csv_text = subprocess.check_output(
        ["mdb-export", str(mdb_path), "文字属性辞書"],
        encoding="utf-8"
    )

    # --- CSV をパース
    reader = csv.DictReader(csv_text.splitlines())

    for row in reader:
        comments = []

        # --- name（必須）
        glyph_name = row["MJ文字図形名"].strip()

        # --- b / v の正規化（None → None）
        raw_b = row["代替文字コード"]
        if raw_b:
            comments.append(f"代替")
        else:
            raw_b = row["MS明朝コード"]
            if raw_b:
                comments.append("MS明朝")
            else:
                raw_b = row["異字体"]
                if raw_b:
                    raw_b = encode_ucs(raw_b)
                    comments.append("異字体")
                    
        b = to_uplus_string(raw_b) if raw_b else None
        if b:
            ok, reason = validate_uplus_input(b)
            if not ok:
                raise ValueError(f"Invalid base for {glyph_name}: {reason}")
        
        raw_v = row["DWPI明朝コード"]
        v = to_uplus_string(raw_v) if raw_v else None
        if v:
            ok, reason = validate_uplus_input(v)
            if not ok:
                raise ValueError(f"Invalid variant for {glyph_name}: {reason}")

        # --- active 判定
        active = v is not None

        if not active:
            comments.insert(0, "実装なし")
        if b:
            comments.insert(0, decode_ucs(b))

        rec = GlyphRecord(
            name=glyph_name,
            b=b,
            v=v,
            active=active,
            comment=sanitize_comment(" ".join(comments)),
        )
        records.append(rec)

    return records
