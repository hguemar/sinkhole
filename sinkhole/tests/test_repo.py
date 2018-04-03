"""Tests for sinkhole.repo module
"""
from sinkhole.repo import RepositoryFile

import dnf
import pytest


class TestRepositoryFile(object):
    """Tests for RepositoryFile class
    """
    def test_parse_repofile(self):
        """Test RepositoryFile .repo file parsing
        """
        data = """
[hguemar-rdo-packager]
name=Copr repo for rdo-packager owned by hguemar
baseurl=https://copr-be.cloud.fedoraproject.org/results/hguemar/rdo-packager/fedora-27-x86_64/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://copr-be.cloud.fedoraproject.org/results/hguemar/rdo-packager/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1"""
        base = dnf.Base()
        conf = base.conf
        repofile = RepositoryFile(conf, data)
        repos = repofile.get_repos()
        assert len(repos) == 1

    def test_raise_error_non_existing_config(self):
        """Test if RepositoryFile fails when provided
        non existing .repo file
        """
        repofn = "toto.conf"
        base = dnf.Base()
        conf = base.conf
        with pytest.raises(IOError,
                           message="File {:s} does not exist".format(repofn)):
            RepositoryFile(conf, repofn)
