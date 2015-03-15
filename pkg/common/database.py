'''
    common.package Module

    License TBD

'''
import json
import os
from os import path
from tempfile import NamedTemporaryFile as TempFile


class Database(object):
    '''
        Class for interacting with the package
        database.

        At the moment database file is simply a 
        list of installed packages. Should probably become
        an sqlite database though.

        @todo: consider making this class work with `with`
            eg.
                with x as d:
                    do stuff
                auto-commit & cleanup

    '''

    def __init__(self, filename):
        self.filename = path.abspath(filename)
        self._load()

    def add(self, package):
        '''
            Add a package to the database.
        '''
        if package in self:

            if self.contains(package, version=True):
                raise ValueError("Given version of %s is already installed." % package.name)
            else:
                self._database[package.name] = package
        else:
            self._database[package.name] = package

    def remove(self, package, version=False):
        '''
            Remove a package from the database.

            if version is true, only remove if 
            the given version is installed
        '''
        if self.contains(package, version=version):
            del self._database[package]

        else:
            if version:
                msg = "Package %s at version %s is not installed." % (package.name, package.version)
                raise ValueError(msg)
            else:
                raise ValueError("Package %s is not installed." % package.version)


    def contains(self, package, version=False):
        '''
            Check for a package by name.

            if version is true, ensure the given 
            version is installed.
        '''
        pkg = self._database.get(package.name, False)

        if pkg and not version:
            return bool(pkg)

        elif pkg:
            return pkg.version is package.version

        return False

    def commit(self):
        '''
            Save the various add and remove operations performed.
        '''
        self._write_replace_save()

    def rollback(self):
        '''
            Reload our _database from the fs.
        '''
        self._load()

    def _load(self):
        '''
            Load the list of packages from the db
        '''
        with open(self.filename) as db_file:
            self._database = json.load(db_file)

    def _write_replace_save(self):
        '''
            Uses a Write-replace pattern
        '''
        with TempFile('w', dir=path.dirname(self.filename), delete=False) as tmp_file:
            tmp_file.write(json.dump(self._database, tmp_file))
            tempname = tmp_file.name

        os.rename(tempname, self.filename)

    def __enter__(self):
        return self

    def __exit__(self, ex_type, value, trace):
        if ex_type is None:
            self.commit()
        else:
            self.rollback()

    def __contains__(self, package):
        return self.contains(package)
