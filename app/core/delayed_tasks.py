import asyncio
from datetime import datetime

from loguru import logger

from app.core import settings
from app.core.time_assistant import time_assistant
from app.services.magic_rust import MagicRustAPI
from app.services.RCC import RustCheatCheckAPI
from app.services.RCC.rcc_cache import rcc_cache


class CheckJoinedPlayersOnServer:
    SECONDS_TO_CHECK_JOINED_PLAYERS = 10 * 60

    def __init__(self) -> None:
        self._previous_check_players_online: set[int] | None = None
        self._mr_api = MagicRustAPI()
        self._rcc_api = RustCheatCheckAPI()

    async def __call__(self) -> None:
        while True:
            await self._check_joined_players()
            await asyncio.sleep(self.SECONDS_TO_CHECK_JOINED_PLAYERS)

    async def _check_joined_players(self) -> None:
        logger.info('Checks joined players')
        online_players_steamid = await self._mr_api.get_online_steamids()
        joined_players = self._get_joined_players(online_players_steamid)
        self._set_new_joined_players(joined_players)
        await self._rcc_api.get_rcc_players(joined_players)  # only for cache

    def _get_joined_players(self, online_players_steamids: list[int]) -> list[int]:
        if self._previous_check_players_online is None:
            return online_players_steamids

        joined_players = [
            steamid for steamid in online_players_steamids if steamid not in self._previous_check_players_online
        ]
        return joined_players

    def _set_new_joined_players(self, joined_players: list[int]) -> None:
        self._previous_check_players_online = set(joined_players)


class ClearRCCCacheEveryWipe:
    def __init__(self) -> None:
        self._rcc_cache = rcc_cache

    async def __call__(self) -> None:
        while True:
            await asyncio.sleep(self._seconds_to_next_wipe())
            self._rcc_cache.clear_cache()

    def _seconds_to_next_wipe(self) -> int:
        next_wipe = time_assistant.get_next_wipe_day()
        print(next_wipe)
        time_now = datetime.now(tz=settings.TIMEZONE)
        print(time_now)
        seconds_to_next_wipe = (next_wipe - time_now).total_seconds()
        logger.info(f'Seconds to next wipe {seconds_to_next_wipe}')
        return seconds_to_next_wipe


def run_delayed_tasks() -> None:
    for task in delayed_tasks:
        asyncio.ensure_future(task())


delayed_tasks = [ClearRCCCacheEveryWipe(), CheckJoinedPlayersOnServer()]
