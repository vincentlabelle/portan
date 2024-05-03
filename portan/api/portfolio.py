from typing import Dict, Iterable, Optional, SupportsInt, Tuple

import portan.library as lib
import portan.source as src

from .exception import PortanError, SourceError
from .source import Source


class Portfolio:
    """A portfolio of financial instruments as defined by its prices
    and returns over a specific time period.

    The time period (i.e., `range_`) defines the prices that will
    extracted from `source`. Thus, available prices within `range_`
    will be fetched, and the returns will be computed based on
    those prices. Both sides of `range_` are inclusive.

    Parameters
    ----------
    allocation: Dict[str, int]
        mapping of ticker (i.e., identifier of a financial instrument)
        to weight, where each weight is an integer corresponding to
        a percentage value (i.e., 25 is equal to 25%), and each
        ticker must be valid as per `source` (e.g., Apple's stock
        identifier is 'AAPL' for Yahoo)
    range_: Tuple[str, str]
        range of dates in ISO format (i.e., [begin, end])
    source: Source
        source of prices (e.g., Yahoo)

    Raises
    ------
    PortanError
        if the `allocation` values do not sum to 100,
        if `range_` contains values which do not represent dates in ISO format,
        if `range_` contains values which aren't valid dates in the Gregorian
        calendar, or
        if the second value in `range_` represents a date prior to the first
        value in `range_`
    """

    def __init__(
        self,
        allocation: Dict[str, SupportsInt],
        range_: Tuple[str, str],
        *,
        source: Source = Source.YAHOO,
    ):
        self._tickers, self._weights = self._convert_allocation(allocation)
        self._range: src.DateRange = self._convert_range(range_)
        self._source: src.PriceSource = self._convert_source(source)
        self._dated: Optional[src.DatedPricesSeries] = None

    def _convert_allocation(
        self,
        allocation: Dict[str, SupportsInt],
    ) -> Tuple[Iterable[str], lib.BalancedWeights]:
        try:
            weights = lib.BalancedWeights.from_int(allocation.values())
        except ValueError as err:
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"values of allocation must sum to 100"
            )
            raise PortanError(msg) from err
        return allocation.keys(), weights

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
        """Fetch the prices from source for this portfolio.

        Raises
        ------
        SourceError
            if there's an unexpected error when fetching prices from this
            portfolio's source, or
            if the fetched prices are in an unexpected format (e.g., non-finite
            prices)
        """
        try:
            self._dated = self._source.get(self._tickers, self._range)
        except src.SourceError as err:
            msg = "cannot fetch prices from source"
            raise SourceError(msg) from err

    @property
    def prices(self) -> Iterable[Tuple[str, Iterable[float]]]:
        """Get the prices for this portfolio. The dates (in ISO format)
        of the prices are also provided.

        The prices are provided per date, and each price corresponds
        to a different ticker on a given date. Moreover, the prices on a
        given date are ordered per ticker using the ordering of the
        tickers at instantiation of this portfolio.

        Raises
        ------
        PortanError
            if the prices for this portfolio were not fetched

        Returns
        -------
        Iterable[Tuple[str, Iterable[float]]]
            the prices for this portfolio
        """
        dated = self._get_dated_or_raise_if_none()
        return dated.to_basic()

    def mean(self) -> float:
        """Get the continuous annualized mean of this portfolio's
        returns.

        Raises
        ------
        PortanError
            if the prices for this portfolio were not fetched, or
            if the ratio of some of the prices fetched over their
            preceding price overflows or is very close to zero
            such that the continuous rate of return is undefined

        Returns
        -------
        float
            continuous annualized mean of this portfolio's returns
        """
        return float(self._wrapped.mean())

    def volatility(self) -> float:
        """Get the continuous annualized volatility of this portfolio's
        returns.

        Raises
        ------
        PortanError
            if the prices for this portfolio were not fetched, or
            if the ratio of some of the prices fetched over their
            preceding price overflows or is very close to zero
            such that the continuous rate of return is undefined

        Returns
        -------
        float
            continuous annualized volatility of this portfolio's returns
        """
        try:
            return float(self._wrapped.dispersion())
        except ValueError as err:
            msg = "cannot determine volatility; unexpected error occurred"
            raise PortanError(msg) from err

    def correlations(self) -> Iterable[Iterable[float]]:
        """Get the correlation matrix of the instruments in
        this portfolio.

        Raises
        ------
        PortanError
            if the prices for this portfolio were not fetched, or
            if the ratio of some of the prices fetched over their
            preceding price overflows or is very close to zero
            such that the continuous rate of return is undefined

        Returns
        -------
        Iterable[Iterable[float]]
            correlation matrix of the instruments in this portfolio
        """
        try:
            correlations = self._rates.correlations()
        except ValueError as err:
            msg = "cannot determine correlations; unexpected error occurred"
            raise PortanError(msg) from err
        return correlations.to_float()

    @property
    def _wrapped(self) -> lib.BrownianConverter:
        return lib.BrownianConverter(
            self._weighted,
            from_=lib.Frequency.DAILY,
            to=lib.Frequency.ANNUAL,
        )

    @property
    def _weighted(self) -> lib.Weighted:
        return lib.Weighted(self._weights, self._rates)

    @property
    def _rates(self) -> lib.RateMatrix:
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
    def _prices(self) -> lib.PriceMatrix:
        dated = self._get_dated_or_raise_if_none()
        if len(dated) == 0:  # corner case!
            # we ensure a length match with weights
            return lib.PriceMatrix.empties(len(self._weights))
        return lib.PriceMatrix.from_float(dated.prices)

    def _get_dated_or_raise_if_none(self) -> src.DatedPricesSeries:
        self._raise_if_dated_is_none()
        return self._dated

    def _raise_if_dated_is_none(self):
        if self._dated is None:
            msg = "cannot perform operation; prices must be fetched first"
            raise PortanError(msg)
