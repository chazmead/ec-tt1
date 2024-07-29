import dataclasses
import datetime


@dataclasses.dataclass(frozen=True)
class Price:
    date: datetime.date
    value: float


@dataclasses.dataclass(frozen=True)
class Prices:
    prices: tuple[Price, ...]
