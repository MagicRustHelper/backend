from typing import Optional

from pydantic import BaseModel


class ModeratorSettingsBase(BaseModel):
    moderator_id: Optional[int] = None
    player_is_new: Optional[int] = None
    exclude_servers: Optional[list[str]] = None
    include_reasons: Optional[list[str]] = None
    exclude_reasons: Optional[list[str]] = None


class CreateModeratorSettings(ModeratorSettingsBase):
    pass


class UpdateModeratorSettings(CreateModeratorSettings):
    pass


class ModeratorSettings(ModeratorSettingsBase):
    pass

    class Config:
        orm_mode = True
