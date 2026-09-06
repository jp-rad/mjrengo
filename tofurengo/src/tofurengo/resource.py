"""
Dynamic dataset resource loader module for the tofurengo library.

This module provides mechanisms to dynamically import glyph data modules and datasets
based on glyph set names and external version string identifiers, resolving their
corresponding wheel distribution library names dynamically.
"""

import importlib
from importlib.metadata import packages_distributions
import re
from typing import Any, Dict

DEFAULT_BASE_NAMESPACE: str = "tofurengo_data"


class ResourceError(Exception):
    """Exception raised when a dataset module or required symbol cannot be loaded."""

    pass


def normalize_version(version: str) -> str:
    """
    Normalize an external version string into a valid Python module version identifier.

    Converts version strings separated by dots, hyphens, or underscores into a
    standardized `v<major>_<minor>_<revision>` format.

    Args:
        version (str): External version string (e.g., "6.02.201", "6.02.201-onka").

    Returns:
        str: Normalized internal version identifier starting with 'v' (e.g., "v6_02_201_onka").

    Examples:
        >>> normalize_version("6.02.201")
        'v6_02_201'
        >>> normalize_version("6.02.201-onka")
        'v6_02_201_onka'
    """
    clean_ver = version.strip()
    normalized = re.sub(r"[.\-]", "_", clean_ver)
    return f"v{normalized}"


def get_wheel_library_name(full_module_name: str) -> str:
    """
    Resolve the installed wheel (.whl) distribution package name for a specific full module path.

    Args:
        full_module_name (str): Full Python import module path
            (e.g., "tofurengo.data.mj.v6_02_201").

    Returns:
        str: Installed wheel distribution name (e.g., "tofurengo-mj-v6-02-201").
             Falls back to a normalized hyphenated representation if metadata lookup fails.
    """
    try:
        dist_map = packages_distributions()

        # Check full module path first, then parent namespaces
        parts = full_module_name.split(".")
        for i in range(len(parts), 0, -1):
            target_namespace = ".".join(parts[:i])
            distributions = dist_map.get(target_namespace)
            if distributions:
                return distributions[0]
    except Exception:
        pass

    # Fallback heuristic: convert module path dots and underscores to hyphens
    return full_module_name.replace(".", "-").replace("_", "-")


def get_resource(
    glyph_set: str,
    version: str,
    base: str = DEFAULT_BASE_NAMESPACE,
) -> Dict[str, Any]:
    """
    Dynamically load and retrieve dataset attributes from a glyph information module.

    Constructs the target module path dynamically using `<base>.<glyph_set>.<internal_version>`
    and verifies that required data symbols (`GLYPH_TABLE`, `VERSION`) exist.

    Args:
        glyph_set (str): Name of the glyph information system (e.g., "mj", "mj_plus", "mj_plusx").
        version (str): External version string following major.minor.revision conventions.
        base (str): Base module namespace. Defaults to "tofurengo_data".

    Returns:
        Dict[str, Any]: Dictionary containing exported module attributes:
            - `"GLYPH_TABLE"` (dict): Map of glyph identifiers to character properties.
            - `"VERSION"` (str): Module version string.
            - `"LIBRARY_NAME"` (str): Specific wheel (.whl) distribution package name housing the dataset.

    Raises:
        ResourceError: If the target module does not exist or lacks required symbols.

    Examples:
        >>> # 1. Standard MJ dataset
        >>> res_mj = get_resource("mj", "6.02.201")
        >>> res_mj["LIBRARY_NAME"]
        'tofurengo-mj-v6-02-201'

        >>> # 2. MJ dataset with revision suffix (-onka)
        >>> res_onka = get_resource("mj", "6.02.201-onka")
        >>> res_onka["LIBRARY_NAME"]
        'tofurengo-mj-v6-02-201-onka'

        >>> # 3. Extended MJ Plus dataset
        >>> res_plus = get_resource("mj_plus", "4.10")
        >>> res_plus["LIBRARY_NAME"]
        'tofurengo-mj-plus-v4-10'

        >>> # 4. Experimental MJ PlusX dataset
        >>> res_plusx = get_resource("mj_plusx", "1.20")
        >>> res_plusx["LIBRARY_NAME"]
        'tofurengo-mj-plusx-v1-20'
    """
    gs = glyph_set.strip()
    ver_norm = normalize_version(version)
    base_ns = base.strip()

    module_name = f"{base_ns}.{gs}.{ver_norm}"

    try:
        mod = importlib.import_module(module_name)
    except ModuleNotFoundError as err:
        raise ResourceError(f"Dataset module not found: '{module_name}'") from err

    required_symbols = ["GLYPH_TABLE", "VERSION"]
    missing_symbols = [sym for sym in required_symbols if not hasattr(mod, sym)]

    if missing_symbols:
        raise ResourceError(
            f"Dataset module '{module_name}' is missing required symbols: {missing_symbols}"
        )

    # Resolve specific wheel distribution package name dynamically
    library_name = get_wheel_library_name(mod.__name__)

    return {
        "GLYPH_TABLE": getattr(mod, "GLYPH_TABLE"),
        "VERSION": getattr(mod, "VERSION"),
        "LIBRARY_NAME": library_name,
    }

