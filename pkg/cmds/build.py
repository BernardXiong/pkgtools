# Module:   build
# Date:     14th March 2015
# Author:   James Mills, prologic at shortcircuit dot net dot au


from __future__ import print_function

from os import getcwd
from shutil import copy, rmtree
from argparse import ArgumentDefaultsHelpFormatter


from pathlib import Path


from ..parsers import parse_pkgfile
from ..utils import download, execute


def PackageType(v):
    p = Path(v).absolute()

    if p.name == "Pkgfile" and p.is_file():
        return p

    if p.is_dir() and p.joinpath("Pkgfile").is_file():
        return p.joinpath("Pkgfile")

    raise IOError(2, "No such file or directory: {}".format(repr(v)))


def prepare(args, conf):
    p = Path.cwd()

    workdir = p.joinpath("work")
    if workdir.is_dir():
        rmtree(str(workdir))

    workdir.mkdir()

    pkgdir = workdir.joinpath("pkg")
    srcdir = workdir.joinpath("src")

    pkgdir.mkdir()
    srcdir.mkdir()

    return {"PKG": str(pkgdir), "SRC": str(srcdir)}


def download_sources(sources, srcdir):
    for source in sources:
        if "://" in source:
            filename = source.split("#", 1)[1] if "#" in source else None
            download(source, filename, srcdir)
        else:
            copy(source, srcdir)


def main(args, conf):
    env = prepare(args, conf)

    data = parse_pkgfile(args.package)

    if args.download or args.download_only:
        download_sources(data["source"], env["SRC"])


def init(subparsers):
    parser = subparsers.add_parser(
        "build",
        help="Build package",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.set_defaults(func=main)

    parser.add_argument(
        "-d", "--download", dest="download",
        default=False, action="store_true",
        help="Download missing source file(s)"
    )

    parser.add_argument(
        "-do", "--download-only", dest="download_only",
        default=False, action="store_true",
        help="Do not build, only download missing source file(s)"
    )

    parser.add_argument(
        "-eo", "--extract-only", dest="extract_only",
        default=False, action="store_true",
        help="Do not build, only extract source file(s)"
    )

    parser.add_argument(
        "-utd", "--up-to-date", dest="up_to_date",
        default=False, action="store_true",
        help="Do not build, only check if package is up to date"
    )

    parser.add_argument(
        "-uf", "--update-footprint", dest="update_footprint",
        default=False, action="store_true",
        help="Update footprint using result from last build"
    )

    parser.add_argument(
        "-if", "--ignore-footprint", dest="ignore_footprint",
        default=False, action="store_true",
        help="Build package without checking footprint"
    )

    parser.add_argument(
        "-in", "--ignore-new", dest="ignore_new",
        default=False, action="store_true",
        help="Build package, ignore new files in a footprint missmatch"
    )

    parser.add_argument(
        "-uc", "--update-checksum", dest="update_checksum",
        default=False, action="store_true",
        help="Update checksum"
    )

    parser.add_argument(
        "-ic", "--ignore-checksum", dest="ignore_checksum",
        default=False, action="store_true",
        help="Build package without checking checksum"
    )

    parser.add_argument(
        "-cc", "--check-checksum", dest="check_checksum",
        default=False, action="store_true",
        help="Do not build, only check checksum"
    )

    parser.add_argument(
        "-ns", "--no-strip", dest="no_strip",
        default=False, action="store_true",
        help="Do not strip executable binaries or libraries"
    )

    parser.add_argument(
        "-f", "--force", dest="force",
        default=False, action="store_true",
        help="Build package even if it appears to be up to date"
    )

    parser.add_argument(
        "-c", "--clean", dest="clean",
        default=False, action="store_true",
        help="Remove package and downloaded files"
    )

    parser.add_argument(
        "-kw", "--keep-work", dest="keep_work",
        default=False, action="store_true",
        help="Keep temporary working directory"
    )

    parser.add_argument(
        "package",
        metavar="PACKAGE", type=PackageType,
        help="Package to build"
    )
