from typing import Iterable, SupportsFloat, Type, TypeVar

from ..coefficient.sequence import CoefficientSequence
from .bound import Bound

T = TypeVar("T", bound="Constraint")


class Constraint:
    """A linear constraint constraining a sequence of unknowns of size `n`.
    The constraint is composed of `n` coefficients and a boundary.

    Parameters
    ----------
    coefficients: CoefficientSequence
        coefficients of the constraint
    bound: Bound
        boundary of the constraint
    """

    @classmethod
    def from_float(
        cls: Type[T],
        coefficients: Iterable[SupportsFloat],
        bound: SupportsFloat,
    ) -> T:
        """Create a constraint from floating-point numbers.

        Parameters
        ----------
        coefficients
            coefficients of the constraint
        bound
            boundary of the constraint

        Raises
        ------
        ValueError
            if any value in `coefficients` is non-finite, or
            if `bound` is nan

        Returns
        -------
        T
            constraint
        """
        return cls(
            CoefficientSequence.from_float(coefficients),
            Bound(bound),
        )

    def __init__(self, coefficients: CoefficientSequence, bound: Bound):
        self._coefficients = coefficients
        self._bound = bound

    @property
    def n(self) -> int:
        """Number of unknowns constrained by this constraint."""
        return len(self._coefficients)

    @property
    def coefficients(self) -> CoefficientSequence:
        """Coefficients of this constraint."""
        return self._coefficients

    @property
    def bound(self) -> Bound:
        """Boundary of this constraint."""
        return self._bound

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self._coefficients == other._coefficients
            and self._bound == other._bound
        )

    def __hash__(self) -> int:
        return hash((self._coefficients, self._bound))

    def __str__(self) -> str:
        return f"(coefficients={self._coefficients}, bound={self._bound})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}{self}>"
