Module mjrengo.resource
=======================

Functions
---------

`get_resource(glyph_set: str, version: str, base: str = 'mjrengo.data') ‑> Dict[str, Any]`
:   Dynamically load a glyph information system module.
    
    Parameters
    ----------
    glyph_set : str
        Name of the glyph information system.
        This value is not restricted and may grow in the future.
        Examples:
            mj
            mj_plus
            mj_plusx
            template
            any_new_set
    
    version : str
        External version string.
        Must follow the major.minor.revision structure.
        Revision may contain '-' or '_'.
        Examples:
            6.02.201
            6.02.201-onka
            4.10
            1.20
    
        The version is internally normalized into:
            v<major>_<minor>_<revision>
    
    base : str
        Base namespace for dataset modules.
        Default: "mjrengo.data"
        May be replaced with any ASCII namespace:
            myproject.datasets
            example.glyph.data
    
    Module Path
    -----------
    The module path constructed is:
    
        <base>.<glyph_set>.<internal_version>
    
    Example:
        glyph_set = "mj"
        version   = "6.02.201-onka"
        base      = "mjrengo.data"
    
        internal_version = "v6_02_201_onka"
    
        module_name = "mjrengo.data.mj.v6_02_201_onka"
    
    Required Module Symbols
    -----------------------
    Each module must define:
    
        PACKAGES      (in __init__.py)
        VERSION       (in data_<glyph_set>_<internal_version>.py)
        GLYPH_TABLE   (in data_<glyph_set>_<internal_version>.py)
    
    Returns
    -------
    dict
        {
            "GLYPH_TABLE": <dict>,
            "VERSION": <str>,
            "PACKAGES": <any>
        }
    
    Raises
    ------
    ResourceError
        If the module does not exist or required symbols are missing.

`normalize_version(ver: str) ‑> str`
:   Normalize an external version string into an internal module identifier.
    
    External version rules:
        - ASCII only
        - Format: major.minor.revision
        - major, minor, revision are separated by dots (.)
        - revision may contain '-' or '_'
        - Examples:
            6.02.201
            6.02.201-onka
            4.10
            1.20
    
    Internal version rules:
        - Prefix 'v'
        - All separators inside revision ('-', '_') are normalized to '_'
        - All dots (.) are also normalized to '_' in the final identifier
        - Examples:
            6.02.201       -> v6_02_201
            6.02.201-onka  -> v6_02_201_onka
            4.10           -> v4_10
            1.20           -> v1_20

Classes
-------

`ResourceError(*args, **kwargs)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException