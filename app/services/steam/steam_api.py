from app.core import settings
from app.entities import SteamBaseResponse, SteamUser
from app.services.api_client import APIClient, ResponseModel


class SteamAPI:
    API_URL = 'http://api.steampowered.com/'
    API_KEY = settings.STEAM_KEY

    def __init__(self) -> None:
        self.api_client = APIClient(self.API_URL, retries=1, sleep=0)
        self.api_key = {'key': self.API_KEY}

    async def get_steam_player(self, steamid: int | str) -> SteamUser:
        return await self.api_request(
            '/ISteamUser/GetPlayerSummaries/v0002/', params={'steamids': steamid}, response_model=SteamBaseResponse
        )

    async def api_request(
        self, endpoint: str, params: dict, response_model: SteamBaseResponse | None = None
    ) -> ResponseModel:
        params |= self.api_key
        response = await self.api_client.api_GET_request(endpoint, params, response_model)
        return response.response.players[0]
