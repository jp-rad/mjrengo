Module mjrengo.src.mjrengo.ucs
==============================

Functions
---------

`decode_ucs(seq: str) ‑> str`
:   Decode a UCS codepoint sequence into a Unicode string.
    Supports BMP + Supplementary Plane + IVS.

`encode_ucs(char: str) ‑> str`
:   Encode a Unicode string (including IVS) into a UCSSeq.