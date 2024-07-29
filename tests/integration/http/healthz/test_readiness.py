import pytest


@pytest.fixture
def endpoint_path() -> str:
    return "/healthz/readiness"


def test_status_code(response_status: int) -> None:
    assert response_status == 200


def test_response_body(response_body: str) -> None:
    assert response_body == ""
