from typing import Iterable, SupportsFloat, SupportsInt, Type, TypeVar

from portan.utilities.collections import Matrix

from ..rate.matrix import RateMatrix
from .sequence import PriceSequence

T = TypeVar("T", bound="PriceMatrix")


class PriceMatrix(Matrix[PriceSequence]):
    """Immutable matrix of prices."""

    @classmethod
    def from_float(
        cls: Type[T],
        values: Iterable[Iterable[SupportsFloat]],
    ) -> T:
        """Create a matrix from floating-point values.

        Parameters
        ----------
        values
            values to create the matrix from

        Raises
        ------
        ValueError
            if the iterables in `values` are not all of the same length,
            if any floating-point number in `values` is non-finite, or
            if any floating-point number in `values` is not strictly positive

        Returns
        -------
        T
            matrix of prices
        """
        return cls(PriceSequence.from_float(value) for value in values)

    @classmethod
    def empties(cls: Type[T], length: SupportsInt) -> T:
        """Create a matrix of empty sequence of prices. The length
        of the matrix being created is `length`.

        Parameters
        ----------
        length
            length of the matrix being created

        Raises
        ------
        ValueError
            if `length` is negative

        Returns
        -------
        T
            matrix of empties
        """
        length_ = int(length)
        cls._raise_if_length_is_negative(length_)
        return cls(PriceSequence([]) for _ in range(length_))

    @classmethod
    def _raise_if_length_is_negative(cls, length: int):
        if length < 0:
            msg = (
                f"cannot instantiate {cls.__name__}; "
                f"length must be non-negative"
            )
            raise ValueError(msg)

    def growth(self) -> RateMatrix:
        """Get the continuous growth rates of the prices in
        this matrix by comparing each price to its preceding price
        for each sequence in this matrix.

        Raises
        ------
        ValueError
            if any pair of consecutive prices in any sequence in this
            matrix is such that `self[i] / self[i-1]` is either
            very big or very small (i.e., close or equal to +inf
            or 0.0)

        Returns
        -------
        RateMatrix
            continuous growth rates of the prices in this matrix
        """
        return RateMatrix(value.growth() for value in self)
