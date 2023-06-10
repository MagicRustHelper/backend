from collections import Counter
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import entities
from app.api.deps import get_current_moder, get_session
from app.db import crud, models, schemas
from app.db.models import Moderator

router = APIRouter(tags=['Reports'])


@router.post('', response_model=models.Report)
async def create_report(
    report_create: schemas.CreateReport,
    *,
    session: AsyncSession = Depends(get_session),
    moderator: Moderator = Depends(get_current_moder)
) -> models.Report:
    return await crud.report.create(session, obj_in=report_create)


@router.get('/{time_start}', response_model=dict[str, int])
async def get_all_reports_by_time(
    time_start: int, *, session: AsyncSession = Depends(get_session), moderator: Moderator = Depends(get_current_moder)
) -> dict[str, int]:
    time_start = datetime.fromtimestamp(time_start)
    steamids = await crud.report.by_unique_author_and_steamid_and_time(session, time_start)
    steamids = Counter(steamids)
    return dict(steamids)


@router.get('/{steamid}/{time_start}', response_model=entities.ReportCount)
async def get_report_count_by_steamid(
    steamid: str,
    time_start: int,
    *,
    session: AsyncSession = Depends(get_session),
    moderator: Moderator = Depends(get_current_moder)
) -> entities.ReportCount:
    time_start = datetime.fromtimestamp(time_start)
    count = await crud.report.get_report_count_by_steamid(session, steamid, time_start)
    return entities.ReportCount(steamid=steamid, count=count)
