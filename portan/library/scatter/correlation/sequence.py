from typing import Iterable, SupportsFloat, Type, TypeVar

from portan.utilities.collections import Sequence

from .correlation import Correlation

T = TypeVar("T", bound="CorrelationSequence")


class CorrelationSequence(Sequence[Correlation]):
    """Immutable sequence of correlations."""

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
            if any value in `values` is outside [-1.0, 1.0]

        Returns
        -------
        T
            sequence from `values`
        """
        return cls(Correlation(value) for value in values)
