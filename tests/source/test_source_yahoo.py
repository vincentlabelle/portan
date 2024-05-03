import pytest

from portan.source.date import MAX_YEAR
from portan.source.date.range import DateRange
from portan.source.date.sequence import DateSequence
from portan.source.exception import SourceError
from portan.source.yahoo import Yahoo


@pytest.fixture(scope="module")
def source() -> Yahoo:
    return Yahoo()


@pytest.fixture(scope="module")
def ticker() -> str:
    return "AAPL"


class TestYahooSpecialCase:
    @pytest.mark.parametrize(
        "range_, expected",
        [
            (
                DateRange.from_string(
                    "2021-08-04",
                    "2021-08-05",
                ),  # The API generates a NaN due to a dividend on the 6th
                DateSequence.from_string(["2021-08-04", "2021-08-05"]),
            ),
            (
                DateRange.from_string(
                    "2021-08-04",
                    "2021-08-06",
                ),  # The API correctly extracts the closing prices
                DateSequence.from_string(
                    [
                        "2021-08-04",
                        "2021-08-05",
                        "2021-08-06",
                    ]
                ),
            ),
            (
                DateRange.from_string(
                    "2020-08-27",
                    "2020-08-30",
                ),  # The API generates a NaN due to a split on the 31st
                DateSequence.from_string(["2020-08-27", "2020-08-28"]),
            ),
            (
                DateRange.from_string(
                    "2020-08-27",
                    "2020-08-31",
                ),  # The API correctly extracts the closing prices
                DateSequence.from_string(
                    [
                        "2020-08-27",
                        "2020-08-28",
                        "2020-08-31",
                    ]
                ),
            ),
        ],
    )
    def test_when_action_generate_extraneous_nan(
        self,
        source: Yahoo,
        ticker: str,
        range_: DateRange,
        expected: DateSequence,
    ):
        # The Yahoo API sometimes extract an extraneous closing price
        # with a NaN value when there's a corporate action (i.e., dividend
        # payment or stock split).
        # We verify that we successfully remove an action day closing price
        # if the closing price is NaN.
        result = source.get(ticker, range_)
        assert result.dates == expected

    def test_when_range_end_is_maximum_date(self, source: Yahoo, ticker: str):
        range_ = DateRange.from_string(
            "2021-09-01",
            f"{str(MAX_YEAR).zfill(4)}-12-31",
        )
        with pytest.raises(SourceError):
            source.get(ticker, range_)


class TestYahooVerbose:
    @pytest.mark.parametrize("verbose", [True, False])
    def test(self, capsys, verbose: bool):
        source = Yahoo(verbose=verbose)
        source.get(
            "-",
            DateRange.from_string("2021-08-03", "2021-08-03"),
        )
        captured = capsys.readouterr()
        if verbose:
            assert captured.out != ""
        else:
            assert captured.out == ""
