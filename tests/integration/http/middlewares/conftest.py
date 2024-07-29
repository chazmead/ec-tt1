from unittest import mock

import pytest
from starlette import types as starlette_types


@pytest.fixture(scope="module")
def anyio_backend() -> str:
    # We only use the asyncio backend, so no need to run tests against trio
    return "asyncio"


@pytest.fixture
def scope() -> starlette_types.Scope:
    _scope: starlette_types.Scope = mock.create_autospec(
        starlette_types.Scope,
        instance=True,
    )
    return _scope


@pytest.fixture
def receive() -> starlette_types.Receive:
    _receive: starlette_types.Receive = mock.create_autospec(
        starlette_types.Receive,
        instance=True,
    )
    return _receive


@pytest.fixture
def send() -> starlette_types.Send:
    _send: starlette_types.Send = mock.create_autospec(
        starlette_types.Send,
        instance=True,
    )
    return _send


@pytest.fixture
async def app() -> starlette_types.ASGIApp:
    app = mock.AsyncMock()
    app.return_value = None
    return app
