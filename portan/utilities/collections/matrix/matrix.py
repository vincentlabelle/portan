from typing import Iterable, Tuple, TypeVar

from ..sequence import Sequence

T = TypeVar("T", bound=Sequence)
M = TypeVar("M", bound="Matrix")


class Matrix(Sequence[T]):
    """Immutable sequence of sequences of the same length
    with default implementation for __init__, __getitem__, __len__,
    __eq__, __hash__, __str__, and __repr__.

    Parameters
    ----------
    values: Iterable[T]
        values to create the sequence from

    Raises
    ------
    ValueError
        if the values in `values` are not all of the same length
    """

    def __init__(self, values: Iterable[T]):
        super().__init__(values)
        self._raise_if_length_mismatch()

    def _raise_if_length_mismatch(self):
        if self._is_length_mismatch():
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"values must all have the same length"
            )
            raise ValueError(msg)

    def _is_length_mismatch(self):
        return len(set(len(value) for value in self)) > 1

    @property
    def nrows(self) -> int:
        """The number of rows in this matrix (i.e., the number of sequences)."""
        return len(self)

    @property
    def ncols(self) -> int:
        """The number of columns in this matrix (i.e., the length of the
        sequences)."""
        if self.is_empty():
            return 0
        return len(self[0])

    def is_empty(self) -> bool:
        """Verify if this matrix is empty.

        Returns
        -------
        bool
            True if this matrix is empty, else False
        """
        return len(self) == 0

    def transpose(self: M) -> M:
        """Transpose this matrix.

        Returns
        -------
        M[T]
            transposed matrix
        """
        return self.__class__(self._transpose())

    def _transpose(self) -> Tuple[T, ...]:
        if self.is_empty():
            return ()
        type_ = self[0].__class__
        return tuple(type_(zipped) for zipped in zip(*self))
