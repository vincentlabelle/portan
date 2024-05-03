from typing import Iterable, Optional, SupportsFloat

import numpy as np

from ..optimisation.constraint import (
    LinearConstraints,
    LinearEqualities,
    LinearInequalities,
)
from ..optimisation.objective import QuadraticCoefficients
from ..optimisation.quadratic import QuadraticProgram
from ..rate import Rate
from ..rate.matrix import RateMatrix


class IMVOProgramFactory:
    """Interface for a factory of :py:class:`QuadraticProgram` for
    a mean-variance optimisation problem."""

    def get(
        self,
        matrix: RateMatrix,
        minimum: Rate,
    ) -> QuadraticProgram:
        """Get the :py:class:`QuadraticProgram` defining the mean-variance
        optimisation problem for `matrix` and `minimum`.

        Parameters
        ----------
        matrix
            matrix where each row represents the observations
            of a random variables
        minimum
            minimum acceptable sample expected value for the
            weighted sum of the random variables

        Raises
        ------
        ValueError
            if any value in the means of `matrix` is non-finite, or
            if any value in the covariance matrix of `matrix` is non-finite

        Returns
        -------
        QuadraticProgram
            program defining the mean-variance optimisation problem
        """
        raise NotImplementedError


class MVOProgramFactory(IMVOProgramFactory):
    """Factory of :py:class:`QuadraticProgram` for a mean-variance
    optimisation problem."""

    def __init__(self):
        self._matrix: Optional[RateMatrix] = None
        self._minimum: Optional[Rate] = None

    def get(
        self,
        matrix: RateMatrix,
        minimum: Rate,
    ) -> QuadraticProgram:
        """Get the :py:class:`QuadraticProgram` defining the mean-variance
        optimisation problem for `matrix` and `minimum`.

        Parameters
        ----------
        matrix
            matrix where each row represents the observations
            of a random variables
        minimum
            minimum acceptable sample expected value for the
            weighted sum of the random variables

        Raises
        ------
        ValueError
            if any value in the means of `matrix` is non-finite, or
            if any value in the covariance matrix of `matrix` is non-finite

        Returns
        -------
        QuadraticProgram
            program defining the mean-variance optimisation problem
        """
        self._matrix, self._minimum = matrix, minimum
        return QuadraticProgram(
            quadratic=self._get_quadratic(),
            constraints=self._get_constraints(),
        )

    def _get_quadratic(self) -> QuadraticCoefficients:
        return QuadraticCoefficients.from_float(self._matrix.covariances())

    def _get_constraints(self) -> LinearConstraints:
        return LinearConstraints(
            equalities=self._get_equalities(),
            inequalities=self._get_inequalities(),
        )

    def _get_equalities(self) -> LinearEqualities:
        return LinearEqualities.from_float(
            coefficients=[[1.0] * len(self._matrix)],
            bounds=[1.0],
        )

    def _get_inequalities(self) -> LinearInequalities:
        return LinearInequalities.from_float(
            coefficients=self._get_inequalities_coefficients(),
            bounds=self._get_inequalities_bounds(),
        )

    def _get_inequalities_coefficients(
        self,
    ) -> Iterable[Iterable[SupportsFloat]]:
        return np.vstack(
            (
                np.identity(
                    len(self._matrix),
                    dtype=np.float_,
                ),
                -np.identity(
                    len(self._matrix),
                    dtype=np.float_,
                ),
                -np.array(
                    self._matrix.means(),
                    dtype=np.float_,
                ),
            )
        )

    def _get_inequalities_bounds(self) -> Iterable[SupportsFloat]:
        return np.concatenate(
            (
                np.ones(len(self._matrix), dtype=np.float_),
                -np.zeros(len(self._matrix), dtype=np.float_),
                -np.array([self._minimum], dtype=np.float_),
            )
        )
