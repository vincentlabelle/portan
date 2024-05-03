from typing import Tuple

import pytest

from portan.utilities.collections import Sequence, SquareMatrix


class TestSquareMatrixInvariants:
    def test_when_is_not_square(self):
        with pytest.raises(ValueError, match="length of each value"):
            SquareMatrix([Sequence([])])

    @pytest.mark.parametrize(
        "values",
        [
            (Sequence([0.01]),),
            (
                Sequence([0.01, 0.02]),
                Sequence([0.03, 0.04]),
            ),
        ],
    )
    def test_when_is_square(self, values: Tuple[Sequence, ...]):
        SquareMatrix(values)  # does not raise


class TestSquareMatrixIsSymmetric:
    @pytest.mark.parametrize(
        "values",
        [
            (Sequence([0.01]),),
            (
                Sequence([0.01, 0.02]),
                Sequence([0.02, 0.04]),
            ),
        ],
    )
    def test_when_symmetrical(self, values: Tuple[Sequence, ...]):
        matrix = SquareMatrix(values)
        assert matrix.is_symmetric()

    @pytest.mark.parametrize(
        "values",
        [
            (
                Sequence([0.01, 0.02]),
                Sequence([0.03, 0.04]),
            ),
            (
                Sequence([0.01, 0.02, 0.03]),
                Sequence([0.03, 0.04, 0.05]),
                Sequence([0.03, 0.06, 0.08]),
            ),
        ],
    )
    def test_when_asymmetrical(self, values: Tuple[Sequence, ...]):
        matrix = SquareMatrix(values)
        assert not matrix.is_symmetric()


class TestSquareMatrixEmpty:
    @pytest.fixture(scope="class")
    def matrix(self) -> SquareMatrix:
        return SquareMatrix([])

    def test_is_symmetric(self, matrix: SquareMatrix):
        assert matrix.is_symmetric()
