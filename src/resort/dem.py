"""Shared DEM access: windowed HRDEM reads and slope/aspect.

Used by steps 04, 07, and 10. Step 03 has its own inline copy of this
logic, written before this module existed; not retrofitted since that
notebook already passed review, but any further DEM-touching notebook
should use this instead of copying the code again.
"""

import numpy as np
import pyproj
import rioxarray
from shapely.geometry import box
from shapely.ops import transform as shp_transform

HRDEM_1M_DTM_URL = (
    "https://canelevation-dem.s3.ca-central-1.amazonaws.com/"
    "hrdem-mosaic-1m/2_4-mosaic-1m-dtm.tif"
)
DEM_NATIVE_CRS = "EPSG:3979"


def clip_dem(bounds, project_crs, buffer_m=200, url=HRDEM_1M_DTM_URL):
    """Windowed HRDEM read (HTTP range requests, no full-tile download),
    clipped to a bounding box (in project_crs) plus a buffer, then
    reprojected once to project_crs. bounds is (minx, miny, maxx, maxy).
    """
    to_native = pyproj.Transformer.from_crs(project_crs, DEM_NATIVE_CRS, always_xy=True).transform
    bounds_native = shp_transform(to_native, box(*bounds)).bounds
    nminx, nminy, nmaxx, nmaxy = bounds_native

    dem_full = rioxarray.open_rasterio(url, masked=True)
    clipped = dem_full.rio.clip_box(
        minx=nminx - buffer_m, miny=nminy - buffer_m,
        maxx=nmaxx + buffer_m, maxy=nmaxy + buffer_m,
    )
    return clipped.rio.reproject(project_crs)


def compute_slope_aspect(dem_da):
    """Slope (degrees and percent) and aspect (degrees, 0=north) from a
    reprojected DEM DataArray, via a simple finite-difference gradient.
    """
    arr = dem_da.values[0]
    res_x, res_y = (abs(r) for r in dem_da.rio.resolution())
    grad_y, grad_x = np.gradient(arr, res_y, res_x)
    slope_deg = np.degrees(np.arctan(np.sqrt(grad_x**2 + grad_y**2)))
    slope_pct = np.tan(np.radians(slope_deg)) * 100
    aspect_deg = np.degrees(np.arctan2(grad_y, -grad_x)) % 360
    return slope_deg, slope_pct, aspect_deg


def sample_at_point(array, x, y, affine):
    """Nearest-pixel lookup at a project-CRS coordinate. Returns NaN for
    points outside the array (e.g. outside a clip window).
    """
    col, row = ~affine * (x, y)
    row, col = int(row), int(col)
    if 0 <= row < array.shape[0] and 0 <= col < array.shape[1]:
        return array[row, col]
    return np.nan


def aspect_class(aspect_deg, n_classes=4):
    """Bin an aspect (degrees) into n_classes compass directions (4 or 8).
    Returns a label like "N", "NE", etc.
    """
    if n_classes == 4:
        labels = ["N", "E", "S", "W"]
    elif n_classes == 8:
        labels = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    else:
        raise ValueError("n_classes must be 4 or 8")
    width = 360 / n_classes
    idx = int(((aspect_deg + width / 2) % 360) // width)
    return labels[idx]
