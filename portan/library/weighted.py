from typing import Type, TypeVar

from .brownian import IArithmeticBrownian
from .mean import Mean
from .rate.matrix import RateMatrix
from .scatter import Dispersion
from .weight.sequence import WeightSequence

T = TypeVar("T", bound="Weighted")


class Weighted(IArithmeticBrownian):
    """Weighted sequences of rates, where each sequence of rates
    is a sample of a random variable.

    Parameters
    ----------
    weights
        ordered weights associated to each sequence of rates
        (or random variable)
    rates
        unweighted sequences of rates

    Raises
    ------
    ValueError
        if the length of `weights` and `rates` are not equal
    """

    @classmethod
    def empty(cls: Type[T]) -> T:
        """Create a weighted with an empty sequence of weights, and
        an empty matrix of rates.

        Returns
        -------
        T
            empty weighted
        """
        return cls(WeightSequence([]), RateMatrix([]))

    def __init__(self, weights: WeightSequence, rates: RateMatrix):
        self._weights = weights
        self._rates = rates
        self._raise_if_length_mismatch()

    def _raise_if_length_mismatch(self):
        if len(self._weights) != len(self._rates):
            msg = (
                f"cannot instantiate {self.__class__.__name__}; "
                f"length of arguments must be equal"
            )
            raise ValueError(msg)

    def mean(self) -> Mean:
        """Get the sample mean (i.e., arithmetic) of the weighted
        sum of the random variables, where each sequence of rates
        is a sample of a random variable.

        Returns
        -------
        Mean
            sample mean of the weighted sum of the random variables
        """
        means = self._rates.means()
        return means.sum(self._weights)

    def dispersion(self) -> Dispersion:
        """Get the sample dispersion (i.e., standard deviation) of the
        weighted sum of the random variables, where each sequence
        of rates is a sample of a random variable.

        Raises
        ------
        ValueError
            if the sample variance of the weighted sum is negative
            (shouldn't happen in practice!)

        Returns
        -------
        Dispersion
            sample dispersion of the weighted sum of the
            random variables
        """
        covariances = self._rates.covariances()
        variance = covariances.variance(self._weights)
        return variance.to_dispersion()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._weights == other._weights and self._rates == other._rates

    def __hash__(self) -> int:
        return hash((self._weights, self._rates))

    def __str__(self) -> str:
        return f"(weights={self._weights}, rates={self._rates})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}{self}>"
