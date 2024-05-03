from typing import Tuple

import pytest

from portan.source.date import Date
from portan.source.date.sequence import DateSequence


class TestDateSequenceInvariants:
    @pytest.mark.parametrize(
        "values",
        [
            (Date("2021-09-01"), Date("2021-09-02")),
            (Date("2021-09-02"), Date("2021-09-01")),
        ],
    )
    def test_order_does_not_matter(self, values: Tuple[Date, ...]):
        DateSequence(values)  # does not raise

    def test_uniqueness_does_not_matter(self):
        DateSequence(
            (
                Date("2021-09-01"),
                Date("2021-09-01"),
            )
        )  # does not raise


class TestDateSequenceAlternativeConstructors:
    @pytest.fixture(scope="class")
    def values(self) -> Tuple[Date, ...]:
        return Date("2021-09-01"), Date("2021-09-02"), Date("2021-09-03")

    @pytest.fixture(scope="class")
    def sequence(self, values: Tuple[Date, ...]) -> DateSequence:
        return DateSequence(values)

    def test_from_string(
        self,
        sequence: DateSequence,
        values: Tuple[Date, ...],
    ):
        result = DateSequence.from_string(str(value) for value in values)
        assert result == sequence


class TestDateSequenceIsAscending:
    def test_when_one_element(self):
        sequence = DateSequence.from_string(["2021-09-01"])
        assert sequence.is_ascending()

    @pytest.mark.parametrize(
        "values",
        [
            ("2021-09-01", "2021-09-02", "2021-09-03"),
            ("2021-09-01", "2021-09-02", "2021-09-02"),
            ("2021-09-01", "2021-09-03", "2021-09-04"),
        ],
    )
    def test_when_multiple_elements_and_sorted(self, values: Tuple[str, ...]):
        sequence = DateSequence.from_string(values)
        assert sequence.is_ascending()

    @pytest.mark.parametrize(
        "values",
        [
            ("2021-09-01", "2021-09-04", "2021-09-03"),
            ("2021-09-03", "2021-09-02", "2021-09-03"),
            ("2021-09-03", "2021-09-02", "2021-09-01"),
        ],
    )
    def test_when_multiple_elements_and_unsorted(self, values: Tuple[str, ...]):
        sequence = DateSequence.from_string(values)
        assert not sequence.is_ascending()


class TestDateSequenceContainsDuplicates:
    def test_when_one_element(self):
        sequence = DateSequence.from_string(("2021-09-01",))
        assert not sequence.contains_duplicates()

    @pytest.mark.parametrize(
        "values",
        [
            ("2021-09-01", "2021-09-02", "2021-09-01"),
            ("2021-09-01", "2021-09-02", "2021-09-02"),
            ("2021-09-02", "2021-09-02", "2021-09-02"),
        ],
    )
    def test_when_multiple_elements_and_contains_duplicates(
        self,
        values: Tuple[str, ...],
    ):
        sequence = DateSequence.from_string(values)
        assert sequence.contains_duplicates()

    def test_when_multiple_elements_and_does_not_contain_duplicates(self):
        sequence = DateSequence.from_string(
            (
                "2021-09-01",
                "2021-09-02",
                "2021-09-03",
            )
        )
        assert not sequence.contains_duplicates()


class TestDateSequenceIntersect:
    @pytest.fixture(scope="class")
    def values(self) -> Tuple[str, ...]:
        return (
            "2021-09-01",
            "2021-09-02",
            "2021-09-03",
        )

    @pytest.fixture(scope="class")
    def sequence(self, values: Tuple[str, ...]) -> DateSequence:
        return DateSequence.from_string(values)

    def test_when_all_is_included_for_both(
        self,
        sequence: DateSequence,
        values: Tuple[str, ...],
    ):
        other = DateSequence.from_string(values)
        assert sequence.intersect(other) == sequence

    def test_when_all_of_one_is_included(
        self,
        sequence: DateSequence,
        values: Tuple[str, ...],
    ):
        other = DateSequence.from_string((*values, "2021-09-04"))
        assert sequence.intersect(other) == sequence
        assert other.intersect(sequence) == sequence

    def test_when_some_is_included_for_both(
        self,
        sequence: DateSequence,
        values: Tuple[str, ...],
    ):
        other = DateSequence.from_string((values[0], "2021-09-04"))
        result = sequence.intersect(other)
        expected = DateSequence.from_string((values[0],))
        assert result == expected

    def test_when_none_is_included_for_both(self, sequence: DateSequence):
        other = DateSequence.from_string(("2021-09-04",))
        result = sequence.intersect(other)
        expected = DateSequence([])
        assert result == expected

    def test_when_is_unordered(self, sequence: DateSequence):
        other = sequence[::-1]
        result = sequence.intersect(other)
        assert result == sequence


class TestDateSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> DateSequence:
        return DateSequence([])

    def test_from_string(self, sequence: DateSequence):
        assert DateSequence.from_string([]) == sequence

    def test_is_ascending(self, sequence: DateSequence):
        assert sequence.is_ascending()

    def test_contains_duplicates(self, sequence: DateSequence):
        assert not sequence.contains_duplicates()

    def test_intersect_when_both_empty(self, sequence: DateSequence):
        assert sequence.intersect(sequence) == sequence

    def test_intersect_when_one_empty(self, sequence: DateSequence):
        other = DateSequence.from_string(("2021-10-31",))
        assert sequence.intersect(other) == sequence
