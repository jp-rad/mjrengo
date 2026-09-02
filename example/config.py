# code/example/config.py

from functools import lru_cache
from pydantic_settings import BaseSettings
# from rptgen1.uno_client_config import UnoClientConfig


class Settings(BaseSettings):
    app_name: str = "Example FastAPI"
    app_host: str = "0.0.0.0"
    app_port: int = 8002

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
