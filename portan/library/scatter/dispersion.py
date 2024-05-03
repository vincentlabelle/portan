from math import isnan, sqrt
from typing import SupportsFloat, TypeVar

from portan.utilities.nonnan import NonNan

T = TypeVar("T", bound="Dispersion")


class Dispersion(NonNan):
    """Measure of the amount of variation or *dispersion* of a set of
    values (i.e., standard deviation).

    Parameters
    ----------
    value: SupportsFloat
        dispersion

    Raises
    ------
    ValueError
        if `value` is negative, or
        if `value` is nan
    """

    def __init__(self, value: SupportsFloat):
        super().__init__(value)
        self._raise_if_is_negative()

    def _raise_if_is_negative(self):
        if self._value < 0.0:
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"value must be non-negative"
            )
            raise ValueError(msg)

    def scale(self: T, factor: SupportsFloat) -> T:
        """Obtain dispersion of the scaled random variable underlying
        this dispersion (i.e., STD(factor * X)).

        Parameters
        ----------
        factor
            factor by which to scale the random variable underlying
            this dispersion

        Raises
        ------
        ValueError
            if `factor` is negative, or
            if `factor` is nan

        Returns
        -------
        T
            scaled dispersion
        """
        self._raise_if_factor_is_negative(factor)
        self._raise_if_factor_is_nan(factor)
        return self.__class__(self._value * sqrt(factor))

    @staticmethod
    def _raise_if_factor_is_negative(factor: SupportsFloat):
        if float(factor) < 0.0:
            msg = "cannot scale; factor must be non-negative"
            raise ValueError(msg)

    @staticmethod
    def _raise_if_factor_is_nan(factor: SupportsFloat):
        if isnan(float(factor)):
            msg = "cannot scale; factor must not be NaN"
            raise ValueError(msg)
