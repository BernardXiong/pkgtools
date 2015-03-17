'''
    common.package Module

    License TBD

'''

from os import path
import glob


# Constants
PKG_VERSION_SEP = "#"


class Package(object):
    '''
        Package Class

        Class methods to create a package instance from a file
        or directory.

        The plan should be to actually abstract the essential CRUX pkg
        parts of this class to a CRUX sub-class.  However, for now this
        will do.
    '''

    def __init__(self, dirpath):
        '''
            From dirpath
        '''
        self.dirpath = path.abspath(dirpath)

        basename = path.basename(dirpath)
        name, version = basename.split(PKG_VERSION_SEP)

        self.name = name
        self.version = version
        self.files = [FileAccessor(f) for f in glob.glob(path.join(self.dirpath, "*"))]

class FileAccessor(object):
    pass
