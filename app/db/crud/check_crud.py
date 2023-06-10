from datetime import datetime

from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import CRUDBase
from app.db.models import Check, Moderator
from app.db.schemas import CreateCheck, ModeratorsCheck, UpdateCheck


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

    async def get_player_last_check(self, session: AsyncSession, steamid: str) -> Check | None:
        statement = select(self.model).filter(self.model.steamid == steamid).order_by(self.model.id.desc())
        result = await session.execute(statement)
        result = result.first()
        return result[0] if result else None

    async def get_moderators_count_checks(
        self, session: AsyncSession, time_start: float, time_end: float
    ) -> list[ModeratorsCheck]:
        statement = (
            select(func.count(self.model.id), self.model.moderator_id, Moderator.name)
            .join(Moderator, self.model.moderator_id == Moderator.id)
            .filter(self.model.start > time_start, self.model.end < time_end)
            .group_by(self.model.moderator_id, Moderator.name)
        )
        result = await session.execute(statement)
        result = result.all()
        return [ModeratorsCheck(count, moderator_id, name) for count, moderator_id, name in result]


check = CRUDCheck(Check)
