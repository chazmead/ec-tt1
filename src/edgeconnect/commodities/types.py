import dataclasses


@dataclasses.dataclass(frozen=True)
class AverageValue:
    value: float
