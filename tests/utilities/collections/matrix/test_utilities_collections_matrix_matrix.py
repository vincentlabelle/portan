from typing import Tuple

import pytest

from portan.utilities.collections import Matrix, Sequence


class TestMatrixInvariants:
    @pytest.mark.parametrize(
        "sequence",
        [
            Sequence([0.03]),
            Sequence([0.03, 0.04, 0.07]),
        ],
    )
    def test_when_length_mismatch(self, sequence: Sequence):
        values = (
            Sequence([0.01, 0.02]),
            sequence,
            Sequence([0.05, 0.06]),
        )
        with pytest.raises(ValueError, match="same length"):
            Matrix(values)

    def test_when_length_match(self):
        values = (
            Sequence([0.01, 0.02]),
            Sequence([0.03, 0.04]),
            Sequence([0.05, 0.06]),
        )
        Matrix(values)  # does not raise

    def test_when_empty(self):
        Matrix([])  # does not raise


class TestMatrixProperties:
    @pytest.fixture(scope="class")
    def values(self) -> Tuple[Sequence, ...]:
        return Sequence([0.01, 0.02]), Sequence([0.03, 0.04])

    @pytest.fixture(scope="class")
    def matrix(self, values: Tuple[Sequence, ...]) -> Matrix:
        return Matrix(values)

    def test_nrows(self, matrix: Matrix, values: Tuple[Sequence, ...]):
        assert matrix.nrows == len(values)

    def test_set_nrows(self, matrix: Matrix):
        with pytest.raises(AttributeError):
            matrix.nrows = 2

    def test_ncols(self, matrix: Matrix, values: Tuple[Sequence, ...]):
        assert matrix.ncols == len(values[0])

    def test_set_ncols(self, matrix: Matrix):
        with pytest.raises(AttributeError):
            matrix.ncols = 2


class TestMatrixIsEmpty:
    def test_when_empty(self):
        matrix = Matrix([])
        assert matrix.is_empty()

    @pytest.mark.parametrize(
        "values",
        [
            (Sequence([]),),
            (Sequence([0.01]),),
            (Sequence([0.01]), Sequence([0.02])),
        ],
    )
    def test_when_non_empty(self, values: Tuple[Sequence, ...]):
        matrix = Matrix(values)
        assert not matrix.is_empty()


class TestMatrixTranspose:
    @pytest.mark.parametrize(
        "values, e_values",
        [
            (
                (Sequence([]),),
                (),
            ),
            (
                (Sequence([0.01]),),
                (Sequence([0.01]),),
            ),
            (
                (Sequence([0.01, 0.02]),),
                (Sequence([0.01]), Sequence([0.02])),
            ),
        ],
    )
    def test_when_one(
        self,
        values: Tuple[Sequence, ...],
        e_values: Tuple[Sequence, ...],
    ):
        matrix = Matrix(values)
        expected = Matrix(e_values)
        assert matrix.transpose() == expected

    @pytest.mark.parametrize(
        "values, e_values",
        [
            (
                (
                    Sequence([]),
                    Sequence([]),
                ),
                (),
            ),
            (
                (
                    Sequence([0.01]),
                    Sequence([0.02]),
                ),
                (Sequence([0.01, 0.02]),),
            ),
            (
                (
                    Sequence([0.01, 0.02]),
                    Sequence([0.03, 0.04]),
                ),
                (
                    Sequence([0.01, 0.03]),
                    Sequence([0.02, 0.04]),
                ),
            ),
        ],
    )
    def test_when_multiple(
        self,
        values: Tuple[Sequence, ...],
        e_values: Tuple[Sequence, ...],
    ):
        matrix = Matrix(values)
        expected = Matrix(e_values)
        assert matrix.transpose() == expected


class TestMatrixEmpty:
    @pytest.fixture(scope="class")
    def matrix(self) -> Matrix:
        return Matrix([])

    def test_nrows(self, matrix: Matrix):
        assert matrix.nrows == 0

    def test_ncols(self, matrix: Matrix):
        assert matrix.ncols == 0

    def test_transpose(self, matrix: Matrix):
        assert matrix.transpose() == matrix
