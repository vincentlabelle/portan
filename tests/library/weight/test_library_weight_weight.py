from math import inf, nan
from typing import SupportsFloat

import pytest

from portan.library.weight import Weight


@pytest.fixture(scope="module")
def value() -> int:
    return 25


@pytest.fixture(scope="module")
def weight(value: int) -> Weight:
    return Weight(value)


class TestWeightInvariants:
    def test_supports_int(self, weight: Weight):
        other = Weight(weight)
        assert other == weight


class TestWeightAlternativeConstructors:
    def test_from_float_when_nan(self):
        with pytest.raises(ValueError, match="NaN"):
            Weight.from_float(nan)

    @pytest.mark.parametrize("value", [inf, -inf, 1e308])
    def test_from_float_when_inf(self, value: float):
        with pytest.raises(OverflowError, match="too big"):
            Weight.from_float(value)

    @pytest.mark.parametrize(
        "value, expected",
        [
            (-0.05, Weight(-5)),
            (0.0, Weight(0)),
            (0.0005, Weight(0)),
            (0.25, Weight(25)),
            (1.0, Weight(100)),
            (0.255, Weight(26)),
            (0.265, Weight(26)),
            (Weight(25), Weight(25)),
        ],
    )
    def test_from_float_when_finite(
        self,
        value: SupportsFloat,
        expected: Weight,
    ):
        result = Weight.from_float(value)
        assert result == expected


class TestWeightStringRepresentation:
    @pytest.mark.parametrize(
        "weight, expected",
        [
            (Weight(25), "0.25"),
            (Weight(0), "0.00"),
            (Weight(2), "0.02"),
            (Weight(-50), "-0.50"),
            (Weight(500), "5.00"),
            (Weight(-1050), "-10.50"),
        ],
    )
    def test_str(self, weight: Weight, expected: str):
        assert str(weight) == expected

    def test_repr(self, weight: Weight):
        assert repr(weight) == f"<{weight.__class__.__name__}({weight})>"


class TestWeightEqual:
    def test_when_equal(self, weight: Weight, value: int):
        other = Weight(value)
        assert other == weight

    def test_when_different_value(self, weight: Weight, value: int):
        other = Weight(value + 1)
        assert other != weight

    def test_when_different_object(self, weight: Weight):
        assert weight != "a"


class TestWeightHash:
    def test_when_equal(self, weight: Weight, value: int):
        other = Weight(value)
        assert hash(other) == hash(weight)

    def test_when_different_value(self, weight: Weight, value: int):
        other = Weight(value + 1)
        assert hash(other) != hash(weight)


class TestWeightCast:
    def test_int(self, weight: Weight, value: int):
        assert int(weight) == value

    @pytest.mark.parametrize(
        "weight, expected",
        [
            (Weight(25), 0.25),
            (Weight(0), 0.0),
            (Weight(2), 0.02),
            (Weight(-50), -0.5),
            (Weight(500), 5.0),
            (Weight(-1050), -10.50),
        ],
    )
    def test_float(self, weight: Weight, expected: float):
        assert float(weight) == expected


class TestWeightArithmetic:
    def test_add(self, weight: Weight, value: int):
        other = Weight(20)
        expected = Weight(value + int(other))
        assert weight + other == expected

    def test_add_when_different_object(self, weight: Weight):
        with pytest.raises(TypeError):
            weight + 1
