from typing import Tuple

import pytest

from portan.library.optimisation.coefficient.matrix import (
    SymmetricCoefficientMatrix,
)
from portan.library.optimisation.coefficient.sequence import CoefficientSequence


class TestSymmetricCoefficientMatrixInvariants:
    @pytest.mark.parametrize(
        "values",
        [
            (),
            (CoefficientSequence.from_float([0.01]),),
            (
                CoefficientSequence.from_float([0.01, 0.02]),
                CoefficientSequence.from_float([0.02, 0.04]),
            ),
            (
                CoefficientSequence.from_float([0.01, 0.02 + 2e-10]),
                CoefficientSequence.from_float([0.02, 0.04]),
            ),
            (
                CoefficientSequence.from_float([0.01, 0.02 - 2e-10]),
                CoefficientSequence.from_float([0.02, 0.04]),
            ),
        ],
    )
    def test_when_symmetrical(self, values: Tuple[CoefficientSequence, ...]):
        SymmetricCoefficientMatrix(values)  # does not raise

    @pytest.mark.parametrize(
        "values",
        [
            (
                CoefficientSequence.from_float([0.01, 0.02]),
                CoefficientSequence.from_float([0.03, 0.04]),
            ),
            (
                CoefficientSequence.from_float([0.01, 0.02, 0.03]),
                CoefficientSequence.from_float([0.03, 0.04, 0.05]),
                CoefficientSequence.from_float([0.03, 0.06, 0.08]),
            ),
            (
                CoefficientSequence.from_float([0.01, 0.02 + 1e-9]),
                CoefficientSequence.from_float([0.02, 0.04]),
            ),
            (
                CoefficientSequence.from_float([0.01, 0.02 - 1e-9]),
                CoefficientSequence.from_float([0.02, 0.04]),
            ),
        ],
    )
    def test_when_asymmetrical(self, values: Tuple[CoefficientSequence, ...]):
        with pytest.raises(ValueError, match="symmetric"):
            SymmetricCoefficientMatrix(values)


class TestSymmetricCoefficientMatrixAlternativeConstructors:
    @pytest.fixture(scope="class")
    def matrix(self) -> SymmetricCoefficientMatrix:
        return SymmetricCoefficientMatrix(
            [
                CoefficientSequence.from_float([1.0, 2.0]),
                CoefficientSequence.from_float([2.0, 4.0]),
            ]
        )

    def test_from_float(self, matrix: SymmetricCoefficientMatrix):
        result = SymmetricCoefficientMatrix.from_float(
            (float(value) for value in sequence) for sequence in matrix
        )
        assert result == matrix

    def test_from_float_supports_float(
        self,
        matrix: SymmetricCoefficientMatrix,
    ):
        result = SymmetricCoefficientMatrix.from_float(matrix)
        assert result == matrix


class TestSymmetricCoefficientMatrixEmpty:
    @pytest.fixture(scope="class")
    def matrix(self) -> SymmetricCoefficientMatrix:
        return SymmetricCoefficientMatrix([])

    def test_from_float(self, matrix: SymmetricCoefficientMatrix):
        assert SymmetricCoefficientMatrix.from_float([]) == matrix
