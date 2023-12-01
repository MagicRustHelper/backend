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


@app.on_event('startup')
async def startup_event() -> None:
    from app.core.delayed_tasks import run_delayed_tasks

    run_delayed_tasks()
