import pytest


@pytest.fixture
def endpoint_path() -> str:
    return "/average/for-range?start_date=2024-01-01&end_date=2024-01-31"


def test_status_code(response_status: int) -> None:
    assert response_status == 200


def test_response_body(response_body: str) -> None:
    assert response_body == '{"value":4.0}'
