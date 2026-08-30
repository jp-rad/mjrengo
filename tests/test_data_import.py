import pytest
from mjrengo.data.mj.v6_02_201 import PACKAGES as mj_v6_02_201_pkg, VERSION as mj_v6_02_201_ver, GLYPH_TABLE as mj_v6_02_201_dic
from mjrengo.data.mj.v6_02_201_onka import PACKAGES as mj_v6_02_201_onka_pkg, VERSION as mj_v6_02_201_onka_ver, GLYPH_TABLE as mj_v6_02_201_onka_dic
from mjrengo.data.mj_plus.v4_10 import PACKAGES as mj_plus_v410_pkg, VERSION as mj_plus_v410_ver, GLYPH_TABLE as mj_plus_v410_dic
from mjrengo.data.mj_plusx.v1_20 import PACKAGES as mj_plus_ex_v120_pkg, VERSION as mj_plus_ex_v120_ver, GLYPH_TABLE as mj_plus_ex_v120_dic

from mjrengo.resource import get_resource


def test_mj_v6_02_201():
    # mj, ver: 6.02.201
    glyph_set = "mj"
    version_external = "6.02.201"
    packages = "mjrengo-data-mj-v6_02_201"
    assert mj_v6_02_201_pkg == packages
    assert mj_v6_02_201_ver == version_external

    res = get_resource(glyph_set, version_external)
    assert res["PACKAGES"] == packages
    assert res["VERSION"] == version_external


def test_mj_v6_02_201_onka():
    # mj, ver: 6.02.201h
    glyph_set = "mj"
    version_external = "6.02.201-onka"
    packages = "mjrengo-data-mj-v6_02_201_onka"
    assert mj_v6_02_201_onka_pkg == packages
    assert mj_v6_02_201_onka_ver == version_external

    res = get_resource(glyph_set, version_external)
    assert res["PACKAGES"] == packages
    assert res["VERSION"] == version_external

def test_mj_plus_v4_10():
    # mj_plus, ver: 4.10
    glyph_set = "mj_plus"
    version_external = "4.10"
    packages = "mjrengo-data-mj_plus-v4_10"
    assert mj_plus_v410_pkg == packages
    assert mj_plus_v410_ver == version_external

    res = get_resource(glyph_set, version_external)
    assert res["PACKAGES"] == packages
    assert res["VERSION"] == version_external

def test_mj_plusx_v1_20():
    # mj_plusx, ver: 1.20
    glyph_set = "mj_plusx"
    version_external = "1.20"
    packages = "mjrengo-data-mj_plusx-v1_20"
    assert mj_plus_ex_v120_pkg == packages
    assert mj_plus_ex_v120_ver == version_external

    res = get_resource(glyph_set, version_external)
    assert res["PACKAGES"] == packages
    assert res["VERSION"] == version_external
