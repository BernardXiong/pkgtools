# Module:   utils
# Date:     14th March 2015
# Author:   James Mills, prologic at shortcircuit dot net dot au

"""Utilities

Utility functions
"""


from __future__ import print_function

import sys
from hashlib import sha256 as sha


from requests import get


def log(msg):
    print(msg, file=sys.stderr)


def download(url):
    pass


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
def extractto(archive, output=None):
    output = output or getcwd()

    if any(archive.endswith(x) for x in [".tar.gz", ".tar.bz2"]):
        with TarFile(archive, "r:{0:s}".format(splitext(archive)[1][1:])) as f:
            f.extractall(output, [x for x in f.getmembers() if not path_exists(x)])
    elif archive.endswith(".zip"):
        with ZipFile(archive) as f:
            f.extractall(output, [x for x in f.namelist() if not path_exists(x)])
    elif archive.endswith(".gz"):
        outfile = path_join(output, splitext(archive)[0])
        if not path_exists(outfile):
            with GzipFile(archive, "rb") as f:
                with open(outfile, "wb") as of:
                    of.write(f.read())
    elif archive.endswith(".bz2"):
        outfile = path_join(output, splitext(archive)[0])
        if not path_exists(outfile):
            with BZ2File(archive, "rb") as f:
                with open(outfile, "wb") as of:
                    of.write(f.read())


def url2basename(url):
    return basename(urlsplit(url)[2])


def rsync(src, dest):
    parts = urlparse(src)
    if parts.netloc:
        if "@" in parts.netloc:
            user, host = parts.netloc.split("@", 1)
        else:
            user, host = "", parts.netloc

        options = "-o ssh {0:s}{1:s}".format(user, host)
    else:
        options = ""

    local("rsync --recursive --compress --stats --progress --human-readable {0:s} {1:s} {2:s}".format(options, src, dest))


def download(url, filename=None, md5=None, pwd=None, bs=8192):
    r = get(url, stream=True)

    if not filename:
        if "Content-Disposition" in r.headers:
            filename = r.headers["Content-Disposition"].split("filename=")[1]
            filename = filename.replace("\"", "").replace("'", "")

    if not filename:
        filename = url2basename(r.url)

    if pwd is not None and not isabs(filename):
        filename = path_join(pwd, filename)

    # Skip if an .md5 exists
    if md5 is not None:
        if path_exists("{0:s}.md5".format(filename)) and md5 == open("{0:s}.md5".format(filename), "r").read().strip():
            return
        else:
            open("{0:s}.md5".format(filename), "w").write(md5)
    else:
        try:
            x = get("{0:s}.md5".format(url))
            x.raise_for_status()
            if path_exists("{0:s}.md5".format(filename)) and x.content.strip() == open("{0:s}.md5".format(filename), "r").read().strip():
                return
            else:
                open("{0:s}.md5".format(filename), "w").write(x.content.strip())
        except:
            pass

    cl = int(r.headers.get("Content-Length", "0"))

    print "Downloading {0:s} Bytes: {1:d} ...".format(basename(filename), cl)
    with open(filename, "wb") as f:
        bar = ProgressBar(max=cl)
        for block in r.iter_content(bs):
            f.write(block)
            bar.next(bs)
        bar.finish()
    print
