# tools/loaders/loader_mdb.py

from pathlib import Path
from pyaccess import AccessDatabase

from ..core.model import GlyphRecord
from ..core.normalize import (
    to_uplus_string,
    validate_uplus_input,
    sanitize_comment,
)


def load_mdb(path: Path, table_name: str, active_flag: bool) -> dict[str, GlyphRecord]:
    """
    MDB を読み込み、GlyphRecord の dict を返す。
    key = glyph_name
    """

    db = AccessDatabase(path)
    df = db.query(f"SELECT * FROM {table_name}")

    records: dict[str, GlyphRecord] = {}

    required = {"glyph_name", "ucs", "rep"}
    if not required.issubset(df.columns):
        missing = required - set(df.columns)
        raise ValueError(f"Missing required columns in MDB table {table_name}: {missing}")

    for _, row in df.iterrows():
        glyph_name = str(row["glyph_name"]).strip()

        # --- UCS 変換 ---
        ucs_raw = str(row["ucs"]).strip()
        ucs = to_uplus_string(ucs_raw)

        ok, reason = validate_uplus_input(ucs)
        if not ok:
            raise ValueError(f"Invalid UCS for {glyph_name}: {reason}")

        # --- REP 変換 ---
        rep_raw = str(row["rep"]).strip()
        rep = to_uplus_string(rep_raw)

        ok, reason = validate_uplus_input(rep)
        if not ok:
            raise ValueError(f"Invalid REP for {glyph_name}: {reason}")

        # --- active ---
        active = active_flag

        # --- comment（MDB に comment がある場合のみ） ---
        comment_raw = str(row.get("comment", "")).strip()
        comment = sanitize_comment(comment_raw)

        rec = GlyphRecord(
            name=glyph_name,
            v=ucs,
            b=rep,
            active=active,
            comment=comment,
        )

        records[glyph_name] = rec

    return records
