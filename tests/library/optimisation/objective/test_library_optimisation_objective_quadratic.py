import pytest

from portan.library.optimisation.coefficient.sequence import CoefficientSequence
from portan.library.optimisation.objective.quadratic import (
    QuadraticCoefficients,
)


class TestQuadraticCoefficientsProperties:
    @pytest.fixture(scope="class")
    def matrix(self) -> QuadraticCoefficients:
        return QuadraticCoefficients(
            [
                CoefficientSequence.from_float([1.0, 2.0]),
                CoefficientSequence.from_float([2.0, 4.0]),
            ]
        )

    def test_n(self, matrix: QuadraticCoefficients):
        assert matrix.n == len(matrix)

    def test_set_n(self, matrix: QuadraticCoefficients):
        with pytest.raises(AttributeError):
            matrix.n = 0


class TestQuadraticCoefficientsEmpty:
    @pytest.fixture(scope="class")
    def matrix(self) -> QuadraticCoefficients:
        return QuadraticCoefficients([])

    def test_n(self, matrix: QuadraticCoefficients):
        assert matrix.n == len(matrix)
