# tests/test_get_resource.py

import types
import sys
import pytest

from mjrengo.resource import get_resource, normalize_version, ResourceError


# ----------------------------------------------------------------------
# Helpers: create fake modules dynamically for testing
# ----------------------------------------------------------------------

def create_fake_module(fullname, packages, version, glyph_table):
    """
    Create a fake module in sys.modules for testing.
    fullname: module name like "mjrengo.data.mj.v6_02_201"
    """
    mod = types.ModuleType(fullname)
    mod.PACKAGES = packages
    mod.VERSION = version
    mod.GLYPH_TABLE = glyph_table
    sys.modules[fullname] = mod
    return mod


# ----------------------------------------------------------------------
# normalize_version tests
# ----------------------------------------------------------------------

def test_normalize_version_basic():
    assert normalize_version("6.02.201") == "v6_02_201"
    assert normalize_version("6.02.201h") == "v6_02_201h"
    assert normalize_version("6.02.201-h1") == "v6_02_201_h1"
    assert normalize_version("6.02.201_h2") == "v6_02_201_h2"
    assert normalize_version("4.10.0") == "v4_10_0"
    assert normalize_version("1.20.a") == "v1_20_a"
    assert normalize_version("1.20.a-2") == "v1_20_a_2"


# ----------------------------------------------------------------------
# get_resource tests
# ----------------------------------------------------------------------

def test_get_resource_success_default_base():
    """
    Test loading a module under the default base namespace "mjrengo.data".
    """

    glyph_set = "mj"
    version_external = "6.02.201"
    version_internal = "v6_02_201"

    fullname = f"mjrengo.data.{glyph_set}.{version_internal}"

    fake_packages = ["dummy"]
    fake_version = version_external
    fake_table = {"MJ000001": {"b": "U+3005"}}

    create_fake_module(fullname, fake_packages, fake_version, fake_table)

    res = get_resource(glyph_set, version_external)

    assert res["PACKAGES"] == fake_packages
    assert res["VERSION"] == fake_version
    assert res["GLYPH_TABLE"] == fake_table


def test_get_resource_success_custom_base():
    """
    Test loading a module under a custom base namespace.
    """

    base = "myproject.datasets"
    glyph_set = "mj_plus"
    version_external = "4.10.0"
    version_internal = "v4_10_0"

    fullname = f"{base}.{glyph_set}.{version_internal}"

    fake_packages = ["dummy2"]
    fake_version = version_external
    fake_table = {"MJPLUS0001": {"b": "U+4E00"}}

    create_fake_module(fullname, fake_packages, fake_version, fake_table)

    res = get_resource(glyph_set, version_external, base=base)

    assert res["PACKAGES"] == fake_packages
    assert res["VERSION"] == fake_version
    assert res["GLYPH_TABLE"] == fake_table


def test_get_resource_missing_module():
    """
    Test that missing modules raise ResourceError.
    """

    glyph_set = "unknown"
    version_external = "1.00.0"

    with pytest.raises(ResourceError):
        get_resource(glyph_set, version_external)


def test_get_resource_missing_symbols():
    """
    Test that modules missing required symbols raise ResourceError.
    """

    glyph_set = "mj"
    version_external = "6.02.201"
    version_internal = "v6_02_201"

    fullname = f"mjrengo.data.{glyph_set}.{version_internal}"

    # Create module missing GLYPH_TABLE
    mod = types.ModuleType(fullname)
    mod.PACKAGES = ["dummy"]
    mod.VERSION = version_external
    sys.modules[fullname] = mod

    with pytest.raises(ResourceError):
        get_resource(glyph_set, version_external)
