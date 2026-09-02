from pydantic import Field
from ._json_base_model import JsonBaseModel

VALID_GLYPH_SETS = ["mj-plus", "mj-plusx", "mj", "mj-onka", ]

class MjrengoRequest(JsonBaseModel):
    glyph_set: str = Field(
        default="mj-plus",
        description="Glyph set to use.",
        enum=VALID_GLYPH_SETS
    )
    text: str = Field(
        default="",
        description="Input text to process."
    )
