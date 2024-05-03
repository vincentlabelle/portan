from math import inf

import pytest

from portan.library.scatter import Dispersion, Variance


class TestVarianceInvariants:
    def test_when_is_negative(self):
        with pytest.raises(ValueError, match="must be non-negative"):
            Variance(-1e-8)

    @pytest.mark.parametrize("value", [0.0, 1.0, 200.0])
    def test_when_is_non_negative(self, value: float):
        Variance(value)  # does not raise


class TestVarianceToDispersion:
    @pytest.mark.parametrize("value", [0.0, 4.0, 200.0, inf])
    def test(self, value: float):
        variance = Variance(value)
        result = variance.to_dispersion()
        expected = Dispersion(value ** 0.5)
        assert result == expected
