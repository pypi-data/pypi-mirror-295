from importlib.metadata import PackageNotFoundError, version  # pragma: no cover

# import custom classes into sdk package
from shapediver.geometry_api_v2.sd_client import SdClient

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
