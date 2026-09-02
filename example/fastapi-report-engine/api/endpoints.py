from fastapi import APIRouter
from api.models.mjrengo_request import MjrengoRequest
from .services import (
    normalize_service,
    render_service,
    convert_service,
)

endpoints_router = APIRouter()

# GET convert (unchanged)
@endpoints_router.get("/convert/{engine}/{text:path}")
def convert(engine: str, text: str):
    return convert_service(engine, text)

# POST normalize (use glyph_set instead of engine)
@endpoints_router.post("/normalize")
def normalize(payload: MjrengoRequest):
    return normalize_service(payload.glyph_set, payload.text)

# POST render (use glyph_set instead of engine)
@endpoints_router.post("/render")
def render(payload: MjrengoRequest):
    return render_service(payload.glyph_set, payload.text)
