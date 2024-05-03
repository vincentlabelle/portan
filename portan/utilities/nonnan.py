from math import isnan
from typing import SupportsFloat


class NonNan:
    """A floating-point number which isn't NaN.

    Parameters
    ----------
    value: SupportsFloat
        non-nan value

    Raises
    ------
    ValueError
        if `value` is nan
    """

    def __init__(self, value: SupportsFloat):
        self._value = float(value)
        self._raise_if_is_nan()

    def _raise_if_is_nan(self):
        if isnan(self._value):
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"value must not be NaN"
            )
            raise ValueError(msg)

    def __float__(self) -> float:
        return float(self._value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self})>"
