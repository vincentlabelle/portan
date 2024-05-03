import pytest

from portan.api.source import Source


@pytest.fixture(scope="module", params=[Source.YAHOO])
def source(request) -> Source:
    return request.param


class TestSourceStringRepresentation:
    def test_str(self, source: Source):
        assert str(source) == source.name

    def test_repr(self, source: Source):
        assert repr(source) == f"<{source.__class__.__name__}({source})>"
