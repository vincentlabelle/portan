from portan.utilities.collections import Matrix

from .sequence import PriceSequence


class PriceMatrix(Matrix[PriceSequence]):
    """Immutable matrix of prices."""

    pass
