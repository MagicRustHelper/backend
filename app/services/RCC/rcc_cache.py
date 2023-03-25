from typing import TYPE_CHECKING, Callable, ParamSpec, TypeVar

from loguru import logger

from app.entities import RCCPlayer

if TYPE_CHECKING:
    from app.services.RCC import RustCheatCheckAPI

P = ParamSpec('P')
RT = TypeVar('RT')
DecoratedFunc = Callable[P, RT]


class RCCPlayerCache:
    def __init__(self) -> None:
        self.players: dict[int, RCCPlayer] = {}

    async def get_cached_player_or_request(
        self, get_rcc_player: Callable[[int], RCCPlayer], rcc_api: 'RustCheatCheckAPI', steamid: int
    ) -> RCCPlayer:
        player = self.players.get(steamid)
        if not player:
            logger.debug(f'{steamid} not in cache. Request....')
            player = await get_rcc_player(rcc_api, steamid)
            self.add_cache(steamid, player)
        else:
            logger.debug(f'Get data from cache {player}')
        return player

    def add_cache(self, steamid: int, player: RCCPlayer) -> None:
        self.players.update({steamid: player})
        logger.debug(f'Add to cache {steamid}:{player}')

    def clear_cache(self) -> None:
        self.players.clear()

    def get_all_cache(self) -> dict[int, RCCPlayer]:
        return self.players


rcc_cache = RCCPlayerCache()


def rcc_player_cache(get_rcc_player: Callable[P, RT]) -> Callable[P, RT]:
    async def wrapper(*args, **kwargs) -> RT:
        player = await rcc_cache.get_cached_player_or_request(get_rcc_player, *args, **kwargs)
        return player

    return wrapper
