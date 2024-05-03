from contextlib import redirect_stdout
from io import StringIO
from typing import Optional

from pandas import DataFrame, Series
from yfinance import Ticker

from .date import Date
from .date.range import DateRange
from .dated.price.series import DatedPriceSeries
from .exception import SourceError
from .source.single import ISingleSource

_SPLIT_NAME = "Stock Splits"
_DIVIDEND_NAME = "Dividends"
_CLOSE_NAME = "Close"


class Yahoo(ISingleSource):
    """Source of prices for a single instrument fetching from Yahoo Finance.

    Parameters
    ----------
    verbose: bool
        whether to display information to the console
    """

    def __init__(self, *, verbose: bool = False):
        self._verbose = verbose
        self._ticker: Optional[str] = None

    def get(self, ticker: str, range_: DateRange) -> DatedPriceSeries:
        """Get prices of `ticker` for business days inside `range_`.

        Parameters
        ----------
        ticker
            ticker of financial instrument to extract prices for
            (must match with tickers from Yahoo Finance)
        range_
            range delimiting the business days for which to extract prices
            (both side of the range are inclusive)

        Raises
        ------
        SourceError
            if there's an unexpected error when fetching prices from the
            source, or
            if the fetched prices are in an unexpected format (e.g., non-finite
            prices)

        Returns
        -------
        DatedPriceSeries
            fetched prices
        """
        self._ticker = ticker
        data = self._get(range_)
        return self._extract_prices_from(data)

    def _get(self, range_: DateRange) -> DataFrame:
        with redirect_stdout(StringIO()) as f:
            data = self._get_from_yahoo(range_)
        if self._verbose:
            print(f.getvalue())
        return data

    def _get_from_yahoo(self, range_: DateRange) -> DataFrame:
        try:
            return Ticker(self._ticker).history(
                start=str(range_.begin),
                end=str(self._increment(range_.end)),
                interval="1d",
                prepost=False,
                actions=True,
                auto_adjust=True,
                back_adjust=False,
                rounding=False,
            )
        except Exception as err:
            msg = (
                f"cannot source prices from Yahoo for {self._ticker}; "
                f"an unexpected error occurred when fetching prices"
            )
            raise SourceError(msg) from err

    def _increment(self, end: Date) -> Date:
        try:
            return end.increment()
        except OverflowError:
            msg = (
                f"cannot source prices from Yahoo for {self._ticker}; "
                f"end date of range_ must be lower than {end}"
            )
            raise SourceError(msg)

    def _extract_prices_from(self, data: DataFrame) -> DatedPriceSeries:
        if len(data) == 0:
            return DatedPriceSeries([])
        return self._extract_prices_when_non_empty(data)

    def _extract_prices_when_non_empty(
        self,
        data: DataFrame,
    ) -> DatedPriceSeries:
        filtered = self._remove_extraneous_actions(data)
        return self._to_dated(filtered)

    def _remove_extraneous_actions(self, data: DataFrame) -> DataFrame:
        return data.loc[~self._is_extraneous_actions(data)]

    @staticmethod
    def _is_extraneous_actions(data: DataFrame) -> Series:
        is_action = (data[_SPLIT_NAME] != 0.0) | (data[_DIVIDEND_NAME] != 0.0)
        return is_action & data[_CLOSE_NAME].isna()

    def _to_dated(self, data: DataFrame) -> DatedPriceSeries:
        try:
            return DatedPriceSeries.from_unsorted_basic(
                zip(
                    data.index.strftime("%Y-%m-%d"),
                    data[_CLOSE_NAME],
                )
            )
        except ValueError:
            msg = (
                f"cannot source prices from Yahoo for {self._ticker}; "
                f"data fetched is in an unexpected format, likely "
                f"cause is some prices which are non-finite "
                f"(i.e., NaN, inf or -inf), negative or zero, "
                f"or duplicated dates"
            )
            raise SourceError(msg)
