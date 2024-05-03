from math import isclose
from typing import Tuple

import pytest

from portan.api.exception import PortanError
from portan.api.instrument import Instrument
from portan.api.source import Source


@pytest.fixture(scope="module")
def ticker() -> str:
    return "AAPL"


@pytest.fixture(scope="module")
def range_() -> Tuple[str, str]:
    return "2021-07-30", "2021-08-31"


class TestInstrumentInvariants:
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
        ticker: str,
        range_: Tuple[str, str],
    ):
        with pytest.raises(PortanError, match="values of range_"):
            Instrument(ticker, range_)

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
        ticker: str,
        range_: Tuple[str, str],
    ):
        with pytest.raises(PortanError, match="values of range_"):
            Instrument(ticker, range_)

    def test_when_invalid_range_values_relationship(self, ticker: str):
        range_ = ("2021-09-02", "2021-09-01")
        with pytest.raises(PortanError, match="values of range_"):
            Instrument(ticker, range_)

    def test_when_valid_range_values(self, ticker: str):
        range_ = ("2021-09-01", "2021-09-02")
        Instrument(ticker, range_)  # does not raise

    def test_supports_all_sources(self, ticker: str, range_: Tuple[str, str]):
        for source in Source:
            Instrument(ticker, range_, source=source)  # does not raise


class TestInstrumentFetch:
    @pytest.mark.parametrize(
        "ticker, range_",
        [
            (
                "AAPL",
                ("2021-09-18", "2021-09-19"),  # weekend
            ),
            (
                "BATMAN",  # does not exist
                ("2021-09-20", "2021-09-21"),
            ),
        ],
    )
    def test_when_no_prices(self, ticker: str, range_: Tuple[str, str]):
        instrument = Instrument(ticker, range_)
        instrument.fetch()
        result = instrument.prices
        assert tuple(result) == ()

    def test_when_prices(self, ticker: str):
        range_ = ("2021-10-01", "2021-10-05")
        for source in Source:
            instrument = Instrument(ticker, range_, source=source)
            instrument.fetch()
            result = instrument.prices
            assert len(tuple(result)) == 3


class TestInstrumentPrices:
    def test_when_unfetched(self, ticker: str, range_: Tuple[str, str]):
        instrument = Instrument(ticker, range_)
        with pytest.raises(PortanError, match="fetch"):
            instrument.prices

    def test_when_fetched(self, ticker: str):
        range_ = ("2021-10-01", "2021-10-05")
        instrument = Instrument(ticker, range_)
        instrument.fetch()
        result = instrument.prices
        assert len(tuple(result)) == 3

    def test_set(self, ticker: str, range_: Tuple[str, str]):
        instrument = Instrument(ticker, range_)
        with pytest.raises(AttributeError):
            instrument.prices = ()


class TestInstrumentMean:
    @pytest.fixture(scope="class")
    def absolute_tolerance(self) -> float:
        return 1e-4

    @pytest.fixture(scope="class")
    def relative_tolerance(self) -> float:
        return 0.0

    def test_when_unfetched(self, ticker: str, range_: Tuple[str, str]):
        instrument = Instrument(ticker, range_)
        with pytest.raises(PortanError, match="fetch"):
            instrument.mean()

    def test_when_no_prices(self, range_: Tuple[str, str]):
        instrument = Instrument("BATMAN", range_)  # ticker doesn't exist
        instrument.fetch()
        result = instrument.mean()
        assert result == 0.0

    def test_when_one_price(self, ticker: str):
        range_ = ("2021-09-20", "2021-09-20")
        instrument = Instrument(ticker, range_)
        instrument.fetch()
        result = instrument.mean()
        assert result == 0.0

    def test_when_two_prices(
        self,
        ticker: str,
        absolute_tolerance: float,
        relative_tolerance: float,
    ):
        range_ = ("2021-10-01", "2021-10-04")
        instrument = Instrument(ticker, range_)
        instrument.fetch()
        result = instrument.mean()
        expected = -6.27818241708764
        assert isclose(
            result,
            expected,
            abs_tol=absolute_tolerance,
            rel_tol=relative_tolerance,
        )

    def test_when_multiple_prices(
        self,
        ticker: str,
        range_: Tuple[str, str],
        absolute_tolerance: float,
        relative_tolerance: float,
    ):
        instrument = Instrument(ticker, range_)
        instrument.fetch()
        result = instrument.mean()
        expected = 0.4766397596250552
        assert isclose(
            result,
            expected,
            abs_tol=absolute_tolerance,
            rel_tol=relative_tolerance,
        )


class TestInstrumentVolatility:
    @pytest.fixture(scope="class")
    def absolute_tolerance(self) -> float:
        return 1e-6

    @pytest.fixture(scope="class")
    def relative_tolerance(self) -> float:
        return 0.0

    def test_when_unfetched(self, ticker: str, range_: Tuple[str, str]):
        instrument = Instrument(ticker, range_)
        with pytest.raises(PortanError, match="fetch"):
            instrument.volatility()

    def test_when_no_prices(self, range_: Tuple[str, str]):
        instrument = Instrument("BATMAN", range_)  # ticker doesn't exist
        instrument.fetch()
        result = instrument.volatility()
        assert result == 0.0

    def test_when_one_price(self, ticker: str):
        range_ = ("2021-09-20", "2021-09-20")
        instrument = Instrument(ticker, range_)
        instrument.fetch()
        result = instrument.volatility()
        assert result == 0.0

    def test_when_two_prices(
        self,
        ticker: str,
        absolute_tolerance: float,
        relative_tolerance: float,
    ):
        range_ = ("2021-10-01", "2021-10-04")
        instrument = Instrument(ticker, range_)
        instrument.fetch()
        result = instrument.volatility()
        assert result == 0.0

    def test_when_multiple_prices(
        self,
        ticker: str,
        range_: Tuple[str, str],
        absolute_tolerance: float,
        relative_tolerance: float,
    ):
        instrument = Instrument(ticker, range_)
        instrument.fetch()
        result = instrument.volatility()
        expected = 0.182530944534189
        assert isclose(
            result,
            expected,
            abs_tol=absolute_tolerance,
            rel_tol=relative_tolerance,
        )
