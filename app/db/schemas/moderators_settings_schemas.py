from typing import Optional

from pydantic import BaseModel


class ModeratorSettingsBase(BaseModel):
    moderator_id: int
    player_is_new: Optional[int] = None
    exclude_servers: Optional[list[str]] = None
    exclude_reasons: Optional[list[str]] = None


class CreateModeratorSettings(ModeratorSettingsBase):
    pass


class UpdateModeratorSettings(CreateModeratorSettings):
    pass


class ModeratorSettings(ModeratorSettingsBase):
    id: int

    class Config:
        orm_mode = True
