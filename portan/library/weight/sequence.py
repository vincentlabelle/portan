from typing import Iterable, SupportsFloat, SupportsInt, Type, TypeVar

from portan.utilities.collections import Sequence

from .weight import Weight

T = TypeVar("T", bound="WeightSequence")


class WeightSequence(Sequence[Weight]):
    """Immutable sequence of weights."""

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
            if any value in `values` is nan
        OverflowError
            if any value in `values` is too big in absolute terms
            (i.e., there's an overflow during the conversion to
            :py:class:`Weight`)

        Returns
        -------
        T
            sequence from `values`
        """
        return cls(Weight.from_float(value) for value in values)

    @classmethod
    def from_int(cls: Type[T], values: Iterable[SupportsInt]) -> T:
        """Create a sequence from integer values (i.e., `values`).

        Parameters
        ----------
        values
            values to create the sequence from

        Returns
        -------
        T
            sequence from `values`
        """
        return cls(Weight(value) for value in values)

    def sum(self) -> Weight:
        """Get the sum of the weights in this sequence.

        Returns
        -------
        Weight
            sum of the weights in this sequence
        """
        return sum(self, start=Weight(0))


class BalancedWeights(WeightSequence):
    """Immutable sequence of weights summing to 100%.

    Parameters
    ----------
    values: Iterable[Weight]
        weights to create the sequence from

    Raises
    ------
    ValueError
        if the sum of `values` is not equal to 100%
    """

    def __init__(self, values: Iterable[Weight]):
        super().__init__(values)
        self._raise_if_does_not_sum_to_one_hundred()

    def _raise_if_does_not_sum_to_one_hundred(self):
        if self.sum() != Weight(100):
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"values must sum to one hundred (i.e., 100%)"
            )
            raise ValueError(msg)
