from fastapi import APIRouter, Depends, Response, status

from app import entities
from app.api.deps import get_current_moder, get_rcc_api, get_rcc_cache
from app.db.models import Moderator
from app.services.RCC import RustCheatCheckAPI
from app.services.RCC.rcc_cache import RCCPlayerCache

router = APIRouter(tags=['RCC'])


@router.get(
    '/player/{steamid}',
    response_model=entities.RCCPlayer,
)
async def get_rcc_player(
    steamid: str,
    *,
    rcc_api: RustCheatCheckAPI = Depends(get_rcc_api),
    moderator: Moderator = Depends(get_current_moder),  # noqa
) -> entities.RCCPlayer:
    return await rcc_api.get_rcc_player(steamid)


@router.post('/players', response_model=list[entities.RCCPlayer])
async def get_rcc_players(
    steamids: list[str],
    *,
    rcc_api: RustCheatCheckAPI = Depends(get_rcc_api),
    moderator: Moderator = Depends(get_current_moder),  # noqa
) -> list[entities.RCCPlayer]:
    return await rcc_api.get_rcc_players(steamids)


@router.post('/access', response_class=Response, status_code=204)
async def get_checker_access(
    steamid: str,
    moder_steamid: str | None = None,
    rcc_api: RustCheatCheckAPI = Depends(get_rcc_api),
    moderator: Moderator = Depends(get_current_moder),
) -> None:
    moder_steamid = moder_steamid or moderator.steamid
    response = await rcc_api.give_checker_access(steamid, moder_steamid)
    if response.status == entities.RCCResponseStatus.SUCCESS:
        return Response('Доступ выдан', status_code=status.HTTP_204_NO_CONTENT)
    return Response('Не удалоь выдать доступ', status_code=status.HTTP_403_FORBIDDEN)


@router.get('/cached', response_model=dict[int, entities.RCCPlayer])
async def get_all_cached_player(
    *,
    rcc_cache: RCCPlayerCache = Depends(get_rcc_cache),
    moderator: Moderator = Depends(get_current_moder),
) -> dict[int, entities.RCCPlayer]:
    return rcc_cache.get_all_cache()


@router.delete('/cached', response_class=Response, status_code=204)
async def clear_rcc_cache(
    *,
    rcc_cache: RCCPlayerCache = Depends(get_rcc_cache),
    moderator: Moderator = Depends(get_current_moder),
) -> None:
    rcc_cache.clear_cache()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
