from typing import Optional

from pydantic import BaseModel, Field, root_validator


DEFAULT_STEAM_AVATAR = 'https://avatars.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg'


class PlayerStats(BaseModel):
    steamid: str | None = None
    kills: int = Field(0, alias='kp_total')
    kills_arrow = Field(0, alias='kp_arrow')
    kills_shot = Field(0, alias='kp_shot')
    kills_melee = Field(0, alias='kp_melee')
    death: int = Field(0, alias='d_player')
    headshot: int = Field(0, alias='kp_head')
    kd: float
    nickname: str = Field(None, alias='name')
    avatar: str = Field(DEFAULT_STEAM_AVATAR)

    @root_validator(pre=True)
    def get_kd(cls, values: dict) -> dict:
        if values.get('d_player') == 0:
            values['kd'] = values.get('kp_total', 0)
        else:
            values['kd'] = round(values.get('kp_total', 0) / values.get('d_player', 1), 1)
        return values


class Player(BaseModel):
    steamid: str = Field(..., alias='id')
    ip: str
    nickname: str
    server_number: int = Field(..., alias='server')
    first_join: int = Field(..., alias='firstjoin')
    vk: Optional[int] = None
    stats: Optional[PlayerStats] = None


class BanInfo(BaseModel):
    ban_id: int = Field(0, alias='banID')
    nickname: str
    steamid: str
    reason: str
    time: int


class ReportMessage(BaseModel):
    author_nickname: str
    report_steamid: str
    server_number: int


class ReportShow(BaseModel):
    steamid: str
    report_count: int
    is_player_new: bool = False
    is_player_online: bool = False
