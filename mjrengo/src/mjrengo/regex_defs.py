import re

# ============================================================
# Regex Definitions (External Module)
# ============================================================

TAG_PATTERN = re.compile(
    r'(?<!\\)(?<!\{)\{(?P<glyph>[A-Za-z0-9]+)'
    r'(?:\s+b=(?P<b>(?:U\+[0-9A-Fa-f]{4,6}(?:\s+U\+[0-9A-Fa-f]{4,6})*)))?'
    r'(?:\s+v=(?P<v>(?:U\+[0-9A-Fa-f]{4,6}(?:\s+U\+[0-9A-Fa-f]{4,6})*)))?'
    r'(?:\s+set=(?P<set>[A-Za-z0-9_+\-]+))?'
    r'\}'
)

RE_ESC_BACKSLASH = re.compile(r'\\\\')   # \\ → \
RE_ESC_LBRACE   = re.compile(r'\\\{')    # \{ → {
