from enum import Enum


class Source(Enum):
    """Source of prices (e.g., Yahoo)."""

    YAHOO = "yahoo"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self})>"
