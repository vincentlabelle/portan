from typing import Any, Iterable, Optional, SupportsFloat

import numpy as np
from osqp import OSQP
from scipy import sparse

from portan.utilities.finite.positive import PositiveFinite

from ...constraint import LinearEqualities, LinearInequalities
from ...constraint.sequence import ConstraintSequence
from ...exception import InfeasibleError, SolverError
from ...objective import QuadraticCoefficients
from ..program import QuadraticProgram
from .solver import IQuadraticSolver


class OSQPSolver(IQuadraticSolver):
    """Solver of quadratic program based on OSQP.

    Information on OSQP is available at
    https://osqp.org/docs/interfaces/solver_settings.html.

    Parameters
    ----------
    absolute_tolerance: PositiveFinite
        absolute tolerance
    relative_tolerance: PositiveFinite
        relative tolerance
    maximum_iteration: int
        maximum number of iterations
    polish: bool
        whether to attempt to polish the solution
    verbose: bool
        whether to display output in console

    Raises
    ------
    ValueError
        if `maximum_iteration` is not strictly positive
    """

    def __init__(
        self,
        *,
        absolute_tolerance: PositiveFinite = PositiveFinite(1e-6),
        relative_tolerance: PositiveFinite = PositiveFinite(1e-6),
        maximum_iteration: int = 1000000,
        polish: bool = True,
        verbose: bool = False,
    ):
        self._absolute_tolerance = absolute_tolerance
        self._relative_tolerance = relative_tolerance
        self._maximum_iteration = maximum_iteration
        self._polish = polish
        self._verbose = verbose
        self._raise_if_maximum_iteration_is_negative_or_zero()

    def _solve(self, program: QuadraticProgram) -> Iterable[SupportsFloat]:
        solver = OSQP()
        program_ = ProgramAdapter(program)
        self._setup(solver, program_)
        result = self._perform_solve(solver)
        self._raise_if_unsolved(result)
        return result.x

    def _setup(self, solver: OSQP, program: "ProgramAdapter"):
        try:
            solver.setup(
                P=program.p_mat,
                q=program.q_vec,
                A=program.a_mat,
                l=program.l_vec,
                u=program.u_vec,
                eps_abs=float(self._absolute_tolerance),
                eps_rel=float(self._relative_tolerance),
                max_iter=self._maximum_iteration,
                polish=self._polish,
                verbose=self._verbose,
            )
        except Exception as err:
            msg = "cannot solve; unable to setup solver"
            raise SolverError(msg) from err

    @staticmethod
    def _perform_solve(solver: OSQP) -> Any:
        try:
            return solver.solve()
        except Exception as err:
            msg = "cannot solve; solver failed during solving"
            raise SolverError(msg) from err

    @staticmethod
    def _raise_if_unsolved(result: Any):
        status = result.info.status_val
        if status in (3, -3, -4, 4):
            msg = "cannot solve; program appears infeasible"
            raise InfeasibleError(msg)
        elif status != 1:
            msg = f"cannot solve; solver ended with status [{status}]"
            raise SolverError(msg)

    def _raise_if_maximum_iteration_is_negative_or_zero(self):
        if self._maximum_iteration <= 0:
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"iterations must be strictly positive"
            )
            raise ValueError(msg)


class ProgramAdapter:
    """Adapter of the quadratic program interface for OSQP.

    Parameters
    ----------
    program: QuadraticProgram
        program to adapt
    """

    def __init__(self, program: QuadraticProgram):
        self._program = program

    @property
    def p_mat(self) -> sparse.csc_matrix:
        """Matrix 'P' for OSQP's setup."""
        return sparse.csc_matrix(
            self._quadratic_to_array(self._program.quadratic)
        )

    @staticmethod
    def _quadratic_to_array(quadratic: QuadraticCoefficients) -> np.ndarray:
        if len(quadratic) == 0:
            return np.empty((0, 0), dtype=np.float_)
        return np.array(quadratic, dtype=np.float_)

    @property
    def q_vec(self) -> Optional[np.ndarray]:
        """Vector 'q' for OSQP's setup."""
        if self._program.linear is None:
            return None
        return np.array(self._program.linear, dtype=np.float_)

    @property
    def a_mat(self) -> sparse.csc_matrix:
        """Matrix 'A' for OSQP's setup."""
        return sparse.csc_matrix(
            np.vstack(
                (
                    self._coefficients_to_array(self._equalities),
                    self._coefficients_to_array(self._inequalities),
                )
            )
        )

    @staticmethod
    def _coefficients_to_array(sequence: ConstraintSequence) -> np.ndarray:
        if len(sequence) == 0:
            return np.empty((0, sequence.n), dtype=np.float_)
        return np.array(sequence.coefficients, dtype=np.float_)

    @property
    def l_vec(self) -> np.ndarray:
        """Vector 'l' for OSQP's setup."""
        return np.concatenate(
            (
                np.array(self._equalities.bounds, dtype=np.float_),
                np.full(len(self._inequalities), -np.inf, dtype=np.float_),
            )
        )

    @property
    def u_vec(self) -> np.ndarray:
        """Vector 'u' for OSQP's setup."""
        return np.concatenate(
            (
                np.array(self._equalities.bounds, dtype=np.float_),
                np.array(self._inequalities.bounds, dtype=np.float_),
            )
        )

    @property
    def _equalities(self) -> LinearEqualities:
        return self._program.constraints.equalities

    @property
    def _inequalities(self) -> LinearInequalities:
        return self._program.constraints.inequalities
