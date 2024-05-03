from typing import Iterable, Optional, Tuple

import portan.library as lib
import portan.source as src

from .exception import PortanError, SourceError
from .source import Source


class Instrument:
    """A financial instrument as defined by its prices and returns
    over a specific time period.

    The time period (i.e., `range_`) defines the prices that will
    extracted from `source`. Thus, available prices within `range_`
    will be fetched, and the returns will be computed based on
    those prices. Both sides of `range_` are inclusive.

    Parameters
    ----------
    ticker: str
        identifier of the financial instrument as per `source`
        (e.g., Apple's stock identifier is 'AAPL' for Yahoo)
    range_: Tuple[str, str]
        range of dates in ISO format (i.e., [begin, end])
    source: Source
        source of prices (e.g., Yahoo)

    Raises
    ------
    PortanError
        if `range_` contains values which do not represent dates in ISO format,
        if `range_` contains values which aren't valid dates in the Gregorian
        calendar, or
        if the second value in `range_` represents a date prior to the first
        value in `range_`
    """

    def __init__(
        self,
        ticker: str,
        range_: Tuple[str, str],
        *,
        source: Source = Source.YAHOO,
    ):
        self._ticker = ticker
        self._range: src.DateRange = self._convert_range(range_)
        self._source: src.PriceSource = self._convert_source(source)
        self._dated: Optional[src.DatedPriceSeries] = None

    def _convert_range(self, range_: Tuple[str, str]) -> src.DateRange:
        try:
            return src.DateRange.from_string(*range_)
        except ValueError as err:
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"values of range_ should represent valid dates of "
                f"the Gregorian calendar in ISO format (i.e., YYYY-MM-DD), "
                f"and the second date should *not* be prior to the first date"
            )
            raise PortanError(msg) from err

    def _convert_source(self, source: Source) -> src.PriceSource:
        factory = src.PriceSourceFactory()
        try:
            return factory.get(source.value)
        except ValueError as err:
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"unknown source"
            )
            raise PortanError(msg) from err

    def fetch(self):
        """Fetch the prices from source for this instrument.

        Raises
        ------
        SourceError
            if there's an unexpected error when fetching prices from this
            instrument's source, or
            if the fetched prices are in an unexpected format (e.g., non-finite
            prices)
        """
        try:
            self._dated = self._source.get(self._ticker, self._range)
        except src.SourceError as err:
            msg = "cannot fetch prices from source"
            raise SourceError(msg) from err

    @property
    def prices(self) -> Iterable[Tuple[str, float]]:
        """Get the prices for this instrument. The dates (in ISO format)
        of the prices are also provided.

        Raises
        ------
        PortanError
            if the prices for this instrument were not fetched

        Returns
        -------
        Iterable[Tuple[str, float]]
            the prices for this instrument
        """
        dated = self._get_dated_or_raise_if_none()
        return dated.to_basic()

    def mean(self) -> float:
        """Get the annualized mean of the continuous returns
        of this instrument.

        Raises
        ------
        PortanError
            if the prices for this instrument were not fetched, or
            if the ratio of some of the prices fetched over their
            preceding price overflows or is very close to zero
            such that the continuous rate of return is undefined

        Returns
        -------
        float
            annualized mean of the continuous returns of this instrument
        """
        return float(self._wrapped.mean())

    def volatility(self) -> float:
        """Get the annualized volatility of the continuous returns
        of this instrument.

        Raises
        ------
        PortanError
            if the prices for this instrument were not fetched, or
            if the ratio of some of the prices fetched over their
            preceding price overflows or is very close to zero
            such that the continuous rate of return is undefined

        Returns
        -------
        float
            annualized volatility of the continuous returns of
            this instrument
        """
        return float(self._wrapped.dispersion())

    @property
    def _wrapped(self) -> lib.BrownianConverter:
        return lib.BrownianConverter(
            self._rates,
            from_=lib.Frequency.DAILY,
            to=lib.Frequency.ANNUAL,
        )

    @property
    def _rates(self) -> lib.RateSequence:
        try:
            return self._prices.growth()
        except ValueError as err:
            msg = (
                "cannot determine rates of growth(return); "
                "ratio of some of the prices fetched over their preceding "
                "price is close or equal to infinity or zero leading to "
                "undefined continuous rates of growth"
            )
            raise PortanError(msg) from err

    @property
    def _prices(self) -> lib.PriceSequence:
        dated = self._get_dated_or_raise_if_none()
        return lib.PriceSequence.from_float(dated.prices)

    def _get_dated_or_raise_if_none(self) -> src.DatedPriceSeries:
        self._raise_if_dated_is_none()
        return self._dated

    def _raise_if_dated_is_none(self):
        if self._dated is None:
            msg = "cannot perform operation; prices must be fetched first"
            raise PortanError(msg)
