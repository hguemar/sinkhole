from sinkhole.config import Config

from six import StringIO


class TestConfig(object):
    def test_shared_state(self):
        configA = Config()
        configA.workers = 4
        configA.output_dir = "/tmp/some_dir"
        configB = Config()
        assert configA.workers == configB.workers == 4
        assert configA.output_dir == configB.output_dir == "/tmp/some_dir"


    def test_read_config(self):
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
        c = Config.read_config(data)
        assert c.workers == 8
        assert c.output_dir == "output/"
        assert c.default_substitutions["releasever"] == "28"
        assert c.default_substitutions["basearch"] == "x86_64"
        
