from typing import TypeVar

from portan.utilities.collections import Sequence

from ...date.sequence import DateSequence
from .dated import Dated

T_co = TypeVar("T_co", bound=Dated, covariant=True)
S = TypeVar("S", bound="DatedSequence")


class DatedSequence(Sequence[T_co]):
    """Immutable sequence of dated."""

    @property
    def dates(self) -> DateSequence:
        """Date of each dated in this sequence (in order)."""
        return DateSequence(value.date for value in self)

    def has_ascending_dates(self) -> bool:
        """Verify if the dates in this sequence are in ascending
        order.

        Returns
        -------
        bool
            True if the dates in this sequence are in ascending order,
            else False
        """
        return self.dates.is_ascending()

    def has_duplicated_dates(self) -> bool:
        """Verify if the dates in this sequence contain duplicates.

        Returns
        -------
        bool
            True if the dates in this sequence contain duplicates,
            else False
        """
        return self.dates.contains_duplicates()

    def compress(self: S, dates: DateSequence) -> S:
        """Compress this sequence by removing the dated which
        date is not in `dates`. The order of this sequence is
        preserved.

        This operation is **not** performed in-place.

        Parameters
        ----------
        dates
            dates to use to determine which dated from this sequence
            to remove

        Returns
        -------
        S
            new compressed sequence
        """
        return self.__class__(value for value in self if value.date in dates)
