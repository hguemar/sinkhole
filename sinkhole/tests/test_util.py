from sinkhole.util import filter_pkgs


class FakeRPM(object):
    def __init__(self, name, source_name):
        self.name = name
        self.source_name = source_name

    def __hash__(self):
        return hash((self.name, self.source_name))
    
    def __eq__(self, other):
        return self.name == other.name and \
            self.source_name == other.source_name
        

class TestFilterPkgs(object):
    def test_filter_pkgs_one(self):
        pkgs = { FakeRPM("python2-requests-2.18.4-1.fc27.noarch.rpm",
                         "python-requests-2.18.4-1.fc27.src.rpm")
             }                         
        patterns = ["python-requests.*"]
        res = filter_pkgs(pkgs, patterns)
        assert res == pkgs
             

    def test_filter_pkgs_one(self):
        pkgs_old = { FakeRPM("python2-requests-2.18.4-1.fc27.noarch.rpm",
                             "python-requests-2.18.4-1.fc27.src.rpm")
             }
        pkgs = pkgs_old | { FakeRPM("grin-1.2.1-15.fc27.noarch.rpm",
                                    "grin-1.2.1-15.fc27.src.rpm") }
        patterns = ["python-requests.*"]
        res = filter_pkgs(pkgs, patterns)
        assert res == pkgs_old
