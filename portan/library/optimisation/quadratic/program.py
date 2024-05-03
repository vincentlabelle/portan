from typing import Optional

from ..constraint import LinearConstraints
from ..objective.linear import LinearCoefficients
from ..objective.quadratic import QuadraticCoefficients


class QuadraticProgram:
    """Quadratic program to solve for a sequence of `n` unknowns. The
    program is of the form::

        minimize 0.5 * x^T * P * x + q^T * x
        subject to A_ub * x <= b_ub
        and A_eq * x == b_eq

    where x is a sequence of `n` unknowns, P is a semi-definite `n` x `n`
    matrix of coefficients, q is a vector of coefficients of size `n`,
    A_ub is a `m_ub` x `n` matrix of coefficients, A_eq is a `m_eq` x `n`
    matrix of coefficients, b_ub is a vector of boundaries of size `m_ub`
    and b_eq is a vector of boundaries of size `m_eq`.

    Parameters
    ----------
    quadratic: QuadraticCoefficients
        quadratic coefficients of the objective function
    constraints: LinearConstraints
        linear constraints
    linear: Optional[LinearCoefficients]
        linear coefficients of the objective function (defaults to None)

    Raises
    ------
    ValueError
        if `quadratic.n` is not equal to `constraints.n`, or
        if `linear` is not None and `linear.n` is not equal to `quadratic.n`
    """

    def __init__(
        self,
        *,
        quadratic: QuadraticCoefficients,
        constraints: LinearConstraints,
        linear: Optional[LinearCoefficients] = None,
    ):
        self._quadratic = quadratic
        self._constraints = constraints
        self._linear = linear
        self._raise_if_number_of_unknowns_mismatch()

    @property
    def n(self) -> int:
        """Number of the unknowns to solve for within this program."""
        return self._quadratic.n

    @property
    def quadratic(self) -> QuadraticCoefficients:
        """Quadratic coefficients of the objective function of this program."""
        return self._quadratic

    @property
    def constraints(self) -> LinearConstraints:
        """Linear constraints of this program"""
        return self._constraints

    @property
    def linear(self) -> Optional[LinearCoefficients]:
        """Linear coefficients of the objective function of this program."""
        return self._linear

    def _raise_if_number_of_unknowns_mismatch(self):
        msg = (
            f"cannot instantiate {self.__class__.__name__}; "
            f"quadratic, linear and constraints must have the "
            f"same n (i.e., number of unknowns)"
        )
        if self._quadratic.n != self._constraints.n:
            raise ValueError(msg)
        if self._linear is not None:
            if self._quadratic.n != self._linear.n:
                raise ValueError(msg)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self._quadratic == other._quadratic
            and self._constraints == other._constraints
            and self._linear == other._linear
        )

    def __hash__(self) -> int:
        return hash((self._quadratic, self._constraints, self._linear))

    def __str__(self) -> str:
        if self._linear is None:
            return (
                f"("
                f"quadratic={self._quadratic}, "
                f"constraints={self._constraints}"
                f")"
            )
        return (
            f"("
            f"quadratic={self._quadratic}, "
            f"constraints={self._constraints}, "
            f"linear={self._linear}"
            f")"
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}{self}>"
