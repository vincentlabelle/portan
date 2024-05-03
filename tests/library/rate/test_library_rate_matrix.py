from typing import Tuple

import pytest

from portan.library.mean.sequence import MeanSequence
from portan.library.rate.matrix import RateMatrix
from portan.library.rate.sequence import RateSequence
from portan.library.scatter import CorrelationMatrix, CovarianceMatrix


class TestRateMatrixMeans:
    @pytest.mark.parametrize(
        "value",
        [
            RateSequence.from_float([]),
            RateSequence.from_float([0.01]),
            RateSequence.from_float([0.1, -0.08]),
        ],
    )
    def test_when_one(self, value: RateSequence):
        matrix = RateMatrix([value])
        result = matrix.means()
        expected = MeanSequence([value.mean()])
        assert result == expected

    @pytest.mark.parametrize(
        "values",
        [
            (
                RateSequence.from_float([]),
                RateSequence.from_float([]),
            ),
            (
                RateSequence.from_float([0.1]),
                RateSequence.from_float([-0.1]),
            ),
            (
                RateSequence.from_float([0.1, -0.08]),
                RateSequence.from_float([-0.1, 0.08]),
            ),
        ],
    )
    def test_when_multiple(self, values: Tuple[RateSequence, ...]):
        matrix = RateMatrix(values)
        result = matrix.means()
        expected = MeanSequence(value.mean() for value in matrix)
        assert result == expected


class TestRateMatrixCovariances:
    @pytest.mark.parametrize(
        "value",
        [
            RateSequence.from_float([]),
            RateSequence.from_float([0.01]),
            RateSequence.from_float([0.1, -0.08]),
        ],
    )
    def test_when_one(self, value):
        matrix = RateMatrix([value])
        result = matrix.covariances()
        expected = CovarianceMatrix.from_iterable(
            [
                (value.covariance(value),),
            ]
        )
        assert result == expected

    @pytest.mark.parametrize(
        "values",
        [
            (
                RateSequence.from_float([]),
                RateSequence.from_float([]),
            ),
            (
                RateSequence.from_float([0.1]),
                RateSequence.from_float([-0.1]),
            ),
            (
                RateSequence.from_float([0.1, -0.08]),
                RateSequence.from_float([-0.1, 0.08]),
            ),
        ],
    )
    def test_when_multiple(self, values: Tuple[RateSequence, ...]):
        matrix = RateMatrix(values)
        result = matrix.covariances()
        expected = CovarianceMatrix.from_iterable(
            [[value.covariance(other) for other in values] for value in values]
        )
        assert result == expected


class TestRateMatrixCorrelations:
    @pytest.mark.parametrize(
        "value",
        [
            RateSequence.from_float([]),
            RateSequence.from_float([0.01]),
            RateSequence.from_float([0.1, -0.08]),
        ],
    )
    def test_when_one(self, value):
        matrix = RateMatrix([value])
        result = matrix.correlations()
        expected = CorrelationMatrix.from_iterable(
            [
                (value.correlation(value),),
            ]
        )
        assert result == expected

    @pytest.mark.parametrize(
        "values",
        [
            (
                RateSequence.from_float([]),
                RateSequence.from_float([]),
            ),
            (
                RateSequence.from_float([0.1]),
                RateSequence.from_float([-0.1]),
            ),
            (
                RateSequence.from_float([0.1, -0.08]),
                RateSequence.from_float([-0.1, 0.08]),
            ),
        ],
    )
    def test_when_multiple(self, values: Tuple[RateSequence, ...]):
        matrix = RateMatrix(values)
        result = matrix.correlations()
        expected = CorrelationMatrix.from_iterable(
            [[value.correlation(other) for other in values] for value in values]
        )
        assert result == expected


class TestRateMatrixEmpty:
    @pytest.fixture(scope="class")
    def matrix(self) -> RateMatrix:
        return RateMatrix([])

    def test_means(self, matrix: RateMatrix):
        assert matrix.means() == MeanSequence([])

    def test_covariances(self, matrix: RateMatrix):
        assert matrix.covariances() == CovarianceMatrix([])

    def test_correlations(self, matrix: RateMatrix):
        assert matrix.correlations() == CorrelationMatrix([])
