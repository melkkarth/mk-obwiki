from importlib.metadata import version, PackageNotFoundError

from mk_obwiki.plugin import ObWikiPlugin

try:
    __version__ = version("mk-obwiki")
except PackageNotFoundError:
    pass
