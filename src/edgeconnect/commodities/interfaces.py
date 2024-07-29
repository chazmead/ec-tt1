from edgeconnect.commodities import types


class Average:
    async def calculate(self) -> types.AverageValue:
        raise NotImplementedError
