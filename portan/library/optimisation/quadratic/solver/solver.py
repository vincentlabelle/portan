from typing import Iterable, SupportsFloat

from portan.utilities.finite import Finite

from ...exception import SolverError
from ..program import QuadraticProgram


class IQuadraticSolver:
    """Interface for solving a quadratic program."""

    def solve(self, program: QuadraticProgram) -> Iterable[Finite]:
        """Solve a quadratic program.

        Parameters
        ----------
        program
            program to solve

        Raises
        ------
        SolverError
            if the solver fails to solve the program for any reason
            except infeasibility
            (e.g., maximum number of iterations is reached)
        InfeasibleError
            if the program appears infeasible

        Returns
        -------
        Iterable[Finite]
            solution of the quadratic program
        """
        if program.n == 0:
            return ()
        values = self._solve(program)
        return self._convert(values)

    def _solve(self, program: QuadraticProgram) -> Iterable[SupportsFloat]:
        raise NotImplementedError

    @staticmethod
    def _convert(values: Iterable[SupportsFloat]) -> Iterable[Finite]:
        try:
            return tuple(Finite(value) for value in values)
        except ValueError:
            msg = "cannot solve; solver's solution contains non-finite values"
            raise SolverError(msg)
