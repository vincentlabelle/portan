from typing import Iterable, Type, TypeVar

from portan.utilities.collections import Sequence

from .date import Date

T = TypeVar("T", bound="DateSequence")


class DateSequence(Sequence[Date]):
    """Immutable sequence of dates."""

    @classmethod
    def from_string(cls: Type[T], values: Iterable[str]) -> T:
        """Create a sequence from strings.

        Parameters
        ----------
        values
            values to create the sequence from

        Raises
        ------
        ValueError
            if any value in `values` is not a date in ISO format, or
            if any value in `values` is not a valid date (see :py:class:`Date`
            for the definition of a valid date)

        Returns
        -------
        T
            sequence of dates
        """
        return cls(Date(value) for value in values)

    def is_ascending(self) -> bool:
        """Verify if this sequence is sorted in ascending order.

        Returns
        -------
        bool
            True if this sequence is sorted in ascending order, else False
        """
        return list(self) == sorted(self)

    def contains_duplicates(self) -> bool:
        """Verify if this sequence contains duplicates.

        Returns
        -------
        bool
            True if this sequence contains duplicates, else False
        """
        return len(self) != len(set(self))

    def intersect(self: T, other: T) -> T:
        """Get the intersection of this sequence and `other`.

        The order of this sequence is preserved in the intersection.

        Parameters
        ----------
        other
            sequence to intersect with this sequence

        Returns
        -------
        T
            intersection between this sequence and `other`
        """
        return self.__class__(value for value in self if value in other)
