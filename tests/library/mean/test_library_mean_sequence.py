from typing import Tuple

import pytest

from portan.library.mean import Mean
from portan.library.mean.sequence import MeanSequence


class TestMeanSequenceSum:
    @pytest.mark.parametrize(
        "factors",
        [
            (1.0,),
            (1.0, 2.0, 3.0),
        ],
    )
    def test_when_length_mismatch(self, factors: Tuple[float, ...]):
        sequence = MeanSequence(
            [
                Mean(4.0),
                Mean(5.0),
            ]
        )
        with pytest.raises(ValueError, match="length of factors"):
            sequence.sum(factors)

    def test_when_one(self):
        value, factor = Mean(4.0), 0.5
        sequence = MeanSequence([value])
        result = sequence.sum([factor])
        expected = Mean(float(value) * factor)
        assert result == expected

    def test_when_multiple(self):
        sequence = MeanSequence(
            [
                Mean(1.0),
                Mean(2.0),
                Mean(3.0),
            ]
        )
        factors = (4.0, 5.0, 6.0)
        result = sequence.sum(factors)
        expected = Mean(
            sum(
                float(value) * factor
                for value, factor in zip(sequence, factors)
            )
        )
        assert result == expected


class TestMeanSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> MeanSequence:
        return MeanSequence([])

    def test_sum(self, sequence: MeanSequence):
        assert sequence.sum([]) == Mean(0.0)
