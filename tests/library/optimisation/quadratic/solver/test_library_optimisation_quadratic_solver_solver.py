from math import inf, nan
from typing import Iterable, SupportsFloat

import pytest

from portan.library.optimisation.constraint import LinearConstraints
from portan.library.optimisation.exception import SolverError
from portan.library.optimisation.objective import QuadraticCoefficients
from portan.library.optimisation.quadratic import QuadraticProgram
from portan.library.optimisation.quadratic.solver import IQuadraticSolver
from portan.utilities.finite import Finite


@pytest.fixture(scope="module")
def program() -> QuadraticProgram:
    return QuadraticProgram(
        quadratic=QuadraticCoefficients.from_float([[1.0]]),
        constraints=LinearConstraints.empty(1),
    )


class TestIQuadraticSolverRaises:
    def test(self, program: QuadraticProgram):
        solver = IQuadraticSolver()
        with pytest.raises(NotImplementedError):
            solver.solve(program)


class TestIQuadraticSolverEmptyProgram:
    def test(self):
        solver = IQuadraticSolver()
        program = QuadraticProgram(
            quadratic=QuadraticCoefficients([]),
            constraints=LinearConstraints.empty(0),
        )
        result = solver.solve(program)
        assert tuple(result) == ()


class _SolverStub(IQuadraticSolver):
    def __init__(self, values: Iterable[SupportsFloat]):
        self._values = values

    def _solve(self, program: QuadraticProgram) -> Iterable[SupportsFloat]:
        return self._values


class TestIQuadraticSolverConversion:
    def test_when_finite(self, program: QuadraticProgram):
        values = (1.0, 2.0, 3.0)
        solver = _SolverStub(values)
        result = solver.solve(program)
        expected = tuple(Finite(value) for value in values)
        assert tuple(result) == expected

    @pytest.mark.parametrize("value", [inf, nan, -inf])
    def test_when_non_finite(self, program: QuadraticProgram, value: float):
        solver = _SolverStub((1.0, value, 3.0))
        with pytest.raises(SolverError, match="non-finite"):
            solver.solve(program)
