Module mjrengo.src.mjrengo.glyph_utils
======================================

Functions
---------

`escape_left_brace(text: str) ‑> str`
:   Normalization phase:
    "{{" → {_ESC_LB_}

`render_escape_left_brace(text: str) ‑> str`
:   Render phase:
    "{{" → {_LB_}

`render_unescape_left_brace(text: str) ‑> str`
:   Render phase:
    {_LB_} → "{"

`unescape_left_brace(text: str) ‑> str`
:   Normalization phase:
    {_ESC_LB_} → "{{"