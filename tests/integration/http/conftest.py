import typing

import httpx
import pytest
from fastapi.testclient import TestClient

from edgeconnect import http


@pytest.fixture
def http_client() -> typing.Iterator[TestClient]:
    with TestClient(http.api) as client:
        yield client


@pytest.fixture
def endpoint_method() -> str:
    return "GET"


@pytest.fixture
def endpoint_path() -> str:
    return "/"


@pytest.fixture
def client_method(
    http_client: TestClient,
    endpoint_method: str,
) -> typing.Callable[[str], httpx._models.Response]:
    _method: typing.Callable[[str], httpx._models.Response] = getattr(
        http_client,
        endpoint_method.lower(),
    )
    return _method


@pytest.fixture
def response(
    client_method: typing.Callable[[str], httpx._models.Response],
    endpoint_path: str,
) -> httpx._models.Response:
    return client_method(endpoint_path)


@pytest.fixture
def response_status(response: httpx._models.Response) -> int:
    return response.status_code


@pytest.fixture
def response_body(response: httpx._models.Response) -> str:
    return response.text


@pytest.fixture
def response_json(
    response: httpx._models.Response,
) -> typing.Any:
    return response.json()
