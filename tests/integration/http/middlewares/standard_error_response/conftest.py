import logging
import typing
from unittest import mock

import pytest
from starlette import (
    requests as starlette_requests,
    responses as starlette_responses,
    types as starlette_types,
)

from edgeconnect.http.middlewares import StandardErrorResponse

CallNext = typing.Callable[
    [starlette_requests.Request],
    typing.Awaitable[starlette_responses.Response],
]


@pytest.fixture
def exception_msg() -> str:
    return "Test Exception"


@pytest.fixture
def raised_exception(
    exception_cls: typing.Type[Exception],
    exception_msg: str,
) -> Exception:
    return exception_cls(exception_msg)


@pytest.fixture
def raising_app(
    app: mock.Mock,
    raised_exception: Exception,
) -> starlette_types.ASGIApp:
    app.side_effect = raised_exception
    _app: starlette_types.ASGIApp = app
    return _app


@pytest.fixture(params=(True, False))
def debug_mode(request: typing.Any) -> bool:
    _mode: bool = request.param
    return _mode


@pytest.fixture
def logger() -> logging.Logger:
    _logger: logging.Logger = mock.create_autospec(logging.Logger, instance=True)
    return _logger


@pytest.fixture
def standard_response_middleware(
    app: starlette_types.ASGIApp,
    debug_mode: bool,
    logger: logging.Logger,
) -> StandardErrorResponse:
    return StandardErrorResponse(
        app=app,
        debug_mode=debug_mode,
        logger=logger,
    )


@pytest.fixture
def request_method() -> str:
    return "GET"


@pytest.fixture
def request_path() -> str:
    return "/test"


@pytest.fixture
def app_request(request_method: str, request_path: str) -> starlette_requests.Request:
    request = mock.create_autospec(starlette_requests.Request, instance=True)
    request.method = request_method
    request.url.path = request_path
    _request: starlette_requests.Request = request
    return _request


@pytest.fixture
def app_response() -> starlette_responses.Response:
    _response: starlette_responses.Response = mock.create_autospec(
        starlette_responses.Response,
        instance=True,
    )
    return _response


@pytest.fixture
def call_next(app_response: starlette_responses.Response) -> CallNext:
    _fn = mock.AsyncMock()
    # as this middleware does not directly refer to the `self._app`, instead it
    # redirects the call to a `call_next` argument passed into the method..
    _fn.return_value = app_response
    return _fn


@pytest.fixture
async def dispatched_response(
    standard_response_middleware: StandardErrorResponse,
    app_request: starlette_requests.Request,
    call_next: CallNext,
) -> starlette_responses.Response:
    return await standard_response_middleware.dispatch(
        request=app_request,
        call_next=call_next,
    )
