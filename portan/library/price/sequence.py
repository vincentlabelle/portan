from typing import Iterable, SupportsFloat, Type, TypeVar

from portan.utilities.collections import Sequence

from ..rate.sequence import RateSequence
from .price import Price

T = TypeVar("T", bound="PriceSequence")


class PriceSequence(Sequence[Price]):
    """Immutable sequence of prices."""

    @classmethod
    def from_float(cls: Type[T], values: Iterable[SupportsFloat]) -> T:
        """Create a sequence from floating-point values.

        Parameters
        ----------
        values
            values to create the sequence from

        Raises
        ------
        ValueError
            if any value in `values` is non-finite, or
            if any value in `values` is not strictly positive

        Returns
        -------
        T
            sequence of prices
        """
        return cls(Price(value) for value in values)

    def growth(self) -> RateSequence:
        """Get the continuous growth rates of the prices in this
        sequence by comparing each price to its preceding price.

        Raises
        ------
        ValueError
            if any pair of consecutive prices in this sequence is such
            that `self[i] / self[i-1]` is either very big or very small
            (i.e., close or equal to +inf or 0.0)

        Returns
        -------
        RateSequence
            continuous growth rates of the prices in this sequence
        """
        return RateSequence(
            [end.growth(begin) for begin, end in zip(self[:-1], self[1:])],
        )
