from math import inf, nan

import pytest

from portan.library.scatter.correlation import Correlation


class TestCorrelationInvariants:
    @pytest.mark.parametrize("value", [-2.0, -1.0 - 1e-8, 1.0 + 1e-8, 2.0])
    def test_when_outside(self, value: float):
        with pytest.raises(ValueError, match="must be inside"):
            Correlation(value)

    @pytest.mark.parametrize("value", [-1.0, -0.5, 0.0, 0.5, 1.0])
    def test_when_inside(self, value: float):
        Correlation(value)  # does not raise


class TestCorrelationAlternativeConstructors:
    @pytest.mark.parametrize("value", [1.0 + 1e-8, 2.0, inf])
    def test_robust_when_above_one(self, value: float):
        result = Correlation.robust(value)
        expected = Correlation(1.0)
        assert result == expected

    @pytest.mark.parametrize("value", [-1.0, -0.5, 0.0, 0.5, 1.0])
    def test_robust_when_inside(self, value: float):
        result = Correlation.robust(value)
        expected = Correlation(value)
        assert result == expected

    @pytest.mark.parametrize("value", [-1.0 - 1e-8, -2.0, -inf])
    def test_robust_when_below_minus_one(self, value: float):
        result = Correlation.robust(value)
        expected = Correlation(-1.0)
        assert result == expected

    def test_robust_when_nan(self):
        with pytest.raises(ValueError, match="finite"):
            Correlation.robust(nan)
