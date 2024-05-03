from typing import Iterable, Type, TypeVar

from .dated import Dated
from .sequence import DatedSequence

T_co = TypeVar("T_co", bound=Dated, covariant=True)
S = TypeVar("S", bound="DatedSeries")


class DatedSeries(DatedSequence[T_co]):
    """Immutable sequence of dated with unique dates, and
    sorted dates in ascending order.

    Parameters
    ----------
    values: Iterable[T_co]
        values to create the series from

    Raises
    ------
    ValueError
        if `values` is not sorted in ascending order, or
        if `values` contains multiple values with the same date
    """

    @classmethod
    def from_unsorted(cls: Type[S], values: Iterable[T_co]) -> S:
        """Create a series by sorting `values` per date in ascending
        order.

        Parameters
        ----------
        values
            values to create the series from

        Raises
        ------
        ValueError
            if `values` contains multiple values with the same date

        Returns
        -------
        S
            dated series
        """
        return cls(sorted(values, key=lambda x: x.date))

    def __init__(self, values: Iterable[T_co]):
        super().__init__(values)
        self._raise_if_has_non_ascending_dates()
        self._raise_if_has_duplicated_dates()

    def _raise_if_has_non_ascending_dates(self):
        if not self.has_ascending_dates():
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"values must be sorted by dates in ascending order"
            )
            raise ValueError(msg)

    def _raise_if_has_duplicated_dates(self):
        if self.has_duplicated_dates():
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"values must not contain multiple values with the same "
                f"date"
            )
            raise ValueError(msg)
