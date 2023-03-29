from fastapi import APIRouter, Depends, Response, status
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
        steamid=moderator.steamid,
        vk_id=moderator.vk_id,
    )


@router.get('/settings', response_model=schemas.ModeratorSettings)
async def get_moderator_settings(
    *, session: AsyncSession = Depends(get_session), moderator: models.Moderator = Depends(get_current_moder)
) -> schemas.ModeratorSettings:
    moderator_settings = await crud.moderator_settings.get(session, moderator.id)
    return schemas.ModeratorSettings(
        moderator_id=moderator_settings.moderator_id,
        player_is_new=moderator_settings.player_is_new,
        include_reasons=moderator_settings.include_reasons,
        exclude_reasons=moderator_settings.exclude_reasons,
        exclude_servers=moderator_settings.exclude_servers,
    )


@router.put('/settings', response_class=Response, status_code=204)
async def update_moderator_settings(
    moderator_settings: schemas.ModeratorSettings,
    *,
    session: AsyncSession = Depends(get_session),
    moderator: models.Moderator = Depends(get_current_moder)
) -> None:
    await crud.moderator_settings.update_by_id(
        session,
        moderator.id,
        schemas.UpdateModeratorSettings(
            player_is_new=moderator_settings.player_is_new,
            exclude_servers=moderator_settings.exclude_servers,
            include_reasons=moderator_settings.include_reasons,
            exclude_reasons=moderator_settings.exclude_reasons,
        ),
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
