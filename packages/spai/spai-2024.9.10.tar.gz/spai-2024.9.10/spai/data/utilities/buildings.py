"""
OpenStreetMapa data download module
"""

from typing import Optional, Union

import geopandas as gpd
import osmnx as ox
import pandas as pd


def download_buildings(
    storage,
    gdf: Union[str, gpd.GeoDataFrame],
    name: Optional[str] = "buildings.geojson",
) -> None:
    """
    Download the buildings from OpenStreetMap for the given area of interest

    Parameters
    ----------
    aoi : Union[str, gpd.GeoDataFrame]
        The area of interest
    storage : BaseStorage
        The storage object

    Raises
    ------
    TypeError
        If the area of interest is not a GeoDataFrame or a filepath
    """
    if isinstance(gdf, str):
        gdf = gpd.read_file(gdf)
    elif not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("AoI must be a GeoDataFrame or a filepath")

    all_buildings = []

    for _, row in gdf.iterrows():
        polygon = row.geometry

        try:
            buildings_gdf = ox.features_from_polygon(polygon, tags={"building": True})
        except ox._errors.InsufficientResponseError:
            continue

        all_buildings.append(buildings_gdf)

    if not all_buildings:
        print("No buildings found")
        return

    final_buildings_gdf = pd.concat(all_buildings, ignore_index=True)
    final_buildings_gdf = final_buildings_gdf[["geometry"]]
    final_buildings_gdf = final_buildings_gdf[
        final_buildings_gdf.geometry.type.isin(("Polygon", "MultyPolygon"))
    ]
    final_buildings_gdf.to_crs(epsg=4326, inplace=True)
    storage.create(final_buildings_gdf, name=name)
