"""Tests for sinkhole.source
"""
from sinkhole.config import Config
from sinkhole.source import Noop, SourceBuilder


class TestNoop(object):
    """Tests for Noop source provider
    """
    def test_build_returns_none(self):
        """Check that Noop.build returns None
        """
        info = {"name": "sources.something",
                "type": "foobar"}
        assert Noop.build(info) is None


class TestSourceBuilder(object):
    """Tests for SourceBuilder factory
    """
    def test_build_empty(self):
        """Check that unrecognized source providers are
        correctly processed
        """
        config = Config()
        config.sources = [{"name": "sources.something",
                           "type": "foobar"}]
        sources = SourceBuilder.build()
        assert len(sources) == 0

    def test_build_non_empty(self):
        """Check that RepoSync provider is correctly built
        """
        config = Config()
        config.sources = [{"name": "sources.fedora",
                           "type": "repofile",
                           "repofile": "something.repo"}]
        sources = SourceBuilder.build()
        assert len(sources) == 1
