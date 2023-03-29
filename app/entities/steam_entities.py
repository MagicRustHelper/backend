from pydantic import BaseModel, Field


class SteamAvatarResponse(BaseModel):
    avatar_url: str = Field(..., alias='avatarUrl')
    avatar_full_url: str = Field(..., alias=('avatarFullUrl'))


class SteamUser(BaseModel):
    steamid: str
    avatarmedium: str
    avatarfull: str
    timecreated: int | None = None


class SteamPlayerResponse(BaseModel):
    players: list[SteamUser]


class SteamBaseResponse(BaseModel):
    response: SteamPlayerResponse
