import asyncio
import dataclasses
import datetime

import alphavantage
from edgeconnect.commodities.services import interfaces, types


@dataclasses.dataclass(frozen=True)
class DailyTimeSeriesClient(
    alphavantage.client.AbstractClient,
    interfaces.MarketClient,
):
    _commodity: str
    _interval: str

    def _get_function(self) -> str:
        return self._commodity

    def _build_query(self) -> str:
        _query = super()._build_query()
        return f"{_query}&interval={self._interval}"

    async def get_prices(self) -> types.Prices:
        _response = await asyncio.to_thread(self._response)
        return types.Prices(
            prices=tuple(
                [
                    types.Price(
                        date=datetime.datetime.strptime(
                            _record["date"],
                            "%Y-%m-%d",
                        ).date(),
                        value=float(_record["value"]),
                    )
                    for _record in _response["data"]
                    if _record["value"] not in (None, ".", "")  # some garbage data
                ]
            ),
        )
