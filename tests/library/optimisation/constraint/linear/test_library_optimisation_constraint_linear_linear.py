from typing import Optional

import pytest

from portan.library.optimisation.constraint.linear import LinearConstraints
from portan.library.optimisation.constraint.linear.equalities import (
    LinearEqualities,
)
from portan.library.optimisation.constraint.linear.inequalities import (
    LinearInequalities,
)


class TestLinearConstraintsInvariants:
    @pytest.mark.parametrize("n", [1, 3])
    def test_when_n_mismatch_and_non_empty(self, n: int):
        with pytest.raises(ValueError, match="same n"):
            LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[[1.0, 2.0]],
                    bounds=[0.0],
                ),
                LinearInequalities.from_float(
                    coefficients=[[3.0] * n],
                    bounds=[0.0],
                ),
            )

    @pytest.mark.parametrize("n", [1, 3])
    def test_when_n_mismatch_and_empty(self, n: int):
        with pytest.raises(ValueError, match="same n"):
            LinearConstraints(
                LinearEqualities([], n=2),
                LinearInequalities([], n=n),
            )

    @pytest.mark.parametrize("n", [0, 2])
    def test_when_equalities_and_inequalities(self, n: int):
        LinearConstraints(
            LinearEqualities.from_float(
                coefficients=[[1.0] * n],
                bounds=[0.0],
            ),
            LinearInequalities.from_float(
                coefficients=[[2.0] * n],
                bounds=[0.0],
            ),
        )  # does not raise

    @pytest.mark.parametrize("n", [0, 2])
    def test_when_no_equalities(self, n: int):
        LinearConstraints(
            LinearEqualities([], n=n),
            LinearInequalities.from_float(
                coefficients=[[1.0] * n],
                bounds=[0.0],
            ),
        )  # does not raise

    @pytest.mark.parametrize("n", [0, 2])
    def test_when_no_inequalities(self, n: int):
        LinearConstraints(
            LinearEqualities.from_float(
                coefficients=[[1.0] * n],
                bounds=[0.0],
            ),
            LinearInequalities([], n=n),
        )  # does not raise

    def test_when_no_constraints(self):
        LinearConstraints(
            LinearEqualities([]),
            LinearInequalities([]),
        )  # does not raise


class TestLinearConstraintsAlternativeConstructors:
    @pytest.mark.parametrize("n", [None, 0, 2])
    def test_empty(self, n: Optional[int]):
        result = LinearConstraints.empty(n)
        expected = LinearConstraints(
            LinearEqualities.empty(n),
            LinearInequalities.empty(n),
        )
        assert result == expected


@pytest.fixture(scope="module")
def equalities() -> LinearEqualities:
    return LinearEqualities.from_float(
        coefficients=[
            [1.0, 2.0],
            [3.0, 4.0],
        ],
        bounds=[0.0, 0.0],
    )


@pytest.fixture(scope="module")
def inequalities() -> LinearInequalities:
    return LinearInequalities.from_float(
        coefficients=[
            [5.0, 6.0],
        ],
        bounds=[1.0],
    )


@pytest.fixture(scope="module")
def constraints(
    equalities: LinearEqualities,
    inequalities: LinearInequalities,
) -> LinearConstraints:
    return LinearConstraints(equalities, inequalities)


class TestLinearConstraintsStringRepresentation:
    def test_str(
        self,
        constraints: LinearConstraints,
        equalities: LinearEqualities,
        inequalities: LinearInequalities,
    ):
        expected = f"(equalities={equalities}, inequalities={inequalities})"
        assert str(constraints) == expected

    def test_repr(self, constraints: LinearConstraints):
        expected = f"<{constraints.__class__.__name__}{constraints}>"
        assert repr(constraints) == expected


class TestLinearConstraintsEqual:
    def test_when_equal(
        self,
        constraints: LinearConstraints,
        equalities: LinearEqualities,
        inequalities: LinearInequalities,
    ):
        other = LinearConstraints(equalities, inequalities)
        assert other == constraints

    def test_when_different_equalities(
        self,
        constraints: LinearConstraints,
        inequalities: LinearInequalities,
    ):
        equalities = LinearEqualities([], n=inequalities.n)
        other = LinearConstraints(equalities, inequalities)
        assert other != constraints

    def test_when_different_inequalities(
        self,
        constraints: LinearConstraints,
        equalities: LinearEqualities,
    ):
        inequalities = LinearInequalities([], n=equalities.n)
        other = LinearConstraints(equalities, inequalities)
        assert other != constraints

    def test_when_different_object(self, constraints: LinearConstraints):
        assert constraints != "a"


class TestLinearConstraintsHash:
    def test_when_equal(
        self,
        constraints: LinearConstraints,
        equalities: LinearEqualities,
        inequalities: LinearInequalities,
    ):
        other = LinearConstraints(equalities, inequalities)
        assert hash(other) == hash(constraints)

    def test_when_different_equalities(
        self,
        constraints: LinearConstraints,
        inequalities: LinearInequalities,
    ):
        equalities = LinearEqualities([], n=inequalities.n)
        other = LinearConstraints(equalities, inequalities)
        assert hash(other) != hash(constraints)

    def test_when_different_inequalities(
        self,
        constraints: LinearConstraints,
        equalities: LinearEqualities,
    ):
        inequalities = LinearInequalities([], n=equalities.n)
        other = LinearConstraints(equalities, inequalities)
        assert hash(other) != hash(constraints)


class TestLinearConstraintsProperties:
    def test_n(
        self,
        constraints: LinearConstraints,
        equalities: LinearEqualities,
    ):
        assert constraints.n == equalities.n

    def test_set_n(
        self,
        constraints: LinearConstraints,
        equalities: LinearEqualities,
    ):
        with pytest.raises(AttributeError):
            constraints.n = equalities.n

    def test_equalities(
        self,
        constraints: LinearConstraints,
        equalities: LinearEqualities,
    ):
        assert constraints.equalities == equalities

    def test_set_equalities(
        self,
        constraints: LinearConstraints,
        equalities: LinearEqualities,
    ):
        with pytest.raises(AttributeError):
            constraints.equalities = equalities

    def test_inequalities(
        self,
        constraints: LinearConstraints,
        inequalities: LinearInequalities,
    ):
        assert constraints.inequalities == inequalities

    def test_set_inequalities(
        self,
        constraints: LinearConstraints,
        inequalities: LinearInequalities,
    ):
        with pytest.raises(AttributeError):
            constraints.inequalities = inequalities
