import dataclasses
import logging
import os
import typing

import requests

logger = logging.getLogger(__name__)

DOMAIN = "www.alphavantage.co"
API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY")


@dataclasses.dataclass(frozen=True)
class AbstractClient:
    def _get_function(self) -> str:
        raise NotImplementedError

    def _get_path(self) -> str:
        return "/query"

    def _build_query(self) -> str:
        _function = self._get_function()
        return f"?function={_function}&apikey={API_KEY}"

    def _build_url(self) -> str:
        _path = self._get_path()
        _query = self._build_query()
        return f"https://{DOMAIN}{_path}{_query}"

    def _response(self) -> dict[str, typing.Any]:
        _url = self._build_url()
        _resp_json: dict[str, typing.Any] = requests.get(_url).json()
        return _resp_json
