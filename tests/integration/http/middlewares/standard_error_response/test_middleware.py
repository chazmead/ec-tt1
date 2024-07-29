import json
import typing
import uuid
from unittest import mock

import pytest
from starlette import requests as starlette_requests, responses as starlette_responses

CallNext = typing.Callable[
    [starlette_requests.Request],
    typing.Awaitable[starlette_responses.Response],
]


class BaseTestCase:
    async def test_status_code(
        self,
        dispatched_response: starlette_responses.Response,
        expected_status_code: int,
    ) -> None:
        assert dispatched_response.status_code == expected_status_code

    async def test_status_code_logged(
        self,
        dispatched_response: starlette_responses.Response,
        logger: mock.Mock,
        expected_status_code: int,
        request_method: str,
        request_path: str,
    ) -> None:
        logger.info.assert_has_calls(
            [
                mock.call(
                    "HTTP Response Status Code Log",
                    extra={
                        "http_request_method": request_method,
                        "http_request_path": request_path,
                        "http_response_status_code": expected_status_code,
                        "http_response_status_category": f"{expected_status_code // 100}xx",
                    },
                ),
            ],
        )


@pytest.mark.anyio
class TestSuccess(BaseTestCase):
    @pytest.fixture(params=("GET", "POST", "PUT", "PATCH", "DELETE"))
    def request_method(self, request: typing.Any) -> str:
        _param: str = request.param
        return _param

    @pytest.fixture(params=(200, 201, 204))
    def response_status_code(self, request: typing.Any) -> int:
        _param: int = request.param
        return _param

    @pytest.fixture
    def expected_status_code(self, response_status_code: int) -> int:
        _param: int = response_status_code
        return _param

    @pytest.fixture
    def app_response(
        self,
        app_response: starlette_responses.Response,
        response_status_code: int,
    ) -> starlette_responses.Response:
        app_response.status_code = response_status_code
        return app_response

    async def test_call_next_called(
        self,
        dispatched_response: starlette_responses.Response,
        call_next: mock.Mock,
        app_request: starlette_requests.Request,
    ) -> None:
        call_next.assert_called_once_with(app_request)

    async def test_response(
        self,
        app_response: starlette_responses.Response,
        dispatched_response: starlette_responses.Response,
    ) -> None:
        assert app_response == dispatched_response


@pytest.mark.anyio
class TestExceptionRaised(BaseTestCase):
    @pytest.fixture
    def exception_cls(self) -> typing.Type[Exception]:
        return Exception

    @pytest.fixture
    def call_next(self, call_next: mock.Mock, raised_exception: Exception) -> CallNext:
        call_next.side_effect = raised_exception
        _call_next: CallNext = call_next
        return _call_next

    @pytest.fixture
    async def decoded_response_content(
        self,
        dispatched_response: starlette_responses.Response,
    ) -> dict[str, typing.Any]:
        _content: dict[str, typing.Any] = json.loads(dispatched_response.body)
        return _content

    @pytest.fixture
    def expected_status_code(self) -> int:
        return 500

    async def test_detail(
        self,
        decoded_response_content: dict[str, typing.Any],
        exception_msg: str,
    ) -> None:
        assert "detail" in decoded_response_content
        assert decoded_response_content["detail"] == exception_msg

    async def test_error_ref(
        self,
        decoded_response_content: dict[str, typing.Any],
    ) -> None:
        assert "error_ref" in decoded_response_content
        # Should always be a UUID, so attempt to decode it.
        uuid.UUID(decoded_response_content["error_ref"])
