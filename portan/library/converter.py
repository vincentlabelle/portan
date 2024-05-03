from .brownian import IArithmeticBrownian
from .frequency import Frequency
from .mean import Mean
from .scatter import Dispersion


class BrownianConverter(IArithmeticBrownian):
    """Converter of frequency of an arithmetic brownian motion.

    Parameters
    ----------
    brownian
        motion to convert the frequency for
    from_
        frequency to convert from
    to
        frequency to convert to
    """

    def __init__(
        self,
        brownian: IArithmeticBrownian,
        from_: Frequency,
        to: Frequency,
    ):
        self._brownian = brownian
        self._from = from_
        self._to = to

    def mean(self) -> Mean:
        """Get the sample mean of the converted motion.

        Returns
        -------
        Mean
            sample mean of the converted motion
        """
        mean = self._brownian.mean()
        return mean.scale(self._from.value / self._to.value)

    def dispersion(self) -> Dispersion:
        """Get the sample dispersion (i.e., standard deviation) of
        the converted motion.

        Returns
        -------
        Dispersion
            sample dispersion of the converted motion
        """
        dispersion = self._brownian.dispersion()
        return dispersion.scale(self._from.value / self._to.value)
