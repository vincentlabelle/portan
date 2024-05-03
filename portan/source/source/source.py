from typing import Iterable, Union

from ..date.range import DateRange
from ..dated.price.series import DatedPriceSeries
from ..dated.prices.series import DatedPricesSeries
from .multiple import IMultipleSource
from .single import ISingleSource


class PriceSource:
    """Source of prices of financial instruments.

    Parameters
    ----------
    single: ISingleSource
        source of prices for a single financial instrument
    multiple: IMultipleSource
        source of prices for multiple financial instruments
    """

    def __init__(
        self,
        single: ISingleSource,
        multiple: IMultipleSource,
    ):
        self._single = single
        self._multiple = multiple

    @property
    def single(self) -> ISingleSource:
        """Source of prices for a single financial instrument. This
        is exposed for testing purposes only."""
        return self._single

    @property
    def multiple(self) -> IMultipleSource:
        """Source of prices for multiple financial instruments. This
        is exposed for testing purposes only."""
        return self._multiple

    def get(
        self,
        tickers: Union[str, Iterable[str]],
        range_: DateRange,
    ) -> Union[DatedPriceSeries, DatedPricesSeries]:
        """Get prices of `tickers` for business days inside `range_`.
        If `tickers` is an iterable then the prices returned are
        only for days where every financial instrument in `tickers`
        has a price available.

        Parameters
        ----------
        tickers
            ticker(s) of financial instrument(s) to extract prices for
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
        Union[DatedPriceSeries, DatedPricesSeries]
            fetched prices
        """
        if isinstance(tickers, str):
            return self._single.get(tickers, range_)
        return self._multiple.get(tickers, range_)
