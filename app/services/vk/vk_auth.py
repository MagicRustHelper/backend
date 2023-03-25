from app.core import settings
from app.entities import VKAuthResponse
from app.services.api_client import APIClient


class VKAuth:
    ACCESS_TOKEN_URL: str = 'https://oauth.vk.com/access_token?client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&code={code}'

    def __init__(self) -> None:
        self.api_client = APIClient(retries=1)

    async def get_oauth2_credentials(self, code: str) -> VKAuthResponse:
        url = self.build_access_token_url(code)
        return await self.api_client.api_GET_request(url, response_model=VKAuthResponse)

    def build_access_token_url(self, code: str) -> str:
        return self.ACCESS_TOKEN_URL.format(
            client_id=settings.VK_CLIENT_ID,
            client_secret=settings.VK_CLIENT_SECRET,
            redirect_uri=settings.VK_REDIRECT_URI,
            code=code,
        )
