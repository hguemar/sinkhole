from sinkhole.repo import RepositoryFile

from six import add_move, MovedModule
add_move(MovedModule('mock', 'mock', 'unittest.mock'))

from six.moves import mock


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
        assert True
        
