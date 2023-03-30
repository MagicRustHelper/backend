import asyncio
import time
from typing import Any, Callable

from app.entities import BanInfo, Player, PlayerStats, ReportShow
from app.services.api_client import APIClient, ResponseModel
from app.services.magic_rust._urls import ModersMethods, SiteMethods, StatsMethods
from app.services.magic_rust.servers import SERVERS_ID


class MagicRustAPI:
    def __init__(self) -> None:
        self.api_client = APIClient()

    async def get_player_stats(self, steamid: int, server_number: int) -> PlayerStats:
        server_id = self._get_server_id(server_number)
        params = {'server': server_id, 'steamid': steamid}
        url = StatsMethods.PLAYER_STATS
        return await self.api_request(url, params=params, response_model=PlayerStats)

    async def get_server_players_stats(self, server_number: int) -> list[PlayerStats]:
        server_id = self._get_server_id(server_number)
        params = {'server': server_id}
        url = StatsMethods.SERVER_STATS
        return await self.api_request(url, params=params, response_model=PlayerStats)

    async def get_player_stats_by_player(self, player: Player) -> Player:
        player.stats = await self.get_player_stats(player.steamid, player.server_number)
        return player

    async def get_online_players(self) -> list[Player]:
        url = ModersMethods.PLAYERS_ONLINE
        return await self.api_request(url, response_model=Player)

    async def get_online_steamids(self) -> list[int]:
        online_players = await self.get_online_players()
        return [player.steamid for player in online_players]

    async def get_online_new_players(self, days: int = 7, stats: bool = False) -> list[Player]:
        players_online = await self.get_online_players()
        time_delta = time.time() - days * 84600
        new_players = list(filter(lambda player: player.first_join >= time_delta, players_online))
        if stats:
            return await self.fill_players_stats(players=new_players)
        return new_players

    async def fill_players_stats(self, players: list[Player]) -> list[Player]:
        return await self.api_requests(self.get_player_stats_by_player, players)

    async def get_banned_players(self) -> list[BanInfo]:
        url = SiteMethods.BAN_LIST
        return await self.api_request(url, response_model=BanInfo)

    async def get_banned_steamids(self) -> list[int]:
        all_bans = await self.get_banned_players()
        return [ban.steamid for ban in all_bans]

    async def is_steamid_banned(self, steamid: int) -> bool:
        banned_steamids = await self.get_banned_steamids()
        return steamid in banned_steamids

    async def mark_online_players(self, reports: list[ReportShow]) -> list[ReportShow]:
        online_steamids = await self.get_online_steamids()
        for report in reports:
            if report.steamid in online_steamids:
                report.is_player_online = True
        return reports

    async def api_request(self, url: str, response_model: ResponseModel, params: dict | None = None) -> ResponseModel:
        return await self.api_client.api_GET_request(url, query=params, response_model=response_model)

    async def api_requests(self, method: Callable[[Any], ResponseModel], args: list[Any]) -> list[ResponseModel]:
        tasks = []
        for arg in args:
            task = asyncio.ensure_future(method(arg))
            tasks.append(task)
        results = await asyncio.gather(*tasks, return_exceptions=False)
        return results

    def _get_server_id(self, server_number: int) -> int:
        return SERVERS_ID.get(server_number, 1655)
