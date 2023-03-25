from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CheckBase(BaseModel):
    steamid: int
    moderator_id: int
    start: datetime
    end: Optional[datetime] = None
    server_number: int
    is_ban: bool


class CreateCheck(CheckBase):
    pass


class UpdateCheck(CheckBase):
    steamid: Optional[int] = None
    moderator_id: Optional[int] = None
    start: Optional[datetime] = None
    server_number: Optional[int] = None
    is_ban: Optional[bool] = None


class Check(CheckBase):
    id: int

    class Config:
        orm_mode = True
