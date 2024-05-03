import pytest

from portan.source.date.range import DateRange
from portan.source.dated.price.series import DatedPriceSeries
from portan.source.dated.prices.series import DatedPricesSeries
from portan.source.source.multiple import IMultipleSource, MultipleSource
from portan.source.source.single import ISingleSource


class TestIMultipleSourceRaises:
    def test(self):
        source = IMultipleSource()
        with pytest.raises(NotImplementedError):
            source.get(
                [
                    "AAPL",
                    "SQ",
                ],
                DateRange.from_string(
                    "2021-08-03",
                    "2021-08-04",
                ),
            )


class TestIMultipleSourceGet:
    def test_when_none(self):
        source = IMultipleSource()
        result = source.get(
            [],
            DateRange.from_string(
                "2021-08-03",
                "2021-08-04",
            ),
        )
        assert result == DatedPricesSeries([])


_TICKERS = ("a", "b")
_RANGE = DateRange.from_string(
    "2021-08-04",
    "2021-08-05",
)
_SINGLES = (
    DatedPriceSeries.from_basic(
        [
            ("2021-10-31", 1.0),
            ("2021-11-01", 2.0),
        ]
    ),
    DatedPriceSeries.from_basic(
        [
            ("2021-10-31", 3.0),
            ("2021-11-01", 4.0),
        ]
    ),
)


class _SingleStub(ISingleSource):
    def __init__(self):
        self._count = -1

    def get(self, ticker: str, range_: DateRange) -> DatedPriceSeries:
        self._count += 1
        assert ticker is _TICKERS[self._count]
        assert range_ is _RANGE
        return _SINGLES[self._count]


class TestMultipleSourceProperties:
    @pytest.fixture(scope="function")
    def single(self) -> _SingleStub:
        return _SingleStub()

    @pytest.fixture(scope="function")
    def source(self, single: _SingleStub) -> MultipleSource:
        return MultipleSource(single)

    def test_single(self, source: MultipleSource, single: _SingleStub):
        assert source.single is single

    def test_set_single(self, source: MultipleSource, single: _SingleStub):
        with pytest.raises(AttributeError):
            source.single = single


class TestMultipleSourceGet:
    @pytest.fixture(scope="function")
    def source(self) -> MultipleSource:
        return MultipleSource(_SingleStub())

    def test_when_one(self, source: MultipleSource):
        result = source.get(_TICKERS[:1], _RANGE)
        expected = DatedPricesSeries.from_single(_SINGLES[0])
        assert result == expected

    def test_when_multiple(self, source: MultipleSource):
        result = source.get(_TICKERS, _RANGE)
        expected = DatedPricesSeries.from_single(
            _SINGLES[0],
        ).add(_SINGLES[1])
        assert result == expected
