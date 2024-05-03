from typing import Tuple

import pytest

from portan.source.price import Price
from portan.source.price.sequence import PriceSequence


@pytest.fixture(scope="module")
def values() -> Tuple[Price, ...]:
    return Price(1.0), Price(2.0), Price(3.0)


@pytest.fixture(scope="module")
def sequence(values: Tuple[Price, ...]) -> PriceSequence:
    return PriceSequence(values)


class TestPriceSequenceAlternativeConstructors:
    def test_from_float(self, sequence: PriceSequence):
        result = PriceSequence.from_float(float(value) for value in sequence)
        assert result == sequence

    def test_from_float_supports_float(self, sequence: PriceSequence):
        result = PriceSequence.from_float(value for value in sequence)
        assert result == sequence


class TestPriceSequenceAdd:
    def test(self, sequence: PriceSequence, values: Tuple[Price, ...]):
        value = Price(4.0)
        result = sequence.add(value)
        expected = PriceSequence((*values, value))
        assert result == expected


class TestPriceSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> PriceSequence:
        return PriceSequence([])

    def test_from_float(self, sequence: PriceSequence):
        assert PriceSequence.from_float([]) == sequence

    def test_add(self, sequence: PriceSequence):
        result = sequence.add(Price(1.0))
        expected = PriceSequence([Price(1.0)])
        assert result == expected
