from math import inf, nan
from typing import Dict, Tuple

import pytest

from portan.api.exception import InfeasibleError, PortanError
from portan.api.mvo import MVO
from portan.api.source import Source


@pytest.fixture(scope="module")
def tickers() -> Tuple[str, ...]:
    return "AAPL", "SQ"


@pytest.fixture(scope="module")
def range_() -> Tuple[str, str]:
    return "2021-07-30", "2021-08-31"


@pytest.fixture(scope="module")
def minimum() -> float:
    return 0.05


@pytest.fixture(scope="module")
def optimiser() -> MVO:
    return MVO()


class TestMVOOptimise:
    @pytest.mark.parametrize(
        "range_",
        [
            ("1-01-01", "0001-01-01"),
            ("0001-01-01", "1-01-01"),
            ("1-01-01", "1-01-01"),
        ],
    )
    def test_when_invalid_range_values_format(
        self,
        optimiser: MVO,
        tickers: Tuple[str, ...],
        range_: Tuple[str, str],
        minimum: float,
    ):
        with pytest.raises(PortanError, match="values of range_"):
            optimiser.optimise(tickers, range_, minimum=minimum)

    @pytest.mark.parametrize(
        "range_",
        [
            ("0001-02-31", "0001-01-01"),
            ("0001-01-01", "0001-02-31"),
            ("0001-02-31", "0001-02-31"),
        ],
    )
    def test_when_invalid_range_values_dates(
        self,
        optimiser: MVO,
        tickers: Tuple[str, ...],
        range_: Tuple[str, str],
        minimum: float,
    ):
        with pytest.raises(PortanError, match="values of range_"):
            optimiser.optimise(tickers, range_, minimum=minimum)

    def test_when_invalid_range_values_relationship(
        self,
        optimiser: MVO,
        tickers: Tuple[str, ...],
        minimum: float,
    ):
        range_ = ("2021-09-02", "2021-09-01")
        with pytest.raises(PortanError, match="values of range_"):
            optimiser.optimise(tickers, range_, minimum=minimum)

    @pytest.mark.parametrize("minimum", [nan, inf, -inf])
    def test_when_invalid_minimum(
        self,
        optimiser: MVO,
        tickers: Tuple[str, ...],
        range_: Tuple[str, str],
        minimum: float,
    ):
        with pytest.raises(PortanError, match="must be finite"):
            optimiser.optimise(tickers, range_, minimum=minimum)

    def test_supports_all_sources(
        self,
        optimiser: MVO,
        tickers: Tuple[str, ...],
    ):
        range_ = ("2021-09-01", "2021-09-01")
        for source in Source:
            optimiser.optimise(
                tickers,
                range_,
                minimum=0.0,
                source=source,
            )  # does not raise

    def test_when_no_tickers(
        self,
        optimiser: MVO,
        range_: Tuple[str, str],
    ):
        result = optimiser.optimise((), range_, minimum=0.0)
        assert result == {}

    @pytest.mark.parametrize(
        "range_",
        [
            ("2021-09-18", "2021-09-19"),  # weekend -> no prices
            ("2021-09-20", "2021-09-20"),  # one price
            ("2021-10-01", "2021-10-04"),  # two prices
            ("2021-07-30", "2021-08-31"),  # multiple prices
        ],
    )
    def test_when_one_ticker(
        self,
        optimiser: MVO,
        range_: Tuple[str, str],
    ):
        tickers = ("AAPL",)
        result = optimiser.optimise(tickers, range_, minimum=-10.0)
        assert result == {"AAPL": 100}

    @pytest.mark.parametrize(
        "range_",
        [
            ("2021-09-18", "2021-09-19"),  # weekend -> no prices
            ("2021-09-20", "2021-09-20"),  # one price
            ("2021-10-01", "2021-10-04"),  # two prices
        ],
    )
    def test_when_multiple_tickers_and_covariances_of_zero(
        self,
        optimiser: MVO,
        tickers: Tuple[str, ...],
        range_: Tuple[str, str],
    ):
        result = optimiser.optimise(tickers, range_, minimum=-20.0)
        assert result == {"AAPL": 50, "SQ": 50}

    @pytest.mark.parametrize(
        "source, expected",
        [
            (Source.YAHOO, {"AAPL": 90, "SQ": 10}),
        ],
    )  # TODO verify the results with an additional source
    def test_when_multiple_tickers_and_non_zero_covariances(
        self,
        optimiser: MVO,
        tickers: Tuple[str, ...],
        range_: Tuple[str, str],
        source: Source,
        expected: Dict[str, int],
    ):
        result = optimiser.optimise(tickers, range_, minimum=0.5, source=source)
        assert result == expected

    def test_when_minimum_is_too_high(
        self,
        optimiser: MVO,
        tickers: Tuple[str, ...],
        range_: Tuple[str, str],
    ):
        with pytest.raises(InfeasibleError):
            optimiser.optimise(tickers, range_, minimum=10.0)

    def test_when_minimum_supports_float(
        self,
        optimiser: MVO,
        tickers: Tuple[str, ...],
    ):
        class _SupportsFloat:
            def __float__(self) -> float:
                return -20.0

        range_ = ("2021-10-01", "2021-10-04")
        result = optimiser.optimise(tickers, range_, minimum=_SupportsFloat())
        assert result == {"AAPL": 50, "SQ": 50}

    def test_when_repeated_tickers(
        self,
        optimiser: MVO,
    ):
        tickers = ("AAPL", "AAPL")
        range_ = ("2021-10-01", "2021-10-04")
        result = optimiser.optimise(tickers, range_, minimum=-20.0)
        assert result == {"AAPL": 100}

    def test_when_ticker_is_invalid(
        self,
        optimiser: MVO,
    ):
        tickers = ("BATMAN",)
        range_ = ("2021-10-01", "2021-10-04")
        result = optimiser.optimise(tickers, range_, minimum=-20.0)
        assert result == {"BATMAN": 100}
