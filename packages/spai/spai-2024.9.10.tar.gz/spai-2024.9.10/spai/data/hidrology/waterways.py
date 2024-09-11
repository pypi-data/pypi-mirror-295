"""
OpenStreetMapa data download module
"""

from typing import Optional, Union

import geopandas as gpd
import pandas as pd

from ..utils.osm import get_all_osm_elements


def download_waterways(
    storage,
    gdf: Union[str, gpd.GeoDataFrame],
    name: Optional[str] = "waterways.geojson",
    waterway_tags: Optional[dict] = {
        "waterway": ["river", "canal", "stream", "brook", "ditch", "drain"]
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
        The waterway tags to use, by default {'waterway': ['river', 'canal', 'stream', 'brook', 'ditch', 'drain']}

    Raises
    ------
    TypeError
        If the area of interest is not a GeoDataFrame or a filepath
    """
    if isinstance(gdf, str):
        gdf = gpd.read_file(gdf)
    elif not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("AoI must be a GeoDataFrame or a filepath")

    all_waterways = get_all_osm_elements(gdf, waterway_tags)
    if not all_waterways:
        print("No waterways found")
        return
    final_waterways_gdf = pd.concat(all_waterways, ignore_index=True)
    final_waterways_gdf = final_waterways_gdf[["geometry"]]
    final_waterways_gdf = final_waterways_gdf[
        final_waterways_gdf.geometry.type.isin(("LineString", "MultiLineString"))
    ]
    storage.create(final_waterways_gdf, name=name)
