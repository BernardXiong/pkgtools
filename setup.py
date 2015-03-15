#!/usr/bin/env python


from setuptools import setup, find_packages


import pkg


setup(
    name=pkg.__name__,
    version=pkg.__version__,
    description=pkg.__doc__.split("\n")[0],
    long_description=open("README.rst", "r").read(),
    author="James Mills",
    author_email="James Mills, prologic at shortcircuit dot net dot au",
    url="https://github.com/vallinux/pkgtools",
    download_url="https://github.com/vallinux/pkgtools/releases",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    license="MIT",
    keywords="package manager",
    platforms="POSIX",
    packages=find_packages("."),
    install_requires=list(open("requirements.txt", "r")),
    entry_points={
        "console_scripts": [
            "pkg=pkg.main:main"
        ]
    },
    zip_safe=True
)
