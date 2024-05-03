from math import isclose
from typing import Dict, Tuple

import pytest
from numpy import allclose

from portan.api.exception import PortanError
from portan.api.portfolio import Portfolio
from portan.api.source import Source


@pytest.fixture(scope="module")
def allocation() -> Dict[str, int]:
    return {"AAPL": 60, "SQ": 40}


@pytest.fixture(scope="module")
def range_() -> Tuple[str, str]:
    return "2021-07-30", "2021-08-31"


class TestPortfolioInvariants:
    @pytest.mark.parametrize(
        "allocation",
        [
            {"AAPL": 60, "SQ": 39},  # equals to 99
            {"AAPL": 60, "SQ": 41},  # equals to 101
            {"AAPL": 99},  # equals to 99
            {"AAPL": 101},  # equals to 101
            {},  # equals 0
        ],
    )
    def test_when_allocation_does_not_sum_to_one(
        self,
        allocation: Dict[str, int],
        range_: Tuple[str, str],
    ):
        with pytest.raises(PortanError, match="allocation must sum to 100"):
            Portfolio(allocation, range_)

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
        allocation: Dict[str, int],
        range_: Tuple[str, str],
    ):
        with pytest.raises(PortanError, match="values of range_"):
            Portfolio(allocation, range_)

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
        allocation: Dict[str, int],
        range_: Tuple[str, str],
    ):
        with pytest.raises(PortanError, match="values of range_"):
            Portfolio(allocation, range_)

    def test_when_invalid_range_values_relationship(
        self,
        allocation: Dict[str, int],
    ):
        range_ = ("2021-09-02", "2021-09-01")
        with pytest.raises(PortanError, match="values of range_"):
            Portfolio(allocation, range_)

    def test_when_ok(
        self,
        allocation: Dict[str, int],
        range_: Tuple[str, str],
    ):
        Portfolio(allocation, range_)  # does not raise

    def test_supports_all_sources(
        self,
        allocation: Dict[str, int],
        range_: Tuple[str, str],
    ):
        for source in Source:
            Portfolio(allocation, range_, source=source)  # does not raise


class TestPortfolioFetch:
    @pytest.mark.parametrize(
        "allocation, range_",
        [
            (
                {"BATMAN": 50, "AAPL": 50},  # invalid ticker
                ("2021-07-30", "2021-08-31"),
            ),
            (
                {"BATMAN": 100},  # invalid ticker
                ("2021-07-30", "2021-08-31"),
            ),
            (
                {"AAPL": 100},
                ("2021-09-18", "2021-09-19"),  # weekend
            ),
            (
                {"SQ": 50, "AAPL": 50},
                ("2021-09-18", "2021-09-19"),  # weekend
            ),
        ],
    )
    def test_when_no_prices(
        self,
        allocation: Dict[str, int],
        range_: Tuple[str, str],
    ):
        portfolio = Portfolio(allocation, range_)
        portfolio.fetch()
        assert tuple(portfolio.prices) == ()

    @pytest.mark.parametrize(
        "allocation, range_, expected",
        [
            (
                {"AAPL": 100},  # single instrument
                ("2021-10-01", "2021-10-05"),
                3,
            ),
            (
                {"AAPL": 50, "SQ": 50},
                ("2021-10-01", "2021-10-05"),  # after inceptions
                3,
            ),
            (
                {"AAPL": 50, "SQ": 50},
                ("2015-10-20", "2015-11-20"),  # during inception of SQ
                2,
            ),
        ],
    )
    def test_when_prices(
        self,
        allocation: Dict[str, int],
        range_: Tuple[str, str],
        expected: int,
    ):
        for source in Source:
            portfolio = Portfolio(allocation, range_, source=source)
            portfolio.fetch()
            result = portfolio.prices
            assert len(tuple(result)) == expected


class TestPortfolioPrices:
    def test_when_unfetched(
        self,
        allocation: Dict[str, int],
        range_: Tuple[str, str],
    ):
        portfolio = Portfolio(allocation, range_)
        with pytest.raises(PortanError, match="fetch"):
            portfolio.prices

    def test_when_fetched(self, allocation: Dict[str, int]):
        range_ = ("2021-10-01", "2021-10-05")
        portfolio = Portfolio(allocation, range_)
        portfolio.fetch()
        result = portfolio.prices
        assert len(tuple(result)) == 3

    def test_set(self, allocation: Dict[str, int], range_: Tuple[str, str]):
        portfolio = Portfolio(allocation, range_)
        with pytest.raises(AttributeError):
            portfolio.prices = ()


class _SupportsInt:
    def __init__(self, value: int):
        self._value = value

    def __int__(self) -> int:
        return self._value


class TestPortfolioMean:
    @pytest.fixture(scope="class")
    def absolute_tolerance(self) -> float:
        return 1e-4

    @pytest.fixture(scope="class")
    def relative_tolerance(self) -> float:
        return 0.0

    def test_when_unfetched(
        self,
        allocation: Dict[str, int],
        range_: Tuple[str, str],
    ):
        portfolio = Portfolio(allocation, range_)
        with pytest.raises(PortanError, match="fetch"):
            portfolio.mean()

    @pytest.mark.parametrize(
        "allocation",
        [
            {"BATMAN": 100},  # ticker doesn't exist
            {"AAPL": 50, "BATMAN": 50},  # ticker doesn't exist
        ],
    )
    def test_when_no_prices(
        self,
        allocation: Dict[str, int],
        range_: Tuple[str, str],
    ):
        portfolio = Portfolio(allocation, range_)
        portfolio.fetch()
        result = portfolio.mean()
        assert result == 0.0

    @pytest.mark.parametrize(
        "allocation",
        [
            {"AAPL": 100},
            {"AAPL": 60, "SQ": 40},
        ],
    )
    def test_when_one_price(self, allocation: Dict[str, int]):
        range_ = ("2021-09-20", "2021-09-20")
        portfolio = Portfolio(allocation, range_)
        portfolio.fetch()
        result = portfolio.mean()
        assert result == 0.0

    @pytest.mark.parametrize(
        "allocation, expected",
        [
            ({"AAPL": 100}, -6.27818241708764),
            ({"AAPL": 60, "SQ": 40}, -9.41529729097709),
        ],
    )
    def test_when_two_prices(
        self,
        allocation: Dict[str, int],
        absolute_tolerance: float,
        relative_tolerance: float,
        expected: float,
    ):
        range_ = ("2021-10-01", "2021-10-04")
        portfolio = Portfolio(allocation, range_)
        portfolio.fetch()
        result = portfolio.mean()
        assert isclose(
            result,
            expected,
            abs_tol=absolute_tolerance,
            rel_tol=relative_tolerance,
        )

    @pytest.mark.parametrize(
        "allocation, expected",
        [
            ({"AAPL": 100}, 0.4766397596250552),
            ({"AAPL": 60, "SQ": 40}, 0.656230375631595),
        ],
    )
    def test_when_multiple_prices(
        self,
        allocation: Dict[str, int],
        range_: Tuple[str, str],
        absolute_tolerance: float,
        relative_tolerance: float,
        expected: float,
    ):
        portfolio = Portfolio(allocation, range_)
        portfolio.fetch()
        result = portfolio.mean()
        assert isclose(
            result,
            expected,
            abs_tol=absolute_tolerance,
            rel_tol=relative_tolerance,
        )

    @pytest.mark.parametrize(
        "allocation, expected",
        [
            ({"AAPL": 100}, -6.27818241708764),
            ({"AAPL": 60, "SQ": _SupportsInt(40)}, -9.41529729097709),
        ],
    )
    def test_allocation_supports_int(
        self,
        allocation: Dict[str, int],
        absolute_tolerance: float,
        relative_tolerance: float,
        expected: float,
    ):
        range_ = ("2021-10-01", "2021-10-04")
        portfolio = Portfolio(allocation, range_)
        portfolio.fetch()
        result = portfolio.mean()
        assert isclose(
            result,
            expected,
            abs_tol=absolute_tolerance,
            rel_tol=relative_tolerance,
        )


class TestPortfolioVolatility:
    @pytest.fixture(scope="class")
    def absolute_tolerance(self) -> float:
        return 1e-6

    @pytest.fixture(scope="class")
    def relative_tolerance(self) -> float:
        return 0.0

    def test_when_unfetched(
        self,
        allocation: Dict[str, int],
        range_: Tuple[str, str],
    ):
        portfolio = Portfolio(allocation, range_)
        with pytest.raises(PortanError, match="fetch"):
            portfolio.volatility()

    @pytest.mark.parametrize(
        "allocation",
        [
            {"BATMAN": 100},  # ticker doesn't exist
            {"AAPL": 50, "BATMAN": 50},  # ticker doesn't exist
        ],
    )
    def test_when_no_prices(
        self,
        allocation: Dict[str, int],
        range_: Tuple[str, str],
    ):
        portfolio = Portfolio(allocation, range_)
        portfolio.fetch()
        result = portfolio.volatility()
        assert result == 0.0

    @pytest.mark.parametrize(
        "allocation",
        [
            {"AAPL": 100},
            {"AAPL": 60, "SQ": 40},
        ],
    )
    def test_when_one_price(self, allocation: Dict[str, int]):
        range_ = ("2021-09-20", "2021-09-20")
        portfolio = Portfolio(allocation, range_)
        portfolio.fetch()
        result = portfolio.volatility()
        assert result == 0.0

    @pytest.mark.parametrize(
        "allocation, expected",
        [
            ({"AAPL": 100}, -6.27818241708764),
            ({"AAPL": 60, "SQ": 40}, -9.41529729097709),
        ],
    )
    def test_when_two_prices(
        self,
        allocation: Dict[str, int],
        absolute_tolerance: float,
        relative_tolerance: float,
        expected: float,
    ):
        range_ = ("2021-10-01", "2021-10-04")
        portfolio = Portfolio(allocation, range_)
        portfolio.fetch()
        result = portfolio.volatility()
        assert result == 0.0

    @pytest.mark.parametrize(
        "allocation, expected",
        [
            ({"AAPL": 100}, 0.182530944534189),
            ({"AAPL": 60, "SQ": 40}, 0.223925754755883),
        ],
    )
    def test_when_multiple_prices(
        self,
        allocation: Dict[str, int],
        range_: Tuple[str, str],
        absolute_tolerance: float,
        relative_tolerance: float,
        expected: float,
    ):
        portfolio = Portfolio(allocation, range_)
        portfolio.fetch()
        result = portfolio.volatility()
        assert isclose(
            result,
            expected,
            abs_tol=absolute_tolerance,
            rel_tol=relative_tolerance,
        )


class TestPortfolioCorrelations:
    @pytest.fixture(scope="class")
    def absolute_tolerance(self) -> float:
        return 1e-4

    @pytest.fixture(scope="class")
    def relative_tolerance(self) -> float:
        return 0.0

    def test_when_unfetched(
        self,
        allocation: Dict[str, int],
        range_: Tuple[str, str],
    ):
        portfolio = Portfolio(allocation, range_)
        with pytest.raises(PortanError, match="fetch"):
            portfolio.correlations()

    @pytest.mark.parametrize(
        "range_, expected",
        [
            (
                ("2021-09-18", "2021-09-19"),
                ((0.0,),),
            ),  # weekend, no prices
            (
                ("2021-09-20", "2021-09-20"),
                ((0.0,),),
            ),  # one price
            (
                ("2021-10-01", "2021-10-04"),
                ((0.0,),),
            ),  # two prices
            (
                ("2021-07-30", "2021-08-31"),
                ((1.0,),),
            ),  # multiple prices
        ],
    )
    def test_when_one_instrument(
        self,
        range_: Tuple[str, str],
        expected: Tuple[Tuple[float, ...], ...],
    ):
        allocation = {"AAPL": 100}
        portfolio = Portfolio(allocation, range_)
        portfolio.fetch()
        result = self._correlations_as_tuples(portfolio)
        assert result == expected

    @pytest.mark.parametrize(
        "range_, expected",
        [
            (
                ("2021-09-18", "2021-09-19"),
                (
                    (0.0, 0.0),
                    (0.0, 0.0),
                ),
            ),  # weekend, no prices
            (
                ("2021-09-20", "2021-09-20"),
                (
                    (0.0, 0.0),
                    (0.0, 0.0),
                ),
            ),  # one price
            (
                ("2021-10-01", "2021-10-04"),
                (
                    (0.0, 0.0),
                    (0.0, 0.0),
                ),
            ),  # two prices
            (
                ("2021-07-30", "2021-08-31"),
                (
                    (1.0, 0.128918764143379),
                    (0.128918764143379, 1.0),
                ),
            ),  # multiple prices
        ],
    )
    def test_when_multiple_instruments(
        self,
        allocation: Dict[str, int],
        range_: Tuple[str, str],
        expected: Tuple[Tuple[float, ...], ...],
        absolute_tolerance: float,
        relative_tolerance: float,
    ):
        portfolio = Portfolio(allocation, range_)
        portfolio.fetch()
        result = self._correlations_as_tuples(portfolio)
        assert allclose(
            result,
            expected,
            atol=absolute_tolerance,
            rtol=relative_tolerance,
        )

    @staticmethod
    def _correlations_as_tuples(
        portfolio: Portfolio,
    ) -> Tuple[Tuple[float, ...], ...]:
        return tuple(map(lambda x: tuple(x), portfolio.correlations()))
