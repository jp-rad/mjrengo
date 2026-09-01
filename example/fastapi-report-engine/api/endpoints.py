from fastapi import APIRouter
from api.models.mjrengo_request import MjrengoRequest
from .services import (
    normalize_service,
    render_service,
    convert_service,
)

endpoints_router = APIRouter()

@endpoints_router.post("/normalize/{engine}")
def normalize(engine: str, payload: MjrengoRequest):
    return normalize_service(engine, payload)

@endpoints_router.post("/render/{engine}")
def render(engine: str, payload: MjrengoRequest):
    return render_service(engine, payload)

@endpoints_router.get("/convert/{engine}")
def convert(engine: str, text: str, use_base: bool = True):
    return convert_service(engine, text, use_base)
