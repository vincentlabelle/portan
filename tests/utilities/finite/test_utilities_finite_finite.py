from math import inf, nan

import pytest

from portan.utilities.finite import Finite


class _SupportsFloat:
    def __init__(self, value: float):
        self._value = value

    def __float__(self) -> float:
        return self._value


class TestFiniteInvariants:
    @pytest.mark.parametrize("value", [inf, -inf, nan])
    def test_when_not_finite(self, value: float):
        with pytest.raises(ValueError, match="value must be finite"):
            Finite(value)

    def test_when_supports_float(self):
        result = Finite(_SupportsFloat(1.0))
        assert result == Finite(1.0)


@pytest.fixture(scope="module")
def value() -> float:
    return 1.0


@pytest.fixture(scope="module")
def finite(value: float) -> Finite:
    return Finite(value)


class TestFiniteStringRepresentation:
    def test_str(self, finite: Finite, value: float):
        assert str(finite) == str(value)

    def test_repr(self, finite: Finite):
        expected = f"<{finite.__class__.__name__}({finite})>"
        assert repr(finite) == expected


class TestFiniteEqual:
    def test_when_equal(self, finite: Finite, value: float):
        other = Finite(value)
        assert other == finite

    def test_when_different_value(self, finite: Finite, value: float):
        other = Finite(value + 0.1)
        assert other != finite

    def test_when_different_object(self, finite: Finite):
        assert finite != "a"


class TestFiniteHash:
    def test_when_equal(self, finite: Finite, value: float):
        other = Finite(value)
        assert hash(other) == hash(finite)

    def test_when_different_value(self, finite: Finite, value: float):
        other = Finite(value + 0.1)
        assert hash(other) != hash(finite)


class TestFiniteCast:
    def test_float(self, finite: Finite, value: float):
        assert float(finite) == value
