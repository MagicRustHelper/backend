import os

if not os.getenv('PROD'):
    from dotenv import load_dotenv

    load_dotenv('.env.dev')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router

app = FastAPI(title='MagicHelper API')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router)
