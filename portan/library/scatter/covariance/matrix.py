from math import isnan
from typing import Iterable, SupportsFloat, Tuple, Type, TypeVar

import numpy as np

from portan.utilities.collections import SymmetricMatrix

from .covariance import Covariance
from .sequence import CovarianceSequence
from .variance import Variance

T = TypeVar("T", bound="CovarianceMatrix")


class CovarianceMatrix(SymmetricMatrix[CovarianceSequence]):
    """Immutable symmetric matrix of covariances."""

    _SYMMETRY_RTOL: float = 1e-8
    _SYMMETRY_ATOL: float = 1e-12

    @classmethod
    def from_iterable(
        cls: Type[T],
        values: Iterable[Iterable[Covariance]],
    ) -> T:
        """Create a matrix from iterables of covariances.

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
            matrix of covariances
        """
        return cls(CovarianceSequence(value) for value in values)

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

    def variance(self, factors: Iterable[SupportsFloat]) -> Covariance:
        """Get the variance of the sum of the scaled random variables
        where each random variable is scaled by its corresponding factor
        in `factors` (i.e., Var[sum(f_i * X_i)]).

        Parameters
        ----------
        factors
            factors to scale the random variables by

        Raises
        ------
        ValueError
            if the length of `factors` does not equal this matrix number of
            rows(columns),
            if any factor in `factors` is nan, or
            if the variance is negative (shouldn't happen in practice!)

        Returns
        -------
        Variance
            variance of the sum of the scaled random variables
        """
        factors_ = tuple(factors)  # freeze!
        self._raise_if_length_mismatch_with_factors(factors_)
        self._raise_if_any_factor_is_nan(factors_)
        return Variance(self._variance(factors_))

    def _raise_if_length_mismatch_with_factors(
        self,
        factors: Tuple[SupportsFloat, ...],
    ):
        if len(self) != len(factors):
            msg = (
                "cannot determine variance; length of factors must "
                "be equal to this matrix length (i.e., number of rows)"
            )
            raise ValueError(msg)

    @staticmethod
    def _raise_if_any_factor_is_nan(
        factors: Tuple[SupportsFloat, ...],
    ):
        if any(isnan(factor) for factor in factors):
            msg = "cannot determine variance; factors must not be NaN"
            raise ValueError(msg)

    def _variance(self, factors: Tuple[SupportsFloat, ...]) -> float:
        return sum(
            [
                value * float(factor)
                for value, factor in zip(
                    [
                        sum(
                            [
                                float(value) * float(factor)
                                for value, factor in zip(sequence, factors)
                            ]
                        )
                        for sequence in self
                    ],
                    factors,
                )
            ]
        )  # f * C * f^T
