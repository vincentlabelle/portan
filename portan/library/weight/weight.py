from math import isnan
from typing import SupportsFloat, SupportsInt, Type, TypeVar

T = TypeVar("T", bound="Weight")


class Weight:
    """Weight in percentage with precision of 0 decimal places (e.g., 25%).

    Parameters
    ----------
    value: int
        weight in percentage (e.g., a value of 50 represents 50%)
    """

    @classmethod
    def from_float(cls: Type[T], value: SupportsFloat) -> T:
        """Create a weight from a floating-point number. If the
        floating point number has too much precision, the number
        is rounded using a half-even strategy.

        Parameters
        ----------
        value
            floating-point number to create a weight from

        Raises
        ------
        ValueError
            if `value` is nan
        OverflowError
            if `value` is too big in absolute terms (i.e., there's
            an overflow during the conversion)

        Returns
        -------
        T
            weight
        """
        value_ = float(value)
        cls._raise_if_value_is_nan(value_)
        return cls._from_float(value_)

    @classmethod
    def _raise_if_value_is_nan(cls, value: float):
        if isnan(value):
            msg = f"cannot instantiate {cls.__name__}; value must not be NaN"
            raise ValueError(msg)

    @classmethod
    def _from_float(cls: Type[T], value: float) -> T:
        rounded = round(value * 100.0, 0)
        try:
            converted = int(rounded)
        except OverflowError:
            msg = (
                f"cannot instantiate {cls.__name__}; "
                f"value is too big in absolute terms"
            )
            raise OverflowError(msg)
        return cls(converted)

    def __init__(self, value: SupportsInt):
        self._value = int(value)

    def __add__(self: T, other: object) -> T:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__class__(self._value + other._value)

    def __int__(self) -> int:
        return self._value

    def __float__(self) -> float:
        return float(str(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return f"{self._sign}{self._digits}"

    @property
    def _sign(self) -> str:
        if self._value < 0:
            return "-"
        return ""

    @property
    def _digits(self) -> str:
        abs_ = abs(self._value)
        if abs_ < 10:
            return f"0.0{abs_}"
        elif abs_ < 100:
            return f"0.{abs_}"
        return f"{str(abs_)[:-2]}.{str(abs_)[-2:]}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self})>"
