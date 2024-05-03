from datetime import date

import pytest

from portan.source.date import MAX_YEAR, MIN_YEAR, Date


class TestDateInvariants:
    @pytest.mark.parametrize(
        "value",
        [
            "",
            "-",
            "a",
            "1",
            "99-12-31",
            "99999-12-31",
        ],
    )
    def test_when_format_is_invalid(self, value: str):
        with pytest.raises(ValueError, match="cannot instantiate"):
            Date(value)

    @pytest.mark.parametrize(
        "value",
        [
            f"{str(MIN_YEAR - 1).zfill(4)}-12-31",  # invalid year
            f"{str(MAX_YEAR + 1).zfill(4)}-01-01",  # invalid year
            "1999-00-01",  # invalid month
            "1999-13-01",  # invalid month
            "1999-01-32",  # invalid day
            "2021-02-29",  # invalid day (not a leap year)
        ],
    )
    def test_when_date_is_invalid(self, value: str):
        with pytest.raises(ValueError, match="cannot instantiate"):
            Date(value)

    @pytest.mark.parametrize(
        "value",
        [
            f"{str(MIN_YEAR).zfill(4)}-01-01",  # minimum year
            f"{str(MAX_YEAR).zfill(4)}-12-31",  # maximum year
            "2020-02-29",  # leap year
        ],
    )
    def test_when_date_is_valid(self, value: str):
        Date(value)  # does not raise


class TestDateAlternativeConstructors:
    def test_today(self):
        result = Date.today()
        expected = Date(date.today().isoformat())
        assert result == expected


@pytest.fixture(scope="module")
def value() -> str:
    return "2021-09-02"


@pytest.fixture(scope="module")
def date_(value: str) -> Date:
    return Date(value)


class TestDateStringRepresentation:
    def test_str(self, date_: Date, value: str):
        assert str(date_) == value

    def test_repr(self, date_: Date):
        expected = f"<{date_.__class__.__name__}({date_})>"
        assert repr(date_) == expected


class TestDateEqual:
    def test_when_equal(self, date_: Date, value: str):
        other = Date(value)
        assert other == date_

    def test_when_different_year(self, date_: Date):
        other = Date("2022-09-02")
        assert other != date_

    def test_when_different_month(self, date_: Date):
        other = Date("2021-10-02")
        assert other != date_

    def test_when_different_day(self, date_: Date):
        other = Date("2021-09-01")
        assert other != date_

    def test_when_different_object(self, date_: Date):
        assert date_ != "a"


class TestDateHash:
    def test_when_equal(self, date_: Date, value: str):
        other = Date(value)
        assert hash(other) == hash(date_)

    def test_when_different_year(self, date_: Date):
        other = Date("2022-09-02")
        assert hash(other) != hash(date_)

    def test_when_different_month(self, date_: Date):
        other = Date("2021-10-02")
        assert hash(other) != hash(date_)

    def test_when_different_day(self, date_: Date):
        other = Date("2021-09-01")
        assert hash(other) != hash(date_)


class TestDateComparison:
    def test_lt_when_equal(self, date_: Date, value: str):
        other = Date(value)
        assert not date_ < other

    @pytest.mark.parametrize(
        "other",
        [
            Date("2021-09-03"),
            Date("2021-10-01"),
            Date("2022-09-01"),
        ],
    )
    def test_lt_when_unequal(self, date_: Date, other: Date):
        assert date_ < other
        assert not other < date_

    def test_lt_when_different_object(self, date_: Date):
        with pytest.raises(TypeError):
            date_ < "a"

    def test_le_when_equal(self, date_: Date, value: str):
        other = Date(value)
        assert date_ <= other

    @pytest.mark.parametrize(
        "other",
        [
            Date("2021-09-03"),
            Date("2021-10-01"),
            Date("2022-09-01"),
        ],
    )
    def test_le_when_unequal(self, date_: Date, other: Date):
        assert date_ <= other
        assert not other <= date_

    def test_le_when_different_object(self, date_: Date):
        with pytest.raises(TypeError):
            date_ <= "a"

    def test_gt_when_equal(self, date_: Date, value: str):
        other = Date(value)
        assert not date_ > other

    @pytest.mark.parametrize(
        "other",
        [
            Date("2021-09-01"),
            Date("2021-08-02"),
            Date("2020-09-02"),
        ],
    )
    def test_gt_when_unequal(self, date_: Date, other: Date):
        assert date_ > other
        assert not other > date_

    def test_gt_when_different_object(self, date_: Date):
        with pytest.raises(TypeError):
            date_ > "a"

    def test_ge_when_equal(self, date_: Date, value: str):
        other = Date(value)
        assert date_ >= other

    @pytest.mark.parametrize(
        "other",
        [
            Date("2021-09-01"),
            Date("2021-08-02"),
            Date("2020-09-02"),
        ],
    )
    def test_ge_when_unequal(self, date_: Date, other: Date):
        assert date_ >= other
        assert not other >= date_

    def test_ge_when_different_object(self, date_: Date):
        with pytest.raises(TypeError):
            date_ >= "a"


class TestDateIncrement:
    @pytest.mark.parametrize("by", [-1, -100])
    def test_when_by_is_negative(self, date_: Date, by: int):
        with pytest.raises(ValueError, match="by must be non-negative"):
            date_.increment(by=by)

    @pytest.mark.parametrize("by", [1000000000, 999999999])
    def test_when_by_is_too_big(self, date_: Date, by: int):
        with pytest.raises(OverflowError, match="magnitude is too high"):
            date_.increment(by=by)

    def test_when_by_is_zero(self, date_: Date):
        result = date_.increment(by=0)
        assert result == date_

    def test_when_by_is_non_zero(self, date_: Date):
        result = date_.increment(by=2)
        expected = Date("2021-09-04")
        assert result == expected

    def test_when_by_is_defaults(self, date_: Date):
        result = date_.increment()
        expected = date_.increment(by=1)
        assert result == expected


class TestDateDecrement:
    @pytest.mark.parametrize("by", [-1, -100])
    def test_when_by_is_negative(self, date_: Date, by: int):
        with pytest.raises(ValueError, match="by must be non-negative"):
            date_.decrement(by=by)

    @pytest.mark.parametrize("by", [1000000000, 999999999])
    def test_when_by_is_too_big(self, date_: Date, by: int):
        with pytest.raises(OverflowError, match="magnitude is too high"):
            date_.decrement(by=by)

    def test_when_by_is_zero(self, date_: Date):
        result = date_.decrement(by=0)
        assert result == date_

    def test_when_by_is_non_zero(self, date_: Date):
        result = date_.decrement(by=2)
        expected = Date("2021-08-31")
        assert result == expected

    def test_when_by_is_defaults(self, date_: Date):
        result = date_.decrement()
        expected = date_.decrement(by=1)
        assert result == expected
