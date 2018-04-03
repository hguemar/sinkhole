""" RPM repositories management
"""

from functools import partial
from multiprocessing import Pool
import os

import dnf
from dnf.conf.parser import substitute
import six
from six.moves import configparser
import yaml

from sinkhole.config import Config
from sinkhole.util import (download_packages, filter_pkgs)


class RepositoryFile(object):
    """ RepositoryFile parses a .repo file
    """
    def __init__(self, conf, repofn):
        self.repofile = repofn
        self.repos = []
        self._parse_repofile(repofn, conf)

    def _parse_repofile(self, repofn, conf):
        if not os.path.isfile(repofn):
            raise IOError("File {:s} does not exists".format(repofn))

        config = configparser.ConfigParser()
        config.read(repofn)

        for section in config.sections():
            repo = dnf.repo.Repo(section, conf)
            for key, value in six.iteritems(config[section]):
                if key in ["name", "baseurl", "enabled",
                           "gpgkey", "gpgcheck"]:
                    setattr(repo, key, value)
                elif key == "metalink":
                    setattr(repo, key, substitute(value, conf.substitutions))
            self.repos.append(repo)

    def get_repos(self):
        """ Returns a list of repositories from .repo file

        Returns:
            list: list of repositories
        """
        return self.repos


class Reposync(object):
    """ Reposync allows to sync repositories with packages filtering
    Repositories to sync are specified by feeding this class with your classic
    .repo files.
    """
    def __init__(self, repofns=[],
                 include_pkgs=None, exclude_pkgs=None):
        self.include_pkgs = include_pkgs
        self.exclude_pkgs = exclude_pkgs
        self.repofns = repofns
        self.base = dnf.Base()
        self.conf = self.base.conf
        config = Config()
        self.conf.substitutions['releasever'] = \
            config.default_substitutions["releasever"]
        self.conf.substitutions['basearch'] = \
            config.default_substitutions["basearch"]
        self.conf.cachedir = Config().output_dir
        self.repos = self.base.repos

    @property
    def substitutions(self):
        """ Return yum/dnf substitutions dict
        """
        return self.conf.substitutions

    @classmethod
    def build(cls, info):
        r, include_pkgs, exclude_pkgs = None, None, None
        repofile = info["repofile"]
        if "constraints" in info:
            constraints_file = info["constraints"]
            with open(constraints_file, "r") as f:
                constraints = yaml.load(f, Loader=yaml.Loader)
                include_pkgs = constraints["includes"]
                exclude_pkgs = constraints["excludes"]

        r = cls([repofile],
                include_pkgs=include_pkgs,
                exclude_pkgs=exclude_pkgs)

        for sub in ["releasever", "basearch"]:
            if sub in info:
                r.substitutions[sub] = info[sub]
        return r

    def run(self):
        """ Do the repo syncing
        """
        self._setup_repos()
        self.base.fill_sack()
        available_pkgs = self.base.sack.query().available().run()
        download_pkgs = self._filter_download_pkgs(available_pkgs)
        #
        # sinkhole --repofile fedora.repo --destdir tmp2
        # 23.27s user 2.14s system 1% cpu 28:19.24 total
        download_pkgs = [pkg.remote_location() for pkg in download_pkgs]

        config = Config()
        with Pool(config.workers) as pool:
            pool.map(partial(download_packages,
                             destdir=config.output_dir),
                     download_pkgs)
        # 3161
        # sinkhole --repofile fedora.repo --destdir tmp2
        # 699.75s user 195.08s system 14% cpu 1:41:17.52 total
        # self.base.download_packages(download_pkgs,
        #                             MultiFileProgressMeter(fo=sys.stdout))

    def _setup_repos(self):
        for repofn in self.repofns:
            repofile = RepositoryFile(self.conf, repofn)
            repositories = repofile.get_repos()
            for repository in repositories:
                self.repos.add(repository)

    def _filter_download_pkgs(self, pkgs):
        """ Private method that returns a list of packages to download

        Args:
            pkgs (list): packages to filter

        Returns:
            list: packages to download
        """
        included = set(pkgs) if not self.include_pkgs else \
            filter_pkgs(pkgs, self.include_pkgs)
        excluded = set() if not self.exclude_pkgs else \
            filter_pkgs(pkgs, self.exclude_pkgs)
        pkgs = list(included - excluded)
        return pkgs
