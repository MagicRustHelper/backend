from datetime import datetime

from sqlalchemy import distinct, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import CRUDBase
from app.db.models import Check
from app.db.schemas import CreateCheck, UpdateCheck


class CRUDCheck(CRUDBase[Check, CreateCheck, UpdateCheck]):
    async def complete_check(self, session: AsyncSession, check_id: int, is_ban: bool = False) -> Check:
        check = await self.get(session, check_id)
        check.end = datetime.now().timestamp()
        check.is_ban = is_ban
        await session.commit()
        return check

    async def cancel_check(self, session: AsyncSession, check_id: int) -> Check:
        return await self.remove(session, id=check_id)

    async def get_checked_players(self, session: AsyncSession, steamids: list[str]) -> dict[str, int]:
        statement = select(distinct(self.model.steamid), self.model.start).filter(self.model.steamid.in_(steamids))
        result = await session.execute(statement)
        result = {steamid: start for steamid, start in result.all()}
        return result


check = CRUDCheck(Check)
