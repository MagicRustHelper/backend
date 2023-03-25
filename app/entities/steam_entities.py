from pydantic import BaseModel, Field


class SteamAvatarResponse(BaseModel):
    avatar_url: str = Field(..., alias='avatarUrl')


class SteamUser(BaseModel):
    steamid: str
    avatarmedium: str
    timecreated: int | None = None


class SteamPlayerResponse(BaseModel):
    players: list[SteamUser]


class SteamBaseResponse(BaseModel):
    response: SteamPlayerResponse
