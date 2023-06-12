from typing import Optional

from pydantic import BaseModel, Field

from app.db.schemas.utils import get_now_time


class CheckBase(BaseModel):
    steamid: str
    moderator_id: int
    start: Optional[int] = Field(default_factory=get_now_time)
    end: Optional[int] = Field(default_factory=get_now_time)
    server_number: int
    is_ban: bool = False


class CreateCheck(CheckBase):
    moderator_id: int | None = None
    moderator_vk_id: int


class UpdateCheck(CheckBase):
    steamid: Optional[str] = None
    moderator_id: Optional[int] = None
    start: Optional[int] = None
    server_number: Optional[int] = None
    is_ban: Optional[bool] = None


class ModeratorsCheckCount(BaseModel):
    moderator_id: int
    count: int
    name: str


class ModeratorsChecksLength(BaseModel):
    name: str
    total_length: float = 0


class Check(CheckBase):
    id: int

    class Config:
        orm_mode = True
