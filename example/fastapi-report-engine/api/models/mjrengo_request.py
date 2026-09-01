from pydantic import Field
from ._json_base_model import JsonBaseModel

class MjrengoRequest(JsonBaseModel):
    text: str = Field(default="")
    use_base: bool = Field(default=True)
