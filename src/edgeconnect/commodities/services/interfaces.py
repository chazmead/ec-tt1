from edgeconnect.commodities.services import types


class MarketClient:
    async def get_prices(self) -> types.Prices:
        raise NotImplementedError
