from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CheckBase(BaseModel):
    steamid: str
    moderator_id: int
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    server_number: int
    is_ban: bool = False


class CreateCheck(CheckBase):
    pass


class UpdateCheck(CheckBase):
    steamid: Optional[str] = None
    moderator_id: Optional[int] = None
    start: Optional[datetime] = None
    server_number: Optional[int] = None
    is_ban: Optional[bool] = None


class Check(CheckBase):
    id: int

    class Config:
        orm_mode = True
