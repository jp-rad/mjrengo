# code/example/fastapi-report-engine/report_engine.py

from typing import List, Optional
from fastapi import UploadFile
from fastapi.responses import FileResponse
from rptgen1.report_generator import create_report_generator
from starlette.background import BackgroundTask
from api.models.render_request import RenderRequest
from config import get_uno_client_config


def generate_report(
    request: RenderRequest,
    template: UploadFile,
    medias: Optional[List[UploadFile]],
):

    def validate_mime_type(mime_type: str, is_disabled: bool = False):
        if is_disabled:
            return mime_type
        if mime_type == "application/vnd.oasis.opendocument.text":
            # Set media_type to 'application/octet-stream' to ensure the file is downloaded as binary data.
            mime_type = "application/octet-stream"
        return mime_type

    def get_type():
        ret = request.type
        if request.type == "auto":
            if template.filename.endswith(".docx"):
                ret = "docx"
            elif template.filename.endswith(".odt"):
                ret = "odt"
            elif template.filename.endswith(".png.cha"):
                ret = "relatorio"
            elif template.filename.endswith(".svg.cha"):
                ret = "relatorio"
            elif template.filename.endswith(".tex"):
                ret = "relatorio"
        return ret

    generator = create_report_generator(
        type=get_type(),
        file_basename=request.file_basename,
        convert_to_pdf=request.convert_to_pdf,
        pdf_filter_options=request.pdf_filter_options,
        uno_client_config=get_uno_client_config(),
    )
    try:
        generator.save_template_file(template.file, template.filename)
        medias = medias or []
        for f in medias:
            generator.save_media_file(f.file, f.filename)
        rendered = generator.render(request.context)
        return FileResponse(
            path=rendered.file_path,
            media_type=validate_mime_type(rendered.mime_type),
            filename=rendered.filename,
            background=BackgroundTask(generator.cleanup_working_directories),
        )
    except Exception as e:
        generator.cleanup_working_directories()
        raise e
