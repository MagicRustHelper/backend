from functools import lru_cache

from httpx import codes

from app.core import settings
from app.entities import SteamFriend, SteamFriendListResponse, SteamPlayerBaseResponse, SteamUser
from app.services.api_client import APIClient


class SteamAPI:
    API_URL = 'http://api.steampowered.com/'
    API_KEY = settings.STEAM_KEY

    def __init__(self) -> None:
        self.api_client = APIClient(self.API_URL, retries=1, sleep=0, exclude_codes=[codes.UNAUTHORIZED])
        self.api_key = {'key': self.API_KEY}

    @lru_cache(maxsize=500)  # noqa: B019
    async def get_steam_player(self, steamid: int | str) -> SteamUser:
        response: SteamPlayerBaseResponse = await self.api_client.api_GET_request(
            '/ISteamUser/GetPlayerSummaries/v0002/',
            query={'steamids': steamid, 'key': self.API_KEY},
            response_model=SteamPlayerBaseResponse,
        )
        return response.response.players[0]

    @lru_cache(maxsize=200)  # noqa: B019
    async def get_player_friend_list(self, stemaid: int | str) -> list[SteamFriend]:
        response: SteamFriendListResponse = await self.api_client.api_GET_request(
            '/ISteamUser/GetFriendList/v0001/',
            query={'steamid': stemaid, 'relationship': 'friend', 'key': self.API_KEY},
            response_model=SteamFriendListResponse,
        )
        if response.friend_list is None:
            return []
        return response.friend_list.friends
