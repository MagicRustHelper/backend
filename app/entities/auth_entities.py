import time

from pydantic import BaseModel, Field

from app.core import settings


def get_exp_time() -> int:
    return time.time() + 60 * 60 * 24 * settings.TOKEN_LIVE_DAYS


class TokenPayload(BaseModel):
    db_id: int
    exp: int = Field(default_factory=get_exp_time)


class VKAuthResponse(BaseModel):
    access_token: str
    expires_in: int
    user_id: int


class AuthData(BaseModel):
    token: str
    avatar_url: str = Field(alias='avatarUrl')


class CreateModerator(BaseModel):
    steamid: str | int
    vk_id: str | int = Field(alias='vkId')
