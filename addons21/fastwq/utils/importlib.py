"""Backport of importlib.import_module from 3.x."""
# While not critical (and in no way guaranteed!), it would be nice to keep this
# code compatible with Python 2.3.
import sys

try:
    from importlib import reload
except:
    pass


def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, "rindex"):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in range(level, 1, -1):
        try:
            dot = package.rindex(".", 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level " "package")
    return f"{package[:dot]}.{name}"


def import_module(name, package=None):
    """Import a module.
    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.
    """
    if name.startswith("."):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != ".":
                break
            level += 1
        name = _resolve_name(name[level:], package, level)

    if name in sys.modules:
        reload(sys.modules[name])
    else:
        __import__(name)
    return sys.modules[name]
