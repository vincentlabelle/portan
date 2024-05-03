from datetime import MAXYEAR, MINYEAR, date, timedelta
from typing import Type, TypeVar

T = TypeVar("T", bound="Date")
MIN_YEAR: int = MINYEAR
MAX_YEAR: int = MAXYEAR


class Date:
    """A date (year, month, day) in the Gregorian calendar.

    Parameters
    ----------
    value: str
        date in ISO format

    Raises
    ------
    ValueError
        if `value` is not a date in ISO format, or
        if `value` doesn't represent a valid date (i.e., a month
        outside [1, 12], a day outside [1, day in month for year],
        or a year outside [MIN_YEAR, MAX_YEAR])
    """

    @classmethod
    def today(cls: Type[T]) -> T:
        """Get the current local date.

        Returns
        -------
        T
            today's date
        """
        return cls(date.today().isoformat())

    def __init__(self, value: str):
        self._value: date = self._convert(value)

    def _convert(self, value: str) -> date:
        try:
            return date.fromisoformat(value)
        except Exception:
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"value must be a date in ISO format, "
                f"with a year in [{MIN_YEAR}, {MAX_YEAR}], "
                f"a month in [1, 12], and "
                f"a day in [1, days in month for year]"
            )
            raise ValueError(msg)

    def increment(self: T, *, by: int = 1) -> T:
        """Increment this date by `by` days. This operation
        is not performed in-place.

        Parameters
        ----------
        by
            number of days to increment this date by

        Raises
        ------
        ValueError
            if `by` is negative
        OverflowError
            if the magnitude of `by` is too high

        Returns
        -------
        T
            date incremented by `by` days in comparison to this date
        """
        self._raise_if_is_negative(by)
        return self._increment(by)

    def decrement(self: T, *, by: int = 1) -> T:
        """Decrement this date by `by` days. This operation
        is not performed in-place.

        Parameters
        ----------
        by
            number of days to decrement this date by

        Raises
        ------
        ValueError
            if `by` is negative
        OverflowError
            if the magnitude of `by` is too high

        Returns
        -------
        T
            date decremented by `by` days in comparison to this date
        """
        self._raise_if_is_negative(by)
        return self._increment(-by)

    def _raise_if_is_negative(self, by: int):
        if by < 0:
            msg = (
                f"cannot increment(decrement) {self.__class__.__name__}; "
                f"by must be non-negative"
            )
            raise ValueError(msg)

    def _increment(self: T, by: int) -> T:
        incremented = self._increment_value(by)
        return self.__class__(incremented.isoformat())

    def _increment_value(self, by: int) -> date:
        try:
            return self._value + timedelta(days=by)
        except OverflowError:
            msg = (
                f"cannot increment(decrement) {self.__class__.__name__}; "
                f"by's magnitude is too high"
            )
            raise OverflowError(msg)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value < other._value

    def __le__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value <= other._value

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value > other._value

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value >= other._value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value.isoformat()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self})>"
