import asyncio
from typing import Any, Callable, TypeVar

from app.core import settings, utils
from app.entities import RCCBaseResponse, RCCPlayer
from app.services.api_client import APIClient
from app.services.RCC.rcc_cache import rcc_player_cache

RCCAPIResponse = TypeVar('RCCAPIResponse', bound=RCCBaseResponse)
T = TypeVar('T')


class RustCheatCheckAPI:
    API_URL = 'https://rustcheatcheck.ru/panel'
    API_KEY = settings.RCC_KEY

    def __init__(self) -> None:
        self.api_client = APIClient(base_url=self.API_URL)
        self.api_key: dict[str, str] = {'key': self.API_KEY}

    @rcc_player_cache
    async def get_rcc_player(self, steamid: str) -> RCCPlayer:
        params = {'player': steamid}
        rcc_player = await self.api_request('getInfo', params, RCCPlayer)
        return rcc_player

    async def get_rcc_players(self, steamids: list[str]) -> list[RCCPlayer]:
        response = []
        for steamid in steamids:
            try:
                rcc_player = await self.get_rcc_player(steamid)
            except Exception:
                continue
            else:
                response.append(rcc_player)
            finally:
                await asyncio.sleep(0.15)
        return response

    async def give_checker_access(self, player_steamid: str, moder_stemaid: str = 0) -> RCCBaseResponse:
        params = {
            'player': player_steamid,
            'moder': moder_stemaid,
        }
        response = await self.api_request('addPlayer', params, RCCBaseResponse)
        return response

    async def api_request(self, api_action: str, params: dict, response_model: T) -> T:
        params |= self.api_key | {'action': api_action}
        response = await self.api_client.api_GET_request('/api', query=params, response_model=response_model)
        return response

    async def api_requests(self, method: Callable[[Any], RCCAPIResponse], args: list[Any]) -> list[RCCAPIResponse]:
        tasks = []
        for arg in args:
            task = asyncio.ensure_future(method(arg))
            tasks.append(task)
        results = await asyncio.gather(*tasks, return_exceptions=False)
        return results
