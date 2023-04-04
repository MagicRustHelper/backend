from typing import Optional

from pydantic import BaseModel


class ModeratorBase(BaseModel):
    name: str
    steamid: int | str
    vk_id: int | str
    avatar_url: Optional[str] = None
    is_superuser: bool = False
    is_bot: bool = False


class CreateModerator(ModeratorBase):
    pass


class UpdateModerator(ModeratorBase):
    name: Optional[str] = None
    steamid: Optional[int] = None
    vk_id: Optional[int] = None
    is_superuser: bool = None
    is_bot: bool = None


class Moderator(ModeratorBase):
    id: int

    class Config:
        orm_mode = True
