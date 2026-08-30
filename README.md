# mjrengo

https://github.com/jp-rad/mjrengo

# Installation

## Install from Remote Repository

To install the latest version directly from GitHub, run:

```bash

pip3 install --upgrade \
    mjrengo@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=mjrengo \
    mjrengo-data-mj_plus-v4_10@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=glyph/mj_plus-v4_10 \
    mjrengo-data-mj_plusx-v1_20@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=glyph/mj_plusx-v1_20 \
    mjrengo-data-mj-v6_02_201@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=glyph/mj-v6_02_201 \
    mjrengo-data-mj-v6_02_201h@git+https://github.com/jp-rad/mjrengo.git@main#subdirectory=glyph/mj-v6_02_201h


```

## Installed version

```bash

pip3 list | grep mjrengo

```

## Uninstall

To uninstall all, run:

```bash

pip3 uninstall -y mjrengo \
    mjrengo-data-mj_plus-v4_10 \
    mjrengo-data-mj_plusx-v1_20 \
    mjrengo-data-mj-v6_02_201 \
    mjrengo-data-mj-v6_02_201h

```
