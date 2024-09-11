def with_rio(func):
    def wrapper(self, *args, **kwargs):
        try:
            import rasterio as rio

            return func(self, rio, *args, **kwargs)
        except ImportError:
            raise ImportError(
                "The rasterio package is required for this function. Please install it with 'pip install rasterio' and try again."
            )

    return wrapper


def with_pyarrow(func):
    def wrapper(self, *args, **kwargs):
        try:
            import pyarrow as pa

            return func(self, pa, *args, **kwargs)
        except ImportError:
            raise ImportError(
                "The pyarrow package is required for this function. Please install it with 'pip install pyarrow' and try again."
            )

    return wrapper


def with_s3fs(func):
    def wrapper(self, *args, **kwargs):
        try:
            import s3fs

            return func(self, s3fs, *args, **kwargs)
        except ImportError:
            raise ImportError(
                "The s3fs package is required for this function. Please install it with 'pip install s3fs' and try again."
            )

    return wrapper


def with_xarray(func):
    def wrapper(self, *args, **kwargs):
        try:
            import xarray as xr

            return func(self, xr, *args, **kwargs)
        except ImportError:
            raise ImportError(
                "The xarray package is required for this function. Please install it with 'pip install xarray' and try again."
            )

    return wrapper


def with_geopandas(func):
    def wrapper(self, *args, **kwargs):
        try:
            import geopandas as gpd

            return func(self, gpd, *args, **kwargs)
        except ImportError:
            raise ImportError(
                "The geopandas package is required for this function. Please install it with 'pip install geopandas' and try again."
            )

    return wrapper


def with_rioxarray(func):
    def wrapper(self, *args, **kwargs):
        try:
            import rioxarray as rxr

            return func(self, rxr, *args, **kwargs)
        except ImportError:
            raise ImportError(
                "The rioxarray package is required for this function. Please install it with 'pip install rioxarray' and try again."
            )

    return wrapper
