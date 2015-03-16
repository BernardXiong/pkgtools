# Module:   pkgfile
# Date:     16th March 2015
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Pkgfile Parser"""


from os import path


from yaml import load


from ..utils import execute


PARSEPKGFILESH = path.join(path.dirname(__file__), "parsepkgfile.sh")


def parse(pkgfile):
    if pkgfile.is_absolute():
        return load(execute([PARSEPKGFILESH, pkgfile.name], cwd=str(pkgfile.parent)))
    else:
        return load(execute([PARSEPKGFILESH, pkgfile.name]))
