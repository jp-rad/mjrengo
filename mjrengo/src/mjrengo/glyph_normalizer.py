from typing import List, Optional

from mjrengo.types import GlyphError, GlyphResult, ReplaceFn
from mjrengo.glyph_utils import GlyphUtils


class GlyphNormalizer:
    """
    ステートレスな正規化クラス。
    タグ解析および置換の実装詳細は replace_fn コールバックへ委任する。

    `replace_fn` はコンストラクタでの事前設定、または `normalize()` 実行時の動的指定の両方に対応。
    """

    def __init__(self, replace_fn: Optional[ReplaceFn] = None):
        """
        :param replace_fn: デフォルトで利用する ReplaceFn（任意）
        """
        self.replace_fn = replace_fn

    def normalize(
        self, 
        text: str, 
        replace_fn: Optional[ReplaceFn] = None
    ) -> GlyphResult:
        """
        正規化メイン処理

        :param text: 対象テキスト
        :param replace_fn: 今回の呼び出しで一時的に利用（または上書き）する ReplaceFn（任意）
        """
        if not text:
            return GlyphResult(success=True, text="", errors=[])

        # 優先順位: 引数の replace_fn > インスタンスの self.replace_fn
        fn = replace_fn or self.replace_fn
        if fn is None:
            raise ValueError("replace_fn is required in __init__ or normalize()")

        errors: List[GlyphError] = []

        # GlyphUtils.process_pipeline で「退避 -> 置換 -> {{ }} 復元」を一括実行
        normalized_text = GlyphUtils.process_pipeline(
            text=text,
            replacer=lambda m: fn(m, errors),
            unescape=False,  # normalize 用: {{ }} のエスケープ表記を保持
        )

        return GlyphResult(
            success=len(errors) == 0,
            text=normalized_text,
            errors=errors,
        )
