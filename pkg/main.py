#!/usr/bin/env python


from __future__ import print_function


from requests import get


def main():
    res = get("http://www.google.com/robots.txt")
    res.raise_for_status()

    print(res.content)


if __name__ == "__main__":
    main()
