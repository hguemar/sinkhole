""" Koji interaction
"""

import os.path

import koji
import six

from sinkhole.util import download_packages


def setup_kojiclient(profile):
    """Setup koji client session
    """
    opts = koji.read_config(profile)
    for key, value in six.iteritems(opts):
        opts[key] = os.path.expanduser(value) if isinstance(value, str) \
                    else value
    kojiclient = koji.ClientSession(opts['server'], opts=opts)
    # FIXME: who cares about authentication???
    # Moreover kerberos authentication can be an annoyance
    if opts['authtype'] == "ssl" or \
       (os.path.isfile(opts['cert']) and opts['authtype'] is None):
        kojiclient.ssl_login(opts['cert'], None, opts['serverca'])
    else:
        print('SKIP authentication')
    return kojiclient


class KojiDownloader(object):
    """ Download builds from koji
    """
    def __init__(self, profile, builds=None, arches=None):
        self.profile = profile
        self.koji = setup_kojiclient(self.profile)
        self._arches = arches
        self._builds = self.builds(builds)

    def builds(self, builds_):
        res = []
        for build in builds_:
            if "@latest" in build:
                b = build[:build.find("@")]
                pkgId = self.koji.getPackageID(b)
                info = self.koji.listBuilds(pkgId)
                if info:
                    res.append(info[0]['nvr'])
            else:
                res.append(build)
        return res

    @classmethod
    def build(cls, info):
        kd = None
        profile = info["profile"]
        kd = cls(profile)
        return kd

    def run(self):
        """ Execute downloads
        """
        urls = []
        pathinfo = koji.PathInfo(topdir=self.koji.opts['topurl'])
        for build in self._builds:
            try:
                info = self.koji.getBuild(build)
                rpms = self.koji.listRPMs(buildID=info['id'],
                                          arches=self._arches)
                fnames = [pathinfo.rpm(rpm) for rpm in rpms]
                urls += [pathinfo.build(info) + '/' + fname
                         for fname in fnames]
            except Exception:
                print('SKIPPED: build {} does not exists'.format(build))
        for url in urls:
            download_packages(url, ".")
