from typing import Iterable, SupportsFloat, Tuple, Type, TypeVar

from ...price.sequence import PriceSequence
from ..generic.series import DatedSeries
from .dated import DatedPrice

T = TypeVar("T", bound="DatedPriceSeries")


class DatedPriceSeries(DatedSeries[DatedPrice]):
    """An immutable series of :py:class:`DatedPrice`."""

    @classmethod
    def from_basic(
        cls: Type[T],
        values: Iterable[Tuple[str, SupportsFloat]],
    ) -> T:
        """Create a series from tuples consisting of a string representing
        a date, and a floating point-number representing a price
        (i.e., from basic Python types).

        Parameters
        ----------
        values
            tuples consisting of a string representing a date,
            and a floating-point number representing a price

        Raises
        ------
        ValueError
            if any string in `values` is not a date in ISO format,
            if any string in `values` is not a valid date (see :py:class:`Date`
            for the definition of a valid date),
            if any floating-point number in `values` is non-finite,
            if any floating-point number in `values` is not strictly positive,
            if the dates (i.e., strings) in `values` are not sorted in
            ascending order, or
            if `values` contains multiple values with the same date
            (i.e., string)

        Returns
        -------
        T
            series of dated
        """
        return cls(cls._from_basic(values))

    @classmethod
    def from_unsorted_basic(
        cls: Type[T],
        values: Iterable[Tuple[str, SupportsFloat]],
    ) -> T:
        """Create a series from tuples consisting of a string representing
        a date, and a floating point-number representing a price
        (i.e., from basic Python types). `values` is sorted by date
        in ascending order prior to creating the series.

        Parameters
        ----------
        values
            tuples consisting of a string representing a date,
            and a floating-point number representing a price

        Raises
        ------
        ValueError
            if any string in `values` is not a date in ISO format,
            if any string in `values` is not a valid date (see :py:class:`Date`
            for the definition of a valid date),
            if any floating-point number in `values` is non-finite,
            if any floating-point number in `values` is not strictly
            positive, or
            if `values` contains multiple values with the same date
            (i.e., string)

        Returns
        -------
        T
            series of dated
        """
        return cls.from_unsorted(cls._from_basic(values))

    @staticmethod
    def _from_basic(
        values: Iterable[Tuple[str, SupportsFloat]],
    ) -> Iterable[DatedPrice]:
        return (DatedPrice.from_basic(*value) for value in values)

    @property
    def prices(self) -> PriceSequence:
        """Price of each dated in this series (in order)."""
        return PriceSequence(value.value for value in self)

    def to_basic(self) -> Iterable[Tuple[str, float]]:
        """Get this series as basic Python types.

        This method returns an iterable of tuples representing
        the dated in this series. The first element of each
        tuple is the date of the corresponding dated as a string
        in ISO format, while the second element is the price as a float.

        Returns
        -------
        Iterable[Tuple[str, float]]
            this series as basic Python types
        """
        return (value.to_basic() for value in self)
