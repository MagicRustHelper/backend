from fastapi import APIRouter, Depends

from app import entities
from app.api.deps import get_current_moder, get_rcc_api
from app.db.models import Moderator
from app.services.RCC import RustCheatCheckAPI

router = APIRouter(tags=['RCC'])


@router.get(
    '/player/{steamid}',
    response_model=entities.RCCPlayer,
)
async def get_rcc_player(
    steamid: int,
    *,
    rcc_api: RustCheatCheckAPI = Depends(get_rcc_api),
    moderator: Moderator = Depends(get_current_moder)  # noqa
) -> entities.RCCPlayer:
    return await rcc_api.get_rcc_player(steamid)


@router.post('/players', response_model=list[entities.RCCPlayer])
async def get_rcc_players(
    steamids: list[int],
    *,
    rcc_api: RustCheatCheckAPI = Depends(get_rcc_api),
    moderator: Moderator = Depends(get_current_moder)  # noqa
) -> list[entities.RCCPlayer]:
    return await rcc_api.get_rcc_players(steamids)
