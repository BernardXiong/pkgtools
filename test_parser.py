#!/usr/bin/env python


from __future__ import print_function

from pprint import pprint


from pkg.parsers import parse_pkgfile


data = parse_pkgfile("Pkgfile")
pprint(data)
