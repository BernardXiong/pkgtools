# Module:   build
# Date:     14th March 2015
# Author:   James Mills, prologic at shortcircuit dot net dot au


from __future__ import print_function


import tarfile
from os import environ, sep
from functools import partial
from shutil import copy, rmtree
from mimetypes import guess_type

from argparse import ArgumentDefaultsHelpFormatter


from pathlib import Path
from progress.spinner import Spinner


from ..parsers import parse_pkgfile
from ..utils import download, execute, extract


def PackageType(v):
    p = Path(v).resolve()

    if p.name == "Pkgfile" and p.is_file():
        return p

    if p.is_dir() and p.joinpath("Pkgfile").is_file():
        return p.joinpath("Pkgfile")

    raise IOError(2, "No such file or directory: {}".format(repr(v)))


def prepare(args, conf):
    workdir = args.package.parent.joinpath("work")

    if workdir.is_dir():
        rmtree(str(workdir))

    workdir.mkdir()

    pkgdir = workdir.joinpath("pkg")
    srcdir = workdir.joinpath("src")

    pkgdir.mkdir()
    srcdir.mkdir()

    return pkgdir, srcdir, workdir


def download_sources(sources, workdir):
    filenames = []

    for source in sources:
        if "://" in source:
            filename = source.split("#", 1)[1] if "#" in source else None
            filename = download(source, filename, str(workdir.parent))
        else:
            filename = source

        filename = workdir.parent.joinpath(filename)
        filenames.append(filename)

    return filenames


def strip_leading(tarinfo, path=None):
    if path is not None:
        tarinfo.name = ".{}".format(tarinfo.name.replace(path, ""))

    return tarinfo


def main(args, conf):
    pkgdir, srcdir, workdir = prepare(args, conf)

    pkg = parse_pkgfile(args.package)

    filenames = []
    if args.download or args.download_only:
        filenames = download_sources(pkg["source"], workdir)

    if args.download_only:
        return

    for filename in filenames:
        filename = str(filename)
        type, encoding = guess_type(filename)
        if type in ("application/x-tar", "application/x-zip-compressed"):
            extract(filename, str(srcdir))
        else:
            copy(filename, str(srcdir))

    if args.extract_only:
        return

    env = {
        "SRC": str(srcdir),
        "PKG": str(pkgdir),
    }

    env.update(environ)

    output = execute(
        ["/bin/bash", "-c", "source Pkgfile && cd $SRC && build"],
        cwd=str(workdir.parent), env=env, stream=True
    )

    with workdir.parent.joinpath("build.log").open("wb") as f:
        spinner = Spinner("Building ... ")
        for c in output:
            f.write(c)
            spinner.next()
        spinner.finish()

    filename = "{}#{}-{}.tar.gz".format(pkg["name"], pkg["version"], pkg["release"])
    with tarfile.open(str(workdir.parent.joinpath(filename)), "w:gz") as f:
        f.add(str(pkgdir), filter=partial(strip_leading, path=str(pkgdir).lstrip(sep)))

    if not args.keep_work:
        rmtree(str(workdir))


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
