from typing import TypeAlias

from fastapi import APIRouter, Depends

from app import entities
from app.api.deps import get_current_moder, get_mr_api
from app.db.models import Moderator
from app.services.magic_rust import MagicRustAPI

steamid: TypeAlias = int
router = APIRouter(tags=['MagicRust'])


@router.get('/players/online', response_model=list[entities.Player])
async def get_online_players(
    mr_api: MagicRustAPI = Depends(get_mr_api), moderator: Moderator = Depends(get_current_moder)
) -> list[entities.Player]:
    return await mr_api.get_online_players()


@router.get('/players/online/dict', response_model=dict[steamid, entities.Player])
async def get_online_players_dict(
    mr_api: MagicRustAPI = Depends(get_mr_api), moderator: Moderator = Depends(get_current_moder)
) -> dict[steamid, entities.Player]:
    players = await mr_api.get_online_players()
    return {player.steamid: player for player in players}


@router.get('/players/online/new', response_model=list[entities.Player])
async def get_online_new_player(
    days: int = 7,
    stats: bool = False,
    *,
    mr_api: MagicRustAPI = Depends(get_mr_api),
    moderator: Moderator = Depends(get_current_moder)
) -> list[entities.Player]:
    return await mr_api.get_online_new_players(days=days, stats=stats)


@router.get('/server/{server_number}/stats/{steamid}', response_model=entities.PlayerStats)
async def get_player_stats(
    server_number: int,
    steamid: int,
    *,
    mr_api: MagicRustAPI = Depends(get_mr_api),
    moderator: Moderator = Depends(get_current_moder)
) -> entities.PlayerStats:
    return await mr_api.get_player_stats(server_number=server_number, steamid=steamid)
