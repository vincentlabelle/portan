from math import inf, nan

import pytest

from portan.utilities.nonnan import NonNan


class TestNonNanInvariants:
    def test_when_is_nan(self):
        with pytest.raises(ValueError, match="value must not be NaN"):
            NonNan(nan)

    @pytest.mark.parametrize("value", [inf, 10.0, 0.0, -205.0])
    def test_when_is_not_nan(self, value: float):
        NonNan(value)  # does not raise

    def test_when_supports_float(self):
        assert NonNan(NonNan(2.0)) == NonNan(2.0)


@pytest.fixture(scope="module")
def value() -> float:
    return 2.0


@pytest.fixture(scope="module")
def nonnan(value: float) -> NonNan:
    return NonNan(value)


class TestNonNanStringRepresentation:
    def test_str(self, nonnan: NonNan, value: float):
        assert str(nonnan) == str(value)

    def test_repr(self, nonnan: NonNan):
        assert repr(nonnan) == f"<{nonnan.__class__.__name__}({nonnan})>"


class TestNonNanEqual:
    def test_when_equal(self, nonnan: NonNan, value: float):
        other = NonNan(value)
        assert other == nonnan

    def test_when_different_value(self, nonnan: NonNan, value: float):
        other = NonNan(value - 1.0)
        assert other != nonnan

    def test_when_different_object(self, nonnan: NonNan):
        assert nonnan != "a"


class TestNonNanHash:
    def test_when_equal(self, nonnan: NonNan, value: float):
        other = NonNan(value)
        assert hash(other) == hash(nonnan)

    def test_when_different_value(self, nonnan: NonNan, value: float):
        other = NonNan(value - 1.0)
        assert hash(other) != hash(nonnan)


class TestNonNanCast:
    def test_float(self, nonnan: NonNan, value: float):
        assert float(nonnan) == value
