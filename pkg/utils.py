# Module:   utils
# Date:     14th March 2015
# Author:   James Mills, prologic at shortcircuit dot net dot au

"""Utilities

Utility functions
"""


from __future__ import print_function

import sys
from bz2 import BZ2File
from gzip import GzipFile
from tarfile import TarFile
from zipfile import ZipFile
from os import getcwd, path
from urlparse import urlsplit
from hashlib import sha256 as sha
from traceback import format_exception
from subprocess import Popen, PIPE, STDOUT


from requests import get
from progress.bar import Bar as ProgressBar


def log(msg):
    print(msg, file=sys.stderr)


def verify(filename, checksum):
    return shasum(filename) == checksum


def shasum(filename, chunksize=4069):
    """Return a SHA checksum of the given file"""

    hash = sha()

    with open(filename, "r") as f:
        buffer = f.read(chunksize)
        while buffer:
            hash.update(buffer)
            buffer = f.read(chunksize)

    return hash.hexdigest()


def shasums(filenames):
    """Return a lis of SHA checksums of all files specified in the list filenames"""

    return ((filename, shasum(filename)) for filename in filenames)


def read_shasum(filename):
    with open(filename, "r") as f:
        for line in f:
            filename, checksum = line.strip().split("\t")
            yield filename, checksum


def write_shasum(checksums, filename):
    with open(filename, "w") as f:
        f.write(
            "\n".join(
                ("{}\t{}".format(filename, checksum) for filename, checksum in checksums)
            )
        )


def extract(archive, output=None):
    output = output or getcwd()

    if any(archive.endswith(x) for x in [".tar.gz", ".tar.bz2"]):
        with TarFile(archive, "r:{0:s}".format(path.splitext(archive)[1][1:])) as f:
            f.extractall(output, [x for x in f.getmembers() if not path.exists(x)])
    elif archive.endswith(".zip"):
        with ZipFile(archive) as f:
            f.extractall(output, [x for x in f.namelist() if not path.exists(x)])
    elif archive.endswith(".gz"):
        outfile = path.join(output, path.splitext(archive)[0])
        if not path.exists(outfile):
            with GzipFile(archive, "rb") as f:
                with open(outfile, "wb") as of:
                    of.write(f.read())
    elif archive.endswith(".bz2"):
        outfile = path.join(output, path.splitext(archive)[0])
        if not path.exists(outfile):
            with BZ2File(archive, "rb") as f:
                with open(outfile, "wb") as of:
                    of.write(f.read())


def url2basename(url):
    return path.basename(urlsplit(url)[2])


def download(url, filename=None, pwd=None, bs=8192):
    r = get(url, stream=True)

    if not filename and "Content-Disposition" in r.headers:
        filename = r.headers["Content-Disposition"].split("filename=")[1]
        filename = filename.replace("\"", "").replace("'", "")
    else:
        filename = url2basename(r.url)

    if pwd is not None and not path.isabs(filename):
        filename = path.join(pwd, filename)

    cl = int(r.headers.get("Content-Length", "0"))

    print("Downloading {0:s} Bytes: {1:d} ...".format(path.basename(filename), cl))
    with open(filename, "wb") as f:
        bar = ProgressBar(max=cl)
        for block in r.iter_content(bs):
            f.write(block)
            bar.next(bs)
        bar.finish()
    print()


def format_error():
    etype, evalue, tb = sys.exc_info()
    traceback = "\r\n".join(
        ("i{}".format(line) for line in format_exception(etype, evalue, tb))
    )
    return "3{}{}\terror.host\t0\r\n{}".format(etype.__name__, evalue, traceback)


def execute(args, **kwargs):
    kwargs.update(stderr=STDOUT, stdout=PIPE)

    try:
        p = Popen(args, **kwargs)
        stdout, _ = p.communicate()
        return stdout
    except:
        return format_error()
