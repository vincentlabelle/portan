from typing import Iterable, Tuple, Type, TypeVar

from ...price.matrix import PriceMatrix
from ..generic.series import DatedSeries
from ..price.series import DatedPriceSeries
from .dated import DatedPrices

T = TypeVar("T", bound="DatedPricesSeries")


class DatedPricesSeries(DatedSeries[DatedPrices]):
    """Immutable series of :py:class:`DatedPrices`.

    Parameters
    ----------
    values: Iterable[DatedPrices]
        values to create the series from

    Raises
    ------
    ValueError
        if `values` is not sorted in ascending order,
        if `values` contains multiple values with the same date, or
        if the number of prices is not the same for all values in `values`
    """

    @classmethod
    def from_single(cls: Type[T], single: DatedPriceSeries) -> T:
        """Create a `DatedPricesSeries` from a series of dated price.

        Parameters
        ----------
        single
            series of dated price to create a `DatedPricesSeries` from

        Returns
        -------
        T
            dated prices series
        """
        return cls(DatedPrices.from_single(value) for value in single)

    def __init__(self, values: Iterable[DatedPrices]):
        super().__init__(values)
        self._raise_if_number_of_prices_mismatch()

    def _raise_if_number_of_prices_mismatch(self):
        if self._is_number_of_prices_mismatch():
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"values must all have the same number of prices."
            )
            raise ValueError(msg)

    def _is_number_of_prices_mismatch(self) -> bool:
        return len(set(len(value.value) for value in self)) > 1

    @property
    def prices(self) -> PriceMatrix:
        """Prices of each dated in this series (in order)
        in matrix format, where each sequence of price is a column."""
        return PriceMatrix(
            (value.value for value in self),
        ).transpose()

    def to_basic(self) -> Iterable[Tuple[str, Iterable[float]]]:
        """Get this series as basic Python types.

        This method returns an iterable of tuples representing
        the dated in this series. The first element of each tuple is
        the date of the corresponding dated as a string in ISO
        format, while the second element is the prices as an
        iterable of float.

        Returns
        -------
        Iterable[Tuple[str, Iterable[float]]]
            this series as basic Python types
        """
        return (
            (str(value.date), (float(price) for price in value.value))
            for value in self
        )

    def add(self: T, single: DatedPriceSeries) -> T:
        """Add a price at the end of each dated's sequence of price
        in this series by concatenating this series with `single`.

        This operation is **not** performed in-place.

        Parameters
        ----------
        single
            series to concatenate with this series

        Raises
        ------
        ValueError
            if `single` does not have the same dates as this series

        Returns
        -------
        T
            new series with concatenated prices
        """
        self._raise_if_dates_mismatch(single)
        return self.__class__(m.add(s.value) for m, s in zip(self, single))

    def _raise_if_dates_mismatch(self, single: DatedPriceSeries):
        if self.dates != single.dates:
            msg = "cannot add; single must have the same dates as this instance"
            raise ValueError(msg)
