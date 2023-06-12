from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_bot, get_current_moder, get_session
from app.db import crud, models, schemas

router = APIRouter(tags=['Checks'])


@router.post('', response_model=models.Check)
async def create_check(
    check_create: schemas.CreateCheck,
    *,
    session: AsyncSession = Depends(get_session),
    bot: models.Moderator = Depends(get_current_bot)
) -> models.Check:
    moderator = await crud.moderator.get_moder_by_vk(session, check_create.moderator_vk_id)
    check_create.moderator_id = moderator.id
    return await crud.check.create(session, obj_in=check_create)


@router.put('/{check_id}', response_model=models.Check)
async def complete_check(
    check_id: int,
    is_ban: bool = False,
    *,
    session: AsyncSession = Depends(get_session),
    bot: models.Moderator = Depends(get_current_bot)
) -> models.Check:
    return await crud.check.complete_check(session, check_id, is_ban)


@router.delete('/{check_id}', response_model=models.Check)
async def cancel_check(
    check_id: int, *, session: AsyncSession = Depends(get_session), bot: models.Moderator = Depends(get_current_bot)
) -> models.Check:
    return await crud.check.cancel_check(session, check_id)


@router.post('/get_checked', response_model=dict[str, int])
async def get_checked_players(
    steamids: list[str],
    *,
    session: AsyncSession = Depends(get_session),
    moderator: models.Moderator = Depends(get_current_moder)
) -> dict[str, int]:
    return await crud.check.get_checked_players(session, steamids)


@router.get('/steamid/{steamid}', response_model=models.Check | dict)
async def get_last_player_check(
    steamid: str,
    *,
    session: AsyncSession = Depends(get_session),
    moderator: models.Moderator = Depends(get_current_moder)
) -> models.Check | dict:
    last_check = await crud.check.get_player_last_check(session, steamid)
    return last_check if last_check else {}


@router.get('/moderators_count', response_model=list[schemas.ModeratorsCheckCount])
async def get_moderators_count_checks(
    time_start: float,
    time_end: float,
    *,
    session: AsyncSession = Depends(get_session),
    moderator: models.Moderator = Depends(get_current_moder)
) -> list[schemas.ModeratorsCheckCount]:
    return await crud.check.get_moderators_count_checks(session, time_start, time_end)


@router.get('/length', response_model=list[schemas.ModeratorsChecksLength])
async def get_moderators_checks_length(
    time_start: float,
    time_end: float,
    *,
    session: AsyncSession = Depends(get_session),
    moderator: models.Moderator = Depends(get_current_moder)
) -> list[schemas.ModeratorsChecksLength]:
    return await crud.check.get_moderator_length_checks(session, time_start, time_end)
