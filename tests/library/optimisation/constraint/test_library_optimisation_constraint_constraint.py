import pytest

from portan.library.optimisation.coefficient.sequence import CoefficientSequence
from portan.library.optimisation.constraint import Constraint
from portan.library.optimisation.constraint.bound import Bound


@pytest.fixture(scope="module")
def coefficients() -> CoefficientSequence:
    return CoefficientSequence.from_float([1.0, 2.0, 3.0])


@pytest.fixture(scope="module")
def bound() -> Bound:
    return Bound(1.0)


@pytest.fixture(scope="module")
def constraint(coefficients: CoefficientSequence, bound: Bound) -> Constraint:
    return Constraint(coefficients, bound)


class TestConstraintAlternativeConstructors:
    def test_from_float(
        self,
        constraint: Constraint,
        coefficients: CoefficientSequence,
        bound: Bound,
    ):
        result = Constraint.from_float(
            (float(value) for value in coefficients),
            float(bound),
        )
        assert result == constraint

    def test_from_float_supports_float(
        self,
        constraint: Constraint,
        coefficients: CoefficientSequence,
        bound: Bound,
    ):
        result = Constraint.from_float(coefficients, bound)
        assert result == constraint

    def test_from_float_when_empty(self, bound: Bound):
        result = Constraint.from_float([], bound)
        expected = Constraint(CoefficientSequence([]), bound)
        assert result == expected


class TestConstraintStringRepresentation:
    def test_str(
        self,
        constraint: Constraint,
        coefficients: CoefficientSequence,
        bound: Bound,
    ):
        expected = f"(coefficients={coefficients}, bound={bound})"
        assert str(constraint) == expected

    def test_repr(self, constraint: Constraint):
        expected = f"<{constraint.__class__.__name__}{constraint}>"
        assert repr(constraint) == expected


class TestConstraintEqual:
    def test_when_equal(
        self,
        constraint: Constraint,
        coefficients: CoefficientSequence,
        bound: Bound,
    ):
        other = Constraint(coefficients, bound)
        assert other == constraint

    def test_when_different_coefficients(
        self,
        constraint: Constraint,
        bound: Bound,
    ):
        coefficients = CoefficientSequence([])
        other = Constraint(coefficients, bound)
        assert other != constraint

    def test_when_different_bound(
        self,
        constraint: Constraint,
        coefficients: CoefficientSequence,
    ):
        bound = Bound(0.0)
        other = Constraint(coefficients, bound)
        assert other != constraint

    def test_when_different_object(self, constraint: Constraint):
        assert constraint != "a"


class TestConstraintHash:
    def test_when_equal(
        self,
        constraint: Constraint,
        coefficients: CoefficientSequence,
        bound: Bound,
    ):
        other = Constraint(coefficients, bound)
        assert hash(other) == hash(constraint)

    def test_when_different_coefficients(
        self,
        constraint: Constraint,
        bound: Bound,
    ):
        coefficients = CoefficientSequence([])
        other = Constraint(coefficients, bound)
        assert hash(other) != hash(constraint)

    def test_when_different_bound(
        self,
        constraint: Constraint,
        coefficients: CoefficientSequence,
    ):
        bound = Bound(0.0)
        other = Constraint(coefficients, bound)
        assert hash(other) != hash(constraint)


class TestConstraintProperties:
    def test_coefficients(
        self,
        constraint: Constraint,
        coefficients: CoefficientSequence,
    ):
        assert constraint.coefficients == coefficients

    def test_set_coefficients(
        self,
        constraint: Constraint,
        coefficients: CoefficientSequence,
    ):
        with pytest.raises(AttributeError):
            constraint.coefficients = coefficients

    def test_bound(
        self,
        constraint: Constraint,
        bound: Bound,
    ):
        assert constraint.bound == bound

    def test_set_bound(
        self,
        constraint: Constraint,
        bound: Bound,
    ):
        with pytest.raises(AttributeError):
            constraint.bound = bound
