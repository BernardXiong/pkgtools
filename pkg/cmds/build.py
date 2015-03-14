# Module:   build
# Date:     14th March 2015
# Author:   James Mills, prologic at shortcircuit dot net dot au


from __future__ import print_function


def main(args):
    print("Build ...")
    print("args:", repr(args))


def init(subparsers):
    parser = subparsers.add_parser(
        "build",
        help="Build package"
    )
    parser.set_defaults(func=main)

    parser.add_argument(
        "-d", "--download", dest="download",
        default=False, type=bool,
        help="Download missing source file(s)"
    )
