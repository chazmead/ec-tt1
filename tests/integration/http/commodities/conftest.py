import typing

import pytest
import responses

import alphavantage


@pytest.fixture
def alphavantage_function() -> str:
    return alphavantage.enums.Commodity.COPPER.value


@pytest.fixture
def alphavantage_interval() -> str:
    return alphavantage.enums.Interval.DAILY.value


@pytest.fixture
def alphavantage_url(
    alphavantage_function: str,
    alphavantage_interval: str,
) -> str:
    return f"https://{alphavantage.client.DOMAIN}/query?function={alphavantage_function}&apikey={alphavantage.client.API_KEY}&interval={alphavantage_interval}"


@pytest.fixture
def _responses() -> typing.Generator[responses.RequestsMock, None, None]:
    with responses.RequestsMock() as resps:
        yield resps


@pytest.fixture
def alphavantage_response_body() -> dict[str, list[dict[str, str]]]:
    return {
        "data": [
            {"date": "2024-01-01", "value": "1.23"},
            {"date": "2024-01-02", "value": "4.56"},
            {"date": "2024-01-03", "value": "7.89"},
        ],
    }


@pytest.fixture(autouse=True)
def alphavantage_api(
    _responses: responses.RequestsMock,
    alphavantage_url: str,
    alphavantage_response_body: dict[str, list[dict[str, str]]],
) -> None:
    _responses.add(
        responses.GET,
        alphavantage_url,
        json=alphavantage_response_body,
        status=200,
    )
