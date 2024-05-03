from typing import Iterable, Optional, SupportsFloat, Tuple, Type, TypeVar

from portan.utilities.collections import Sequence

from ..coefficient.matrix import CoefficientMatrix
from .bound.sequence import BoundSequence
from .constraint import Constraint

T = TypeVar("T", bound="ConstraintSequence")


class ConstraintSequence(Sequence[Constraint]):
    """Immutable sequence of linear constraints constraining a
    sequence of unknowns of size `n`.

    Parameters
    ----------
    values: Iterable[Constraint]
        values to create the sequence from
    n: Optional[int]
        number of unknowns constrained by the sequence to create
        (defaults to None)

    Raises
    ------
    ValueError
        if values in `values` do not all have the same `n`,
        if the `values` `n` doesn't match with `n`, or
        if `n` is negative
    """

    @classmethod
    def empty(cls: Type[T], n: Optional[int] = None) -> T:
        """Create an empty sequence of linear constraints.

        Parameters
        ----------
        n
            number of unknowns constrained by the sequence to create
            (defaults to None)

        Raises
        ------
        ValueError
            if `n` is negative

        Returns
        -------
        T
            empty sequence of constraints
        """
        return cls([], n=n)

    @classmethod
    def from_float(
        cls: Type[T],
        *,
        coefficients: Iterable[Iterable[SupportsFloat]],
        bounds: Iterable[SupportsFloat],
        n: Optional[int] = None,
    ) -> T:
        """Create a sequence from floating-point values.

        Parameters
        ----------
        coefficients
            coefficients of the constraints in the sequence to create
            (in order)
        bounds
            boundaries of the constraints in the sequence to create
            (in order)
        n
            number of unknowns constrained by the sequence to create

        Raises
        ------
        ValueError
            if the length of `coefficients` is not equal to the length
            of `bounds`,
            if any value in `coefficients` is non-finite,
            if any value in `bounds` is nan,
            if the iterables in `coefficients` do not all have the same
            length,
            if `n` does not match with the length of the iterables in
            `coefficients`, or
            if `n` is negative

        Returns
        -------
        T
            sequence of constraints
        """
        coefficients_, bounds_ = tuple(coefficients), tuple(bounds)  # freeze!
        cls._raise_if_length_mismatch(coefficients_, bounds_)
        return cls._from_float(coefficients_, bounds_, n)

    @classmethod
    def _raise_if_length_mismatch(
        cls: Type[T],
        coefficients: Tuple[Iterable[SupportsFloat], ...],
        bounds: Tuple[SupportsFloat, ...],
    ):
        if len(coefficients) != len(bounds):
            msg = (
                f"cannot instantiate {cls.__name__}; "
                f"length of coefficients must be equal to length"
                f"of bounds"
            )
            raise ValueError(msg)

    @classmethod
    def _from_float(
        cls: Type[T],
        coefficients: Tuple[Iterable[SupportsFloat], ...],
        bounds: Tuple[SupportsFloat, ...],
        n: Optional[int],
    ) -> T:
        return cls(
            (
                Constraint.from_float(coef, bound)
                for coef, bound in zip(coefficients, bounds)
            ),
            n=n,
        )

    def __init__(
        self,
        values: Iterable[Constraint],
        *,
        n: Optional[int] = None,
    ):
        super().__init__(values)
        self._n = self._discover(n)
        self._raise_if_number_of_unknowns_mismatch()

    def _discover(self, n: Optional[int]):
        if n is not None:
            self._raise_if_is_negative(n)
            return n
        if len(self) == 0:
            return 0
        return self[0].n

    def _raise_if_is_negative(self, n: int):
        if n < 0:
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"n must be non-negative"
            )
            raise ValueError(msg)

    def _raise_if_number_of_unknowns_mismatch(self):
        if self._is_number_of_unknowns_mismatch():
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"values must all have the same n, and it must "
                f"match with the n provided (if provided)"
            )
            raise ValueError(msg)

    def _is_number_of_unknowns_mismatch(self):
        set_ = set(value.n for value in self)
        set_.add(self._n)
        return len(set_) > 1

    @property
    def n(self) -> int:
        """Number of unknowns constrained by this sequence."""
        return self._n

    @property
    def coefficients(self) -> CoefficientMatrix:
        """Coefficients of the constraints in this sequence (in order)."""
        return CoefficientMatrix(value.coefficients for value in self)

    @property
    def bounds(self) -> BoundSequence:
        """Boundaries of the constraints in this sequence (in order)."""
        return BoundSequence(value.bound for value in self)
