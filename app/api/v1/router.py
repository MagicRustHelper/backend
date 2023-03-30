from fastapi import APIRouter

from app.api.v1 import auth_endpoint, magic_endpoint, profile_endpoint, rcc_endpoint, steam_endpoint

api_router = APIRouter(prefix='/v1')
api_router.include_router(rcc_endpoint.router, prefix='/rcc')
api_router.include_router(auth_endpoint.router, prefix='/auth')
api_router.include_router(magic_endpoint.router, prefix='/magic')
api_router.include_router(steam_endpoint.router, prefix='/steam')
api_router.include_router(profile_endpoint.router, prefix='/profile')