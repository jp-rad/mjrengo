Module mjrengo.src.mjrengo.engine
=================================

Functions
---------

`make_replace_fn(glyph_table: Dict[str, Dict[str, Any]], set_name: str) ‑> mjrengo.src.mjrengo.engine.ReplaceFn`
:   v0.5.8 Normalization Rules:
    
    - glyph-name を環境の glyph_table で解決
    - b/v を環境固有の UCSSeq に置き換える
    - set は必ず環境の set_name に強制置換する
    - active=false の場合は正規化しない

Classes
-------

`GlyphError(code: str, message: str, params: Dict[str, Any] = <factory>)`
:   GlyphError(code: str, message: str, params: Dict[str, Any] = <factory>)

    ### Instance variables

    `code: str`
    :   The type of the None singleton.

    `message: str`
    :   The type of the None singleton.

    `params: Dict[str, Any]`
    :   The type of the None singleton.

    ### Methods

    `to_dict(self) ‑> Dict[str, Any]`
    :

`GlyphResult(success: bool, text: str, errors: List[mjrengo.src.mjrengo.engine.GlyphError] = <factory>)`
:   GlyphResult(success: bool, text: str, errors: List[mjrengo.src.mjrengo.engine.GlyphError] = <factory>)

    ### Instance variables

    `errors: List[mjrengo.src.mjrengo.engine.GlyphError]`
    :   The type of the None singleton.

    `success: bool`
    :   The type of the None singleton.

    `text: str`
    :   The type of the None singleton.

    ### Methods

    `to_dict(self) ‑> Dict[str, Any]`
    :

`GlyphTagEngine(replace_fn: mjrengo.src.mjrengo.engine.ReplaceFn)`
:   Stateless glyph tag processor.
    Tag semantics are fully delegated to replace_fn.
    
    Syntax (v0.5.8):
    
        {<glyph-name> [b=<UCSSeq>] [v=<UCSSeq>] [set=<Identifier>]}

    ### Class variables

    `TAG_PATTERN`
    :   The type of the None singleton.

    ### Methods

    `normalize_tags(self, text: str) ‑> mjrengo.src.mjrengo.engine.GlyphResult`
    :   Normalization (v0.5.8):
        
        - "{{" → {_ESC_LB_}
        - TAG_PATTERN により b/v/set を正規化
        - {_ESC_LB_} → "{{"}
        - {_LB_} はそのまま残す

    `render_text(self, text: str, use_base: bool = False, tofu: str = 'U+25A1') ‑> str`
    :   Rendering Rules (v0.5.9):
        
        mode="v"       → v → b → tofu
        mode="b"       → b → tofu
        
        - use_base=True  → mode="b"
        - use_base=False → mode="v"

`ReplaceFn(*args, **kwargs)`
:   Base class for protocol classes.
    
    Protocol classes are defined as::
    
        class Proto(Protocol):
            def meth(self) -> int:
                ...
    
    Such classes are primarily used with static type checkers that recognize
    structural subtyping (static duck-typing).
    
    For example::
    
        class C:
            def meth(self) -> int:
                return 0
    
        def func(x: Proto) -> int:
            return x.meth()
    
        func(C())  # Passes static type check
    
    See PEP 544 for details. Protocol classes decorated with
    @typing.runtime_checkable act as simple-minded runtime protocols that check
    only the presence of given attributes, ignoring their type signatures.
    Protocol classes can be generic, they are defined as::
    
        class GenProto[T](Protocol):
            def meth(self) -> T:
                ...

    ### Ancestors (in MRO)

    * typing.Protocol
    * typing.Generic