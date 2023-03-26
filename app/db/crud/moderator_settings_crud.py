from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import CRUDBase
from app.db.models import ModeratorSettings
from app.db.schemas import CreateModeratorSettings, UpdateModeratorSettings


class CRUDModeratorSettings(CRUDBase[ModeratorSettings, CreateModeratorSettings, UpdateModeratorSettings]):
    async def update_by_id(
        self, session: AsyncSession, id: int, new_moderator_settings: UpdateModeratorSettings
    ) -> None:
        old_settings = await self.get(session, id)
        await self.update(session, db_obj=old_settings, obj_in=new_moderator_settings)


moderator_settings = CRUDModeratorSettings(ModeratorSettings)
