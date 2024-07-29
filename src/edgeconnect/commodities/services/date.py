import dataclasses
import datetime

from edgeconnect import commodities
from edgeconnect.commodities.services import interfaces, types


@dataclasses.dataclass(frozen=True)
class CommodityAverageValueByDateService(commodities.interfaces.Average):
    _start_date: datetime.date
    _end_date: datetime.date

    _market_client: interfaces.MarketClient

    def _filtered_prices(self, prices: types.Prices) -> types.Prices:
        _filtered = tuple(
            filter(
                lambda price: self._start_date <= price.date <= self._end_date,
                prices.prices,
            )
        )
        return types.Prices(prices=_filtered)

    def _average_price(self, prices: types.Prices) -> float:
        return sum(price.value for price in prices.prices) // len(prices.prices)

    async def calculate(self) -> commodities.types.AverageValue:
        _prices = await self._market_client.get_prices()
        _filtered_prices = self._filtered_prices(_prices)
        _average_price = self._average_price(_filtered_prices)

        return commodities.types.AverageValue(
            value=_average_price,
        )
