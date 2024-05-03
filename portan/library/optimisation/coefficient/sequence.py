from typing import Iterable, SupportsFloat, Type, TypeVar

from portan.utilities.collections import Sequence

from .coefficient import Coefficient

T = TypeVar("T", bound="CoefficientSequence")


class CoefficientSequence(Sequence[Coefficient]):
    """Immutable sequence of coefficients."""

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
            if any value in `values` is not finite

        Returns
        -------
        T
            coefficient sequence
        """
        return cls(Coefficient(value) for value in values)
