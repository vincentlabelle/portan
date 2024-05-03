from typing import Iterable, SupportsFloat, Type, TypeVar

from ...date import Date
from ...price import Price
from ...price.sequence import PriceSequence
from ..generic import Dated
from ..price.dated import DatedPrice

T = TypeVar("T", bound="DatedPrices")


class DatedPrices(Dated[PriceSequence]):
    """Prices of financial instruments at a specific date."""

    @classmethod
    def from_basic(
        cls: Type[T],
        date: str,
        prices: Iterable[SupportsFloat],
    ) -> T:
        """Create a dated from a string and floating-point numbers
        (i.e., basic Python types)

        Parameters
        ----------
        date
            date at which `prices` are from
        prices
            prices as of `date`

        Raises
        ------
        ValueError
            if `date` is not a date in ISO format,
            if `date` doesn't represent a valid date (see :py:class:`Date`
            for a definition of a valid date),
            if any value in `prices` is not finite, or
            if any value in `prices` is not strictly positive

        Returns
        -------
        T
            dated prices
        """
        return cls(
            Date(date),
            PriceSequence.from_float(prices),
        )

    @classmethod
    def from_single(cls: Type[T], single: DatedPrice) -> T:
        """Create a `DatedPrices` from a *single* financial
        instrument dated price.

        Parameters
        ----------
        single
            dated price to create a `DatedPrices` from

        Returns
        -------
        T
            dated prices
        """
        return cls(single.date, PriceSequence([single.value]))

    def add(self: T, price: Price) -> T:
        """Add a price at the end of this dated's sequence of prices.

        This operation is **not** performed in-place.

        Parameters
        ----------
        price
            price to add to this dated

        Returns
        -------
        T
            new dated with `price` at the end of
            the sequence of prices
        """
        return self.__class__(self.date, self.value.add(price))
