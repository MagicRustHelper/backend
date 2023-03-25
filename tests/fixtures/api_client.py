from typing import Any, Union

import pytest
from pydantic import parse_obj_as

from app.services.api_client import APIClient, HTTPClient, ResponseModel
from app.services.magic_rust.magic_rust_api import MagicRustAPI
from app.services.RCC.rcc_api import RustCheatCheckAPI


@pytest.fixture
def mocked_rcc_api() -> RustCheatCheckAPI:
    def get_rcc_api(return_value: Any) -> RustCheatCheckAPI:
        rcc_api = RustCheatCheckAPI()
        rcc_api.api_client = MockedAPIClient(return_value)
        return rcc_api

    return get_rcc_api


@pytest.fixture
def mocked_mr_api() -> MagicRustAPI:
    def get_magic_rust_api(return_value: Any) -> MagicRustAPI:
        mr_api = MagicRustAPI()
        mr_api.api_client = MockedAPIClient(return_value)
        return mr_api

    return get_magic_rust_api


@pytest.fixture
def mocked_api_client() -> APIClient:
    def get_api_client(return_value: Any) -> APIClient:
        client = MockedAPIClient(return_value)
        return client

    return get_api_client


class MockedHTTPClient(HTTPClient):
    def __init__(self, return_value: Any) -> None:
        self.return_value = return_value

    async def raw_request(self, *args, **kwargs) -> Any:  # noqa
        return self.return_value


class MockedAPIClient(APIClient):
    def __init__(self, return_value: Any) -> None:
        self.http_client = MockedHTTPClient(return_value)

    def _parse_response(
        self, response: Any, response_model: ResponseModel | None = None
    ) -> Union[ResponseModel, list[ResponseModel], None]:
        response_json = response
        if isinstance(response_json, dict):
            return response_model.parse_obj(response_json)
        elif isinstance(response_json, list):
            return parse_obj_as(list[response_model], response_json)
        else:
            raise TypeError('Not supported response_json type')
