import pytest

from portan.source.date import Date
from portan.source.dated.price import DatedPrice
from portan.source.price import Price


@pytest.fixture(scope="module")
def date() -> Date:
    return Date("2021-09-01")


@pytest.fixture(scope="module")
def price() -> Price:
    return Price(100.0)


@pytest.fixture(scope="module")
def dated(date: Date, price: Price) -> DatedPrice:
    return DatedPrice(date, price)


class TestDatedPriceAlternativeConstructors:
    def test_from_basic(self, dated: DatedPrice, date: Date, price: Price):
        result = DatedPrice.from_basic(str(date), float(price))
        assert result == dated

    def test_from_basic_supports_float(
        self,
        dated: DatedPrice,
        date: Date,
        price: Price,
    ):
        result = DatedPrice.from_basic(str(date), price)
        assert result == dated


class TestDatedPriceToBasic:
    def test(self, dated: DatedPrice, date: Date, price: Price):
        result = dated.to_basic()
        expected = (str(date), float(price))
        assert result == expected

    def test_reverts_to(self, dated: DatedPrice):
        basic = dated.to_basic()
        other = DatedPrice.from_basic(*basic)
        assert other == dated
