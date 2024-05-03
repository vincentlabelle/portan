from typing import SupportsFloat

from portan.utilities.finite import Finite


class PositiveFinite(Finite):
    """Strictly positive finite floating-point number.

    Parameters
    ----------
    value: SupportsFloat
        strictly positive finite value

    Raises
    ------
    ValueError
        if `value` is not finite, or
        if `value` is not strictly positive
    """

    def __init__(self, value: SupportsFloat):
        super().__init__(value)
        self._raise_if_is_negative_or_zero()

    def _raise_if_is_negative_or_zero(self):
        if self._value <= 0.0:
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"value must be strictly positive"
            )
            raise ValueError(msg)
