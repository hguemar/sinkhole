from collections import defaultdict

from sinkhole.config import Config
from sinkhole.repo import Reposync


class Noop(object):
    """ Default provider for unrecognized source
    """
    @classmethod
    def build(cls, info):
        """ Build source provider
        """
        print("Unrecognized source {} (type: {})".format(info["name"],
                                                         info["type"]))
        return None


SOURCES = {"repofile": Reposync}
SOURCES = defaultdict(lambda: Noop, SOURCES)


class SourceBuilder(object):
    """ Build a source from config
    """
    @staticmethod
    def build():
        """ Build all sources
        """
        config = Config()
        sources = []
        for info in config.sources:
            typ = info["type"]
            source = SOURCES[typ].build(info)
            if source:
                sources.append(source)
        return sources
