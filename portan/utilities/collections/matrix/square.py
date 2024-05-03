from typing import Iterable, TypeVar

from ..sequence import Sequence
from .matrix import Matrix

T = TypeVar("T", bound=Sequence)


class SquareMatrix(Matrix[T]):
    """Immutable sequence of sequences of the same length
    with default implementation for __init__, __getitem__, __len__,
    __eq__, __hash__, __str__, and __repr__. The sequence's length
    is matching with the length of the sequences it contains.

    Parameters
    ----------
    values: Iterable[T]
        values to create the sequence from

    Raises
    ------
    ValueError
        if the values in `values` are not all of the same length, or
        if the length of each value in `values` does not match with the
        number of values in `values`
    """

    def __init__(self, values: Iterable[T]):
        super().__init__(values)
        self._raise_if_is_not_square()

    def _raise_if_is_not_square(self):
        if not self.is_empty():
            if self.nrows != self.ncols:
                msg = (
                    f"cannot instantiate {self.__class__.__name__}; "
                    f"length of each value must match with the number "
                    f"of values"
                )
                raise ValueError(msg)

    def is_symmetric(self) -> bool:
        """Verify if this matrix is symmetric.

        Returns
        -------
        bool
            True if this matrix is symmetric, else False
        """
        return tuple(self) == self._transpose()
