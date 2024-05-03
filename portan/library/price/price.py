from math import log
from typing import TypeVar

from portan.utilities.finite.positive import PositiveFinite

from ..rate import Rate

T = TypeVar("T", bound="Price")


class Price(PositiveFinite):
    """Price of a financial instrument (e.g., 101.402).

    The price of a financial instrument is represented internally with a
    finite and strictly positive floating-point number with
    undefined precision.
    """

    def growth(self: T, begin: T) -> Rate:
        """Get the continuous rate of growth of this price when comparing it
        to the price at the beginning of the period (i.e., `begin`).

        Parameters
        ----------
        begin
            price a the beginning of the period

        Raises
        ------
        ValueError
            if the ratio of this price over `begin` is either too small
            or too big (ie., close or equal to +inf or 0.0)

        Returns
        -------
        Rate
            continuous rate of growth
        """
        return Rate(log(self._value / begin._value))
