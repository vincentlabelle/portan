import pytest

from portan.library.optimisation.objective.linear import LinearCoefficients


class TestLinearCoefficientsProperties:
    @pytest.fixture(scope="class")
    def sequence(self) -> LinearCoefficients:
        return LinearCoefficients.from_float([1.0, 2.0, 3.0])

    def test_n(self, sequence: LinearCoefficients):
        assert sequence.n == len(sequence)

    def test_set_n(self, sequence: LinearCoefficients):
        with pytest.raises(AttributeError):
            sequence.n = 0


class TestLinearCoefficientsEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> LinearCoefficients:
        return LinearCoefficients([])

    def test_n(self, sequence: LinearCoefficients):
        assert sequence.n == 0
