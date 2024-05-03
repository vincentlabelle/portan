from enum import Enum


class Frequency(Enum):
    """Frequency of measurements (e.g., frequency of price measurements)."""

    ANNUAL = 1
    MONTHLY = 12
    DAILY = 252

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self})>"
