from typing import Tuple

import pytest

from portan.source.date import Date
from portan.source.date.sequence import DateSequence
from portan.source.dated.generic import Dated
from portan.source.dated.generic.sequence import DatedSequence


class TestDatedSequenceHasAscendingDates:
    def test_when_one(self):
        sequence = DatedSequence(
            [
                Dated(Date("2021-09-01"), 1),
            ]
        )
        assert sequence.has_ascending_dates()

    @pytest.mark.parametrize(
        "dates",
        [
            ("2021-09-01", "2021-09-02", "2021-09-03"),  # consecutive
            ("2021-09-01", "2021-09-02", "2021-09-02"),  # equal
            ("2021-09-01", "2021-09-03", "2021-09-04"),  # non-consecutive
        ],
    )
    @pytest.mark.parametrize(
        "values",
        [
            (1, 2, 3),  # ascending
            (3, 2, 1),  # descending
            (2, 1, 3),  # unsorted
        ],
    )
    def test_when_multiple_and_ascending(
        self,
        dates: Tuple[str, ...],
        values: Tuple[int, ...],
    ):
        sequence = DatedSequence(
            Dated(
                Date(date),
                value,
            )
            for date, value in zip(dates, values)
        )
        assert sequence.has_ascending_dates()

    @pytest.mark.parametrize(
        "dates",
        [
            ("2021-09-01", "2021-09-04", "2021-09-03"),  # unsorted
            ("2021-09-03", "2021-09-02", "2021-09-01"),  # descending
        ],
    )
    @pytest.mark.parametrize(
        "values",
        [
            (1, 2, 3),  # ascending
            (3, 2, 1),  # descending
            (2, 1, 3),  # unsorted
        ],
    )
    def test_when_multiple_and_not_ascending(
        self,
        dates: Tuple[str, ...],
        values: Tuple[int, ...],
    ):
        sequence = DatedSequence(
            Dated(
                Date(date),
                value,
            )
            for date, value in zip(dates, values)
        )
        assert not sequence.has_ascending_dates()


class TestDatedSequenceHasDuplicatedDates:
    def test_when_one(self):
        sequence = DatedSequence(
            [
                Dated(Date("2021-09-01"), 1),
            ]
        )
        assert not sequence.has_duplicated_dates()

    @pytest.mark.parametrize(
        "dates",
        [
            ("2021-09-01", "2021-09-02", "2021-09-01"),
            ("2021-09-01", "2021-09-01", "2021-09-01"),
        ],
    )
    @pytest.mark.parametrize(
        "values",
        [
            (1, 2, 3),  # no duplicates
            (1, 1, 1),  # duplicated
        ],
    )
    def test_when_multiple_and_has_duplicates(
        self,
        dates: Tuple[str, ...],
        values: Tuple[int, ...],
    ):
        sequence = DatedSequence(
            Dated(
                Date(date),
                value,
            )
            for date, value in zip(dates, values)
        )
        assert sequence.has_duplicated_dates()

    @pytest.mark.parametrize(
        "values",
        [
            (1, 2, 3),  # no duplicates
            (1, 1, 1),  # duplicated
        ],
    )
    def test_when_multiple_and_unique(
        self,
        values: Tuple[int, ...],
    ):
        dates = ("2021-09-01", "2021-09-02", "2021-09-03")
        sequence = DatedSequence(
            Dated(
                Date(date),
                value,
            )
            for date, value in zip(dates, values)
        )
        assert not sequence.has_duplicated_dates()


class TestDatedSequenceCompress:
    @pytest.fixture(scope="class")
    def sequence(self) -> DatedSequence:
        return DatedSequence(
            [
                Dated(Date("2021-10-31"), 1),
                Dated(Date("2021-11-01"), 2),
                Dated(Date("2021-11-03"), 2),
            ]
        )

    @pytest.mark.parametrize(
        "dates",
        [
            DateSequence([]),
            DateSequence.from_string(["0001-01-01"]),
        ],
    )
    def test_when_none_selected(
        self,
        sequence: DatedSequence,
        dates: DateSequence,
    ):
        result = sequence.compress(dates)
        expected = DatedSequence([])
        assert result == expected

    @pytest.mark.parametrize(
        "dates",
        [
            DateSequence.from_string(
                [
                    "2021-10-31",
                    "2021-11-03",
                ]
            ),
            DateSequence.from_string(
                [
                    "2021-10-31",
                    "2021-11-03",
                    "2021-11-04",
                ]
            ),
        ],
    )
    def test_when_some_selected(
        self,
        sequence: DatedSequence,
        dates: DateSequence,
    ):
        result = sequence.compress(dates)
        expected = DatedSequence(
            [value for value in sequence if value.date in dates]
        )
        assert result == expected

    def test_when_all_selected(self, sequence: DatedSequence):
        result = sequence.compress(sequence.dates)
        assert result == sequence

    def test_dates_order_is_irrelevant(self, sequence: DatedSequence):
        dates = sequence.dates[::-1]
        result = sequence.compress(dates)
        assert result == sequence


class TestDatedSequenceEmpty:
    @pytest.fixture(scope="class")
    def sequence(self) -> DatedSequence:
        return DatedSequence([])

    def test_dates(self, sequence: DatedSequence):
        assert sequence.dates == DateSequence([])

    def test_has_ascending_dates(self, sequence: DatedSequence):
        assert sequence.has_ascending_dates()

    def test_has_duplicated_dates(self, sequence: DatedSequence):
        assert not sequence.has_duplicated_dates()

    def test_compress_when_no_dates(self, sequence: DatedSequence):
        dates = DateSequence([])
        assert sequence.compress(dates) == sequence

    def test_compress_when_dates(self, sequence: DatedSequence):
        dates = DateSequence.from_string(["2021-10-31"])
        assert sequence.compress(dates) == sequence
