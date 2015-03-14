'''
    Unit tests for pkg.common.package module
'''

import unittest
from pkg.common.package import Package


class TestPackage(unittest.TestCase):
    '''
        Test cases for the pkg.common.Package class
    '''

    def setUp(self):
        self.filename = 'test/resources/test_package#0.1.1.pkg.tar.gz'

    def test_get_package(self):
        '''
            Test we get our expected result back from the
            
        '''

        pkg = Package.from_file(self.filename)

        assert pkg.name is "test_package"
        assert pkg.version is "0.1.1"
        assert isinstance(pkg.files, list)
