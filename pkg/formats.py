import re
import shlex


class Package(object):
    """An abstract package class
    This class provides no functionality whatsoever. Use either
    :class:`PacmanPackage`, :class:`Pkgfile`, or another subclass instead.

    The class provides attributes common to all packages. All attributes are
    supposed to be read-only.

    .. attribute:: name

        The name of the package.

    .. attribute:: version

        The version of the package, as a string.

    .. attribute:: release

        Release version of the package, i.e., version of the package itself,
        as an integer.

    .. attribute:: description

        Description of the package.

    .. attribute:: url

        Package's website.

    .. attribute:: licenses

        A list of licenses.

    .. attribute:: groups

        A list of groups the package belongs to.

    .. attribute:: provides

        A list of "virtual provisions" that the package provides.

    .. attribute:: depends

        A list of the names of packages the package depends on.

    .. attribute:: optdepends

        A list of optional dependencies which are not required during runtime.

    .. attribute:: conflicts

        A list of packages the package conflicts with.

    .. attribute:: replaces

        A list of packages this package replaces.

    .. attribute:: architectures

        A list of architectures the package can be installed on.

    .. attribute:: backup

        A list of files which should be backed up on upgrades

    .. attribute:: options

        Options used when building the package, represented as a list. This
        list is equivalent to that of `options` in a Pkgfile. See
        :manpage:`Pkgfile(5)` for more information.

    For more information about these attributes see :manpage:`Pkgfile(5)`.

    """
    def __init__(self, pkgfile):
        super(Package, self).__init__()
        self.name = ""
        self.version = ""
        self.release = ""
        self.description = ""
        self.url = ""
        self.licenses = []
        self.groups = []
        self.provides = []
        self.depends = []
        self.optdepends = []
        self.conflicts = []
        self.replaces = []
        self.architectures = []
        self.options = []
        self.backup = []


class Pkgfile(Package):
    """A :manpage:`Pkgfile(5)` parser

    The :class:`Pkgfile` class provides information about a
    package by parsing a :manpage:`Pkgfile(5)` file.

    To instantiate a :class:`PacmanPackage` object, pass the package's file
    path in the constructor::

        >>> from pkg.formats import Pkgfile
        >>> package = Pkgfile("Pkgfile")

    If *fileobj* is specified, it is used as an alternative to a
    :class:`file` like object opened for *name*. It is supposed to be
    at position 0. For example::

        >>> f = open("Pkgfile", "r")
        >>> package = Pkgfile(fileobj=f)
        >>> f.close()

    .. note::

        *fileobj* is not closed.

    The packages metadata can then be accessed directly::

        >>> print package
        "foo 1.0-1"
        >>> print package.description
        "Example package"

    In addition to the attributes provided by :class:`Package`,
    :class:`Pkgfile` provides the following attributes:

    .. attribute:: install

        The filename of the install scriptlet.

    .. attribute:: checksums

        A dictionary containing the checksums of files in the
        :attr:`sources` list. The dictionary's keys are the algorithms
        used, and can be any of 'md5', 'sha1', 'sha256', 'sha384', and
        'sha512'. The value is a list of checksums. The elements
        correspond to files in the :attr:`sources` list, in relation to
        their position.

    .. attribute:: sources

        A list containing the URIs of filenames. Local file paths can be
        relative and do not require a protocol prefix.

    .. attribute:: makedepends

        A list of compile-time dependencies.

    .. attribute:: noextract

        A list of files not to be extracted. These files correspond to
        the basenames of the URIs in :attr:`sources`

    """
    _symbol_regex = re.compile(r"\$(?P<name>{[\w\d_]+}|[\w\d]+)")

    def __init__(self, name=None, fileobj=None):
        super(Pkgfile, self).__init__(fileobj)
        self.install = ""
        self.checksums = {
            'md5': [],
            'sha1': [],
            'sha256': [],
            'sha384': [],
            'sha512': [],
        }
        self.noextract = []
        self.sources = []
        self.makedepends = []

        # Symbol lookup table
        self._var_map = {
            'pkgname': 'name',
            'pkgver': 'version',
            'pkgdesc': 'description',
            'pkgrel': 'release',
            'source': 'sources',
            'arch': 'architectures',
            'license': 'licenses',
        }
        self._checksum_fields = (
            'md5sums',
            'sha1sums',
            'sha256sums',
            'sha384sums',
            'sha512sums',
        )
        # Symbol table
        self._symbols = {}

        if not name and not fileobj:
            raise ValueError("nothing to open")
        should_close = False
        if not fileobj:
            fileobj = open(name, "r")
            should_close = True
        self._parse(fileobj)
        if should_close:
            fileobj.close()

    def _handle_assign(self, token):
        var, equals, value = token.strip().partition('=')
        # Is it an array?
        if value[0] == '(' and value[-1] == ')':
            self._symbols[var] = self._clean_array(value)
        else:
            self._symbols[var] = self._clean(value)

    def _parse(self, fileobj):
        """Parse Pkgfile"""
        if hasattr(fileobj, "seek"):
            fileobj.seek(0)
        parser = shlex.shlex(fileobj, posix=True)
        parser.whitespace_split = True
        in_function = False
        while 1:
            token = parser.get_token()
            if token is None or token == '':
                break
            # Skip escaped newlines and functions
            if token == '\n' or in_function:
                continue
            # Special case:
            # Array elements are dispersed among tokens, we have to join
            # them first
            if token.find("=(") >= 0 and not token.rfind(")") >= 0:
                in_array = True
                elements = []
                while in_array:
                    _token = parser.get_token()
                    if _token == '\n':
                        continue
                    if _token[-1] == ')':
                        _token = '"%s")' % _token.strip(')')
                        token = token.replace('=(', '=("', 1) + '"'
                        token = " ".join((token, " ".join(elements), _token))
                        in_array = False
                    else:
                        elements.append('"%s"' % _token.strip())
            # Assignment
            if re.match(r"^[\w\d_]+=", token):
                self._handle_assign(token)
            # Function definitions
            elif token == '{':
                in_function = True
            elif token == '}' and in_function:
                in_function = False
        self._substitute()
        self._assign_local()
        if self.release:
            self.release = float(self.release)

    def _clean(self, value):
        """Pythonize a bash string"""
        return " ".join(shlex.split(value))

    def _clean_array(self, value):
        """Pythonize a bash array"""
        return shlex.split(value.strip('()'))

    def _replace_symbol(self, matchobj):
        """Replace a regex-matched variable with its value"""
        symbol = matchobj.group('name').strip("{}")
        # If the symbol isn't found fallback to an empty string, like bash
        try:
            value = self._symbols[symbol]
        except KeyError:
            value = ''
        # BUG: Might result in an infinite loop, oops!
        return self._symbol_regex.sub(self._replace_symbol, value)

    def _substitute(self):
        """Substitute all bash variables within values with their values"""
        for symbol in self._symbols:
            value = self._symbols[symbol]
            # FIXME: This is icky
            if isinstance(value, str):
                result = self._symbol_regex.sub(self._replace_symbol, value)
            else:
                result = [
                    self._symbol_regex.sub(self._replace_symbol, x)
                    for x in value
                ]
            self._symbols[symbol] = result

    def _assign_local(self):
        """Assign values from _symbols to Pkgfile variables"""
        for var in self._symbols:
            value = self._symbols[var]
            if var in self._checksum_fields:
                key = var.replace('sums', '')
                self.checksums[key] = value
            else:
                if var in self._var_map:
                    var = self._var_map[var]
                setattr(self, var, value)
