from typing import TypeAlias

from fastapi import APIRouter, Depends

from app import entities
from app.api.deps import get_current_moder, get_mr_api, get_steam_friends_api
from app.db.models import Moderator
from app.services.magic_rust import MagicRustAPI
from app.services.steam.steam_friends import SteamFriends

steamid: TypeAlias = int
router = APIRouter(tags=['MagicRust'])


@router.get('/players/online', response_model=list[entities.Player])
async def get_online_players(
    stats: bool = False,
    *,
    mr_api: MagicRustAPI = Depends(get_mr_api),
    moderator: Moderator = Depends(get_current_moder),
) -> list[entities.Player]:
    return await mr_api.get_online_players(stats=stats)


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
    moderator: Moderator = Depends(get_current_moder),
) -> list[entities.Player]:
    return await mr_api.get_online_new_players(days=days, stats=stats)


@router.get('/server/{server_number}/stats/{steamid}', response_model=entities.PlayerStats)
async def get_player_stats(
    server_number: int,
    steamid: int,
    *,
    mr_api: MagicRustAPI = Depends(get_mr_api),
    moderator: Moderator = Depends(get_current_moder),
) -> entities.PlayerStats:
    return await mr_api.get_player_stats(server_number=server_number, steamid=steamid)


@router.post('/players/fill-stats', response_model=list[entities.Player])
async def fill_players_stats(
    players: list[entities.Player],
    *,
    mr_api: MagicRustAPI = Depends(get_mr_api),
    moderator: Moderator = Depends(get_current_moder),
) -> entities.Player:
    return await mr_api.fill_players_stats(players)


@router.get('/players/banned', response_model=list[entities.BanInfo])
async def get_banned_players(
    *, mr_api: MagicRustAPI = Depends(get_mr_api), moderator: Moderator = Depends(get_current_moder)
) -> list[entities.BanInfo]:
    return await mr_api.get_banned_players()


@router.get('/server/{server_number}/players/friendship')
async def get_players_friendship(
    server_number: int,
    *,
    mr_api: MagicRustAPI = Depends(get_mr_api),
    steamid_friends: SteamFriends = Depends(get_steam_friends_api),
    moderator: Moderator = Depends(get_current_moder),
) -> list[list[str]]:
    online_players = await mr_api.get_online_players_by_server(server_number)
    online_steamids = [str(player.steamid) for player in online_players]
    return await steamid_friends.find_parties(online_steamids, online_steamids.copy())
