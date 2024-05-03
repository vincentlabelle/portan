from .mean import Mean
from .scatter import Dispersion


class IArithmeticBrownian:
    """Interface for an arithmetic brownian motion."""

    def mean(self) -> Mean:
        """Get the sample mean of the motion.

        Returns
        -------
        Mean
            sample mean of the motion
        """
        raise NotImplementedError

    def dispersion(self) -> Dispersion:
        """Get the sample dispersion (i.e., standard deviation)
        of the motion

        Returns
        -------
        Dispersion
            sample dispersion of the motion
        """
        raise NotImplementedError
