from ..date.range import DateRange
from ..dated.price.series import DatedPriceSeries


class ISingleSource:
    """Interface for sources of prices for a single financial instrument."""

    def get(self, ticker: str, range_: DateRange) -> DatedPriceSeries:
        """Get prices of `ticker` for business days inside `range_`.

        Parameters
        ----------
        ticker
            ticker of financial instrument to extract prices for
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
        raise NotImplementedError
