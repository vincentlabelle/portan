from typing import Iterable, Tuple

from ..date.range import DateRange
from ..dated.prices.builder import DatedPricesSeriesBuilder
from ..dated.prices.series import DatedPricesSeries
from .single import ISingleSource


class IMultipleSource:
    """Interface for sources of prices for multiple financial instruments."""

    def get(
        self,
        tickers: Iterable[str],
        range_: DateRange,
    ) -> DatedPricesSeries:
        """Get prices of all tickers in `tickers` for business days inside
        `range_`. The prices returned are only for days where every financial
        instrument in `tickers` has a price available.

        Parameters
        ----------
        tickers
            tickers of financial instruments to extract prices for
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
        DatedPricesSeries
            fetched prices
        """
        tickers_ = tuple(tickers)  # freeze!
        if len(tickers_) == 0:
            return DatedPricesSeries([])
        return self._get(tickers_, range_)

    def _get(
        self,
        tickers: Tuple[str, ...],
        range_: DateRange,
    ) -> DatedPricesSeries:
        raise NotImplementedError


class MultipleSource(IMultipleSource):
    """Source of prices for multiple financial instruments fetching
    prices for each instrument individually from a :py:class:`ISingleSource`
    and combining them.

    Parameters
    ----------
    single: ISingleSource
        source of prices for single financial instrument from which to
        fetch individual instrument prices
    """

    def __init__(self, single: ISingleSource):
        self._single = single

    @property
    def single(self) -> ISingleSource:
        """Source of prices for single financial instrument from which
        to fetch individual instrument prices. This is exposed for testing
        purposes only."""
        return self._single

    def _get(
        self,
        tickers: Tuple[str, ...],
        range_: DateRange,
    ) -> DatedPricesSeries:
        builder = DatedPricesSeriesBuilder()
        for ticker in tickers:
            builder.add(self._single.get(ticker, range_))
        return builder.get()
