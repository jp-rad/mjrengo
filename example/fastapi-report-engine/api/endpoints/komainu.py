# code/example/fastapi-report-engine/api/endpoints/komainu.py

from fastapi import APIRouter, File, UploadFile
from typing import List, Optional
from api.models.render_request import RenderRequest
from services.report_engine import generate_report

router = APIRouter()


@router.post("/komainu", summary="Report Engine")
def render(
    request: RenderRequest,
    template: UploadFile,
    medias: Optional[List[UploadFile]] = File(None),
):
    if not medias:
        medias = []
    return generate_report(request, template, medias)
