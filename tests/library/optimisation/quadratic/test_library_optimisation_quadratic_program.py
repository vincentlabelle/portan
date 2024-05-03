from typing import Optional

import pytest

from portan.library.optimisation.constraint import (
    LinearConstraints,
    LinearEqualities,
    LinearInequalities,
)
from portan.library.optimisation.objective import (
    LinearCoefficients,
    QuadraticCoefficients,
)
from portan.library.optimisation.quadratic import QuadraticProgram


class TestQuadraticProgramInvariants:
    @pytest.fixture(scope="class")
    def quadratic(self) -> QuadraticCoefficients:
        return QuadraticCoefficients.from_float(
            [
                [1.0, 2.0],
                [2.0, 4.0],
            ]
        )

    @pytest.mark.parametrize("n", [1, 3])
    def test_when_linear_is_none_and_n_mismatch(
        self,
        quadratic: QuadraticCoefficients,
        n: int,
    ):
        constraints = LinearConstraints.empty(n)
        with pytest.raises(ValueError, match="same n"):
            QuadraticProgram(
                quadratic=quadratic,
                constraints=constraints,
            )

    def test_when_linear_is_none_and_n_match(
        self,
        quadratic: QuadraticCoefficients,
    ):
        constraints = LinearConstraints.empty(quadratic.n)
        QuadraticProgram(
            quadratic=quadratic,
            constraints=constraints,
        )  # does not raise

    @pytest.mark.parametrize("n_constraints", [1, 2, 3])
    @pytest.mark.parametrize("n_linear", [1, 2, 3])
    def test_when_linear_is_not_none(
        self,
        quadratic: QuadraticCoefficients,
        n_constraints: int,
        n_linear: int,
    ):
        constraints = LinearConstraints.empty(n_constraints)
        linear = LinearCoefficients.from_float([1.0] * n_linear)
        if quadratic.n != constraints.n or quadratic.n != linear.n:
            with pytest.raises(ValueError, match="same n"):
                QuadraticProgram(
                    quadratic=quadratic,
                    constraints=constraints,
                    linear=linear,
                )
        else:
            QuadraticProgram(
                quadratic=quadratic,
                constraints=constraints,
                linear=linear,
            )  # does not raise


@pytest.fixture(scope="module")
def quadratic() -> QuadraticCoefficients:
    return QuadraticCoefficients.from_float(
        [
            [1.0, 2.0],
            [2.0, 4.0],
        ]
    )


@pytest.fixture(scope="module")
def constraints() -> LinearConstraints:
    return LinearConstraints(
        LinearEqualities.empty(2),
        LinearInequalities.from_float(coefficients=[[1.0, 0.0]], bounds=[2.0]),
    )


@pytest.fixture(
    scope="module",
    params=[LinearCoefficients.from_float([1.0, 2.0]), None],
)
def linear(request) -> Optional[LinearCoefficients]:
    return request.param


@pytest.fixture(scope="class")
def program(
    quadratic: QuadraticCoefficients,
    constraints: LinearConstraints,
    linear: LinearCoefficients,
) -> QuadraticProgram:
    return QuadraticProgram(
        quadratic=quadratic,
        constraints=constraints,
        linear=linear,
    )


class TestQuadraticProgramStringRepresentation:
    def test_str(
        self,
        program: QuadraticProgram,
        quadratic: QuadraticCoefficients,
        constraints: LinearConstraints,
        linear: Optional[LinearCoefficients],
    ):
        result = str(program)
        if linear is None:
            expected = f"(quadratic={quadratic}, constraints={constraints})"
        else:
            expected = (
                f"(quadratic={quadratic}, "
                f"constraints={constraints}, "
                f"linear={linear})"
            )
        assert result == expected

    def test_repr(self, program: QuadraticProgram):
        assert repr(program) == f"<{program.__class__.__name__}{program}>"


class TestQuadraticProgramEqual:
    def test_when_equal(
        self,
        program: QuadraticProgram,
        quadratic: QuadraticCoefficients,
        constraints: LinearConstraints,
        linear: Optional[LinearCoefficients],
    ):
        other = QuadraticProgram(
            quadratic=quadratic,
            constraints=constraints,
            linear=linear,
        )
        assert other == program

    def test_when_different_quadratic(
        self,
        program: QuadraticProgram,
        constraints: LinearConstraints,
        linear: Optional[LinearCoefficients],
    ):
        quadratic = QuadraticCoefficients.from_float(
            [
                [3.0, 4.0],
                [4.0, 5.0],
            ]
        )
        other = QuadraticProgram(
            quadratic=quadratic,
            constraints=constraints,
            linear=linear,
        )
        assert other != program

    def test_when_different_constraints(
        self,
        program: QuadraticProgram,
        quadratic: QuadraticCoefficients,
        linear: Optional[LinearCoefficients],
    ):
        constraints = LinearConstraints.empty(2)
        other = QuadraticProgram(
            quadratic=quadratic,
            constraints=constraints,
            linear=linear,
        )
        assert other != program

    def test_when_different_linear(
        self,
        program: QuadraticProgram,
        quadratic: QuadraticCoefficients,
        constraints: LinearConstraints,
    ):
        linear = LinearCoefficients.from_float([0.0, 0.0])
        other = QuadraticProgram(
            quadratic=quadratic,
            constraints=constraints,
            linear=linear,
        )
        assert other != program

    def test_when_different_object(self, program: QuadraticProgram):
        assert program != "a"


class TestQuadraticProgramHash:
    def test_when_equal(
        self,
        program: QuadraticProgram,
        quadratic: QuadraticCoefficients,
        constraints: LinearConstraints,
        linear: Optional[LinearCoefficients],
    ):
        other = QuadraticProgram(
            quadratic=quadratic,
            constraints=constraints,
            linear=linear,
        )
        assert hash(other) == hash(program)

    def test_when_different_quadratic(
        self,
        program: QuadraticProgram,
        constraints: LinearConstraints,
        linear: Optional[LinearCoefficients],
    ):
        quadratic = QuadraticCoefficients.from_float(
            [
                [3.0, 4.0],
                [4.0, 5.0],
            ]
        )
        other = QuadraticProgram(
            quadratic=quadratic,
            constraints=constraints,
            linear=linear,
        )
        assert hash(other) != hash(program)

    def test_when_different_constraints(
        self,
        program: QuadraticProgram,
        quadratic: QuadraticCoefficients,
        linear: Optional[LinearCoefficients],
    ):
        constraints = LinearConstraints.empty(2)
        other = QuadraticProgram(
            quadratic=quadratic,
            constraints=constraints,
            linear=linear,
        )
        assert hash(other) != hash(program)

    def test_when_different_linear(
        self,
        program: QuadraticProgram,
        quadratic: QuadraticCoefficients,
        constraints: LinearConstraints,
    ):
        linear = LinearCoefficients.from_float([0.0, 0.0])
        other = QuadraticProgram(
            quadratic=quadratic,
            constraints=constraints,
            linear=linear,
        )
        assert hash(other) != hash(program)


class TestQuadraticProgramProperties:
    def test_n(
        self,
        program: QuadraticProgram,
        quadratic: QuadraticCoefficients,
    ):
        assert program.n == quadratic.n

    def test_set_n(
        self,
        program: QuadraticProgram,
        quadratic: QuadraticCoefficients,
    ):
        with pytest.raises(AttributeError):
            program.n = quadratic.n

    def test_quadratic(
        self,
        program: QuadraticProgram,
        quadratic: QuadraticCoefficients,
    ):
        assert program.quadratic == quadratic

    def test_set_quadratic(
        self,
        program: QuadraticProgram,
        quadratic: QuadraticCoefficients,
    ):
        with pytest.raises(AttributeError):
            program.quadratic = quadratic

    def test_constraints(
        self,
        program: QuadraticProgram,
        constraints: LinearConstraints,
    ):
        assert program.constraints == constraints

    def test_set_constraints(
        self,
        program: QuadraticProgram,
        constraints: LinearConstraints,
    ):
        with pytest.raises(AttributeError):
            program.constraints = constraints

    def test_linear(
        self,
        program: QuadraticProgram,
        linear: LinearCoefficients,
    ):
        assert program.linear == linear

    def test_set_linear(
        self,
        program: QuadraticProgram,
        linear: LinearCoefficients,
    ):
        with pytest.raises(AttributeError):
            program.linear = linear
