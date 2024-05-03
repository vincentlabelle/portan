from typing import SupportsFloat, Type, TypeVar

from portan.utilities.finite import Finite

T = TypeVar("T", bound="Correlation")


class Correlation(Finite):
    """Joint variability of two random variables.

    Parameters
    ----------
    value: SupportsFloat
        correlation

    Raises
    ------
    ValueError
        if `value` is not finite, or
        if `value` is outside [-1.0, 1.0]
    """

    @classmethod
    def robust(cls: Type[T], value: SupportsFloat) -> T:
        """Robustly construct a correlation by rounding down
        values above(below) one(minus one) to one(minus one).

        Parameters
        ----------
        value
            value to construct a correlation from

        Raises
        ------
        ValueError
            if `value` is nan

        Returns
        -------
        T
            correlation from `value`
        """
        value_ = float(value)
        if value_ > 1.0:
            return cls(1.0)
        elif value_ < -1.0:
            return cls(-1.0)
        return cls(value)

    def __init__(self, value: SupportsFloat):
        super().__init__(value)
        self._raise_if_outside_minus_one_and_plus_one()

    def _raise_if_outside_minus_one_and_plus_one(self):
        if not -1.0 <= self._value <= 1.0:
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"value must be inside [-1.0, 1.0]"
            )
            raise ValueError(msg)
