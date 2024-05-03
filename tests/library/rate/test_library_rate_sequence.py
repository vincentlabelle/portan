from math import isclose
from typing import Tuple

import pytest

from portan.library.mean import Mean
from portan.library.rate import Rate
from portan.library.rate.sequence import RateSequence
from portan.library.scatter import Correlation, Covariance, Dispersion


class TestRateSequenceAlternativeConstructors:
    @pytest.fixture(scope="class")
    def values(self) -> Tuple[Rate, ...]:
        return (
            Rate(0.0),
            Rate(1.0),
            Rate(2.0),
        )

    @pytest.fixture(scope="class")
    def sequence(self, values: Tuple[Rate, ...]) -> RateSequence:
        return RateSequence(values)

    def test_from_float(
        self,
        sequence: RateSequence,
        values: Tuple[Rate, ...],
    ):
        result = RateSequence.from_float(float(value) for value in values)
        assert result == sequence

    def test_from_float_when_supports_float(
        self,
        sequence: RateSequence,
        values: Tuple[Rate, ...],
    ):
        result = RateSequence.from_float(value for value in values)
        assert result == sequence


class TestRateSequenceMean:
    def test_when_one(self):
        value = Rate(0.01)
        sequence = RateSequence([value])
        result = sequence.mean()
        assert result == Mean(value)

    def test_when_multiple(self):
        sequence = RateSequence(
            [
                Rate(0.01),
                Rate(0.02),
                Rate(0.03),
            ]
        )
        result = sequence.mean()
        expected = Mean(
            sum([float(value) for value in sequence]) / len(sequence)
        )
        assert result == expected


class TestRateSequenceDispersion:
    @pytest.fixture(scope="class")
    def absolute_tolerance(self) -> float:
        return 1e-12

    @pytest.fixture(scope="class")
    def relative_tolerance(self) -> float:
        return 0.0

    def test_when_one(self):
        sequence = RateSequence.from_float([0.01])
        assert sequence.dispersion() == Dispersion(0.0)

    def test_when_multiple(
        self,
        absolute_tolerance: float,
        relative_tolerance: float,
    ):
        sequence = RateSequence(
            [
                Rate(0.01),
                Rate(0.02),
                Rate(0.03),
            ]
        )
        result = sequence.dispersion()
        expected = self._get_sample_dispersion(sequence)
        assert isclose(
            result,
            expected,
            abs_tol=absolute_tolerance,
            rel_tol=relative_tolerance,
        )

    @staticmethod
    def _get_sample_dispersion(sequence: RateSequence) -> Dispersion:
        return Dispersion(
            (
                sum(
                    [
                        (float(value) - float(sequence.mean())) ** 2
                        for value in sequence
                    ]
                )
                / (len(sequence) - 1)
            )
            ** 0.5
        )


class TestRateSequenceCorrelation:
    @pytest.fixture(scope="class")
    def absolute_tolerance(self) -> float:
        return 1e-12

    @pytest.fixture(scope="class")
    def relative_tolerance(self) -> float:
        return 0.0

    @pytest.mark.parametrize(
        "other",
        [
            RateSequence(
                [
                    Rate(0.01),
                ]
            ),
            RateSequence(
                [
                    Rate(0.01),
                    Rate(0.02),
                    Rate(0.03),
                ]
            ),
        ],
    )
    def test_when_length_mismatch(self, other: RateSequence):
        sequence = RateSequence(
            [
                Rate(0.01),
                Rate(0.02),
            ]
        )
        with pytest.raises(ValueError, match="length of other"):
            sequence.correlation(other)

    @pytest.mark.parametrize(
        "value",
        [
            Rate(0.01),
            Rate(0.02),
        ],
    )
    def test_when_one(self, value: Rate):
        sequence = RateSequence([Rate(0.01)])
        other = RateSequence([value])
        assert sequence.correlation(other) == Correlation(0.0)

    def test_when_multiple(
        self,
        absolute_tolerance: float,
        relative_tolerance: float,
    ):
        sequence = RateSequence(
            [
                Rate(0.01),
                Rate(0.02),
                Rate(0.03),
            ]
        )
        other = RateSequence(
            [
                Rate(0.04),
                Rate(0.06),
                Rate(0.05),
            ]
        )
        result = sequence.correlation(other)
        expected = self._get_sample_correlation(sequence, other)
        assert isclose(
            result,
            expected,
            abs_tol=absolute_tolerance,
            rel_tol=relative_tolerance,
        )

    @staticmethod
    def _get_sample_correlation(
        sequence: RateSequence,
        other: RateSequence,
    ) -> Correlation:
        return Correlation(
            float(sequence.covariance(other))
            / float(sequence.dispersion())
            / float(other.dispersion())
        )


class TestRateSequenceCovariance:
    @pytest.fixture(scope="class")
    def absolute_tolerance(self) -> float:
        return 1e-12

    @pytest.fixture(scope="class")
    def relative_tolerance(self) -> float:
        return 0.0

    @pytest.mark.parametrize(
        "other",
        [
            RateSequence(
                [
                    Rate(0.01),
                ]
            ),
            RateSequence(
                [
                    Rate(0.01),
                    Rate(0.02),
                    Rate(0.03),
                ]
            ),
        ],
    )
    def test_when_length_mismatch(self, other: RateSequence):
        sequence = RateSequence(
            [
                Rate(0.01),
                Rate(0.02),
            ]
        )
        with pytest.raises(ValueError, match="length of other"):
            sequence.covariance(other)

    def test_when_one(self):
        sequence = RateSequence([Rate(0.01)])
        other = RateSequence([Rate(0.02)])
        assert sequence.covariance(other) == Covariance(0.0)

    def test_when_multiple(
        self,
        absolute_tolerance: float,
        relative_tolerance: float,
    ):
        sequence = RateSequence(
            [
                Rate(0.01),
                Rate(0.02),
                Rate(0.03),
            ]
        )
        other = RateSequence(
            [
                Rate(0.04),
                Rate(0.05),
                Rate(0.06),
            ]
        )
        result = sequence.covariance(other)
        expected = self._get_sample_covariance(sequence, other)
        assert isclose(
            result,
            expected,
            abs_tol=absolute_tolerance,
            rel_tol=relative_tolerance,
        )

    @staticmethod
    def _get_sample_covariance(
        sequence: RateSequence,
        other: RateSequence,
    ) -> Covariance:
        return Covariance(
            sum(
                [
                    (float(s) - float(sequence.mean()))
                    * (float(o) - float(other.mean()))
                    for s, o in zip(sequence, other)
                ]
            )
            / (len(sequence) - 1)
        )


class TestRateSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> RateSequence:
        return RateSequence([])

    def test_from_float(self, sequence: RateSequence):
        assert RateSequence.from_float([]) == sequence

    def test_mean(self, sequence: RateSequence):
        assert sequence.mean() == Mean(0.0)

    def test_dispersion(self, sequence: RateSequence):
        assert sequence.dispersion() == Dispersion(0.0)

    def test_correlation(self, sequence: RateSequence):
        assert sequence.correlation(sequence) == Correlation(0.0)

    def test_covariance(self, sequence: RateSequence):
        assert sequence.covariance(sequence) == Covariance(0.0)
