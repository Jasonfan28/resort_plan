"""Shared live-data access: City of Revelstoke ArcGIS FeatureServers and
the ParcelMap BC WFS. Used by steps 07 and 10.
"""

import geopandas as gpd
import requests

CITY_ARCGIS_BASE = "https://services8.arcgis.com/td7Y0VOEClDw7sGk/arcgis/rest/services"
PARCELMAP_BC_WFS = "https://openmaps.gov.bc.ca/geo/pub/WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW/ows"
PARCELMAP_BC_TYPENAME = "pub:WHSE_CADASTRE.PMBC_PARCEL_FABRIC_POLY_SVW"


def fetch_city_layer(service_name, layer=0, where="1=1", envelope=None, out_sr=26911, page_size=2000):
    """Paginated fetch from a City of Revelstoke ArcGIS FeatureServer layer.

    envelope, if given, is (minx, miny, maxx, maxy) in out_sr, used to
    restrict the query to features intersecting that box.
    """
    url = f"{CITY_ARCGIS_BASE}/{service_name}/FeatureServer/{layer}/query"
    params = {
        "where": where,
        "outFields": "*",
        "f": "geojson",
        "outSR": out_sr,
        "resultRecordCount": page_size,
    }
    if envelope is not None:
        minx, miny, maxx, maxy = envelope
        params.update({
            "geometry": f"{minx},{miny},{maxx},{maxy}",
            "geometryType": "esriGeometryEnvelope",
            "spatialRel": "esriSpatialRelIntersects",
            "inSR": out_sr,
        })
    features = []
    offset = 0
    while True:
        params["resultOffset"] = offset
        r = requests.get(url, params=params, timeout=60)
        r.raise_for_status()
        batch = r.json().get("features", [])
        features.extend(batch)
        if len(batch) < page_size:
            break
        offset += len(batch)
    if not features:
        return gpd.GeoDataFrame()
    return gpd.GeoDataFrame.from_features(features, crs=f"EPSG:{out_sr}")


def fetch_parcelmap_bc(cql_filter, out_crs="EPSG:26911", page_size=2000):
    """Paginated fetch from the province-wide ParcelMap BC WFS, filtered
    by a CQL_FILTER string (e.g. "MUNICIPALITY='Revelstoke, City of'").
    Requires sortBy for pagination: the service has no natural feature
    order without one.
    """
    params = {
        "service": "WFS", "version": "2.0.0", "request": "GetFeature",
        "typeNames": PARCELMAP_BC_TYPENAME, "outputFormat": "json",
        "srsName": out_crs, "CQL_FILTER": cql_filter,
        "count": page_size, "sortBy": "PARCEL_FABRIC_POLY_ID",
    }
    features = []
    start = 0
    while True:
        params["startIndex"] = start
        r = requests.get(PARCELMAP_BC_WFS, params=params, timeout=60)
        r.raise_for_status()
        batch = r.json().get("features", [])
        features.extend(batch)
        if len(batch) < page_size:
            break
        start += len(batch)
    if not features:
        return gpd.GeoDataFrame()
    return gpd.GeoDataFrame.from_features(features, crs=out_crs)
