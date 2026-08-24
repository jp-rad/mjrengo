# code/example/fastapi-report-engine/main.py

from fastapi import FastAPI
import uvicorn
from api import api
from config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)
app.include_router(api.api_router)


def serve():
    """Serve the web application."""
    uvicorn.run(app, port=settings.app_port, host=settings.app_host)


if __name__ == "__main__":
    serve()
