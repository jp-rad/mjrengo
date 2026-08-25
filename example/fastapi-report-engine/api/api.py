# code/example/fastapi-report-engine/api/api.py

from fastapi import APIRouter
from .endpoints import komainu

api_router = APIRouter()
api_router.include_router(komainu.router)
