from typing import TypeVar, Union

import httpx
from pydantic import BaseModel, parse_obj_as

from app.services.http_client import HTTPClient

ResponseModel = TypeVar('ResponseModel', bound=BaseModel)


class APIClient:
    def __init__(
        self, base_url: str = '', retries: int = 3, sleep: int = 6, exclude_codes: list[httpx.codes] | None = None
    ) -> None:
        self.http_client = HTTPClient(base_url, retries=retries, sleep=sleep, exclude_codes=exclude_codes)

    async def api_GET_request(
        self,
        url: str,
        query: dict | None = None,
        response_model: ResponseModel | None = None,
    ) -> ResponseModel:
        response = await self.http_client.request_get(url, query=query)
        return self._parse_response(response, response_model)

    async def api_POST_request(
        self,
        url: str,
        query: str | None = None,
        payload: dict | None = None,
        response_model: ResponseModel | None = None,
    ) -> ResponseModel:
        response = await self.http_client.request_post(url, query=query, payload=payload)
        return self._parse_response(response, response_model)

    async def api_PUT_request(
        self,
        url: str,
        query: dict | None = None,
        payload: dict | None = None,
        response_model: ResponseModel | None = None,
    ) -> ResponseModel:
        response = await self.http_client.requets_put(url, query=query, payload=payload)
        return self._parse_response(response, response_model)

    async def api_DELETE_request(
        self,
        url: str,
        query: dict | None = None,
        response_model: ResponseModel | None = None,
    ) -> ResponseModel:
        response = await self.http_client.request_delete(url, query=query)
        return self._parse_response(response, response_model)

    def _parse_response(
        self,
        response: httpx.Response,
        response_model: ResponseModel | None = None,
    ) -> Union[ResponseModel, list[ResponseModel], None]:
        if response_model is None:
            return

        response_json = response.json()
        if isinstance(response_json, dict):
            return response_model.parse_obj(response_json)
        elif isinstance(response_json, list):
            return parse_obj_as(list[response_model], response_json)
        else:
            raise TypeError('Not supported response_json type')
