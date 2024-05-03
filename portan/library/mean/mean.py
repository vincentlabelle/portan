from math import isnan
from typing import SupportsFloat, TypeVar

from portan.utilities.nonnan import NonNan

T = TypeVar("T", bound="Mean")


class Mean(NonNan):
    """Measure of central point of a set of values."""

    def scale(self: T, factor: SupportsFloat) -> T:
        """Scale this mean by `factor`.

        Parameters
        ----------
        factor
            factor to scale the mean by

        Raises
        ------
        ValueError
            if `factor` is nan

        Returns
        -------
        T
            scaled mean
        """
        factor_ = float(factor)
        self._raise_if_factor_is_nan(factor_)
        return self.__class__(self._value * factor_)

    @staticmethod
    def _raise_if_factor_is_nan(factor: float):
        if isnan(factor):
            msg = "cannot scale; factor must not be NaN"
            raise ValueError(msg)

    def __add__(self: T, other: object) -> T:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(self._value + other._value)

    def __sub__(self: T, other: object) -> T:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(self._value - other._value)
