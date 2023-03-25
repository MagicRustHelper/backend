import secrets
from typing import Any, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    MAGIC_STATS_API_LINK: str
    MAGIC_MODERS_API_LINK: str

    ALGORITHM: str = 'HS256'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    TOKEN_LIVE_DAYS = 30

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            port=values.get('POSTGRES_PORT'),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    VK_CLIENT_ID: int
    VK_CLIENT_SECRET: str
    VK_REDIRECT_URI: str

    OWNER_VK_ID: int
    OWNER_VK_NAME: str
    OWNER_STEAMID: int

    RCC_KEY: str

    STEAM_KEY: str


settings = Settings()
