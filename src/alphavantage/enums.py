import enum


class Commodity(enum.Enum):
    COPPER = "COPPER"
    NATURAL_GAS = "NATURAL_GAS"


class Interval(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
