from typing import Tuple

import pytest

from portan.library.weight import Weight
from portan.library.weight.sequence import BalancedWeights, WeightSequence


class TestWeightSequenceAlternativeConstructors:
    def test_from_float(self):
        result = WeightSequence.from_float([0.25, 0.5, 0.4])
        expected = WeightSequence([Weight(25), Weight(50), Weight(40)])
        assert result == expected

    def test_from_float_when_supports_float(self):
        expected = WeightSequence([Weight(1), Weight(2), Weight(3)])
        result = WeightSequence.from_float(value for value in expected)
        assert result == expected

    def test_from_int(self):
        result = WeightSequence.from_int([1, 2, 3])
        expected = WeightSequence([Weight(1), Weight(2), Weight(3)])
        assert result == expected

    def test_from_int_when_supports_int(self):
        expected = WeightSequence([Weight(1), Weight(2), Weight(3)])
        result = WeightSequence.from_int(value for value in expected)
        assert result == expected


class TestWeightSequenceSum:
    def test_when_one(self):
        sequence = WeightSequence.from_int([1])
        assert sequence.sum() == Weight(1)

    def test_when_multiple(self):
        sequence = WeightSequence.from_int([1, -2, 3])
        assert sequence.sum() == Weight(2)


class TestWeightSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> WeightSequence:
        return WeightSequence([])

    def test_from_float(self, sequence: WeightSequence):
        other = WeightSequence.from_float([])
        assert other == sequence

    def test_from_int(self, sequence: WeightSequence):
        other = WeightSequence.from_int([])
        assert other == sequence

    def test_sum(self, sequence: WeightSequence):
        assert sequence.sum() == Weight(0)


class TestBalancedWeightsInvariants:
    @pytest.mark.parametrize(
        "values",
        [
            (Weight(100),),
            (Weight(20), Weight(-10), Weight(90)),
        ],
    )
    def test_when_sums_to_one_hundred(self, values: Tuple[Weight, ...]):
        BalancedWeights(values)  # does not raise

    @pytest.mark.parametrize(
        "values",
        [
            (),
            (Weight(99),),
            (Weight(101),),
            (Weight(20), Weight(-10), Weight(80)),
        ],
    )
    def test_when_does_not_sum_to_one_hundred(self, values: Tuple[Weight, ...]):
        with pytest.raises(ValueError, match="must sum to one"):
            BalancedWeights(values)
