from math import sqrt
from typing import SupportsFloat

from ..dispersion import Dispersion
from .covariance import Covariance


class Variance(Covariance):
    """Measure of the amount of *variation* of a set of
    values.

    Parameters
    ----------
    value: SupportsFloat
        positive non-nan variance

    Raises
    ------
    ValueError
        if `value` is nan, or
        if `value` is negative
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

    def to_dispersion(self) -> Dispersion:
        """Get the standard deviation (i.e., dispersion) from
        this variance.

        Returns
        -------
        Dispersion
            standard deviation from this variance
        """
        return Dispersion(sqrt(self._value))
