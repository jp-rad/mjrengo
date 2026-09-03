# mjrengo

mjrengo is a toolkit that provides a unified “Glyph Tag abstraction layer”
for handling large-scale Japanese glyph systems such as MJ and MJ+,  
both widely used in Japanese government and public documents.

In Unicode, a single glyph may correspond to multiple UCS code point sequences (UCSSeq)
and multiple IVS (Variation Selectors).  
Furthermore, glyph numbering schemes and attribute systems differ across datasets,
making consistent management and exchange of glyph information essential.

## Features

- Abstract glyph specification using Glyph Tags  
  (glyph-name / UCSSeq / IVS handled in a unified format)

- Stable glyph management and exchange even in environments  
  that do not support IVS/VDS

- Provides datasets compatible with MJ and MJ+

## Namespace Package Layout

The project uses PEP 420 namespace packages.  
Each dataset module provides its own `GLYPH_TABLE`, `VERSION`, and `PACKAGES` definitions.

```
mjrengo/
    engine/
    normalize/
    replace/
    builder/
    data/
        mj/
            v6_02_201/
                contains GLYPH_TABLE
            v6_02_201_onka/
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

There are **two installation methods** available, depending on how you prefer to obtain the packages:

### **1. Install from GitHub Pages**  

This method uses a PEP 503–compatible simple index hosted on GitHub Pages.  
Pip downloads pre‑built wheel files, so installation is fast and does not require any build tools.  

```
pip3 install --upgrade --no-deps --index-url https://jp-rad.github.io/mjrengo/simple/ \
    mjrengo \
    mjrengo-data-mj-plus-v4-10 \
    mjrengo-data-mj-plusx-v1-20 \
    mjrengo-data-mj-v6-02-201-onka \
    mjrengo-data-mj-v6-02-201-onka
```

Use this when you want **simple installation**, **no build tools**, and **versioned wheels** directly from the project’s release pipeline.

---

### **2. Install directly from the Git repository**  
This method pulls the source code from GitHub and builds each package locally.  
It is useful when you want the **latest commit**, **development versions**, or when testing changes.

```
pip3 install --upgrade --no-deps \
    mjrengo@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=mjrengo \
    mjrengo-data-mj_plus-v4_10@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=glyph/mj_plus-v4_10 \
    mjrengo-data-mj_plusx-v1_20@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=glyph/mj_plusx-v1_20 \
    mjrengo-data-mj-v6_02_201@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=glyph/mj-v6_02_201 \
    mjrengo-data-mj-v6_02_201_onka@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=glyph/mj-v6_02_201_onka
```

Choose this when you need **development builds**, **source-level debugging**, or **custom modifications**.



## Check Installed Version

```
pip3 list | grep mjrengo
```



## Uninstallation

Remove all mjrengo packages:

```
pip3 uninstall -y \
    mjrengo \
    mjrengo-data-mj_plus-v4_10 \
    mjrengo-data-mj_plusx-v1_20 \
    mjrengo-data-mj-v6_02_201 \
    mjrengo-data-mj-v6_02_201_onka
```


## Usage Example

This example shows how to load MJ glyph datasets using `build_engine()`,
normalize MJ tags, and render final Unicode characters.

```
from mjrengo.builder import build_engine

# Input text containing MJ090001 tags
text = "'{MJ090001}'"

# ------------------------------------------------------------
# MJ glyph (source form) version 6.02.201
# ------------------------------------------------------------
engine = build_engine("mj", "6.02.201")  # set_name defaults to "mj"

norm = engine.normalize_tags(text)

# Output:
# '{MJ090001 b=U+5B89 v=U+1B002 set=mj}'
print(norm.text)

rendered = engine.render_text(norm.text, True)
# Output:
# '<Japanese Character (Kanji)>'
print(rendered)

# ------------------------------------------------------------
# MJ glyph (phonetic form) version 6.02.201-onka
# ------------------------------------------------------------
engine = build_engine("mj", "6.02.201-onka", "mj_hira")

norm = engine.normalize_tags(text)

# Output:
# '{MJ090001 b=U+3042 v=U+1B002 set=mj_hira}'
print(norm.text)

rendered = engine.render_text(norm.text, True)

# Output:
# '<Japanese Character (Hiragana)>'
print(rendered)

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
