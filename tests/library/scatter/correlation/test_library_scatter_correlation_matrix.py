from typing import Tuple

import pytest

from portan.library.scatter.correlation import Correlation
from portan.library.scatter.correlation.matrix import CorrelationMatrix
from portan.library.scatter.correlation.sequence import CorrelationSequence


class TestCorrelationMatrixInvariants:
    @pytest.mark.parametrize(
        "values",
        [
            (),
            (CorrelationSequence.from_float([0.01]),),
            (
                CorrelationSequence.from_float([0.01, 0.02]),
                CorrelationSequence.from_float([0.02, 0.04]),
            ),
            (
                CorrelationSequence.from_float([0.01, 0.02 + 2e-10]),
                CorrelationSequence.from_float([0.02, 0.04]),
            ),
            (
                CorrelationSequence.from_float([0.01, 0.02 - 2e-10]),
                CorrelationSequence.from_float([0.02, 0.04]),
            ),
        ],
    )
    def test_when_symmetrical(self, values: Tuple[CorrelationSequence, ...]):
        CorrelationMatrix(values)  # does not raise

    @pytest.mark.parametrize(
        "values",
        [
            (
                CorrelationSequence.from_float([0.01, 0.02]),
                CorrelationSequence.from_float([0.03, 0.04]),
            ),
            (
                CorrelationSequence.from_float([0.01, 0.02, 0.03]),
                CorrelationSequence.from_float([0.03, 0.04, 0.05]),
                CorrelationSequence.from_float([0.03, 0.06, 0.08]),
            ),
            (
                CorrelationSequence.from_float([0.01, 0.02 + 1e-9]),
                CorrelationSequence.from_float([0.02, 0.04]),
            ),
            (
                CorrelationSequence.from_float([0.01, 0.02 - 1e-9]),
                CorrelationSequence.from_float([0.02, 0.04]),
            ),
        ],
    )
    def test_when_asymmetrical(self, values: Tuple[CorrelationSequence, ...]):
        with pytest.raises(ValueError, match="symmetric"):
            CorrelationMatrix(values)


class TestCorrelationMatrixAlternativeConstructors:
    @pytest.mark.parametrize(
        "values",
        [
            ((Correlation(1.0),),),
            (
                (Correlation(1.0), Correlation(-1.0)),
                (Correlation(-1.0), Correlation(0.5)),
            ),
        ],
    )
    def test_from_iterable(self, values: Tuple[Tuple[Correlation, ...], ...]):
        result = CorrelationMatrix.from_iterable(values)
        expected = CorrelationMatrix(
            CorrelationSequence(value) for value in values
        )
        assert result == expected


class TestCorrelationMatrixToFloat:
    def test(self):
        matrix = CorrelationMatrix(
            [
                CorrelationSequence(
                    [
                        Correlation(1.0),
                        Correlation(-1.0),
                    ]
                ),
                CorrelationSequence(
                    [
                        Correlation(-1.0),
                        Correlation(0.5),
                    ]
                ),
            ]
        )
        result = self._to_float_as_tuples(matrix)
        expected = (
            (1.0, -1.0),
            (-1.0, 0.5),
        )
        assert result == expected

    @staticmethod
    def _to_float_as_tuples(matrix: CorrelationMatrix):
        return tuple(map(lambda x: tuple(x), matrix.to_float()))


class TestCorrelationMatrixEmpty:
    @pytest.fixture(scope="class")
    def matrix(self) -> CorrelationMatrix:
        return CorrelationMatrix([])

    def test_from_iterable(self, matrix: CorrelationMatrix):
        assert CorrelationMatrix.from_iterable([]) == matrix

    def test_to_float(self, matrix: CorrelationMatrix):
        assert tuple(matrix.to_float()) == ()
