from math import inf, nan, sqrt

import pytest

from portan.library.scatter import Dispersion


class TestDispersionInvariants:
    def test_when_is_negative(self):
        with pytest.raises(ValueError, match="value must be non-negative"):
            Dispersion(-1e-8)

    @pytest.mark.parametrize("value", [0.0, 1e8, 100.0, inf])
    def test_when_is_non_negative_nor_nan(self, value: float):
        Dispersion(value)  # does not raise


@pytest.fixture(scope="module")
def value() -> float:
    return 2.0


@pytest.fixture(scope="module")
def dispersion(value: float) -> Dispersion:
    return Dispersion(value)


class TestDispersionScale:
    def test_when_factor_is_negative(self, dispersion: Dispersion):
        with pytest.raises(ValueError, match="factor must be non-negative"):
            dispersion.scale(-1e-8)

    def test_when_factor_is_nan(self, dispersion: Dispersion):
        with pytest.raises(ValueError, match="factor must not be NaN"):
            dispersion.scale(nan)

    @pytest.mark.parametrize("factor", [0.0, 3.0, inf])
    def test_when_factor_is_non_negative_nor_nan(
        self,
        dispersion: Dispersion,
        value: float,
        factor: float,
    ):
        result = dispersion.scale(factor)
        expected = Dispersion(value * sqrt(factor))
        assert result == expected

    def test_when_supports_float(self, dispersion: Dispersion, value: float):
        factor = Dispersion(3.0)
        result = dispersion.scale(factor)
        expected = Dispersion(value * sqrt(factor))
        assert result == expected
