from six import add_move, MovedModule
add_move(MovedModule('mock', 'mock', 'unittest.mock'))

from six.moves import mock

from sinkhole.config import Config
from sinkhole.source import Noop, SourceBuilder


class TestNoop(object):
    def test_build(self):
        info = { "name": "sources.something",
                 "type": "foobar" }
        assert Noop.build(info) is None


class TestSourceBuilder(object):
    def test_build_empty(self):
        config = Config()
        config.sources = [{ "name": "sources.something",
                            "type": "foobar" }]
        sources = SourceBuilder.build()
        assert len(sources) == 0

    def test_build_non_empty(self):
        config = Config()
        config.sources = [{ "name": "sources.fedora",
                            "type": "repofile",
                            "repofile": "something.repo" }]
        sources = SourceBuilder.build()
        assert len(sources) == 1
