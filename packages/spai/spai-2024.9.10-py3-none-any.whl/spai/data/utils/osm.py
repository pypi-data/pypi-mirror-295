"""
OpenStreetMapa data download module
"""

from typing import List

import geopandas as gpd
import osmnx as ox
from shapely.validation import make_valid


def get_all_osm_elements(gdf: gpd.GeoDataFrame, tags: dict) -> List:
    """
    Iterate over a given AOI GeoDataFrame and get all the desired OSM elements defined in the tags

    Parameters
    ----------
    gdf: gpd.GeoDataFrame
        The GeoDataFrame of the Area of Interest
    tags: dict
        Dict with the OSM tags of the elements to download

    Returns
    -------
    all_elements: List
        List with all the required elements
    """
    all_elements = []

    for _, row in gdf.iterrows():
        # create polygon from row as shapely.geometry.Polygon
        polygon = row.geometry
        if not polygon.is_valid:
            polygon = make_valid(polygon)

        for key, values in tags.items():
            if isinstance(values, list):
                for value in values:
                    try:
                        waterway_gdf = ox.features_from_polygon(
                            polygon, tags={key: value}
                        )
                        all_elements.append(waterway_gdf)
                    except ox._errors.InsufficientResponseError:
                        continue
            else:
                try:
                    waterway_gdf = ox.features_from_polygon(polygon, tags={key: values})
                    all_elements.append(waterway_gdf)
                except ox._errors.InsufficientResponseError:
                    continue

    return all_elements
