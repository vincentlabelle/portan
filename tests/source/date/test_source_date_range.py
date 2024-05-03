import pytest

from portan.source.date import Date
from portan.source.date.range import DateRange


@pytest.fixture(scope="module")
def begin() -> Date:
    return Date("2021-09-01")


@pytest.fixture(scope="module")
def end() -> Date:
    return Date("2021-09-02")


class TestDateRangeInvariants:
    def test_when_end_is_lower_than_begin(self, begin: Date, end: Date):
        with pytest.raises(ValueError, match="end must be greater"):
            DateRange(end, begin)

    def test_when_end_is_not_lower_than_begin(self, begin: Date, end: Date):
        DateRange(begin, end)  # does not raise
        DateRange(begin, begin)  # does not raise


class TestDateRangeAlternativeConstructors:
    def test_from_string(self, range_: DateRange, begin: Date, end: Date):
        result = DateRange.from_string(str(begin), str(end))
        assert result == range_


@pytest.fixture(scope="module")
def range_(begin: Date, end: Date) -> DateRange:
    return DateRange(begin, end)


class TestDateRangeStringRepresentation:
    def test_str(self, range_: DateRange, begin: Date, end: Date):
        expected = f"(begin={begin}, end={end})"
        assert str(range_) == expected

    def test_repr(self, range_: DateRange):
        expected = f"<{range_.__class__.__name__}{range_}>"
        assert repr(range_) == expected


class TestDateRangeEqual:
    def test_when_equal(self, range_: DateRange, begin: Date, end: Date):
        other = DateRange(begin, end)
        assert other == range_

    def test_when_different_begin(self, range_: DateRange, end: Date):
        other = DateRange(end, end)
        assert other != range_

    def test_when_different_end(self, range_: DateRange, begin: Date):
        other = DateRange(begin, begin)
        assert other != range_

    def test_when_different_object(self, range_: DateRange):
        assert range_ != "a"


class TestDateRangeHash:
    def test_when_equal(self, range_: DateRange, begin: Date, end: Date):
        other = DateRange(begin, end)
        assert hash(other) == hash(range_)

    def test_when_different_begin(self, range_: DateRange, end: Date):
        other = DateRange(end, end)
        assert hash(other) != hash(range_)

    def test_when_different_end(self, range_: DateRange, begin: Date):
        other = DateRange(begin, begin)
        assert hash(other) != hash(range_)


class TestDateRangeProperties:
    def test_begin(self, range_: DateRange, begin: Date):
        assert range_.begin == begin

    def test_set_begin(self, range_: DateRange, begin: Date):
        with pytest.raises(AttributeError):
            range_.begin = begin

    def test_end(self, range_: DateRange, end: Date):
        assert range_.end == end

    def test_set_end(self, range_: DateRange, end: Date):
        with pytest.raises(AttributeError):
            range_.end = end
