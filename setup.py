#!/usr/bin/env python


from setuptools import find_packages, setup


import pkg


def main():
    setup(
        name=pkg.__name__,
        version=pkg.__version__,
        packages=find_packages(),
        entry_points={
            "console_scripts": [
                "pkg=pkg.main:main",
            ]
        }
    )


if __name__ == "__main__":
    main()
