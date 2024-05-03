import pytest

from portan.library.scatter.covariance import Covariance
from portan.library.scatter.covariance.sequence import CovarianceSequence


class TestCovarianceSequenceAlternativeConstructors:
    @pytest.fixture(scope="class")
    def sequence(self) -> CovarianceSequence:
        return CovarianceSequence(
            [
                Covariance(0.1),
                Covariance(0.2),
                Covariance(0.3),
            ]
        )

    def test_from_float(self, sequence: CovarianceSequence):
        result = CovarianceSequence.from_float(
            float(value) for value in sequence
        )
        assert result == sequence

    def test_from_float_supports_float(self, sequence: CovarianceSequence):
        result = CovarianceSequence.from_float(sequence)
        assert result == sequence


class TestCovarianceSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> CovarianceSequence:
        return CovarianceSequence([])

    def test_from_float(self, sequence: CovarianceSequence):
        assert CovarianceSequence.from_float([]) == sequence
