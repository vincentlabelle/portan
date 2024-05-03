from typing import Optional, Type, TypeVar

from .equalities import LinearEqualities
from .inequalities import LinearInequalities

T = TypeVar("T", bound="LinearConstraints")


class LinearConstraints:
    """Linear **equality** and **inequality** constraints constraining
    a sequence of unknowns of size `n`. The inequality constraints
    are of the form ax <= b.

    Parameters
    ----------
    equalities
        equality constraints constraining the sequence of unknowns
    inequalities
        inequality constraints constraining the sequence of unknowns

    Raises
    ------
    ValueError
        if `equalities.n` is not equal to `inequalities.n`
    """

    @classmethod
    def empty(cls: Type[T], n: Optional[int]) -> T:
        """Create a empty linear constraints.

        Parameters
        ----------
        n
            number of unknowns constrained by the sequence to create

        Returns
        -------
        T
            empty linear constraints
        """
        return cls(
            LinearEqualities.empty(n),
            LinearInequalities.empty(n),
        )

    def __init__(
        self,
        equalities: LinearEqualities,
        inequalities: LinearInequalities,
    ):
        self._equalities = equalities
        self._inequalities = inequalities
        self._raise_if_number_of_unknowns_mismatch()

    def _raise_if_number_of_unknowns_mismatch(self):
        if self._equalities.n != self._inequalities.n:
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"equalities and inequalities must have the same n"
            )
            raise ValueError(msg)

    @property
    def n(self) -> int:
        """Number of unknowns constraints by this `LinearConstraints`."""
        return self._equalities.n

    @property
    def equalities(self) -> LinearEqualities:
        """Equality constraints of this `LinearConstraints` constraining
        the unknowns."""
        return self._equalities

    @property
    def inequalities(self) -> LinearInequalities:
        """Inequality constraints of this `LinearConstraints` constraining
        the unknowns."""
        return self._inequalities

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self._equalities == other._equalities
            and self._inequalities == other._inequalities
        )

    def __hash__(self) -> int:
        return hash((self._equalities, self._inequalities))

    def __str__(self) -> str:
        return (
            f"("
            f"equalities={self._equalities}, "
            f"inequalities={self._inequalities}"
            f")"
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}{self}>"
