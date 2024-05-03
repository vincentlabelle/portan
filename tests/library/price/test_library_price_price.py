from math import log

import pytest

from portan.library.price import Price
from portan.library.rate import Rate


class TestPriceGrowth:
    def test_when_ratio_is_normal(self):
        begin, end = Price(2.0), Price(0.1)
        result = end.growth(begin)
        expected = Rate(log(float(end) / float(begin)))
        assert result == expected

    def test_when_ratio_is_too_big(self):
        begin, end = Price(1e-309), Price(1.0)
        with pytest.raises(ValueError, match="value must be finite"):
            end.growth(begin)

    def test_when_ratio_is_too_small(self):
        begin, end = Price(1e50), Price(1e-320)
        with pytest.raises(ValueError, match="math domain"):
            end.growth(begin)
