""" Config file
"""

from six.moves import configparser


class Config(object):
    """Configuration object

    Uses Borg pattern to keep shared state across instances
    """
    _shared_state = {
        "_workers": 4,
        "_output_dir": "tmp/",
        "_sources": [],
        "_default_substitutions": {}

    }

    def __init__(self):
        self.__dict__ = self._shared_state

    @property
    def workers(self):
        return self._workers

    @workers.setter
    def workers(self, workers):
        self._workers = workers

    @property
    def output_dir(self):
        return self._output_dir

    @output_dir.setter
    def output_dir(self, output_dir):
        self._output_dir = output_dir

    @property
    def sources(self):
        return self._sources

    @sources.setter
    def sources(self, sources):
        self._sources = sources

    @property
    def default_substitutions(self):
        return self._default_substitutions

    @classmethod
    def read_config(cls, fn):
        """Read config file

        Args:
          fn: either filename or file-like object pointing to configuration

        Returns:
            Config: Config object
        """
        config = cls()
        cf = configparser.ConfigParser()
        fp = fn if hasattr(fn, "readline") else open(fn, "r")
        cf.readfp(fp)

        workers = cf.getint("main", "workers")
        output_dir = cf.get("main", "output_dir")
        config.workers = workers
        config.output_dir = output_dir
        config.default_substitutions["releasever"] = \
            cf.get("main", "releasever")
        config.default_substitutions["basearch"] = cf.get("main", "basearch")
        sources = [section for section in cf.sections()
                   if section.startswith("sources")]
        config.sources = []
        for source in sources:
            s = {k: cf.get(source, k) for k in cf.options(source)}
            s["name"] = source
            config.sources.append(s)
        return config
