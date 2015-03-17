'''
    Module:   pkg.install
    Date:     15th March 2015
    Author:   Nathan Schmidt
'''

from pkg.common.database import Database
from pkg.common.package import Package
from pkg.utils import extract

from argparse import ArgumentDefaultsHelpFormatter



def is_uri(argpgk):
    '''
        Place holder
    '''
    return False

def uri_download(argpkg):
    '''
        Returns a tar filepath from a download
    '''
    return "filepath"

def init(subparsers):
    '''
        Setup the cli options for install
    '''
    parser = subparsers.add_parser(
        "install",
        help="Install package"
    )

    parser.set_defaults(func=main)

    parser.add_argument(
        "-d", "--dry-run", dest="dry_run",
        default=False, action="store_true",
        help="Do not complete install, only output what would happen."
    )

    parser.add_argument(
        "package", metavar="PACKAGE",
        type=str, help="Install package from file or by name"
    )


def main(args, conf):
    '''
        Install
    '''

    print "Args", args
    print "Conf", conf

    # Assuming we always end up with a 'tar'
    # like file at the end
    tarpath = args.package

    # At first instance just intall a damn tar file, we can 
    # worry about the rest of it later

    if is_uri(args.package):
        tarpath = uri_download(args.package)

    # Extract Tar to a tmp location
    tmpfile = TempFile('w', dir=path.dirname(self.filename), delete=False)
    extract(tarpath, tmpfile)

    package = Package(tmpfile.name)

    # Update database
    # Copy files to their destinations
        # If any copies fail - undo
        # - Should package copy check permissions before attempting to copy?
        # - Should we check all permissions before starting the copy?
        # If database commit fails - undo
