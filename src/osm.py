import os
import osmnx
from src.config import log, settings


def get_osm_street_data(place: str, 
                        save_file_path: str, 
                        network_type: str = "drive", 
                        simplify: bool = False):
    """Download street data from OpenStreetMap

    This function retrieves vector data from OpenStreetMap. Some parameters are retrieved from the configuration file for this solution (config.py).

    Parameters (also available in docstring for osmnx.graph_from_place method)
    ----------
    place : str
        The place to download data for. Must be a real place and geocodable by OSMNX.
    network_type : str
        The type of road network to retrieve. 
    simplify : bool
        Simplifies data a little bit. 
    save_file_path : str
        Path to file to which downloaded vector data should be save to.

    Returns
    -------
    None

    """

    # Check if file already exists
    if os.path.exists(save_file_path):
        log.success("File exists. Skipping download of OSM data.")
        return

    # Retrieve and set basic osmnx settings
    use_cache=settings.osmnx_use_cache
    log_console=settings.osmnx_log_console
    osmnx.config(use_cache=use_cache, log_console=log_console)

    # Download street data from openstreetmap
    data = osmnx.graph_from_place(place, network_type=network_type, simplify=simplify)
    _, roads = osmnx.graph_to_gdfs(data)
    roads.to_file(save_file_path, driver='GPKG')
