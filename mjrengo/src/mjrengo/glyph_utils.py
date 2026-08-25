
TAG_LB = "{_LB_}"
ESCAPED_LB = "{_LB_ESCAPED_}"

def escape_left_brace(text: str) -> str:
    """Normalize phase: escape literal '{{'."""
    return (text or "").replace("{{", ESCAPED_LB)

def unescape_left_brace(text: str) -> str:
    """Normalize phase: restore escaped '{{'."""
    return (text or "").replace(ESCAPED_LB, "{{")

def protect_left_brace(text: str) -> str:
    """Render phase: protect '{{' from tag parsing."""
    return (text or "").replace("{{", TAG_LB)

def restore_left_brace(text: str) -> str:
    """Render phase: restore '{' after rendering."""
    return (text or "").replace(TAG_LB, "{")
