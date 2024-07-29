import datetime
import typing

import fastapi

import alphavantage
from edgeconnect import commodities
from edgeconnect.commodities.services import alphavantage as av

router = fastapi.APIRouter()


def _commodity_average_by_date_composite_root(
    start_date: datetime.date,
    end_date: datetime.date,
) -> commodities.services.CommodityAverageValueByDateService:
    return commodities.services.CommodityAverageValueByDateService(
        _start_date=start_date,
        _end_date=end_date,
        _market_client=av.DailyTimeSeriesClient(
            _commodity=alphavantage.enums.Commodity.COPPER.value,
            _interval=alphavantage.enums.Interval.DAILY.value,
        ),
    )


@router.get("/average/for-range")
async def lookup(
    commodity_average_service: typing.Annotated[
        commodities.interfaces.Average,
        fastapi.Depends(_commodity_average_by_date_composite_root),
    ],
) -> commodities.types.AverageValue:
    return await commodity_average_service.calculate()
