from fastapi import APIRouter, Path
from api.models.mjrengo_request import MjrengoRequest, VALID_GLYPH_SETS
from .services import (
    normalize_service,
    render_service,
    convert_service,
)

endpoints_router = APIRouter()
from fastapi import Path

@endpoints_router.get("/convert/{glyph_set}/{text:path}")
def convert(
    glyph_set: str = Path(
        ...,
        description="Glyph set to use.",
        enum=VALID_GLYPH_SETS
    ),
    text: str = Path(
        ...,
        description="Input text to process."
    )
):
    return convert_service(glyph_set, text)

# POST normalize (use glyph_set instead of engine)
@endpoints_router.post("/normalize")
def normalize(payload: MjrengoRequest):
    return normalize_service(payload.glyph_set, payload.text)

# POST render (use glyph_set instead of engine)
@endpoints_router.post("/render")
def render(payload: MjrengoRequest):
    return render_service(payload.glyph_set, payload.text)
