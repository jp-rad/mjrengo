import re
from typing import Optional

from mjrengo.ucs import decode_ucs
from mjrengo.glyph_utils import GlyphUtils


class GlyphRenderer:
    """正規化済みタグを Unicode 文字へ変換・描画するエンジン"""

    def __init__(
        self,
        use_base: bool = False,
        tofu: str = "U+25A1",
    ):
        """
        :param use_base: デフォルトで基底文字(b)を優先するかどうか
        :param tofu: 該当文字がない場合の代替文字列 (デフォルト: "U+25A1")
        """
        self.use_base = use_base
        self.tofu = tofu

    def render(
        self,
        text: str,
        use_base: Optional[bool] = None,
        tofu: Optional[str] = None,
    ) -> str:
        """
        正規化済みテキストを描画（Unicode変換 & アンエスケープ）する

        :param text: 正規化済みテキスト
        :param use_base: 一時的に use_base 設定を上書き指定（任意）
        :param tofu: 一時的に tofu 設定を上書き指定（任意）
        :return: 描画完了テキスト
        """
        if not text:
            return ""

        # 引数が指定されていればそれを優先し、None ならインスタンスのデフォルト値を使用
        actual_use_base = self.use_base if use_base is None else use_base
        actual_tofu = self.tofu if tofu is None else tofu

        def _render_tag(m: re.Match) -> str:
            b = m.group("b")
            v = m.group("v")

            if actual_use_base:
                seq = b or actual_tofu
            else:
                seq = v or b or actual_tofu

            return decode_ucs(seq)

        # 描画時: エスケープ表記を解除する (unescape=True)
        return GlyphUtils.process_pipeline(text, _render_tag, unescape=True)