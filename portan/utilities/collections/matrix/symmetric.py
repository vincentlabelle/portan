from typing import Iterable, TypeVar

from ..sequence import Sequence
from .square import SquareMatrix

T = TypeVar("T", bound=Sequence)


class SymmetricMatrix(SquareMatrix[T]):
    """Immutable sequence of sequences of the same length
    with default implementation for __init__, __getitem__, __len__,
    __eq__, __hash__, __str__, and __repr__. The sequences
    form a symmetrical matrix.

    Parameters
    ----------
    values: Iterable[T]
        values to create the sequence from

    Raises
    ------
    ValueError
        if the values in `values` are not all of the same length,
        if the length of each value in `values` does not match with the
        number of values in `values`, or
        if the values do not form a symmetric matrix
    """

    def __init__(self, values: Iterable[T]):
        super().__init__(values)
        self._raise_if_is_asymmetric()

    def _raise_if_is_asymmetric(self):
        if not self.is_symmetric():
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"values must form a symmetric matrix"
            )
            raise ValueError(msg)
