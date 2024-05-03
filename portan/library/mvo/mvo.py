from typing import Type, TypeVar

from ..optimisation.quadratic import IQuadraticSolver
from ..rate import Rate
from ..rate.matrix import RateMatrix
from ..weight.sequence import WeightSequence
from .factory import IMVOProgramFactory, MVOProgramFactory

T = TypeVar("T", bound="MeanVarianceOptimiser")


class MeanVarianceOptimiser:
    """Optimiser finding the optimal weights to minimize the
    sample variance of the weighted sum of random variables, while
    ensuring the sample expected value of the weighted sum is
    above or equal to a certain threshold.

    Parameters
    ----------
    factory: IMVOProgramFactory
        factory of :py:class:`QuadraticProgram` for the mean-variance
        optimisation problem
    solver: IQuadraticSolver
        solver to use to perform the optimisation
    """

    @classmethod
    def default(cls: Type[T], solver: IQuadraticSolver) -> T:
        """Create the default optimiser (i.e., with the default
        factory of :py:class:`QuadraticProgram`).

        Parameters
        ----------
        solver
            solver to use to perform the optimisation

        Returns
        -------
        T
            default optimiser
        """
        return cls(MVOProgramFactory(), solver)

    def __init__(self, factory: IMVOProgramFactory, solver: IQuadraticSolver):
        self._factory = factory
        self._solver = solver

    @property
    def factory(self) -> IMVOProgramFactory:
        """Factory of :py:class:`QuadraticProgram` used for the mean-variance
        optimisation problem. This property is exposed for testing purposes
        only."""
        return self._factory

    @property
    def solver(self) -> IQuadraticSolver:
        """Solver used to perform the optimisation. This property is exposed
        for testing purposes only."""
        return self._solver

    # TODO we should return a BalancedWeights!
    def optimise(
        self,
        matrix: RateMatrix,
        minimum: Rate,
    ) -> WeightSequence:
        """Get the optimal weights to minimize the sample variance
        of the weighted sum of the random variables, while ensuring the
        sample expected value of the weighted sum is above or equal
        to `minimum`. The random variables are represented by the rows
        of `matrix` (i.e., each row is a sample of a random variable).

        Parameters
        ----------
        matrix
            matrix where each row represents the observations of
            a random variables
        minimum
            minimum acceptable sample expected value for the weighted sum
            of the random variables

        Raises
        ------
        ValueError
            if any value in the means of `matrix` is non-finite, or
            if any value in the covariance matrix of `matrix` is not finite
        SolverError
            if the solver fails to solve the program for any reason
            except infeasibility
            (e.g., maximum number of iterations is reached)
        InfeasibleError
            if the program appears infeasible
        OverflowError
            if any value in the solution is too big in absolute terms
            such that it cannot be converted to :py:class:`Weight`

        Returns
        -------
        WeightSequence
            optimal weights
        """
        if len(matrix) == 0:
            return WeightSequence([])
        program = self._factory.get(matrix, minimum)
        optimum = self._solver.solve(program)
        return WeightSequence.from_float(optimum)
