from pydantic import BaseModel, Field


class SteamAvatarResponse(BaseModel):
    avatar_url: str = Field(..., alias='avatarUrl')
    avatar_full_url: str = Field(..., alias=('avatarFullUrl'))


class SteamFriend(BaseModel):
    steamid: str
    relationship: str
    friend_since: int


class SteamFriends(BaseModel):
    friends: list[SteamFriend] = Field(default_factory=list)


class SteamFriendListResponse(BaseModel):
    friend_list: SteamFriends | None = Field(alias='friendslist', default=None)


class SteamUser(BaseModel):
    steamid: str
    avatarmedium: str
    avatarfull: str
    timecreated: int | None = None


class SteamPlayerResponse(BaseModel):
    players: list[SteamUser]


class SteamPlayerBaseResponse(BaseModel):
    response: SteamPlayerResponse
