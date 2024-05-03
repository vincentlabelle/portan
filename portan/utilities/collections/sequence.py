from collections.abc import Sequence as abcSequence
from typing import Iterable, TypeVar, Union

T_co = TypeVar("T_co", covariant=True)
S = TypeVar("S", bound="Sequence")


class Sequence(abcSequence[T_co]):
    """Immutable sequence of objects with default implementation
    for __init__, __getitem__, __len__, __eq__, __hash__,
    __str__, and __repr__.

    Parameters
    ----------
    values: Iterable[T_co]
        values to create the sequence from
    """

    def __init__(self, values: Iterable[T_co]):
        self._values = tuple(values)

    def __getitem__(self: S, item: Union[slice, int]) -> Union[S, T_co]:
        if isinstance(item, slice):
            return self.__class__(self._values[item])
        return self._values[item]

    def __len__(self) -> int:
        return len(self._values)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._values == other._values

    def __hash__(self) -> int:
        return hash(self._values)

    def __str__(self) -> str:
        return f"({', '.join(str(value) for value in self)})"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}{self}>"
