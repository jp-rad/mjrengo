# mjrengo

mjrengo is a toolkit for UCS and IVS normalization and unified glyph‑data integration.  
It provides a consistent interface for loading, normalizing, and merging glyph datasets used in MJ and GJ workflows.  
All dataset modules are distributed as independent Python packages under the `mjrengo.data.*` namespace.

Repository:  
https://github.com/jp-rad/mjrengo

## Features

- Deterministic UCS and IVS normalization
- Unified glyph table compiled from multiple authoritative datasets
- Loader for DWPI Mincho attribute dictionary
- Versioned data modules for reproducible builds
- PEP 420 namespace package layout

## Namespace Package Layout

The project uses PEP 420 namespace packages.  
Each dataset module provides its own `GLYPH_TABLE`, `VERSION`, and `PACKAGES` definitions.

```
mjrengo/
    engine/
    normalize/
    replace/
    data/
        mj/
            v6_02_201/
                contains GLYPH_TABLE
            v6_02_201h/
                contains GLYPH_TABLE
        mj_plus/
            v4_10/
                contains GLYPH_TABLE
        mj_plusx/
            v1_20/
                contains GLYPH_TABLE
        template/
            v0_1_0/
                contains GLYPH_TABLE
```

Each subdirectory under `mjrengo.data.*` represents an independently versioned dataset module.  
Each module exposes a glyph table through its `GLYPH_TABLE` symbol.

## Installation

Install the latest version directly from GitHub:

```
pip3 install --upgrade \
    mjrengo@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=mjrengo \
    mjrengo-data-mj_plus-v4_10@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=glyph/mj_plus-v4_10 \
    mjrengo-data-mj_plusx-v1_20@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=glyph/mj_plusx-v1_20 \
    mjrengo-data-mj-v6_02_201@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=glyph/mj-v6_02_201 \
    mjrengo-data-mj-v6_02_201h@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=glyph/mj-v6_02_201h
```

## Check Installed Version

```
pip3 list | grep mjrengo
```

## Uninstallation

Remove all mjrengo packages:

```
pip3 uninstall -y mjrengo \
    mjrengo-data-mj_plus-v4_10 \
    mjrengo-data-mj_plusx-v1_20 \
    mjrengo-data-mj-v6_02_201 \
    mjrengo-data-mj-v6_02_201h
```

## Usage Example

### Load a glyph record

```
from mjrengo import get_resource

glyphs = get_resource("mj_plus", version="4_10")

rec = glyphs["MJ000001"]
print(rec.b, rec.v, rec.active)
```

### Normalize UCS / IVS

```
from mjrengo.normalize import normalize_ucs

ucs = "U+FA0E"
base = normalize_ucs(ucs)
print(base)
```

### Example: normalize_tags test

```
set_name = "test"

def test_normalize_success():
    fn = make_replace_fn(glyph_table, set_name)
    engine = GlyphTagEngine(fn)

    result = engine.normalize_tags("{MJ000001}")
    assert result.success is True
    assert result.errors == []
    assert result.text == "{MJ000001 b=U+3005 v=U+3005 set=test}"
```

## Data Sources

This project uses dataset materials published on the following official pages:

- IPA MJ List  
  https://moji.or.jp/mojikiban/mjlist/

- Digital Wide Area DWPI Mincho  
  https://www.digitalwidearea.org/dwpi_mincho

All dataset materials are used solely as source data for generating unified glyph tables.  
All copyrights remain with their respective publishers.

## License

Released under the MIT License.  
All datasets retain their original copyright notices.

## Notes

- Each dataset module provides its own GLYPH_TABLE.
- Data modules are versioned independently.
- The core engine does not embed any dataset.
- Namespace packages allow multiple datasets to coexist without conflicts.
```
