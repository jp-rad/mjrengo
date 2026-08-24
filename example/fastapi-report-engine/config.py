# code/example/fastapi-report-engine/config.py

from functools import lru_cache
from pydantic_settings import BaseSettings
from rptgen1.uno_client_config import UnoClientConfig


class Settings(BaseSettings):
    app_name: str = "Report Engine"
    app_host: str = "0.0.0.0"
    app_port: int = 8002
    unoserver_host: str = "unoserver"  # "127.0.0.1"
    unoserver_port: str = "2003"
    unoserver_location: str = "auto"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_uno_client_config():
    settings = get_settings()
    return UnoClientConfig(
        server=settings.unoserver_host,
        port=settings.unoserver_port,
        host_location=settings.unoserver_location,
    )
