from typing import Iterable, SupportsFloat, Type, TypeVar

from portan.utilities.collections import Sequence

from .price import Price

T = TypeVar("T", bound="PriceSequence")


class PriceSequence(Sequence[Price]):
    """Immutable sequence of prices."""

    @classmethod
    def from_float(cls: Type[T], values: Iterable[SupportsFloat]) -> T:
        """Create a sequence from floating-point numbers.

        Parameters
        ----------
        values
            values to create the sequence from

        Raises
        ------
        ValueError
            if any value in `values` is not finite, or
            if any value in `values` is not strictly positive

        Returns
        -------
        T
            sequence from `values`
        """
        return cls(Price(value) for value in values)

    def add(self: T, value: Price) -> T:
        """Add `value` at the end of this sequence.

        This operation is **not** performed in-place.

        Parameters
        ----------
        value
            value to add at the end of this sequence

        Returns
        -------
        T
            new sequence with `value` added at the end
        """
        return self.__class__((*self, value))
