from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import CRUDBase
from app.db.models import Check
from app.db.schemas import CreateCheck, UpdateCheck


class CRUDCheck(CRUDBase[Check, CreateCheck, UpdateCheck]):
    async def complete_check(self, session: AsyncSession, check_id: int, is_ban: bool = False) -> Check:
        check = await self.get(session, check_id)
        check.end = datetime.now()
        check.is_ban = is_ban
        await session.commit()
        return check

    async def cancel_check(self, session: AsyncSession, check_id: int) -> Check:
        return await self.remove(session, id=check_id)


check = CRUDCheck(Check)
