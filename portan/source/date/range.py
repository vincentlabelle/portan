from typing import Type, TypeVar

from .date import Date

T = TypeVar("T", bound="DateRange")


class DateRange:
    """A range of time delimited by two dates.

    Parameters
    ----------
    begin: Date
        beginning of the range
    end: Date
        end of the range

    Raises
    ------
    ValueError
        if `end` is before `begin` (i.e., `end < begin`)
    """

    @classmethod
    def from_string(cls: Type[T], begin: str, end: str) -> T:
        """Instantiate a date range delimited by `begin` and
        `end`.

        Parameters
        ----------
        begin
            beginning of the range
        end
            end of the range

        Raises
        ------
        ValueError
            if `begin` or `end` is not a date in ISO format,
            if `begin or `end` is not a valid date (see :py:class:`Date` for
            the definition of a valid date), or
            if `end` represents a date that is before `begin`

        Returns
        -------
        T
            date range delimited by `begin` and `end`
        """
        return cls(Date(begin), Date(end))

    def __init__(self, begin: Date, end: Date):
        self._begin = begin
        self._end = end
        self._raise_if_end_is_lower_than_begin()

    def _raise_if_end_is_lower_than_begin(self):
        if self._end < self._begin:
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"end must be greater than or equal to begin"
            )
            raise ValueError(msg)

    @property
    def begin(self) -> Date:
        """Beginning of range."""
        return self._begin

    @property
    def end(self) -> Date:
        """End of range."""
        return self._end

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._begin == other._begin and self._end == other._end

    def __hash__(self) -> int:
        return hash((self._begin, self._end))

    def __str__(self) -> str:
        return f"(begin={self._begin}, end={self._end})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}{self}>"
