import pytest

from portan.source.date import Date
from portan.source.dated.price import DatedPrice
from portan.source.dated.prices import DatedPrices
from portan.source.price import Price
from portan.source.price.sequence import PriceSequence


@pytest.fixture(scope="module")
def date() -> Date:
    return Date("2021-10-31")


@pytest.fixture(scope="module")
def prices() -> PriceSequence:
    return PriceSequence.from_float([1.0, 2.0, 3.0])


@pytest.fixture(scope="module")
def dated(date: Date, prices: PriceSequence) -> DatedPrices:
    return DatedPrices(date, prices)


class TestDatedPricesAlternativeConstructors:
    def test_from_basic(
        self,
        dated: DatedPrices,
        date: Date,
        prices: PriceSequence,
    ):
        result = DatedPrices.from_basic(
            str(date),
            (float(price) for price in prices),
        )
        assert result == dated

    def test_from_basic_supports_float(
        self,
        dated: DatedPrices,
        date: Date,
        prices: PriceSequence,
    ):
        result = DatedPrices.from_basic(
            str(date),
            (price for price in prices),
        )
        assert result == dated

    def test_from_single(self):
        single = DatedPrice.from_basic("2021-10-31", 100.0)
        result = DatedPrices.from_single(single)
        expected = DatedPrices.from_basic("2021-10-31", [100.0])
        assert result == expected


class TestDatedPricesAdd:
    def test(self, dated: DatedPrices, date: Date, prices: PriceSequence):
        value = Price(4.0)
        result = dated.add(value)
        expected = DatedPrices(date, prices.add(value))
        assert result == expected
