import logging
import traceback
import typing
import uuid

from fastapi.encoders import jsonable_encoder
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

logger = logging.getLogger(__name__)


class StandardErrorResponse(BaseHTTPMiddleware):
    _debug_mode = False
    _logger = logging.getLogger(__name__)

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        self._debug_mode = kwargs.pop("debug_mode", self._debug_mode)
        self._logger = kwargs.pop("logger", self._logger)
        super().__init__(*args, **kwargs)

    def _data_from_exception(self, exc: Exception) -> dict[str, typing.Any]:
        return {
            "detail": str(exc),
            "error_ref": str(uuid.uuid4()),
        }

    def _standard_error_response(self, exc: Exception) -> Response:
        error_data = self._data_from_exception(exc)
        if self._debug_mode:  # pragma: nocover
            error_data["__debug"] = {
                "exc_msg": str(exc),
                "exc_tb": traceback.extract_tb(exc.__traceback__).format(),
            }

        self._logger.exception(
            f"ExcMiddleware: {exc.__class__.__name__}: {exc}",
            extra=error_data,
        )

        return JSONResponse(
            content=jsonable_encoder(error_data),
            status_code=getattr(exc, "http_status", 500),
        )

    async def dispatch(
        self,
        request: Request,
        call_next: typing.Callable[[Request], typing.Awaitable[Response]],
    ) -> Response:
        try:
            response = await call_next(request)
        except Exception as exc:
            try:
                response = self._standard_error_response(exc)
            except Exception:  # pragma: nocover
                # If we get an exception formatting the exception then this should
                # get logged and bubble up as an outlier and return a standard 500
                # this should be the ONLY time an exception bubbles up to the server
                logger.exception("ERR: Error Formatting Standard Response")
                raise

        self._logger.info(
            "HTTP Response Status Code Log",
            extra={
                "http_request_method": request.method,
                "http_request_path": request.url.path,
                "http_response_status_code": response.status_code,
                "http_response_status_category": f"{response.status_code // 100}xx",
            },
        )
        return response
