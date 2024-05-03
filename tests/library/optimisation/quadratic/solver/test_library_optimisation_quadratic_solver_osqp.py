from typing import Optional, Tuple

import numpy as np
import pytest

from portan.library.optimisation.constraint import (
    LinearConstraints,
    LinearEqualities,
    LinearInequalities,
)
from portan.library.optimisation.exception import InfeasibleError, SolverError
from portan.library.optimisation.objective import (
    LinearCoefficients,
    QuadraticCoefficients,
)
from portan.library.optimisation.quadratic import OSQPSolver, QuadraticProgram
from portan.library.optimisation.quadratic.solver.osqp import ProgramAdapter
from portan.utilities.finite import Finite
from portan.utilities.finite.positive import PositiveFinite


class TestOSQPSolverInvariants:
    @pytest.mark.parametrize("value", [-1, 0])
    def test_when_maximum_iteration_is_negative_or_zero(self, value: int):
        with pytest.raises(ValueError, match="strictly positive"):
            OSQPSolver(maximum_iteration=value)

    def test_when_maximum_iteration_is_non_negative(self):
        OSQPSolver(maximum_iteration=1)  # does not raise


@pytest.fixture(scope="module")
def solver() -> OSQPSolver:
    return OSQPSolver()


class TestOSQPSolverSolve:
    @pytest.mark.parametrize("linear", [None, LinearCoefficients([])])
    def test_when_no_coefficients_nor_constraints(
        self,
        solver: OSQPSolver,
        linear: Optional[LinearCoefficients],
    ):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            linear=linear,
            constraints=LinearConstraints.empty(0),
        )
        result = solver.solve(program)
        assert tuple(result) == ()

    @pytest.mark.parametrize("linear", [None, LinearCoefficients([])])
    def test_when_no_coefficients_nor_inequalities(
        self,
        solver: OSQPSolver,
        linear: Optional[LinearCoefficients],
    ):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            linear=linear,
            constraints=LinearConstraints(
                LinearEqualities.from_float(coefficients=[[]], bounds=[0.0]),
                LinearInequalities.empty(0),
            ),
        )
        result = solver.solve(program)
        assert tuple(result) == ()

    @pytest.mark.parametrize("linear", [None, LinearCoefficients([])])
    def test_when_no_coefficients_nor_equalities(
        self,
        solver: OSQPSolver,
        linear: Optional[LinearCoefficients],
    ):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            linear=linear,
            constraints=LinearConstraints(
                LinearEqualities.empty(0),
                LinearInequalities.from_float(
                    coefficients=[[], []],
                    bounds=[1.0, 0.0],
                ),
            ),
        )
        result = solver.solve(program)
        assert tuple(result) == ()

    @pytest.mark.parametrize("linear", [None, LinearCoefficients([])])
    def test_when_no_coefficients(
        self,
        solver: OSQPSolver,
        linear: Optional[LinearCoefficients],
    ):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            linear=linear,
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[[]],
                    bounds=[0.0],
                ),
                LinearInequalities.from_float(
                    coefficients=[[], []],
                    bounds=[1.0, 0.0],
                ),
            ),
        )
        result = solver.solve(program)
        assert tuple(result) == ()

    @pytest.mark.parametrize(
        "linear, expected",
        [
            (
                None,
                (Finite(0.0), Finite(0.0)),
            ),
            (
                LinearCoefficients.from_float([1.0, -1.0]),
                (Finite(-1.0), Finite(1.0)),
            ),
        ],
    )
    def test_when_no_constraints(
        self,
        solver: OSQPSolver,
        linear: Optional[LinearCoefficients],
        expected: Tuple[Finite, ...],
    ):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(
                [
                    [1.0, 0.0],
                    [0.0, 1.0],
                ]
            ),
            linear=linear,
            constraints=LinearConstraints.empty(2),
        )
        result = solver.solve(program)
        assert tuple(result) == expected

    @pytest.mark.parametrize(
        "linear, expected",
        [
            (
                None,
                (Finite(1.0), Finite(0.0)),
            ),
            (
                LinearCoefficients.from_float([1.0, -1.0]),
                (Finite(1.0), Finite(1.0)),
            ),
        ],
    )
    def test_when_no_inequalities(
        self,
        solver: OSQPSolver,
        linear: Optional[LinearCoefficients],
        expected: Tuple[Finite, ...],
    ):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(
                [
                    [1.0, 0.0],
                    [0.0, 1.0],
                ]
            ),
            linear=linear,
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[[1.0, 0.0]],
                    bounds=[1.0],
                ),
                LinearInequalities.empty(2),
            ),
        )
        result = solver.solve(program)
        assert tuple(result) == expected

    @pytest.mark.parametrize(
        "linear, expected",
        [
            (
                None,
                (Finite(-1.0), Finite(0.0)),
            ),
            (
                LinearCoefficients.from_float([1.0, -1.0]),
                (Finite(-1.0), Finite(1.0)),
            ),
        ],
    )
    def test_when_no_equalities(
        self,
        solver: OSQPSolver,
        linear: Optional[LinearCoefficients],
        expected: Tuple[Finite, ...],
    ):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(
                [
                    [1.0, 0.0],
                    [0.0, 1.0],
                ]
            ),
            linear=linear,
            constraints=LinearConstraints(
                LinearEqualities.empty(2),
                LinearInequalities.from_float(
                    coefficients=[
                        [1.0, 0.0],
                        [0.0, 1.0],
                    ],
                    bounds=[-1.0, 1.0],
                ),
            ),
        )
        result = solver.solve(program)
        assert tuple(result) == expected

    @pytest.mark.parametrize(
        "linear, expected",
        [
            (
                None,
                (Finite(-1.0), Finite(-1.0)),
            ),
            (
                LinearCoefficients.from_float([1.0, -1.0]),
                (Finite(-1.0), Finite(-1.0)),
            ),
        ],
    )
    def test_when_constraints(
        self,
        solver: OSQPSolver,
        linear: Optional[LinearCoefficients],
        expected: Tuple[Finite, ...],
    ):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(
                [
                    [1.0, 0.0],
                    [0.0, 1.0],
                ]
            ),
            linear=linear,
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[
                        [0.0, 1.0],
                    ],
                    bounds=[-1.0],
                ),
                LinearInequalities.from_float(
                    coefficients=[
                        [1.0, 0.0],
                        [0.0, 1.0],
                    ],
                    bounds=[-1.0, 1.0],
                ),
            ),
        )
        result = solver.solve(program)
        assert tuple(result) == expected


class TestOSQPSolverInfeasible:
    def test(self, solver: OSQPSolver):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(
                [
                    [1.0, 0.0],
                    [0.0, 1.0],
                ]
            ),
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[
                        [1.0, 0.0],
                        [1.0, 0.0],
                    ],
                    bounds=[1.0, 2.0],
                ),
                LinearInequalities.empty(2),
            ),
        )
        with pytest.raises(InfeasibleError, match="infeasible"):
            solver.solve(program)


class TestOSQPSolverMaximumIterations:
    def test(self):
        solver = OSQPSolver(maximum_iteration=1)
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(
                [
                    [1.0, 0.0],
                    [0.0, 1.0],
                ]
            ),
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[
                        [1.0, 0.0],
                        [1.0, 0.0],
                    ],
                    bounds=[1.0, 2.0],
                ),
                LinearInequalities.empty(2),
            ),
        )
        with pytest.raises(SolverError, match="ended with status"):
            solver.solve(program)


class TestOSQPSolverSettings:
    @pytest.fixture(scope="class")
    def program(self) -> QuadraticProgram:
        return QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(
                [
                    [1.0, 0.0],
                    [0.0, 1.0],
                ]
            ),
            constraints=LinearConstraints.empty(2),
        )

    @pytest.mark.parametrize("verbose", [True, False])
    def test_verbose(
        self,
        program: QuadraticProgram,
        verbose: bool,
        capsys,
    ):
        solver = OSQPSolver(verbose=verbose)
        solver.solve(program)
        captured = capsys.readouterr()
        if verbose:
            assert captured.out != ""
        else:
            assert captured.out == ""

    @pytest.mark.parametrize("polish", [True, False])
    def test_polish(
        self,
        program: QuadraticProgram,
        polish: bool,
        capsys,
    ):
        solver = OSQPSolver(polish=polish, verbose=True)
        solver.solve(program)
        captured = capsys.readouterr()
        if polish:
            assert "polish: on" in captured.out
        else:
            assert "polish: off" in captured.out

    @pytest.mark.parametrize("maximum", [1, 2])
    def test_maximum_iteration(
        self,
        program: QuadraticProgram,
        maximum: int,
        capsys,
    ):
        solver = OSQPSolver(maximum_iteration=maximum, verbose=True)
        solver.solve(program)
        captured = capsys.readouterr()
        assert f"max_iter = {maximum}" in captured.out

    @pytest.mark.parametrize(
        "tolerance",
        [PositiveFinite(1e-2), PositiveFinite(1e-4)],
    )
    def test_relative_tolerance(
        self,
        program: QuadraticProgram,
        tolerance: PositiveFinite,
        capsys,
    ):
        solver = OSQPSolver(relative_tolerance=tolerance, verbose=True)
        solver.solve(program)
        captured = capsys.readouterr()
        assert f"eps_rel = {float(tolerance):.1e}" in captured.out

    @pytest.mark.parametrize(
        "tolerance",
        [PositiveFinite(1e-2), PositiveFinite(1e-4)],
    )
    def test_absolute_tolerance(
        self,
        program: QuadraticProgram,
        tolerance: PositiveFinite,
        capsys,
    ):
        solver = OSQPSolver(absolute_tolerance=tolerance, verbose=True)
        solver.solve(program)
        captured = capsys.readouterr()
        assert f"eps_abs = {float(tolerance):.1e}" in captured.out


class TestProgramAdapterPMat:
    def test_when_no_coefficients(self):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints.empty(0),
        )
        adapted = ProgramAdapter(program)
        expected = np.empty((0, 0), dtype=np.float_)
        assert np.array_equal(adapted.p_mat.toarray(), expected)

    def test_when_coefficients(self):
        values = [
            [1.0, 2.0],
            [2.0, 3.0],
        ]
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(values),
            constraints=LinearConstraints.empty(2),
        )
        adapted = ProgramAdapter(program)
        assert np.array_equal(adapted.p_mat.toarray(), values)


class TestProgramAdapterQVec:
    def test_when_none(self):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            linear=None,
            constraints=LinearConstraints.empty(0),
        )
        adapted = ProgramAdapter(program)
        assert adapted.q_vec is None

    def test_when_no_coefficients(self):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            linear=LinearCoefficients([]),
            constraints=LinearConstraints.empty(0),
        )
        adapted = ProgramAdapter(program)
        assert np.array_equal(adapted.q_vec, [])

    def test_when_coefficients(self):
        values = [4.0, 5.0]
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(
                [
                    [1.0, 2.0],
                    [2.0, 3.0],
                ]
            ),
            linear=LinearCoefficients.from_float(values),
            constraints=LinearConstraints.empty(2),
        )
        adapted = ProgramAdapter(program)
        assert np.array_equal(adapted.q_vec, values)


class TestProgramAdapterAMat:
    def test_when_no_coefficients_nor_constraints(self):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints.empty(0),
        )
        adapted = ProgramAdapter(program)
        expected = np.empty((0, 0), dtype=np.float_)
        assert np.array_equal(adapted.a_mat.toarray(), expected)

    def test_when_no_coefficients_nor_equalities(self):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints(
                equalities=LinearEqualities.empty(0),
                inequalities=LinearInequalities.from_float(
                    coefficients=[[], []],
                    bounds=[1.0, 2.0],
                ),
            ),
        )
        adapted = ProgramAdapter(program)
        expected = np.empty((2, 0), dtype=np.float_)
        assert np.array_equal(adapted.a_mat.toarray(), expected)

    def test_when_no_coefficients_nor_inequalities(self):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints(
                equalities=LinearEqualities.from_float(
                    coefficients=[[], []],
                    bounds=[1.0, 2.0],
                ),
                inequalities=LinearInequalities.empty(0),
            ),
        )
        adapted = ProgramAdapter(program)
        expected = np.empty((2, 0), dtype=np.float_)
        assert np.array_equal(adapted.a_mat.toarray(), expected)

    def test_when_no_coefficients(self):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints(
                equalities=LinearEqualities.from_float(
                    coefficients=[[]],
                    bounds=[3.0],
                ),
                inequalities=LinearInequalities.from_float(
                    coefficients=[[], []],
                    bounds=[1.0, 2.0],
                ),
            ),
        )
        adapted = ProgramAdapter(program)
        expected = np.empty((3, 0), dtype=np.float_)
        assert np.array_equal(adapted.a_mat.toarray(), expected)

    def test_when_no_constraints(self):
        values = [
            [1.0, 2.0],
            [2.0, 3.0],
        ]
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(values),
            constraints=LinearConstraints.empty(2),
        )
        adapted = ProgramAdapter(program)
        expected = np.empty((0, 2), dtype=np.float_)
        assert np.array_equal(adapted.a_mat.toarray(), expected)

    def test_when_no_inequalities(self):
        values = [[1.0, 0.0]]
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(
                [
                    [1.0, 2.0],
                    [2.0, 3.0],
                ]
            ),
            constraints=LinearConstraints(
                LinearEqualities.from_float(coefficients=values, bounds=[1.0]),
                LinearInequalities.empty(2),
            ),
        )
        adapted = ProgramAdapter(program)
        assert np.array_equal(adapted.a_mat.toarray(), values)

    def test_when_no_equalities(self):
        values = [[1.0, 0.0]]
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(
                [
                    [1.0, 2.0],
                    [2.0, 3.0],
                ]
            ),
            constraints=LinearConstraints(
                LinearEqualities.empty(2),
                LinearInequalities.from_float(
                    coefficients=values,
                    bounds=[1.0],
                ),
            ),
        )
        adapted = ProgramAdapter(program)
        assert np.array_equal(adapted.a_mat.toarray(), values)

    def test_when_constraints(self):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients.from_float(
                [
                    [1.0, 2.0],
                    [2.0, 3.0],
                ]
            ),
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[[0.0, 1.0]],
                    bounds=[2.0],
                ),
                LinearInequalities.from_float(
                    coefficients=[[1.0, 0.0]],
                    bounds=[1.0],
                ),
            ),
        )
        adapted = ProgramAdapter(program)
        expected = [[0.0, 1.0], [1.0, 0]]
        assert np.array_equal(adapted.a_mat.toarray(), expected)


class TestProgramAdapterLVec:
    def test_when_no_constraints(self):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints.empty(0),
        )
        adapted = ProgramAdapter(program)
        assert np.array_equal(adapted.l_vec, [])

    def test_when_equality_constraints(self):
        values = [1.0]
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints(
                LinearEqualities.from_float(coefficients=[[]], bounds=values),
                LinearInequalities.empty(0),
            ),
        )
        adapted = ProgramAdapter(program)
        assert np.array_equal(adapted.l_vec, values)

    def test_when_inequality_constraints(self):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints(
                LinearEqualities.empty(0),
                LinearInequalities.from_float(coefficients=[[]], bounds=[1.0]),
            ),
        )
        adapted = ProgramAdapter(program)
        assert np.array_equal(adapted.l_vec, [-np.inf])

    def test_when_constraints(self):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[[], []],
                    bounds=[1.0, 2.0],
                ),
                LinearInequalities.from_float(
                    coefficients=[[]],
                    bounds=[3.0],
                ),
            ),
        )
        adapted = ProgramAdapter(program)
        assert np.array_equal(adapted.l_vec, [1.0, 2.0, -np.inf])


class TestProgramAdapterUVec:
    def test_when_no_constraints(self):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints.empty(0),
        )
        adapted = ProgramAdapter(program)
        assert np.array_equal(adapted.u_vec, [])

    def test_when_equality_constraints(self):
        values = [1.0]
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints(
                LinearEqualities.from_float(coefficients=[[]], bounds=values),
                LinearInequalities.empty(0),
            ),
        )
        adapted = ProgramAdapter(program)
        assert np.array_equal(adapted.u_vec, values)

    def test_when_inequality_constraints(self):
        values = [1.0]
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints(
                LinearEqualities.empty(0),
                LinearInequalities.from_float(coefficients=[[]], bounds=values),
            ),
        )
        adapted = ProgramAdapter(program)
        assert np.array_equal(adapted.u_vec, values)

    def test_when_constraints(self):
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints(
                LinearEqualities.from_float(
                    coefficients=[[], []],
                    bounds=[1.0, 2.0],
                ),
                LinearInequalities.from_float(
                    coefficients=[[]],
                    bounds=[3.0],
                ),
            ),
        )
        adapted = ProgramAdapter(program)
        assert np.array_equal(adapted.u_vec, [1.0, 2.0, 3.0])
