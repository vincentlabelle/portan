from typing import Tuple

import pytest

from portan.source.dated.price import DatedPrice
from portan.source.dated.price.series import DatedPriceSeries
from portan.source.price.sequence import PriceSequence


@pytest.fixture(scope="module")
def values() -> Tuple[DatedPrice, ...]:
    return (
        DatedPrice.from_basic("2021-09-01", 100.0),
        DatedPrice.from_basic("2021-09-02", 101.0),
        DatedPrice.from_basic("2021-09-03", 99.0),
    )


@pytest.fixture(scope="module")
def series(values: Tuple[DatedPrice, ...]) -> DatedPriceSeries:
    return DatedPriceSeries(values)


class TestDatedPriceSeriesAlternativeConstructors:
    def test_from_basic(
        self,
        series: DatedPriceSeries,
        values: Tuple[DatedPrice, ...],
    ):
        result = DatedPriceSeries.from_basic(
            (str(value.date), float(value.value)) for value in values
        )
        assert result == series

    def test_from_basic_supports_float(
        self,
        series: DatedPriceSeries,
        values: Tuple[DatedPrice, ...],
    ):
        result = DatedPriceSeries.from_basic(
            (str(value.date), value.value) for value in values
        )
        assert result == series

    def test_from_unsorted_basic_when_sorted(self):
        values = (
            ("2021-09-01", 100.0),
            ("2021-09-02", 101.0),
            ("2021-09-03", 100.0),
        )
        result = DatedPriceSeries.from_unsorted_basic(values)
        expected = DatedPriceSeries.from_basic(values)
        assert result == expected

    def test_from_unsorted_basic_when_unsorted(self):
        values = (
            ("2021-09-01", 100.0),
            ("2021-09-04", 101.0),
            ("2021-09-03", 102.0),
        )
        result = DatedPriceSeries.from_unsorted_basic(values)
        expected = DatedPriceSeries.from_basic(
            sorted(values, key=lambda x: x[0])
        )
        assert result == expected

    def test_from_unsorted_basic_supports_float(
        self,
        series: DatedPriceSeries,
        values: Tuple[DatedPrice, ...],
    ):
        result = DatedPriceSeries.from_basic(
            (str(value.date), value.value) for value in values
        )
        assert result == series


class TestDatedPriceSeriesProperties:
    def test_prices(self, series: DatedPriceSeries):
        expected = PriceSequence(value.value for value in series)
        assert series.prices == expected

    def test_set_prices(self, series: DatedPriceSeries):
        with pytest.raises(AttributeError):
            series.prices = PriceSequence([])


class TestDatedPriceSequenceToBasic:
    def test_when_one(self):
        value = ("2021-09-01", 100.0)
        series = DatedPriceSeries([DatedPrice.from_basic(*value)])
        result = series.to_basic()
        expected = (value,)
        assert tuple(result) == expected

    def test_when_multiple(self):
        values = (
            ("2021-09-01", 100.0),
            ("2021-09-02", 99.0),
            ("2021-09-03", 100.0),
        )
        series = DatedPriceSeries(
            DatedPrice.from_basic(*value) for value in values
        )
        result = series.to_basic()
        assert tuple(result) == values

    def test_reverts_to(self, series: DatedPriceSeries):
        basic = series.to_basic()
        other = DatedPriceSeries.from_basic(basic)
        assert other == series


class TestDatedPriceSeriesEmpty:
    @pytest.fixture(scope="class")
    def series(self) -> DatedPriceSeries:
        return DatedPriceSeries([])

    def test_from_basic(self, series: DatedPriceSeries):
        assert DatedPriceSeries.from_basic([]) == series

    def test_from_unsorted_basic(self, series: DatedPriceSeries):
        assert DatedPriceSeries.from_unsorted_basic([]) == series

    def test_prices(self, series: DatedPriceSeries):
        assert series.prices == PriceSequence([])

    def test_to_basic(self, series: DatedPriceSeries):
        assert tuple(series.to_basic()) == ()
