import pytest

from portan.utilities.finite.positive import PositiveFinite


class TestPositiveFiniteInvariants:
    @pytest.mark.parametrize("value", [0.0, -100.0])
    def test_when_value_is_not_strictly_positive(self, value: float):
        with pytest.raises(ValueError, match="strictly positive"):
            PositiveFinite(value)

    @pytest.mark.parametrize("value", [1e-12, 100.0])
    def test_when_value_is_strictly_positive(self, value: float):
        PositiveFinite(value)  # does not raise
