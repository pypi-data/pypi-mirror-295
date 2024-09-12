from rasterio import RasterioIOError


class EarthscaleError(Exception):
    """Base class for exceptions in this module."""

    pass


class RasterFileNotFoundError(EarthscaleError):
    """Raised when a file is not found"""

    pass


def convert_rasterio_to_earthscale(
    e: RasterioIOError,
) -> RasterioIOError | EarthscaleError:
    """Handle rasterio IO errors."""
    if "No such file or directory" in e.args[0]:
        return RasterFileNotFoundError(e.args[0])
    return e
