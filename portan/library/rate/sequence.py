import statistics as stats
from typing import Iterable, SupportsFloat, Type, TypeVar

from portan.utilities.collections import Sequence

from ..brownian import IArithmeticBrownian
from ..mean import Mean
from ..scatter import Correlation, Covariance, Dispersion
from .rate import Rate

T = TypeVar("T", bound="RateSequence")


class RateSequence(Sequence[Rate], IArithmeticBrownian):
    """Immutable sequence of rates."""

    @classmethod
    def from_float(
        cls: Type[T],
        values: Iterable[SupportsFloat],
    ) -> T:
        """Create a sequence from floating-point values.

        Parameters
        ----------
        values
            values to create the sequence from

        Raises
        ------
        ValueError
            if any value in `values` is non-finite

        Returns
        -------
        T
            sequence of rates
        """
        return cls(Rate(value) for value in values)

    def mean(self) -> Mean:
        """Get the sample (i.e., arithmetic) mean of the rates in
        this sequence.

        Returns
        -------
        Mean
            sample mean of the rates in this sequence
        """
        if len(self) == 0:
            return Mean(0.0)
        elif len(self) == 1:
            return Mean(self[0])
        return Mean(stats.mean(self._to_floats()))

    def dispersion(self) -> Dispersion:
        """Get the sample dispersion (i.e., standard deviation) of the
        rates in this sequence.

        Returns
        -------
        Dispersion
            sample dispersion of the rates in this sequence
        """
        if len(self) <= 1:
            return Dispersion(0.0)
        return Dispersion(stats.stdev(self._to_floats()))

    def correlation(self: T, other: T) -> Correlation:
        """Get the sample correlation of the rates in this sequence
        with the rates in `other`.

        Parameters
        ----------
        other
            sequence for which to get the correlation with this sequence

        Raises
        ------
        ValueError
            if the length of `other` and `self` are not equal,
            if both the sample covariance of `other` and `self`, and
            the sample dispersion of `self` or of `other` are non-finite
            (shouldn't happen in practice!)

        Returns
        -------
        Correlation
            sample correlation between the rates in this sequence
            and the rates in `other`
        """
        self._raise_if_length_mismatch_with_other(other)
        if Dispersion(0.0) in (self.dispersion(), other.dispersion()):
            return Correlation(0.0)
        return Correlation.robust(self._correlation(other))

    def _correlation(self: T, other: T) -> float:
        return (
            float(self.covariance(other))
            / float(self.dispersion())
            / float(other.dispersion())
        )

    def covariance(self: T, other: T) -> Covariance:
        """Get the sample covariance of the rates in this sequence
        with the rates in `other`.

        Parameters
        ----------
        other
            sequence for which to get the covariance with this sequence

        Raises
        ------
        ValueError
            if the length of `other` and `self` are not equal

        Returns
        -------
        Covariance
            sample covariance between the rates in this sequence
            and the rates in `other`
        """
        self._raise_if_length_mismatch_with_other(other)
        if len(self) <= 1:
            return Covariance(0.0)
        return Covariance(self._covariance(other))

    def _raise_if_length_mismatch_with_other(self: T, other: T):
        if len(self) != len(other):
            msg = (
                "cannot determine covariance; length of other must be "
                "equal to this sequence length"
            )
            raise ValueError(msg)

    def _covariance(self: T, other: T) -> float:
        s_mean, o_mean = float(self.mean()), float(other.mean())
        sum_ = sum(
            (s - s_mean) * (o - o_mean)
            for s, o in zip(self._to_floats(), other._to_floats())
        )
        return sum_ / (len(self) - 1)

    def _to_floats(self) -> Iterable[float]:
        return (float(value) for value in self)
