from typing import Tuple

import pytest

from portan.library.price.matrix import PriceMatrix
from portan.library.price.sequence import PriceSequence
from portan.library.rate.matrix import RateMatrix


class TestPriceMatrixAlternativeConstructors:
    @pytest.fixture(
        scope="class",
        params=[
            ((1.0, 2.0), (3.0, 4.0)),
            ((), ()),
        ],
    )
    def values(self, request) -> Tuple[Tuple[float, ...], ...]:
        return request.param

    @pytest.fixture(scope="class")
    def matrix(self, values: Tuple[Tuple[float, ...], ...]) -> PriceMatrix:
        return PriceMatrix(PriceSequence.from_float(value) for value in values)

    def test_from_float(
        self,
        matrix: PriceMatrix,
        values: Tuple[Tuple[float, ...], ...],
    ):
        result = PriceMatrix.from_float(values)
        assert result == matrix

    def test_from_float_supports_float(self, matrix: PriceMatrix):
        result = PriceMatrix.from_float([*matrix])
        assert result == matrix

    def test_empties_when_length_is_negative(self):
        with pytest.raises(ValueError, match="non-negative"):
            PriceMatrix.empties(-1)

    @pytest.mark.parametrize("length", [1, 2])
    def test_empties_when_length_is_non_negative(self, length: int):
        result = PriceMatrix.empties(length)
        expected = PriceMatrix(PriceSequence([]) for _ in range(length))
        assert result == expected


class TestPriceMatrixGrowth:
    @pytest.mark.parametrize(
        "value",
        [
            PriceSequence([]),
            PriceSequence.from_float([1.0]),
            PriceSequence.from_float([2.0, 4.0]),
        ],
    )
    def test_when_one(self, value: PriceSequence):
        matrix = PriceMatrix([value])
        result = matrix.growth()
        expected = RateMatrix([value.growth()])
        assert result == expected

    @pytest.mark.parametrize(
        "values",
        [
            (
                PriceSequence([]),
                PriceSequence([]),
            ),
            (
                PriceSequence.from_float([1.0]),
                PriceSequence.from_float([2.0]),
            ),
            (
                PriceSequence.from_float([1.0, 4.0]),
                PriceSequence.from_float([2.0, 5.0]),
            ),
        ],
    )
    def test_when_multiple(self, values: Tuple[PriceSequence, ...]):
        matrix = PriceMatrix(values)
        result = matrix.growth()
        expected = RateMatrix(value.growth() for value in values)
        assert result == expected


class TestPriceMatrixEmpty:
    @pytest.fixture(scope="class")
    def matrix(self) -> PriceMatrix:
        return PriceMatrix([])

    def test_from_float(self, matrix: PriceMatrix):
        assert PriceMatrix.from_float([]) == matrix

    def test_empties(self, matrix: PriceMatrix):
        assert PriceMatrix.empties(0) == matrix

    def test_growth(self, matrix: PriceMatrix):
        assert matrix.growth() == RateMatrix([])
