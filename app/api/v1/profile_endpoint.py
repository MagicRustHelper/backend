from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_moder, get_session
from app.db import crud, models, schemas

router = APIRouter(tags=['Profile'])


@router.get('/data', response_model=schemas.Moderator)
async def get_profile_data(*, moderator: models.Moderator = Depends(get_current_moder)) -> schemas.Moderator:
    return schemas.Moderator(
        id=moderator.id,
        name=moderator.name,
        avatar_url=moderator.avatar_url,
        is_bot=moderator.is_bot,
        is_superuser=moderator.is_superuser,
        steamid=moderator.steamid,
        vk_id=moderator.vk_id,
    )


@router.get('/settings', response_model=schemas.ModeratorSettings)
async def get_moderator_settings(
    *, session: AsyncSession = Depends(get_session), moderator: models.Moderator = Depends(get_current_moder)
) -> schemas.ModeratorSettings:
    moderator_settings = await crud.moderator_settings.get(session, moderator.id)
    return schemas.ModeratorSettings(
        id=moderator_settings.moderator_id,
        player_is_new=moderator_settings.player_is_new,
        exclude_reasons=moderator_settings.exclude_reasons,
        exclude_servers=moderator_settings.exclude_servers,
    )
