""" Config file management
"""

import six
from six.moves import configparser

if six.PY2:
    configparser.ConfigParser.read_file = \
        lambda self, x: configparser.ConfigParser.readfp(self, x)


class Config(object):
    """Configuration object

    Uses Borg pattern to keep shared state across instances
    """
    _shared_state = {
        "_workers": 4,
        "_output_dir": "tmp/",
        "_sources": [],
        "_default_substitutions": {},
        "_masher_opts": "",
        "_masher_workers": 1
    }

    def __init__(self):
        self.__dict__ = self._shared_state

    @property
    def workers(self):
        """Property: workers (Number of processes)
        """
        return self._workers

    @workers.setter
    def workers(self, workers):
        """Property(setter): workers (Number of processes)
        """
        self._workers = workers

    @property
    def output_dir(self):
        """Property: output_dir (Output directory)
        """
        return self._output_dir

    @output_dir.setter
    def output_dir(self, output_dir):
        """Property(setter): output_dir (Output directory)
        """
        self._output_dir = output_dir

    @property
    def sources(self):
        """Property: sources (sources providers)
        """
        return self._sources

    @sources.setter
    def sources(self, sources):
        """Property(setter): sources (sources providers)
        """
        self._sources = sources

    @property
    def default_substitutions(self):
        """Property: default_substitutions (Yum repo file substitutions)
        """
        return self._default_substitutions

    @property
    def masher_opts(self):
        """Property: masher_opts (createrepo options)
        """
        return self._masher_opts

    @masher_opts.setter
    def masher_opts(self, opts):
        """Property(setter): masher_opts (createrepo options)
        """
        self._masher_opts = opts

    @property
    def masher_workers(self):
        """Property: masher_workers (createrepo workers)
        """
        return self._masher_workers

    @masher_workers.setter
    def masher_workers(self, nb):
        """Property(setter): masher_workers (createrepo workers)
        """
        self._masher_workers = int(nb)

    @classmethod
    def read_config(cls, fname):
        """Read config file

        Args:
          fname: either filename or file-like object pointing to configuration

        Returns:
            Config: Config object
        """
        config = cls()
        conf = configparser.ConfigParser()
        fobj = fname if hasattr(fname, "readline") else open(fname, "r")
        conf.read_file(fobj)

        workers = conf.getint("main", "workers")
        output_dir = conf.get("main", "output_dir")
        config.workers = workers
        config.output_dir = output_dir
        config.default_substitutions["releasever"] = \
            conf.get("main", "releasever")
        config.default_substitutions["basearch"] = conf.get("main", "basearch")

        try:
            config.masher_opts = conf.get("masher", "opts")
            config.masher_workers = conf.getint("masher", "workers")
        except configparser.NoSectionError:
            print("Warning: Masher has not been configured")
        except configparser.NoOptionError:
            print("Warning: Masher options has not been defined."
                  "Using default parameters")

        sources = [section for section in conf.sections()
                   if section.startswith("sources")]
        config.sources = []
        for source in sources:
            provider = {k: conf.get(source, k) for k in conf.options(source)}
            provider["name"] = source
            config.sources.append(provider)
        return config
