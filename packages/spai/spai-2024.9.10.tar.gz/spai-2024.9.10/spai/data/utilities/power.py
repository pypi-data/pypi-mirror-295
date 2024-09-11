from typing import Optional, Union

import geopandas as gpd
import pandas as pd

from ..utils.osm import get_all_osm_elements


def download_power_networks(
    storage,
    gdf: Union[str, gpd.GeoDataFrame],
    line_name: Optional[str] = "power_lines.geojson",
    point_name: Optional[str] = "power_points.geojson",
    polygon_name: Optional[str] = "power_polygons.geojson",
    power_tags: Optional[dict] = {
        "power": ["line", "cable", "substation", "plant", "transformer"]
    },
) -> None:
    """
    Download power network elements from OpenStreetMap for the given area of interest and separate them by geometry type.

    Parameters
    ----------
    gdf : Union[str, gpd.GeoDataFrame]
        The area of interest
    storage : BaseStorage
        The storage object
    line_name : str, optional
        The name of the file to store line geometries, by default "power_lines.geojson"
    point_name : str, optional
        The name of the file to store point geometries, by default "power_points.geojson"
    polygon_name : str, optional
        The name of the file to store polygon geometries, by default "power_polygons.geojson"
    power_tags : dict, optional
        The power tags to use, by default includes power lines, cables, substations, plants, and transformers.

    Raises
    ------
    TypeError
        If the area of interest is not a GeoDataFrame or a filepath
    """
    if isinstance(gdf, str):
        gdf = gpd.read_file(gdf)
    elif not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("AoI must be a GeoDataFrame or a filepath")

    all_power_networks = get_all_osm_elements(gdf, power_tags)
    if not all_power_networks:
        print("No power network elements found")
        return

    final_power_networks_gdf = pd.concat(all_power_networks, ignore_index=True)

    # Filter by geometry type
    lines_gdf = final_power_networks_gdf[
        final_power_networks_gdf.geometry.type.isin(("LineString", "MultiLineString"))
    ]
    points_gdf = final_power_networks_gdf[
        final_power_networks_gdf.geometry.type.isin(("Point", "MultiPoint"))
    ]
    polygons_gdf = final_power_networks_gdf[
        final_power_networks_gdf.geometry.type.isin(("Polygon", "MultiPolygon"))
    ]

    # Clean each GeoDataFrame to remove any invalid field types (e.g., lists)
    lines_gdf = lines_gdf.applymap(lambda x: x if not isinstance(x, list) else str(x))
    points_gdf = points_gdf.applymap(lambda x: x if not isinstance(x, list) else str(x))
    polygons_gdf = polygons_gdf.applymap(
        lambda x: x if not isinstance(x, list) else str(x)
    )

    # Store the filtered geometries
    if not lines_gdf.empty:
        storage.create(lines_gdf, name=line_name)
    if not points_gdf.empty:
        storage.create(points_gdf, name=point_name)
    if not polygons_gdf.empty:
        storage.create(polygons_gdf, name=polygon_name)
