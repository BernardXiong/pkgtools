#!/usr/bin/env python
# Module:   main
# Date:     14th March 2015
# Author:   James Mills, prologic at shortcircuit dot net dot au


from __future__ import print_function

from os.path import dirname
from pkgutil import iter_modules
from importlib import import_module
from argparse import ArgumentParser


from . import cmds
from . import __doc__, __version__


def parse_args():
    parser = ArgumentParser(
        description=__doc__,
        version=__version__,
    )

    parser.add_argument(
        "-q", "--quiet", dest="quiet",
        default=False, type=bool,
        help="Enable quiet mode",
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        description="Available Commands",
        help="Description"
    )

    for _, name, _ in iter_modules([dirname(cmds.__file__)]):
        mod = import_module(".{}".format(name), cmds.__name__)
        mod.init(subparsers)

    return parser.parse_args()


def main():
    args = parse_args()

    args.func(args)


if __name__ == "__main__":
    main()
