from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import CRUDBase
from app.db.models import Moderator
from app.db.schemas import CreateModerator, UpdateModerator


class CRUDModerator(CRUDBase[Moderator, CreateModerator, UpdateModerator]):
    async def get_moder_by_vk(self, session: AsyncSession, vk_id: int) -> Moderator:
        statement = select(self.model).where(self.model.vk_id == vk_id)
        return await session.scalar(statement)


moderator = CRUDModerator(Moderator)
