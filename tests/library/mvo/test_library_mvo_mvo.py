from typing import Iterable, SupportsFloat

import pytest

from portan.library.mvo import MeanVarianceOptimiser
from portan.library.mvo.factory import IMVOProgramFactory, MVOProgramFactory
from portan.library.optimisation.constraint import LinearConstraints
from portan.library.optimisation.objective import QuadraticCoefficients
from portan.library.optimisation.quadratic import (
    IQuadraticSolver,
    QuadraticProgram,
)
from portan.library.rate import Rate
from portan.library.rate.matrix import RateMatrix
from portan.library.rate.sequence import RateSequence
from portan.library.weight.sequence import WeightSequence


class TestMeanVarianceOptimiserAlternativeConstructors:
    def test_default(self):
        solver = IQuadraticSolver()
        result = MeanVarianceOptimiser.default(solver)
        assert result.solver is solver
        assert isinstance(result.factory, MVOProgramFactory)


class TestMeanVarianceOptimiserProperties:
    @pytest.fixture(scope="class")
    def solver(self) -> IQuadraticSolver:
        return IQuadraticSolver()

    @pytest.fixture(scope="class")
    def factory(self) -> IMVOProgramFactory:
        return IMVOProgramFactory()

    @pytest.fixture(scope="class")
    def optimiser(
        self,
        factory: IMVOProgramFactory,
        solver: IQuadraticSolver,
    ) -> MeanVarianceOptimiser:
        return MeanVarianceOptimiser(factory, solver)

    def test_solver(
        self,
        optimiser: MeanVarianceOptimiser,
        solver: IQuadraticSolver,
    ):
        assert optimiser.solver is solver

    def test_set_solver(
        self,
        optimiser: MeanVarianceOptimiser,
        solver: IQuadraticSolver,
    ):
        with pytest.raises(AttributeError):
            optimiser.solver = solver

    def test_factory(
        self,
        optimiser: MeanVarianceOptimiser,
        factory: IMVOProgramFactory,
    ):
        assert optimiser.factory is factory

    def test_set_factory(
        self,
        optimiser: MeanVarianceOptimiser,
        factory: IMVOProgramFactory,
    ):
        with pytest.raises(AttributeError):
            optimiser.factory = factory


_MATRIX = RateMatrix(
    [
        RateSequence([]),
    ]
)
_MINIMUM = Rate(0.0)
_PROGRAM = QuadraticProgram(
    quadratic=QuadraticCoefficients.from_float([[1.0]]),
    constraints=LinearConstraints.empty(1),
)
_OPTIMUM = (0.5, 0.2, 0.3)


class _Solver(IQuadraticSolver):
    def _solve(self, program: QuadraticProgram) -> Iterable[SupportsFloat]:
        assert program is _PROGRAM
        return _OPTIMUM


class _Factory(IMVOProgramFactory):
    def get(
        self,
        matrix: RateMatrix,
        minimum: Rate,
    ) -> QuadraticProgram:
        assert matrix in [RateMatrix([]), _MATRIX]
        assert minimum is _MINIMUM
        return _PROGRAM


class TestMeanVarianceOptimiserOptimise:
    @pytest.fixture(scope="class")
    def solver(self) -> _Solver:
        return _Solver()

    @pytest.fixture(scope="class")
    def factory(self) -> _Factory:
        return _Factory()

    @pytest.fixture(scope="class")
    def optimiser(
        self,
        factory: _Factory,
        solver: _Solver,
    ) -> MeanVarianceOptimiser:
        return MeanVarianceOptimiser(factory, solver)

    def test_when_empty(self, optimiser: MeanVarianceOptimiser):
        matrix = RateMatrix([])
        result = optimiser.optimise(matrix, _MINIMUM)
        assert result == WeightSequence([])

    def test_when_non_empty(self, optimiser: MeanVarianceOptimiser):
        result = optimiser.optimise(_MATRIX, _MINIMUM)
        expected = WeightSequence.from_float(_OPTIMUM)
        assert result == expected
