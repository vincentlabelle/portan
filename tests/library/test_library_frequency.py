import pytest

from portan.library.frequency import Frequency


class TestFrequencyInvariants:
    @pytest.mark.parametrize(
        "frequency, expected",
        [
            (Frequency.ANNUAL, 1),
            (Frequency.MONTHLY, 12),
            (Frequency.DAILY, 252),
        ],
    )
    def test_value(self, frequency: Frequency, expected: int):
        assert frequency.value == expected


class TestFrequencyStringRepresentation:
    @pytest.fixture(
        scope="class",
        params=[Frequency.ANNUAL, Frequency.MONTHLY, Frequency.DAILY],
    )
    def frequency(self, request) -> Frequency:
        return request.param

    def test_str(self, frequency: Frequency):
        assert str(frequency) == frequency.name

    def test_repr(self, frequency: Frequency):
        expected = f"<{frequency.__class__.__name__}({frequency})>"
        assert repr(frequency) == expected
