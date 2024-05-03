from typing import Optional

from ..price.series import DatedPriceSeries
from .series import DatedPricesSeries


class DatedPricesSeriesBuilder:
    """Builder of :py:class:`DatedPricesSeries` from multiple
    :py:class:`DatedPriceSeries`. The builder creates a
    :py:class:`DatedPricesSeries` from all intersecting
    dates in the :py:class:`DatedPriceSeries` added.
    """

    def __init__(self):
        self._series: Optional[DatedPricesSeries] = None

    def add(self, single: DatedPriceSeries):
        """Add a :py:class:`DatedPriceSeries` to the
        :py:class:`DatedPricesSeries` being built.

        Parameters
        ----------
        single
            series of single financial instrument prices
            to add to the :py:class:`DatedPricesSeries`
            being built
        """
        if self._series is None:
            self._series = DatedPricesSeries.from_single(single)
        else:
            self._add(single)

    def _add(self, single: DatedPriceSeries):
        intersection = self._series.dates.intersect(single.dates)
        new = self._series.compress(intersection)
        compressed = single.compress(intersection)
        self._series = new.add(compressed)

    def get(self) -> DatedPricesSeries:
        """Get the :py:class:`DatedPricesSeries` built using this
        builder.

        Raises
        ------
        RuntimeError
            if no :py:class:`DatedPriceSeries` were added

        Returns
        -------
        DatedPricesSeries
            built series
        """
        self._raise_if_series_is_none()
        return self._series

    def _raise_if_series_is_none(self):
        if self._series is None:
            msg = "cannot get; must add singles before"
            raise RuntimeError(msg)
