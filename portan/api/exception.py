class BasePortanError(Exception):
    """Base class for all of Portan's exceptions."""

    pass


class PortanError(BasePortanError):
    """Exception for general errors."""

    pass


class SourceError(BasePortanError):
    """Exception for errors related to a source of prices (e.g., Yahoo)."""

    pass


class InfeasibleError(BasePortanError):
    """Exception for errors related to an infeasible optimisation problem."""

    pass
