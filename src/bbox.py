import os
import geopandas as gpd
from src.config import log, settings
from shapely.geometry import Polygon


def create_bounding_box(save_file_path: str, latitudes: list, 
                        longitudes: list, crs: str): 
    """Create a bounding box from sets of longitude and latitude coordinates, and save as geopackage.

    Parameters
    ----------
    save_file_path : str
        Full or relative path with filename and ending to which output (should be saved to.
    latitudes : list
        List of coordinates. Same order as 'latitudes' parameter
    longitudes : list
        List of coordinates. Same order as 'longitudes' parameter
    crs : str
        Coordinate reference system id. E.g., '32610'

    Returns
    -------
    None

    """

    if os.path.exists(save_file_path):
        log.success('Bounding box file exists. Skipping bounding box creation')
        return

    polygon_geom = Polygon(zip(longitudes, latitudes))
    crs = f'EPSG:{crs}'
    polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_geom])       
    polygon.to_file(filename=save_file_path, driver='GPKG', layer='name')
