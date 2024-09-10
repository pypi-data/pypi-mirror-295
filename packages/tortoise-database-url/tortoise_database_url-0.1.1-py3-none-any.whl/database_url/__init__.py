import importlib.metadata as importlib_metadata

from ._main import DatabaseUrlError, InvalidEngine, from_django_item, generate

try:
    __version__ = importlib_metadata.version(__name__)
except importlib_metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = "0.1.0"

__all__ = (
    "__version__",
    "generate",
    "from_django_item",
    "InvalidEngine",
    "DatabaseUrlError",
)


# Re-export imports so they look like they live directly in this package
for __value in list(locals().values()):
    if getattr(__value, "__module__", "").startswith("database_url."):
        __value.__module__ = __name__

del __value
