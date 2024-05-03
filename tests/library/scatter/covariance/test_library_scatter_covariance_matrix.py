from math import inf, nan
from typing import Tuple

import pytest

from portan.library.scatter import (
    Covariance,
    CovarianceMatrix,
    CovarianceSequence,
    Variance,
)


class TestCorrelationMatrixInvariants:
    @pytest.mark.parametrize(
        "values",
        [
            (),
            (CovarianceSequence.from_float([0.01]),),
            (
                CovarianceSequence.from_float([0.01, 0.02]),
                CovarianceSequence.from_float([0.02, 0.04]),
            ),
            (
                CovarianceSequence.from_float([0.01, 0.02 + 2e-10]),
                CovarianceSequence.from_float([0.02, 0.04]),
            ),
            (
                CovarianceSequence.from_float([0.01, 0.02 - 2e-10]),
                CovarianceSequence.from_float([0.02, 0.04]),
            ),
        ],
    )
    def test_when_symmetrical(self, values: Tuple[CovarianceSequence, ...]):
        CovarianceMatrix(values)  # does not raise

    @pytest.mark.parametrize(
        "values",
        [
            (
                CovarianceSequence.from_float([0.01, 0.02]),
                CovarianceSequence.from_float([0.03, 0.04]),
            ),
            (
                CovarianceSequence.from_float([0.01, 0.02, 0.03]),
                CovarianceSequence.from_float([0.03, 0.04, 0.05]),
                CovarianceSequence.from_float([0.03, 0.06, 0.08]),
            ),
            (
                CovarianceSequence.from_float([0.01, 0.02 + 1e-9]),
                CovarianceSequence.from_float([0.02, 0.04]),
            ),
            (
                CovarianceSequence.from_float([0.01, 0.02 - 1e-9]),
                CovarianceSequence.from_float([0.02, 0.04]),
            ),
        ],
    )
    def test_when_asymmetrical(self, values: Tuple[CovarianceSequence, ...]):
        with pytest.raises(ValueError, match="symmetric"):
            CovarianceMatrix(values)


class TestCovarianceMatrixAlternativeConstructors:
    @pytest.mark.parametrize(
        "values",
        [
            ((Covariance(2.0),),),
            (
                (Covariance(2.0), Covariance(4.0)),
                (Covariance(4.0), Covariance(1.0)),
            ),
        ],
    )
    def test_from_iterable(self, values: Tuple[Tuple[Covariance, ...], ...]):
        result = CovarianceMatrix.from_iterable(values)
        expected = CovarianceMatrix(
            CovarianceSequence(value) for value in values
        )
        assert result == expected


class TestCovarianceMatrixVariance:
    @pytest.fixture(scope="class")
    def matrix(self) -> CovarianceMatrix:
        return CovarianceMatrix.from_iterable(
            [
                (Covariance(2.0), Covariance(4.0)),
                (Covariance(4.0), Covariance(1.0)),
            ]
        )

    @pytest.mark.parametrize("factors", [(1.0,), (1.0, 2.0, 3.0)])
    def test_when_factors_length_mismatch(
        self,
        matrix: CovarianceMatrix,
        factors: Tuple[float, ...],
    ):
        with pytest.raises(ValueError, match="length of factors"):
            matrix.variance(factors)

    def test_when_nan_factors(self, matrix: CovarianceMatrix):
        factors = (1.0, nan)
        with pytest.raises(ValueError, match="must not be NaN"):
            matrix.variance(factors)

    def test_when_one(self):
        matrix = CovarianceMatrix.from_iterable(
            [
                (Covariance(2.0),),
            ]
        )
        factors = (4.0,)
        result = matrix.variance(factors)
        expected = Variance(32.0)
        assert result == expected

    def test_when_multiple(self, matrix: CovarianceMatrix):
        factors = (3.0, 2.0)
        result = matrix.variance(factors)
        expected = Variance(70.0)
        assert result == expected

    def test_when_inf(self, matrix: CovarianceMatrix):
        factors = (inf, 2.0)
        result = matrix.variance(factors)
        expected = Variance(inf)
        assert result == expected

    def test_when_negative(self):
        matrix = CovarianceMatrix.from_iterable(
            [
                (Covariance(2.0), Covariance(-4.0)),
                (Covariance(-4.0), Covariance(1.0)),
            ]
        )
        factors = (3.0, 2.0)
        with pytest.raises(ValueError, match="must be non-negative"):
            matrix.variance(factors)


class TestCovarianceMatrixEmpty:
    @pytest.fixture(scope="class")
    def matrix(self) -> CovarianceMatrix:
        return CovarianceMatrix([])

    def test_from_iterable(self, matrix: CovarianceMatrix):
        other = CovarianceMatrix.from_iterable([])
        assert other == matrix

    def test_variance(self, matrix: CovarianceMatrix):
        assert matrix.variance([]) == Variance(0.0)
