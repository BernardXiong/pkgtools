# Module:   build
# Date:     14th March 2015
# Author:   James Mills, prologic at shortcircuit dot net dot au


from __future__ import print_function

from argparse import ArgumentDefaultsHelpFormatter


def main(args, conf):
    print("Build ...")
    print("args:", repr(args))
    print("conf:", repr(conf))


def init(subparsers):
    parser = subparsers.add_parser(
        "build",
        help="Build package",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.set_defaults(func=main)

    parser.add_argument(
        "-d", "--download", dest="download",
        default=False, type=bool,
        help="Download missing source file(s)"
    )

    parser.add_argument(
        "-do", "--download-only", dest="download_only",
        default=False, type=bool,
        help="Do not build, only download missing source file(s)"
    )

    parser.add_argument(
        "-eo", "--extract-only", dest="extract_only",
        default=False, type=bool,
        help="Do not build, only extract source file(s)"
    )

    parser.add_argument(
        "-utd", "--up-to-date", dest="up_to_date",
        default=False, type=bool,
        help="Do not build, only check if package is up to date"
    )

    parser.add_argument(
        "-uf", "--update-footprint", dest="update_footprint",
        default=False, type=bool,
        help="Update footprint using result from last build"
    )

    parser.add_argument(
        "-if", "--ignore-footprint", dest="ignore_footprint",
        default=False, type=bool,
        help="Build package without checking footprint"
    )

    parser.add_argument(
        "-in", "--ignore-new", dest="ignore_new",
        default=False, type=bool,
        help="Build package, ignore new files in a footprint missmatch"
    )

    parser.add_argument(
        "-uc", "--update-checksum", dest="update_checksum",
        default=False, type=bool,
        help="Update checksum"
    )

    parser.add_argument(
        "-ic", "--ignore-checksum", dest="ignore_checksum",
        default=False, type=bool,
        help="Build package without checking checksum"
    )

    parser.add_argument(
        "-cc", "--check-checksum", dest="check_checksum",
        default=False, type=bool,
        help="Do not build, only check checksum"
    )

    parser.add_argument(
        "-ns", "--no-strip", dest="no_strip",
        default=False, type=bool,
        help="Do not strip executable binaries or libraries"
    )

    parser.add_argument(
        "-f", "--force", dest="force",
        default=False, type=bool,
        help="Build package even if it appears to be up to date"
    )

    parser.add_argument(
        "-c", "--clean", dest="clean",
        default=False, type=bool,
        help="Remove package and downloaded files"
    )

    parser.add_argument(
        "-kw", "--keep-work", dest="keep_work",
        default=False, type=bool,
        help="Keep temporary working directory"
    )
