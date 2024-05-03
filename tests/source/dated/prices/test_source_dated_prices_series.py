from typing import Tuple

import pytest

from portan.source.dated.price.series import DatedPriceSeries
from portan.source.dated.prices import DatedPrices
from portan.source.dated.prices.series import DatedPricesSeries
from portan.source.price.matrix import PriceMatrix


class TestDatedPricesSeriesInvariants:
    @pytest.mark.parametrize(
        "prices",
        [[5.0], [5.0, 6.0, 7.0]],
    )
    def test_when_number_of_prices_mismatch(self, prices: Tuple[float, ...]):
        with pytest.raises(ValueError, match="number of prices"):
            DatedPricesSeries(
                [
                    DatedPrices.from_basic("2021-10-31", [1.0, 2.0]),
                    DatedPrices.from_basic("2021-11-01", prices),
                    DatedPrices.from_basic("2021-11-02", [3.0, 4.0]),
                ]
            )

    def test_when_number_of_prices_match(self):
        DatedPricesSeries(
            [
                DatedPrices.from_basic("2021-10-31", [1.0, 2.0]),
                DatedPrices.from_basic("2021-11-01", [5.0, 6.0]),
                DatedPrices.from_basic("2021-11-02", [3.0, 4.0]),
            ]
        )  # does not raise


class TestDatedPriceSeriesAlternativeConstructors:
    def test_from_single(self):
        single = DatedPriceSeries.from_basic(
            [
                ("2021-10-31", 100.0),
                ("2021-11-01", 101.0),
            ]
        )
        result = DatedPricesSeries.from_single(single)
        expected = DatedPricesSeries(
            [DatedPrices.from_single(value) for value in single]
        )
        assert result == expected


@pytest.fixture(scope="module")
def series() -> DatedPricesSeries:
    return DatedPricesSeries(
        [
            DatedPrices.from_basic("2021-11-01", [1.0, 2.0]),
            DatedPrices.from_basic("2021-11-02", [3.0, 4.0]),
        ]
    )


class TestDatedPricesSeriesProperties:
    def test_prices(self, series: DatedPricesSeries):
        expected = PriceMatrix(value.value for value in series).transpose()
        assert series.prices == expected

    def test_set_prices(self, series: DatedPricesSeries):
        with pytest.raises(AttributeError):
            series.prices = PriceMatrix([])


class TestDatedPricesSeriesToBasic:
    def test_when_one(self):
        value = ("2021-11-01", (1.0, 2.0))
        series = DatedPricesSeries(
            [
                DatedPrices.from_basic(*value),
            ]
        )
        result = self._get_basic_as_tuples(series)
        expected = (value,)
        assert result == expected

    def test_when_multiple(self):
        values = (
            ("2021-11-01", (1.0, 2.0)),
            ("2021-11-02", (3.0, 4.0)),
        )
        series = DatedPricesSeries(
            DatedPrices.from_basic(*value) for value in values
        )
        result = self._get_basic_as_tuples(series)
        assert result == values

    @staticmethod
    def _get_basic_as_tuples(series: DatedPricesSeries):
        return tuple(
            (
                value[0],
                tuple(value[1]),
            )
            for value in series.to_basic()
        )


class TestDatedPricesSeriesAdd:
    def test_when_dates_mismatch(self, series: DatedPricesSeries):
        single = DatedPriceSeries.from_basic(
            [
                ("2021-11-01", 5.0),
                ("2021-11-03", 6.0),
            ]
        )
        with pytest.raises(ValueError, match="same dates"):
            series.add(single)

    def test_when_dates_match(self, series: DatedPricesSeries):
        single = DatedPriceSeries.from_basic(
            [
                ("2021-11-01", 6.0),
                ("2021-11-02", 5.0),
            ]
        )
        result = series.add(single)
        expected = DatedPricesSeries(
            m.add(s.value) for m, s in zip(series, single)
        )
        assert result == expected


class TestDatedPriceSequenceEmpty:
    @pytest.fixture(scope="class")
    def series(self) -> DatedPricesSeries:
        return DatedPricesSeries([])

    def test_from_single(self, series: DatedPricesSeries):
        assert DatedPricesSeries.from_single(DatedPriceSeries([])) == series

    def test_prices(self, series: DatedPricesSeries):
        assert series.prices == PriceMatrix([])

    def test_to_basic(self, series: DatedPricesSeries):
        assert tuple(series.to_basic()) == ()

    def test_add(self, series: DatedPricesSeries):
        result = series.add(DatedPriceSeries([]))
        assert result == series
