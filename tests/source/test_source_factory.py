import pytest

from portan.source.factory import PriceSourceFactory
from portan.source.source.multiple import MultipleSource
from portan.source.yahoo import Yahoo


@pytest.fixture(scope="module")
def factory() -> PriceSourceFactory:
    return PriceSourceFactory()


class TestPriceSourceFactory:
    def test_when_yahoo(self, factory: PriceSourceFactory):
        result = factory.get("yahoo")
        assert isinstance(result.single, Yahoo)
        assert isinstance(result.multiple, MultipleSource)
        assert isinstance(result.multiple.single, Yahoo)

    def test_when_unknown(self, factory: PriceSourceFactory):
        with pytest.raises(ValueError, match="unknown source"):
            factory.get("batman")
