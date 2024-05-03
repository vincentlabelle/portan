import pytest

from portan.library.frequency import Frequency
from portan.library.rate import Rate


class TestRateConvert:
    @pytest.mark.parametrize(
        "from_, to",
        [
            (Frequency.MONTHLY, Frequency.ANNUAL),
            (Frequency.MONTHLY, Frequency.DAILY),
            (Frequency.MONTHLY, Frequency.MONTHLY),
        ],
    )
    def test_when_finite(
        self,
        from_: Frequency,
        to: Frequency,
    ):
        rate = Rate(1.0)
        result = rate.convert(from_=from_, to=to)
        expected = Rate(float(rate) * from_.value / to.value)
        assert result == expected

    def test_when_non_finite(self):
        rate = Rate(1e308)
        with pytest.raises(ValueError, match="must be finite"):
            rate.convert(from_=Frequency.DAILY, to=Frequency.ANNUAL)
