import pytest

from portan.library.optimisation.coefficient import Coefficient
from portan.library.optimisation.coefficient.sequence import CoefficientSequence


class TestCoefficientSequenceAlternativeConstructors:
    @pytest.fixture(scope="class")
    def coefficients(self) -> CoefficientSequence:
        return CoefficientSequence(
            [
                Coefficient(1.0),
                Coefficient(2.0),
            ]
        )

    def test_from_float(self, coefficients: CoefficientSequence):
        result = CoefficientSequence.from_float(
            float(value) for value in coefficients
        )
        assert result == coefficients

    def test_from_float_supports_float(self, coefficients: CoefficientSequence):
        result = CoefficientSequence.from_float(coefficients)
        assert result == coefficients


class TestCoefficientSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> CoefficientSequence:
        return CoefficientSequence([])

    def test_from_float(self, sequence: CoefficientSequence):
        assert CoefficientSequence.from_float([]) == sequence
