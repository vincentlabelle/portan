from typing import Iterable, SupportsFloat, Type, TypeVar

import numpy as np

from portan.utilities.collections import Matrix, SymmetricMatrix

from .sequence import CoefficientSequence


class CoefficientMatrix(Matrix[CoefficientSequence]):
    """Immutable matrix of coefficients."""

    pass


S = TypeVar("S", bound="SymmetricCoefficientMatrix")


class SymmetricCoefficientMatrix(SymmetricMatrix[CoefficientSequence]):
    """Immutable symmetric matrix of coefficients"""

    _SYMMETRY_RTOL: float = 1e-8
    _SYMMETRY_ATOL: float = 1e-12

    @classmethod
    def from_float(
        cls: Type[S],
        values: Iterable[Iterable[SupportsFloat]],
    ) -> S:
        """Create a matrix from floating-point numbers.

        Parameters
        ----------
        values
            values to create the matrix from

        Raises
        ------
        ValueError
            if any floating-point number in `values` is not finite,
            if the iterables in `values` are not all of the same length,
            if the length of each iterable in `values` is not equal to
            the number of iterables in `values`, or
            if the values in `values` do not form a symmetric matrix

        Returns
        -------
        S
            coefficient matrix
        """
        return cls(CoefficientSequence.from_float(value) for value in values)

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
