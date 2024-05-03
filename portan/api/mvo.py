from typing import Dict, Iterable, Optional, SupportsFloat, Tuple

import portan.library as lib
import portan.source as src

from .exception import InfeasibleError, PortanError, SourceError
from .source import Source

# TODO reduce duplication in API


class MVO:
    """Asset-based mean-variance optimiser for a collection of financial
    instruments. The optimiser finds the optimal allocation amongst
    the financial instruments that minimizes volatility while
    achieving a specific minimum expected return."""

    def __init__(self):
        self._tickers: Optional[Tuple[str, ...]] = None
        self._range: Optional[src.DateRange] = None
        self._minimum: Optional[lib.Rate] = None
        self._source: Optional[src.PriceSource] = None

    def optimise(
        self,
        tickers: Iterable[str],
        range_: Tuple[str, str],
        *,
        minimum: SupportsFloat,
        source: Source = Source.YAHOO,
    ) -> Dict[str, int]:
        """Find the optimal allocation between the financial instruments
        identified by `tickers` by using historical prices.

        The time period (i.e., `range_`) defines the prices that will
        extracted from `source`. Thus, available prices within `range_`
        will be fetched, and the returns will be computed based on
        those prices. Both sides of `range_` are inclusive.

        The minimum acceptable expected rate of return must be
        selected carefully has the optimisation problem may be infeasible
        if `minimum` is too high.

        In the event, where the covariance between financial instruments
        is undefined (e.g., less than two rates of return by instrument)
        the optimisation will allocate between each instrument equally
        unless allocating equally would not achieve the minimum
        acceptable expected rate of return.

        Parameters
        ----------
        tickers
            identifiers of financial instruments on which to
            perform the optimisation, where each ticker must be
            valid as per `source` (e.g., Apple's stock identifier
            is `AAPL` for Yahoo)
        range_
            ranges of dates in ISO format (i.e., [begin, end])
        minimum
            minimum acceptable expected annual **continuous** rate of return
        source
            source of prices (e.g., Yahoo)

        Raises
        ------
        PortanError
            if `range_` contains values which do not represent dates
            in ISO format,
            if `range_` contains values which aren't valid dates in
            the Gregorian calendar,
            if the second value in `range_` represents a date prior to
            the first value in `range_`,
            if `minimum` is nan,
            if some of the financial instruments selected have a non-finite
            mean or non-finite covariance,
            if the solver failed to find the solution,
            if the conversion of the solution to integer failed, or
            if the ratio of some of the prices fetched (for any
            financial instrument) over their preceding price overflows
            or is very close to zero such that the continuous rate
            of return is undefined
        InfeasibleError
            if the problem appears infeasible
        SourceError
            if there's an unexpected error when fetching prices, or
            if the fetched prices are in an unexpected format (e.g., non-finite
            prices)

        Returns
        -------
        Dict[str, int]
            mapping of tickers to weights (i.e., optimal allocation),
            where weights are integers corresponding to percentage
            values (i.e., 25 is 25%)
        """
        self._setup(tickers, range_, minimum, source)
        weights = self._optimise()
        return self._map_to_tickers(weights)

    def _setup(
        self,
        tickers: Iterable[str],
        range_: Tuple[str, str],
        minimum: SupportsFloat,
        source: Source,
    ):
        self._tickers = self._convert_tickers(tickers)
        self._range = self._convert_range(range_)
        self._minimum = self._convert_minimum(minimum)
        self._source = self._convert_source(source)

    @staticmethod
    def _convert_tickers(tickers: Iterable[str]) -> Tuple[str, ...]:
        return tuple(set(tickers))

    @staticmethod
    def _convert_range(range_: Tuple[str, str]) -> src.DateRange:
        try:
            return src.DateRange.from_string(*range_)
        except ValueError as err:
            msg = (
                "cannot optimise; values of range_ should represent "
                "valid dates of the Gregorian calendar in ISO "
                "format (i.e., YYYY-MM-DD), and the second date "
                "should *not* be prior to the first date"
            )
            raise PortanError(msg) from err

    @staticmethod
    def _convert_minimum(minimum: SupportsFloat) -> lib.Rate:
        try:
            return lib.Rate(minimum).convert(
                from_=lib.Frequency.ANNUAL,
                to=lib.Frequency.DAILY,
            )
        except ValueError as err:
            msg = "cannot optimise; minimum must be finite"
            raise PortanError(msg) from err

    @staticmethod
    def _convert_source(source: Source) -> src.PriceSource:
        factory = src.PriceSourceFactory()
        try:
            return factory.get(source.value)
        except ValueError as err:
            msg = "cannot optimise; unknown source"
            raise PortanError(msg) from err

    def _optimise(self):
        try:
            return self._optimiser.optimise(self._rates, self._minimum)
        except ValueError as err:
            msg = (
                "cannot optimise; some financial instruments selected "
                "have a non-finite mean, or non-finite covariance"
            )
            raise PortanError(msg) from err
        except lib.InfeasibleError as err:
            msg = (
                "cannot optimise; problem appears infeasible, consider "
                "reducing minimum"
            )
            raise InfeasibleError(msg) from err
        except lib.SolverError as err:
            msg = "optimisation failed; the solver failed to find the solution"
            raise PortanError(msg) from err
        except OverflowError as err:
            msg = (
                "conversion of solution to integer failed; some solutions "
                "of the solver are too big in absolute terms"
            )
            raise PortanError(msg) from err

    @property
    def _optimiser(self) -> lib.MeanVarianceOptimiser:
        return lib.MeanVarianceOptimiser.default(
            lib.OSQPSolver(),
        )

    @property
    def _rates(self) -> lib.RateMatrix:
        try:
            return self._prices.growth()
        except ValueError as err:
            msg = (
                "cannot optimise; unable to determine rates of "
                "growth(return) for financial instruments, ratio of "
                "some of the prices fetched over their preceding price "
                "is close or equal to infinity or zero leading to "
                "undefined continuous rates of growth"
            )
            raise PortanError(msg) from err

    @property
    def _prices(self) -> lib.PriceMatrix:
        dated = self._dated  # cache (operation is long)!
        if len(dated) == 0:  # corner case!
            # we ensure a length match with weights
            return lib.PriceMatrix.empties(len(self._tickers))
        return lib.PriceMatrix.from_float(dated.prices)

    @property
    def _dated(self) -> src.DatedPricesSeries:
        try:
            return self._source.get(self._tickers, self._range)
        except src.SourceError as err:
            msg = "cannot fetch prices from source"
            raise SourceError(msg) from err

    def _map_to_tickers(self, weights: lib.WeightSequence) -> Dict[str, int]:
        return {
            ticker: int(weight)
            for ticker, weight in zip(self._tickers, weights)
        }
