import pytest

from portan.source.dated.price.series import DatedPriceSeries
from portan.source.dated.prices import DatedPrices
from portan.source.dated.prices.builder import DatedPricesSeriesBuilder
from portan.source.dated.prices.series import DatedPricesSeries


@pytest.fixture(scope="function")
def builder() -> DatedPricesSeriesBuilder:
    return DatedPricesSeriesBuilder()


class TestDatedPricesSeriesBuilderGet:
    def test_when_none(self, builder: DatedPricesSeriesBuilder):
        with pytest.raises(RuntimeError, match="add singles"):
            builder.get()

    def test_when_some(self, builder: DatedPricesSeriesBuilder):
        single = DatedPriceSeries.from_basic([("2021-10-31", 100.0)])
        builder.add(single)
        builder.get()  # does not raise


class TestDatedPricesSeriesBuilderAdd:
    @pytest.fixture(scope="class")
    def single(self) -> DatedPriceSeries:
        return DatedPriceSeries.from_basic(
            [
                ("2021-10-31", 100.0),
                ("2021-11-01", 99.0),
                ("2021-11-02", 101.0),
            ]
        )

    @pytest.fixture(scope="function")
    def builder(
        self,
        builder: DatedPricesSeriesBuilder,
        single: DatedPriceSeries,
    ) -> DatedPricesSeriesBuilder:
        builder.add(single)
        return builder

    def test_when_one(
        self,
        builder: DatedPricesSeriesBuilder,
        single: DatedPriceSeries,
    ):
        result = builder.get()
        expected = DatedPricesSeries.from_single(single)
        assert result == expected

    def test_when_multiple_and_all_equal(
        self,
        builder: DatedPricesSeriesBuilder,
        single: DatedPriceSeries,
    ):
        other = DatedPriceSeries.from_basic(
            [
                ("2021-10-31", 10.0),
                ("2021-11-01", 9.0),
                ("2021-11-02", 11.0),
            ]
        )
        builder.add(other)
        result = builder.get()
        expected = DatedPricesSeries.from_single(
            single,
        ).add(other)
        assert result == expected

    @pytest.mark.parametrize(
        "other, expected",
        [
            (
                DatedPriceSeries.from_basic(
                    [
                        ("2021-11-02", 10.0),
                        ("2021-11-03", 9.0),
                        ("2021-11-04", 11.0),
                    ]
                ),
                DatedPricesSeries(
                    [
                        DatedPrices.from_basic("2021-11-02", [101.0, 10.0]),
                    ]
                ),
            ),  # right intersection
            (
                DatedPriceSeries.from_basic(
                    [
                        ("2021-10-29", 10.0),
                        ("2021-10-30", 9.0),
                        ("2021-10-31", 11.0),
                    ]
                ),
                DatedPricesSeries(
                    [
                        DatedPrices.from_basic("2021-10-31", [100.0, 11.0]),
                    ]
                ),
            ),  # left intersection
            (
                DatedPriceSeries.from_basic(
                    [
                        ("2021-10-29", 10.0),
                        ("2021-11-01", 9.0),
                        ("2021-11-03", 11.0),
                    ]
                ),
                DatedPricesSeries(
                    [
                        DatedPrices.from_basic("2021-11-01", [99.0, 9.0]),
                    ]
                ),
            ),  # middle intersection
            (
                DatedPriceSeries.from_basic(
                    [
                        ("2021-10-30", 10.0),
                        ("2021-11-01", 9.0),
                        ("2021-11-02", 11.0),
                    ]
                ),
                DatedPricesSeries(
                    [
                        DatedPrices.from_basic("2021-11-01", [99.0, 9.0]),
                        DatedPrices.from_basic("2021-11-02", [101.0, 11.0]),
                    ]
                ),
            ),  # inside intersection
        ],
    )
    def test_when_multiple_and_some_equal(
        self,
        builder: DatedPricesSeriesBuilder,
        single: DatedPriceSeries,
        other: DatedPriceSeries,
        expected: DatedPricesSeries,
    ):
        builder.add(other)
        result = builder.get()
        assert result == expected

    def test_when_multiple_and_none_equal(
        self,
        builder: DatedPricesSeriesBuilder,
        single: DatedPriceSeries,
    ):
        other = DatedPriceSeries.from_basic(
            [
                ("2021-11-03", 10.0),
                ("2021-11-04", 9.0),
                ("2021-11-05", 11.0),
            ]
        )
        builder.add(other)
        result = builder.get()
        expected = DatedPricesSeries([])
        assert result == expected
