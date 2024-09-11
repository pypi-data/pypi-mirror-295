"""
OpenStreetMapa data download module
"""

from typing import Optional, Union

import geopandas as gpd
import pandas as pd

from ..utils.osm import get_all_osm_elements


def download_roads(
    storage,
    gdf: Union[str, gpd.GeoDataFrame],
    name: Optional[str] = "roads.geojson",
    waterway_tags: Optional[dict] = {
        "highway": ["motorway", "trunk", "primary", "secondary", "tertiary"]
    },
) -> None:
    """
    Download the waterways from OpenStreetMap for the given area of interest

    Parameters
    ----------
    aoi : Union[str, gpd.GeoDataFrame]
        The area of interest
    storage : BaseStorage
        The storage object
    waterway_tags : dict, optional
        The waterway tags to use, by default {'highway': ['motorway', 'trunk', 'primary', 'secondary', 'tertiary']}

    Raises
    ------
    TypeError
        If the area of interest is not a GeoDataFrame or a filepath
    """
    if isinstance(gdf, str):
        gdf = gpd.read_file(gdf)
    elif not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("AoI must be a GeoDataFrame or a filepath")

    all_roads = get_all_osm_elements(gdf, waterway_tags)

    if not all_roads:
        print("No roads found")
        return

    final_roads_gdf = pd.concat(all_roads, ignore_index=True)
    final_roads_gdf = final_roads_gdf[["geometry"]]
    final_roads_gdf = final_roads_gdf[
        final_roads_gdf.geometry.type.isin(("LineString", "MultiLineString"))
    ]
    storage.create(final_roads_gdf, name=name)
