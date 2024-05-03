from typing import Iterable, Type, TypeVar

import numpy as np

from portan.utilities.collections.matrix import SymmetricMatrix

from .correlation import Correlation
from .sequence import CorrelationSequence

T = TypeVar("T", bound="CorrelationMatrix")


class CorrelationMatrix(SymmetricMatrix[CorrelationSequence]):
    """Immutable symmetric matrix of correlations."""

    _SYMMETRY_RTOL: float = 1e-8
    _SYMMETRY_ATOL: float = 1e-12

    @classmethod
    def from_iterable(
        cls: Type[T],
        values: Iterable[Iterable[Correlation]],
    ) -> T:
        """Create a matrix from iterables of correlations.

        Parameters
        ----------
        values
            values to create the matrix from

        Raises
        ------
        ValueError
            if the values in `values` are not all of the same length,
            if the length of each value in `values` does not match with the
            number of values in `values`, or
            if the values do not form a symmetric matrix

        Returns
        -------
        T
            correlation matrix from `values`
        """
        return cls(CorrelationSequence(value) for value in values)

    def is_symmetric(self) -> bool:
        """Verify if this matrix is symmetric.

        Returns
        -------
        bool
            True if this matrix is symmetric, else False
        """
        array = np.array(self, dtype=np.float_)
        return np.allclose(
            array,
            array.T,
            rtol=self._SYMMETRY_RTOL,
            atol=self._SYMMETRY_ATOL,
        )

    def to_float(self) -> Iterable[Iterable[float]]:
        """Get this matrix as floating-point numbers.

        Returns
        -------
        Iterable[Iterable[float]]
            this matrix as floating-point numbers
        """
        return ((float(value) for value in sequence) for sequence in self)
