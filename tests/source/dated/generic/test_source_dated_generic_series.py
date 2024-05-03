import pytest

from portan.source.date import Date
from portan.source.dated.generic import Dated
from portan.source.dated.generic.series import DatedSeries


class TestDatedSeriesInvariants:
    def test_when_unsorted(self):
        with pytest.raises(ValueError, match="values must be sorted"):
            DatedSeries(
                (
                    Dated(Date("2021-09-01"), 1),
                    Dated(Date("2021-09-04"), 2),
                    Dated(Date("2021-09-03"), 3),
                )
            )

    def test_when_non_unique(self):
        with pytest.raises(ValueError, match="values.+with the same date"):
            DatedSeries(
                (
                    Dated(Date("2021-09-01"), 1),
                    Dated(Date("2021-09-02"), 2),
                    Dated(Date("2021-09-02"), 3),
                )
            )

    def test_when_unique_and_sorted(self):
        DatedSeries(
            (
                Dated(Date("2021-09-01"), 1),
                Dated(Date("2021-09-02"), 0),
                Dated(Date("2021-09-03"), 1),
            )
        )  # does not raise


class TestDatedSeriesAlternativeConstructors:
    def test_from_unsorted_when_sorted(self):
        values = (
            Dated(Date("2021-09-01"), 1),
            Dated(Date("2021-09-02"), 0),
            Dated(Date("2021-09-03"), 1),
        )
        result = DatedSeries.from_unsorted(values)
        expected = DatedSeries(values)
        assert result == expected

    def test_from_unsorted_when_unsorted(self):
        values = (
            Dated(Date("2021-09-01"), 1),
            Dated(Date("2021-09-04"), 2),
            Dated(Date("2021-09-03"), 3),
        )
        result = DatedSeries.from_unsorted(values)
        expected = DatedSeries(sorted(values, key=lambda x: x.date))
        assert result == expected

    def test_from_unsorted_when_non_unique(self):
        with pytest.raises(ValueError, match="values.+with the same date"):
            DatedSeries.from_unsorted(
                (
                    Dated(Date("2021-09-01"), 1),
                    Dated(Date("2021-09-01"), 2),
                )
            )


class TestDatedSeriesEmpty:
    @pytest.fixture(scope="class")
    def series(self) -> DatedSeries:
        return DatedSeries([])

    def test_from_unsorted(self, series: DatedSeries):
        assert DatedSeries.from_unsorted([]) == series
