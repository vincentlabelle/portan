import pytest

from portan.source.date import Date
from portan.source.dated.generic import Dated


@pytest.fixture(scope="module")
def date() -> Date:
    return Date("2021-09-01")


@pytest.fixture(scope="module")
def value() -> int:
    return 100


@pytest.fixture(scope="module")
def dated(date: Date, value: int) -> Dated:
    return Dated(date, value)


class TestDatedStringRepresentation:
    def test_str(self, dated: Dated, date: Date, value: int):
        assert str(dated) == f"(date={date}, value={value})"

    def test_repr(self, dated: Dated):
        assert repr(dated) == f"<{dated.__class__.__name__}{dated}>"


class TestDatedEqual:
    def test_when_equal(self, dated: Dated, date: Date, value: int):
        other = Dated(date, value)
        assert other == dated

    def test_when_different_date(self, dated: Dated, value: int):
        date = Date("0001-01-01")
        other = Dated(date, value)
        assert other != dated

    def test_when_different_value(self, dated: Dated, date: Date):
        other = Dated(date, 1)
        assert other != dated

    def test_when_different_object(self, dated: Dated):
        assert dated != "a"


class TestDatedHash:
    def test_when_equal(self, dated: Dated, date: Date, value: int):
        other = Dated(date, value)
        assert hash(other) == hash(dated)

    def test_when_different_date(self, dated: Dated, value: int):
        date = Date("0001-01-01")
        other = Dated(date, value)
        assert hash(other) != hash(dated)

    def test_when_different_value(self, dated: Dated, date: Date):
        other = Dated(date, 1)
        assert hash(other) != hash(dated)


class TestDatedProperties:
    def test_date(self, dated: Dated, date: Date):
        assert dated.date == date

    def test_set_date(self, dated: Dated, date: Date):
        with pytest.raises(AttributeError):
            dated.date = date

    def test_value(self, dated: Dated, value: int):
        assert dated.value == value

    def test_set_value(self, dated: Dated, value: int):
        with pytest.raises(AttributeError):
            dated.value = value
