from math import log
from typing import Tuple

import pytest

from portan.library.price import Price
from portan.library.price.sequence import PriceSequence
from portan.library.rate.sequence import RateSequence


class TestPriceSequenceAlternativeConstructors:
    @pytest.fixture(scope="class")
    def values(self) -> Tuple[Price, ...]:
        return (
            Price(0.01),
            Price(0.02),
            Price(0.03),
        )

    @pytest.fixture(scope="class")
    def sequence(self, values: Tuple[Price, ...]) -> PriceSequence:
        return PriceSequence(values)

    def test_from_float(
        self,
        sequence: PriceSequence,
        values: Tuple[Price, ...],
    ):
        other = PriceSequence.from_float(float(value) for value in values)
        assert other == sequence

    def test_from_float_when_supports_float(
        self,
        sequence: PriceSequence,
        values: Tuple[Price, ...],
    ):
        other = PriceSequence.from_float(value for value in values)
        assert other == sequence


class TestPriceSequenceGrowth:
    def test_when_one_element(self):
        sequence = PriceSequence([Price(1.0)])
        assert sequence.growth() == RateSequence([])

    def test_when_two_elements(self):
        sequence = PriceSequence.from_float([2.0, 4.0])
        result = sequence.growth()
        expected = RateSequence.from_float([log(4.0 / 2.0)])
        assert result == expected

    def test_when_more_than_two_elements(self):
        sequence = PriceSequence.from_float([2.0, 4.0, 3.0])
        result = sequence.growth()
        expected = RateSequence.from_float(
            [
                log(4.0 / 2.0),
                log(3.0 / 4.0),
            ]
        )
        assert result == expected


class TestPriceSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> PriceSequence:
        return PriceSequence([])

    def test_from_float(self, sequence: PriceSequence):
        other = PriceSequence.from_float([])
        assert other == sequence

    def test_growth(self, sequence: PriceSequence):
        assert sequence.growth() == RateSequence([])
