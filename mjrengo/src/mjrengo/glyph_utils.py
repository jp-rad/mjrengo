ESC_LB = "{_ESC_LB_}"      # 正規化フェーズ用内部トークン（"{{" の一時退避）
TAG_LB = "{_LB_}"          # ユーザー用リテラル "{"


def escape_left_brace(text: str) -> str:
    """
    Normalization phase:
    "{{" → {_ESC_LB_}
    """
    return (text or "").replace("{{", ESC_LB)


def unescape_left_brace(text: str) -> str:
    """
    Normalization phase:
    {_ESC_LB_} → "{{"
    """
    return (text or "").replace(ESC_LB, "{{")


def render_escape_left_brace(text: str) -> str:
    """
    Render phase:
    "{{" → {_LB_}
    """
    return (text or "").replace("{{", TAG_LB)


def render_unescape_left_brace(text: str) -> str:
    """
    Render phase:
    {_LB_} → "{"
    """
    return (text or "").replace(TAG_LB, "{")
