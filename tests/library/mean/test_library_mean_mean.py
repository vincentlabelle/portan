from math import inf, nan

import pytest

from portan.library.mean import Mean


@pytest.fixture(scope="module")
def mean() -> Mean:
    return Mean(2.0)


class TestMeanArithmetic:
    def test_add(self, mean: Mean):
        other = Mean(4.0)
        result = mean + other
        expected = Mean(float(mean) + float(other))
        assert result == expected

    def test_add_when_different_object(self, mean: Mean):
        with pytest.raises(TypeError):
            mean + 4.0

    def test_sub(self, mean: Mean):
        other = Mean(4.0)
        result = mean - other
        expected = Mean(float(mean) - float(other))
        assert result == expected

    def test_sub_when_different_object(self, mean: Mean):
        with pytest.raises(TypeError):
            mean - 4.0


class TestMeanScale:
    def test_when_scale_is_nan(self, mean: Mean):
        with pytest.raises(ValueError, match="must not be NaN"):
            mean.scale(nan)

    @pytest.mark.parametrize(
        "factor, expected",
        [
            (3.0, Mean(6.0)),
            (inf, Mean(inf)),
        ],
    )
    def test_when_scale_is_not_nan(
        self,
        mean: Mean,
        factor: float,
        expected: Mean,
    ):
        result = mean.scale(factor)
        assert result == expected
