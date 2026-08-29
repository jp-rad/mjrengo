import pytest
from mjrengo.data.mj.v6_02_201 import PACKAGES as mj_v6_02_201_pkg, VERSION as mj_v6_02_201_ver, GLYPH_TABLE as mj_v6_02_201_dic
from mjrengo.data.mj_plus.v4_10 import PACKAGES as mj_plus_v410_pkg, VERSION as mj_plus_v410_ver, GLYPH_TABLE as mj_plus_v410_dic
from mjrengo.data.mj_plusx.v1_20 import PACKAGES as mj_plus_ex_v120_pkg, VERSION as mj_plus_ex_v120_ver, GLYPH_TABLE as mj_plus_ex_v120_dic

def test_mj():
    assert mj_v6_02_201_pkg == "mjrengo-data-mj-v6_02_201"
    assert mj_v6_02_201_ver == "6.02.201"

def test_mj_plus():
    assert mj_plus_v410_pkg == "mjrengo-data-mj-plus-v4_10"
    assert mj_plus_v410_ver == "4.10"

def test_mj_plus_ex():
    assert mj_plus_ex_v120_pkg == "mjrengo-data-mj-plusx-v1_20"
    assert mj_plus_ex_v120_ver == "1.20"
