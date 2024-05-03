from typing import SupportsFloat, Tuple, Type, TypeVar

from ...date import Date
from ...price import Price
from ..generic import Dated

T = TypeVar("T", bound="DatedPrice")


class DatedPrice(Dated[Price]):
    """Price of a financial instrument at a specific date."""

    @classmethod
    def from_basic(cls: Type[T], date: str, price: SupportsFloat) -> T:
        """Create a dated from a string and a floating-point number
        (i.e., from basic Python types).

        Parameters
        ----------
        date
            date at which `price` is from
        price
            price as of `date`

        Raises
        ------
        ValueError
            if `date` is not a date in ISO format,
            if `date` is not a valid date (see :py:class:`Date` for a
            definition of a valid date),
            if `price` is not finite, or
            if `price` is not strictly positive

        Returns
        -------
        T
            dated price
        """
        return cls(Date(date), Price(price))

    def to_basic(self) -> Tuple[str, float]:
        """Get this dated as basic Python types.

        This method returns a tuple representing this dated
        where the first element is the date as a string in ISO format,
        and the second element is the price as a float.

        Returns
        -------
        Tuple[str, float]
            this dated as basic Python types
        """
        return str(self._date), float(self._value)
