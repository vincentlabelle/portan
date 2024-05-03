from typing import Generic, TypeVar

from ...date import Date

T = TypeVar("T")


class Dated(Generic[T]):
    """Generic value as of a specific date.

    Parameters
    ----------
    date: Date
        date as of which `value` is from
    value: T
        value as of `date`
    """

    def __init__(self, date: Date, value: T):
        self._date = date
        self._value = value

    @property
    def date(self) -> Date:
        """Date as of which this instance value is from."""
        return self._date

    @property
    def value(self) -> T:
        """Value as of this instance's date."""
        return self._value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._date == other._date and self._value == other._value

    def __hash__(self) -> int:
        return hash((self._date, self._value))

    def __str__(self) -> str:
        return f"(date={self._date}, value={self._value})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}{self}>"
