from portan.utilities.collections import Matrix

from ..mean.sequence import MeanSequence
from ..scatter import CorrelationMatrix, CovarianceMatrix
from .sequence import RateSequence


class RateMatrix(Matrix[RateSequence]):
    """Immutable matrix of rates."""

    def means(self) -> MeanSequence:
        """Get the sample mean (i.e., arithmetic) of each sequence
        in this matrix.

        Returns
        -------
        MeanSequence
            sample mean of each sequence in this matrix (in order)
        """
        return MeanSequence(value.mean() for value in self)

    def covariances(self) -> CovarianceMatrix:
        """Get the covariance matrix of the covariances between
        each sequence in this matrix.

        Returns
        -------
        CovarianceMatrix
            covariance matrix of the covariances between each
            sequence in this matrix
        """
        return CovarianceMatrix.from_iterable(
            [
                [sequence.covariance(other) for other in self]
                for sequence in self
            ]
        )

    def correlations(self) -> CovarianceMatrix:
        """Get the correlation matrix of the correlations between
        each sequence in this matrix.

        Raises
        ------
        ValueError
            if any correlation is undefined (i.e., NaN)
            (shouldn't happen in practice!)

        Returns
        -------
        CorrelationMatrix
            correlation matrix of the correlations between each
            sequence in this matrix
        """
        return CorrelationMatrix.from_iterable(
            [
                [sequence.correlation(other) for other in self]
                for sequence in self
            ]
        )
