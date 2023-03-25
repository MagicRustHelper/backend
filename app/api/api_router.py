from fastapi import APIRouter

from app.api.v1.router import api_router as router_v1

api_router = APIRouter()
api_router.include_router(router_v1)
