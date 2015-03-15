'''
    Module:   pkg.install
    Date:     15th March 2015
    Author:   Nathan Schmidt
'''

from pkg.common.database import Database
from pkg.common.package import Package


def main(args, conf):
    '''
        Each runnable cli module should export a `main`
        function. This function will be called with the
        arguments passed to the entry point.
    '''

    print "Args", args
    print "Conf", conf



