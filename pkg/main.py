#!/usr/bin/env python
# Module:   main
# Date:     14th March 2015
# Author:   James Mills, prologic at shortcircuit dot net dot au


from __future__ import print_function

from os.path import dirname
from pkgutil import iter_modules
from importlib import import_module
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType


from yaml import load as load_yaml


from . import cmds
from . import __doc__, __version__


def parse_args():
    parser = ArgumentParser(
        description=__doc__,
        version=__version__,
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-c", "--config", dest="config",
        default="/etc/pkg.yml", type=FileType("r"),
        help="Specify alternative configuration file"
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

    conf = load_yaml(args.config)

    args.func(args, conf)


if __name__ == "__main__":
    main()
