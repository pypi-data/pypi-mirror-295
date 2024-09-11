from typing import Optional, Union

import geopandas as gpd
import pandas as pd

from ..utils.osm import get_all_osm_elements


def download_pipelines(
    storage,
    gdf: Union[str, gpd.GeoDataFrame],
    name: Optional[str] = "pipelines_lines.geojson",
    pipeline_tags: Optional[dict] = {
        "man_made": ["pipeline"],
        "pipeline": ["oil", "gas", "water", "sewage", "heat"],
    },
) -> None:
    """
    Download pipeline (oleoductos) elements from OpenStreetMap for the given area of interest.

    Parameters
    ----------
    gdf : Union[str, gpd.GeoDataFrame]
        The area of interest
    storage : BaseStorage
        The storage object
    name : str, optional
        The name of the file to store line geometries, by default "pipelines_lines.geojson"
    pipeline_tags : dict, optional
        The pipeline tags to use, by default includes pipelines for oil, gas, water, sewage, and heat.

    Raises
    ------
    TypeError
        If the area of interest is not a GeoDataFrame or a filepath
    """
    if isinstance(gdf, str):
        gdf = gpd.read_file(gdf)
    elif not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("AoI must be a GeoDataFrame or a filepath")

    all_pipelines = get_all_osm_elements(gdf, pipeline_tags)
    if not all_pipelines:
        print("No pipeline elements found")
        return

    final_pipelines_gdf = pd.concat(all_pipelines, ignore_index=True)

    # Filter for LineString and MultiLineString geometries (pipelines are lines)
    lines_gdf = final_pipelines_gdf[
        final_pipelines_gdf.geometry.type.isin(("LineString", "MultiLineString"))
    ]

    # Clean the GeoDataFrame to remove any invalid field types (e.g., lists)
    lines_gdf = lines_gdf.applymap(lambda x: x if not isinstance(x, list) else str(x))

    # Store the line geometries
    if not lines_gdf.empty:
        storage.create(lines_gdf, name=name)
