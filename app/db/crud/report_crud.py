from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud import CRUDBase
from app.db.models import Report
from app.db.schemas import CreateReport, UpdateReport


class CRUDReport(CRUDBase[Report, CreateReport, UpdateReport]):
    async def by_unique_author_and_steamid_and_time(self, session: AsyncSession, time_start: datetime) -> list[int]:
        query = (
            select(self.model.report_steamid)
            .where(self.model.time >= time_start)
            .group_by(self.model.report_steamid, self.model.author_nickname)
        )
        result = await session.scalars(query)
        return result.all()

    async def get_report_count_by_steamid(self, session: AsyncSession, steamid: int, time_start: datetime) -> int:
        query = select(func.count(func.distinct(self.model.author_nickname, self.model.report_steamid))).where(
            self.model.report_steamid == steamid, self.model.time >= time_start
        )
        result = await session.scalars(query)
        return result.first()


report = CRUDReport(Report)
