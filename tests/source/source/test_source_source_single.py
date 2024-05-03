import pytest

from portan.source.date import Date
from portan.source.date.range import DateRange
from portan.source.date.sequence import DateSequence
from portan.source.dated.price.series import DatedPriceSeries
from portan.source.source.single import ISingleSource
from portan.source.yahoo import Yahoo


@pytest.fixture(scope="module", params=[Yahoo()])
def source(request) -> ISingleSource:
    return request.param


@pytest.fixture(scope="module")
def ticker() -> str:
    return "AAPL"


class TestISingleSourceRaises:
    def test(self, ticker: str):
        source = ISingleSource()
        with pytest.raises(NotImplementedError):
            source.get(
                ticker,
                DateRange.from_string("2021-08-03", "2021-08-04"),
            )


class TestISingleSourceDates:
    @pytest.mark.parametrize(
        "range_, expected",
        [
            (
                DateRange.from_string("2021-08-03", "2021-08-03"),
                DateSequence.from_string(["2021-08-03"]),
            ),
            (
                DateRange.from_string("2021-08-03", "2021-08-04"),
                DateSequence.from_string(["2021-08-03", "2021-08-04"]),
            ),
        ],
    )
    def test(
        self,
        source: ISingleSource,
        ticker: str,
        range_: DateRange,
        expected: DateSequence,
    ):
        result = source.get(ticker, range_)
        assert result.dates == expected


class TestISingleSourceInvalidTicker:
    def test(self, source: ISingleSource):
        result = source.get(
            "-",
            DateRange.from_string(
                "2021-08-03",
                "2021-08-04",
            ),  # days when the market was open!
        )
        assert result == DatedPriceSeries([])


class TestISingleSourceUnavailableData:
    def test_when_range_includes_only_days_in_the_future(
        self,
        source: ISingleSource,
        ticker: str,
    ):
        today = Date.today()
        range_ = DateRange(
            today.increment(),
            today.increment(by=8),
        )
        result = source.get(ticker, range_)
        assert result == DatedPriceSeries([])

    def test_when_range_includes_days_in_the_future(
        self,
        source: ISingleSource,
        ticker: str,
    ):
        today = Date.today()
        range_ = DateRange(
            today.decrement(by=8),
            today.increment(by=8),
        )
        result = source.get(ticker, range_)
        assert all(
            today.increment(by=by_) not in result.dates for by_ in range(1, 9)
        )

    def test_when_range_includes_only_days_prior_to_inception(
        self,
        source: ISingleSource,
        ticker: str,
    ):
        range_ = DateRange.from_string("1900-12-01", "1900-12-31")
        result = source.get(ticker, range_)
        assert result == DatedPriceSeries([])

    def test_when_range_includes_days_prior_to_inception(
        self,
        source: ISingleSource,
        ticker: str,
    ):
        inception = Date("1980-12-12")
        range_ = DateRange(
            inception.decrement(by=8),
            inception,
        )
        result = source.get(ticker, range_)
        assert result.dates == DateSequence([inception])

    @pytest.mark.parametrize(
        "range_, expected",
        [
            (
                DateRange.from_string(
                    "2021-09-12",
                    "2021-09-13",
                ),  # The 12th was a Sunday
                DateSequence.from_string(["2021-09-13"]),
            ),
            (
                DateRange.from_string(
                    "2021-09-10",
                    "2021-09-13",
                ),  # The 11th and 12th were respectively Saturday and Sunday
                DateSequence.from_string(["2021-09-10", "2021-09-13"]),
            ),
            (
                DateRange.from_string(
                    "2020-12-24",
                    "2020-12-25",
                ),  # The 25th is an holiday
                DateSequence.from_string(["2020-12-24"]),
            ),
            (
                DateRange.from_string(
                    "2020-12-25",
                    "2020-12-25",
                ),  # The 25th is an holiday
                DateSequence([]),
            ),
        ],
    )
    def test_when_range_includes_days_when_the_market_is_closed(
        self,
        source: ISingleSource,
        ticker: str,
        range_: DateRange,
        expected: DateSequence,
    ):
        result = source.get(ticker, range_)
        assert result.dates == expected
