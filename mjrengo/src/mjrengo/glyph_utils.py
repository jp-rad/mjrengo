from email.mime import text
import re
from typing import Tuple, Dict, Callable

MARK_LB = "\u0002"  # {{ 用プレースホルダー
# MARK_RB = "\u0003"  # }} 用プレースホルダー
TAG_PATTERN = re.compile(
    r"\{"
    r"(?P<glyph>[^\s\}]+)"                  # 先頭のグリフ名 (必須)
    r"(?:(?=.*?\bb=(?P<b>[^\s\}]+))|)"      # b=値 (任意)
    r"(?:(?=.*?\bv=(?P<v>[^\s\}]+))|)"      # v=値 (任意)
    r"(?:(?=.*?\bset=(?P<set>[^\s\}]+))|)"  # set=値 (任意)
    r"[^\}]*"                               # その他の未定義属性を無視して閉じ括弧までスキップ
    r"\}",
    re.DOTALL
)


class GlyphUtils:
    """{{ }} によるエスケープ退避・復元およびタグパースを行うユーティリティ"""

    @staticmethod
    def escape_tokens(text: str) -> str:
        """{{ と }} を制御文字へ一時退避"""
        # return text.replace("{{", MARK_LB).replace("}}", MARK_RB)
        return text.replace("{{", MARK_LB)

    @staticmethod
    def restore_tokens_keep_escape(text: str) -> str:
        """normalize 用: プレースホルダーを {{ と }} (エスケープ表記) へ戻す"""
        # return text.replace(MARK_LB, "{{").replace(MARK_RB, "}}")
        return text.replace(MARK_LB, "{{")
    
    @staticmethod
    def restore_tokens_unescape(text: str) -> str:
        """render 用: プレースホルダーを { と } (単一波括弧) へ復元（アンエスケープ）"""
        # return text.replace(MARK_LB, "{").replace(MARK_RB, "}")
        return text.replace(MARK_LB, "{")
    
    @staticmethod
    def parse_tag_content(content: str) -> Tuple[str, Dict[str, str]]:
        """タグの中身から glyph_name と属性辞書を取得"""
        tokens = content.strip().split()
        if not tokens:
            return "", {}
        
        glyph_name = tokens[0]
        props = {}
        for token in tokens[1:]:
            if "=" in token:
                k, v = token.split("=", 1)
                props[k] = v
        return glyph_name, props

    @classmethod
    def process_pipeline(
        cls, 
        text: str, 
        replacer: Callable[[re.Match], str], 
        unescape: bool = True
    ) -> str:
        """
        退避 -> パース・置換 -> 復元のパイプラインを一括実行
        :param unescape: True の場合は { } へアンエスケープ (render), False の場合は {{ }} を保持 (normalize)
        """
        s = cls.escape_tokens(text)
        s = TAG_PATTERN.sub(replacer, s)
        if unescape:
            s = cls.restore_tokens_unescape(s)
        else:
            s = cls.restore_tokens_keep_escape(s)
        return s
    