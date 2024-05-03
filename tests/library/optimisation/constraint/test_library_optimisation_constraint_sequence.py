from typing import Optional, Tuple

import pytest

from portan.library.optimisation.coefficient.matrix import CoefficientMatrix
from portan.library.optimisation.constraint import Constraint
from portan.library.optimisation.constraint.bound.sequence import BoundSequence
from portan.library.optimisation.constraint.sequence import ConstraintSequence


class TestConstraintSequenceInvariants:
    @pytest.mark.parametrize("n", [None, 0, 2])
    def test_when_n_discovery_when_empty(self, n: Optional[int]):
        sequence = ConstraintSequence([], n=n)
        if n is None:
            assert sequence.n == 0
        else:
            assert sequence.n == n

    @pytest.mark.parametrize("n", [None, 3])
    def test_when_n_discovery_when_non_empty(self, n: Optional[int]):
        sequence = ConstraintSequence(
            [
                Constraint.from_float([1.0, 2.0, 3.0], 4.0),
                Constraint.from_float([5.0, 6.0, 7.0], 8.0),
            ],
            n=n,
        )
        assert sequence.n == 3

    @pytest.mark.parametrize("coefficients", [(4.0,), (4.0, 5.0, 6.0)])
    def test_when_values_n_mismatch(self, coefficients: Tuple[float, ...]):
        with pytest.raises(ValueError, match="same n"):
            ConstraintSequence(
                [
                    Constraint.from_float([1.0, 2.0], 3.0),
                    Constraint.from_float(coefficients, 6.0),
                    Constraint.from_float([7.0, 8.0], 9.0),
                ]
            )

    @pytest.mark.parametrize("n", [1, 3])
    def test_when_n_mismatch(self, n: int):
        with pytest.raises(ValueError, match="same n"):
            ConstraintSequence(
                [
                    Constraint.from_float([1.0, 2.0], 3.0),
                    Constraint.from_float([3.0, 4.0], 5.0),
                ],
                n=n,
            )

    def test_when_n_is_negative(self):
        with pytest.raises(ValueError, match="non-negative"):
            ConstraintSequence([], n=-1)


@pytest.fixture(scope="module")
def n() -> int:
    return 2


@pytest.fixture(scope="module")
def values() -> Tuple[Constraint, ...]:
    return (
        Constraint.from_float([1.0, 2.0], 3.0),
        Constraint.from_float([4.0, 5.0], 6.0),
    )


@pytest.fixture(scope="module")
def sequence(
    values: Tuple[Constraint, ...],
    n: int,
) -> ConstraintSequence:
    return ConstraintSequence(values, n=n)


class TestConstraintSequenceAlternativeConstructors:
    @pytest.mark.parametrize("n", [None, 0, 2])
    def test_empty(self, n: Optional[int]):
        result = ConstraintSequence.empty(n)
        expected = ConstraintSequence([], n=n)
        assert result == expected

    @pytest.mark.parametrize(
        "bounds",
        [
            (1.0,),
            (1.0, 2.0, 3.0),
        ],
    )
    def test_from_float_when_length_mismatch(self, bounds: Tuple[float, ...]):
        with pytest.raises(ValueError, match="length of coefficients"):
            ConstraintSequence.from_float(
                coefficients=[
                    [1.0, 2.0],
                    [3.0, 4.0],
                ],
                bounds=bounds,
            )

    def test_from_float(self, sequence: ConstraintSequence):
        result = ConstraintSequence.from_float(
            coefficients=(
                (float(value) for value in seq) for seq in sequence.coefficients
            ),
            bounds=(float(bound) for bound in sequence.bounds),
        )
        assert result == sequence

    def test_from_float_suppots_float(self, sequence: ConstraintSequence):
        result = ConstraintSequence.from_float(
            coefficients=sequence.coefficients,
            bounds=sequence.bounds,
        )
        assert result == sequence


class TestConstraintSequenceProperties:
    def test_n(self, sequence: ConstraintSequence, n: int):
        assert sequence.n == n

    def test_set_n(self, sequence: ConstraintSequence, n: int):
        with pytest.raises(AttributeError):
            sequence.n = n

    def test_coefficients(
        self,
        sequence: ConstraintSequence,
        values: Tuple[Constraint, ...],
    ):
        expected = CoefficientMatrix(value.coefficients for value in values)
        assert sequence.coefficients == expected

    def test_set_coefficients(self, sequence: ConstraintSequence):
        with pytest.raises(AttributeError):
            sequence.coefficients = CoefficientMatrix([])

    def test_bounds(
        self,
        sequence: ConstraintSequence,
        values: Tuple[Constraint, ...],
    ):
        expected = BoundSequence(value.bound for value in values)
        assert sequence.bounds == expected

    def test_set_bounds(self, sequence: ConstraintSequence):
        with pytest.raises(AttributeError):
            sequence.bounds = BoundSequence([])


class TestConstraintSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> ConstraintSequence:
        return ConstraintSequence([])

    def test_from_float(self, sequence: ConstraintSequence):
        other = ConstraintSequence.from_float(coefficients=[], bounds=[])
        assert other == sequence

    def test_n(self, sequence: ConstraintSequence):
        assert sequence.n == 0

    def test_coefficients(self, sequence: ConstraintSequence):
        assert sequence.coefficients == CoefficientMatrix([])

    def test_bounds(self, sequence: ConstraintSequence):
        assert sequence.bounds == BoundSequence([])
