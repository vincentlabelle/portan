from typing import Iterable, SupportsFloat, Tuple, TypeVar

from portan.utilities.collections import Sequence

from .mean import Mean

T = TypeVar("T", bound="MeanSequence")


class MeanSequence(Sequence[Mean]):
    def sum(self, factors: Iterable[SupportsFloat]) -> Mean:
        """Get the weighted sum of the means in this sequence.

        Raises
        ------
        ValueError
            if the length of `factors` is not equal to the length of
            this sequence, or
            if any factor in `factors` is nan

        Returns
        -------
        Mean
            weighted sum of the means in this sequence
        """
        if len(self) == 0:
            return Mean(0.0)
        scaled = self._scale(factors)
        return scaled._sum()

    def _scale(self: T, factors: Iterable[SupportsFloat]) -> T:
        factors_ = tuple(factors)  # freeze!
        self._raise_if_length_mismatch_with_factors(factors_)
        return self.__class__(
            value.scale(factor) for value, factor in zip(self, factors_)
        )

    def _raise_if_length_mismatch_with_factors(
        self,
        factors: Tuple[SupportsFloat, ...],
    ):
        if len(factors) != len(self):
            msg = (
                "cannot scale; length of factors must be equal "
                "to the length of this sequence"
            )
            raise ValueError(msg)

    def _sum(self) -> Mean:
        return sum(self, start=Mean(0.0))
