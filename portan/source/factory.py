from .source import PriceSource
from .source.multiple import MultipleSource
from .yahoo import Yahoo


class PriceSourceFactory:
    """Simple factory of :py:class:`PriceSource`."""

    def get(self, name: str) -> PriceSource:
        """Get a :py:class:`PriceSource` which fetches all prices
        from `name` (e.g., yahoo).

        Parameters
        ----------
        name: str
            name of source of prices for the constructed
            :py:class:`PriceSource`

        Raises
        ------
        ValueError
            if `name` is an unknown source of prices

        Returns
        -------
        PriceSource
            source of price
        """
        single = self._get_single(name)
        return PriceSource(single, MultipleSource(single))

    def _get_single(self, name: str):
        if name == "yahoo":
            return Yahoo()
        self._raise_due_to_unknown_source()

    @staticmethod
    def _raise_due_to_unknown_source():
        msg = "cannot create source; unknown source"
        raise ValueError(msg)
