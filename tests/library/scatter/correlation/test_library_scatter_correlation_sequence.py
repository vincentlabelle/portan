import pytest

from portan.library.scatter.correlation import Correlation
from portan.library.scatter.correlation.sequence import CorrelationSequence


class TestCorrelationSequenceAlternativeConstructors:
    @pytest.fixture(scope="class")
    def sequence(self) -> CorrelationSequence:
        return CorrelationSequence(
            [
                Correlation(0.1),
                Correlation(0.2),
                Correlation(0.3),
            ]
        )

    def test_from_float(self, sequence: CorrelationSequence):
        result = CorrelationSequence.from_float(
            float(value) for value in sequence
        )
        assert result == sequence

    def test_from_float_supports_float(self, sequence: CorrelationSequence):
        result = CorrelationSequence.from_float(sequence)
        assert result == sequence


class TestCorrelationSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> CorrelationSequence:
        return CorrelationSequence([])

    def test_from_float(self, sequence: CorrelationSequence):
        assert CorrelationSequence.from_float([]) == sequence
