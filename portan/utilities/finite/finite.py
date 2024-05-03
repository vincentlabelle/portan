from math import isfinite
from typing import SupportsFloat, TypeVar

T = TypeVar("T", bound="Finite")


class Finite:
    """Finite floating-point number.

    Parameters
    ----------
    value: SupportsFloat
        finite value

    Raises
    ------
    ValueError
        if `value` is not finite
    """

    def __init__(self, value: SupportsFloat):
        self._value = float(value)
        self._raise_if_is_not_finite()

    def _raise_if_is_not_finite(self):
        if not isfinite(self._value):
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"value must be finite"
            )
            raise ValueError(msg)

    def __float__(self) -> float:
        return self._value

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
