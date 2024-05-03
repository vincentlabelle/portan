import pytest

from portan.library.brownian import IArithmeticBrownian
from portan.library.converter import BrownianConverter
from portan.library.frequency import Frequency
from portan.library.mean import Mean
from portan.library.scatter import Dispersion

_MEAN = Mean(2.0)
_DISPERSION = Dispersion(0.1)


class _BrownianStub(IArithmeticBrownian):
    def mean(self) -> Mean:
        return _MEAN

    def dispersion(self) -> Dispersion:
        return _DISPERSION


class TestBrownianConverter:
    @pytest.mark.parametrize(
        "to",
        [
            Frequency.ANNUAL,
            Frequency.MONTHLY,
            Frequency.DAILY,
        ],
    )
    def test_mean(self, to: Frequency):
        from_ = Frequency.MONTHLY
        converter = BrownianConverter(
            _BrownianStub(),
            from_=from_,
            to=to,
        )
        result = converter.mean()
        expected = _MEAN.scale(from_.value / to.value)
        assert result == expected

    @pytest.mark.parametrize(
        "to",
        [
            Frequency.ANNUAL,
            Frequency.MONTHLY,
            Frequency.DAILY,
        ],
    )
    def test_dispersion(self, to: Frequency):
        from_ = Frequency.MONTHLY
        converter = BrownianConverter(
            _BrownianStub(),
            from_=from_,
            to=to,
        )
        result = converter.dispersion()
        expected = _DISPERSION.scale(from_.value / to.value)
        assert result == expected
