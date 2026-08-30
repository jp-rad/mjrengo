# tests/test_builder.py

import types
import sys
import pytest

from mjrengo.builder import build_engine
from mjrengo.resource import ResourceError


def create_fake_module(fullname, glyph_table, version, packages):
    mod = types.ModuleType(fullname)
    mod.GLYPH_TABLE = glyph_table
    mod.VERSION = version
    mod.PACKAGES = packages
    sys.modules[fullname] = mod
    return mod


def test_build_engine_default_set_name():
    """
    set_name=None → glyph_set が使われることを確認する
    """

    glyph_set = "template"
    version_external = "0.1.0"
    version_internal = "v0_1_0"

    fullname = f"mjrengo.data.{glyph_set}.{version_internal}"

    glyph_table = {"MJ000001": {"b": "U+3005", "v": "U+3005"}}
    packages = ["dummy"]
    version = version_external

    create_fake_module(fullname, glyph_table, version, packages)

    engine = build_engine(glyph_set, version_external)

    result = engine.normalize_tags("{MJ000001}")
    assert result.success is True
    assert "set=template" in result.text


def test_build_engine_custom_set_name():
    """
    set_name を明示指定した場合
    """

    glyph_set = "template"
    version_external = "0.1.0"
    version_internal = "v0_1_0"

    fullname = f"mjrengo.data.{glyph_set}.{version_internal}"

    glyph_table = {"MJ000001": {"b": "U+3005", "v": "U+3005"}}
    packages = ["dummy"]
    version = version_external

    create_fake_module(fullname, glyph_table, version, packages)

    engine = build_engine(glyph_set, version_external, set_name="test")

    result = engine.normalize_tags("{MJ000001}")
    assert result.success is True
    assert "set=test" in result.text


def test_build_engine_missing_module():
    """
    モジュールが存在しない場合は ResourceError
    """

    with pytest.raises(ResourceError):
        build_engine("unknown", "1.00.0")
