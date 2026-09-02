from pydantic import Field
from ._json_base_model import JsonBaseModel

class MjrengoRequest(JsonBaseModel):
    glyph_set: str = Field(default="mj-plus")
    text: str = Field(default="")
