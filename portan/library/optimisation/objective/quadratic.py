from ..coefficient.matrix import SymmetricCoefficientMatrix


class QuadraticCoefficients(SymmetricCoefficientMatrix):
    """Coefficients of the quadratic term of an objective function
    of a program to solve. The solution of the program is a
    sequence of size `n`."""

    @property
    def n(self) -> int:
        """Number of unknowns of the program"""
        return len(self)
