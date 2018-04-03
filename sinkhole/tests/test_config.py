"""Tests for sinkhole.config
"""
from sinkhole.config import Config

from six import StringIO


class TestConfig(object):
    """Tests for Config class
    """
    def test_shared_state(self):
        """Check that state is shared across instances of Config
        """
        config1 = Config()
        config1.workers = 4
        config1.output_dir = "/tmp/some_dir"
        config2 = Config()
        assert config1.workers == config2.workers == 4
        assert config1.output_dir == config2.output_dir == "/tmp/some_dir"

    def test_read_config(self):
        """Check that configuration file are properly parsed
        """
        data = StringIO("""[main]
workers = 8
output_dir = output/
releasever = 28
basearch = x86_64

[sources.fedora]
type=repofile
repofile=sources/fedora.repo
constraints=sources/fedora_constraints
""")
        config = Config.read_config(data)
        assert config.workers == 8
        assert config.output_dir == "output/"
        assert config.default_substitutions["releasever"] == "28"
        assert config.default_substitutions["basearch"] == "x86_64"
