class BaseSolverError(Exception):
    """Base class for all exceptions related to a solver."""

    pass


class SolverError(BaseSolverError):
    """Exception for any errors related to a solver except an infeasible
    program."""

    pass


class InfeasibleError(SolverError):
    """Exception for an infeasible program."""

    pass
