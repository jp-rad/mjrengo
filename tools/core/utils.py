# tools/core/utils.py

def require_columns(df, required: set, source: str) -> None:
    """
    DataFrame に必要なカラムが揃っているか確認する。
    足りなければ ValueError。
    """
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in {source}: {missing}")
