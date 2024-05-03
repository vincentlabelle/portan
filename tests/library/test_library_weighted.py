from math import isclose
from typing import Tuple

import pytest

from portan.library.mean import Mean
from portan.library.rate.matrix import RateMatrix
from portan.library.rate.sequence import RateSequence
from portan.library.scatter import Dispersion
from portan.library.weight.sequence import WeightSequence
from portan.library.weighted import Weighted


class TestWeightedInvariants:
    @pytest.mark.parametrize(
        "weights",
        [
            WeightSequence.from_int([100]),
            WeightSequence.from_int([33, 33, 34]),
        ],
    )
    def test_when_length_mismatch(self, weights: WeightSequence):
        rates = RateMatrix(
            [
                RateSequence.from_float([0.01, 0.03]),
                RateSequence.from_float([0.03, 0.02]),
            ]
        )
        with pytest.raises(ValueError, match="length of arguments"):
            Weighted(weights, rates)

    def test_when_length_match(self):
        weights = WeightSequence.from_int([50, 50])
        rates = RateMatrix(
            [
                RateSequence.from_float([0.01, 0.03]),
                RateSequence.from_float([0.03, 0.02]),
            ]
        )
        Weighted(weights, rates)  # does not raise


class TestWeightedAlternativeConstructors:
    def test_empty(self):
        result = Weighted.empty()
        expected = Weighted(WeightSequence([]), RateMatrix([]))
        assert result == expected


@pytest.fixture(scope="module")
def weights() -> WeightSequence:
    return WeightSequence.from_int([50, 50])


@pytest.fixture(scope="module")
def rates() -> RateMatrix:
    return RateMatrix(
        [
            RateSequence.from_float([0.01]),
            RateSequence.from_float([0.02]),
        ]
    )


@pytest.fixture(scope="module")
def weighted(weights: WeightSequence, rates: RateMatrix) -> Weighted:
    return Weighted(weights, rates)


class TestWeightedStringRepresentation:
    def test_str(
        self,
        weighted: Weighted,
        weights: WeightSequence,
        rates: RateMatrix,
    ):
        expected = f"(weights={weights}, rates={rates})"
        assert str(weighted) == expected

    def test_repr(self, weighted: Weighted):
        assert repr(weighted) == f"<{weighted.__class__.__name__}{weighted}>"


class TestWeightedEqual:
    def test_when_equal(
        self,
        weighted: Weighted,
        weights: WeightSequence,
        rates: RateMatrix,
    ):
        other = Weighted(weights, rates)
        assert other == weighted

    def test_when_different_weights(
        self,
        weighted: Weighted,
        rates: RateMatrix,
    ):
        weights = WeightSequence.from_int([0] * len(rates))
        other = Weighted(weights, rates)
        assert other != weighted

    def test_when_different_rates(
        self,
        weighted: Weighted,
        weights: WeightSequence,
    ):
        rates = RateMatrix([RateSequence([])] * len(weights))
        other = Weighted(weights, rates)
        assert other != weighted

    def test_when_different_object(self, weighted):
        assert weighted != "a"


class TestWeightedHash:
    def test_when_equal(
        self,
        weighted: Weighted,
        weights: WeightSequence,
        rates: RateMatrix,
    ):
        other = Weighted(weights, rates)
        assert hash(other) == hash(weighted)

    def test_when_different_weights(
        self,
        weighted: Weighted,
        rates: RateMatrix,
    ):
        weights = WeightSequence.from_int([0] * len(rates))
        other = Weighted(weights, rates)
        assert hash(other) != hash(weighted)

    def test_when_different_rates(
        self,
        weighted: Weighted,
        weights: WeightSequence,
    ):
        rates = RateMatrix([RateSequence([])] * len(weights))
        other = Weighted(weights, rates)
        assert hash(other) != hash(weighted)


class TestWeightedMean:
    def test_when_empty(self):
        weighted = Weighted(
            WeightSequence([]),
            RateMatrix([]),
        )
        result = weighted.mean()
        assert result == Mean(0.0)

    @pytest.mark.parametrize(
        "sequence, expected",
        [
            (RateSequence([]), Mean(0.0)),
            (RateSequence.from_float([0.01]), Mean(0.005)),
            (RateSequence.from_float([0.01, 0.04]), Mean(0.0125)),
        ],
    )
    def test_when_one(self, sequence: RateSequence, expected: Mean):
        weighted = Weighted(
            WeightSequence.from_int([50]),
            RateMatrix([sequence]),
        )
        result = weighted.mean()
        assert result == expected

    @pytest.mark.parametrize(
        "sequences, expected",
        [
            (
                (
                    RateSequence([]),
                    RateSequence([]),
                ),
                Mean(0.0),
            ),
            (
                (
                    RateSequence.from_float([0.01]),
                    RateSequence.from_float([0.04]),
                ),
                Mean(0.025),
            ),
            (
                (
                    RateSequence.from_float([0.01, 0.04]),
                    RateSequence.from_float([0.04, 0.02]),
                ),
                Mean(0.0275),
            ),
        ],
    )
    def test_when_multiple(
        self,
        sequences: Tuple[RateSequence, ...],
        expected: Mean,
    ):

        weighted = Weighted(
            WeightSequence.from_int([50, 50]),
            RateMatrix(sequences),
        )
        result = weighted.mean()
        assert result == expected


class TestWeightedDispersion:
    @pytest.fixture(scope="class")
    def absolute_tolerance(self) -> float:
        return 1e-8

    @pytest.fixture(scope="class")
    def relative_tolerance(self) -> float:
        return 1e-8

    def test_when_empty(self):
        weighted = Weighted(
            WeightSequence([]),
            RateMatrix([]),
        )
        result = weighted.dispersion()
        assert result == Dispersion(0.0)

    @pytest.mark.parametrize(
        "sequence, expected",
        [
            (
                RateSequence([]),
                Dispersion(0.0),
            ),
            (
                RateSequence.from_float([0.01]),
                Dispersion(0.0),
            ),
            (
                RateSequence.from_float([0.01, 0.04]),
                Dispersion(0.010606602),
            ),
        ],
    )
    def test_when_one(
        self,
        sequence: RateSequence,
        expected: Dispersion,
        absolute_tolerance: float,
        relative_tolerance: float,
    ):
        weighted = Weighted(
            WeightSequence.from_int([50]),
            RateMatrix([sequence]),
        )
        result = weighted.dispersion()
        assert isclose(
            result,
            expected,
            abs_tol=absolute_tolerance,
            rel_tol=relative_tolerance,
        )

    @pytest.mark.parametrize(
        "sequences, expected",
        [
            (
                (
                    RateSequence([]),
                    RateSequence([]),
                ),
                Dispersion(0.0),
            ),
            (
                (
                    RateSequence.from_float([0.01]),
                    RateSequence.from_float([0.04]),
                ),
                Dispersion(0.0),
            ),
            (
                (
                    RateSequence.from_float([0.01, 0.04]),
                    RateSequence.from_float([0.04, 0.02]),
                ),
                Dispersion(0.003535534),
            ),
        ],
    )
    def test_when_multiple(
        self,
        sequences: Tuple[RateSequence, ...],
        expected: Dispersion,
        absolute_tolerance: float,
        relative_tolerance: float,
    ):

        weighted = Weighted(
            WeightSequence.from_int([50, 50]),
            RateMatrix(sequences),
        )
        result = weighted.dispersion()
        assert isclose(
            result,
            expected,
            abs_tol=absolute_tolerance,
            rel_tol=relative_tolerance,
        )
