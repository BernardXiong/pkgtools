'''
    common.package Module

    License TBD

'''

import shutil
import glob
from os import path


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
    '''
        Directory class for interacting with Package files
    '''

    def __init__(self, filepath):
        self._path = filepath

    def copy_to(self, dest):
        '''
            Copy file from package to `dest`
        '''
        shutil.copy(self._path, dest)    

    def __repr__(self):
        return "<FileAccessor: %s>" % self._path

    def __get__(self, instance):
        return self._path

    def __set__(self, instance, val):
        raise AttributeError('Cannot set this file')

