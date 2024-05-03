from typing import Tuple

import pytest

from portan.source.date.range import DateRange
from portan.source.dated.price.series import DatedPriceSeries
from portan.source.dated.prices.series import DatedPricesSeries
from portan.source.source import PriceSource
from portan.source.source.multiple import IMultipleSource
from portan.source.source.single import ISingleSource

_SINGLE_RESULT = DatedPriceSeries([])
_MULTIPLE_RESULT = DatedPricesSeries([])


class _SingleStub(ISingleSource):
    def get(self, ticker: str, range_: DateRange) -> DatedPriceSeries:
        return _SINGLE_RESULT


class _MultipleStub(IMultipleSource):
    def _get(
        self,
        tickers: Tuple[str, ...],
        range_: DateRange,
    ) -> DatedPricesSeries:
        return _MULTIPLE_RESULT


class TestPriceSourceProperties:
    @pytest.fixture(scope="class")
    def single(self) -> _SingleStub:
        return _SingleStub()

    @pytest.fixture(scope="class")
    def multiple(self) -> _MultipleStub:
        return _MultipleStub()

    @pytest.fixture(scope="class")
    def source(
        self,
        single: _SingleStub,
        multiple: _MultipleStub,
    ) -> PriceSource:
        return PriceSource(single, multiple)

    def test_single(self, source: PriceSource, single: _SingleStub):
        assert source.single is single

    def test_set_single(self, source: PriceSource, single: _SingleStub):
        with pytest.raises(AttributeError):
            source.single = single

    def test_multiple(self, source: PriceSource, multiple: _MultipleStub):
        assert source.multiple is multiple

    def test_set_multiple(self, source: PriceSource, multiple: _MultipleStub):
        with pytest.raises(AttributeError):
            source.multiple = multiple


class TestPriceSourceGet:
    @pytest.fixture(scope="class")
    def range_(self) -> DateRange:
        return DateRange.from_string("2021-10-31", "2021-11-01")

    @pytest.fixture(scope="class")
    def source(self) -> PriceSource:
        return PriceSource(_SingleStub(), _MultipleStub())

    def test_when_string(self, source: PriceSource, range_: DateRange):
        result = source.get("AAPL", range_)
        assert result is _SINGLE_RESULT

    def test_when_iterable(self, source: PriceSource, range_: DateRange):
        result = source.get(["AAPL"], range_)
        assert result is _MULTIPLE_RESULT
