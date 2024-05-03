from typing import TypeVar

from portan.utilities.finite import Finite

from ..frequency import Frequency

T = TypeVar("T", bound="Rate")


class Rate(Finite):
    """Continuous rate of growth (e.g., 0.012).

    A rate of growth is represented internally with a
    finite floating-point number with undefined precision.
    """

    def convert(self: T, *, from_: Frequency, to: Frequency) -> T:
        """Convert the frequency of this rate.

        This operation is *not* performed in-place.

        Parameters
        ----------
        from_
            current frequency of this rate
        to
            frequency to convert to

        Raises
        ------
        ValueError
            if the converted rate is non-finite

        Returns
        -------
        T
            rate with converted frequency
        """
        return self.__class__(self._value * from_.value / to.value)
