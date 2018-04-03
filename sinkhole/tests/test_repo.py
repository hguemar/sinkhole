from sinkhole.repo import RepositoryFile

import pytest
import six
if six.PY3:
    import unittest.mock as mock
else:
    import mock


class TestRepositoryFile(object):
    def test_parse_repofile(self):
        data = """[hguemar-rdo-packager]
name=Copr repo for rdo-packager owned by hguemar
baseurl=https://copr-be.cloud.fedoraproject.org/results/hguemar/rdo-packager/fedora-27-x86_64/
type=rpm-md
skip_if_unavailable=True
gpgcheck=1
gpgkey=https://copr-be.cloud.fedoraproject.org/results/hguemar/rdo-packager/pubkey.gpg
repo_gpgcheck=0
enabled=1
enabled_metadata=1"""

        m = mock.mock_open(read_data=data)
        with mock.patch("os.path.isfile", return_value=True):
            with mock.patch("__main__.open", m, create=True):
                r = RepositoryFile(None, "something.repo")
                assert r.repofile == "something.repo"
                repos = r.get_repos()
                assert len(repos) == 1

    def test_raise_error_non_existing_config(self):
        repofn = "toto.conf"
        with pytest.raises(IOError,
                           message="File {:s} does not exist".format(repofn)):
            RepositoryFile(None, repofn)
