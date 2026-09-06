import pytest
from tofurengo.resource import get_resource


def test_mj_v6_02_201():
    glyph_set = "mj"
    version = "6.02.201"
    
    res = get_resource(glyph_set, version)
    assert res["VERSION"] == version
    assert res["LIBRARY_NAME"] == "tofurengo-data-mj-v6-02-201"


def test_mj_v6_02_201_onka():
    glyph_set = "mj"
    version = "6.02.201-onka"
    
    res = get_resource(glyph_set, version)
    assert res["VERSION"] == version
    assert res["LIBRARY_NAME"] == "tofurengo-data-mj-v6-02-201-onka"

def test_mj_plus_v4_10():
    glyph_set = "mj_plus"
    version = "4.10"

    res = get_resource(glyph_set, version)
    assert res["VERSION"] == version
    assert res["LIBRARY_NAME"] == "tofurengo-data-mj-plus-v4-10"

def test_mj_plusx_v1_20():
    glyph_set = "mj_plusx"
    version = "1.20"

    res = get_resource(glyph_set, version)
    assert res["VERSION"] == version
    assert res["LIBRARY_NAME"] == "tofurengo-data-mj-plusx-v1-20"

