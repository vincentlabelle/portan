from typing import Iterable, SupportsFloat, Type, TypeVar

from portan.utilities.collections import Sequence

from .covariance import Covariance

T = TypeVar("T", bound="CovarianceSequence")


class CovarianceSequence(Sequence[Covariance]):
    """Immutable sequence of covariances."""

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

        Returns
        -------
        T
            sequence from `values`
        """
        return cls(Covariance(value) for value in values)
