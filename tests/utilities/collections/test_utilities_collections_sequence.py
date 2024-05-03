from random import sample
from typing import Any, Callable, Tuple

import pytest

from portan.utilities.collections import Sequence


class _T:
    def __init__(self, value: int):
        self._value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self})>"


class TestSequenceInvariants:
    def test_freezes(self):
        values = [
            _T(0),
            _T(1),
            _T(2),
        ]
        initial = Sequence(values)
        values[1] = _T(0)
        final = Sequence(values)
        assert initial != final


@pytest.fixture(scope="module")
def values() -> Tuple[_T, ...]:
    return (
        _T(0),
        _T(1),
        _T(2),
    )


@pytest.fixture(scope="module")
def sequence(values: Tuple[_T, ...]) -> Sequence:
    return Sequence(values)


class TestSequenceStringRepresentation:
    def test_str(self, sequence: Sequence, values: Tuple[_T, ...]):
        expected = f"({', '.join(str(value) for value in values)})"
        assert str(sequence) == expected

    def test_repr(self, sequence: Sequence):
        expected = f"<{sequence.__class__.__name__}{sequence}>"
        assert repr(sequence) == expected


@pytest.fixture(scope="module")
def shuffle() -> Callable[[Tuple[Any, ...]], Tuple[Any, ...]]:
    def _shuffle(values: Tuple[Any, ...]) -> Tuple[Any, ...]:
        shuffled, length = values, len(values)
        while shuffled == values:
            shuffled = tuple(sample(shuffled, k=length))
        return shuffled

    return _shuffle


class TestSequenceEqual:
    def test_when_equal(
        self,
        sequence: Sequence,
        values: Tuple[_T, ...],
    ):
        other = Sequence(values)
        assert other == sequence

    def test_when_different_values(self, sequence: Sequence):
        other = Sequence([_T(0)] * len(sequence))
        assert other != sequence

    def test_when_different_len(
        self,
        sequence: Sequence,
        values: Tuple[_T, ...],
    ):
        other = Sequence(values + (_T(0),))
        assert other != sequence

    def test_when_different_order(
        self,
        sequence: Sequence,
        values: Tuple[_T, ...],
        shuffle: Callable[[Tuple[Any, ...]], Tuple[Any, ...]],
    ):
        other = Sequence(shuffle(values))
        assert other != sequence

    def test_when_different_object(self, sequence: Sequence):
        assert sequence != "a"


class TestSequenceHash:
    def test_when_equal(
        self,
        sequence: Sequence,
        values: Tuple[_T, ...],
    ):
        other = Sequence(values)
        assert hash(other) == hash(sequence)

    def test_when_different_values(self, sequence: Sequence):
        other = Sequence([_T(0)] * len(sequence))
        assert hash(other) != hash(sequence)

    def test_when_different_len(
        self,
        sequence: Sequence,
        values: Tuple[_T, ...],
    ):
        other = Sequence(values + (_T(0),))
        assert hash(other) != hash(sequence)

    def test_when_different_order(
        self,
        sequence: Sequence,
        values: Tuple[_T, ...],
        shuffle: Callable[[Tuple[Any, ...]], Tuple[Any, ...]],
    ):
        other = Sequence(shuffle(values))
        assert hash(other) != hash(sequence)


class TestSequenceIsSequence:
    def test_len(self, sequence: Sequence, values: Tuple[_T, ...]):
        assert len(sequence) == len(values)

    def test_getitem_when_slice(
        self,
        sequence: Sequence,
        values: Tuple[_T, ...],
    ):
        assert sequence[1:] == Sequence(values[1:])

    def test_getitem_when_int(
        self,
        sequence: Sequence,
        values: Tuple[_T, ...],
    ):
        assert sequence[1] == values[1]

    def test_getitem_when_out_of_bounds(self, sequence: Sequence):
        with pytest.raises(IndexError):
            sequence[len(sequence)]

    def test_is_immutable(self, sequence: Sequence):
        with pytest.raises(TypeError):
            sequence[1] = _T(0)


class TestSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> Sequence:
        return Sequence([])

    def test_str(self, sequence: Sequence):
        assert str(sequence) == "()"

    def test_repr(self, sequence: Sequence):
        assert repr(sequence) == f"<{sequence.__class__.__name__}()>"

    def test_eq_when_equal(self, sequence: Sequence):
        other = Sequence([])
        assert other == sequence

    def test_eq_when_unequal(self, sequence: Sequence):
        other = Sequence([_T(0)])
        assert other != sequence

    def test_hash_when_equal(self, sequence: Sequence):
        other = Sequence([])
        assert hash(other) == hash(sequence)

    def test_hash_when_unequal(self, sequence: Sequence):
        other = Sequence([_T(0)])
        assert hash(other) != hash(sequence)

    def test_len(self, sequence: Sequence):
        assert len(sequence) == 0

    def test_getitem_when_slice(self, sequence: Sequence):
        assert sequence[1:] == sequence

    def test_getitem_when_out_of_bounds(self, sequence: Sequence):
        with pytest.raises(IndexError):
            sequence[0]
