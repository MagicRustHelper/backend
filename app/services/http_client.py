import asyncio
import sys

import httpx
from loguru import logger


class HTTPClient:
    def __init__(
        self, base_url: str = '', retries: int = 3, sleep: int = 6, exclude_codes: list[httpx.codes] | None = None
    ) -> None:
        user_agent = f'MAGIC RUST HELPER (v2.0); Python {sys.version_info.major}.{sys.version_info.minor} // HTTPX v{httpx.__version__}'
        self.client = httpx.AsyncClient(
            base_url=base_url,
            limits=httpx.Limits(max_connections=60, max_keepalive_connections=10, keepalive_expiry=60 * 60),
            timeout=httpx.Timeout(60 * 60),
        )
        self.client.headers.update({'User-Agent': user_agent})
        self.retries = retries
        self.sleep = sleep
        self.exclude_codes = exclude_codes or []

    async def raw_request(
        self, url: str, http_method: str, query: dict | None = None, payload: dict | None = None, **kwargs
    ) -> httpx.Response:
        retry = self.retries
        while retry > 0:
            logger.debug(f'{retry} Make request: {http_method}: {url} | Query: {query} | Payload: {payload}')
            response = await self.client.request(
                http_method,
                url,
                params=query,
                data=payload,
                **kwargs,
            )
            logger.debug('Receive response {}: {}', response.request, response.text)
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                if response.status_code in self.exclude_codes:
                    return response
                retry -= 1
                logger.warning(e)
                if retry == 0:
                    raise e
                await asyncio.sleep(self.sleep)
            else:
                return response

    async def request_get(self, url: str, query: dict | None = None, **kwargs) -> httpx.Response:
        return await self.raw_request(url, 'GET', query=query, **kwargs)

    async def request_post(
        self, url: str, query: dict | None = None, payload: dict | None = None, **kwargs
    ) -> httpx.Response:
        return await self.raw_request(url, 'POST', query=query, payload=payload, **kwargs)

    async def requets_put(
        self, url: str, query: dict | None = None, payload: dict | None = None, **kwargs
    ) -> httpx.Response:
        return await self.raw_request(url, 'PUT', query=query, payload=payload, **kwargs)

    async def request_delete(self, url: str, query: dict | None = None, **kwargs) -> httpx.Response:
        return await self.raw_request(url, 'DELETE', query=query, **kwargs)
